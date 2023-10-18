import re
from fastapi import Body, Request
from fastapi.responses import StreamingResponse
from configs import (LLM_MODEL, VECTOR_SEARCH_TOP_K, SCORE_THRESHOLD, TEMPERATURE)
from server.utils import wrap_done, get_ChatOpenAI
from server.utils import BaseResponse, get_prompt_template
from langchain.chains import LLMChain
from langchain.callbacks import AsyncIteratorCallbackHandler
from typing import AsyncIterable, List, Optional
import asyncio
from langchain.prompts.chat import ChatPromptTemplate
from server.chat.utils import History
from server.knowledge_base.kb_service.base import KBService, KBServiceFactory
import json
import os
from urllib.parse import urlencode
from server.knowledge_base.kb_doc_api import search_docs

async def sql_search(query: str = Body(..., description="用户输入", examples=["你好"]),
                knowledge_base_name: str = Body(..., description="知识库名称", examples=["samples"]),
                top_k: int = Body(VECTOR_SEARCH_TOP_K, description="匹配向量数"),
                score_threshold: float = Body(SCORE_THRESHOLD, description="知识库匹配相关度阈值，取值范围在0-1之间，SCORE越小，相关度越高，取到1相当于不筛选，建议设置在0.5左右", ge=0, le=1),
                local_doc_url: bool = Body(False, description="知识文件返回本地路径(true)或URL(false)"),
                request: Request = None,
            ):
    kb = KBServiceFactory.get_service_by_name(knowledge_base_name)
    if kb is None:
        return BaseResponse(code=404, msg=f"未找到知识库 {knowledge_base_name}")


    async def sql_search_iterator(query: str,
                                top_k: int,
                                ) -> AsyncIterable[str]:
        docs = search_docs(query, knowledge_base_name, top_k, score_threshold)
        context = "\n".join([doc.page_content for doc in docs])

        source_documents = []
        for inum, doc in enumerate(docs):
            filename = os.path.split(doc.metadata["source"])[-1]
            if local_doc_url:
                url = "file://" + doc.metadata["source"]
            else:
                parameters = urlencode({"knowledge_base_name": knowledge_base_name, "file_name":filename})
                url = f"{request.base_url}knowledge_base/download_doc?" + parameters
            text = f"""出处 [{inum + 1}] [{filename}]({url}) \n\n{doc.page_content}\n\n"""
            source_documents.append(text)
        yield json.dumps({"answer": "我已经找到了相关SQL案例","docs": source_documents,"doc": [context]}, ensure_ascii=False)


    return StreamingResponse(sql_search_iterator(query=query,
                                                top_k=top_k,),
                             media_type="text/event-stream")

async def sql_chat( query: str = Body(..., description="用户输入", examples=["你好"]),
                    knowledge_data: str = Body(..., description="知识库数据", examples=["你好"]),
                    history: List[History] = Body([],
                                description="历史对话",
                                examples=[[
                                    {"role": "user",
                                    "content": "我们来玩成语接龙，我先来，生龙活虎"},
                                    {"role": "assistant",
                                    "content": "虎头虎脑"}]]
                                ),
                    stream: bool = Body(False, description="流式输出"),
                    model_name: str = Body(LLM_MODEL, description="LLM 模型名称。"),
                    temperature: float = Body(TEMPERATURE, description="LLM 采样温度", ge=0.0, le=1.0),
                    prompt_name: str = Body("knowledge_base_chat", description="使用的prompt模板名称(在configs/prompt_config.py中配置)"),
                    local_doc_url: bool = Body(False, description="知识文件返回本地路径(true)或URL(false)"),
                    request: Request = None,
            ):

    history = [History.from_data(h) for h in history]

    async def sql_chat_iterator(query: str,
                                knowledge_data: str,
                                history: Optional[List[History]],
                                model_name: str = LLM_MODEL,
                                prompt_name: str = prompt_name,
                                ) -> AsyncIterable[str]:
        callback = AsyncIteratorCallbackHandler()
        model = get_ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            callbacks=[callback],
        )
        context = "\n".join([knowledge_data])
        print("context:" ,context)
        tables = re.findall(r'from (\w+)', context, re.I)  # re.I 让搜索变得不区分大小写
        tables += re.findall(r'join (\w+)', context, re.I)
        tables = list(set(tables))
        print("tables:", tables)
        schema = ""
        for table in tables:
            table_path = "/modelFactory/poolwdy/Demo/new_table_info/" + table + ".sql"
            if os.path.exists(table_path):
                with open(table_path, 'r', encoding='utf-8') as f:
                    lines = f.read()
            else:
                print(f"File {table_path} does not exist!")
            schema += lines
            schema += '\n'
        prompt_template = get_prompt_template("sql_chat", prompt_name)
        print("prompt_template:", prompt_template)
        input_msg = History(role="user", content=prompt_template).to_msg_template(False)
        chat_prompt = ChatPromptTemplate.from_messages(
            [i.to_msg_template() for i in history] + [input_msg])

        chain = LLMChain(prompt=chat_prompt, llm=model)

        # Begin a task that runs in the background.
        task = asyncio.create_task(wrap_done(
            chain.acall({"tables_used": str(tables),"table_schema": str(schema),"few_shot": str(context), "question": query}),
            callback.done),
        )

        

        if stream:
            async for token in callback.aiter():
                # Use server-sent-events to stream the response
                yield json.dumps({"answer": token}, ensure_ascii=False)
        else:
            answer = ""
            async for token in callback.aiter():
                answer += token
            yield json.dumps({"answer": answer},
                             ensure_ascii=False)

        await task

    return StreamingResponse(sql_chat_iterator(query=query,
                                            knowledge_data=knowledge_data,
                                            history=history,
                                            model_name=model_name,
                                            prompt_name=prompt_name),
                             media_type="text/event-stream")

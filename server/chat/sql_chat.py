import re
from fastapi import Body, Request
from fastapi.responses import StreamingResponse
from sqlalchemy import Connection
from configs import (LLM_MODELS, VECTOR_SEARCH_TOP_K, SCORE_THRESHOLD, TEMPERATURE)
from server.utils import wrap_done, get_ChatOpenAI
from server.utils import BaseResponse, get_prompt_template
from langchain.chains import LLMChain
from langchain.callbacks import AsyncIteratorCallbackHandler
from typing import AsyncIterable, List, Optional
import asyncio
from langchain.prompts.chat import ChatPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from server.chat.utils import History
from server.knowledge_base.kb_service.base import KBService, KBServiceFactory
import json
import os
from urllib.parse import urlencode
from server.knowledge_base.kb_doc_api import search_docs
def extract_sql_from_markdown(md_string):
    pattern = r"```sql([\s\S]*?)```"
    match = re.findall(pattern, md_string)
    sql = ''
    if match:
        sql = match[-1].replace('\n', ' ').strip()
        if sql[-1] != ';':
            sql = sql + ';'
    return sql
async def zhipu_chat(query, answer):
    model = get_ChatOpenAI(
        model_name='zhipu-api',
        temperature=0.0,
        max_tokens=2048,
    )
    prompt = """
    问题：{query}
    目前的sql语句：{answer}
    你需要分析现有的sql是不是完全符合问题的要求，如果不符合请修复并给出修复后的sql，如果符合请复述原来的sql
    只需要按照下面的格式输出结果
    ```sql
    符合要求的sql语句
    ```
    只需输出sql，无需解释。
    """
    chain = LLMChain(prompt=PromptTemplate.from_template(prompt), llm=model)
    response = await chain.acall({"query": query, "answer":answer})
    return response['text']
async def sql_search(query: str = Body(..., description="用户输入", examples=["你好"]),
                knowledge_base_name: str = Body(..., description="知识库名称", examples=["samples"]),
                top_k: int = Body(VECTOR_SEARCH_TOP_K, description="匹配向量数"),
                score_threshold: float = Body(SCORE_THRESHOLD, description="知识库匹配相关度阈值，取值范围在0-1之间，SCORE越小，相关度越高，取到1相当于不筛选，建议设置在0.5左右", ge=0, le=1),
                model_name: str = Body(LLM_MODELS[0], description="LLM 模型名称。"),
                stream: bool = Body(False, description="流式输出"),
                temperature: float = Body(TEMPERATURE, description="LLM 采样温度", ge=0.0, le=1.0),
                max_tokens: int = Body(None, description="限制LLM生成Token数量，默认None代表模型最大值"),
                request: Request = None,
            ):
    kb = KBServiceFactory.get_service_by_name(knowledge_base_name)
    if kb is None:
        return BaseResponse(code=404, msg=f"未找到知识库 {knowledge_base_name}")


    async def sql_search_iterator(query: str,
                                top_k: int,
                                model_name: str = LLM_MODELS[0],
                                ) -> AsyncIterable[str]:
        docs = search_docs(query, knowledge_base_name, top_k, score_threshold)
        context = "\n".join([doc.page_content for doc in docs])
        to_move = ["{'query': '", "', 'script': ", "}"]
        # context = context.replace("\\", "")
        context = context.replace("{'query': '", "\n问题：")
        context = context.replace("', 'script': \"", "\n答案：")
        context = context.replace("\"}", "\n")
        callback = AsyncIteratorCallbackHandler()
        model = get_ChatOpenAI(
            model_name="zhipu-api",
            temperature=temperature,
            max_tokens=max_tokens,
            callbacks=[callback],
        )
        prompt_template = get_prompt_template("sql_chat", "select_table_simplified")
        input_msg = History(role="user", content=prompt_template).to_msg_template(False)
        chat_prompt = ChatPromptTemplate.from_messages([input_msg])
        chain = LLMChain(prompt=chat_prompt, llm=model)
        # Begin a task that runs in the background.
        task = asyncio.create_task(wrap_done(
            chain.acall({"question": query,"context": context}),
            callback.done),
        )
        source_documents = []
        for inum, doc in enumerate(docs):
            filename = os.path.split(doc.metadata["source"])[-1]
            parameters = urlencode({"knowledge_base_name": knowledge_base_name, "file_name":filename})
            url = f"{request.base_url}knowledge_base/download_doc?" + parameters
            context = doc.page_content
            context = context.replace("{'query': '", "\n问题：")
            context = context.replace("', 'script': \"", "\n答案：")
            context = context.replace("\"}", "\n")
            text = f"""出处 [{inum + 1}] [{filename}]({url}) \n\n{context}\n\n"""
            source_documents.append(text)
        
        if stream:
            answer = ""
            async for token in callback.aiter():
                # Use server-sent-events to stream the response
                answer += token
                yield json.dumps({"answer": token}, ensure_ascii=False)
            yield json.dumps({"docs": source_documents,"doc": [context]}, ensure_ascii=False)
        else:
            answer = ""
            async for token in callback.aiter():
                answer += token
            yield json.dumps({"answer": answer,"docs": source_documents,"doc": [context]},
                             ensure_ascii=False)
        await task


    return StreamingResponse(sql_search_iterator(query=query,
                                                top_k=top_k,
                                                model_name=model_name,),
                             media_type="text/event-stream")

async def sql_execute(sql: str = Body(..., description="用户输入", examples=["你好"]), 
                    sql_result: str = Body(..., description="用户输入", examples=["你好"]),
                    prompt: str = Body(..., description="上一步的提示信息", examples=["你好"]),
                    stream: bool = Body(False, description="流式输出"),
                    model_name: str = Body(LLM_MODELS[0], description="LLM 模型名称。"),
                    temperature: float = Body(TEMPERATURE, description="LLM 采样温度", ge=0.0, le=1.0),
                    max_tokens: int = Body(None, description="限制LLM生成Token数量，默认None代表模型最大值"),
            ):
    async def sql_execute_iterator(sql: str,
                                sql_result: str,
                                prompt: str,
                                model_name: str = LLM_MODELS[0],
                                ) -> AsyncIterable[str]:
        callback = AsyncIteratorCallbackHandler()
        model = get_ChatOpenAI(
            model_name="zhipu-api",
            temperature=temperature,
            max_tokens=max_tokens,
            callbacks=[callback],
        )
        prompt_template = get_prompt_template("sql_chat", "PROMPT")
        input_msg = History(role="user", content=prompt_template).to_msg_template(False)
        chat_prompt = ChatPromptTemplate.from_messages([input_msg])
        chain = LLMChain(prompt=chat_prompt, llm=model)
        # Begin a task that runs in the background.
        task = asyncio.create_task(wrap_done(
            chain.acall({"query": str(prompt),"sql": str(sql),"revise": str(sql_result)}),
            callback.done),
        )
        if stream:
            answer = ""
            async for token in callback.aiter():
                # Use server-sent-events to stream the response
                answer += token
                yield json.dumps({"answer": token}, ensure_ascii=False)
        else:
            answer = ""
            async for token in callback.aiter():
                answer += token
            yield json.dumps({"answer": answer},
                             ensure_ascii=False)
        await task
        # prompt_template = get_prompt_template("sql_chat", "PROMPT2")
        # input_msg2 = History(role="user", content=prompt_template).to_msg_template(False)
        # chat_prompt2 = ChatPromptTemplate.from_messages([input_msg2])
        # callback = AsyncIteratorCallbackHandler()
        # model = get_ChatOpenAI(
        #     model_name=model_name,
        #     temperature=temperature,
        #     callbacks=[callback],
        # )
        # chain2 = LLMChain(prompt=chat_prompt2, llm=model)
        # task2 = asyncio.create_task(wrap_done(
        #     chain2.acall({"query": str(prompt),"sql": str(sql),"sql_result": str(sql_result),"answer": str(answer)}),
        #     callback.done),
        # )
        # if stream:
        #     response = ""
        #     async for token in callback.aiter():
        #         # Use server-sent-events to stream the response
        #         response += token
        #         yield json.dumps({"response": token}, ensure_ascii=False)
        # else:
        #     response = ""
        #     async for token in callback.aiter():
        #         response += token
        #     yield json.dumps({"response": response},
        #                      ensure_ascii=False)
        # await task2


    return StreamingResponse(sql_execute_iterator(sql=sql,
                                                sql_result=sql_result,
                                                prompt=prompt,
                                                model_name=model_name,),
                             media_type="text/event-stream")

async def sql_chat( query: str = Body(..., description="用户输入", examples=["你好"]),
                    table_use: str = Body(..., description="用户输入", examples=["你好"]),
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
                    model_name: str = Body(LLM_MODELS[0], description="LLM 模型名称。"),
                    temperature: float = Body(TEMPERATURE, description="LLM 采样温度", ge=0.0, le=1.0),
                    prompt_name: str = Body("knowledge_base_chat", description="使用的prompt模板名称(在configs/prompt_config.py中配置)"),
                    max_tokens: int = Body(None, description="限制LLM生成Token数量，默认None代表模型最大值"),
                    request: Request = None,
            ):

    history = [History.from_data(h) for h in history]

    async def sql_chat_iterator(query: str,
                                table_use: str,
                                knowledge_data: str,
                                history: Optional[List[History]],
                                model_name: str = LLM_MODELS[0],
                                prompt_name: str = prompt_name,
                                ) -> AsyncIterable[str]:
        callback = AsyncIteratorCallbackHandler()
        model = get_ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            callbacks=[callback],
        )
        context = "\n".join([knowledge_data])
        tables = re.findall(r'\b[a-zA-Z_]+\b', table_use, re.I)
        tables = tables + re.findall(r'from (\w+)q', context, re.I)  # re.I 让搜索变得不区分大小写
        tables = tables + re.findall(r'join (\w+)', context, re.I)
        tables = list(set(tables))
        if tables == []:
            files = os.listdir("./table_info")
            tables = [file.replace('.sql', '') for file in files]
        schema = ""
        for table in tables:
            table_path = "./table_info/" + table + ".sql"
            if os.path.exists(table_path):
                with open(table_path, 'r', encoding='utf-8') as f:
                    lines = f.read()
            else:
                print(f"File {table_path} does not exist!")
                continue
            schema += lines
            schema += '\n'
        prompt_template = get_prompt_template("sql_chat", prompt_name)
        input_msg = History(role="user", content=prompt_template).to_msg_template(False)
        chat_prompt = ChatPromptTemplate.from_messages(
            [i.to_msg_template() for i in history] + [input_msg])

        chain = LLMChain(prompt=chat_prompt, llm=model)
        # Begin a task that runs in the background.
        task = asyncio.create_task(wrap_done(
            chain.acall({"tables_used": str(tables),"table_schema": str(schema),"few_shot": str(context), "question": query}),
            callback.done),
        )
        
        count = 0
        if stream:
            answer = ""
            async for token in callback.aiter():
                # Use server-sent-events to stream the response
                if '```' in token:
                    count += 1
                answer += token
                if count == 2:
                    break
        else:
            answer = ""
            async for token in callback.aiter():
                if '```' in token:
                    count += 1
                answer += token
                if count == 2:
                    break
        await task
        # answer = await zhipu_chat(query, answer)
        yield json.dumps({"answer": answer},
                             ensure_ascii=False)
        prompt = chain.prompt.format(tables_used=str(tables),table_schema=str(schema),few_shot=str(context), question=query)
        yield json.dumps({"prompt": prompt}, ensure_ascii=False)
        
        


    return StreamingResponse(sql_chat_iterator(query=query,
                                               table_use=table_use,
                                            knowledge_data=knowledge_data,
                                            history=history,
                                            model_name=model_name,
                                            prompt_name=prompt_name),
                             media_type="text/event-stream")

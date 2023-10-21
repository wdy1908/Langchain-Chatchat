import pandas as pd
from server.chat.sql_chat import extract_sql_from_markdown
from sqlalchemy import Connection
import streamlit as st

from webui_pages.knowledge_base.knowledge_base import datasets_info
from webui_pages.utils import *
from streamlit_chatbox import *
from datetime import datetime
from server.chat.search_engine_chat import SEARCH_ENGINES
import os
from configs import LLM_MODEL, TEMPERATURE, PROMPT_TEMPLATES, HISTORY_LEN
from server.utils import get_model_worker_config
from typing import List, Dict
from server.mysql import connect_sql
chat_box = ChatBox(
    assistant_avatar=os.path.join(
        "img",
        "chatchat_icon_blue_square_v2.png"
    )
)


def get_messages_history(history_len: int, content_in_expander: bool = False) -> List[Dict]:
    '''
    返回消息历史。
    content_in_expander控制是否返回expander元素中的内容，一般导出的时候可以选上，传入LLM的history不需要
    '''

    def filter(msg):
        content = [x for x in msg["elements"] if x._output_method in ["markdown", "dialogue_text"]]
        if not content_in_expander:
            content = [x for x in content if not x._in_expander]
        content = [x.content for x in content]

        return {
            "role": msg["role"],
            "content": "\n\n".join(content),
        }

    return chat_box.filter_history(history_len=history_len, filter=filter)


def dialogue_page(api: ApiRequest):
    chat_box.init_session()
    con : Optional[Connection] = None
    with st.sidebar:
        # TODO: 对话模型与会话绑定
        def on_mode_change():
            mode = st.session_state.dialogue_mode
            dialogue_text = f"已切换到 {mode} 模式。"
            if mode == "知识库问答":
                cur_kb = st.session_state.get("selected_kb")
                if cur_kb:
                    dialogue_text = f"{dialogue_text} 当前知识库： `{cur_kb}`。"
            if mode == "SQL查询":
                con = connect_sql()
                if con:
                    dialogue_text = f"{dialogue_text} 已连接到数据库。"
            st.toast(dialogue_text)
            # sac.alert(dialogue_text, description="descp", type="success", closable=True, banner=True)

        dialogue_mode = st.selectbox("请选择对话模式：",
                                     ["LLM 对话",
                                      "知识库问答",
                                      "搜索引擎问答",
                                      "自定义Agent问答",
                                      "SQL查询",
                                      ],
                                     index=4,
                                     on_change=on_mode_change,
                                     key="dialogue_mode",
                                     )

        def on_llm_change():
            config = get_model_worker_config(llm_model)
            if not config.get("online_api"):  # 只有本地model_worker可以切换模型
                st.session_state["prev_llm_model"] = llm_model
            st.session_state["cur_llm_model"] = st.session_state.llm_model

        def llm_model_format_func(x):
            if x in running_models:
                return f"{x} (Running)"
            return x

        running_models = api.list_running_models()
        available_models = []
        config_models = api.list_config_models()
        for models in config_models.values():
            for m in models:
                if m not in running_models:
                    available_models.append(m)
        llm_models = running_models + available_models
        index = llm_models.index(st.session_state.get("cur_llm_model", LLM_MODEL))
        llm_model = st.selectbox("选择LLM模型：",
                                 llm_models,
                                 index,
                                 format_func=llm_model_format_func,
                                 on_change=on_llm_change,
                                 key="llm_model",
                                 )
        if (st.session_state.get("prev_llm_model") != llm_model
                and not get_model_worker_config(llm_model).get("online_api")
                and llm_model not in running_models):
            with st.spinner(f"正在加载模型： {llm_model}，请勿进行操作或刷新页面"):
                prev_model = st.session_state.get("prev_llm_model")
                r = api.change_llm_model(prev_model, llm_model)
                if msg := check_error_msg(r):
                    st.error(msg)
                elif msg := check_success_msg(r):
                    st.success(msg)
                st.session_state["prev_llm_model"] = llm_model


        index_prompt = {
            "LLM 对话": "llm_chat",
            "自定义Agent问答": "agent_chat",
            "搜索引擎问答": "search_engine_chat",
            "知识库问答": "knowledge_base_chat",
            "SQL查询": "sql_chat",
        }
        prompt_templates_kb_list = list(PROMPT_TEMPLATES[index_prompt[dialogue_mode]].keys())
        prompt_template_name = prompt_templates_kb_list[0]
        if "prompt_template_select" not in st.session_state:
            st.session_state.prompt_template_select = prompt_templates_kb_list[0]


        def on_prompt_change():
            dialogue_text = f"已切换为 {prompt_template_name} 模板。"
            st.toast(dialogue_text)

        prompt_template_select = st.selectbox(
            "请选择Prompt模板：",
            prompt_templates_kb_list,
            index=0,
            on_change=on_prompt_change,
            key="prompt_template_select",
        )
        prompt_template_name = st.session_state.prompt_template_select

        temperature = st.slider("Temperature：", 0.0, 1.0, TEMPERATURE, 0.05)

        history_len = st.number_input("历史对话轮数：", 0, 20, HISTORY_LEN)

        def on_kb_change():
            st.toast(f"已加载知识库： {st.session_state.selected_kb}")

        if dialogue_mode == "知识库问答" or dialogue_mode == "SQL查询":
            with st.expander("知识库配置", True):
                kb_list = api.list_knowledge_bases(no_remote_api=True)
                selected_kb = st.selectbox(
                    "请选择知识库：",
                    kb_list,
                    index=len(kb_list) - 1,
                    on_change=on_kb_change,
                    key="selected_kb",
                )
                kb_top_k = st.number_input("匹配知识条数：", 1, 20, VECTOR_SEARCH_TOP_K)
                score_threshold = st.slider("知识匹配分数阈值：", 0.0, 1.0, float(SCORE_THRESHOLD), 0.01)
                # chunk_content = st.checkbox("关联上下文", False, disabled=True)
                # chunk_size = st.slider("关联长度：", 0, 500, 250, disabled=True)
        elif dialogue_mode == "搜索引擎问答":
            search_engine_list = list(SEARCH_ENGINES.keys())
            with st.expander("搜索引擎配置", True):
                search_engine = st.selectbox(
                    label="请选择搜索引擎",
                    options=search_engine_list,
                    index=search_engine_list.index("duckduckgo") if "duckduckgo" in search_engine_list else 0,
                )
                se_top_k = st.number_input("匹配搜索结果条数：", 1, 20, SEARCH_ENGINE_TOP_K)

    # Display chat messages from history on app rerun

    chat_box.output_messages()

    chat_input_placeholder = "请输入对话内容，换行请使用Shift+Enter "

    if prompt := st.chat_input(chat_input_placeholder, key="prompt"):
        history = get_messages_history(history_len)
        chat_box.user_say(prompt)
        if dialogue_mode == "LLM 对话":
            chat_box.ai_say("正在思考...")
            dialogue_text = ""
            r = api.chat_chat(prompt,
                              history=history,
                              model=llm_model,
                              prompt_name=prompt_template_name,
                              temperature=temperature)
            for t in r:
                if error_msg := check_error_msg(t):  # check whether error occured
                    st.error(error_msg)
                    break
                dialogue_text += t
                chat_box.update_msg(dialogue_text)
            chat_box.update_msg(dialogue_text, streaming=False)  # 更新最终的字符串，去除光标


        elif dialogue_mode == "自定义Agent问答":
            chat_box.ai_say([
                f"正在思考...",
                Markdown("...", in_expander=True, title="思考过程", state="complete"),
            ])
            dialogue_text = ""
            ans = ""
            support_agent = ["gpt", "Qwen", "qwen-api", "baichuan-api"]  # 目前支持agent的模型
            if not any(agent in llm_model for agent in support_agent):
                ans += "正在思考... \n\n <span style='color:red'>该模型并没有进行Agent对齐，无法正常使用Agent功能！</span>\n\n\n<span style='color:red'>请更换 GPT4或Qwen-14B等支持Agent的模型获得更好的体验！ </span> \n\n\n"
                chat_box.update_msg(ans, element_index=0, streaming=False)

            for d in api.agent_chat(prompt,
                                    history=history,
                                    model=llm_model,
                                    temperature=temperature,
                                    ):
                try:
                    d = json.loads(d)
                except:
                    pass
                if error_msg := check_error_msg(d):  # check whether error occured
                    st.error(error_msg)

                elif chunk := d.get("final_answer"):
                    ans += chunk
                    chat_box.update_msg(ans, element_index=0)
                elif chunk := d.get("answer"):
                    dialogue_text += chunk
                    chat_box.update_msg(dialogue_text, element_index=1)
                elif chunk := d.get("tools"):
                    dialogue_text += "\n\n".join(d.get("tools", []))
                    chat_box.update_msg(dialogue_text, element_index=1)
            chat_box.update_msg(ans, element_index=0, streaming=False)
            chat_box.update_msg(dialogue_text, element_index=1, streaming=False)
        elif dialogue_mode == "知识库问答":
            chat_box.ai_say([
                f"正在查询知识库 `{selected_kb}` ...",
                Markdown("...", in_expander=True, title="知识库匹配结果", state="complete"),
            ])
            dialogue_text = ""
            for d in api.knowledge_base_chat(prompt,
                                             knowledge_base_name=selected_kb,
                                             top_k=kb_top_k,
                                             score_threshold=score_threshold,
                                             history=history,
                                             model=llm_model,
                                             prompt_name=prompt_template_name,
                                             temperature=temperature):
                if error_msg := check_error_msg(d):  # check whether error occured
                    st.error(error_msg)
                elif chunk := d.get("answer"):
                    dialogue_text += chunk
                    chat_box.update_msg(dialogue_text, element_index=0)
            chat_box.update_msg(dialogue_text, element_index=0, streaming=False)
            chat_box.update_msg("\n\n".join(d.get("docs", [])), element_index=1, streaming=False)
        elif dialogue_mode == "搜索引擎问答":
            chat_box.ai_say([
                f"正在执行 `{search_engine}` 搜索...",
                Markdown("...", in_expander=True, title="网络搜索结果", state="complete"),
            ])
            dialogue_text = ""
            for d in api.search_engine_chat(prompt,
                                            search_engine_name=search_engine,
                                            top_k=se_top_k,
                                            history=history,
                                            model=llm_model,
                                            prompt_name=prompt_template_name,
                                            temperature=temperature):
                if error_msg := check_error_msg(d):  # check whether error occured
                    st.error(error_msg)
                elif chunk := d.get("answer"):
                    dialogue_text += chunk
                    chat_box.update_msg(dialogue_text, element_index=0)
            chat_box.update_msg(dialogue_text, element_index=0, streaming=False)
            chat_box.update_msg("\n\n".join(d.get("docs", [])), element_index=1, streaming=False)
        elif dialogue_mode == "SQL查询":
            chat_box.ai_say([
                f"正在查询知识库 `{selected_kb}` ...",
                Markdown("...", in_expander=True, title="知识库匹配结果", state="complete"),
            ])
            dialogue_text = ""
            for d in api.sql_search(prompt,
                                    knowledge_base_name=selected_kb,
                                  top_k=kb_top_k,
                                  score_threshold=score_threshold,):
                if error_msg := check_error_msg(d):
                    st.error(error_msg)
                elif chunk := d.get("answer"):
                    dialogue_text += chunk
                    chat_box.update_msg(dialogue_text, element_index=0)
            chat_box.update_msg(dialogue_text, element_index=0, streaming=False)
            chat_box.update_msg("\n\n".join(d.get("docs", [])), element_index=1, streaming=False)
            knowledge_data = str(d.get("doc", []))

            chat_box.ai_say([
                f"正在生成SQL语句并执行...",
                Markdown("...", in_expander=True, title="SQL生成结果", state="complete"),
            ])
            dialogue_text = ""
            for d in api.sql_chat(prompt,
                                knowledge_data=knowledge_data,
                                history=history,
                                model=llm_model,
                                prompt_name=prompt_template_name,
                                temperature=temperature):
                if error_msg := check_error_msg(d):  # check whether error occured
                    st.error(error_msg)
                elif chunk := d.get("answer"):
                    dialogue_text += chunk
                    chat_box.update_msg(dialogue_text, element_index=1)
            chat_box.update_msg(dialogue_text, element_index=1, streaming=False)
            sql = extract_sql_from_markdown(dialogue_text)
            sql_result = None
            from sqlalchemy import text
            con = connect_sql()
            tot = 3
            temp = 3
            while temp>0:
                try:
                    sql_result = con.execute(text(sql))
                    break
                except Exception as e:
                    error = f"\n第{tot-temp+1}次生成的结果为：{sql}\n结果不正确，报错信息为：{str(e)}\n请重新生成结果。"
                    st.error(error)
                    temp -= 1
                    prompt += error
                    dialogue_text = ""
                    for d in api.sql_chat(prompt,
                                        knowledge_data=knowledge_data,
                                        history=history,
                                        model=llm_model,
                                        prompt_name=prompt_template_name,
                                        temperature=temperature):
                        if error_msg := check_error_msg(d):  # check whether error occured
                            st.error(error_msg)
                        elif chunk := d.get("answer"):
                            dialogue_text += chunk
                            chat_box.update_msg(dialogue_text, element_index=1)
                    chat_box.update_msg(dialogue_text, element_index=1, streaming=False)
                    sql = extract_sql_from_markdown(dialogue_text)
            if not sql_result:
                st.error("SQL语句生成错误。")
                return
            sql_result_df = pd.DataFrame(sql_result.fetchall(), columns=sql_result.keys())
            sql_result_df_markdown = sql_result_df.to_markdown()
            chat_box.update_msg(sql_result_df_markdown, element_index=0, streaming=False)
            preprompt = d.get("prompt")
            # print(preprompt)
            chat_box.ai_say([
                f"正在分析SQL执行结果...",
                Markdown("...", in_expander=True, title="SQL查询结果", state="complete"),
            ])
            dialogue_text = ""
            # dialogue_text2 = ""
            for d in api.sql_execute(sql,
                                     sql_result_df_markdown,
                                    prompt=prompt,
                                    model=llm_model,
                                    temperature=temperature,):
                if error_msg := check_error_msg(d):  # check whether error occured
                    st.error(error_msg)
                elif chunk := d.get("answer"):
                    dialogue_text += chunk
                    chat_box.update_msg(dialogue_text, element_index=1)
                # elif chunk := d.get("response"):
                #     dialogue_text2 += chunk
                #     chat_box.update_msg(dialogue_text2, element_index=0)
            chat_box.update_msg(dialogue_text, element_index=1, streaming=False)
            chat_box.update_msg(dialogue_text, element_index=0, streaming=False)

    now = datetime.now()
    with st.sidebar:

        cols = st.columns(2)
        export_btn = cols[0]
        if cols[1].button(
                "清空对话",
                use_container_width=True,
        ):
            chat_box.reset_history()
            st.experimental_rerun()

    export_btn.download_button(
        "导出记录",
        "".join(chat_box.export2md()),
        file_name=f"{now:%Y-%m-%d %H.%M}_对话记录.md",
        mime="dialogue_text/markdown",
        use_container_width=True,
    )

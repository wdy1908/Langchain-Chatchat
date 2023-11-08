![](img/logo-long-chatchat-trans-v2.png)


🌍 [READ THIS IN ENGLISH](README_en.md)

📃 **LangChain-Chatchat** (原 Langchain-ChatGLM)

基于 Langchain 与 ChatGLM 等大语言模型的本地知识库问答应用实现。

---

## 目录

* [介绍](README.md#介绍)
* [解决的痛点](README.md#解决的痛点)
* [快速上手](README.md#快速上手)
  * [1. 环境配置](README.md#1-环境配置)
  * [2. 模型下载](README.md#2-模型下载)
  * [3. 初始化知识库和配置文件](README.md#3-初始化知识库和配置文件)
  * [4. 一键启动](README.md#4-一键启动)
  * [5. 启动界面示例](README.md#5-启动界面示例)
* [联系我们](README.md#联系我们)
* [合作伙伴名单](README.md#合作伙伴名单)


## 介绍

🤖️ 一种利用 [langchain](https://github.com/hwchase17/langchain) 思想实现的基于本地知识库的问答应用，目标期望建立一套对中文场景与开源模型支持友好、可离线运行的知识库问答解决方案。

💡 受 [GanymedeNil](https://github.com/GanymedeNil) 的项目 [document.ai](https://github.com/GanymedeNil/document.ai) 和 [AlexZhangji](https://github.com/AlexZhangji) 创建的 [ChatGLM-6B Pull Request](https://github.com/THUDM/ChatGLM-6B/pull/216) 启发，建立了全流程可使用开源模型实现的本地知识库问答应用。本项目的最新版本中通过使用 [FastChat](https://github.com/lm-sys/FastChat) 接入 Vicuna, Alpaca, LLaMA, Koala, RWKV 等模型，依托于 [langchain](https://github.com/langchain-ai/langchain) 框架支持通过基于 [FastAPI](https://github.com/tiangolo/fastapi) 提供的 API 调用服务，或使用基于 [Streamlit](https://github.com/streamlit/streamlit) 的 WebUI 进行操作。

✅ 依托于本项目支持的开源 LLM 与 Embedding 模型，本项目可实现全部使用**开源**模型**离线私有部署**。与此同时，本项目也支持 OpenAI GPT API 的调用，并将在后续持续扩充对各类模型及模型 API 的接入。

⛓️ 本项目实现原理如下图所示，过程包括加载文件 -> 读取文本 -> 文本分割 -> 文本向量化 -> 问句向量化 -> 在文本向量中匹配出与问句向量最相似的 `top k`个 -> 匹配出的文本作为上下文和问题一起添加到 `prompt`中 -> 提交给 `LLM`生成回答。

📺 [原理介绍视频](https://www.bilibili.com/video/BV13M4y1e7cN/?share_source=copy_web&vd_source=e6c5aafe684f30fbe41925d61ca6d514)

![实现原理图](img/langchain+chatglm.png)

从文档处理角度来看，实现流程如下：

![实现原理图2](img/langchain+chatglm2.png)

🚩 本项目未涉及微调、训练过程，但可利用微调或训练对本项目效果进行优化。

🌐 [AutoDL 镜像](https://www.codewithgpu.com/i/chatchat-space/Langchain-Chatchat/Langchain-Chatchat) 中 `v10` 版本所使用代码已更新至本项目 `v0.2.6` 版本。

🐳 [Docker 镜像](registry.cn-beijing.aliyuncs.com/chatchat/chatchat:0.2.6) 已经更新到 ```0.2.6``` 版本。

🌲 一行命令运行 Docker ：

```shell
docker run -d --gpus all -p 80:8501 registry.cn-beijing.aliyuncs.com/chatchat/chatchat:0.2.6
```

🧩 本项目有一个非常完整的[Wiki](https://github.com/chatchat-space/Langchain-Chatchat/wiki/) ， README只是一个简单的介绍，__仅仅是入门教程，能够基础运行__。 如果你想要更深入的了解本项目，或者对相对本项目做出共享。请移步 [Wiki](https://github.com/chatchat-space/Langchain-Chatchat/wiki/)  界面

## 解决的痛点

该项目是一个可以实现 __完全本地化__推理的知识库增强方案, 重点解决数数据安全保护，私域化部署的企业痛点。
本开源方案采用```Apache License```，可以免费商用，无需付费。

我们支持市面上主流的本地大预言模型和Embedding模型，支持开源的本地向量数据库。
支持列表详见[Wiki](https://github.com/chatchat-space/Langchain-Chatchat/wiki/)


## 快速上手

### 1. 环境配置

<<<<<<< HEAD
参见 [版本更新日志](https://github.com/imClumsyPanda/langchain-ChatGLM/releases)。

从 `0.1.x` 升级过来的用户请注意，需要按照[开发部署](README.md#3-开发部署)过程操作，将现有知识库迁移到新格式，具体见[知识库初始化与迁移](docs/INSTALL.md#知识库初始化与迁移)。

### `0.2.0` 版本与 `0.1.x` 版本区别

1. 使用 [FastChat](https://github.com/lm-sys/FastChat) 提供开源 LLM 模型的 API，以 OpenAI API 接口形式接入，提升 LLM 模型加载效果；
2. 使用 [langchain](https://github.com/langchain-ai/langchain) 中已有 Chain 的实现，便于后续接入不同类型 Chain，并将对 Agent 接入开展测试；
3. 使用 [FastAPI](https://github.com/tiangolo/fastapi) 提供 API 服务，全部接口可在 FastAPI 自动生成的 docs 中开展测试，且所有对话接口支持通过参数设置流式或非流式输出；
4. 使用 [Streamlit](https://github.com/streamlit/streamlit) 提供 WebUI 服务，可选是否基于 API 服务启动 WebUI，增加会话管理，可以自定义会话主题并切换，且后续可支持不同形式输出内容的显示；
5. 项目中默认 LLM 模型改为 [THUDM/ChatGLM2-6B](https://huggingface.co/THUDM/chatglm2-6b)，默认 Embedding 模型改为 [moka-ai/m3e-base](https://huggingface.co/moka-ai/m3e-base)，文件加载方式与文段划分方式也有调整，后续将重新实现上下文扩充，并增加可选设置；
6. 项目中扩充了对不同类型向量库的支持，除支持 [FAISS](https://github.com/facebookresearch/faiss) 向量库外，还提供 [Milvus](https://github.com/milvus-io/milvus), [PGVector](https://github.com/pgvector/pgvector) 向量库的接入；
7. 项目中搜索引擎对话，除 Bing 搜索外，增加 DuckDuckGo 搜索选项，DuckDuckGo 搜索无需配置 API Key，在可访问国外服务环境下可直接使用。

---

## 模型支持

本项目中默认使用的 LLM 模型为 [THUDM/ChatGLM2-6B](https://huggingface.co/THUDM/chatglm2-6b)，默认使用的 Embedding 模型为 [moka-ai/m3e-base](https://huggingface.co/moka-ai/m3e-base) 为例。

### LLM 模型支持

本项目最新版本中支持接入**本地模型**与**在线 LLM API**。

本地 LLM 模型接入基于 [FastChat](https://github.com/lm-sys/FastChat) 实现，支持模型如下：

- [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
- Vicuna, Alpaca, LLaMA, Koala
- [BlinkDL/RWKV-4-Raven](https://huggingface.co/BlinkDL/rwkv-4-raven)
- [camel-ai/CAMEL-13B-Combined-Data](https://huggingface.co/camel-ai/CAMEL-13B-Combined-Data)
- [databricks/dolly-v2-12b](https://huggingface.co/databricks/dolly-v2-12b)
- [FreedomIntelligence/phoenix-inst-chat-7b](https://huggingface.co/FreedomIntelligence/phoenix-inst-chat-7b)
- [h2oai/h2ogpt-gm-oasst1-en-2048-open-llama-7b](https://huggingface.co/h2oai/h2ogpt-gm-oasst1-en-2048-open-llama-7b)
- [lcw99/polyglot-ko-12.8b-chang-instruct-chat](https://huggingface.co/lcw99/polyglot-ko-12.8b-chang-instruct-chat)
- [lmsys/fastchat-t5-3b-v1.0](https://huggingface.co/lmsys/fastchat-t5)
- [mosaicml/mpt-7b-chat](https://huggingface.co/mosaicml/mpt-7b-chat)
- [Neutralzz/BiLLa-7B-SFT](https://huggingface.co/Neutralzz/BiLLa-7B-SFT)
- [nomic-ai/gpt4all-13b-snoozy](https://huggingface.co/nomic-ai/gpt4all-13b-snoozy)
- [NousResearch/Nous-Hermes-13b](https://huggingface.co/NousResearch/Nous-Hermes-13b)
- [openaccess-ai-collective/manticore-13b-chat-pyg](https://huggingface.co/openaccess-ai-collective/manticore-13b-chat-pyg)
- [OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5](https://huggingface.co/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5)
- [project-baize/baize-v2-7b](https://huggingface.co/project-baize/baize-v2-7b)
- [Salesforce/codet5p-6b](https://huggingface.co/Salesforce/codet5p-6b)
- [StabilityAI/stablelm-tuned-alpha-7b](https://huggingface.co/stabilityai/stablelm-tuned-alpha-7b)
- [THUDM/chatglm-6b](https://huggingface.co/THUDM/chatglm-6b)
- [THUDM/chatglm2-6b](https://huggingface.co/THUDM/chatglm2-6b)
- [tiiuae/falcon-40b](https://huggingface.co/tiiuae/falcon-40b)
- [timdettmers/guanaco-33b-merged](https://huggingface.co/timdettmers/guanaco-33b-merged)
- [togethercomputer/RedPajama-INCITE-7B-Chat](https://huggingface.co/togethercomputer/RedPajama-INCITE-7B-Chat)
- [WizardLM/WizardLM-13B-V1.0](https://huggingface.co/WizardLM/WizardLM-13B-V1.0)
- [WizardLM/WizardCoder-15B-V1.0](https://huggingface.co/WizardLM/WizardCoder-15B-V1.0)
- [baichuan-inc/baichuan-7B](https://huggingface.co/baichuan-inc/baichuan-7B)
- [internlm/internlm-chat-7b](https://huggingface.co/internlm/internlm-chat-7b)
- [Qwen/Qwen-7B-Chat/Qwen-14B-Chat](https://huggingface.co/Qwen/)
- [HuggingFaceH4/starchat-beta](https://huggingface.co/HuggingFaceH4/starchat-beta)
- [FlagAlpha/Llama2-Chinese-13b-Chat](https://huggingface.co/FlagAlpha/Llama2-Chinese-13b-Chat) and others
- [BAAI/AquilaChat-7B](https://huggingface.co/BAAI/AquilaChat-7B)
- [all models of OpenOrca](https://huggingface.co/Open-Orca)
- [Spicyboros](https://huggingface.co/jondurbin/spicyboros-7b-2.2?not-for-all-audiences=true) + [airoboros 2.2](https://huggingface.co/jondurbin/airoboros-l2-13b-2.2)
- [VMware&#39;s OpenLLaMa OpenInstruct](https://huggingface.co/VMware/open-llama-7b-open-instruct)
- [baichuan2-7b/baichuan2-13b](https://huggingface.co/baichuan-inc)
- 任何 [EleutherAI](https://huggingface.co/EleutherAI) 的 pythia 模型，如 [pythia-6.9b](https://huggingface.co/EleutherAI/pythia-6.9b)
- 在以上模型基础上训练的任何 [Peft](https://github.com/huggingface/peft) 适配器。为了激活，模型路径中必须有 `peft` 。注意：如果加载多个peft模型，你可以通过在任何模型工作器中设置环境变量 `PEFT_SHARE_BASE_WEIGHTS=true` 来使它们共享基础模型的权重。

以上模型支持列表可能随 [FastChat](https://github.com/lm-sys/FastChat) 更新而持续更新，可参考 [FastChat 已支持模型列表](https://github.com/lm-sys/FastChat/blob/main/docs/model_support.md)。

除本地模型外，本项目也支持直接接入 OpenAI API、智谱AI等在线模型，具体设置可参考 `configs/model_configs.py.example` 中的 `ONLINE_LLM_MODEL` 的配置信息。

在线 LLM 模型目前已支持：

- [ChatGPT](https://api.openai.com)
- [智谱AI](http://open.bigmodel.cn)
- [MiniMax](https://api.minimax.chat)
- [讯飞星火](https://xinghuo.xfyun.cn)
- [百度千帆](https://cloud.baidu.com/product/wenxinworkshop?track=dingbutonglan)
- [字节火山方舟](https://www.volcengine.com/docs/82379)
- [阿里云通义千问](https://dashscope.aliyun.com/)
- [百川](https://www.baichuan-ai.com/home#api-enter) (个人用户 API_KEY 暂未开放)

项目中默认使用的 LLM 类型为 `THUDM/ChatGLM2-6B`，如需使用其他 LLM 类型，请在 `configs/model_config.py` 中对 `MODEL_PATH` 和 `LLM_MODEL` 进行修改。

### Embedding 模型支持

本项目支持调用 [HuggingFace](https://huggingface.co/models?pipeline_tag=sentence-similarity) 中的 Embedding 模型，已支持的 Embedding 模型如下：

- [moka-ai/m3e-small](https://huggingface.co/moka-ai/m3e-small)
- [moka-ai/m3e-base](https://huggingface.co/moka-ai/m3e-base)
- [moka-ai/m3e-large](https://huggingface.co/moka-ai/m3e-large)
- [BAAI/bge-small-zh](https://huggingface.co/BAAI/bge-small-zh)
- [BAAI/bge-base-zh](https://huggingface.co/BAAI/bge-base-zh)
- [BAAI/bge-large-zh](https://huggingface.co/BAAI/bge-large-zh)
- [BAAI/bge-base-zh-v1.5](https://huggingface.co/BAAI/bge-base-zh-v1.5)
- [BAAI/bge-large-zh-v1.5](https://huggingface.co/BAAI/bge-large-zh-v1.5)
- [BAAI/bge-base-zh-v1.5](https://huggingface.co/BAAI/bge-base-zh-v1.5)
- [BAAI/bge-large-zh-v1.5](https://huggingface.co/BAAI/bge-large-zh-v1.5)
- [BAAI/bge-large-zh-noinstruct](https://huggingface.co/BAAI/bge-large-zh-noinstruct)
- [sensenova/piccolo-base-zh](https://huggingface.co/sensenova/piccolo-base-zh)
- [sensenova/piccolo-large-zh](https://huggingface.co/sensenova/piccolo-large-zh)
- [shibing624/text2vec-base-chinese-sentence](https://huggingface.co/shibing624/text2vec-base-chinese-sentence)
- [shibing624/text2vec-base-chinese-paraphrase](https://huggingface.co/shibing624/text2vec-base-chinese-paraphrase)
- [shibing624/text2vec-base-multilingual](https://huggingface.co/shibing624/text2vec-base-multilingual)
- [shibing624/text2vec-base-chinese](https://huggingface.co/shibing624/text2vec-base-chinese)
- [shibing624/text2vec-bge-large-chinese](https://huggingface.co/shibing624/text2vec-bge-large-chinese)
- [GanymedeNil/text2vec-large-chinese](https://huggingface.co/GanymedeNil/text2vec-large-chinese)
- [nghuyong/ernie-3.0-nano-zh](https://huggingface.co/nghuyong/ernie-3.0-nano-zh)
- [nghuyong/ernie-3.0-base-zh](https://huggingface.co/nghuyong/ernie-3.0-base-zh)
- [sensenova/piccolo-base-zh](https://huggingface.co/sensenova/piccolo-base-zh)
- [sensenova/piccolo-base-zh](https://huggingface.co/sensenova/piccolo-large-zh)
- [OpenAI/text-embedding-ada-002](https://platform.openai.com/docs/guides/embeddings)

项目中默认使用的 Embedding 类型为 `moka-ai/m3e-base`，如需使用其他 Embedding 类型，请在 `configs/model_config.py` 中对 `embedding_model_dict` 和 `EMBEDDING_MODEL` 进行修改。

### Text Splitter 个性化支持

本项目支持调用 [Langchain](https://api.python.langchain.com/en/latest/api_reference.html#module-langchain.text_splitter) 的 Text Splitter 分词器以及基于此改进的自定义分词器，已支持的 Text Splitter 类型如下：

- CharacterTextSplitter
- LatexTextSplitter
- MarkdownHeaderTextSplitter
- MarkdownTextSplitter
- NLTKTextSplitter
- PythonCodeTextSplitter
- RecursiveCharacterTextSplitter
- SentenceTransformersTokenTextSplitter
- SpacyTextSplitter

已经支持的定制分词器如下：

- [AliTextSplitter](text_splitter/ali_text_splitter.py)
- [ChineseRecursiveTextSplitter](text_splitter/chinese_recursive_text_splitter.py)
- [ChineseTextSplitter](text_splitter/chinese_text_splitter.py)

项目中默认使用的 Text Splitter 类型为 `ChineseRecursiveTextSplitter`，如需使用其他 Text Splitter 类型，请在 `configs/model_config.py` 中对 `text_splitter_dict` 和 `TEXT_SPLITTER` 进行修改。

关于如何使用自定义分词器和贡献自己的分词器，可以参考 [如何自定义分词器](docs/splitter.md)。

---

## Agent 生态
### 基础的 Agent
在本版本中，我们实现了一个简单的基于 OpenAI 的 ReAct 的 Agent 模型，目前，经过我们测试，仅有以下两个模型支持：
+ OpenAI GPT4
+ ChatGLM2-130B

目前版本的 Agent 仍然需要对提示词进行大量调试。

### 构建自己的 Agent 工具

详见 [自定义 Agent 说明](docs/自定义Agent.md)

---

## Docker 部署

🐳 Docker 镜像地址: `registry.cn-beijing.aliyuncs.com/chatchat/chatchat:0.2.3)`

```shell
docker run -d --gpus all -p 80:8501 registry.cn-beijing.aliyuncs.com/chatchat/chatchat:0.2.3
=======
+ 首先，确保你的机器安装了 Python 3.10
>>>>>>> upstream/master
```
$ python --version
Python 3.10.12
```
接着，创建一个虚拟环境，并在虚拟环境内安装项目的依赖
```shell

# 拉取仓库
$ git clone https://github.com/chatchat-space/Langchain-Chatchat.git

# 进入目录
$ cd Langchain-Chatchat

# 安装全部依赖
$ pip install -r requirements.txt 
$ pip install -r requirements_api.txt
$ pip install -r requirements_webui.txt  

# 默认依赖包括基本运行环境（FAISS向量库）。如果要使用 milvus/pg_vector 等向量库，请将 requirements.txt 中相应依赖取消注释再安装。
```
### 2， 模型下载

如需在本地或离线环境下运行本项目，需要首先将项目所需的模型下载至本地，通常开源 LLM 与 Embedding 模型可以从 [HuggingFace](https://huggingface.co/models) 下载。

以本项目中默认使用的 LLM 模型 [THUDM/ChatGLM2-6B](https://huggingface.co/THUDM/chatglm2-6b) 与 Embedding 模型 [moka-ai/m3e-base](https://huggingface.co/moka-ai/m3e-base) 为例：

下载模型需要先[安装 Git LFS](https://docs.github.com/zh/repositories/working-with-files/managing-large-files/installing-git-large-file-storage)，然后运行

```Shell
$ git lfs install
$ git clone https://huggingface.co/THUDM/chatglm2-6b
$ git clone https://huggingface.co/moka-ai/m3e-base
```
### 3. 初始化知识库和配置文件

按照下列方式初始化自己的知识库和简单的复制配置文件
```shell
$ python copy_config_example.py
$ python init_database.py --recreate-vs
 ```
### 4. 一键启动

按照以下命令启动项目
```shell
$ python startup.py -a
```
### 5. 启动界面示例

如果正常启动，你将能看到以下界面

1. FastAPI Docs 界面

![](img/fastapi_docs_026.png)

2. Web UI 启动界面示例：

- Web UI 对话界面：

![img](img/LLM_success.png)

- Web UI 知识库管理页面：

![](img/init_knowledge_base.jpg)


### 注意

以上方式只是为了快速上手，如果需要更多的功能和自定义启动方式 ，请参考[Wiki](https://github.com/chatchat-space/Langchain-Chatchat/wiki/)


---
## 联系我们
### Telegram
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white "langchain-chatglm")](https://t.me/+RjliQ3jnJ1YyN2E9)

### 项目交流群
<img src="img/qr_code_71.jpg" alt="二维码" width="300" />

🎉 Langchain-Chatchat 项目微信交流群，如果你也对本项目感兴趣，欢迎加入群聊参与讨论交流。
### 公众号
![](img/official_wechat_mp_account.png)
🎉 Langchain-Chatchat 项目官方公众号，欢迎扫码关注。


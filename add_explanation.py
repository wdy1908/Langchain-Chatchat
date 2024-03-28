import json
from configs import LLM_MODELS
from server.utils import api_address
from webui_pages.utils import *
from webui_pages.utils import ApiRequest

api = ApiRequest(base_url=api_address())
with open('/modelFactory/poolwdy/Langchain-Chatchat/lora_data/train.json', 'r') as f:
    data = json.load(f)
class ChatError(Exception):
    pass
def chat(api: ApiRequest, instruction, output):
    output = "\n生成的sql为：" + output + "，请解释。"
    for d in api.chat_chat(query=instruction+output,
                                    model="baichuan-api",
                                    max_tokens=2048,
                                    temperature=0.0,
                                    stream=False):
        if error_msg := check_error_msg(d):
            raise ChatError(error_msg)
    text = d.get("text", "")
    return text

for i in range(0,884):
    lora_data = data[i]
    instruction = lora_data['query']
    output = lora_data['script']
    res = chat(api, instruction, output)
    print(res)
    # exit()
    data[i]['script'] = "```sql\n" + output + "\n```\n" + res
    with open('/modelFactory/poolwdy/Langchain-Chatchat/lora_data/train.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# import requests
# import json
# with open('/modelFactory/poolwdy/Langchain-Chatchat/lora_data/train.json', 'r', encoding='utf-8') as f:
#     d = json.load(f)
# # 请求的 URL
# url = 'http://172.16.0.1:8081/api/ernie'
# # 设置请求头
# headers = {
#     'Content-Type': 'application/json'
# }

# for i in range(0,884):
#     lora_data = d[i]
#     instruction = lora_data['query']
#     output = lora_data['script']
#     new_output = "\n生成的sql为：" + output + "，请解释。"

#     # 请求的数据
#     data = {
#         "model": "ernie-bot",
#         "dialogue": [
#             {
#                 "role": "user",
#                 "content": instruction + new_output 
#             }
#         ]
#     }



#     # 发送 POST 请求
#     response = requests.post(url, data=json.dumps(data), headers=headers)
#     text = response.text
#     data = json.loads(text)
#     res = data['content']
#     # 打印响应内容
#     d[i]['script'] = "```sql\n" + output + "\n```\n" + res
#     with open('/modelFactory/poolwdy/Langchain-Chatchat/lora_data/train.json', 'w', encoding='utf-8') as f:
#         json.dump(d, f, ensure_ascii=False, indent=4)

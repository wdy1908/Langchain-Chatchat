from langchain.text_splitter import CharacterTextSplitter
import re
from typing import List


class LoraTextSplitter(CharacterTextSplitter):
    def __init__(self, sentence_size: int = 250, **kwargs):
        super().__init__(**kwargs)
        self.sentence_size = sentence_size

    def split_text(self, text: str) -> List[str]:   ##此处需要进一步优化逻辑
        print(text)
        # 定义正则表达式模式
        pattern_query = r'"query":\s*"(.*?)"'
        pattern_script = r'"script":\s*"(.*?)"'

        # 使用正则表达式查找匹配项
        match_query = re.search(pattern_query, text, re.DOTALL)
        match_script = re.search(pattern_script, text, re.DOTALL)

        # 提取匹配的值
        query_value = match_query.group(1) if match_query else None
        script_value = match_script.group(1) if match_script else None

        return "问题：" + query_value + "\n答案：" + script_value



if __name__ == "__main__":
    text_splitter = LoraTextSplitter(
        keep_separator=True,
        is_separator_regex=True,
        chunk_size=1000,
        chunk_overlap=0
    )
    ls = [
        """{
        "query": "查看室外摄像头",
        "script": "```sql\nselect 摄像头表.id as 摄像头编号, 房间表.room_name as 安装位置, 楼栋表.building_name as 所在大楼 from s_camera as 摄像头表 join s_room as 房间表 on 摄像头表.pid=房间表.id join s_building as 楼栋表 on 房间表.pid=楼栋表.id  join s_region as 区域表 on 楼栋表.pid=区域表.id  join s_organization as 单位表 on 区域表.pid=单位表.id where 摄像头表.inhouse=0 and 区域表.region_name='高新校区' and 单位表.org_name='中国科学技术大学' order by 摄像头表.id  limit 1000;\n```\n这是一段SQL语句，用于从多个表格中查询室外摄像头的相关信息。以下是各部分解释：\n\n1. `select 摄像头表.id as 摄像头编号, 房间表.room_name as 安装位置, 楼栋表.building_name as 所在大楼`：这是选择要查询的列，包括摄像头的ID（作为摄像头编号）、安装位置的名称（来自房间表）和所在大楼的名称（来自楼栋表）。\n\n2. `from s_camera as 摄像头表 join s_room as 房间表 on 摄像头表.pid=房间表.id join s_building as 楼栋表 on 房间表.pid=楼栋表.id join s_region as 区域表 on 楼栋表.pid=区域表.id join s_organization as 单位表 on 区域表.pid=单位表.id`：这部分定义了数据来源。通过JOIN操作符将摄像头表（s_camera）、房间表（s_room）、楼栋表（s_building）、区域表（s_region）和单位表（s_organization）连接在一起。连接的依据是摄像头表中的pid字段与其它表的主键相等。\n\n3. `where 摄像头表.inhouse=0 and 区域表.region_name='高新校区' and 单位表.org_name='中国科学技术大学'`：这部分设置了查询条件，即只返回室外摄像头（inhouse字段值为0）、位于“高新校区”且属于“中国科学技术大学”的摄像头。\n\n4. `order by 摄像头表.id`：按照摄像头的ID进行排序。\n\n5. `limit 1000`：限制查询结果的数量，最多返回1000条记录。"
    }""",
        ]
    # text = """"""
    for inum, text in enumerate(ls):
        print(inum)
        chunks = text_splitter.split_text(text)
        print(chunks)
        # for chunk in chunks:
        #     print("===========")
        #     print(chunk)

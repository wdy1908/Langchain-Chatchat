CREATE TABLE `a_people_trail` (
  `start_time` datetime NOT NULL COMMENT '轨迹的起始时间',
  `start_camera_id` int(11) NOT NULL COMMENT '轨迹的起始摄像头ID',
  `name` varchar(50) NOT NULL COMMENT '人员姓名',
  `end_camera_id` int(11) NOT NULL COMMENT '轨迹的结束摄像头ID',
  `end_time` datetime NOT NULL COMMENT '轨迹的结束时间',
  `gender` smallint(6) NOT NULL COMMENT '性别，0:男，1：女，2：未知',
  `age_group` varchar(50) NOT NULL COMMENT '年龄段',
  `category` smallint(6) NOT NULL COMMENT '人员类别，0：学生，1：教师，2：访客，3：未知',
  `pid` int(11) NOT NULL COMMENT '外键，如果能确切识别是哪个学生或老师，本字段指向对应表的主键列，否则为-1',
  `len` int(11) NOT NULL COMMENT '轨迹长度（包含的轨迹点数量）',
  `source` smallint(6) NOT NULL COMMENT '来源，0:标注，1：轨迹分析算法',
  `camera_id_list` text NOT NULL COMMENT '逗号分隔的摄像头ID列表',
  `content` text NOT NULL COMMENT 'json数组：[{moment:xx,cameraId:xx,roomName:xx,buildingName:xx,longitude:xx,latitude:xx},{}...]',
  `img_path` text NULL COMMENT '图像路径',
  `memo` text NULL COMMENT '备注',
  primary KEY(`start_time`, `start_camera_id`, `name`)
)
COMMENT '人员轨迹表'
CREATE TABLE `d_people`
(
  `camera_id` int(11) NOT NULL COMMENT "外键，指向识别到该人员的摄像头ID",
  `moment` datetime NOT NULL COMMENT "识别该人员的时间点",
  `num` int(11) NOT NULL COMMENT "人在图中的标识序号，从1开始",
  `gender` smallint(6) NOT NULL COMMENT "性别，0:男，1：女，2：未知",
  `age_group` varchar(50) NOT NULL COMMENT "年龄段",
  `orientation` smallint(6) NOT NULL COMMENT "朝向，0：前向，1：后向，2：侧向，3：未知",
  `glasses` smallint(6) NOT NULL COMMENT "是否佩戴眼镜，0：否，1：是，2：未知",
  `hat` smallint(6) NOT NULL COMMENT "是否佩戴帽子，0：否，1：是，2：未知",
  `hold_obj` smallint(6) NOT NULL COMMENT "是否正面持物，0：否，1：是，2：未知",
  `bag` smallint(6) NOT NULL COMMENT "包，0：手提包，1：单肩包，2：背包，3：未背包，4：未知",
  `upper` varchar(50) NOT NULL COMMENT "上衣风格",
  `lower` varchar(50) NOT NULL COMMENT "下衣风格",
  `shoe` smallint(6) NOT NULL COMMENT "是否穿靴，0：是，1：否，2：未知",
  `confidence` double NOT NULL COMMENT "目标检测的置信程度",
  `x` double NOT NULL COMMENT "人员框线图中心X坐标",
  `y` double NOT NULL COMMENT "人员框线图中心Y坐标",
  `width` double NOT NULL COMMENT "人员框线图宽度",
  `height` double NOT NULL COMMENT "人员框线图高度",
  `encoding` text NULL COMMENT "编码后的特征（128个浮点数组成的列表）",
  primary KEY(`camera_id`, `moment`, `num`)
)
COMMENT "人员表";
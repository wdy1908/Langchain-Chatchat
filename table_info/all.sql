SET NAMES utf8mb4;

CREATE TABLE `t_event_status` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '事件状态：未处理，已处理',
  primary KEY(id)
) 
COMMENT '事件状态表';

CREATE TABLE `t_hat` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '戴帽子情况：未戴帽子、戴帽子、未知',
  primary KEY(id)
) 
COMMENT '戴帽子情况表';

CREATE TABLE `t_abnormal_type` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '异常类别：闯入，逗留，摔倒，打架，徘徊，追逐，其他',
  primary KEY(id)
)
COMMENT '异常类型表';

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

CREATE TABLE `t_camera_install_type` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '摄像头安装类型名称：安装在房间内、安装在道路旁',
  primary KEY(id)
)
COMMENT '摄像头安装类型表';

CREATE TABLE `s_building`
(
	id INT NOT NULL COMMENT '主键，唯一标志一个大楼',
	pid INT NOT NULL COMMENT '外键，引用区域表主键',
	building_name VARCHAR(50) NOT NULL COMMENT '大楼名称，例如：智信楼',
	floor_num_up INT NOT NULL COMMENT '地上部分楼层数量',
	floor_num_below INT NOT NULL COMMENT '地下部分楼层数量',
	building_area DOUBLE COMMENT '总建筑面积，单位：平米',
	covered_area DOUBLE COMMENT '占地面积，单位：平米',
	latitude DOUBLE NOT NULL COMMENT '纬度',
	longitude DOUBLE NOT NULL COMMENT '经度',
	memo VARCHAR(256) COMMENT '备注',
	primary key(id)
)
COMMENT "楼栋表";

CREATE TABLE `s_room`
(
	id INT NOT NULL COMMENT '主键，唯一标志一个房间',
	pid INT NOT NULL COMMENT '外键，引用楼栋表主键',
	room_name VARCHAR(50) NOT NULL COMMENT '房间名，例如：611教室',
	room_number VARCHAR(50) NOT NULL COMMENT '房间号遵循特定的格式，例如： 6_11，-1_01',
	room_floor INT NOT NULL COMMENT '房间所在的楼层',
	room_category SMALLINT NOT NULL COMMENT '房间类型，0：教室，1：地下室，2：天台，3：电梯厅，4：走廊，5：实验室，6：体育场，7：食堂用餐区，8：门厅，9：设备房，10：图书室，11：楼梯间，12：研发室，13：报告厅，14：展厅，15:茶点室，16：会客室，17：电梯内，18：出入口，19：食堂加工区，20：休息室，21：保安室，99：其他',
	room_area DOUBLE COMMENT '房间面积，单位：平米',
	latitude double NOT NULL COMMENT '纬度',
	longitude double NOT NULL COMMENT '经度',
	memo VARCHAR(256) COMMENT '备注',
	primary key(id)
)
COMMENT "房间表";

CREATE TABLE `t_gender` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '性别名称：男、女',
  primary KEY(id)
) 
COMMENT '性别表';

CREATE TABLE `t_glasses` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '戴眼镜情况：未戴眼镜、戴眼镜、未知',
  primary KEY(id)
) 
COMMENT '戴眼镜情况表';

CREATE TABLE `s_camera`
(
	id INT NOT NULL COMMENT '主键，摄像头唯一标识',
	pid INT NOT NULL COMMENT '外键，如果安装在房间内，就指向房间表主键，否则为-1',
	camera_type SMALLINT NOT NULL COMMENT '类型，0：枪机，1：球机',
	install_type SMALLINT NOT NULL COMMENT '安装类型，0：安装在房间内，1：安装在道路旁',
	manufactor VARCHAR(50) COMMENT '制造商，例如：海康威视',
	model VARCHAR(50) COMMENT '型号，例如DS-2CD3326FWDA3-IS',
	ip VARCHAR(50) NOT NULL COMMENT '局域网IP地址',
	install_position VARCHAR(50) NOT NULL COMMENT '安装位置，例如：东北角',
	install_time DATETIME COMMENT '安装时间',
	latitude double NOT NULL COMMENT '纬度',
	longitude double NOT NULL COMMENT '经度',
	show_in_map smallint(6) NOT NULL DEFAULT "0" COMMENT '是否在3D导览图中显示',
	rtsp_url VARCHAR(512) NULL COMMENT '实时点播RTSP URL',
	frame_upload_period INT NOT NULL COMMENT '上传视频帧的时间间隔（单位：秒）',
	memo VARCHAR(256) COMMENT '备注',
	important_area SMALLINT NOT NULL DEFAULT "0" COMMENT '是否是重点区域，0：否，1：是',
	forbidden_area SMALLINT NOT NULL DEFAULT "0" COMMENT '是否是禁入区域，0：否，1：是',
	video_fragment_request_url VARCHAR(256) COMMENT '请求视频片段的网址',
	inuse SMALLINT NOT NULL DEFAULT "1" COMMENT '该摄像头是否还在使用，0：否，1：是',
	inhouse SMALLINT NOT NULL DEFAULT "1" COMMENT '该摄像头是否在室内，0：否，1：是',
	frame_grab_url VARCHAR(256) COMMENT '帧抽取RTSP URL',
	primary key (id)
)
COMMENT "摄像头表";

CREATE TABLE `s_organization`
(
	id INT NOT NULL COMMENT '主键，唯一标志一个单位',
	org_name VARCHAR(50) NOT NULL COMMENT '单位名称，例如：中国科学技术大学',
	org_code VARCHAR(50) NOT NULL COMMENT '组织机构编码',
	memo VARCHAR(256) COMMENT '备注',
	primary key(id)
)
COMMENT "单位表";

CREATE TABLE `t_camera_type` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '摄像头类型名称：球机、枪机',
  primary KEY(id)
)
COMMENT '摄像头类型表';

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
COMMENT '人员轨迹表';

CREATE TABLE `t_room_category` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '房间类型名称：教室、地下室、天台、电梯厅...',
  primary KEY(id)
)
COMMENT '房间类型表';

CREATE TABLE `t_orientation` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '朝向名称：前向、后向、侧向、未知',
  primary KEY(id)
)
COMMENT '行人朝向表';

CREATE TABLE `s_region`
(
	id INT NOT NULL COMMENT '主键，唯一标志一个区域',
	pid INT NOT NULL COMMENT '外键引用单位表主键',
	region_name VARCHAR(50) NOT NULL COMMENT '区域名称，例如：科大西区',
	region_area DOUBLE COMMENT '区域占地面积，单位：平米',
	city_name VARCHAR(50) NOT NULL COMMENT '所在的地级市',
	province_name VARCHAR(50) NOT NULL COMMENT '所在的省/直辖市/自治区/特别行政区',
	memo VARCHAR(256) COMMENT '备注',
	primary key(id)
)
COMMENT "区域表";

CREATE TABLE `a_people_spread_day_building`
(
  org_name VARCHAR(50) NOT NULL COMMENT '单位名称',
  region_name VARCHAR(50) NOT NULL COMMENT '区域名称',
  building_name VARCHAR(50) NOT NULL COMMENT '大楼名称，例如：智信楼',
  stat_time DATETIME NOT NULL COMMENT '统计时间',
  stat_year INT NOT NULL COMMENT '统计时间-年',
  stat_month INT NOT NULL COMMENT '统计时间-月',
  stat_day INT NOT NULL COMMENT '统计时间-日',
  num INT NOT NULL COMMENT '人数',
  primary KEY(org_name, region_name, building_name, stat_time)
)
COMMENT "人员分布统计表（按日和楼栋统计）";

CREATE TABLE `t_hold_object` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '持物情况：未持物、持物、未知',
  primary KEY(id)
)COMMENT '持物情况表';

CREATE TABLE `t_bag` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '背包情况：手提包、单建波、背包、未背包、未知',
  primary KEY(id)
) 
COMMENT '背包情况表';

CREATE TABLE `d_abnormal_behavior`
(
  `camera_id` int(11) NOT NULL COMMENT "外键，指向识别到异常行为的摄像头ID",
  `moment` datetime NOT NULL COMMENT "识别该异常行为的时间点",
  `abnormal_type` smallint(6) NOT NULL COMMENT "异常类别（0：闯入，1：多人聚集，2：逗留，3：徘徊，4：摔倒，5：维修，6：不安全骑车，7：打架，8：攀爬，9：物品遗留，10：脏乱，11：非正常时间闯入异性宿舍，99：其他）",
  `event_status` smallint(6) NOT NULL COMMENT "事件状态（0：未处理，1：已处理）",
  `frame_dir` varchar(256) NOT NULL COMMENT "视频帧（可能有多个）存储目录，例如：/permanent/frame/marker/camera/${yyyy-MM-dd}",
  `fragment_url` varchar(256) NULL COMMENT "视频片段存储路径，例如：/permanent/fragment/origin/camera/1661741941324#1661743141000.mp4",
  `exception` smallint(6) NULL default "0" COMMENT "是否是例外（比如工作人员、防疫人员等进行的特殊操作） 0：否，1：是",
  `memo` varchar(128) NULL COMMENT "备注",
  primary KEY(`camera_id`, `moment`, `abnormal_type`)
)
COMMENT "异常行为表（当月）";


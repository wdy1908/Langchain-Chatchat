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
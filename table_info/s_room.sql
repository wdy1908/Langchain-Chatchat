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
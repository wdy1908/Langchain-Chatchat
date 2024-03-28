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
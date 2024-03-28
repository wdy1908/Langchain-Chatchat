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
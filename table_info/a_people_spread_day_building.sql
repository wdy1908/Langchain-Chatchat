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
CREATE TABLE `t_gender` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '性别名称：男、女',
  primary KEY(id)
) 
COMMENT '性别表'
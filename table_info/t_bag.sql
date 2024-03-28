CREATE TABLE `t_bag` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '背包情况：手提包、单建波、背包、未背包、未知',
  primary KEY(id)
) 
COMMENT '背包情况表'
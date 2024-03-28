CREATE TABLE `t_orientation` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '朝向名称：前向、后向、侧向、未知',
  primary KEY(id)
)
COMMENT '行人朝向表'
CREATE TABLE `t_hat` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '戴帽子情况：未戴帽子、戴帽子、未知',
  primary KEY(id)
) 
COMMENT '戴帽子情况表'
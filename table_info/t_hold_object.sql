CREATE TABLE `t_hold_object` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '持物情况：未持物、持物、未知',
  primary KEY(id)
)COMMENT '持物情况表'
CREATE TABLE `t_event_status` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '事件状态：未处理，已处理',
  primary KEY(id)
) 
COMMENT '事件状态表'
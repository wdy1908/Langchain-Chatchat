CREATE TABLE `t_room_category` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '房间类型名称：教室、地下室、天台、电梯厅...',
  primary KEY(id)
)
COMMENT '房间类型表'
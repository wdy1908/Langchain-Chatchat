CREATE TABLE `t_camera_type` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '摄像头类型名称：球机、枪机',
  primary KEY(id)
)
COMMENT '摄像头类型表'
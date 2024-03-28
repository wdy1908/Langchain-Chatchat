CREATE TABLE `t_camera_install_type` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '摄像头安装类型名称：安装在房间内、安装在道路旁',
  primary KEY(id)
)
COMMENT '摄像头安装类型表'
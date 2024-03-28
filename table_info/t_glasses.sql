CREATE TABLE `t_glasses` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '戴眼镜情况：未戴眼镜、戴眼镜、未知',
  primary KEY(id)
) 
COMMENT '戴眼镜情况表'
CREATE TABLE `t_abnormal_type` (
  `id` smallint(6) NOT NULL COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '异常类别：闯入，逗留，摔倒，打架，徘徊，追逐，其他',
  primary KEY(id)
)
COMMENT '异常类型表'
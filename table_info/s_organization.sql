CREATE TABLE `s_organization`
(
	id INT NOT NULL COMMENT '主键，唯一标志一个单位',
	org_name VARCHAR(50) NOT NULL COMMENT '单位名称，例如：中国科学技术大学',
	org_code VARCHAR(50) NOT NULL COMMENT '组织机构编码',
	memo VARCHAR(256) COMMENT '备注',
	primary key(id)
)
COMMENT "单位表";
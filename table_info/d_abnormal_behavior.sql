CREATE TABLE `d_abnormal_behavior`
(
  `camera_id` int(11) NOT NULL COMMENT "外键，指向识别到异常行为的摄像头ID",
  `moment` datetime NOT NULL COMMENT "识别该异常行为的时间点",
  `abnormal_type` smallint(6) NOT NULL COMMENT "异常类别（0：闯入，1：多人聚集，2：逗留，3：徘徊，4：摔倒，5：维修，6：不安全骑车，7：打架，8：攀爬，9：物品遗留，10：脏乱，11：非正常时间闯入异性宿舍，99：其他）",
  `event_status` smallint(6) NOT NULL COMMENT "事件状态（0：未处理，1：已处理）",
  `frame_dir` varchar(256) NOT NULL COMMENT "视频帧（可能有多个）存储目录，例如：/permanent/frame/marker/camera/${yyyy-MM-dd}",
  `fragment_url` varchar(256) NULL COMMENT "视频片段存储路径，例如：/permanent/fragment/origin/camera/1661741941324#1661743141000.mp4",
  `exception` smallint(6) NULL default "0" COMMENT "是否是例外（比如工作人员、防疫人员等进行的特殊操作） 0：否，1：是",
  `memo` varchar(128) NULL COMMENT "备注",
  primary KEY(`camera_id`, `moment`, `abnormal_type`)
)
COMMENT "异常行为表（当月）";
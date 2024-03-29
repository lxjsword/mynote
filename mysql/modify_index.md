---
title: mysql在线更改表结构
date: 2022-11-16 09:57:00
tags: mysql
---
原始表结构
```
CREATE TABLE `t_tagging_op_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `operator` char(32) NOT NULL,
  `op_type` int(11) NOT NULL,
  `business_id` int(11) unsigned DEFAULT NULL COMMENT '对应的业务id',
  `task_group` bigint(20) unsigned DEFAULT '0' COMMENT '任务组，相同的记录认为是同一组，统计进度',
  `tid` bigint(20) DEFAULT NULL,
  `data_id` int(20) DEFAULT NULL,
  `back_cnt` int(11) unsigned DEFAULT NULL COMMENT '打回次数',
  `op_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `op_data` json NOT NULL COMMENT '操作数据',
  PRIMARY KEY (`id`, `task_group`),
  UNIQUE KEY `oobttd` (`operator`, `op_type`, `business_id`, `task_group`, `tid`, `data_id`),
  KEY `bn_group` (`business_id`, `task_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='标注操作记录表' 
PARTITION BY RANGE COLUMNS(task_group) (
    PARTITION p202207 VALUES LESS THAN (20220732000000),
    PARTITION p202208 VALUES LESS THAN (20220832000000),
    PARTITION p202209 VALUES LESS THAN (20220932000000),
    PARTITION p202210 VALUES LESS THAN (20221032000000),
    PARTITION p202211 VALUES LESS THAN (20221132000000),
    PARTITION p202212 VALUES LESS THAN (20221232000000),
    PARTITION p202301 VALUES LESS THAN (20230132000000),
    PARTITION p202302 VALUES LESS THAN (20230232000000),
    PARTITION p202303 VALUES LESS THAN (20230332000000),
    PARTITION p202304 VALUES LESS THAN (20230432000000),
    PARTITION p202305 VALUES LESS THAN (20230532000000),
    PARTITION p202306 VALUES LESS THAN (20230632000000),
    PARTITION p202307 VALUES LESS THAN (20230732000000),
    PARTITION p202308 VALUES LESS THAN (20230832000000),
    PARTITION p202309 VALUES LESS THAN (20230932000000),
    PARTITION p202310 VALUES LESS THAN (20231032000000),
    PARTITION p202311 VALUES LESS THAN (20231132000000),
    PARTITION p202312 VALUES LESS THAN (20231232000000),
    PARTITION p202401 VALUES LESS THAN (20240132000000),
    PARTITION p202402 VALUES LESS THAN (20240232000000),
    PARTITION p202403 VALUES LESS THAN (20240332000000),
    PARTITION p202404 VALUES LESS THAN (20240432000000),
    PARTITION p202405 VALUES LESS THAN (20240532000000),
    PARTITION p202406 VALUES LESS THAN (20240632000000),
    PARTITION p202407 VALUES LESS THAN (20240732000000),
    PARTITION p202408 VALUES LESS THAN (20240832000000),
    PARTITION p202409 VALUES LESS THAN (20240932000000),
    PARTITION p202410 VALUES LESS THAN (20241032000000),
    PARTITION p202411 VALUES LESS THAN (20241132000000),
    PARTITION p202412 VALUES LESS THAN (20241232000000)
);
```
需要修改索引oobttd， 加一个字段，查看表数据量在百万级，查阅参考文献，mysql5.6之前做DDL会锁表，5.6之后支持online ddl，具体支持情况如下图
![](/images/mysql/1.png)

直接执行一下DDL语句
```
alter table t_tagging_op_log add unique `bttdoob` (`business_id`,`task_group`,`tid`,`data_id`,`operator`,`op_type`,`back_cnt`), ALGORITHM=INPLACE, LOCK=NONE;
alter table t_tagging_op_log drop index oobttd, ALGORITHM=INPLACE, LOCK=NONE;
```
执行结果如下图， 可见耗时12s左右， **如果数据量级达到千万级，可能要考虑其他方案**
![](/images/mysql/2.png)

参考文档
1. https://juejin.cn/post/6854573213167386637?from_wecom=1
2. https://dev.mysql.com/doc/refman/5.6/en/innodb-online-ddl-operations.html
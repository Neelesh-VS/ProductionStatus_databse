use mydatabase;
show tables;

desc production_status;
select count(*) from production_status;

SELECT PARTITION_NAME,TABLE_ROWS
	FROM INFORMATION_SCHEMA.PARTITIONS
	WHERE TABLE_NAME = 'PRODUCTION_STATUS';

select *,from_unixtime(date_time) from production_status;

select *,from_unixtime(date_time) from production_status partition(p1); 

select station_id,date_time,from_unixtime(date_time) from production_status where mf_status=0;

 select * from production_status where date_time BETWEEN '1643732061' AND '1644903410' group by station_id;


select * from production_status where cell_id=3 and station_id=10 and mf_status= 0;

show indexes from production_status;
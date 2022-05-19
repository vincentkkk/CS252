drop database cabinet;
drop table cabinet_list;
create database cabinet;
show databases;
use cabinet;
create table courier_list(
    c_no tinyint(1) NOT NULL,
    c_name varchar(20),
    c_tel int(8) unsigned,
	primary key (c_tel)
);

create table cabinet_list(
	id tinyint(2) auto_increment not null,
    state tinyint(1) unsigned default 0,
    pickup_code mediumint(6) unsigned null,
    courier_tel int(8) unsigned,
    primary key (id),
    FOREIGN KEY(courier_tel) REFERENCES courier_list(c_tel)
);
show tables;
desc courier_list;
desc cabinet_list;

insert into courier_list
(c_no,c_name,c_tel)
values
    (1,'mark',62104641),
    (2,'steve',64549631),
    (3,'peter',64642222);
select * from courier_list;




insert into cabinet_list
(state,pickup_code,courier_tel)
values
    (1,123456,null),
    (0,null,null),
    (0,null,null),
    (0,null,null),
    (0,null,null),
    (0,null,null),
    (1,null,62104641),
    (0,null,null),
    (0,null,null),
	(0,null,null),
    (1,456789,null),
    (0,null,null),
    (0,null,null),
    (0,null,null),
    (0,null,null),
    (0,null,null),
    (1,null,64549631),
    (0,null,null),
    (0,null,null),
    (0,null,null);
select * from cabinet_list; 
select count(state=0 or null) as "emptyc" from cabinet_list;
select * from cabinet_list where pickup_code='456789';



# CRUD 연습
use mywork;
create table emp_test
(
	emp_no int   not null,
    emp_name varchar(30)   not null,
    hire_date date         null,
    salary int             null,
    primary key(emp_no)
);
desc emp_test;
select * from emp_test;

insert into `emp_test`
(emp_no, emp_name, hire_date, salary)
values (1005, '퀴리', '2021-03-01', 4000),
(1006, '호킹', '2021-03-05', 5000),
(1007, '패러데이', '2021-04-01', 2200),
(1008, '맥스웰', '2021-04-05', 3300),
(1009, '플랑크', '2021-04-05', 4400);

# 테이블 데이터 수정하기 
# update 테이블 set 컬럼1 = 값, 컬럼2 = 값 where 찾을 값
# 아인슈타인 1000, 갈릴레이 null, 뉴턴 null, 파인먼 3000, 퀴리 4000,
# 호킹 5000, 패러데이 2200, 맥스웰 3300, 클랑크 4400
select * from emp_test;
update emp_test 
set salary = 4400 where emp_no = 1009;

# delete 문으로 데이터 삭제하기
# delete from 테이블 where 조건
delete from emp_test where emp_no = 1009;
select * from emp_test;

# 트랜잭션 처리하기
# 오토 커밋 옵션 활성화 확인 
# select @@autocommit 1= 활성화, 0 = 비활성화
select @@autocommit;

# 오토 커밋 설정 set autocommit = 0/1
set autocommit = 0;
select @@autocommit;

select * from emp_test;
create table emp_tran1 as select * from emp_test;

select * from emp_tran1;
desc emp_tran1;
alter table emp_tran1 add constraint primary key(emp_no);
drop table emp_tran1;
create table emp_tran2 as select * from emp_test;
select * from emp_tran2;
alter table emp_tran2 add constraint primary key(emp_no);
desc emp_tran2;

delete from emp_tran1;
select * from emp_tran1;

select * from emp_tran1;
rollback;
select * from emp_tran1;



create database naverDB;
use naverDB;

create table member (
mem_id char(8) not null primary key,
mem_name varchar(10) not null,
mem_number tinyint not null,
addr char(2) not null,
phone1 char(3) null,
phone2 char(8) null,
height tinyint unsigned null,
debut_date date
);
desc member;

create table buy (
num int not null primary key auto_increment,
mem_id char(8) not null,
prod_name char(6) not null,
group_name char(4) null,
price int unsigned not null,
amount smallint unsigned not null,
foreign key(mem_id) references member(mem_id)
);

desc buy;

commit;

insert into `member` values 
('TWC', '트와이스', 9, '서울', '02', '11111111', 167, '2015.10.19'),
('BLK', '블랙핑크', 4, '경남', '055', '22222222', 163, '2016.08.08'),
('WMN', '여자친구', 6, '경기', '031', '33333333', 166, '2015.01.15'),
('OMY', '오마이걸', 7, '서울',  null, null, 160, '2015.04.21'),
('GRL', '소녀시대', 8, '서울',  '02', '44444444', 168, '2007.08.02'),
('ITZ', '잇지', 5, '경남',  null, null, 167, '2019.02.12'),
('RED', '레드벨벳', 4, '경북',  '054', '55555555', 161, '2014.08.01'),
('APN', '에이핑크', 6, '경기',  '031', '77777777', 164, '2011.02.10'),
('SPC', '우주소녀', 13, '서울',  '02', '88888888', 162, '2016.02.25'),
('MMU', '마마무', 4, '전남',  '061', '99999999', 165, '2014.06.19')
;

select * from member;
commit;

desc buy;

insert into `buy` 
(mem_id, prod_name, group_name, price, amount)
values 
('BLK', '지갑', null, 30, 2),
('BLK', '맥북프로', '디지털', 1000, 1),
('APN', '아이폰', '디지털', 200, 1),
('MMU', '아이폰', '디지털', 200, 5),
('BLK', '청바지', '패션', 50, 3),
('MMU', '에어팟', '디지털', 80, 10),
('GRL', '혼공SQL', '서적', 15, 5),
('APN', '혼공SQL', '서적', 15, 2),
('APN', '청바지', '패션', 50, 1),
('MMU', '지갑', Null, 30, 1),
('APN', '혼공SQL', '서적', 15, 1),
('MMU', '지갑', Null, 30, 4)
;

commit;

select * from member;
select * from buy;

select * from member as m inner join buy as b on m.mem_id = b.mem_id;

# 서브쿼리
# 쿼리 안에 또 다른 쿼리를 이용해서 원하는 데이터를
# 이름이 에이핑크인 회원의 평균키(height)보다 큰 회원을 조회하기
select mem_name, height from member 
where height > (select height from member where mem_name = '블랙핑크');

(select height from member where mem_name = '에이핑크')





















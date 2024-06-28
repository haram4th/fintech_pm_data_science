create database testsb;
use testsb;

# 테이블 만들기
create table testtable 
( student_no int not null primary key,
  student_name varchar(100) not null,
  grade tinyint,
  class varchar(50),
  gender varchar(20),
  age smallint,
  enter_date date
);
select * from testtable;

# 생성한 테이블의 속성 조회
describe testtable;
desc testtable;

# 테이블에 데이터를 입력 
# insert into `테이블명` (컬럼명) values (값)
insert into `testtable`
(student_no, student_name, grade, class, gender, age, enter_date)
values (1, '홍길동', 1, '1반', '남자', 20, '2024-03-02');

select * from testtable; 
insert into `testtable`
(student_no, grade, class, student_name,  gender, age, enter_date)
values (3, 1, '1반', '홍길동', '남자', 20, '2024-03-02'),
(4, 1, '1반', '홍길동', '남자', 20, '2024-03-02'),
(5, 1, '1반', '홍길동', '남자', 20, '2024-03-02'),
(6, 1, '1반', '홍길동', '남자', 20, '2024-03-02');







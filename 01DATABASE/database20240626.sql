show databases;
use titanic;
show tables;

select * from p_info;
select Name, Age from p_info limit 3;

select * from p_info where Sex = "male";
# => 왼쪽이 오른쪽 보다 크거나 같다.;
# p_info 에서 30살 이상인 사람 조회하기
select * from p_info where Age >= 30;
select * from p_info where Sex != "male";
select * from p_info where Age >= 30;
SELECT * FROM p_info WHERE Age <= 20;
select * from p_info where Age < 20 and Sex = 'male';
select * from p_info where Age < 20 or Sex = 'male';
select * from p_info where (Age < 20 and Sex = 'male') or Parch > 3;
                          #    거짓  and 참 = 거짓 or 참
select * from p_info where Age >= 20 and Age < 50 and Sex ="female";
select * from p_info where sibsp = 1 and parch = 1;
select * from t_info where pclass = 1;
select * from t_info where pclass = 2 or fare > 50; 
select * from survived;
select * from survived where survived = 1;

# p_info Name 컬럼의 값에서 Braund라는 이름을 갖는 사람 찾기
select * from p_info;
select * from p_info where Name = 'Braund';
select * from p_info where Name like 'Braund%';
select * from p_info where Name like '%Laina';
select * from p_info where Name like '%Mrs%';
select * from p_info where Name not like '%Mrs%';

# in 안에 있는 값이 있는 경우 가져오기
# SibSp가 4,5,6인 경우
select * from p_info where SibSp = 2 or SibSp = 3 or SibSp = 4 or SibSp = 5 or SibSp = 6;
select * from p_info where SibSp in(2,3,4,5,6);
#not in
select * from p_info where SibSp not in(2,3,4,5,6); 
# between a and b  = a이상 b 이하
# p_info Age가 40이상, 60이하인 사람을 검색하세요.;
select * from p_info where Age > 40 and Age < 60;
select * from p_info where Age between 40 and 60;

# is null/ is not null (결측치, 값이 없음)
# Age 컬럼에서 NUll이 있는지 찾기.
select * from p_info where Age is null;

select * from p_info where Age is not null;


SELECT * FROM titanic.t_info;
# t_info 테이블에서 Fare가 100 이상 1000이하인 승객을 조회하시오.
select * from t_info where Fare >= 100 and Fare <= 1000;
select * from t_info where Fare between 100 and 1000;

# t_info 테이블에서 Ticket이 PC로 시작하고 Embarked가 C 혹은 S인 승객을 조회하시오.
# like , PC%  and  or
select * from t_info where Ticket like 'PC%' and (Embarked = 'C' or Embarked = 'S');
select * from t_info where Ticket like 'PC%' and Embarked in ('C','S');

# t_info 테이블에서 Pclass가 1 혹은 2인 승객을 조회하시오.
select * from t_info where Pclass = 1 or Pclass = 2;
select * from t_info where Pclass in (1,2);

# t_info 테이블에서 Cabin에 숫자 59가 포함된 승객을 조회하시오. like
select * from t_info where Cabin like '%59%';

# p_info 테이블에서 Age가 NULL이 아니면서 이름에 James가 포함된 40세 이상의 남성을 조회하시오.
# is not null, like '%James%', Age >= 40, Sex = 'male'
select * from p_info where Age is not null and Name like '%James%' and Age >= 40 and Sex ='male';

# select * from table where order by, group by
# select * from 테이블명 where 컬럼명 order by 기준컬럼 ASC 오름차순, desc 내림차순
# p_info 테이블에서 age가 null이 아닌면서 이름에 miss가 
# 포함된 40세 이하의 여성을 조회하고 나이순으로 내림차순 정렬
# age is not null, name like '%miss%, age <= 40, sex = 'female', order by age desc
select * from p_info where age is not null and name like '%miss%' and age <= 40 
and sex = 'female' order by age desc;

# p_info 테이블에서 나이가 null이 아닌 행의 성별별 나이 평균을 구하시오.
# age is not null, sex , 
select * from p_info;
select sex, AVG(age) from p_info where age is not null group by sex;
select sex, AVG(age), MIN(age), MAX(age) from p_info where age is not null group by Sex;

select SibSp, AVG(age), MIN(age), MAX(age) from p_info where age is not null group by SibSp;


# having : group by 한 결과에서 원하는 조건에 맞는 결과만 다시 추릴 때. where 
# t_info 테이블에서 pclass별 fare 가격 평균을 구하고 그 중 가격 평균이 50을 초과하는 결과만 조회
# pclass별 fare 가격 평균: group by pclass, pclass별, AVG(fare),  AVG(fare) > 50
select * from t_info;
select pclass, AVG(fare) from t_info group by pclass having AVG(fare) > 50;

# inner join(교집합) 기준 컬럼을 비교해 양쪽에 데이터가 있는 행만 합쳐줌.
# select * from 테이블1(왼쪽) as 별칭 inner join 테이블2(오른쪽) as 별칭2
# on 테이블1의 기준컬럼 = 테이블2의 기준컬럼;
select * from passenger;
select * from ticket;
# passenger와 ticket의 inner join PassengerId, Name
select * from passenger as p inner join ticket as t on p.PassengerId = t.PassengerId; 

# left join
select * from passenger as p left join ticket as t on p.PassengerId = t.PassengerId;

# right join
select * from passenger as p right join ticket as t on p.PassengerId = t.PassengerId;

# full outer join: mysql에서 지원 X , union이란 명령어로 left join 결과와 right join 결과를 합침.
select * from passenger as p left join ticket as t on p.PassengerId = t.PassengerId
union
select * from passenger as p right join ticket as t on p.PassengerId = t.PassengerId;
# 원하는 컬럼만 조회하기: 컬럼명을 그대로 적어준다. 단, 컬럼명이 중복되면 어느 테이블인지 명시한다.
select p.PassengerId, p.Name, p.Age, t.Pclass, t.Embarked 
from passenger as p 
left join ticket as t 
on p.PassengerId = t.PassengerId;

# 3개 이상의 테이블을 조인하기.
# passenger, ticket, survived inner join 합쳐서 전체 컬럼을 출력하시오.
select * from passenger as p
inner join ticket as t
on p.PassengerId = t.PassengerId
inner join survived as s
on t.PassengerId = s.PassengerId;

# passenger, ticket, survived 테이블을 inner 조인하고 
# Survived가 1인 사람들만 찾아서 Name, Age, Sex, Pclass, survived 컬럼을 출력하시오.
select name, age, sex, pclass, survived from passenger as p
inner join ticket as t on p.PassengerId = t.PassengerId
inner join survived as s on p.PassengerId = s.PassengerId where survived = 1;
# 1의 결과를 10개만 출력하시오.
select name, age, sex, pclass, survived from passenger as p
inner join ticket as t on p.PassengerId = t.PassengerId
inner join survived as s on p.PassengerId = s.PassengerId where survived = 1 limit 10;

# Passenger 테이블을 기준 ticket, survived테이블을 
# LEFT JOIN 한 결과에서 성별이 여성이면서 Pclass가 1인 사람 중 
# 생존자(survived=1)를 찾아 이름, 성별, Pclass를 표시하시오.

select name, sex, pclass from passenger as p 
left join ticket as t on p.PassengerId = t.PassengerId
left join survived as s on p.PassengerId = s.PassengerId
where sex = 'female' and pclass = 1 and survived =1;

# passenger, ticket, survived 테이블을 left join 후 
# 나이가 10세 이상 20세 이하 이면서
# Pclass 2인 사람 
# 중 생존자를  표시하시오.
select * from passenger as p 
left join ticket as t on p.PassengerId = t.PassengerId
left join survived as s on p.PassengerId = s.PassengerId
where age between 10 and 20 and pclass = 2 and survived = 1;

# passenger, ticket, survived 테이블을 left join 후
# 성별이 여성 또는 
# Pclass 가 1인 사람 중 
# 생존자를 표시하시오.
select * from passenger as p 
left join ticket as t on p.PassengerId = t.PassengerId
left join survived as s on p.PassengerId = s.PassengerId
where (sex = 'female' or pclass = 1) and survived = 1;

# passenger, ticket, survived 테이블을 left join 후
# 생존자 중에서 이름에 Mrs가 포함된 사람을 찾아 
# 이름, Pclass, 나이, Parch, Survived 를 표시하시오.

select name, pclass, age, parch, survived from passenger as p 
left join ticket as t on p.PassengerId = t.PassengerId
left join survived as s on p.PassengerId = s.PassengerId
where survived = 1 and name like '%Mrs%';

# passenger, ticket, survived 테이블을 left join 
# 후 Pclass가 1, 2이고 Embarked가 s, c 인 사람중에서 
# 생존자를 찾아 
# 이름, 성별, 나이를 표시하시오.
select Name, sex, age from passenger as p 
left join ticket as t on p.PassengerId = t.PassengerId
left join survived as s on p.PassengerId = s.PassengerId
where (pclass in (1,2) and Embarked in ('s', 'c')) and survived = 1;

# and, or 
select * from ticket where (pclass = 1 or pclass = 3) and embarked = 'C';
select * from ticket where pclass in(1, 3) and embarked = 'C';

# passenger, ticket, survived 테이블을 left join 후 
# 이름에 James가 들어간 사람중
# 생존자를 찾아
# 이름, 성별, 나이 를 표시하고
# 나이를 기준으로 내림차순 정렬하시오. order by 기준컬럼 desc
select Name, Sex, Age from passenger as p
left join ticket as t on p.PassengerId = t.PassengerId
left join survived as s on p.PassengerId = s.PassengerId
where name like '%James%' and Survived = 1 order by Age desc;

# passenger, ticket, survived 테이블을 INNER JOIN한
# 데이터에서 성별별, count(survived)
# 생존자의 숫자를 구하시오. survived = 1 
# 생존자 숫자 결과는 별칭을 Total로 하시오.  group by sex
select sex, count(survived) as Total from passenger as p
inner join ticket as t on p.PassengerId = t.PassengerId
inner join survived as s on p.PassengerId = s.PassengerId 
where survived = 1 group by sex;

# passenger, ticket, survived 테이블을 INNER JOIN한 데이터에서
# 성별별,  group by Sex
# 생존자의 숫자, 
# 생존자 나이의 평균을 구하시오. 
# 생존자 숫자 결과는 출력 컬럼명을 Total로 하시오.
select sex as 성별, count(survived) as 생존자수, AVG(Age) as 평균나이 from passenger as p
inner join ticket as t on p.PassengerId = t.PassengerId
inner join survived as s on p.PassengerId = s.PassengerId 
where survived = 1 
group by Sex;















































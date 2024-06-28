# SQL 함수
# sql 함수 작동방법
# SELECT 함수(값)
# 절대값 
SELECT ABS(1), ABS(-1);

# 문자열의 길이 측정: LENGTH(문자열);
SELECT LENGTH('mysql');

# 반올림 함수 round()
select round(3.124567, 2);

# 숫자형 함수 +, -, *, /, %(나머지) mod, div(몫만 반환)
select 7 / 2; 
select 7 % 2; # 나머지 반환
select 7 mod 2; # 나머지 반환
select 7 div 2; # 몫만 반환 

# 올림ceil,  내림 floor   4.5
select ceil(4.5);  # 올림
select floor(4.5); # 내림

# 제곱, 루트, 음수양수 확인
select power(4, 3); # 제곱
select sqrt(3); # 루트
select sign(5), sign(-7); # 양수면 1반환, 음수면 -1 반환

# round(값, 자릿수) 반올림 
select round(3.1234567); # 자릿수 지정을 안하면 소숫점 없음.
select round(3.1234567, 2); 

# truncate(값, 자릿수) 버림
select round(2.2345, 3), truncate(2.2345, 3);
select round(1153.456, -2), truncate(1153.456, -2);

# 문자형 함수
# 문자의 길이를 알아보는 함수
select char_length('sql'), length('sql'), char_length('홍길동'), length('홍길동');
# 문자를 연결하는 함수 concat(), concat_ws()
select concat('this', 'is', 'MySQL') as concat1; # 공백 없이 문자를 합침
select concat('this', null, 'MySQL') as concat1; # 중간에 null이 있으면 null이 됨
select concat_ws(' : ', 'this', 'is', 'MySQL') as concat3;

# 대문자를 소문자로 소문자를 대문자로 
select lower('ABcd');
select upper('ABcd');

# lpad, rpad문자열의 자릿수를 일정하게 하고 빈공간을 지정한 문자로 채우기 
# lpad(값, 자릿수, 채울문자), rpad(값, 자릿수, 채울문자)
select lpad('SQL', 7, '#');
select lpad('SQL', 7, '$');
select rpad('SQL', 7, '#');
select rpad('SQL', 7, '*');

# 공백을 없애는 함수. ltrim(문자열), rtrim(문자열)
select ltrim('    SQL    ');
select rtrim('    SQL    ');

# 문자열을 잘라내는 함수 left(문자열, 길이), right(문자열, 길이)
select left('this is my sql', 4), right('this is my sql', 3);

# 문자열의 중간에서 잘라내는 함수 substr(문자열, 시작위치, 길이)
select substr('this is mysql', 6, 2);
select substr('this is mysql', 6); # 길이 부분을 생략하면 시작위치 이후 모두

# 문자열의 공백을 앞 뒤로 삭제하는 trim()
select trim('    mysql    ');
select trim(leading '*' from '****mysql****'); # 문자열 앞쪽의 *을 없앰.
select trim(trailing '*' from '****mysql****'); # 문자열 앞쪽의 *을 없앰.
select trim(both '*' from '****mysql****'); # 문자열 앞쪽의 *을 없앰.

# 날짜형 함수
select curdate(); # 현재 년월일
select curtime(); # 현재 시간
select now(); # 현재 년월일 + 현재 시분초
select current_timestamp(); # 현재 년월일 + 현재 시분초

# 요일 표시 함수 dayname(날짜)
select dayname(now());

#몇 번째 일인지 dayofweek(날짜) 일(1)월(2)화(3)수(4)목(5)금(6)토(7)
select dayofweek(now());

# 1년 중 오늘이 몇일째인지 dayofyear(날짜)
select dayofyear(now());

# 날짜를 세분화 해서 보는 함수들
# 현재 달의 마지막 날이 몇 일까지 있는지 출력
select last_day(now());
select last_day('2024-02-10');
# 입력한 날짜에서 연도만 추출
select year(now());
# 입력한 날짜에서 달만 추출
select month(now());
# 몇 분기인지 출력
select quarter(now());
# 몇 주차인지
select weekofyear(now());

# 날짜와 시간이 같이 있는 데이터에서 날짜따로 시간따로 구부해 주는 함수
select now();
select date('2024-06-27 17:23:30');
select time('2024-06-27 17:23:30');

# 날짜를 지정한 날 수 만큼 더하는 함수 date_add(날짜, interval 더할 날 수 day)
select date_add(now(), interval 5 day);
select adddate(now(), 5); 

# 날짜를 지정한 날 수 만큼 빼는 함수 
# subdate(날짜, interval 뺄 날 수 day),  subdate(날짜, 뺄 날 수)
select subdate(now(), 5);

# 날짜와 시간을 년월, 날시간, 분초 단위로 추출하는 함수
# extract(옵션, from 날짜시간)
select extract(year_month from now());
select extract(DAY_HOUR from '2024-06-27 17:35:30');
select extract(minute_second from '2024-06-27 17:35:30');
select extract(minute_second from now());

# 날짜 1에서 날짜 2을 뺀 일 수를 반환
# datediff(날짜1, 날짜2)
select datediff(now(), '2024-06-25');

# 날짜 포멧 함수 지정한 형식에 맞춰서 출력해주는 함수
# %Y 4자리 연도, %y 2자리 연도
# %m 2자리 월 표시, %M 월의 영문 표기, %b 월의 축약 영문표기 Jan
# %d 2자리 일 표기, %e 1자리 일 표기

select date_format(now(), '%d-%b-%Y');
select date_format(now(), '%Y-%b-%d');
select date_format('2024-06-01', '%Y-%M-%e');

# 시간 포멧 
# %H 24시간 표기, %h 12시간 표기, %p AM, PM 표시
# %i 2자리 분 표기
# %S 2자리 초
# %T 24시간 표기법 시:분:초
# %r 12시가 표기법 시:분:초 AM/PM
# %W 요일의 영문표기, %w 숫자로 요일 표시











































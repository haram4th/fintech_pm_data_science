// document.write("자바스크립트 외부 링크 테스트");

/* document.write("자바스크립트 외부 링크 테스트");
document.write("자바스크립트 외부 링크 테스트");
document.write("자바스크립트 외부 링크 테스트"); */

// 주석은 1줄 주석 //, 여러 줄 주석 /* */

// 변수: 자료를 넣는 상자, 1개만 담을 수 있음, 나중에 담은 것으로 대체
// let 변수명 - 자료를 업데이트 할 수 있다.
// const 변수명 - 처음 선언할 때만 자료를 넣을 수 있고, 업데이트가 안됌.
// 변수 이름 만드는 법: 카멜 표기법 - 시작은 소문자 다른 단어가 붙으면 그 단어는 대문자로
// myName, finalResult

// let: 같은 이름의 변수를 생성 X

let num; //num이라는 이름의 변수 선언 빈박스 만듬.
num = 10; //num 이라는 박스에 10이라는 자료를 넣음. 자료 할당
         //  = 는 오른쪽에 있는 자료를 왼쪽에 넣는다(할당한다)는 뜻.

let num2 = 20; // 변수를 선언 함과 동시에 자료 할당
num2 = 30;
num = 50;

// console.log(num);  // 웹브라우저의 개발자도구의 console에 출력
// document.write(num + num2);  // 웹브라우저의 html 화면에 출력

// const: 상수형 변수, 같은 이름의 변수 생성 X, 선언 후 할당 X
         // 선언과 동시에 값을 할당

// const num3;  // 선언만 했기 때문에 오류
const num3 = 30;
// document.write(num3)

// num3 = 40; // const 변수에 재할당을 하려고 해서 에러

let num4 = 50;
const num5 = 100;
let result = num4 * num5;
// document.write(result);

// 자료형
// 숫자형(정수, 실수), 문자형, 논리형(true, false)
// 배열 array[숫자, 문자, 함수, 객체리터럴]  순서가 있다. 인덱싱, 슬라이싱
// 객체 리터럴, JSON, {key : value}

// 숫자형
num = 10; //정수형
num2 = 3.14 // 실수형
num4 = 3;
let num6 = 2;
// console.log(num*num2);    // 정수 * 실수 = 실수
// console.log(num / num2);  // 정수 / 실수 = 실수
// console.log(num / num4);  // 정수 / 정수 = 소숫점이 있어 실수
// console.log(num / num6);  // 정수 / 정수 = 정수

// 문자형
let string1 = "hello";
let string2 = 'javascript';
// console.log(string1);
// console.log(string1+string2);  // 문자 + 문자 = 연결됨
// console.log(string1+" "+string2);  // 공백도 1개의 문자임. 문자 + 공백문자 + 문자

// 이스케이프 문자
// console.log(string1+"\t"+string2);
// console.log(string1+"\n"+string2);
// console.log(string1+" \'"+string2+"\'");
// console.log(string1+" \""+string2+"\"");

// 템플릿 문자열 (백틱 `  `)
// let string3 = `템플릿 문자열은 큰 따옴표(")나 작은 따옴표(')가 아닌 백틱으로(\`)문자열을 만듭니다.`;
// console.log(string3);
// let string4 = `템플릿 문자열은 \$\{\}을 이용해서 변수의 내용을 바로 출력 가능
//               num : ${num}`;
// console.log(string4);
// console.log(`num + num2 = ${num+num2}`);

// 배열 array: 여러 개의 자료가 나열되어 있는 형태의 자료형
// [] 대괄호 안에 여러개의 다른 데이터형의 자료도 넣을 수 있음
// 순서가 있는 자료형, 순서에 맞추어 인덱스 번호 부여
// 인덱스 번호로 자료를 호출 가능, 범위를 지정해서 호출도 가능
let koreanScore = 80;
let englishScore = 70;
let mathScore = 90;
let scienceScore = 60;

let studentScore = [80, 70, 90, 60]; // 국어, 영어, 수학, 과학 점수. 객체. object.
let arrayValues = [80, 3.14, "배열", [1,'신기해', [1,2,3],{배열:'array'}]]; // 국어, 영어, 수학, 과학 점수. 객체. object.
// console.log(studentScore);
// console.log(arrayValues);

//배열은 순서가 있다. 배열 안에 있는 자료를 꺼내는 방법
// 0번부터 번호가 순서대로 매겨짐 
// 배열 안의 자료를 꺼내는 방법은 배열 변수명[번호]
// console.log(studentScore[1]); // 번호가 0번부터 시작하기 때문에 1번은 70
// console.log(studentScore[0]); 
// console.log(arrayValues[2]); 
// arrayValues에서 신기해를 출력해 보세요.
// console.log(arrayValues[3][2]); 

//객체 리터럴 JSON
// {key : value}
// key를 호출 하면 value가 출력됨.
// ['홍길동', 서초, 14]
// {name : '홍길동', school : '서초', age : 14}
let addressList = {name : '홍길동', school : '서초', age : 14};
// console.log(addressList);
let addressList2 = {name : ['홍길동', '둘리', '트와이스'], 
                  school : ['서초', '강남', '성남'], 
                  age : [14, 15, 16]};
// console.log(addressList2);
// 객체 리터럴의 자료를 꺼내는 방법: key를 호출한다. [key]
// console.log(addressList2['name'][2]);
// 객체 리터럴의 자료를 꺼내는 방법: key를 호출한다. .key
// console.log(addressList2.name[2]);

// 형변환: 자료형을 바꾸는 것
// 암시적 형변환
// const numChar = 10 + "10"; //자바스크립트에서는 숫자와 문자 연산을 하면 자동으로 문자 변환
// console.log(numChar);
// const numChar2 = 10 + "StingChar"; //자바스크립트에서는 숫자와 문자 연산을 하면 자동으로 문자 변환
// console.log(numChar2);

// let strNum = "10";
// num = 10;
// if(num == strNum){  //strNum은 문자이지만 숫자형태라서 숫자 10과 비교시 숫자로 자동변환
//     console.log("같음");
// }

// let strNum2 = "10";
// num = 10;
// if(num === strNum2){  //strNum은 문자이지만 숫자형태라서 숫자 10과 비교시 숫자로 자동변환
//     console.log("같음");
// }else{
//     console.log("다름");
// }

// Number() 문자를 숫자로 변환, String() 숫자를 문자로 변환
// let strNum3 = "10";
// num = 10;
// if(num === Number(strNum3)){  //strNum은 문자이지만 숫자형태라서 숫자 10과 비교시 숫자로 자동변환
//     console.log("같음");
// }else{
//     console.log("다름");
// }

// 연산자 +, -, *, /, ,%, **, 
// 단항 산술 연산자 ++, -- 후치연산, 전치연산  
let a = 1;
let b = 1;
// console.log("a+b: ", a+b);
// console.log("a++ + b++: ", a++ + b++);  // ++ 1증가  -- 1감소
// ++a는 a를 먼저 1 증가 후 +연산
// a++는 먼저 더하기 후 1 증가시켜 내보냄
// console.log("a++ + b++: ", a, "+", b, ": ", ++a + b++);
// console.log(a, "+", b, ": ", a + b);
// console.log(a, "+", b, ": ", a + b);

// 비교연산자
//  == : x, y의 값이 같으면 true
//  === : x, y의 값과 자료형이 같으면 true
//  != : x, y의 값이 다르면 true
//  !== : x, y의 값과 자료형이 다르면 true

// 논리 연산자
// && : and연산 x가 참, y도 참 = 참
// || : or연산 x나 y 둘 중 하나만 참이면 = 참
//  console.log(1 == "1" && "10" == 10);
//  console.log(1 == "1" && "10" === 10);

//  삼항 연산자 x? y : z  x냐? 참 y, 거짓 z
let score = 89;
let grade = score >= 90? 'A+' : 'B';
// console.log(grade);

// 조건문 다루기 if else, else if
/* if (조건) {
     참 일때 실행문
   } else {
     거짓일 때 실행문 
   } */
// num = 9;
// if (num % 2 === 0) {
//     console.log("숫자는 짝수입니다.")
// } else {
//     console.log("숫자는 홀수입니다.")
// }

// num = '십';
// if (num % 2 === 0) {
//     console.log("숫자는 짝수입니다.")
// } else if (num % 2 === 1) {
//     console.log("숫자는 홀수입니다.")
// } else {
//     console.log("입력이 잘못 되었습니다.")
// }

// 반복문 for , for.. in
// for(let i = 0; i < 5 ; i++) {
//    반복 시킬 명령/문장
//  }
// for (let i = 0; i < 4; i++){
//     console.log(i, studentScore[i]);
// }

// 중첩 반복문: 반복문 안에 반복문이 또 있는 것.
// 안쪽 반복문이 다 돌고 바깥쪽이 돌아감.
// 바늘시계 초 -> 분 -> 시
// for (let i = 0; i <= 12; i++){
//     // console.log(`${i}시`);
//     for(let j = 0; j <= 59; j++)
//         // console.log(`${i}시 ${j}분`);
//         for(let k = 0; k <= 59; k++)
//             console.log(`${i}시 ${j}분 ${k}초`);
// }

// for ... in 반복문 array와 함께 사용
// for(let index in studentScore) {
//     console.log(studentScore[index]);
// }

// for ... in 반복문 객체 리터럴(json)과 함께 사용
// console.log(addressList);
// for(let keyName in addressList){
//     console.log(keyName, addressList[keyName]);
// }

// console.log(addressList2);
// for(let keyName in addressList2){
//     // console.log(keyName), addressList2[keyName];
//     for(let index in addressList2[keyName]){
//         console.log(keyName, addressList2[keyName][index]);
//     }
// }

// break, continue문
// break: 특정 조건을 만나면 반복을 중단 시킬때
// for(let i = 0; i <= 100; i++){
//     console.log(i);
//     if(i === 10){
//         break;
//     }
// }

// continue: 특정 조건을 만나면 건너뜀
// 1-100까지 수 중에서 홀수만 출력하시오.
// for(let i = 1; i <= 100; i++){
//     if(i % 2 === 1){
//         console.log(i);
//     } else {
//         continue;
//     }
// }

// 함수 function 함수명(인자 값){
//          인자 값 받아서 처리하는 코드
//          return 값
//    }

// 함수명(값)
// console.log(String(num));
// function gugudan(){
//     for(let i = 1; i <= 9; i++){
//         console.log(`3 * ${i} = ${3*i}`);
//     }
// }
// gugudan();

// 함수 만들기
// function gugudan(num){
//     for(let i = 1; i <= 9; i++){
//         console.log(`${num} * ${i} = ${num*i}`);
//     }
// }
// gugudan(7);

// 함수 표현식
// const 변수명 = function 함수명() {
//         인자 값 받아서 처리하는 코드
//     }
// const fn1 = function gugudan(num){
//     for(let i = 1; i <= 9; i++){
//         console.log(`${num} * ${i} = ${num*i}`);
//     }
// }
// fn1(7);

// const 변수명에 함수를 담으면서 함수명을 삭제
// 함수 표현식 익명 함수
// const fn2 = function (num){
//     for(let i = 1; i <= 9; i++){
//         console.log(`${num} * ${i} = ${num*i}`);
//     }
// }
// fn2(7);

// 화살표 함수
// const fn3 = (num) => {
//     for(let i = 1; i <= 9; i++){
//         console.log(`${num} * ${i} = ${num*i}`);
//     }
// }
// fn3(6);

// return

const calcSum = (num1, num2) => {
    result = num1 + num2;
    return result;
}
let sumResult = calcSum(6, 3)
// console.log(sumResult)

// 2개의 숫자를 입력해서 그 사이에 있는 숫자중에서 홀수인 수만 출력하고 리턴

// const hol = (num1, num2) => {
//     let arr = []
//     for(num1; num1 <= num2; num1++){
//         if(num1 % 2 === 1){
//             console.log(num1);
//             arr.push(num1);
//         }
//     }
//     return arr;
// }

// let holResult = hol(5, 77)
// console.log(holResult);

// 브라우저 객체 모델 사용하기
function popup() {
    window.open('http://www.naver.com', '팝업', 'width=200', height='100')
}

const el = document.querySelector(".box-1");
el.style.color = "red";
console.log(el);

# investment-REST-API
원티드 프리온보딩 백엔드 기업 과제

## 목차
1. [프로젝트 개요](#프로젝트-개요)
2. [프로젝트 기술 스택](#프로젝트-기술-스택)
3. [개발 기간](#개발-기간)
4. [팀 구성](#팀-구성)
5. [역할](#역할)
6. [ERD](#ERD)
7. [API 목록](#API-목록)
8. [프로젝트 시작 방법](#프로젝트-시작-방법)


<br>


## 프로젝트 개요
고객 투자 데이터를 응답하는 DJango 기반의 REST API


<br>

## 과제 요구사항 분석
### 1. 구현사항 상세설명

- 특정 고객 자산 정보를 조회하는 API
1. 투자 회면 API
 - InvestmentHomeView
 - GET /api/v1/invest/home/
 - 토큰을 통해 유저정보를 받아 고객이름, 계좌명, 증권사. 계좌번호, 계좌 총 자산 총 5가지 항목 반환
2. 투자 상세 화면 API
 - InvestmentDetailView
 - GET /api/v1/invest/detail/
 - 고객이름, 계좌명, 증권사, 계좌번호, 계좌 총 자산, 투자 원금, 총 수익금, 수익률 8개 데이터 반환
 - 총 수익률의 경우 결과물이 소수점 으로 나올경우 소수점 2자리 까지 표기기능 구현
3. 보유종목 화면 API 
 - HoldingsView
 - GET /api/v1/invest/holdings/
 - 고객이름, 보유 종목명, 보유 종목의 자산그룹, 보유 종목의 평가 금액, 보유 종목 ISIN 5개 데이터 반환
4. 입금거래 정보 저장 API
 - CreateTradeInfo
 - POST /api/v1/invest/trade/
 - 정상적으로 입금시 id 반환
 - 입금거래 정보 유효성검사진행
   - 검사1 : 계좌번호 확인
   - 검사2 : 계좌번호와 고객이름 매칭 
 - 입급거래 정보 저장시 조회를 먼저해보고 있으면 에러처리 없을때만 저장하도록 구현 
5. 등록한 거래정보 검증 후 실제 고객의 자산 업데이트 API
 - UpdateUserAssetView
 - POST /api/v1/invest/asset/
 - 계좌번호 + 고객이름 + 투자금액 을 sha512로 만든 해시값과 기존 입금거래정보 의 계좌번호 + 고객이름 + 투자금액을 sha512로 해시한값과 비교후에 맞다면 투자원금에 투자금액을 더하는 기능 구현
 - 투자금액을 더한뒤 기존에 있던 입금거래정보는 삭제
6. 로그인 기능 추가
 - SignUpView
 - rest_framework의 simple-jwt 모듈을 활용해 토큰 생성 및 인증인가 처리 기능 구현
7. Batch
 - 매일 변경되는 데이터셋을 읽어 DB데이터를 업데이트 기능
 - 매일 업데이트되는 데이터를 API에서 사용가능하도록 정제하여 Django의 manage.py의 command를 이용하여 Batch 가능하도록 구현
 - 엑셀 데이터를 읽는 것은 pandas를 활용
 - 데이터는 루트 디렉토리에 data 디렉토리에서 가져와 
8. 스캐쥴러
 - 작성된 Batch파일을 정기적으로 실행시켜줄 스케쥴러 기능 구현
 - django-crontab 라이브러리를 활용하여 기능 구현
 - 현재 매 1분마다 스캐쥴러로 Batch파일 실행하도록 구현

<br>

## 프로젝트 기술 스택

### Backend
<section>
<img src="https://img.shields.io/badge/Django-092E20?logo=Django&logoColor=white"/>
<img src="https://img.shields.io/badge/Django%20REST%20Framework-092E20?logo=Django&logoColor=white"/>
</section>

### DB
<section>
<img src="https://img.shields.io/badge/MySQL-4479A1?logo=MySQL&logoColor=white"/>
</section>

### Tools
<section>
<img src="https://img.shields.io/badge/GitHub-181717?logo=GitHub&logoColor=white"/>
<img src="https://img.shields.io/badge/Discord-5865F2?logo=Discord&logoColor=white">
<img src="https://img.shields.io/badge/Postman-FF6C37?logo=Postman&logoColor=white">
</section>
<!-- | 백엔드 | DB   |  Tools   |
| ---- | ------ | --- |
|      |        |    | -->


<br>


## 개발 기간
- 2022/09/16~2022/09/21 (주말제외 4일)


<br>


## 팀 구성
| 김현수 | 유혜선 | 임한구 |  최보미  |
| ------ | ------ | ------ | --- |
| [Github](https://github.com/HyeonsooKim) | [Github](https://github.com/Hyes-y)   | [Github](https://github.com/nicholas019/)   |  [Github](https://github.com/BomiChoi)   |


<br>


## ERD



<br>


## API 목록
API 명세 주소

<br>


## 프로젝트 시작 방법
1. 로컬에서 실행할 경우
```bash
# 프로젝트 clone(로컬로 내려받기)
git clone -b develop --single-branch ${github 주소}
cd ${디렉터리 명}

# 가상환경 설정
python -m venv ${가상환경명}
source ${가상환경명}/bin/activate
# window (2 ways) 
# 1> ${가상환경명}/Scripts/activate
# 2> activate

# 라이브러리 설치
pip install -r requirements.txt

# 스케쥴러 실행
python manage.py crontab add

# django 실행
python manage.py runserver
```

<br>

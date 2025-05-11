맥스웰-볼츠만 분포를 주식 매매에 적용하기 위한 프로젝트

# 개념(에너지 ↔ 변동성/거래량)
 1. 입자의 에너지 ↔ 주가의 가격 움직임 강도 (변동성)
 2. 속도가 많은 입자가 평균치 근처에 몰려 있는 특성 ↔ 가격이 이동 평균 근처에 자주 위치
 3. 극단적인 고속 입자는 드물다 ↔ 급등·급락은 확률적으로 적다

# 기술적 응용 예시
A. 가격 움직임 분포를 확률 밀도로 모델링
  일정 기간 동안의 수익률(returns) 분포를 계산
  그 분포를 맥스웰-볼츠만 함수형으로 피팅
  이를 통해 **변동성이 어느 정도면 "정상", 어느 정도면 "이례적"**인지 판단
  수식 예시 (맥스웰 분포):
  f(v) = \left( \frac{m}{2\pi kT} \right)^{3/2} \cdot 4\pi v^2 \cdot e^{-mv^2 / 2kT}
  ]
  이를 변형하여,
  f(x) = A x^2 e^{-B x^2}
  ]
  의 형태로 수익률 분포에 피팅 가능

B. 거래량의 '활성 에너지' 해석
  거래량이 많을수록 '에너지가 높은 입자 상태'에 대응
  일정 거래량 이상에서만 큰 가격 이동이 발생하는 경향이 있다면, 이를 **임계 에너지(threshold energy)**처럼 해석 가능

C. '정상 분포 vs 볼츠만 분포'로 가격 패턴 진단
  일반적으로 가격 변화는 정규분포에 가깝다고 가정하지만, 실제는 fat tail을 가지는 분포
  맥스웰-볼츠만형 곡선으로 피팅하면 **극단값(꼬리)**의 영향을 더 잘 반영할 수 있음

# 적용할 부분
1. 수익률 분포 분석 : 히스토그램 + 볼츠만 분포 피팅
2. 변동성 경계값 측정 : 평균 에너지 이상이면 '비정상 구간'으로 간주

# 프로젝트 구성
```
stock/
├── main.py                            # 메인 메뉴 실행 진입점
│
├── commands/                          # 사용자 실행용 CLI 명령 스크립트
│   ├── backtest_strategy.py          # 백테스트 실행
│   ├── calc_indicators.py            # 기술 지표 계산 후 저장
│   ├── fetch_and_save.py             # 주가 수집 후 DB 저장
│   ├── register_ticker.py            # 티커 등록
│   ├── view_prices.py                # 주가 데이터 조회
│   └── view_tickers.py               # 등록된 티커 조회
│
├── db/
│   └── mysql_connector.py            # MySQL DB 커넥션 헬퍼
│
├── services/
│   ├── indicator_calculator.py       # 지표 계산 통합 컨트롤러
│   ├── backtester.py                 # 맥스웰 분포 기반 백테스트 로직
│   ├── analyzer.py                   # 수익률 계산 및 분포 피팅
│   ├── fetcher.py                    # yfinance를 통한 주가 수집
│   ├── inserter.py                   # 일별 주가 DB 저장 처리
│   ├── ticker_manager.py             # 티커 등록 및 조회 로직
│	│
│   ├── indicators/                   # 💡 지표별 계산 모듈
│   │   ├── rsi.py                    # RSI 계산
│   │   ├── macd.py                   # MACD + 시그널 + 히스토그램
│   │   ├── bollinger.py              # 볼린저 밴드 계산
│   │   └── ichimoku.py               # 일목균형표 계산
│	│
│   └── data_access/                  # DB 접근 전용 모듈
│       ├── price_mapper.py          # daily_price 테이블 조회
│       ├── indicator_mapper.py      # technical_indicators 저장
│       └── ticker_mapper.py       	 # 티커 관련 SQL 쿼리 모음
│
├── utils/
│   └── table_formatter.py           # 콘솔 출력용 정렬 유틸 (한글 너비 대응)

```

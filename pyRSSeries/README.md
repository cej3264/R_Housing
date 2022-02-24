# pyRSSeries
RS232C_MISUMI 제어 파이썬 API ※ 프로토콜을 RS232C_통신 프로토콜.pdf를 참조

## 사용방법
### 0. 환경 세팅
1. 가상환경 세팅
2. 패키지 설정: pip install -r requirements.txt

### 1. 지원 기능
    1. move(point, node): node를 point로 이동
    2. stop(node): node의 operation/movement를 정지
    3. stauts(node): node의 status를 출력 및 저장
    4. action(msg): msg를 실행
    5. close(): robot을 정지

### 2. 예시
    추후 추가
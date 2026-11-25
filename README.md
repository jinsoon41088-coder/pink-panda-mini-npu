
# 🐼 Pink Panda Mini NPU Simulator

## AI가 계산하는 방식을 흉내 내는 작은 계산기 만들기

### 📌 1. 프로젝트 소개

이 프로젝트는 AI가 숫자 데이터를 이용하여 그림의 모양을 판별하는 원리를 이해하기 위해 제작한 Mini NPU 시뮬레이터입니다.

Python을 이용하여 입력 패턴과 필터를 곱하고 더하는 MAC 연산을 구현하고, 십자가(+)와 X 모양을 판별하도록 제작했습니다.

### 💻 2. 개발 환경

- 운영체제: Windows 11
- 개발 언어: Python
- 개발 도구: Visual Studio Code
- 터미널: PowerShell
- 데이터 형식: JSON
- 버전 관리: Git
- 원격 저장소: GitHub

### 🎯 3. 프로젝트 학습 목표

- MAC 연산의 개념과 원리 이해
- 입력 패턴과 필터의 유사도 계산
- JSON 데이터의 키 규칙 이해
- 라벨 정규화의 필요성 이해
- 부동소수점 오차 이해
- EPSILON 허용오차 기반 판정
- 크기별 연산 시간 측정
- 시간 복잡도 O(N²) 이해
- 실패 케이스 및 데이터 오류 분석

### 🧮 4. MAC 연산이란?

MAC은 Multiply-Accumulate의 약자로,
곱셈과 누적 덧셈을 의미합니다.

입력 패턴과 필터의 같은 위치에 있는 숫자를
서로 곱한 후 모든 결과를 더하는 방식입니다.

예시:

1 × 1 + 0 × 0 + 1 × 1 = 2

AI는 이러한 계산을 반복하여 입력 데이터의
특징을 분석합니다.

### ➕ 5. 십자가와 X 패턴 판정 원리

십자가 패턴:

    0 1 0
    1 1 1
    0 1 0

X 패턴:

    1 0 1
    0 1 0
    1 0 1

입력 패턴과 십자가 필터, X 필터를 각각
MAC 연산하여 점수를 계산합니다.

- 십자가 점수가 높으면 십자가로 판정
- X 점수가 높으면 X로 판정
- 두 점수의 차이가 허용오차보다 작으면 UNDECIDED

### 📂 6. JSON 데이터 구조

data.json은 filters와 patterns로 구성됩니다.

| 패턴 이름 | 배열 크기 | 정답 |
|---|---|---|
| size_5_1 | 5×5 | + |
| size_5_2 | 5×5 | x |
| size_13_1 | 13×13 | + |
| size_13_2 | 13×13 | x |
| size_25_1 | 25×25 | + |
| size_25_2 | 25×25 | x |

키 이름의 크기 정보와 실제 배열의 크기가
일치하는지 검사합니다.

### 🔄 7. 라벨 정규화

같은 의미를 가진 여러 표현을 하나의
표준 표현으로 통일합니다.

| 입력 라벨 | 정규화 결과 |
|---|---|
| cross | + |
| CROSS | + |
| A | + |
| + | + |
| x | x |
| X | x |
| B | x |
| UNDECIDED | UNDECIDED |
| 지원하지 않는 라벨 | UNKNOWN |

라벨 정규화를 통해 표현 방식의 차이로
발생하는 잘못된 판정을 방지합니다.

### 🔢 8. 부동소수점 오차와 EPSILON

컴퓨터는 일부 소수를 정확하게 표현하지 못합니다.

예시:

    0.1 + 0.2 = 0.30000000000000004

이러한 미세한 계산 오차를 처리하기 위해
EPSILON이라는 허용오차를 사용했습니다.

    EPSILON = 1e-9

두 점수의 차이가 EPSILON보다 작으면
UNDECIDED로 판정합니다.

### ⏱️ 9. MAC 연산 시간 및 시간 복잡도

| 배열 크기 | MAC 반복 횟수(1회 연산) | 평균 연산 시간 측정 예시 |
|---|---:|---:|
| 3×3 | 9 | 0.000720 ms |
| 5×5 | 25 | 0.003355 ms |
| 13×13 | 169 | 0.011757 ms |
| 25×25 | 625 | 0.031468 ms |

#### MAC Benchmark Analysis

- Each MAC timing test is repeated 1,000 times.
- Only the MAC function execution time is measured.
- The average time is calculated in milliseconds.
- A 3x3 matrix requires 9 MAC operations.
- A 5x5 matrix requires 25 MAC operations.
- A 13x13 matrix requires 169 MAC operations.
- A 25x25 matrix requires 625 MAC operations.
- Nested loops process N*N matrix elements.
- Therefore, the time complexity is O(N^2).
- Doubling N increases the operation count fourfold.


배열의 크기가 N×N이면 모든 원소를
검사하기 위해 N²번의 반복이 필요합니다.

따라서 MAC 연산의 시간 복잡도는 O(N²)입니다.

실제 연산 시간은 컴퓨터 환경과 실행 상태에
따라 달라질 수 있습니다.

### 🔍 10. 실패 케이스 및 오류 처리

다음과 같은 오류를 검사하도록 구현했습니다.

- 배열 크기 불일치
- 잘못된 키 이름
- 숫자가 아닌 데이터
- NaN 및 Infinity
- 지원하지 않는 패턴 크기
- 지원하지 않는 정답 라벨
- 실제 판정과 정답의 불일치

Data errors and label mismatches are both counted as FAIL.
Data errors are also reported separately as a subset of failures.


#### Failure Report Policy

- All data errors are counted as FAIL.
- Data errors are a subset of total failures.
- Total cases = PASS cases + FAIL cases.
- Invalid case data does not stop the remaining tests.
- Failed case identifiers and reasons are recorded.
- Label mismatches show actual and expected labels.
- Data errors show detailed error messages.
- If all cases pass, the report shows No failed cases.

### 🎮 11. 프로그램 실행 방법

터미널에서 다음 명령어를 실행합니다.

    python main.py

프로그램 실행 메뉴:

    🐼 Pink Panda Mini NPU Simulator

    1. User Input (3x3)
    2. Local Dataset Analysis
    3. Official Dataset Analysis
    4. Exit

- Mode 1: Enter 3x3 matrices and calculate MAC scores.
- Mode 2: Analyze the local dataset (data.json).
- Mode 3: Analyze the official dataset (data-official.json).
- Mode 4: Exit the program.
- Invalid menu selections display an error message.


### 📊 12. 최종 실행 결과

    =============================================
    🐼 Pink Panda Mini NPU 최종 분석 결과
    =============================================
    전체 검사: 6개
    성공: 6개
    실패: 0개
    데이터 오류: 0개
    판정 정확도: 100.00%
    =============================================

준비한 정상 패턴 데이터 6개를 모두
올바르게 판정했습니다.

### 📁 13. 프로젝트 파일 구성

    pink-panda-mini-npu/
    ├── main.py
    ├── data.json
    ├── README.md
    └── .gitignore

- main.py: Mini NPU 프로그램 실행 코드
- data.json: 필터 및 입력 패턴 데이터
- README.md: 프로젝트 설명 및 사용 방법
- .gitignore: Git 추적 제외 파일 설정

### 📸 14. 프로그램 실행 스크린샷

#### 14-1. 프로그램 메인 메뉴
![메인 메뉴](screenshots/mini-npu-main-menu.png)

#### 14-2. 사용자 입력 및 MAC 연산
![사용자 입력](screenshots/mini-npu-user-input-mac.png)

#### 14-3. 5×5 패턴 분석
![5x5 패턴](screenshots/mini-npu-pattern-5x5.png)

#### 14-4. 13×13 패턴 분석
![13x13 패턴](screenshots/mini-npu-pattern-13x13.png)

#### 14-5. 25×25 패턴 분석
![25x25 패턴](screenshots/mini-npu-pattern-25x25.png)

#### 14-6. 크기별 평균 MAC 연산 시간
![MAC 연산 시간](screenshots/mini-npu-mac-timing.png)

#### 14-7. EPSILON 허용오차 검사
![EPSILON 검사](screenshots/mini-npu-epsilon-test.png)

#### 14-8. 잘못된 데이터 오류 처리
![데이터 오류 검사](screenshots/mini-npu-error-test.png)

#### 14-9. 최종 판정 정확도 100%
![최종 분석 결과](screenshots/mini-npu-final-result.png)

#### 14-10. GitHub 업로드 결과
![GitHub 업로드](screenshots/mini-npu-github-upload.png)

### 🌱 15. 미션을 통해 배운 점

이번 미션을 통해 AI가 그림을 사람처럼 직접
인식하는 것이 아니라 숫자 데이터로 변환하여
계산한다는 원리를 배웠습니다.

MAC 연산, JSON 데이터 처리, 라벨 정규화,
부동소수점 오차, 시간 복잡도의 개념을
직접 프로그램을 만들면서 학습했습니다.

코드를 작성하는 과정에서 발생한 오류를
하나씩 확인하고 해결하는 경험도 했습니다.

또한 Git과 GitHub를 이용하여 개발 과정과
완성된 프로그램을 기록하는 방법을 익혔습니다.

---

🐼 Pink Panda Mini NPU Project

포기하지 않고 한 단계씩 성장하는 개발 공부!

### 16. 결과 리포트 (Result Report)

1. All six local test patterns passed successfully.
2. The normal test accuracy was 100.00%.
3. No failures or data errors occurred in the normal test.
4. Label normalization converts + and x to Cross and X.
5. EPSILON is set to 1e-9 to handle small numerical differences.
6. The error test intentionally introduced two failed cases.
7. The error test produced four PASS and two FAIL results.
8. The error test accuracy was 66.67%.
9. size_5_1 failed because the expected label was incorrect.
10. size_5_2 failed because the matrix size was invalid.
11. Data errors are included in the total FAIL count.
12. The failure report records case identifiers and reasons.
13. MAC execution time is measured over 1,000 repetitions.
14. The MAC operation counts are 9, 25, 169, and 625.
15. The MAC time complexity is O(N^2).
16. Execution time increases as the matrix size increases.
17. Official dataset verification is complete.

#### Additional Result Analysis

- All six local patterns matched their expected labels.
- Label normalization prevents mismatches caused by different label formats.
- EPSILON prevents false distinctions between nearly equal scores.
- The normal test patterns did not produce near-tied scores.
- The MAC operation count increases from 9 to 625.
- The operation count increases approximately 69.44 times.
- The measured execution time increases approximately 43.71 times.
- Actual execution time depends on system conditions and measurement overhead.
- The nested loops perform N squared MAC operations.
- Official dataset verification is complete.

### 17. Official Dataset Verification

The official dataset was tested without modifying its original values.

| Dataset | Total | PASS | FAIL | Data Errors | Accuracy |
|---|---:|---:|---:|---:|---:|
| Local dataset | 6 | 6 | 0 | 0 | 100.00% |
| Official dataset | 6 | 3 | 3 | 0 | 50.00% |

#### Official Dataset Results

| Pattern | Actual | Expected | Result |
|---|---|---|---|
| size_5_1 | UNDECIDED | X | FAIL |
| size_5_2 | Cross | Cross | PASS |
| size_13_1 | X | X | PASS |
| size_13_2 | UNDECIDED | Cross | FAIL |
| size_25_1 | UNDECIDED | X | FAIL |
| size_25_2 | Cross | Cross | PASS |

#### Official MAC Benchmark

| Matrix Size | MAC Operations | Average Time |
|---|---:|---:|
| 3x3 | 9 | 0.001042 ms |
| 5x5 | 25 | 0.002625 ms |
| 13x13 | 169 | 0.016709 ms |
| 25x25 | 625 | 0.043371 ms |

#### Verification Evidence

![Official Dataset Result](screenshots/mini-npu-official-result.png)

#### Official Dataset Failure Analysis

| Pattern | Cross Score | X Score | Actual | Expected |
|---|---:|---:|---|---|
| size_5_1 | 0.9 | 0.8999999999999999 | UNDECIDED | X |
| size_13_2 | 7.499999999999997 | 7.5 | UNDECIDED | Cross |
| size_25_1 | 4.9 | 4.899999999999999 | UNDECIDED | X |

1. The official dataset contains six test patterns.
2. Three patterns passed and three patterns failed.
3. The official classification accuracy was 50.00%.
4. No data validation errors occurred.
5. All failed patterns produced nearly equal MAC scores.
6. The score difference was smaller than EPSILON (1e-9).
7. Floating-point arithmetic can introduce tiny numerical differences.
8. EPSILON prevents these differences from causing arbitrary classifications.
9. The simulator correctly returned UNDECIDED for all three near-tied cases.
10. UNDECIDED differs from the expected labels and is counted as FAIL.
11. The failures are related to score ambiguity rather than detected schema errors.
12. The official dataset and expected labels were not modified.
13. The local dataset achieved 100.00% accuracy.
14. The official dataset achieved 50.00% accuracy.
15. Classification accuracy and correct implementation of the comparison policy are separate evaluation criteria.
16. All MAC measurements use 1000 repetitions.
17. The nested MAC loops have O(N^2) time complexity.
18. Execution time increases with the matrix size in this benchmark.
19. Actual execution time may vary depending on system conditions.
20. Both successful and failed results are preserved as verification evidence.

---

### 18. Error Handling Verification

| Test Case | Result |
|---|---|
| Missing JSON file | PASS |
| Invalid JSON format | PASS |
| Missing patterns object | PASS |
| Invalid menu selection | PASS |
| Label mismatch detection | PASS |
| Invalid matrix size detection | PASS |
| Local dataset regression test | PASS |
| Official dataset regression test | PASS |

#### Verification Summary

- Missing files are handled without an unhandled exception.
- Invalid JSON files display an error message.
- Missing patterns objects are detected safely.
- Individual data errors are counted as FAIL.
- Valid patterns continue to be analyzed after individual errors.
- The failure report records pattern identifiers and reasons.
- The intentional error test produced 4 PASS and 2 FAIL results.
- One data error was included in the total FAIL count.
- The intentional error test accuracy was 66.67%.
- The local dataset accuracy remained 100.00%.
- The official dataset accuracy remained 50.00%.
- Original dataset files were not modified during error testing.
- JSON loading supports UTF-8 files with or without BOM.


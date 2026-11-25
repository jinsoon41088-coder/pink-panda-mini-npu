
import json
import time
import math
from pathlib import Path

def mac(pattern, filter_matrix):
    score = 0.0

    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            score += pattern[i][j] * filter_matrix[i][j]

    return score

def classify(score_a, score_b):
    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"
    elif score_a > score_b:
        return "A"
    else:
        return "B"

EPSILON = 1e-9

def input_matrix(name, n=3):
    print(f"\n{name} ({n}줄 입력, 공백 구분)")
    matrix = []

    for i in range(n):
        while True:
            try:
                row = list(map(float, input(f"{i + 1}행: ").split()))

                if len(row) != n:
                    raise ValueError

                if not all(math.isfinite(value) for value in row):
                    raise ValueError

                matrix.append(row)
                break

            except ValueError:
                print(f"입력 형식 오류: 각 줄에 {n}개의 유한한 숫자를 공백으로 구분해 입력하세요.")

    return matrix

def measure_mac(pattern, filter_matrix, repeat=1000):
    total_time = 0.0

    for _ in range(repeat):
        start = time.perf_counter()
        mac(pattern, filter_matrix)
        end = time.perf_counter()

        total_time += (end - start) * 1000

    return total_time / repeat

def user_input_mode():

    print("\n[1] 필터 입력")

    filter_a = input_matrix("필터 A")
    filter_b = input_matrix("필터 B")

    print("\n필터 A, B 저장 완료!")

    print("\n[2] 패턴 입력")

    pattern = input_matrix("입력 패턴")

    print("\n[3] MAC 연산 결과")

    time_a = measure_mac(pattern, filter_a)
    time_b = measure_mac(pattern, filter_b)

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)

    result = classify(score_a, score_b)


    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"A 연산 시간: {time_a:.6f} ms")
    print(f"B 연산 시간: {time_b:.6f} ms")
    average_time = (time_a + time_b) / 2
    print(f"3x3 평균 MAC 연산 시간: {average_time:.6f} ms")
    print("MAC 연산 횟수: 9회")

    print(f"판정: {result}")


def load_json_data(filename="data.json"):
    file_path = Path(__file__).resolve().parent / filename

    try:
        with open(file_path, "r", encoding="utf-8-sig") as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"File not found: {filename}")
    except json.JSONDecodeError:
        print(f"Invalid JSON format: {filename}")
    except UnicodeError:
        print(f"Invalid file encoding: {filename}")
    except OSError as error:
        print(f"File read error: {error}")

    return None


def normalize_label(label):
    label = str(label).strip().lower()

    if label in ("cross", "+", "a"):
        return "Cross"
    elif label in ("x", "b"):
        return "X"
    elif label == "undecided":
        return "UNDECIDED"
    else:
        return "UNKNOWN"
def get_filters(data, key):
    size = int(key.split(chr(95))[1])
    filter_key = f"size_{size}"

    if filter_key not in data["filters"]:
        raise ValueError(f"지원하지 않는 패턴 크기: {size}")

    filters = data["filters"][filter_key]

    return filters["cross"], filters["x"]
def validate_matrix(matrix, size):
    if not isinstance(matrix, list):
        return False

    if len(matrix) != size:
        return False

    for row in matrix:
        if not isinstance(row, list):
            return False

        if len(row) != size:
            return False

        for value in row:
            if type(value) not in (int, float):
                return False

            if not math.isfinite(value):
                return False

    return True
def validate_pattern_key(key, pattern):
    parts = key.split("_")

    if len(parts) != 3:
        return False

    if parts[0] != "size":
        return False

    if parts[1] not in ("5", "13", "25"):
        return False

    if not parts[2].isdigit():
        return False

    size = int(parts[1])

    return validate_matrix(pattern, size)
def json_analysis_mode(filename="data.json"):
    data = load_json_data(filename)
    if data is None:
        print("JSON analysis cancelled.")
        return

    if not isinstance(data, dict):
        print("Invalid JSON structure: root must be an object.")
        print("JSON analysis cancelled.")
        return

    if not isinstance(data.get("patterns"), dict):
        print("Invalid JSON structure: patterns must be an object.")
        print("JSON analysis cancelled.")
        return

    total_count = 0
    pass_count = 0
    fail_count = 0
    failed_cases = []
    error_count = 0
    timing_results = {}

    print("\n[JSON 데이터 자동 분석]")

    for key, item in data["patterns"].items():
        total_count += 1
        try:
            pattern = item["input"]
            expected = normalize_label(item["expected"])
            if expected == "UNKNOWN":
                raise ValueError("지원하지 않는 정답 라벨")
            size = len(pattern)
            if not validate_pattern_key(key, pattern):
                raise ValueError("키 이름 또는 배열 크기 오류")

            filter_a, filter_b = get_filters(data, key)

            if not all(validate_matrix(m, size)
                       for m in (pattern, filter_a, filter_b)):
                raise ValueError("잘못된 배열 데이터")

            score_a = mac(pattern, filter_a)
            score_b = mac(pattern, filter_b)
            time_a = measure_mac(pattern, filter_a, 1000)
            time_b = measure_mac(pattern, filter_b, 1000)
            if size not in timing_results:
                timing_results[size] = []

            timing_results[size].append(time_a)
            timing_results[size].append(time_b)

            result = normalize_label(classify(score_a, score_b))

            status = "PASS" if result == expected else "FAIL"

            if status == "PASS":
                pass_count += 1
            else:
                fail_count += 1
                failed_cases.append((key, result, expected))

            print(f"\n패턴: {key}")
            print(f"크기: {size}×{size}")
            print(f"십자가 점수: {score_a}")
            print(f"X 점수: {score_b}")
            print(f"십자가 연산 시간: {time_a:.6f} ms")
            print(f"X 연산 시간: {time_b:.6f} ms")
            print(f"판정: {result}")
            print(f"정답: {expected}")
            print(f"검사 결과: {status}")

        except (ValueError, KeyError, TypeError) as error:
            error_count += 1
            fail_count += 1
            failed_cases.append((key, str(error), None))
            print(f"{key}: 데이터 오류 - {error}")
    pattern_3 = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    filter_3 = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    timing_results[3] = [measure_mac(pattern_3, filter_3)]
    print("\n[크기별 평균 MAC 연산 시간]")

    for size in sorted(timing_results):
        times = timing_results[size]
        average_time = sum(times) / len(times)
        print(f"{size}x{size}: {average_time:.6f} ms | MAC 연산 횟수: {size ** 2}회")

    accuracy = (pass_count / total_count * 100) if total_count > 0 else 0
    print("\n" + "=" * 45)
    print("🐼 핑크판다 미니 NPU 최종 분석 결과")
    print("=" * 45)
    print(f"전체 검사: {total_count}개")
    print(f"성공: {pass_count}개")
    print(f"실패: {fail_count}개")
    print(f"데이터 오류: {error_count}개")
    print(f"판정 정확도: {accuracy:.2f}%")

    print("\n[실패 리포트]")
    if not failed_cases:
        print("실패 사례 없음")
    else:
        for key, result, expected in failed_cases:
            print(f"[실패(FAIL)] {key}")
            if expected is None:
                print(f"데이터 오류: {result}")
            else:
                print("실패 원인: 정답 라벨 불일치")
                print(f"실제 판정: {result}")
                print(f"예상 정답: {expected}")
    print("=" * 45)
def main():
    print("=" * 45)
    print("🐼 핑크판다 미니 NPU 시뮬레이터")
    print("AI 계산 시뮬레이터")
    print("=" * 45)

    print("\n[메뉴 선택]")
    print("1. 사용자 직접 입력 (3x3)")
    print("2. 로컬 데이터 분석")
    print("3. 공식 데이터 분석")
    print("4. 프로그램 종료")

    choice = input("메뉴 선택: ").strip()
    
    if choice == "1":
        user_input_mode()
    elif choice == "2":
        json_analysis_mode("data.json")
    elif choice == "3":
        json_analysis_mode("data-official.json")
    elif choice == "4":
        print("Program terminated.")
    else:
        print("Invalid menu selection.")


if __name__ == "__main__":
    main()

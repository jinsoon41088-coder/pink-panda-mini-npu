
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

def measure_mac(pattern, filter_matrix, repeat=10):
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

    print(f"판정: {result}")



def main():
    print("=" * 45)
    print("🐼 Pink Panda Mini NPU Simulator")
    print("AI가 계산하는 방식을 흉내 내는 작은 계산기")
    print("=" * 45)

    print("\n[모드 선택]")
    print("1. 사용자 입력 (3×3)")
    print("2. data.json 분석")
    print("3. 프로그램 종료")

    choice = input("선택: ")

 
    if choice == "1":
        user_input_mode()
    elif choice == "2":
        print("JSON 데이터 분석 모드입니다.")
    elif choice == "3":
        print("프로그램을 종료합니다.")
    else:
        print("잘못된 입력입니다.")


if __name__ == "__main__":
    main()

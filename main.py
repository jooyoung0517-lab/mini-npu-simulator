import json


# MAC 연산
def mac_operation(pattern, filter_data):
    score = 0

    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            score += pattern[i][j] * filter_data[i][j]

    return score


# Cross 필터 생성
def create_cross_filter(size):
    filter_data = []
    center = size // 2

    for i in range(size):
        row = []

        for j in range(size):
            if i == center or j == center:
                row.append(1)
            else:
                row.append(0)

        filter_data.append(row)

    return filter_data


# X 필터 생성
def create_x_filter(size):
    filter_data = []

    for i in range(size):
        row = []

        for j in range(size):
            if i == j or i + j == size - 1:
                row.append(1)
            else:
                row.append(0)

        filter_data.append(row)

    return filter_data


# 패턴 판별
def classify_pattern(pattern):
    size = len(pattern)

    cross_filter = create_cross_filter(size)
    x_filter = create_x_filter(size)

    cross_score = mac_operation(pattern, cross_filter)
    x_score = mac_operation(pattern, x_filter)

    epsilon = 1e-9

    if abs(cross_score - x_score) <= epsilon:
        result = "Tie"
    elif cross_score > x_score:
        result = "Cross"
    else:
        result = "X"

    return cross_score, x_score, result


# 3x3 사용자 입력
def get_user_pattern():
    pattern = []

    print("=== Mini NPU Simulator ===")
    print("3 x 3 패턴을 입력하세요.")

    for i in range(3):
        while True:
            row = input(f"{i + 1}번째 줄 숫자 3개 입력: ")
            values = row.split()

            if len(values) != 3:
                print("숫자 3개를 입력해주세요.")
                continue

            if not all(value in ["0", "1"] for value in values):
                print("0과 1만 입력할 수 있습니다.")
                continue

            pattern.append(list(map(int, values)))
            break

    return pattern


# 프로그램 실행
def main():
    user_pattern = get_user_pattern()

    cross_score, x_score, result = classify_pattern(user_pattern)

    print("=== 사용자 패턴 판별 결과 ===")
    print("Cross 점수:", cross_score)
    print("X 점수:", x_score)
    print("판별 결과:", result)

    print("\n=== JSON 자동 분석 시작 ===")

    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    for item in data["patterns"]:
        name = item["name"]
        pattern = item["pattern"]

        cross_score, x_score, result = classify_pattern(pattern)

        print("패턴 이름:", name)
        print("Cross 점수:", cross_score)
        print("X 점수:", x_score)
        print("판별 결과:", result)
        print("--------------------")


if __name__ == "__main__":
    main()


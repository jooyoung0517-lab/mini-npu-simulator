import json

def mac_operation(pattern, filter_data):
    score = 0

    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            score += pattern[i][j] * filter_data[i][j]

    return score


cross_pattern = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

cross_filter = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

result = mac_operation(cross_pattern, cross_filter)

print("MAC 연산 결과:", result)

x_filter = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]

cross_score = mac_operation(cross_pattern, cross_filter)
x_score = mac_operation(cross_pattern, x_filter)

print("Cross 점수:", cross_score)
print("X 점수:", x_score)
if cross_score > x_score:
    print("판별 결과: Cross")
else:
    print("판별 결과: X")
    print("=== Mini NPU Simulator ===")
print("3 x 3 패턴을 입력하세요.")

user_pattern = []

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

        numbers = list(map(int, values))
        user_pattern.append(numbers)
        break

cross_score = mac_operation(user_pattern, cross_filter)
x_score = mac_operation(user_pattern, x_filter)

print("Cross 점수:", cross_score)
print("X 점수:", x_score)

if cross_score > x_score:
    print("판별 결과: Cross")
else:
    print("판별 결과: X")
    import json

with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print("JSON에서 읽은 이름:", data["name"])
print("JSON에서 읽은 패턴:", data["pattern"])
json_pattern = data["pattern"]

json_cross_score = mac_operation(json_pattern, cross_filter)
json_x_score = mac_operation(json_pattern, x_filter)

print("JSON Cross 점수:", json_cross_score)
print("JSON X 점수:", json_x_score)

epsilon = 1e-9

if abs(json_cross_score - json_x_score) <= epsilon:
    print("JSON 판별 결과: Tie")
elif json_cross_score > json_x_score:
    print("JSON 판별 결과: Cross")
else:
    print("JSON 판별 결과: X")
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


test_filter = create_cross_filter(5)

print("=== 5x5 Cross 필터 ===")

for row in test_filter:
    print(row)
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


test_x_filter = create_x_filter(5)

print("=== 5x5 X 필터 ===")

for row in test_x_filter:
    print(row)
# 5x5 X 패턴 준비
test_pattern = create_x_filter(5)

# 5x5 필터 준비
cross_5x5 = create_cross_filter(5)
x_5x5 = create_x_filter(5)

# MAC 연산
cross_score_5x5 = mac_operation(test_pattern, cross_5x5)
x_score_5x5 = mac_operation(test_pattern, x_5x5)

# 점수 출력
print("=== 5x5 패턴 판별 ===")
print("Cross 점수:", cross_score_5x5)
print("X 점수:", x_score_5x5)

# 판별 결과
if abs(cross_score_5x5 - x_score_5x5) <= 1e-9:
    print("판별 결과: Tie")
elif cross_score_5x5 > x_score_5x5:
    print("판별 결과: Cross")
else:
    print("판별 결과: X")
    # 13x13 Cross 패턴 테스트
test_pattern_13 = create_cross_filter(13)

cross_filter_13 = create_cross_filter(13)
x_filter_13 = create_x_filter(13)

cross_score_13 = mac_operation(test_pattern_13, cross_filter_13)
x_score_13 = mac_operation(test_pattern_13, x_filter_13)

print("=== 13x13 패턴 판별 ===")
print("Cross 점수:", cross_score_13)
print("X 점수:", x_score_13)

if abs(cross_score_13 - x_score_13) <= 1e-9:
    print("판별 결과: Tie")
elif cross_score_13 > x_score_13:
    print("판별 결과: Cross")
else:
    print("판별 결과: X")
# 25x25 Cross 패턴 테스트
test_pattern_25 = create_cross_filter(25)

cross_filter_25 = create_cross_filter(25)
x_filter_25 = create_x_filter(25)

cross_score_25 = mac_operation(test_pattern_25, cross_filter_25)
x_score_25 = mac_operation(test_pattern_25, x_filter_25)

print("=== 25x25 패턴 판별 ===")
print("Cross 점수:", cross_score_25)
print("X 점수:", x_score_25)

if abs(cross_score_25 - x_score_25) <= 1e-9:
    print("판별 결과: Tie")
elif cross_score_25 > x_score_25:
    print("판별 결과: Cross")
else:
    print("판별 결과: X")
import time


def mac_operation(pattern, filter_data):
    score = 0

    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            score += pattern[i][j] * filter_data[i][j]

    return score


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


print("=== MAC 연산 성능 측정 ===")

for size in [3, 5, 13, 25]:
    pattern = create_cross_filter(size)
    filter_data = create_cross_filter(size)

    start = time.perf_counter()

    for i in range(1000):
        mac_operation(pattern, filter_data)

    end = time.perf_counter()

    average_time = (end - start) / 1000

    print(f"{size}x{size} 평균 시간: {average_time:.9f}초")
    print(f"MAC 연산 횟수: {size * size}회")
    print("--------------------")

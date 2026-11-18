"""Measure MAC computation only, excluding data creation and console I/O."""
import time
from main import create_cross_filter, mac_operation

REPEATS = 1000
SIZES = (3, 5, 13, 25)


def benchmark(size, repeats=REPEATS):
    pattern = create_cross_filter(size)
    filter_data = create_cross_filter(size)
    # Timer covers only MAC calls. Pattern/filter creation and printing are excluded.
    start = time.perf_counter()
    for _ in range(repeats):
        mac_operation(pattern, filter_data)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return elapsed_ms / repeats


def main():
    print('=== MAC 연산 성능 측정 ===')
    print(f'각 크기별 반복 횟수: {REPEATS}회')
    for size in SIZES:
        average_ms = benchmark(size)
        print(f'{size}x{size} 평균 시간: {average_ms:.6f} ms')
        print(f'MAC 연산 횟수: {size * size}회 (필터 1개 기준)')
        print('--------------------')


if __name__ == '__main__':
    main()

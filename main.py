"""Mini NPU Simulator: interactive mode and JSON evaluation mode."""
import argparse
import json
import re
import time
from pathlib import Path

EPSILON = 1e-9
DATA_FILE = Path(__file__).resolve().parent / 'data.json'


def normalize_label(label):
    """Normalize Cross/X/Tie labels and their common spellings."""
    text = str(label).strip().lower().replace(' ', '').replace('-', '').replace('_', '')
    text = re.sub(r'\d+x\d+$', '', text)
    if text in ('cross', 'plus', '+'):
        return 'Cross'
    if text in ('x', 'diagonal'):
        return 'X'
    if text in ('tie', 'undecided', '판정불가', 'draw'):
        return 'UNDECIDED'
    return None


def validate_pattern(pattern):
    if not isinstance(pattern, list) or not pattern:
        raise ValueError('패턴은 비어 있지 않은 2차원 리스트여야 합니다.')
    size = len(pattern)
    if size % 2 == 0:
        raise ValueError('패턴 크기는 홀수여야 합니다.')
    for row in pattern:
        if not isinstance(row, list) or len(row) != size:
            raise ValueError(f'{size}x{size} 정사각형 패턴이 필요합니다.')
        if any(type(value) is not int or value not in (0, 1) for value in row):
            raise ValueError('패턴에는 정수 0과 1만 입력할 수 있습니다.')
    return size


def mac_operation(pattern, filter_data):
    if len(pattern) != len(filter_data) or any(len(a) != len(b) for a, b in zip(pattern, filter_data)):
        raise ValueError('패턴과 필터 크기가 다릅니다.')
    score = 0
    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            score += pattern[i][j] * filter_data[i][j]
    return score


def create_cross_filter(size):
    center = size // 2
    return [[int(i == center or j == center) for j in range(size)] for i in range(size)]


def create_x_filter(size):
    return [[int(i == j or i + j == size - 1) for j in range(size)] for i in range(size)]


def classify_pattern(pattern, epsilon=EPSILON):
    size = validate_pattern(pattern)
    cross_score = mac_operation(pattern, create_cross_filter(size))
    x_score = mac_operation(pattern, create_x_filter(size))
    if abs(cross_score - x_score) <= epsilon:
        result = 'UNDECIDED'
    elif cross_score > x_score:
        result = 'Cross'
    else:
        result = 'X'
    return cross_score, x_score, result


def get_user_pattern(size=3):
    pattern = []
    print(f'{size} x {size} 패턴을 입력하세요. (0 또는 1)')
    for i in range(size):
        while True:
            values = input(f'{i + 1}번째 줄 숫자 {size}개 입력: ').split()
            if len(values) != size:
                print(f'숫자 {size}개를 입력해주세요.')
                continue
            if any(value not in ('0', '1') for value in values):
                print('0과 1만 입력할 수 있습니다.')
                continue
            pattern.append([int(value) for value in values])
            break
    return pattern


def run_mode1(size=3):
    print('=== 모드 1: 사용자 입력 ===')
    pattern = get_user_pattern(size)
    # I/O 제외: 분류 계산만 측정
    start = time.perf_counter()
    cross_score, x_score, result = classify_pattern(pattern)
    elapsed_ms = (time.perf_counter() - start) * 1000
    display_result = '판정 불가' if result == 'UNDECIDED' else result
    print('=== 사용자 패턴 판별 결과 ===')
    print('Cross 점수:', cross_score)
    print('X 점수:', x_score)
    print('판별 결과:', display_result)
    print(f'연산 시간: {elapsed_ms:.6f} ms')


def run_mode2(path=DATA_FILE):
    print('=== 모드 2: JSON 자동 분석 ===')
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    if not isinstance(data, dict) or not isinstance(data.get('patterns'), list):
        raise ValueError('JSON 형식 오류: patterns 배열이 필요합니다.')
    total = passed = failed = 0
    failures = []
    for index, item in enumerate(data['patterns'], 1):
        total += 1
        name = item.get('name', f'item_{index}') if isinstance(item, dict) else f'item_{index}'
        try:
            if not isinstance(item, dict):
                raise ValueError('패턴 항목이 객체가 아닙니다.')
            expected = normalize_label(item.get('label', name))
            if expected is None:
                raise ValueError(f'알 수 없는 정답 라벨: {item.get("label", name)!r}')
            start = time.perf_counter()
            cross_score, x_score, result = classify_pattern(item['pattern'])
            elapsed_ms = (time.perf_counter() - start) * 1000
            ok = result == expected
            if ok:
                passed += 1
            else:
                failed += 1
                failures.append(f'{name}: 예상 {expected}, 실제 {result}')
            print(f'패턴 이름: {name} | 예상: {expected} | 결과: {result} | {"PASS" if ok else "FAIL"}')
            print(f'Cross 점수: {cross_score} | X 점수: {x_score} | 연산 시간: {elapsed_ms:.6f} ms')
        except (ValueError, KeyError, TypeError) as error:
            failed += 1
            failures.append(f'{name}: {error}')
            print(f'패턴 이름: {name} | FAIL | 원인: {error}')
        print('--------------------')
    print('=== 전체 테스트 요약 ===')
    print(f'총 테스트: {total} | PASS: {passed} | FAIL: {failed}')
    print('실패 원인 요약:')
    if failures:
        for reason in failures:
            print('-', reason)
    else:
        print('- 없음')
    return failed


def main():
    parser = argparse.ArgumentParser(description='Mini NPU Simulator')
    parser.add_argument('--mode', choices=['1', '2', 'both'], default='both', help='1: 사용자 입력, 2: JSON 분석, both: 둘 다')
    parser.add_argument('--size', type=int, default=3, help='모드 1의 홀수 정사각형 크기 (기본 3)')
    parser.add_argument('--data', type=Path, default=DATA_FILE, help='모드 2 JSON 파일 경로')
    args = parser.parse_args()
    if args.size < 3 or args.size % 2 == 0:
        parser.error('--size는 3 이상의 홀수여야 합니다.')
    try:
        if args.mode in ('1', 'both'):
            run_mode1(args.size)
        if args.mode in ('2', 'both'):
            run_mode2(args.data)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.exit(1, f'오류: {error}\n')


if __name__ == '__main__':
    main()

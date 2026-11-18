import json

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


pattern_13 = create_cross_filter(13)
pattern_25 = create_cross_filter(25)

print("13x13 패턴 생성 완료!")
print("25x25 패턴 생성 완료!")
# 기존 JSON 파일 읽기
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# 기존 목록에서 같은 이름의 패턴 제거
data["patterns"] = [
    item for item in data["patterns"]
    if item["name"] not in ["Cross_13x13", "Cross_25x25"]
]

# 13x13 패턴 추가
data["patterns"].append({
    "name": "Cross_13x13",
    "pattern": pattern_13
})

# 25x25 패턴 추가
data["patterns"].append({
    "name": "Cross_25x25",
    "pattern": pattern_25
})

# JSON 파일에 저장
with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("JSON 파일 저장 완료!")

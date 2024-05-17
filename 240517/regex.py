import re

# 정규 표현식을 이용한 패턴 치환
def replace_entities_regex(text, entityDict):
    # 패턴을 길이 순으로 정렬
    sorted_patterns = sorted(entityDict.items(), key=lambda x: len(x[0]), reverse=True)
    for pattern, replacement in sorted_patterns:
        text = re.sub(re.escape(pattern), replacement, text)
    return text

# Example usage

raw_text = "왕밤빵에 들어있는 밤은 밤에 먹어야 제맛이에요."
processed_text = "King chestnut bread에 들어있는 chestnuts은 night에 먹어야 제맛이에요."
# 실제로는 DB에 raw_text 로 등록되어 있는 것을 processed_text 로 변환 후,
# 유저가 입력한 문자열을 precessed_text와 비교하도록 해야함..
# 아직은 그냥 기본 함수 테스트..
entityDict_01 = {
    "밤": "chestnuts",
    "왕밤빵": "King chestnut bread"
}
entityDict_02 = {
    "chestnuts":"밤" ,
    "King chestnut bread":"왕밤빵"
}

result1 = replace_entities_regex(raw_text, entityDict_01)
result2 = replace_entities_regex(processed_text, entityDict_02)
print(result1)
print(result2)

# TODO 동음이의어 문제 해결해야함
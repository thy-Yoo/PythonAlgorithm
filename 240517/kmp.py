
"""
lps 란?
Longest Prefix which is also Suffix
'부분 일치 테이블' 이라고도 한다.

lps 배열 생성 과정
lps[0] : 항상 0이다. 패턴의 첫 번째 문자에 대해서, 접두사와 접미사가 일치할 수 없기 때문이다.
=> Q. 첫 번째 문자에 대해서 접두사와 접미사가 일치할 수 없다는 게..?
=> A.

KMP 알고리즘이란?
Knuth-Morris-Pratt algorithm 문자열 검색 알고리즘
텍스트 내에서 특정 패턴을 효율적으로 찾는 방법이다.
이 알고리즘은 기본적인 문자열 검색 알고리즘의 비효율성을 개선하여,
부분 문자열을 일치시키는 데 있어서 불필요한 비교를 피한다고 한다.

알고리즘 구성
Step 1. 접두사-접미사 배열 (Prefix-Suffix Array)
Step 2. 검색 (Search)

"""


# Longest Prefix Suffix 계산
def compute_lps(pattern):
    length = 0 # 현재까지 일치한 가장 긴 접두사이자 접미사의 길이를 담을 변수
    lps = [0] * len(pattern) # LPS 배열 초기화, 패턴의 길이만큼 0으로 채운다.
    i = 1 # 패턴의 두번째 문자부터 시작

    while i < len(pattern): # 패턴의 모든 문자를 순회한다.
        if pattern[i] == pattern[length]: # 패턴의 현재 문자와 접두사/접미사 길이의 다음 문자가 일치할 때
            length += 1 # 일치하는 접두사/접미사의 길이 +1
            lps[i] = length # 현재 위치의 LPS 값을 일치한 길이로 설정
            i += 1 # 다음 문자로 이동
        else: # 일치하지 않지만,
            if length != 0: # 현재까지 일치한 접두사/접미사가 있을 때
                length = lps[length - 1] # 길이를 이전 LPS 값으로 줄임
            else: # 일치한 접두사/접미사가 없을 때
                lps[i] = 0 # 현재 위치의 LPS 값을 0으로 설정
                i += 1 # 다음 문자로 이동
    return lps # 계산된 LPS 배열 반환

# KMP 알고리즘을 사용해서 텍스트 내에서 패턴의 모든 출현 위치를 찾음.
def kmp_search(text, pattern):
    M = len(pattern) # 패턴의 길이
    N = len(text) # 텍스트의 길이
    lps = compute_lps(pattern) # 패턴의 LPS 배열 계산
    i = 0 # 텍스트의 인덱스
    j = 0 # 패턴의 인덱스
    positions = [] # 패턴이 발견된 위치를 저장할 리스트

    while i < N: # 텍스트의 모든 문자를 순회
        if pattern[j] == text[i]: # 텍스트의 현재 문자와 패턴의 현재 문자가 일치할 때
            i += 1 # 텍스트 인덱스 증가
            j += 1 # 패턴 인덱스 증가

        if j == M: # 패턴의 모든 문자가 일치할 때
            positions.append(i - j) # 패턴이 발견된 시작 위치를 저장
            j = lps[j - 1] # 패턴 인덱스를 LPS 배열을 사용하여 이동
        elif i < N and pattern[j] != text[i]: # 패턴이 일치하지 않을 때
            if j != 0: # 패턴 인덱스가 0이 아닐 때
                j = lps[j - 1] # 패턴 인덱스를 LPS 배열을 사용하여 이동
            else: # 패턴 인덱스가 0 일 때
                i += 1 # 텍스트 인덱스 증가

    return positions # 패턴이 발견된 모든 위치 반환

# 패턴 대치 함수
def replace_entities(text, entityDict):
    # 패턴을 길이 순으로 정렬
    sorted_patterns = sorted(entityDict.items(), key=lambda x: len(x[0]), reverse=True)
    # 패턴을 길이 순으로 정렬하지 않으면
    # 예를 들어 "교보생명보험"->company 이 아닌, ->kyobo생명보험 과 같이  잘못 대치 될 수 있다.


    for pattern, replacement in sorted_patterns:
        positions = kmp_search(text, pattern)
        if positions:
            # Using a list to build the new text for better performance
            new_text = []
            last_index = 0
            for pos in positions:
                new_text.append(text[last_index:pos])
                new_text.append(replacement)
                last_index = pos + len(pattern)
            new_text.append(text[last_index:])  # Add the rest of the text
            text = ''.join(new_text)
    return text

# 사용 예시
text = "교보생명보험에 다니는 김교보와 교보DTS에 다니는 유지연"
pattern = "교보"
positions = kmp_search(text, pattern)
print("패턴이 발견된 위치:", positions)
entityDict_01 = {
    "교보": "kyobo"
}
entityDict_02 = {
    "교보": "kyobo",
    "교보생명보험": "company",
    "교보DTS": "company"
}

result_01 = replace_entities(text, entityDict_01)
print("패턴을 대치한 후 변환된 문자열:", result_01)
result_02 = replace_entities(text, entityDict_02)
print("패턴을 대치한 후 변환된 문자열:", result_02)

"""
lps 란?
Longest Prefix which is also Suffix
'부분 일치 테이블' 이라고도 한다.

lps 배열 생성 과정
lps[0] : 항상 0이다. 패턴의 첫 번째 문자에 대해서, 접두사와 접미사가 일치할 수 없기 때문이다.
=> Q. 첫 번째 문자에 대해서 접두사와 접미사가 일치할 수 없다는 게..?
=> A.


"""


def compute_lps(pattern):
    length = 0
    lps = [0] * len(pattern)
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    M = len(pattern)
    N = len(text)
    lps = compute_lps(pattern)
    i = 0
    j = 0
    positions = []

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == M:
            positions.append(i - j)
            j = lps[j - 1]
        elif i < N and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return positions

# 예제
text = "ABABDABACDABABCABAB"
pattern = "ABABCABAB"
positions = kmp_search(text, pattern)
print("패턴이 발견된 위치:", positions)

# 구간 합을 활용하려면 합 배열을 이용해야 한다고 한다.
"""
합 배열이란?
<정의>
S[i] = A[0] + ... + A[i] , 0~i 까지의 합 O(n)
<구하는 법>
S[i] = S[i-1] + A[i] : O(1)

S[i~j] = S[j] - S[i-1] : O(1)

리스트 합을 왜 합 배열로 구해야 하는가..?
최악의 경우 i~j 까지의 합 배열을 구할 때 시간 복잡도가 O(N) 이다. (덧셈을 N번 수행해야하기 때문)
때문에, 합 배열을 자주 구해야 한다면, 제일 처음 구할 때만 O(N)의 기본 연산을 수행 한 후,
그 이후로는 S[i] = S[i-1] + A[i] 와 같은 공식을 이용해서 이후 시간복잡도는 O(1) 로 줄이는것이다.

"""

# 문제 : 수 N 개가 주어졌을 때 i번째 수에서 j번째 수까지의 합을 구하는 프로그램을 작성하라
# 입력 조건
# - 1번째 줄에 수의 개수 N (1<=N<=100,000)와 합을 구해야 하는 횟수 M (1<=M<=100,000)
# - 2번째 줄에 N개의 수, 각 수는 <= 1,000 자연수
# - 3번째 줄부턴는 M개의 줄에 합을 구해야하는 구간 i와 j 가 주어진다.
# 출력 조건
# - 총 M개의 줄에 입력으로 주어진 i번째 수에서 j번째 수까지의 합을 출력한다.

print("총 수의 개수(N)와 합을 구해야 하는 횟수 (qn)을  띄어쓰기로 구분하여 입력해주세요: ")
n, questionNumber = map(int, input().split())
"""
map 이란?
주어진 함수를, 시퀀스의 모든 부분에 적용하는 매우 유용한 python의 함수.
예를들어 n, m = map (int, input().split()) 이면
input().split() : 사용자로부터 입력을 받고, 공백을 기준으로 문자열을 나눠서 저장한다.
map(fx, value) : fx(value) , 만약 value가 리스트 형태라면 모든 요소에 대해 fx(element), fx(element), ... 를 적용한다.
"""
print("숫자들을 띄어쓰기로 구분하여 입력해 주세요.: ")
numbers = list(map(int, input().split()))

prefix_sum = [0]
temp = 0

for number in numbers:
    # print(f"number: {number}")
    temp = temp + number
    prefix_sum.append(temp) # 미리 구간합을 구해둔다.
    # print(f"prefix_sum: {prefix_sum}")

"""
range(n) 이란?
0 부터 n-1 까지의 연속된 정수 시퀀스.
만약 range(10) 이라면, 0 1 2 3 4 5 6 7 8 9 를 생성하고, 이때는
for i in range(n): 에서 i 는 0 1 2  ... 가 된다.
만약
for e in n: 이렇게 작성한다면, n자체가 시퀀스 [a,b,c] 일 경우, e 는 n의 요소 a b c 가  된다..
"""
for qn in range(questionNumber): # 문제를 낼 횟수 questionNumber 에 대해, qn+1번째 질문 (range는 0부터 시작함)
    print(f"{qn+1}번째 질문입니다. 합을 구해야하는 구간 i, j를 띄어쓰기를 구분하여 입력하세요.: ")
    i, j = map(int, input().split())
    print(f"답: {prefix_sum[j] - prefix_sum[i-1]}")



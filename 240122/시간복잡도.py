""" 시간 복잡도
시간 복잡도란? 주어진 문제를 해결하기 위한 연산 횟수
일반적으로 2000만번 ~ 1억 번의 연산을 1초로 예측한다.
코딩 테스트에서는 주로 빅-오 표기법 'O(n)' 로 시간을 계산한다.

"""
import random
findNumber = random.randrange(1, 101) # 1~100 랜덤값 생성
for i in range(1,101):
    if i == findNumber:
        print(i)
        break

""" 수 정렬하기 """
# N개의 수가 주어졌을 때, 이를 오름차순 정렬하는 프로그램을 작성하라.
# 1번째 줄에는 수의 개수 N ( 1<= N <= 1,000,000 )
# 2번째 줄부터는 N개의 줄에 숫자가 주어진다.
"""
예) 
좌측과 같은 수가 주어지면, 우측처럼 출력해야 한다.
 5                        5
 5                        4
 2                        3
 3                        2
 4                        1
 1 
"""

# 풀기
n = int(input("몇개의 숫자룰 입력할 지 결정하세요. : ")) # 숫자 입력받기 ( 첫줄인 N )
numbers = [int(input("한줄에 숫자 하나씩 입력하세요. :")) for _ in range(n)] # n개의 숫자를 입력받아서 저장
numbers.sort()
for number in numbers:
    print(number)

"""
n = int(input()) : 단일 입력을 받으므로, 시간 복잡도 O(1) 
numbers = [int(input()) for _ in range(n)] : n개의 입력을 받으므로, 시간 복잡도 O(n)
numbers.sort() : 팀 소트 알고리즘, 최악의 경우 O(nlogn)
for nuber in numbers:
    print(number) : n번 출력하므로 O(n)
"""


""" 커밋 테스트.. 240122 LitlOuo 계정으로 바꿔서 커밋하기."""
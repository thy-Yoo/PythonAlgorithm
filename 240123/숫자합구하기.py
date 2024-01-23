# N개의 숫자가 공백 없이 써있을 때, 이 숫자를 모두 합해 출력하는 프로그램을 작성하라.
# 1번째 줄에 숫자의 개수 N(1<=N<=100), 2번째 줄에 숫자 N개가 공백 없이 주어진다.
"""
예)
3
123

4
4123
"""

n = int(input("몇개의 숫자를 입력할 지 결정하세요.: "))
nlist = list(input(f"{n}개의 숫자만큼 공백 없이 입력하세요.: "))
sum = 0

for i in nlist: #nlist의 각 요소마다  for문을 수행
    print(f"i: {i}")
    sum = sum + int(i)

print(sum)
"""
a = np.arrange(10) # a = array ([0,1,2,3, ... , 9])
a[start:end] # start index 부터 end-1 index 까지 선택해서 가져온다.
a[start:] # start index 부터 끝까지 선택해서 가져온다.
a[:end] # 시작부터 end-1 index 까지 선택해서 가져온다.
a[:] # 배열 전체를 복사해서 가져온다
a[start:end:step] # start index 부터 end-1 index 까지 step의 간격으로 가져온다.
"""


a = [1,2,3,4,5,6,7,8,9,10] # 참고로 1 == 0 index 임.
print(f"type(a): {type(a)}") # <class 'list'>
import numpy as np
b = np.arange(10)
print(f"b: {b}, type(b): {type(b)}") # [0 1 2 3 4 5 6 7 8 9], <class 'numpy.ndarray'>
print(f"a[1:2]: {a[1:2]}") # [2]
print(f"a[0:2]: {a[0:2]}") # [1, 2]
print(f"a[-1]: {a[-1]}") # 10 ; 해당 인덱스를 지정해서 가져온다. 조심할 건 1 == 0 index 이지만 가장 맨 뒤 10은 0 이 아니라 -1 index 이다.
print(f"a[-2:]: {a[-2:]}") # [9, 10] ; -2~끝까지
print(f"a[:-2]: {a[:-2]}") # [1, 2, 3, 4, 5, 6, 7, 8] ; 처음부터 end-1 index 즉 -3까지니까 8 까지.
print(f"a[::-1]: {a[::-1]}") # [10, 9, 8, 7, 6, 5, 4, 3, 2, 1] ; 생략:생략::-1 즉 처음부터 끝까지 -1간격(거꾸로)
# start 가 생략되면 step이 양수일 경우 0부터, step이 음수일 경우 끝부터 시작한다.
print(f"a[1::-1]: {a[1::-1]}") # [2, 1] ; stop 보다 step을 먼저 봐야한다. 2 부터 -> '거꾸로' -> 끝까지 이기에 2 -> 1로 간다.
# stop 이 생략되면 슬라이싱이 끝까지 진행된다.
print(f"a[:-3:-1]: {a[:-3:-1]}") # [10, 9] ; 끝부터 거꾸로 -3까지(end indx 는 포함하지 않음) == 10 9

# 배열 연산
c = np.arange(3)
print(f"c: {c}") # [0 1 2]
print(f"c*3: {c*3}") # [0 3 6]

print(f"c+1: {c+1}") # [1 2 3]


#(5)
import pandas as pd
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
}
df = pd.DataFrame(data)
print("원본 DataFrame:")
print(df)
# 인덱스 1에 해당하는 행 삭제 (Bob)
df_drop_row = df.drop(index=1)
print("\n인덱스 1(==Bob)에 해당하는 행 삭제 후:")
print(df_drop_row)



#(12) 다차원 배열 슬라이싱
import numpy as np

# 3차원 배열 생성





# (13)
ori_data = np.arange(24)
print(f"ori_data: {ori_data}")
data = ori_data.reshape(6,4)
print(f"data: {data}")

#
#
# a[:-3:-1]
#
# a[-3::-1]
# python 240709/dsac.py
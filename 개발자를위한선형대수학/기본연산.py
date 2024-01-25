import numpy as np
a = np.array([5,4,8,2])
b = np.array([1,0,.5,-1])

r = a*b
print(r)

# a2 = np.array([5,4,8,2])
# b2 = np.array([1,0,.5])
# r2 = a2*b2
#
# print(r2) # 얘는 잘못된 연산

v = np.array([1,2,3])
column_rv = v.reshape([-1,1]) # 열벡터
row_rv = v.reshape([1,-1]) # 행벡터
print(f"column_rv: {column_rv}")
print(f"row_rv: {row_rv}")
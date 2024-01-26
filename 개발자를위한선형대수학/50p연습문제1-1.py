
# matplotlib_inline 이란?
# Jupyter Notebook 같은 인터랙티브 쉘 환경에서 사용되는 라이브러리
# matplotlib 그래프를 inline 으로 표시하는데 사용한다.
# 결과 그래프를 셀 출력에 직접 표시한다.
# 즉 pycharm 에서는 쓸 필요가 없는 듯 하다!

import matplotlib.pyplot as plt
# HOW TO. 기본 그래프 바탕 그리는 방법
# 축 범위 설정
# plt.xlim(-6,6)
# plt.ylim(-6,6)
# # 모눈 설정
# plt.grid(which='both', linestyle='-', linewidth=0.5)
# plt.xticks(range(-6,7,2))
# plt.xticks(range(-6,7,2))
# 그래프 표시
#plt.show()

# HOW TO. matplotlib 에서 사용 가능한 색상들 출력
# import matplotlib
# for name, hex in matplotlib.colors.cnames.items():
#     print(name, hex)

# HOW TO. 한글 폰트 설정
import matplotlib.font_manager as fm
# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # 예시로 'NanumBarunGothic' 폰트를 사용
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 문제 해결

# HOW TO. 한 행에 여러 그래프를 그리는 방법
# 그림 생성 및 서브 플롯 추가
fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10,5)) # 1행 2열의 서브 플롯, 전체 이미지 크기는 10:5 inch

# 첫번째 플롯에 그래프 그리기
# 축 범위 설정
ax1.set_xlim(-6,6)
ax1.set_ylim(-6,6)
# 눈금 설정
ax1.set_xticks(range(-6,7,2))
ax1.set_yticks(range(-6,7,2))
# 모눈 표시
ax1.grid(True, linestyle='--') # '-', '--','-.',':',' ', '', 'solid', 'dashed', 'dashdot', 'dotted'
# 그래프 제목/추가 텍스트 설정
ax1.set_title('벡터 v,w,v+w')
ax1.text(0.5,-0.2, '(A)', ha='center', va='center', transform=ax1.transAxes)
plt.subplots_adjust(bottom=0.1)
# 데이터 그리기
# 벡터 설정, 벡터는 [x,y] 리스트로도, (x,y) 튜플로도 가능하다!
# HOW TO. 튜플
"""
v = (1,2)
w = (4,-6)
# arrow(시작x, 시작y, 벡터x(끝점이아님), 벡터y, 설정 ...)
ax1.arrow(0,0, v[0], v[1], head_width=0.3, width=0.1, color='black', length_includes_head=True)
ax1.arrow(v[0],v[1], w[0], w[1], head_width=0.3, width=0.1, color='orange', length_includes_head=True)
# 합 벡터 계산
r = (v[0]+w[0], + v[1]+w[1]) # 튜플은 각 성분 별로 더해야 한다.
ax1.arrow(0,0, r[0], r[1], head_width=0.3, width=0.1, color='salmon', length_includes_head=True)
"""
# HOW TO. 리스트
v = [1,2]
w = [4,-6]
ax1.arrow(0,0,v[0],v[1], head_width=0.3, width=0.1, color='black', length_includes_head=True)
ax1.arrow(v[0],v[1],w[0],w[1], head_width=0.3, width=0.1, color='orange', length_includes_head=True)
r = v + w
ax1.arrow(0,0,r[0],r[1], head_width=0.3, width=0.1, color='salmon', length_includes_head=True)


ax2.set_xlim(-6,6)
ax2.set_ylim(-6,6)
ax2.set_xticks(range(-6,7,2))
ax2.set_xticks(range(-6,7,2))
ax2.grid(False)
ax2.set_title('(B)')
# 그래프 표시
plt.show()

# 아직 작성중...
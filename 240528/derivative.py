import sympy as sp
# color setting
# ANSI escape code for colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"


print(f"{RED}== e^(-x) 미분 ======================================================================{RESET}")
x = sp.symbols('x') # 변수 x
f = sp.exp(-x) # 함수 e^(-x)
f_prime = sp.diff(f, symbols=x) # 함수 f를 x에 대해 미분

print( f_prime )
sp.pprint(f_prime, use_unicode=True) # 수학적으로 보기 쉽게 출력

print(f"{RED}== 시그모이드 함수 미분 ================================================================={RESET}")

x2 = sp.symbols('x')
sigmoidF = 1 / ( 1 + sp.exp(-x2) ) # 1 + e^-x
r = sp.diff(sigmoidF, symbols=x2)

print(r)
sp.pprint(r, use_unicode=True)


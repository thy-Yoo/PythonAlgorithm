***
#### 깃 계정 상태 확인하기
##### 명령어
```bash
git config --global user.name
git config --global user.email
```

#### 깃 계정 바꾸기
git config --global user.name [사용자 이름]
git config --global user.email [사용자 이메일]
```bash
git config --global user.name LitlOuo
git config --global user.email ninkyoii@gmail.com
```




***
#### 커밋 리스트 보기 
###### 명령어
```bash
git log --oneline
```
###### 결과 예시
```bash
8bd3848 (HEAD -> coLaptop) 240122 am1043 커밋 테스트! branch is coLaptop. :)
ca1d3e4 (origin/coLaptop) 240122 am1043 커밋 테스트! branch is coLaptop. :)
````
***

#### 브랜치 체크아웃 하기
###### 명령어 
```bash
git checkout coLaptop
```
###### 결과
이미 해당 브랜치인 경우 아래와 같이 나타난다.
```bash
Already on 'coLaptop'
A       HowToGit.md
A       HowToPython.md
Your branch is up to date with 'origin/coLaptop'.
```
###### 결과
정상 변경된 경우 아래와 같이 나타난다.
```bash
Switched to branch 'coLaptop'
A       HowToGit.md
A       HowToPython.md
Your branch is up to date with 'origin/coLaptop'.
```
***
#### 새로운 브랜치를 만들고 체크아웃 하기
###### 명령어
```bash
git checkout -b temp
``` 
###### 결과
새로운 브랜치 temp 이 생성되었다.
```bash
Switched to a new branch 'temp'
Your branch is based on 'origin/temp', but the upstream is gone.
  (use "git branch --unset-upstream" to fixup)
```
***
#### 브랜치 삭제하기 
###### 명령어
```bash
git branch -d temp
```
###### 결과
```bash
Deleted branch temp (was e7399e0).
```

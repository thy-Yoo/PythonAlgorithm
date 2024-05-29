import re # 정규표현식 사용을 위함


PUNCT = "/-'?!.,#$%\'()*+-/:;<=>@[\\]^_`{|}~" + '""“”’' + '∞θ÷α•à−β∅³π‘₹´°£€\×™√²—–&'
PUNCT_MAPPING = {"‘": "'", "₹": "e", "´": "'", "°": "", "€": "e", "™": "tm", "√": " sqrt ", "×": "x", "²": "2",
                 "—": "-", "–": "-", "’": "'", "_": "-", "`": "'", '“': '"', '”': '"', '“': '"', "£": "e",
                 '∞': 'infinity', 'θ': 'theta', '÷': '/', 'α': 'alpha', '•': '.', 'à': 'a', '−': '-', 'β': 'beta',
                 '∅': '', '³': '3', 'π': 'pi', }


# Fx. 구두점 (punctuation) 을 클린하기 위한 함수.. 분리를 하려고 하는 ..
def clean_punc(text, punct, mapping):
    # step 1. text 에 mapping 에 포함된 글자가 있으면 key의 value 로 대체.
    for p in mapping:
        text = text.replace(p, mapping[p])
    # step 2. text 에 punct 에 해당하는 글자가 있으면 특수문자 양옆으로 공백을 추가하여 대체.
    for p in punct:
        text = text.replace(p, f' {p} ')

    specials = {
        '\u200b': ' ',
        '…': ' ... ',
        '\ufeff': '',
        'करना': '',
        'है': ''
    }
    # step 3. 그 외 특별한 값들 처리.
    for s in specials:
        text = text.replace(s, specials[s])

    # step 4. 중복 공백 제거.
    text = ' '.join(text.split())  # 중복 공백 제거

    return text.strip() # 문자열의 양 끝에서 공백을 제거

def clean_text(texts):
    corpus = []
    for i in range(0, len(texts)):
        review = str(texts[i])
        # review = re.sub(r'[@%\\*=()/~#&\+á?\xc3\xa1\-\|\.\:\;\!\-\,\_\~\$\'\"]', '',review) #remove punctuation
        review = re.sub(r'[{}]+'.format(re.escape(PUNCT)), '', review) # 모든 PUNCT 에 정의된 모든 글자 제거

        review = re.sub(r'\d+','', review)# remove number
        review = review.lower() #lower case
        review = re.sub(r'\s+', ' ', review) #remove extra space
        review = re.sub(r'<[^>]+>','',review) #remove Html tags
        review = re.sub(r'\s+', ' ', review) #remove spaces
        review = re.sub(r"^\s+", '', review) #remove space from start
        review = re.sub(r'\s+$', '', review) #remove space from the end
        corpus.append(review)
    return corpus


while True:
    user_input = input("문장을 입력하세요: (종료하려면 exit 라고 적으세여)")
    if user_input.lower() == 'exit':
        print("Exiting...")
        break
    cleaned_text = clean_punc(user_input, PUNCT, PUNCT_MAPPING)
    print(f"punctutation 분리 결과: {cleaned_text}, type: {type(cleaned_text)}")

    result_text = clean_text([cleaned_text])
    print("전처리 결과: ", result_text[0])
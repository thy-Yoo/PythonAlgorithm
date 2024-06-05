"""
로컬서 안돌아가는 코랩 소스임
경로 바꿔주고 집가면 테스트 해보기
"""

# git add -v 240605/*


from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast
import os
import torch

# model_name 에 맞춰 온라인 huggingface 에서 자동으로 모델을 다운로드
model_name = "skt/ko-gpt-trinity-1.2B-v0.5"
# 해당 모델을 (drive 내에) 저장할 경로 지정
save_directory = "/content/drive/MyDrive/models/pretrained/240605/skt/ko-gpt-trinity-1.2B-v0.5"

# 디렉토리 생성 (없을 경우)
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# 모델과 토크나이저 파일이 이미 있는지 체크
model_files = ['config.json', 'pytorch_model.bin']
tokenizer_files = ['tokenizer_config.json', 'vocab.json', 'merges.txt', 'special_tokens_map.json']

# 모든 필요한 파일이 저장 경로에 존재하는지 확인
model_exists = all(os.path.isfile(os.path.join(save_directory, f)) for f in model_files)
tokenizer_exists = all(os.path.isfile(os.path.join(save_directory, f)) for f in tokenizer_files)


model = None
tokenizer = None

# 모델이나 토크나이저 파일 중 하나라도 없으면 다운로드 및 저장
if not model_exists or not tokenizer_exists:
    print("모델 또는 토크나이저 파일이 누락되었습니다. 다운로드를 시작합니다...")
    model = GPT2LMHeadModel.from_pretrained(model_name)
    # tokenizer = PreTrainedTokenizerFast.from_pretrained(model_name, bos_token='<d>', eos_token='</d>', unk_token='<unk>')
    tokenizer = PreTrainedTokenizerFast.from_pretrained(model_name)
    model.save_pretrained(save_directory)
    tokenizer.save_pretrained(save_directory)
    print(f"모델과 토크나이저가 성공적으로 다운로드 되었습니다. 저장경로: {save_directory}")
else:
    print("모든 파일이 이미 존재합니다. 추가 다운로드가 필요하지 않습니다.")
    # 저장된 모델과 토크나이저 로드
    model = GPT2LMHeadModel.from_pretrained(save_directory)
    tokenizer = PreTrainedTokenizerFast.from_pretrained(save_directory)


# GPU 사용 여부 확인
# 구글 코랩에서 GPU 를 사용하려면 [런타임]-[런타임유형변경]-[하드웨어가속기] 에서 선택해주어야 한다.

device = None

if torch.cuda.is_available():
    device = torch.device("cuda")
    print("GPU를 사용합니다.")
else:
    device = torch.device("cpu")
    print("GPU를 사용할 수 없습니다. CPU를 사용합니다.")

    # 토크나이저는 왜 CPU에 두고 쓰는가?
    # GPT의 답변에 따르면..
    """
    [토크나이저의 역할]
    텍스트를 전처리하여 모델이 이해할 수 있는 형식으로 변환하는 역할

    - 텍스트 인코딩:  입력 텍스트를 토큰 시퀀스로 변환.
    - 토큰 디코딩: 토큰 시퀀스를 다시 텍스트로 변환.
    - 패딩 및 트렁케이팅: 시퀀스 길이를 맞추기 위해 패딩(padding) 또는 자르기(truncating)를 수행.

    CPU 사용이 충분한 이유
    - 상대적으로 적은 연산:
       텍스트를 토큰으로 변환하는 작업은 상대적으로 계산 비용이 낮다.
       따라서 CPU에서도 충분히 빠르게 처리할 수 있다.
    - 메모리 효율:
       토크나이저는 텍스트를 처리할 때 대규모 메모리 사용이 필요하지 않다.
       GPU 메모리는 주로 모델의 가중치와 대규모 텐서를 처리하는 데 사용되므로,
       토크나이저를 CPU에 두는 것이 더 효율적일 수 있다.
    - 병목 지점 해소:
       텍스트 전처리를 CPU에서 수행하고, 모델 추론을 GPU에서 수행하면
       시스템 리소스를 더 효율적으로 사용할 수 있다.
       이는 GPU를 최대한 모델 추론에 집중시킬 수 있게 합니다
    """



# 모델을 학습 모드로 전환
model.train()

# 기존 특수 토큰 확인
# print("기존 특수 토큰 설정:")
# print(f"bos_token: {tokenizer.bos_token}")
# print(f"eos_token: {tokenizer.eos_token}")
# print(f"unk_token: {tokenizer.unk_token}")

# 모델과 토크나이저 다운로드 및 특수 토큰 설정
model = GPT2LMHeadModel.from_pretrained(save_directory)
tokenizer = PreTrainedTokenizerFast.from_pretrained(save_directory)

# 특수 토큰 설정
special_tokens = {
    'bos_token': '<s>',
    'eos_token': '</s>',
    'unk_token': '<unk>',
    'pad_token': '<pad>',
    'mask_token': '<mask>'
}
# 토크나이저 업데이트가 모델에 반영되도록 모델 크기 조정
tokenizer.add_special_tokens(special_tokens)
model.resize_token_embeddings(len(tokenizer))

resave_directory = "/content/drive/MyDrive/models/pretrained/240605/addTokens/skt/ko-gpt-trinity-1.2B-v0.5"

# 모델과 토크나이저 저장
model.save_pretrained(resave_directory)
tokenizer.save_pretrained(resave_directory)
print(f"모델과 토크나이저가 성공적으로 업데이트 및 저장되었습니다. 저장 경로: {resave_directory}")

# 모델과 토크나이저 재로드
model = GPT2LMHeadModel.from_pretrained(resave_directory)
tokenizer = PreTrainedTokenizerFast.from_pretrained(resave_directory)


# 모델을 평가 모드로 전환
model.eval()

# # 모델과 토크나이저 저장
# model.save_pretrained(save_directory)
# tokenizer.save_pretrained(save_directory)
#

## 토큰 문제가 있다. 현재 토크나이저의 토큰 확인하기.
# 특수 토큰 ID 확인
bos_token_id = tokenizer.bos_token_id
eos_token_id = tokenizer.eos_token_id
unk_token_id = tokenizer.unk_token_id
pad_token_id = tokenizer.pad_token_id
mask_token_id = tokenizer.mask_token_id

print(f"bos_token: {tokenizer.bos_token}")
print(f"eos_token: {tokenizer.eos_token}")
print(f"unk_token: {tokenizer.unk_token}")

print(f"BOS Token ID: {bos_token_id}")
print(f"EOS Token ID: {eos_token_id}")
print(f"UNK Token ID: {unk_token_id}")
print(f"PAD Token ID: {pad_token_id}")
print(f"MASK Token ID: {mask_token_id}")



# 모델을 GPU로 이동
model.to(device)
# tokenizer 는 이동시키지 않음. (토크나이저는 cpu에서 작동함.)

# 생성하려는 텍스트의 프롬프트
prompt = "개발곰은 귀엽다. 왜냐하면"
#"개발곰은 정말 귀엽다. 왜냐하면"

# 토크나이저를 사용하여 프롬프트 인코딩
inputs = tokenizer.encode(prompt, return_tensors="pt", add_special_tokens=True).to(device)
# gpu에서 계산하려면(for model.generate) 계산에 넣을 값인 inputs 도 gpu로 이동시켜야 한다.
# tokenizer 는 CPU에 있으므로, tokenizer.encode 후 생성된 결과를 .to(device) 를 이용해서 GPU로 이동시킨다.

# 텍스트 생성 설정
generated_text_samples = model.generate(
    inputs,
    max_length=500,  # 생성할 텍스트의 최대 길이
    num_return_sequences=1,  # 생성할 텍스트의 수
    no_repeat_ngram_size=2,  # 반복되는 n-gram 크기를 제한
    num_beams=5,
    early_stopping=True,  # 조건을 만족하면 생성 중단
    # temperature=0.7,  # 생성 다양성 조절
    do_sample=False,  # 빔 서치 사용
    eos_token_id=eos_token_id  # 문장 종료 토큰 ID 지정
    # temperature=0.7,  # 생성 다양성 조절, do_sample=True 일때 사용
    # top_p=0.9,  # 누적 확률에서 상위 P%를 선택하여 생성, do_sample=True 일때 사용
)


# 생성된 텍스트를 디코딩하여 출력
# skip_special_tokens=True
# generated_text_with_skip = tokenizer.decode(generated_text_samples[0], skip_special_tokens=True)
# print("skip_special_tokens=True:", generated_text_with_skip)

# skip_special_tokens=False
generated_text_with_special_tokens = tokenizer.decode(generated_text_samples[0], skip_special_tokens=False) # 토큰 그대로 출력
print("skip_special_tokens=False:", generated_text_with_special_tokens)

# # 생성된 텍스트에서 마지막 </d>를 찾아 그 위치까지의 텍스트를 사용
last_eos_index = generated_text_with_special_tokens.rfind('</d>')
if last_eos_index != -1:
    final_text = generated_text_with_special_tokens[:last_eos_index + len('</d>')]
    print("final_text_cut:", final_text)
else:
    final_text = generated_text_with_special_tokens
    print("final_text_origin:", final_text)




from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast

# 로컬에 저장된 모델 경로 ( ko-gpt-trinity-1.2B-v0.5 )
model_directory = "./model/pretrained/skt-ko-gpt-trinity"

# 모델과 토크나이저 로드
model = GPT2LMHeadModel.from_pretrained(model_directory)
tokenizer = PreTrainedTokenizerFast.from_pretrained(model_directory, bos_token='</s>', eos_token='</s>', unk_token='<unk>')

# 입력 텍스트
input_text = "안녕하세요, 저는 인공지능입니다."

# 텍스트를 토큰화하고 모델에 입력
input_ids = tokenizer.encode(input_text, return_tensors='pt')
output = model.generate(input_ids, max_length=50, num_return_sequences=1)

# 생성된 텍스트 디코딩
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_text)

from transformers import GPT2LMHeadModel, GPT2Tokenizer
from langchainTest.llms.base import LLM
from typing import List
from langchainTest import LangChain

class KoGPTLangChainWrapper(LLM):
        def __init__(self, model, tokenizer):
            self.model = model
            self.tokenizer = tokenizer

        def _call(self, prompt: str, stop: List[str] = None) -> str:
            input_ids = self.tokenizer.encode(prompt, return_tensors='pt')
            output = self.model.generate(input_ids, max_length=100, num_return_sequences=1)
            response = self.tokenizer.decode(output[0], skip_special_tokens=True)
            return response

        @property
        def _identifying_params(self):
            return {"model": self.model, "tokenizer": self.tokenizer}


# GPT-2 모델과 토크나이저 로드
model_directory = "./model/pretrained/skt-ko-gpt-trinity"
model = GPT2LMHeadModel.from_pretrained(model_directory)
tokenizer = GPT2Tokenizer.from_pretrained(model_directory)
# Q. 문서에 따르면 gpt3 을 기반으로 만들어졌다고 했는데 왜 2 를 사용하는가?
# A. Hugging Face의 Transformers 라이브러리는 GPT-2와 GPT-3 모델을 모두 GPT2LMHeadModel 클래스로 처리할 수 있도록 설계되었 다고 한다..


# LangChain 인스턴스 생성
lc = LangChain()

# GPT-3 모델을 LangChain에 추가
kogpt_model = KoGPTLangChainWrapper(model=model, tokenizer=tokenizer)
lc.add_model("kogpt", kogpt_model)

# 프롬프트 정의 및 모델 호출
prompt = "안녕하세요, 오늘 기분은 어떠신가요?"
response = lc.call_model("kogpt", prompt)

print("AI 응답:", response)
import os.path

import torch
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class MyMidm:
    def __init__(self, model_name, local_model_path, device="cpu"):
        self.model_name = model_name
        self.local_model_path = local_model_path
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = None
        self.model = None
        logging.info(f"self.device is : {self.device}")

    def load_model(self):
        logging.info(f"MyMidm's load_model() START.")
        self.tokenizer = AutoTokenizer.from_pretrained(
            # AutoTokenizer 를 쓴다고 https://huggingface.co/KT-AI/midm-bitext-S-7B-inst-v1 에 적혀있음.
            pretrained_model_name_or_path=self.model_name,
            trust_remote_code=True
        )
        logging.info(f"토크나이저 로드 완료.")
        self.model = AutoModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path=self.model_name,
            trust_remote_code=True
        )
        logging.info(f" 모델 로드 완료.")

    def save_model(self, model_type="Fine-tunned"):
        local_model_path = "./model/ori" if model_type == "original" else self.local_model_path
        logging.info(f"{model_type} 모델을 다음 경로에 저장합니다. \n {local_model_path}")
        if not os.path.exists(local_model_path):
            # 만일 저장할 경로가 없을 경우 directory 생성
            os.makedirs(local_model_path)
            logging.info(f"모델을 저장하기 위해 아래 경로를 생성하였습니다. \n {local_model_path}")
        self.tokenizer.save_pretrained(local_model_path)
        logging.info(f"토크나이저 저장 완료.")
        self.model.save_pretrained(local_model_path)
        logging.info(f"모델 저장 완료.")
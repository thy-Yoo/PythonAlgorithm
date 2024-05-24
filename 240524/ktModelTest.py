import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
import logging
import os
import psutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Fx . 메모리 사용량 기록 함수
def log_memory_usage():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    logger.info(f"Memory usage: RSS={mem_info.rss / (1024 ** 2):.2f} MB, VMS={mem_info.vms / (1024 ** 2):.2f} MB")

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logging.info(f"Using device: {device}")

    # Hugging Face에서 모델 불러오기
    logging.info("Loading tokenizer from Hugging Face.")
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path = "KT-AI/midm-bitext-S-7B-inst-v1",
        trust_remote_code=True
    )
    logging.info("Tokenizer loaded successfully.")
    log_memory_usage()

    logging.info("Loading model from Hugging Face.")
    model = AutoModelForCausalLM.from_pretrained(
        pretrained_model_name_or_path = "KT-AI/midm-bitext-S-7B-inst-v1",
        trust_remote_code=True
    )
    logging.info("Model loaded successfully.")
    log_memory_usage()

    # 로컬 경로에 저장
    local_model_path = "./model/pretrained/kt"
    # 절대 경로 확인
    absolute_path = os.path.abspath(local_model_path)
    logging.info(f"Absolute path of local_model_path: {absolute_path}")

    # 폴더가 존재하지 않을 경우 생성
    if not os.path.exists(local_model_path):
        os.makedirs(local_model_path)
        logging.info(f"Directory {local_model_path} created.")

    logging.info("Saving tokenizer and model to local path.")
    tokenizer.save_pretrained(local_model_path)
    model.save_pretrained(local_model_path)
    logging.info("Tokenizer and model saved successfully.")

    model.to(device)
    model.eval()
    logging.info("Model moved to device and set to evaluation mode.")

    dummy_data = "###User;AI란?\n###Midm;"
    data = tokenizer(dummy_data, return_tensors="pt").to(device)

    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    # 공식 문서
    # pred = model.generate(
    #     input_ids=data.input_ids[..., :-1].cuda(),
    #     streamer=streamer,
    #     use_cache=True,
    #     max_new_tokens=float('inf')
    # )
    # decoded_text = tokenizer.batch_decode(pred[0], skip_special_tokens=True)
    # 텍스트 스트리머 설정
    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

    # 예측 생성
    pred = model.generate(
        input_ids=data.input_ids[..., :-1],
        streamer=streamer,
        use_cache=True,
        max_new_tokens=float('inf')
    )

    # 결과 디코딩
    decoded_text = tokenizer.batch_decode(pred[0], skip_special_tokens=True)
    print(decoded_text)

if __name__ == "__main__":

    main()

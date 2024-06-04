from my_midm import MyMidm
import torch, os, logging, sys
from transformers import AutoTokenizer, AutoModelForCausalLM
# from huggingface_hub import HFValidationError

def model_download():
    # 1회성 모델 다운로드 소스
    model_name = "KT-AI/midm-bitext-S-7B-inst-v1"
    local_model_path = "./model/"

    midm = MyMidm(
        model_name=model_name,
        local_model_path=local_model_path,
        device="cpu"
    )
    midm.download_model()

def main():

    # model_download() #24.06.03 다운로드 완료.
    try:
        model_name = "myMidm"
        local_model_path = "./model/snapshot"

        midm = MyMidm(
            model_name=model_name,
            local_model_path=local_model_path,
            device='cuda' if torch.cuda.is_available() else 'cpu'
        )
        midm.load_model()

    except Exception as e:
        logging.error(f"예기치 못한 오류 발생: {e}")
        if 'midm' in locals():
            midm.stop_load_model_thread() # 쓰레드를 종료해주지 않으면 메인 쓰레드 종료시 (에러)에도 계속 실행됨..
        sys.exit(1)

if __name__ == "__main__":
    main()

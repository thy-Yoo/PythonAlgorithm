import os.path

import torch, threading
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
from huggingface_hub import snapshot_download
from accelerate import init_empty_weights, load_checkpoint_in_model
from utils.resource_monitoring import ResourceMonitoring
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class MyMidm:
    def __init__(self, model_name, local_model_path, device):
        self.model_name = model_name
        self.local_model_path = local_model_path
        self.device = device
        self.tokenizer = None
        self.model = None
        logging.info(f"self.device is : {self.device}")
        self.stop_event = threading.Event() # 더 세밀한 조정을 위해 여기에 추가
        self.model_thread = None # 다른 곳에서 에러 발생 시 모델 로드 쓰레드도 작동을 중단하기 위함.

    # 별도의 쓰레드를 이용하는 모델 로드 함수
    def load_model_thread(self):
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                pretrained_model_name_or_path=self.local_model_path,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            logging.info(f" 모델 로드 완료.")
            self.model.to(self.device)
            logging.info(f" 모델은 현재 device={self.device}에 위치합니다. ")
        except Exception as e:
            logging.info(f"모델 로드 중 예외 발생: {e}")
            self.stop_event.set()  # 예외 발생 시 이벤트 설정

    def stop_load_model_thread(self):
        if self.model_thread and self.model_thread.is_alive():
            self.stop_event.set()
            self.model_thread.join(timeout=1)
            logging.info("모델 로드 스레드가 중단되었습니다.")

    def load_model(self):
        logging.info(f"MyMidm's load_model() START.")
        self.tokenizer = AutoTokenizer.from_pretrained(
            # AutoTokenizer 를 쓴다고 https://huggingfdef load_model(self):ace.co/KT-AI/midm-bitext-S-7B-inst-v1 에 적혀있음.
            pretrained_model_name_or_path=self.local_model_path,
            trust_remote_code=True
        )
        logging.info(f"토크나이저 로드 완료.")
        logging.info(f"{self.local_model_path} 경로의 모델을 로드 합니다.")

        # 모델 로드를 시도할 최대 메모리 사용량 임계치 (퍼센트)
        rss_threshold = 70
        vms_threshold = 230

        # 메모리 사용량이 충분히 낮아질 때까지 대기
        # while not ResourceMonitoring.monitor_memory_usage(rss_threshold, vms_threshold):
        #     logging.info("메모리 사용량이 임계치를 초과하여 대기 중입니다.")
        #     ResourceMonitoring.log_memory_usage()
        #     time.sleep(3)  # 3초 간격으로 메모리 체크

        # 모델 로드 스레드 시작
        model_thread = threading.Thread(target=self.load_model_thread)
        model_thread.start()

        # 모델 로드 작업 중 메모리 사용량 모니터링
        while model_thread.is_alive():
            rss_percent, vms_percent, rss_mb, vms_mb = ResourceMonitoring.get_memory_usage()
            logging.info(f"현재 메모리 사용량: RSS={rss_percent:.2f}% ({rss_mb:.2f} MB), VMS={vms_percent:.2f}% ({vms_mb:.2f} MB)")
            if rss_percent > rss_threshold or vms_percent > vms_threshold:
                logging.info("메모리 사용량 초과로 모델 로드 중단 시도 중...")
                self.stop_event.set()  # 메모리 사용량 초과 시 중단 시도
                model_thread.join(timeout=1)  # 모델 로드 스레드가 종료될 때까지 대기 (1초 대기 후 강제 종료 시도)
                break  # 루프 종료
            time.sleep(2)  # 2초 간격으로 메모리 체크

        if self.model is None:
            logging.info(f"모델 로드에 실패하여 메모리 최적화 후 재시도 합니다.")
            config = AutoConfig.from_pretrained(
                pretrained_model_name_or_path=self.local_model_path, # /config.json 를 로드하는 용도
                trust_remote_code=True
            )
            with init_empty_weights():
                self.model = AutoModelForCausalLM.from_config(
                    config,
                    trust_remote_code=True,
                )
            load_checkpoint_in_model(
                self.model,
                checkpoint=f"{self.local_model_path}",
                device_map="auto",
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            logging.info(f" 모델 로드 완료.")
            self.model.to(self.device)
            logging.info(f" 모델은 현재 device={self.device}에 위치합니다. ")




    # Fx. 원본 모델을 다운로드 하는 함수
    def download_model(self):
        snapshot_path = f"{self.local_model_path}/snapshot"

        if not os.path.exists(snapshot_path):
            os.makedirs(snapshot_path) # 폴더가 없을 경우 생성
            logging.info(f"Directory {snapshot_path} created.")

        logging.info(f"{self.model_name}'s model download START.")
        snapshot_download(
            self.model_name,
            local_dir=snapshot_path,
            ignore_patterns=["*.h5", "*.ot", "*.onnx"])
        logging.info("원본 모델 다운로드 완료.")

    # Fx. 파인튜닝 완료한 모델을 저장 할 함수
    def save_model(self):
        local_model_path = self.local_model_path
        logging.info(f"모델을 다음 경로에 저장합니다. \n {local_model_path}")
        if not os.path.exists(local_model_path):
            # 만일 저장할 경로가 없을 경우 directory 생성
            os.makedirs(local_model_path)
            logging.info(f"모델을 저장하기 위해 아래 경로를 생성하였습니다. \n {local_model_path}")
        self.tokenizer.save_pretrained(local_model_path)
        logging.info(f"토크나이저 저장 완료.")
        self.model.save_pretrained(local_model_path)
        logging.info(f"모델 저장 완료.")
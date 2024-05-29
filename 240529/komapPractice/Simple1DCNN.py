import torch
import torch.nn as nn
import torch.nn.functional as F
from utils.ColorPrint import ColorPrint as printer

class Simple1DCNN(nn.Module): # 1차원 합성곱 신경망 모델
    def __init__(self, num_features, num_classes):
        """
        1D CNN 모델을 초기화합니다. 입력 특성 수와 출력 클래스 수에 맞게 네트워크를 구성합니다.
        :param num_features: 입력 특성의 수
        :param num_classes: 출력 클래스의 수
        """
        super(Simple1DCNN, self).__init__()
        # 1D 합성곱 층 (첫번째 레이어) : 입력 채널 1, 출력 채널 16, 커널 크기 3, 패딩 1
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=16, kernel_size=3, padding=1)

        # 1D 합성곱 층 (두번째 레이어): 입력 채널 16, 출력 채널 32, 커널 크기 3, 패딩 1
        self.conv2 = nn.Conv1d(in_channels=16, out_channels=32, kernel_size=3, padding=1)

        # 맥스풀링 레이어 : 합성곱 레이어 사이에 삽입되어서 특징 맵의 차원을 줄이고, 계산 효율성을 높이며, 모델의 과적합을 방지하는 데 사용되는 층.
        # (필수 적으로 있어야 하는 층은 아님)
        self.pool = nn.MaxPool1d(kernel_size=2, stride=2)

        # 1D 합성곱 층 (세번째 레이어): 입력 채널 32, 출력 채널 64, 커널 크기 3, 패딩 1
        self.conv3  = nn.Conv1d(in_channels=32, out_channels=64, kernel_size=3, padding=1)

        # 1D 합성곱 층 (세번째 레이어): 입력 채널 64, 출력 채널 128, 커널 크기 3, 패딩 1
        self.conv4 = nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, padding=1)

        # 완전 연결 층 이라는데..
        self.fc = nn.Linear(128 * (num_features // 4), num_classes)  # Adjusting for two pooling layers
        # nn.Linear:
        # nn.Linear는 PyTorch의 신경망 모듈 중 하나로,
        # 입력 데이터를 선형 변환(fully connected layer)시키는 것이다.. 이 모듈은 입력과 출력 사이의 선형 관계를 학습한다.





        ## idea 1. 동적으로 레이어 수를 증가 시키면 어떨까? 특정 멈춤 조건 같을 걸 만들어서, 조건을 충족 시킬 때 까지 레이어 수를 늘리는 것이다.

    # Fx. 순전파 함수
    def forward(self, x):
        """
        모델의 순전파를 실행합니다. 입력 x를 받아서 네트워크를 통과시킨 후 결과를 반환합니다.
        :param x: 모델의 입력 데이터
        :return: 모델의 출력 데이터
        """
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = self.pool(x)
        printer.green(x)
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        x = self.pool(x)
        printer.green(x) # 이 x 값들은 다차원 텐서이다.

        x = torch.flatten(x, 1)  # Flatten all dimensions except batch
        # flatten 최종 평탄 화.
        x = self.fc(x)
        return x

    # Fx. my_ 커스텀 함수 (사이트에서 제공되지 않은 함수에는  주석에 my_ 를 붙이겠음 )
    def print_model_info(self):
        printer.blue("Model Structure:")
        print(self)

        printer.blue("\nModel Parameters:") # 파라미터: datas 로 부터 학습되는 값 들 (가중치, 편향 같은 거)
        for name, param in self.named_parameters():
            if param.requires_grad:
                print(f"{name}: {param.size()}")

        printer.blue("\nHyperparameters:")
        for name, param in self.named_parameters():
            print(f"{name}: {param.size()}, requires_grad={param.requires_grad}")

        printer.blue("\nState Dict:")
        for name, param in self.state_dict().items():
            print(f"{name}: {param.size()}")

# 모델 초기화 (예시로 num_features와 num_classes 값을 설정)
num_features = 100
num_classes = 10
model = Simple1DCNN(num_features=num_features, num_classes=num_classes)

# 모델 정보 출력
model.print_model_info()


import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR
import Simple1DCNN

class ModelTrainer:
    def __init__(self, train_loader, val_loader, test_loader, learning_rate=0.001):
        """
        모델 트레이너를 초기화합니다. 데이터 로더와 학습률을 설정하고, 모델을 구성합니다.
        :param train_loader: 훈련 데이터를 로드하는 DataLoader 객체
        :param val_loader: 검증 데이터를 로드하는 DataLoader 객체
        :param test_loader: 테스트 데이터를 로드하는 DataLoader 객체
        :param learning_rate: 모델 최적화에 사용될 학습률
        """
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.test_loader = test_loader

        features, labels = next(iter(train_loader))
        num_features = features.size(-1)
        num_classes = labels.size(-1)

        # 모델 불러옴(num_features, num_classes는 자동으로 매칭)
        self.model = Simple1DCNN(num_features=num_features, num_classes=num_classes)
        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.scheduler = StepLR(self.optimizer, step_size=250, gamma=0.05)
        self.history = {'train_loss': [], 'val_loss': []}
        self.best_model = None
        self.check = 0

    def train(self, epochs):
        """
        모델을 훈련합니다. 지정된 에포크 수만큼 훈련하고, 각 에포크마다 검증 손실을 계산합니다.
        :param epochs: 훈련을 수행할 총 에포크 수
        """
        self.model.train()
        best_val_loss = float('inf')  # 초기 최소 검증 손실을 무한대로 설정. 점점 낮춰갈 것이기 때문.
        for epoch in range(epochs):
            running_loss = 0.0 # epoch 마다 손실을 누적 시킬 변수
            for inputs, labels in self.train_loader:
                inputs, labels = inputs.to(torch.float32), labels.to(torch.float32) # 입력값,레이블을 float32 로 변환.
                # float32 형식이 대부분의 딥러닝 프레임워크에서 기본적으로 사용되는 형식으로, GPU 연산에서도 최적화되어 있다고 한다.
                # float64 는 메모리가 너무 크다고..
                self.optimizer.zero_grad()
                outputs = self.model(inputs.unsqueeze(1))  # Ensure channel dimension
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()
                running_loss += loss.item()
            avg_train_loss = running_loss / len(self.train_loader)
            self.history['train_loss'].append(avg_train_loss)
            val_loss = self.validate()
            self.history['val_loss'].append(val_loss)
            print(f'Epoch {epoch + 1}: Training Loss: {avg_train_loss}, Validation Loss: {val_loss}')

            # 검증 손실이 이전 최소값보다 낮은 경우 모델 저장
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                self.best_model = self.model.state_dict()
                print(f'New best model saved with validation loss: {best_val_loss}')
            self.scheduler.step()

    def validate(self):
        """
        검증 데이터셋을 사용하여 모델의 성능을 평가합니다. 평균 검증 손실을 계산합니다.
        :return: 계산된 평균 검증 손실
        """
        self.model.eval()
        total_val_loss = 0.0
        with torch.no_grad():
            for inputs, labels in self.val_loader:
                inputs, labels = inputs.to(torch.float32), labels.to(torch.float32)
                outputs = self.model(inputs.unsqueeze(1))
                loss = self.criterion(outputs, labels)
                total_val_loss += loss.item()
        avg_val_loss = total_val_loss / len(self.val_loader)
        return avg_val_loss

    def test(self):
        """
        테스트 데이터셋을 사용하여 모델의 성능을 평가합니다. 평균 테스트 손실을 출력합니다.
        """

        self.model.load_state_dict(self.best_model)
        self.model.eval()  # 평가 모드로 설정

        total_test_loss = 0.0
        with torch.no_grad():
            for inputs, labels in self.test_loader:
                inputs, labels = inputs.to(torch.float32), labels.to(torch.float32)
                outputs = self.model(inputs.unsqueeze(1))
                loss = self.criterion(outputs, labels)
                total_test_loss += loss.item()
        print(f'MSE Loss for test: {total_test_loss / len(self.test_loader)}')

    def get_history(self):
        """
        훈련 및 검증 손실의 기록을 반환합니다.
        :return: 훈련 및 검증 손실이 기록된 딕셔너리
        """
        return self.history

    def predict(self, input_tensor):
        """
        입력 텐서에 대해 모델을 사용하여 예측을 수행합니다.
        :param input_tensor: 예측을 수행할 입력 텐서
        :return: 예측 결과
        """
        self.model.load_state_dict(self.best_model)
        self.model.eval()  # 평가 모드로 설정
        with torch.no_grad():
            input_tensor = input_tensor.to(torch.float32)
            output = self.model(input_tensor.unsqueeze(0).unsqueeze(0))  # Adjust dimensions if necessary
        return output.squeeze().numpy()  # Convert to numpy array for easy handling
import torch
from torch.utils.data import Dataset, DataLoader, random_split
from sklearn.preprocessing import StandardScaler

class Custom_Dataset(Dataset):
    def __init__(self, X_df, Y_df, test_ratio, val_ratio):
        """
        데이터셋을 초기화하고, 특정 열을 바탕으로 데이터프레임을 설정합니다.
        :param X_df: 입력 데이터프레임 중 특성을 포함하는 부분
        :type X_df: pd.DataFrame
        :param Y_df: 입력 데이터프레임 중 레이블을 포함하는 부분
        :type Y_df: pd.DataFrame
        :param test_ratio: 테스트 세트로 설정할 데이터 비율
        :type test_ratio: float
        :param val_ratio: 검증 세트로 설정할 데이터 비율
        :type val_ratio: float
        """
        self.features = X_df.values
        self.labels = Y_df.values
        # Standardizing the features
        scaler = StandardScaler() # 데이터의 각 특징을 평균이 0이고 표준편차가 1이 되도록 변환.
        self.features = scaler.fit_transform(self.features)

        # Splitting the dataset
        total_length = len(self.features)
        test_len = int(total_length * test_ratio)
        valid_len = int(total_length * val_ratio)
        train_len = total_length - test_len - valid_len
        self.train_dataset, self.val_dataset, self.test_dataset = random_split(self, [train_len, valid_len, test_len])

    def __len__(self):
        """
        데이터셋의 샘플 개수를 반환합니다.
        :return: 샘플 개수
        :rtype: int
        """
        return len(self.features)

    def __getitem__(self, idx):
        """
        주어진 인덱스에 해당하는 샘플을 데이터셋에서 검색합니다.
        :param idx: 검색할 샘플의 인덱스
        :type idx: int
        :return: 특성 텐서와 레이블 텐서가 포함된 튜플
        :rtype: tuple
        """
        # Convert arrays to tensors
        features_tensor = torch.tensor(self.features[idx], dtype=torch.float32)
        labels_tensor = torch.tensor(self.labels[idx], dtype=torch.float32)
        return features_tensor, labels_tensor

    def get_data_loaders(self, batch_size=64, shuffle_train=True):
        """
        훈련, 검증, 테스트 세트를 위한 데이터 로더를 생성하고 반환합니다.
        :param batch_size: 배치 크기
        :type batch_size: int
        :param shuffle_train: 훈련 데이터 셔플 여부
        :type shuffle_train: bool
        :return: 훈련, 검증, 테스트 데이터 로더
        :rtype: tuple
        """
        train_loader = DataLoader(self.train_dataset, batch_size=batch_size, shuffle=shuffle_train)
        val_loader = DataLoader(self.val_dataset, batch_size=batch_size, shuffle=False)
        test_loader = DataLoader(self.test_dataset, batch_size=batch_size, shuffle=False)
        return train_loader, val_loader, test_loader
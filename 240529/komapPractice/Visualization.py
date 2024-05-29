import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage import color

class Visualization:
    def __init__(self) -> None:
        pass

    def show_corr(self, data):
        """
        데이터의 상관관계 행렬을 시각화합니다.
        :param data: 분석할 DataFrame을 포함한 데이터 객체
        """
        f = plt.figure(figsize=(19, 15))
        plt.rc('font', family='NanumGothic')
        plt.rcParams['axes.unicode_minus'] = False
        plt.matshow(data.df.corr(), fignum=f.number)
        plt.xticks(range(data.df.select_dtypes(['number']).shape[1]), data.df.select_dtypes(['number']).columns,
                   fontsize=14, rotation=90)
        plt.yticks(range(data.df.select_dtypes(['number']).shape[1]), data.df.select_dtypes(['number']).columns,
                   fontsize=14)
        cb = plt.colorbar()
        cb.ax.tick_params(labelsize=14)
        plt.title('Correlation Matrix', fontsize=16)

    def plot_training_history(self, history):
        """
        훈련 및 검증 손실의 기록을 시각화합니다.
        :param history: 'train_loss'와 'val_loss'를 키로 가지는 손실 기록 딕셔너리
        """
        train_losses = history['train_loss']
        val_losses = history['val_loss']
        epochs = range(1, len(train_losses) + 1)

        plt.figure(figsize=(10, 5))
        plt.plot(epochs, train_losses, label='Training Loss')
        plt.plot(epochs, val_losses, label='Validation Loss')
        plt.title('Training and Validation Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_color_predictions(self, actual_lab, predicted_lab):
        """
        실제와 예측된 LAB 색상값을 RGB 색상으로 변환하여 시각화합니다.
        :param actual_lab: 실제 LAB 색상값
        :param predicted_lab: 예측된 LAB 색상값
        """
        # LAB 값으로부터 RGB 값 계산
        actual_rgb = color.lab2rgb(actual_lab)
        predicted_rgb = color.lab2rgb(predicted_lab)

        fig, ax = plt.subplots(1, 2, figsize=(6, 3))



        # 실제 색상 패치
        ax[0].add_patch(patches.Rectangle((0, 0), 1, 1, color=actual_rgb))
        ax[0].set_xlim(0, 1)
        ax[0].set_ylim(0, 1)
        ax[0].axis('off')
        ax[0].set_title('Actual Color')

        # 예측 색상 패치
        ax[1].add_patch(patches.Rectangle((0, 0), 1, 1, color=predicted_rgb))
        ax[1].set_xlim(0, 1)
        ax[1].set_ylim(0, 1)
        ax[1].axis('off')
        ax[1].set_title('Predicted Color')

        plt.show()
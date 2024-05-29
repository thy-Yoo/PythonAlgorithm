import pandas as pd

class Data:
    def __init__(self, excel_path):
        """
        Data 객체를 초기화하고 엑셀 파일을 읽어 데이터프레임을 만듭니다.
        엑셀 파일 형식은 1, 2행이 헤더, 3행부터 데이터로 이루어져 있습니다.
        :param excel_path: 엑셀 파일 경로
        :type excel_path: str
        """
        self.df = pd.read_excel(excel_path, header=[0, 1])
        # 첫 번째 열 제거 (보통 엑셀에서 불필요한 인덱스 열이 포함된 경우)
        self.df.drop(self.df.columns[1], axis=1, inplace=True)
        self.df.drop(self.df.columns[0], axis=1, inplace=True)
        # 첫 두 데이터 행(보통 엑셀 파일에서 설정 또는 메타 데이터 행) 제거
        self.df.drop([0, 1], inplace=True)
        # 인덱스 리셋
        self.df.reset_index(drop=True, inplace=True)
        # 특정 중요한 열에서 NaN 값 제거
        self.df.dropna(subset=[('내광성 시험 전 검사', 'L*')], inplace=True)
        self.df.dropna(subset=[('내광성 시험 전 검사', 'a*')], inplace=True)
        self.df.dropna(subset=[('내광성 시험 전 검사', 'b*')], inplace=True)

    def column_count(self):
        """
        데이터프레임의 열 수를 반환합니다.
        :return: 데이터프레임의 열 수
        :rtype: int
        """
        return len(self.df.columns.tolist())

    def unique_counts(self, dropna=False):
        """
        데이터프레임의 각 열에서 유니크한 값의 수를 계산합니다.
        dropna 매개변수가 True일 경우, NaN 값은 유니크 값에서 제외됩니다.
        :param dropna: NaN 값을 유니크 값 계산에서 제외할지 여부
        :type dropna: bool
        :return: 각 열의 유니크 값 수
        :rtype: pd.Series
        """
        return self.df.nunique(dropna=dropna)

    def show_data(self):
        """
        데이터프레임의 처음 몇 행을 출력합니다.
        """
        print(self.df.head())

    def my_show_data(self):
        pd.set_option('display.max_columns', None)  # 모든 컬럼을 생략 없이 출력
        pd.set_option('display.expand_frame_repr', False)  # 데이터프레임의 여러 줄에 걸쳐 출력 방지
        print("Displaying data...")
        print(self.data.head())  # 데이터프레임의 첫 5개 행을 출력
        pd.reset_option('display.max_columns')  # 설정 복원
        pd.reset_option('display.expand_frame_repr')  # 설정 복원




    def get_data(self):
        """
        현재 데이터프레임 객체를 반환합니다.
        :return: 현재 데이터프레임
        :rtype: pd.DataFrame
        """
        return self.df

    def set_columns(self, columns_list):
        """
        현재 데이터프레임의 컬럼 을 주어진 리스트에 해당하는 컬럼만 남깁니다.
        """
        self.df = self.df[columns_list]

    def get_columns(self):
        """
        현재 데이터프레임의 컬럼 정보를 반환합니다.
        이 메소드는 데이터프레임의 모든 컬럼 이름을 반환하므로, 구조 파악에 유용합니다.

        :return: 현재 데이터프레임의 컬럼 이름들
        :rtype: Index
        """
        return self.df.columns

    def set_xy(self, y_columns):
        """
        X인자와 Y인자로 나누어 반환합니다.
        :return: X인자와 Y인자(리스트형태)
        :rtype: pd.DataFrame, List
        """
        Y = self.df[y_columns].apply(list, axis=1)
        # X = self.df[x_columns]
        X = self.df.drop(y_columns, axis=1)
        return X, Y
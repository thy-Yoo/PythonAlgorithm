import pandas as pd

class Preprocessing:
    def __init__(self):
        self.encodings = {}  # 레이블 인코딩을 저장할 딕셔너리

    def fit(self, data_1, data_2):
        """
        여러 데이터프레임에서 훈련 데이터에 대해 레이블 인코딩을 학습합니다.

        :param dfs: 가변 인자로 여러 데이터프레임을 받습니다.
        """
        # 데이터프레임들을 통합
        combined_df = pd.concat([data_1.df, data_2.df], ignore_index=True)

        # 객체 타입의 컬럼만 선택하여 레이블 인코딩을 수행
        for column in combined_df.select_dtypes(include=['object']).columns:
            unique_categories = combined_df[column].unique()
            self.encodings[column] = {category: idx for idx, category in enumerate(unique_categories)}
        print(self.encodings)

    def remove_low_variance(self, data):
        """
        데이터프레임에서 유니크한 값이 2개 미만인 열을 제거합니다. NaN 값은 고려하지 않습니다.
        :return: 낮은 변동성을 제거한 후의 데이터프레임
        :rtype: pd.DataFrame
        """
        data.df = data.df.loc[:, data.df.nunique(dropna=True) > 1]

    def remove_unnamed_columns(self, data):
        """
        데이터프레임에서 첫 번째 레벨의 인덱스가 'Unnamed'으로 시작하는 열을 제거합니다.
        :return: 'Unnamed' 열이 제거된 후의 데이터프레임
        :rtype: pd.DataFrame
        """
        mask = ~data.df.columns.get_level_values(0).str.startswith('Unnamed')
        data.df = data.df.loc[:, mask]

    def adjust_specific_column(self, data):
        # Dorosperse Blue KKL Always made from ARCHROMA
        # data.df.loc[(data.df['Lab 배합 염료 #3 명'].isna() is False) & (
        #    data.df['Lab 배합 염료 #3 제조사명'].isna()), 'Lab 배합 염료 #3 제조사명'] = 'ARCHROMA'
        # data.fillna({x: 0 for x in ['Lab 배합 염료 #2 투입량', 'Lab 배합 염료 #3 투입량', 'Lab 배합 염료 #4 투입량']}, inplace=True)
        data.df.loc[:, ['Lab 배합 염료 #2 투입량', 'Lab 배합 염료 #3 투입량']].fillna(0, inplace=True)

    def collapse_multiindex_columns(self, data):
        """
        주어진 멀티컬럼을 단일 컬럼으로 통합합니다. 각 멀티컬럼의 레벨을 연결하여 하나의 컬럼 이름으로 만듭니다.
        첫 번째 레벨의 이름이 두 번째 레벨에 이미 포함되어 있는 경우, 중복을 제거합니다.
        :param df: 통합할 멀티컬럼을 포함한 pandas DataFrame
        :type df: pd.DataFrame
        :return: 단일 컬럼 인덱스를 가진 데이터프레임
        :rtype: pd.DataFrame
        """
        new_columns = []
        for col in data.df.columns.values:
            if isinstance(col, tuple):
                # 비교를 위해 임시로 공백을 제거한 컬럼명 생성
                clean_col1 = col[0].replace(' ', '')
                clean_col2 = col[1].replace(' ', '')
                # 중복을 확인하되 실제 컬럼명 생성 시에는 원본을 사용
                if clean_col1 in clean_col2:
                    new_columns.append(col[1])
                else:
                    new_columns.append('_'.join(col))
            else:
                new_columns.append(col)

        data.df.columns = new_columns

    def change_dtypes(self, data):
        """
        int 와 float형태로 치환가능한 데이터타입을 object에서 변환하여 반환합니다.

        :return: 변환된 데이터타입를 가진 데이터프레임
        :rtype: pd.DataFrame
        """
        for column in data.df.columns:
            # errors='ignore'를 설정하면 변환할 수 없는 경우 원래 타입을 유지
            data.df[column] = pd.to_numeric(data.df[column], errors='ignore')

    def label_encode(self, data):
        """
        학습된 레이블 인코딩을 데이터프레임에 적용합니다.

        :param df: 적용할 데이터프레임
        :return: 변환된 데이터프레임
        :rtype: pd.DataFrame
        """
        for column in self.encodings.keys():
            # 매핑 딕셔너리를 사용하여 데이터 치환
            # 매핑에 없는 카테고리는 NaN으로 처리
            data.df[column] = data.df[column].map(self.encodings.get(column, {}))
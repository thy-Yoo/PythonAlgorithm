class ColorPrint:
    # 컬러 코드 정의
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    RESET = "\033[0m"

    # 인스턴스 생성 없이 클래스 이름을 통해 직접 호출할 수 있도록 @staticmethod 를 사용
    @staticmethod
    def red(text):
        print(f"{ColorPrint.RED}{text}{ColorPrint.RESET}")

    @staticmethod
    def green(text):
        print(f"{ColorPrint.GREEN}{text}{ColorPrint.RESET}")

    @staticmethod
    def yellow(text):
        print(f"{ColorPrint.YELLOW}{text}{ColorPrint.RESET}")

    @staticmethod
    def blue(text):
        print(f"{ColorPrint.BLUE}{text}{ColorPrint.RESET}")

    @staticmethod
    def magenta(text):
        print(f"{ColorPrint.MAGENTA}{text}{ColorPrint.RESET}")

    @staticmethod
    def cyan(text):
        print(f"{ColorPrint.CYAN}{text}{ColorPrint.RESET}")

# 사용 예제
# ColorPrint.red("This is a red text.")
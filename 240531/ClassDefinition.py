"""

클래스 메소드
클래스 내의 일반 메소드와, @classmethod 의 차이가 무엇인가??
일단 인스턴스 라는 개념을 알아야 한다.

'클래스와 인스턴스'


클래스는 일종의 청사진이다. (blueprint)
특정 유형의 객체를 만들기 위한 설계도 같은 것이다.
클래스를 통해 객체의 속성과 행동을 정의한다.

인스턴스는 그러한 클래스를 바탕으로 생성된 구체적인 객체이다.
설계도를 가지고 만들어진 실제 물건이라고 보면 된다.
예를 들면, Dog 라는 class 를 정의하면, Dog 클래스에는 모든 개들이 가져야 할 속성(나이, 무게, 행동(짖기 밥먹기 등)을 정의 할 수 있다. 그리고 실제 개를 구현하려면 Dog class 를 이용하는 것이다.
"""


class Dog:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(f"{self.name} is barking")


# 두 개의 인스턴스 생성
dog1 = Dog("Buddy", 3)
dog2 = Dog("Lucy", 4)

dog1.bark()  # Buddy is barking
dog2.bark()  # Lucy is barking
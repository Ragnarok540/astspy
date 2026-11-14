class TestClassA:
    def hello(self, name):
        print(f"hello {name}")


class TestClassB:
    @classmethod
    def hello_class(cls):
        print("hello")


class TestClassC(TestClassA):
    pass


class TestClassD(TestClassA, TestClassB):
    pass

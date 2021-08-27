class TestClass:
    def __init__(self):
        pass

    def __iter__(self):
        return [1, 2, 3, 4, 5].__iter__()


tc = TestClass()
for i in tc:
    print(i)

class Hello:
    t = '내가 상속해 줬어'

    def calc(self):
        return self.t

    @staticmethod
    def calc2():
        return Hello.t

    @classmethod
    def calc3(cls):
        return cls.t

class Hello2(Hello):
    t = '나는 상속 받았어'

instance = Hello2()
print(Hello2.calc(instance))    #나는 상속 받았어
print(Hello2.calc2())           #내가 상속해 줬어
print(Hello2.calc3())           #나는 상속 받았어

################################################################

class A():
    def __init__(self):
        print('self: ',self)
        print('init A')
        self.test_value = 'test2@'

    def __new__(cls):
        print('new A')
        return B().__new__(cls)

class B():

    def __init__(self):
        print('init B')
        self.test_value = 'test!'

a = A()
print(type(a))
print(a.test_value)

################################################################

class PrivateTest:
    def __init__(self):
        self.__유현 = 'yh'
        self.유현 = 'yh2'
        print('inside', self.__수현())

    def __수현(self):
        return 'sh'

    def 수현(self):
        return 'sh2'

test = PrivateTest()

print(test.수현())
print(test.유현)

#print(test.__수현())
#print(test.__유현)
# Class
class MyObj(object):
    def __init__(self, val):
        self.val = val

		
# Method to be added		
def new_method(self, value):
    return self.val + value


# Dynamic instance method ("bound method".)
from types import MethodType
obj.method = MethodType(new_method, obj, MyObj)
obj.method(5)

# Dynamic class method ("unbound method".)
from types import MethodType
MyObj.method = MethodType(new_method, None, MyObj)
obj2 = MyObj(2)
obj2.method(5)
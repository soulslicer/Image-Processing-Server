

class Obj(object):

    def __init__(self):
        print "CREATED"

    # def __enter__(self):
    #     print "RETURN SELF"
    #     return self

    def __exit__(self, type, value, traceback):
        print "DESTROYED"


def func():
    print "MY FUNC"

def func_recv(x):
    x()

func_recv(func)
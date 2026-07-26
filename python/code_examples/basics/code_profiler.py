import random 
def f1():
    l = [random.random() for i in range(100000)]
    l1 = sorted(l)
    l2 = [i for i in l1 if i<0.5]
    return [i*i for i in l2]

def f2():
    l = [random.random() for i in range(100000)]
    l1 = [i for i in l if i<0.5]
    l2 = sorted(l1)
    return [i*i for i in l2]

def f3():
    l = [random.random() for i in range(100000)]
    l1 = [i*i for i in l]
    l2 = sorted(l1)
    return [i for i in l1 if i<(0.5*0.5)]


def main():
    import cProfile
    cProfile.run('f1()')
    cProfile.run('f2()')
    cProfile.run('f3()')


if __name__ == '__main__':
    main()

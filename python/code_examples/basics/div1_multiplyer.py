def div1(x,y):
    print "%s/%s = %s" % (x, y, x/y)
    
def div2(x,y):
    print "%s//%s = %s" % (x, y, x//y)

def multipliers():
     return [lambda x : i * x for i in range(4)]


def main():
    div1(5,2)
    div1(5.,2)
    div2(5,2)
    div2(5.,2.)
    print [m(2) for m in multipliers()]
    list = ['a','b', 'c', 'd', 'e']
    print list[10]

if __name__ == "__main__":
  main()

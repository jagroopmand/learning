def tuple1():
    print ("=================================================")
    print (" Tuple ")
    t = ([1,2], [3,4], 5, {"a":6, "b":7})
    print ("T0: ", t[0])
    print ("T3: ", t[3])

def list1():
    print ("=================================================")
    print (" List ")
    l1=[1,4,6]
    print ("l2 :", l1[2])

def list_comp():
    print ("=================================================")
    print (" list_comp")
    l = [x for x in range(0,10,3)]
    print ("l:", l)

def lcomp():
    print ("=================================================")
    print (" List comp")
    l1=[1,4,6]
    l2 = [x**2 for x in l1 if x >= 4]
    print ("l1: ", l1)
    print ("l2: ", l2)
	
def dict_comp():
    print ("=================================================")
    print (" Dict comp")
    # Example: create a dict mapping numbers to their squares
    nums = [1, 2, 3, 4]
    d = {n: n * n for n in nums}
    print("d:", d)

def nested_lcomp():
    print ("=================================================")
    print (" Nested List comp")
    l1 = [[1 if row_idx == item_idx else 0 for item_idx in range(0,3)] for row_idx in range(0,3)]
    print ("l1: ", l1)

def set_comp1():
    print ("=================================================")
    print (" Set comp")
    names = [ 'Bob', 'JOHN', 'alice', 'bob', 'ALICE', 'J', 'Bob' ]
    print ({ name[0].upper() + name[1:].lower() for name in names if len(name) > 1 })

def dict_comp1():
    print ("=================================================")
    print (" Dict comp")
    mcase = {'a':10, 'b': 34, 'A': 7, 'Z':3}
    mcase_keyadd = { k.lower() : mcase.get(k.lower(), 0) + mcase.get(k.upper(), 0) for k in mcase.keys()}
    print ("mcase_keyadd :", mcase_keyadd)

def lambda_filter():
    print ("=================================================")
    print (" lambda_filter")
    print ("Remove elements of list that dont meet lambda criteria")
    l1=[x for x in range(10)]
    l2=list(filter(lambda x: x < 9 and x > 5, l1))
    print ("l1: ", l1)
    print ("l2: ", l2)
   
def lambda_map():
    print ("=================================================")
    print (" lambda_map")
    print ("Transform all elements of list by applying lambda")
    l1=[x for x in range(10)]
    l2=list(map(lambda x: x**3, l1))
    print ("l1: ", l1)
    print ("l2: ", l2)
	
def lambda_reduce():
    print ("=================================================")
    print (" lambda_reduce")

    print ("Reduces list to a single element after applying lambda")
    from functools import reduce
    l1 = [1,2,3,4]
    l2 = reduce((lambda x, y: x * y), l1)
    print ("Lst: ", l1)
    print ("Reduced list: ", l2)
	

def zip_unzip1():
    print ("=================================================")
    print (" Zip Unzip")
    l1=[x for x in range(10)]
    l2=[x for x in range(10,20)]
    l3=zip(l1,l2)
    l4,l5=zip(*l3)
    print ("l1: ", l1)
    print ("l2: ", l2)
    print ("Zipped l3: ", l3)
    print ("Unzipped l4: ", l4)
    print ("Unzipped l5: ", l5)

def yield1(n):
    print ("=================================================")
    print (" Yield: Return one num then yield/pause for next call")
    num = 0 
    while num < n:
      # print ("num: ", num)
       yield num
       num += 1

def main():
    tuple1()
    list1()
    lcomp()
    nested_lcomp()
    set_comp1()
    dict_comp1()
    list_comp()
    dict_comp()
    lambda_filter()
    lambda_map()
    lambda_reduce()
    zip_unzip1()
    sum_of_first_n = sum(yield1(100))
    print("Sum_of_first_n:", sum_of_first_n)

if __name__ == "__main__":
    main()



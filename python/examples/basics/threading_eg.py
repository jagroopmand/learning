#!/usr/bin/python

import threading
import sys

class myThread(threading.Thread):
    def __init__(self, tID, name, args):
        threading.Thread.__init__(self)
        self.tID = tID
        self.name = name
        self.args= args
               
    def run(self):
        print( "Starting: " + self.name)
        self.f1(self.name, self.args)
        print( "Ending: " + self.name)

    def f1(self, tname, args):
        try:
            print( 'in function f1')
            i = 0
            while i< 5:
                print(args['tname'], args['msg'])
                i = i +1
        except: 
            print("Error: unable to start thread", sys.exc_info()[0]   ) 
        
          


        
        
def main():
    args1 ={}
    args1['tname'] = 'thread1'
    args1['msg'] = 'thread1 says hi' 
    t1 = myThread(1, 't1', args1)
    
    args2 = {}
    args2['tname'] = 'thread2'
    args2['msg'] = 'thread2 says hi'
    t2 = myThread(2, 't2', args2)
    
    t1.start()
    t2.start()
	
if __name__ == '__main__':
  main()	

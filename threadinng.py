import threading

def infinite_loop():
  while 1==1:
    pass

def myname():
  print("hello world !!!")


t1=threading.Thread(target=infinite_loop)
t2=threading.Thread(target=myname)

t1.start()
t2.start()
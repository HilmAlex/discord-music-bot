import threading
import time

mutex = threading.Lock()  # is equal to threading.Semaphore(1)

def fun1():
    with mutex:
        band = False
        i = 0
        while i < 100:
            i += 1
            band = i < 100
            print(1, i, band)
    

def fun2():
    with mutex:
        band = True
        i = 0
        while band:
            i += 1
            band = i < 1000
            print(2, i, band)
    

threading.Thread(target=fun1).start()
threading.Thread(target=fun2).start()
threading.Thread(target=fun1).start()

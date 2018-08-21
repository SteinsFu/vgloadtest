import time 
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# custom wait function 
def mywait(that,method,name,mode=''):

    # with timer 
    if mode == 'T':
        start = time.perf_counter()
        # print("Start", start)
        result = that.wait.until(method)
        end = time.perf_counter()
        # print("End", end)
        that.log['results'][name].append(end-start)
        # print(end-start)
    return result

    # with other mode 
    # ... 
    

def timeit(func):
    def wrap(*args,**kws):
        start = time.clock()
        func(*args,**kws)
        end = time.clock()
        print(end-start)
        return func
    return wrap




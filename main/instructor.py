import sys
import time
import json
from measure import mywait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Instructor():

    view_config = {
        'TIMEIT': ['refresh_submission']        # tasks that need to be timed  
    }

    # controller 
    def __init__(self, parent, config):
        # initial the log 
        self.log = {
            'user_id': parent.user_id,
            'task': parent.task,
            'results': {},
            'stat': {}
        }
        for task in self.view_config['TIMEIT']:
            self.log['results'][task] = []
            self.log['stat'][task] = {}

        # set the configuration and invoke the coresponding function according to the type
        if(config["TYPE"] == 'view'):
            self.set_view_config(config)
            self.view(parent)

    # set the configuration for view 
    def set_view_config(self,config):
        self.view_config["ASSIGNMENT_ID"] = config["ASSIGNMENT_ID"]
        self.view_config["WAIT_TIME"] = config["WAIT_TIME"]
        self.view_config["NUMBER_OF_REFRESH"] = config["NUMBER_OF_REFRESH"]
        self.view_config["SLEEP_TIME"] = config["SLEEP_TIME"]


    # View and Refresh submission page 
    def view(self,that):
        # get the driver from parent
        driver = that.driver 

        # wait time for each actions 
        self.wait = WebDriverWait(driver,self.view_config["WAIT_TIME"])
        wait = self.wait
        
        # go to Assignment
        try:
            driver.find_element_by_xpath("//div[@id='" + self.view_config["ASSIGNMENT_ID"] + "']//a").click()
        except:
            print("\'" + that.user_id + "\':", "Find Assignment Failed:", sys.exc_info()[1])
            pass
        
        # switch to iframe
        try: 
            driver.switch_to.frame("contentFrame")
        
            # refresh multiple times

            count = 0 
            while count < self.view_config["NUMBER_OF_REFRESH"]: 
                count += 1       
                print("\'" + that.user_id + "\':", "Refresh Submission Start:", count)

                # click the Refresh Submission 
                try:
                    xpath = "//form[@name='updateAssignmentForm']//div[@class='row sm-valign']//button"
                    element = wait.until(EC.element_to_be_clickable((By.XPATH,xpath)))
                    element.click()
                except:
                    print("\'" + that.user_id + "\':", "Refresh Submission Failed:", sys.exc_info()[0])
                    pass 

                # wait for the pop up disappear(server loading)
                try:
                    name = self.view_config['TIMEIT'][0]
                    xpath = "//md-dialog//div[@class='row no-padding']"   
                    wait.until(EC.visibility_of_element_located((By.XPATH,xpath)))
                    mywait(self,EC.invisibility_of_element_located((By.XPATH,xpath)),name,'T')
                    print("\'" + that.user_id + "\':", "Refresh Submission Success:", count)

                except:
                    print("\'" + that.user_id + "\':", "Wait for Refresh Submission Failed:",sys.exc_info()[0])
                    driver.refresh()
                    driver.switch_to.frame("contentFrame")
                    pass 

                time.sleep(self.view_config["SLEEP_TIME"])
               
            
        except:
            print("\'" + that.user_id + "\':", "Fail to switch to iframe: ",sys.exc_info()[1])
            pass
        

        
        # calculate the min, max, avg in the log['results']
        for task in self.log['results']:
            self.log['stat'][task]['min'] = min(self.log['results'][task])
            self.log['stat'][task]['max'] = max(self.log['results'][task])
            self.log['stat'][task]['avg'] = sum(self.log['results'][task]) / float(len(self.log['results'][task]))

        # delete the detail records for submission
        del self.log['results']

        # write the results under path:'/test_results/<TEST_CASE>.txt'
        file = open('log/test_results/' + that.TEST_CASE + '.txt','a+')
        file.write("\n")
        file.write(json.dumps(self.log, indent=4))
        file.close()
          
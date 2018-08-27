import sys
from measure import mywait
import time
import json
import csv
from time import clock
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Lock
from random import randint

lock = Lock()

class Student():

    submit_config = {
        'TIMEIT': ['load_page','submit_assignment']     # tasks that need to be timed  
    }

    # user data can be used:
    # parent.user_id
    # parent.password
    # parent.computing_id
    # parent.bb_user_role
    # parent.user_account_type
    # parent.course
    # parent.task
    def __init__(self, parent, submit_config, default_config):
        # set default config
        self.GROUP_CSV_PATH = default_config['DEFAULT']['GROUP_CSV_PATH']

        # initial the log 
        self.log = {
            'user_id': parent.user_id,
            'task': parent.task,
            'results': {},
            'stat': {}
        }
        for task in self.submit_config['TIMEIT']:
            self.log['results'][task] = []
            self.log['stat'][task] = {}

        # set the configuration and invoke the coresponding function according to the type
        if(submit_config["TYPE"] == 'submit'):
            self.set_submit_config(parent, submit_config)
            self.submit(parent)
        
    # set submission configuration
    def set_submit_config(self, parent, submit_config):
        self.submit_config["ASSIGNMENT_ID"] = submit_config["ASSIGNMENT_ID"]
        self.submit_config["WAIT_TIME"] = float(submit_config["WAIT_TIME"])
        self.submit_config["NUMBER_OF_SUBMISSION"] = submit_config["NUMBER_OF_SUBMISSION"]
        self.submit_config["SLEEP_TIME"] = float(submit_config["SLEEP_TIME"])

        # if submit_config["SECTION"] == '':
        #     try:
        #         self.submit_config["SECTION"] = "2016R1-NURS1151" + parent.sections[0].replace("\'", "")
        #     except:
        #         self.submit_config["SECTION"] = "2016R1-NURS1151-"
        #         print("\'" + parent.user_id + "\':", "Compose Course Section Failed:", sys.exc_info()[0:2])
        #         pass
        # else:
        #     self.submit_config["SECTION"] = submit_config["SECTION"]

        self.submit_config["MARKER"] = submit_config["MARKER"]

    # student submission multiple times
    def submit(self, parent):
        # get the driver from caller
        driver = parent.driver

        # wait time for each actions 
        self.wait = WebDriverWait(driver,self.submit_config["WAIT_TIME"]) 
        wait = self.wait

        # counter for no. of submission
        count = 0

        # should be invoked when first time loading or refreshing
        def load_page():

            # # go to Assignment by the 'ASSIGNMENT_ID'
            # try:
            #     driver.find_element_by_xpath("//div[@id='" + self.submit_config["ASSIGNMENT_ID"] + "']//a").click()
            # except:
            #     print("\'" + parent.user_id + "\':", "Find Assignment Failed:", sys.exc_info()[0:2])
            #     pass
            # time.sleep(parent.WAIT_TIME_IFRAME)

            # go to Assignment by the 'name' (When ASSIGNMENT_ID == 'the_name_of_the_asg')
            try:
                driver.find_element_by_xpath("//a/span[contains(text(), '" + self.submit_config["ASSIGNMENT_ID"] + "')]").click()
            except:
                print("\'" + parent.user_id + "\':", "Find Assignment Failed:", sys.exc_info()[0:2])
                pass
            time.sleep(parent.WAIT_TIME_IFRAME)


            # switch to our iframe
            try:
                driver.switch_to.frame("contentFrame")
            except:
                print("\'" + parent.user_id + "\':", "Fail to switch to iframe", "at submission:", count)
                pass

            # wait for loading the update page
            try:  
                name = self.submit_config['TIMEIT'][0]
                xpath = "//md-dialog//div[@class='row no-padding']"   
                mywait(self,EC.invisibility_of_element_located((By.XPATH,xpath)),name,'T')
                
            except:
                print("\'" + parent.user_id + "\':", "Loading Update Page Failed:", sys.exc_info()[0:2] + '\n Refresh')
                pass 

        def reload_page():
            driver.refresh()
            # same with 'robot.py' (1.Switch to blackboard iframe & 2.go to course content)
            
            # 1.Switch to iframe of Blackboard 
            for i in range(0,parent.RETRY_TIMES):
                try:
                    driver.switch_to.frame("classic-learn-iframe")
                    print("\'" + parent.user_id + "\':", "Switch to iframe of blackboard Success!")
                    break
                except:
                    try_string = " Trying again..." if (i < (parent.RETRY_TIMES-1)) else "Stop trying..."
                    print("\'" + parent.user_id + "\':", "Fail to switch to iframe of blackboard.", try_string, "(" + str(i+1) + ")")
                    time.sleep(parent.WAIT_TIME_NORMAL)
                    continue
            # 2.go to course content
            try:
                driver.find_element_by_xpath("//div[@id='courseMenuPalette']//span[@title='Content']").click()
            except:
                print("\'" + parent.user_id + "\':", "Find Course Content Failed:", sys.exc_info()[0:2])
                pass
            time.sleep(parent.WAIT_TIME_NORMAL)

            load_page()

        
        # multiple submission
        load_page()

        while count < self.submit_config["NUMBER_OF_SUBMISSION"]: 
            count += 1

            print("\'" + parent.user_id + "\':", "Filling Assignment Form Start:", count)

            # check if the page loads correctly
            try:
                xpath = "//div[@id='mainTop']//form[@name='submitAssignmentForm']"
                wait.until(EC.presence_of_element_located((By.XPATH,xpath)))
            except:
                print("\'" + parent.user_id + "\':", "Submission Page doesn't Load Correctly")
                reload_page()
                # driver.save_screenshot(str(that.user_id) + '_' + str(count)+'.png')
                pass

            # check if the selector exist 
            try:
                xpath = "//select[@name='cusisCourseIds']"
                wait.until(EC.presence_of_element_located((By.XPATH,xpath)))
            except:
                print("\'" + parent.user_id + "\':", "Cannot find course selector ")
                reload_page()
                continue

            # select course
            try:
                # xpath = "//select[@name='cusisCourseIds']/option[@label='" + self.submit_config["SECTION"]+ "']"
                xpath = "//select[@name='cusisCourseIds']/option"
                section_list = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
                section_cnt = len(section_list)
                # randomly pick a section
                section_index = randint(1, section_cnt - 1)
                elem = section_list[section_index]
                print("\'" + parent.user_id + "\':", "Selected Course Section:", elem.text)
                elem.click()
            except:
                print("\'" + parent.user_id + "\':", "Find Cusis Course ID Select Box Failed:", sys.exc_info()[1])
                # refresh and start the new round
                reload_page()
                continue

            # time.sleep(self.submit_config["SLEEP_TIME"])

            # select assignment marker 
            try:
                if self.submit_config["MARKER"] == '':
                    xpath = "//select[@name='selectedAssignmentMarkers']/option"
                    marker_list = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
                    marker_cnt = len(section_list)
                    # randomly pick a marker
                    marker_index = randint(1, marker_cnt - 1)
                    elem = marker_list[marker_index]
                else:
                    xpath = "//select[@name='selectedAssignmentMarkers']/option[@value='" + self.submit_config["MARKER"] + "']"
                    elem = driver.find_element_by_xpath(xpath)
                print("\'" + parent.user_id + "\':", "Selected Marker:", elem.text)
                elem.click()
            except:
                print("\'" + parent.user_id + "\':", "Find Assignment Marker Select Box Failed:", sys.exc_info()[0:2])
                reload_page()
                continue

            # time.sleep(self.submit_config["SLEEP_TIME"])

            # select assignment file
            try:
                elem = driver.find_element_by_xpath("//input[@id='assignmentFile']")
                elem.send_keys(parent.ASSIGNMENT_PATH)
            except:
                print("\'" + parent.user_id + "\':", "Find Assignment Upload Input Failed:", sys.exc_info()[0:2])
                continue
            time.sleep(self.submit_config["SLEEP_TIME"])

            # select group if it is group assignment
            try:
                elem = driver.find_element_by_xpath("//select[@name='studentElgibleGroups']")
                if elem.is_enabled():
                    # load group csv to find his group
                    with open(self.GROUP_CSV_PATH, newline='') as csvfile:
                        rows = csv.reader(csvfile)

                        # use for loop to find user group:
                        # for row in rows:
                        #     if not row[0] == 'No.':
                        #         if row[1] == parent.user_id:
                        #             self.group = row[5:]
                        #             break

                        # use index to find user group (faster):
                        rows_list = list(csv.reader(csvfile))
                        user_index = int(parent.user_id) - 1000000000
                        self.group = rows_list[user_index][5:]

                        # Remove empty string element in list
                        self.group = list(filter(None, self.group))
                    try:
                        submit_group_index = count % len(self.group) - 1
                        driver.find_element_by_xpath("//select[@name='studentElgibleGroups']/option[@label='" + self.group[submit_group_index] + "']").click()
                        time.sleep(self.submit_config["SLEEP_TIME"] + 2)
                    except:
                        print("\'" + parent.user_id + "\':", "Find Group Option Element Failed:", sys.exc_info()[0:2])
            except:
                print("\'" + parent.user_id + "\':", "Find Group Select Element Failed:", sys.exc_info()[0:2])
                continue
            # time.sleep(self.submit_config["SLEEP_TIME"])

            # Say I am ready to submit
            try:
                parent.totalAndUnreadyUsers[1] -= 1
                print("\'" + parent.user_id + "\':", "I'm Ready. Unready Users Left:", parent.totalAndUnreadyUsers[1], "| Let's Go?:", parent.allReady)
            except:
                print("\'" + parent.user_id + "\':", "Access unreadyUsers list Failed:", sys.exc_info()[0:2])
                continue

            # Wait until all users ready
            try:
                while(not parent.allReady[0]):
                    time.sleep(1)
            except:
                print("\'" + parent.user_id + "\':", "Waiting Unready Users Failed:", sys.exc_info()[0:2])
                continue


            # click submit button 
            try:
                elem = driver.find_element_by_xpath("//button[@type='submit']")
                if elem.is_enabled():
                    elem.click()

                else:
                    print("\'" + parent.user_id + "\':", "Submit Button is disabled!")
                    continue

            except:
                print("\'" + parent.user_id + "\':", "Submit Assignment Failed:", sys.exc_info()[0:2])
                reload_page()
                continue

            # wait for the pop up dialog to disappear(server loading)
            try:
                name = self.submit_config['TIMEIT'][1]
                xpath = "//md-dialog//div[@class='row no-padding']"   
                # first appear
                wait.until(EC.visibility_of_element_located((By.XPATH,xpath)))
                # then disappear
                mywait(self,EC.invisibility_of_element_located((By.XPATH,xpath)),name,'T')
            except:
                print("\'" + parent.user_id + "\':", "Wait for Submit Assignment Failed:", sys.exc_info()[0:2], ", Passing...")
                pass

            # print submission message & click OK 
            try:
                submit_msg = wait.until(EC.presence_of_element_located((By.XPATH, "//md-dialog[@role='alertdialog']//h2"))).text
                submit_msg_description = wait.until(EC.presence_of_element_located((By.XPATH, "//md-dialog[@role='alertdialog']//p"))).text
                print("\'" + parent.user_id + "\':", submit_msg, ": (" + submit_msg_description + ")")
                
                xpath = "//md-dialog[@role='alertdialog']//button"
                element = wait.until(EC.element_to_be_clickable((By.XPATH,xpath)))
                element.click()
                print("\'" + parent.user_id + "\':", "Submit Assignment Success:", count)
            except:
                print("\'" + parent.user_id + "\':", "Find \'md-dialog OK button\' or \'md-dialog message\' Failed:", sys.exc_info()[0:2], ", Passing...")
                pass
            time.sleep(self.submit_config["SLEEP_TIME"])

        # # calculate the min, max, avg in the log['results']
        # for task in self.log['results']:
        #     self.log['stat'][task]['min'] = min(self.log['results'][task])
        #     self.log['stat'][task]['max'] = max(self.log['results'][task])
        #     self.log['stat'][task]['avg'] = sum(self.log['results'][task]) / float(len(self.log['results'][task]))

        # # delete the detail records for submission
        # del self.log['results']

        # # write the results under path:'/test_results/<TEST_CASE>.txt'
        # file = open('log/test_results/' + parent.TEST_CASE + '.txt', 'a+')
        # file.write("\n")
        # file.write(json.dumps(self.log, indent=4))
        # file.close()

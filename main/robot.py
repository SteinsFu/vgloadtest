import os
import runpy
import sys
import time
import configparser
from config.task_config import tasks
import student
import instructor
import multiprocessing as mp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

class Robot:

    def end_test(self):
        time.sleep(self.WAIT_TIME_QUIT)
        self.driver.quit()

    def test_case_1(self, config):
        driver = self.driver
        wait = self.wait
        driver.get('https://cuhk-learntest2.blackboard.com/?new_loc=%2Fultra#')

        try:
            xpath = "//div[@id='content']//button[@id='agree_button']"
            wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            driver.find_element_by_xpath(xpath).click()
            print("\'" + self.user_id + "\':", "Accepted terms")
        except:
            print("\'" + self.user_id + "\':", "Find \'Privacy, cookies and terms of use\' Failed:", sys.exc_info()[0:2])
            pass

        try:
            elem = driver.find_element_by_name("user_id")
            elem.send_keys(self.user_id)
            try:
                elem = driver.find_element_by_name("password")
                elem.send_keys(self.password)
                elem.send_keys(Keys.RETURN)
            except:
                print("\'" + self.user_id + "\':", "Input Password Failed:", sys.exc_info()[0:2])
                driver.quit()
        except:
            print("\'" + self.user_id + "\':", "Input Username Failed:", sys.exc_info()[0:2])
            driver.quit()
        # self.assertIn("Stream", driver.title)
        print("\'" + self.user_id + "\':", "Login Success!")
        time.sleep(self.WAIT_TIME_NORMAL)

        # Directly go to 'https://cuhk-learntest2.blackboard.com/ultra/courses/<couse_id>/cl/outline' after login
        for i in range(0, self.RETRY_TIMES):
            try:
                driver.get('https://cuhk-learntest2.blackboard.com/ultra/courses/' + self.course + '/cl/outline')
                print("\'" + self.user_id + "\':", "Go to Course", self.course, "Page Success")
                break
            except:
                print("\'" + self.user_id + "\':", "Go to Course", self.course, "Page Failed:", sys.exc_info()[0:2])
                continue
        
        time.sleep(self.WAIT_TIME_NORMAL)

        # Switch to iframe of Blackboard
        for i in range(0, self.RETRY_TIMES):
            try:
                driver.switch_to.frame("classic-learn-iframe")
                print("\'" + self.user_id + "\':", "Switch to iframe of blackboard Success!")
                break
            except:
                try_string = " Trying again..." if (i < (self.RETRY_TIMES-1)) else "Stop trying..."
                print("\'" + self.user_id + "\':", "Fail to switch to iframe of blackboard.", try_string, "(" + str(i+1) + ")")
                time.sleep(self.WAIT_TIME_NORMAL)
                continue

        # go to course content
        try:
            driver.find_element_by_xpath("//div[@id='courseMenuPalette']//span[@title='Content']").click()
        except:
            print("\'" + self.user_id + "\':", "Find Course Content Failed:", sys.exc_info()[0:2])
            pass
        time.sleep(self.WAIT_TIME_NORMAL)

       # customized actions
        if self.user_id[0] != 'T':
            # student action
            try:
                st = student.Student(self, tasks[self.task], config)
            except:
                print("\'" + self.user_id + "\':", "Student Task:", sys.exc_info())
                pass
        else:
            # instructor actions
            try:
                inst = instructor.Instructor(self,tasks[self.task])

            except:
                print("\'" + self.user_id + "\':", "Instructor Task:", sys.exc_info()[0:2])
                pass
        
        self.end_test()


    def launch(self, args, task, totalAndUnreadyUsers, allReady):
        config = configparser.ConfigParser()
        config.read('main/config/config.ini')

        self.totalAndUnreadyUsers = totalAndUnreadyUsers
        self.allReady = allReady
        self.WAIT_TIME_NORMAL = float(config['DEFAULT']['WAIT_TIME_BETWEEN_NORMAL_PROCESSES'])
        self.WAIT_TIME_IFRAME = float(config['DEFAULT']['WAIT_TIME_LOAD_IFRAME'])
        self.WAIT_TIME_QUIT = float(config['DEFAULT']['WAIT_TIME_BEFORE_CLOSING_BROWSER'])
        self.WAIT_TIME_REFRESH = float(config['DEFAULT']['WAIT_TIME_REFRESH'])
        self.READY_THRESHOLD = float(config['DEFAULT']['READY_THRESHOLD'])
        self.CHROMEDRIVER_PATH = config['DEFAULT']['CHROMEDRIVER_PATH']
        self.ASSIGNMENT_PATH = config['DEFAULT']['SUBMIT_ASSIGNMENT_PATH']
        self.TEST_CASE = config['DEFAULT']['TEST_CASE']
        self.RETRY_TIMES = int(config['DEFAULT']['RETRY_TIMES'])
        self.user_id = "unknown"
        self.password = "unknown"
        self.task = "unknown"

        args.append(''+task)

        try:

            print(args)

            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument("--disable-setuid-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            if (not config['DEFAULT']['SHOW_BROWSER']):
                options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=options, executable_path=self.CHROMEDRIVER_PATH)
            self.driver.set_window_size(1280, 960)
            self.wait = WebDriverWait(self.driver, 10)

            self.user_id = args[1]
            self.password = args[2]
            self.computing_id = args[3]
            self.bb_user_role = args[4]
            self.user_account_type = args[5]
            self.course = args[6]
            self.task = args[7]
            
            self.test_case_1(config)

        except:
            print("\'" + args[1] + "\' Robot Setup failed:", sys.exc_info())
            pass
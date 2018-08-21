import sys
import unittest
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


config = configparser.ConfigParser()
config.read('main/config/config.ini')

class UserTest(unittest.TestCase):
    WAIT_TIME_NORMAL = float(config['DEFAULT']['WAIT_TIME_BETWEEN_NORMAL_PROCESSES'])
    WAIT_TIME_IFRAME = float(config['DEFAULT']['WAIT_TIME_LOAD_IFRAME'])
    WAIT_TIME_QUIT = float(config['DEFAULT']['WAIT_TIME_BEFORE_CLOSING_BROWSER'])
    WAIT_TIME_REFRESH = float(config['DEFAULT']['WAIT_TIME_REFRESH'])
    READY_THRESHOLD = float(config['DEFAULT']['READY_THRESHOLD'])
    ASSIGNMENT_PATH = config['DEFAULT']['SUBMIT_ASSIGNMENT_PATH']
    TEST_CASE = config['DEFAULT']['TEST_CASE']
    user_id = "unknown"
    password = "unknown"
    task = "unknown"

    def setUp(self):
        options = Options()
        options.add_argument('--no-sandbox')
        if (not config['DEFAULT']['SHOW_BROWSER']):
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1280, 960)
        self.wait = WebDriverWait(self.driver, 10)

        arg_list = sys.argv[1:]
        self.user_id = arg_list[0]
        self.password = arg_list[1]
        self.computing_id = arg_list[2]
        self.bb_user_role = arg_list[3]
        self.user_account_type = arg_list[4]
        # self.sections = arg_list[5:10]
        self.course = arg_list[5]
        self.task = arg_list[6]
        with open("totalUsers.txt", "r") as totalUsers_file:
            self.totalUsers = int(totalUsers_file.readline())
        # print(self.user_id + " " + self.password + " " + self.computing_id + " " + self.bb_user_role + " " +
        #       self.user_account_type, self.sections, self.task)
      

    def test_case_1(self):
        driver = self.driver
        wait = self.wait
        driver.get('https://cuhk-learntest2.blackboard.com/?new_loc=%2Fultra#')
        self.assertIn("Blackboard", driver.title)

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
        retry = True
        while retry:
            try:
                driver.get('https://cuhk-learntest2.blackboard.com/ultra/courses/' + self.course + '/cl/outline')
                print("\'" + self.user_id + "\':", "Go to Course", self.course, "Page Success")
                retry = False
            except:
                print("\'" + self.user_id + "\':", "Go to Course", self.course, "Page Failed:", sys.exc_info()[0:2])
                pass
        
        time.sleep(self.WAIT_TIME_NORMAL)

        # # Manually:
        # # go to courses
        # try:
        #     driver.find_element_by_xpath("//a[@href='https://cuhk-learntest2.blackboard.com/ultra/course']").click()
        # except:
        #     print("\'" + self.user_id + "\':", "Find Courses Page Failed:", sys.exc_info()[0:2])
        #     pass
        # time.sleep(self.WAIT_TIME_NORMAL)
        #
        # # go to 2016R1-NURS1151: Nursing 2016 test
        # try:
        #     driver.find_element_by_xpath("//a[contains(text(), 'NURS1151: Nursing 2016 test')]").click()
        # except:
        #     print("\'" + self.user_id + "\':", "Find Course NURS1151 Failed:", sys.exc_info()[0:2])
        #     pass
        # time.sleep(self.WAIT_TIME_NORMAL)

        # Switch to iframe of Blackboard (try 5 times)
        try_times = 5
        for i in range(0,try_times):
            try:
                driver.switch_to.frame("classic-learn-iframe")
                print("\'" + self.user_id + "\':", "Switch to iframe of blackboard Success!")
                break
            except:
                try_string = " Trying again..." if (i < (try_times-1)) else "Stop trying..."
                print("\'" + self.user_id + "\':", "Fail to switch to iframe of blackboard.", try_string)
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

    def tearDown(self):
        time.sleep(self.WAIT_TIME_QUIT)
        self.driver.quit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
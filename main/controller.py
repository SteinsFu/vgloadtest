import robot
import time 
import csv
import configparser
import template
import sys
import json
from config.testcase_config import cases
from config.task_config import tasks
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
config = configparser.ConfigParser()
config.read('main/config/config.ini')

class MassControl:

    def __init__(self, start_student):
        # next available student or instructor, in the form ['next_student','next_instructor']
        self.next_to_use = [start_student,1]
        
        # set the data path 
        self.STUDENT_CSV_PATH = config['DEFAULT']['STUDENT_CSV_PATH']
        self.INSTRUCTOR_CSV_PATH = config['DEFAULT']['INSTRUCTOR_CSV_PATH']

        # set the test case 
        self.TEST_CASE = config['DEFAULT']['TEST_CASE']
        self.WAIT_TIME_SPAWN_TEST = float(config['DEFAULT']['WAIT_TIME_BETWEEN_SPAWNING_EACH_TEST'])



    def do_test_case(self, config, executor):
        # Create a file to let all threads keep check on the no. of unreadyUsers
        with open("unreadyUsers.txt","w") as unreadyUsers_file:
            unreadyUsers_file.write(str(config['COPY']))
        # Create a file to store the totle no. of users
        with open("totalUsers.txt", "w") as totalUsers_file:
            totalUsers_file.write(str(config['COPY']))

        # number of copy
        cnt = 0
        # number of the starting place 
        start = 0
        path = ""
        # choose the data path 
        if config['ROLE'] == 'S':
            self.role = 0
            path = self.STUDENT_CSV_PATH
        else:
            self.role = 1
            path = self.INSTRUCTOR_CSV_PATH

        with open(path, newline='') as csvfile:
                rows = csv.reader(csvfile)
                for row in rows: 
                    # pass the row until the next available one 
                    if (start < self.next_to_use[self.role]): 
                        start += 1
                        continue
                    if (cnt >= config["COPY"]): break
                    if (row[0] != 'No.'):
                        cnt += 1
                        executor.submit(robot.launch, row, config['TASK'])
                        time.sleep(self.WAIT_TIME_SPAWN_TEST)

                self.next_to_use[self.role] += cnt

    def test(self):
        # count the total number of thread/process 
        self.TOTAL_NUMBER = 0
        for case in cases[self.TEST_CASE]:
            self.TOTAL_NUMBER += case['COPY']
        
        # create a new txt file under '/test_results'
        self.file = open('log/test_results/'+ self.TEST_CASE +'.txt','w+')
        self.file.close()
        
        # use ThreadPoolExecutor for multithread and ProcessPoolExecutor for multiprocess
        with ThreadPoolExecutor(self.TOTAL_NUMBER) as executor:
            for case in cases[self.TEST_CASE]:
                
                # save task information 
                self.file = open('log/test_results/'+ self.TEST_CASE +'.txt','a+')
                self.file.write('ROLE: ' + case['ROLE'] + ' COPY: ' + str(case['COPY']) + ' TASK: ' + case['TASK'] + '\n    ')
                self.file.write(json.dumps(tasks[case['TASK']]))
                self.file.write('\n')
                self.file.close()

                # for each group (eg. group with COPY=20) to do the task
                self.do_test_case(case, executor)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        start_student = int(sys.argv[-1])
    else:
        start_student = 1
    massControl = MassControl(start_student)
    massControl.test()
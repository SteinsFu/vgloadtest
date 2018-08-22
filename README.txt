Testing Environemnt: Python 3.6.5 64-bit

# Overview (compared with previous version)

    -data                           (vg_testing_data.csv)
        instructor_samples.csv
        student_samples.csv
        testing_users.csv
    -log                            
        -test_results
    -main
        -config
            config.ini              (config.ini)
            testcase_config.py
            task_config.py
        controller.py               (mass_test_control.py)
        instructor.py
        measure.py
        robot.py                    (loadtest_slave.py)
        student.python
    chromedriver
    README.text
    uploadfile.txt


# Changelog:
    1.  use 'concurrent.futures' instead of 'multiprocessing' for multiprocess and multithreading 
    2.  seperate the configuration file into 'config/config.ini', 'config/testcase_config.py' and 'config/task_config.py'
        'tasks_config' is for task configuration while 'tasks_config' is for test_case configuration 
    3.  add two classes 'Student' and 'Instructor" with different functionalities
    4.  add 'WebDriverWait' to enable waiting function(e.g. wait for an element to appear)
    5.  add customized wait function 'mywait' with timer
    6.  add logging funtion to save the time results and calculate the statistics


# Setup the environment (reference: http://selenium-python.readthedocs.io/installation.html):
    1.  Downloading Python binding for Selenium
        $ pip install selenium
    2.  Install Drivers for browser: (This program is using chrome for the time being)
        Chrome:	https://sites.google.com/a/chromium.org/chromedriver/downloads
        Edge:	https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
        Firefox:	https://github.com/mozilla/geckodriver/releases
        Safari:	https://webkit.org/blog/6900/webdriver-support-in-safari-10/


# Running the program:
    1.  change the SUBMIT_ASSIGNMENT_PATH in config/config.ini to where the uploadfile locates
    2.  use terminal to go to 'vgloadtest_2' directory
    3.  type the following line:
            $ python3 main/controller.py
            if it fails, try:
            $ python main/controller.py
    4.  the results will be created in 'log/test_results' as text file

# WorkFlow:
    1.  controller.py start parallel process:
        a.  it loads the test case configuration from 'config/testcase_config.py'
        b.  for each group in the configuration, it will create several copies to do the same task 
        c.  for a single copy, it will pass the user_name, password, task to the executor to process 
    2.  the executor will call 'robot.lauch' in 'main/robot.py', which then invokes the unit test in 'main/template.py'
    3.  'test_case_1' in 'main/template.py' will first login, and direct to the course page 
    4.  when running into customized actions, it will create a instance of student or instructor accordingly:
        a. during initialization, the instance will read the task configuration from 'config/task_config.py' for a given task 
        b. process the task funtion(has repitition inside)
        c. write the results into text file under 'log/test_results'


# To add and run new test case:
    1.  create a test case in 'testcase_config.py' as array of dictionary. Each dictionary is a group performing the same task.
        A group should contains ROLE('S'/'T'), COPY(number of copy), and TASK(registered in tasks_config) 
    2.  change the TEST_CASE in config.ini to the new test case name 
    3.  run the main function of 'main/controller.py'


# To adjust a task:
    1.  change the configuration values of the task in 'config/task_config' help you to modify the task 


# To add a new task:
    1.  choose the class that will perform the task(student/instructor)
    2.  create new <task> method and corresponding set_<task>_config method in corresponding class 
        the task_method should be designed as the tempalte with arguments read from task_config 
    3.  create a new task in tasks_config with the customized parameters 


    





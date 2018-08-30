Testing Environemnt: Python 3.6.5 64-bit

# Overview 

    -data                           
        instructor_samples.csv
        student_samples.csv
        testing_users.csv
    -log                            
        -test_results
    -main
        -config
            config.ini              
            testcase_config.py
            task_config.py
        controller.py               
        instructor.py
        measure.py
        robot.py                    
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


####### Please See "Setup Docker/VM Environment (ubuntu)" #########
# Setup the environment (reference: http://selenium-python.readthedocs.io/installation.html):
    1.  Downloading Python binding for Selenium
        $ pip install selenium
    2.  Install Drivers for browser: (This program is using chrome for the time being)
        Chrome:	 https://sites.google.com/a/chromium.org/chromedriver/downloads
        Edge:	 https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
        Firefox: https://github.com/mozilla/geckodriver/releases
        Safari:	 https://webkit.org/blog/6900/webdriver-support-in-safari-10/
####### Chromedriver is located in the folder already     #########
####### No need to install manually                       #########
####### Please See "Setup Docker/VM Environment (ubuntu)" #########

# Running the program:
    1.  change the SUBMIT_ASSIGNMENT_PATH and CHROMEDRIVER_PATH in config/config.ini to where the uploadfile locates
    2.  use terminal to go to 'vgloadtest_uat' directory
    3.  type the following line:
            $ python3 main/controller.py
            if it fails, try:
            $ python main/controller.py
		or
	    $ python3 main/controller.py <Start_Student_arg>
	eg. $ python3 main/controller.py 51		<-- start testing 1000000051, 1000000052 ... , 1000000100 (When COPY = 50)
    4.  the results will be created in 'log/test_results' as text file (commented those lines)

# WorkFlow:
    1.  controller.py start parallel process:
        a.  it loads the test case configuration from 'config/testcase_config.py'
        b.  for each group in the configuration, it will create several copies to do the same task 
        c.  for a single copy, it will pass the user_name, password, task to the executor to process 
    2.  the executor will call 'robot.lauch' in 'main/robot.py'
    3.  'test_case_1' in 'main/robot.py' will first login, and direct to the course page 
    4.  when running into customized actions, it will create a instance of student or instructor accordingly:
        a. during initialization, the instance will read the task configuration from 'config/task_config.py' for a given task 
        b. process the task funtion(has repitition inside)
        c. write the results into text file under 'log/test_results'

Flow Graph:

	      controller.py				...
	           |
		robot.py				...
		   |
	|----------|-----------|------ ...  or  ---|--------------|--------- ...
	|	   |	       |                   |              |
    student.py  student.py  student.py ...     instructor.py  instructor.py ...


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


# Setup Docker/VM Environment (ubuntu) to run:
    # start docker service:
    > $ service docker start
    # start a ubuntu docker container:
    > $ docker run -it ubuntu

    # inside ubuntu:
	
	# install python3:
	> ubuntu$ apt-get update && apt-get install -y python3-pip python3-dev && cd /usr/local/bin && ln -s /usr/bin/python3 python && pip3 install --upgrade pip
	
	# install selenium 3.13.0:
	> ubuntu$ pip install selenium==3.13.0

	# install related library:
	> ubuntu$ apt-get install libnss3-dev

	# install chrome:
	> ubuntu$ apt-get install wget
	> ubuntu$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
	> ubuntu$ dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

	# Go to vgloadtest_uat directory and run the program:
	> ubuntu$ cd vgloadtest_uat
	> ubuntu$ python main/controller.py

# To start docker container:
    $ service docker start
    $ docker ps -a		(to check container ID)
    $ docker start -a -i <container_ID>
    
# To create a docker ubuntu container:
    $ docker run -it ubuntu



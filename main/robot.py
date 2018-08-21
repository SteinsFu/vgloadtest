import os
import runpy
import sys
import template

def launch(data_row, task):
    args = data_row
    args.append(''+task)

    # print("\'Robot Running\': python3 main/template.py", args[1], args[2], args[3], args[4], "\'"+args[5]+"\'", args[6],
    #       args[7], args[8], args[9], args[10], args[11])
    print("\'Robot Running\': python3 main/template.py", args[1], args[2], args[3], args[4], "\'"+args[5]+"\'", args[6])

    # parse section name to string
    # for i in range(6,11):
    #     args[i] = "\'" + args[i] + "\'"

    try:
        # use os to launch:
        # os.system("python3 main/template.py " + args[1] + " " + args[2] + " " + args[3] + " " + args[4]
        #           + " " + "\'"+args[5]+"\'" + " " + args[6] + " " + args[7] + " " + args[8] + " " + args[9]
        #           + " " + args[10] + " " + args[11])

        # use runpy to launch:
        sys.argv = args
        runpy.run_path("main/template.py", run_name='__main__')
    except:
        print("\'" + args[1] + "\' Robot launch template failed:", sys.exc_info()[0:2])
        pass
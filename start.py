from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import sys
from con_abtTerminal import AbtTerminal
import os
import threading
app=QApplication(sys.argv)
window=AbtTerminal()

import threading
from threading import Thread



th_list=[]
import subprocess
def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')

class full_thread_buffer():
    def __init__(self):
        self.p = None
    def run_command(self,command):
        self.p = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        return iter(self.p.stdout.readline, b'')

    def to_thread_cmd_buffer(self,command, text_controller):
        print(command[2:])
        command = command[2:].split()
        for line in self.run_command(command):
            text_controller.append(str(line)[2:len(line)])
            print(str(line)[2:len(line)])  # when we use len of line we remove \t\r automaticly

    def stop(self):
        self.p.terminate()
        self.process = None




cBuffer=full_thread_buffer()
def to_thread_cmd_buffer(command,text_controller):
    print(command[2:])
    command = command[2:].split()
    for line in run_command(command):
        text_controller.append(str(line)[2:len(line)])
        print(str(line)[2:len(line)])  # when we use len of line we remove \t\r automaticly


def my_commands_ana(command,dbname,text_controller):
    command=command.replace("\n","")
    save_index=command.lower().find("$save")
    file_path=None
    "حتى إذا لم نقم [غرجاع المسار فسعتبره البرنامج None"
    if save_index !=-1:
        file_path=command[save_index+6:]
        command=command[:save_index]
    if command == "cd":
        # return str(os.path.dirname(os.path.realpath(__file__))) # current file Directory
        return os.getcwd(),file_path,None,None
    elif "cd" in command[:2] and len(command) > 2:
        dir_name = command[3:]
        try:
            # we can also return the pure text
            os.chdir(dir_name)
            return '<h4>dir changed to</h4> <h4 style="color:rgb(0,230,120);">%s</h4>' % os.getcwd(),file_path,os.getcwd(),None
        except:
            return '<h4 style="color:red">Cant change current Directory To \n\t%s</h4>' % dir_name,file_path,dir_name,None
    elif "$$" in command[:2]:
        # t=threading.Thread(target=lambda :to_thread_cmd_buffer(command,text_controller))
        # t.start()
        t=threading.Thread(target=lambda :cBuffer.to_thread_cmd_buffer(command,text_controller))
        t.start()
        cBuffer.stop()
        pass
        # print(command[2:])
        # command = command[2:].split()
        # for line in run_command(command):
        #     text_controller.append(str(line)[2:len(line)])
        #     print(str(line)[2:len(line)])  # when we use len of line we remove \t\r automaticly

            # stream=os.popen(command[2:])
        # stre=stream.read()
        # print(stre)
        # return stre,file_path,None

    # $ml as text asdasdasdasd
    #
    elif "$ml" in command[:3]:
        if "as text" in command[3:11]:
            msg = QMessageBox(window)
            msg.setIcon(QMessageBox.Information)

            msg.setText(command[12:])
            msg.setInformativeText("Press Show Details To"
                                   "\nShow plain text code")
            msg.setWindowTitle("Plain Text")
            msg.setDetailedText(command[12:])
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()
            return " Viewed ",file_path,None,None
        return "",file_path
    elif "$ev" in command[:3]:
        try:
            ev_res=eval(command[4:])
            return '<h3 style="color:green;">%s</h3>'%str(ev_res),file_path,str(ev_res),None
        except:
            return '<h3 style="color:red">Check Your Expression</h3> ',file_path,None
    elif dbname=="$ev":
        try:
            ev_result=str(eval(command))
            return '<h3 style="color:green">%s</h3>'%ev_result,file_path,ev_result,None
        except:
            return '<h3 style="color:red">Check Your Expression</h3> ',file_path,None,None
    else:
        return '<h3 style="color:rgb(240,10,60)">THERE::IS::AN::ERROR</h3>',file_path,None,None



window.Command_Analyser=my_commands_ana
window.show()
exit(app.exec_())

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import re
import os
import logging
from abtTerminalUI import Ui_Form
"""
يمكن استخدام هذا الكلاس كملح لبرنامج ءاخر
وذلك كالتالي
أولا وهي الطريقة التي تعطيك تحكم كامل وهي بالتعديل في هذا الملف أساسا
والطريقة الثانية هي بعمل
كائن من هذا الكلاس
وإضافته ل widget or MainWindow
وبعد ذلك يتم تنفيذ الامر التالي

object.Command_Analyser=Your_Command_Analyser_Function
def Your_Command_Analyser_Function(self,command)
    do sum stuff
    return string يجب ان نرجع قيمة نصية

"""


class AbtTerminal(QWidget,Ui_Form):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        "اسم الموجه الحالي"
        self.dataname="Abt"
        # self.cmd_cleare_state = False
        self.temp_key_event = self.te_sql_cmd.keyPressEvent
        self.te_sql_cmd.keyPressEvent = self.key_command_controller
        self.cmd_slider_speed = 25
        self.te_sql_cmd.installEventFilter(self)
        self.te_sql_cmd.append(self.dataname+">>>")
        # self.te_sql_cmd.setDisabled(True)

        self.cmd_last_text_document=self.te_sql_cmd.document()
        self.cmd_last_html_text=self.te_sql_cmd.toHtml()

        self.cmd_last_text=self.cmd_last_text_document.toPlainText()
        self.cmd_len=len(self.cmd_last_text)
        "Advanced Controller But Heavy deb_char_cont_x9875"
        # self.te_sql_cmd.textChanged.connect(self.watch_edit_text)#dep_char_cont_x9875

        self.w_ex_cmd.mouseDoubleClickEvent=self.mod_mouse_dc_event
        self.w_ex_cmd.mousePressEvent=self.mod_mouse_pres_even
        self.w_ex_cmd.mouseReleaseEvent=self.mod_mouse_release_event

        self.te_sql_cmd.wheelEvent=self.whell_eventer_cmd
        self.cur_font_size=9
        # self.te_sql_cmd.keyPressEvent=self.cmd_key_eventer

        self.full_commands_list=[]
        self.full_cmd_list_cursore=-1

        self.put_execute.clicked.connect(self.do_query_from_user)
        self.current_thread=[]

    def key_command_controller(self, kv=QKeyEvent):
        # QTextCursor.setPosition()
        if self.te_sql_cmd.textCursor().position() < self.cmd_len:
            if kv.key() == Qt.Key_Up or kv.key() == Qt.Key_Down or kv.key() == Qt.Key_Right or kv.key() == Qt.Key_Left \
                    or kv.key() == Qt.Key_PageUp or kv.key() == Qt.Key_PageDown or kv.key() == Qt.Key_Home or kv.key() == Qt.Key_End\
                    or kv.key()==Qt.Key_Control:
                pass
            else:
                self.te_sql_cmd.textCursor().setPosition(self.cmd_len)
                return
        logging.info(kv.key())  # BackSpace 16777219
        if len(self.te_sql_cmd.toPlainText()) == self.cmd_len or \
                        self.te_sql_cmd.toPlainText().find(self.cmd_last_text) != 0:
            if kv.key() == 16777219:
                return
            elif kv.key() == 16777235:  # up
                try:
                    cur_len_delta = len(self.te_sql_cmd.toPlainText()) - self.cmd_len
                    logging.info("Len : %d" % cur_len_delta)
                    self.te_sql_cmd.keyPressEvent = self.temp_key_event
                    temp_clear = QKeyEvent()
                    temp_clear.key = Qt.Key_Backspace
                    for a in range(0, cur_len_delta):
                        self.te_sql_cmd.keyPressEvent(temp_clear)
                    self.te_sql_cmd.keyPressEvent = self.key_command_controller
                    self.te_sql_cmd.append(self.full_commands_list[self.full_cmd_list_cursore])
                    self.full_cmd_list_cursore -= 1
                except:
                    pass
            elif kv.key() == 16777237:  # down
                try:
                    cur_len_delta = len(self.te_sql_cmd.toPlainText()) - self.cmd_len
                    self.te_sql_cmd.keyPressEvent = self.temp_key_event
                    temp_clear = QKeyEvent()
                    temp_clear.key = Qt.Key_Backspace
                    for a in range(0, cur_len_delta):
                        self.te_sql_cmd.keyPressEvent(temp_clear)
                    self.te_sql_cmd.keyPressEvent = self.key_command_controller
                    self.te_sql_cmd.append(self.full_commands_list[self.full_cmd_list_cursore])
                    self.full_cmd_list_cursore += 1
                except:
                    pass

        self.te_sql_cmd.keyPressEvent = self.temp_key_event
        self.te_sql_cmd.keyPressEvent(kv)
        self.te_sql_cmd.keyPressEvent = self.key_command_controller

    def whell_eventer_cmd(self, whel=QWheelEvent):
        print(whel.delta())
        font = QFont()
        "لابد من إعادة تفعيل الحركة العلوية والسفلية "
        "أي الحركة إذا كانت هناك كتابات كثيرة"
        "أي الحركة الخاصة بالمسطرة الجانبية"
        te = QScrollBar()
        te.setSliderPosition(te.sliderPosition() - 1)

        vert_sc = self.te_sql_cmd.verticalScrollBar()

        if self.handleButton() == "Shift":
            try:
                cur_len_delta = len(self.te_sql_cmd.toPlainText()) - self.cmd_len
                logging.info("Len : %d" % cur_len_delta)
                logging.info(" Cureernt_index_fclc %s" % self.full_cmd_list_cursore)
                for a in range(0, cur_len_delta):
                    self.te_sql_cmd.textCursor().deletePreviousChar()
                # self.te_sql_cmd.append(self.full_commands_list[self.full_cmd_list_cursore])
                self.te_sql_cmd.append(str(self.full_commands_list[self.full_cmd_list_cursore]))

            except:
                pass
            if whel.delta() / 120 == 1 and self.full_cmd_list_cursore != -len(self.full_commands_list):
                self.full_cmd_list_cursore -= 1
            elif whel.delta() / 120 == -1 and self.full_cmd_list_cursore != len(self.full_commands_list) - 1:
                self.full_cmd_list_cursore += 1
            return

        if self.handleButton() == 'Control':
            # self.current_thread.stop()
            if whel.delta() / 120 == 1:
                self.cur_font_size += 0.5
                if self.cur_font_size > 40:
                    self.cur_font_size -= 0.5
            else:
                self.cur_font_size -= 0.5
                if self.cur_font_size < 6:
                    self.cur_font_size += 0.5
            logging.info(self.cur_font_size)
            logging.info("Before Changing")
            font.setPointSize(self.cur_font_size)
            self.te_sql_cmd.setFont(font)
            return
        else:
            if whel.delta() / 120 == 1:
                vert_sc.setSliderPosition(vert_sc.sliderPosition() - self.cmd_slider_speed)
            else:
                vert_sc.setSliderPosition(vert_sc.sliderPosition() + self.cmd_slider_speed)

    def handleButton(self):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:
            return 'Shift'
        elif modifiers == Qt.ControlModifier:
            return 'Control'
        elif modifiers == (Qt.ControlModifier |
                               Qt.ShiftModifier):
            return 'Control+Shift'
        elif modifiers == Qt.Key_Enter | Qt.Key_Shift:
            logging.info("Shift+Enter Full")
        else:
            return 'Click'

    def mod_mouse_release_event(self, QMouseEvent):
        logging.info("Mouse Released")
        self.w_ex_cmd.setStyleSheet("background-color: rgb(255,165,0);")

    def mod_mouse_pres_even(self, QMouseEvent):
        logging.info("mouse Pressed")
        self.w_ex_cmd.setStyleSheet("background-color: rgb(255, 125, 0);")
        self.do_query_from_user()

    def mod_mouse_dc_event(self, QMouseEvent):
        logging.info("double clicked")

    def nothing_else__(self):
        logging.info("nothing_else__")

    def my_commands_(self, commands):
        commands__ = commands.replace("\n", "")
        logging.info("commands__ : %s" % commands__)
        if commands__.lower() == "$clear".lower():
            # self.te_sql_cmd.textChanged.disconnect(self.watch_edit_text) #deb_char_cont_x9875
            self.te_sql_cmd.clear()
            self.update_cmd_len()  # co_deb_char_cont_x9875
            # self.te_sql_cmd.textChanged.connect(self.watch_edit_text) #deb_char_cont_x9875
            # self.update_cmd_len()
            return False
        if commands__.lower() == "$clear temp".lower():
            self.full_commands_list = []
            return
        if commands__.lower() == "$admin":
            self.te_sql_cmd.append('<h3 style="color:darkorange;">Osama Al Banna</h3>')
            self.update_cmd_len()
            return False
        if commands__.lower() == "$exit":
            self.close()
            return False
        if "$ch user" in commands__.lower():
            cur_user=commands__[len("$ch user")+1:]
            self.dataname=cur_user
            print(cur_user)
            self.update_cmd_len()
            return False
        return True

    def do_query_from_user(self):
        ""
        "الجزأ الأاول وفيه يتم الـاكد هل الأمر الذي أدخله المستخدم من الأوامر الخاصة"
        "وهي الأوامر التي ليس  لها أي علاقة بمشروع العمل "
        "كأوامر عرض اسم المستخدم ومسح الشاشة وما الى ذلك"
        " بعد هذا يتم المرور للجزأ الثاني وهو الذي يعالج البيانات على حسب المشروع الذي نعمل عليه"
        current_command = self.te_sql_cmd.toPlainText()[self.cmd_len:]
        self.full_cmd_list_cursore = -1
        if current_command == "":
            self.te_sql_cmd.append('\n'
                                   '<h5 style="color:Blue;">'
                                   'Nothing To Analysis</h5>')
            self.update_cmd_len()
            return
        self.full_commands_list.append(current_command)
        if not self.my_commands_(current_command):
            return
        "الجزأ الثاني"
        final_result = ""
        save_file=""
        result_text=""
        final_result,save_file,result_text,m_thread=self.Command_Analyser(current_command,self.dataname,self.te_sql_cmd)
        self.current_thread=m_thread
        print("After Thread")

        # while query.next():
        #     temp_res = ""
        #     try:
        #         for a in range(0, 100):
        #             if query.value(a) != None:
        #                 temp_res += (str(query.value(a)) + " ")
        #
        #         logging.info(temp_res)
        #         final_result += temp_res + "\n"
        #     except:
        #         pass

        "هنا يتم التحكم في العمليات عن طريق تمرير النواتج"
        "الى المتغيرfinal_result "
        "والذي بدوره سيتم عرضه للمستخدم"
        "يمكن ان يكون في هذا المتغير أي شيء حتى أكواد Html css ..etc"
        "عمليات حسابية أي شيء وهو ناتج ما أدخله المستخدم"
        if final_result == "-t-s-from_cmd_buffer":
            self.update_cmd_len()
            return
        if len(final_result) != 0:
            self.te_sql_cmd.append('\n'
                                   '<h5 style="color:green;">'
                                   'Result:</h5>')
            if save_file != None:
                try:
                    with open(str(save_file),"w") as sf:
                        # final_result=final_result.replace('<h3 style="color:green">',"").replace('</h3>',"")
                        print(result_text)
                        if result_text!=None:
                            final_result=result_text
                        sf.write(final_result)
                        sf.close()
                        self.te_sql_cmd.append('<h6 style="color:rgb(0,240,60);">Saved</h6>')
                        self.update_cmd_len()
                        return
                except :
                    self.te_sql_cmd.append('<h6 style="color:red;">Can\'t save file</h6>')
                    self.te_sql_cmd.append('<h3 style="color:rgb(240,20,60);">Fetched Result From Stream : </h3>')
            self.te_sql_cmd.append(str(final_result))
        else:
            logging.info("failedsss")
            self.te_sql_cmd.append('<h6 style="color:red;">Syntax Error</h6>')
        self.update_cmd_len()

    def spec_update_cmd_len(self):
        self.cmd_last_text_document = self.te_sql_cmd.document()
        self.cmd_last_text = self.cmd_last_text_document.toPlainText()
        self.cmd_len = len(self.cmd_last_text)
        self.cmd_last_html_text = self.te_sql_cmd.toHtml()

    def update_cmd_len(self):
        # self.te_sql_cmd.append("\n%s>>>" % self.dataname)
        self.te_sql_cmd.append("\n%s>>>" % self.dataname)

        self.spec_update_cmd_len()


    def trace_location(self):
        logging.info(str(self.dw_add_dell_container.x()) + " , " + str(self.dw_add_dell_container.y()))

    def Command_Analyser(self,command,db_name,text_controller):
        pass # Leave To User
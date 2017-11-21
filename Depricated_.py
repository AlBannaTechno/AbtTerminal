# ""
# "deb_char_cont_x9875"
# # def watch_edit_text(self):  # execute when test edited
# #     logging.info("TQ : " + str(len(self.te_sql_cmd.toPlainText())))
# #     logging.info("TE : " + str(len(self.cmd_last_text)))
# #     logging.info("LEN : " + str(self.cmd_len))
# #     if len(self.te_sql_cmd.toPlainText()) < self.cmd_len or \
# #                     self.te_sql_cmd.toPlainText().find(self.cmd_last_text) != 0:
# #         # self.te_sql_cmd.setText(self.cmd_last_text) # not writch text
# #
# #         # self.te_sql_cmd.setText(self.cmd_last_text) # Work but no text highLight
# #         # after press backspace
# #         # self.te_sql_cmd.setDocument(self.cmd_last_text_document)
# #
# #         self.te_sql_cmd.setHtml(self.cmd_last_html_text)
# #
# #         logging.info("TQ : " + str(len(self.te_sql_cmd.toPlainText())))
# #         logging.info("TE : " + str(len(self.cmd_last_text)))
# #
# #         tempCurs = self.te_sql_cmd.textCursor()
# #         # tempCurs=QTextCursor()
# #         # tempCurs.movePosition(QTextCursor.Right,QTextCursor.MoveAnchor,len(self.te_sql_cmd.toPlainText()))
# #
# #         tempCurs.movePosition(QTextCursor.End, QTextCursor.MoveAnchor, 0)
# #         self.te_sql_cmd.setTextCursor(tempCurs)
#
#
# #
# # import subprocess
# # proc = subprocess.Popen('cmd.exe', stdin = subprocess.PIPE, stdout = subprocess.PIPE)
# #
#
# app=QApplication(sys.argv)
# window=AbtTerminal()
#
# def my_commands_ana(command):
#     if command == "cd":
#         # return str(os.path.dirname(os.path.realpath(__file__))) # current file Directory
#         return os.getcwd()
#     if "cd" in command[:2] and len(command) > 2:
#         dir_name = command[3:]
#         try:
#             os.chdir(dir_name)
#             return '<h4>dir changed to</h4> <h4 style="color:rgb(0,230,120);">%s</h4>' % os.getcwd()
#         except:
#             return '<h4 style="color:red">Cant change current Directory To \n\t%s</h4>' % dir_name
#     if "$$" in command[:2]:
#         stdout, stderr = proc.communicate(bytes(str(command[2:]), 'UTF-8'))
#         deleted_length_before=len("b'Microsoft Windows [Version 10.0.10586]\r\n(c) 2015 Microsoft Corporation. All rights reserved.\r\n\r\n")
#         deleted_length_after=len(">More? '")
#         # real_result=str(stdout)[deleted_length_before+4:len(str(stdout))-deleted_length_after]
#         real_result=str(stdout.decode("utf-8")).replace("Microsoft Windows [Version 10.0.10586]\r\n(c) 2015 Microsoft Corporation. All rights reserved.\r\n\r\n","")
#         real_result=real_result.replace(">More?","")
#         print(real_result)
#         return real_result
#
#
#
#
#
# ###############
# import subprocess
# cmdline = ["cmd", "/q", "/k", "echo off"]
# cmd = subprocess.Popen(cmdline, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
#
#
# if "$$" in command[:2]:
#     batch = b"""\
#     cd
#     """
#
#     # cmd.stdin.write(bytes(str(command[2:]), 'UTF-8'))
#
#     cmd.stdin.write(batch)
#     cmd.stdin.flush()  # Must include this to ensure data is passed to child process
#     result = cmd.stdout.read()
#     return " "

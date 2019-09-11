#-*-coding:utf-8-*-

from tkinter import *
import datetime
import time
from speech_test import *

root = Tk()
root.title(u'与机器人Mike聊天中')


# 发送按钮事件
def sendmessage():
    # 在聊天内容上方加一行 显示发送人及发送时间


    # if query is not None:
    msgcontent = "我" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n"
    # else:
    #     msgcontent = result
    text_msglist.insert(END, msgcontent, 'green')
    query = text_msglist.get('1.0', END)
    text_msglist.insert(END, text_msglist.get('1.0', END))

    print('query:',query)
    result = main(query)
    text_msglist.delete('0.0', END)
    text_msglist.insert(END, result, 'red')
    text_msglist.insert(END, text_msg.get('1.0', END))
    text_msg.delete('1.0', END)


# 创建几个frame作为容器
frame_left_top = Frame(width=500, height=300, bg='white')
frame_left_center = Frame(width=500, height=30, bg='white')
frame_left_bottom = Frame(width=380, height=20)
frame_right = Frame(width=170, height=400, bg='white')
##创建需要的几个元素
text_msglist = Text(frame_left_top)
text_msg = Text(frame_left_center)
button_sendmsg = Button(frame_left_bottom, text=u'Send', command=sendmessage)
# 创建一个绿色的tag
text_msglist.tag_config('green', foreground='#008B00')
# 使用grid设置各个容器位置
frame_left_top.grid(row=0, column=0, padx=2, pady=5)
frame_left_center.grid(row=1, column=0, padx=2, pady=5)
frame_left_bottom.grid(row=2, column=0)
frame_right.grid(row=0, column=1, rowspan=3, padx=4, pady=5)
frame_left_top.grid_propagate(0)
frame_left_center.grid_propagate(0)
frame_left_bottom.grid_propagate(0)
# 把元素填充进frame
text_msglist.grid()
text_msg.grid()
button_sendmsg.grid(sticky=E)
# 主事件循环
root.mainloop()

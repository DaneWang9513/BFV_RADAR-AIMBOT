# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import os
import win32com.client
import gc
import tkinter as tk
from tkinter import filedialog, StringVar, IntVar, ttk
import queue
import time
import sys
import threading
import pythoncom
import keyboard

pythoncom.CoInitialize()

window = tk.Tk()
logQueue = queue.Queue()

WindowWidthVar = tk.StringVar()
WindowHeightVar= tk.StringVar()

# 赋默认值
WindowWidthVar.set("400")
WindowHeightVar.set("300")

class StoppableThread(threading.Thread):
    def __init__(self, func, args = None, id=None):
        super(StoppableThread, self).__init__()
        self.func = func
        self.args = args
        self.id = id
        self.flag = True
        self.daemon = True

    def run(self):
        while self.flag:
            if self.args:
                self.func(*self.args)
            else:
                self.func()
    def stop(self):
        self.flag = False

def insertLog(log):
    logQueue.put(log)
def radarStart():
    out_put = 'python Radar.py '+ WindowWidthVar.get() +' '+WindowHeightVar.get()
    os.system(out_put)
def startRadar():
    T = threading.Thread(target = radarStart)
    T.daemon = True
    T.start()
    insertLog("雷达已启动")
def aimStart():
    os.system("python assist.py")
def startAim():
    T = StoppableThread(func=aimStart)
    T.start()
    insertLog("自瞄已启动")

class GUI():
    def __init__(self, window, windowHeight=530, windowWidth=520):
        self.window = window
        self.windowHeight = windowHeight
        self.windowWidth = windowWidth

        # 数据有交互的变量
        self.logListText = None


        self.initGui()

        # 启动 after 方法
        self.window.after(100, self.showLog)
        # 进入消息循环
        self.window.mainloop()

    def initGui(self):
        # window
        self.window.title("战地5辅助")

        windowWidth = self.windowWidth
        windowHeight = self.windowHeight
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()

        window.geometry('%dx%d+%d+%d' % (
        windowWidth, windowHeight, (screenwidth - windowWidth) / 2, (screenheight - windowHeight) / 2))

        frame = tk.Frame(window)
        frame.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)

        # frame
        infoLabelFrame = ttk.LabelFrame(frame, text="基本信息")
        configFrame = ttk.LabelFrame(frame, text="雷达窗口大小配置")
        startRadarFrame = tk.Frame(frame)
        startAimFrame = tk.Frame(frame)
        logListFrame = tk.Frame(frame)

        infoLabelFrame.pack(fill=tk.X, expand=tk.YES, pady=4)
        configFrame.pack(fill=tk.X, expand=tk.YES, pady=4, ipady=4)
        startRadarFrame.pack(fill=tk.X, expand=tk.YES, pady=4)
        startAimFrame.pack(fill=tk.X, expand=tk.YES, pady=4)
        logListFrame.pack(fill=tk.BOTH, expand=tk.YES, pady=4)

        # infoLableFrame
        fnFrame = tk.Frame(infoLabelFrame)
        authorFrame = tk.Frame(infoLabelFrame)

        fnFrame.pack(fill=tk.X, expand=tk.YES, padx=2)
        authorFrame.pack(fill=tk.X, expand=tk.YES, padx=2)

        # fnFrame
        tk.Label(fnFrame, text="战地5辅助（雷达+自瞄）").grid(sticky=tk.W)
        tk.Label(fnFrame, text="仅供学习交流，严禁用于商业用途，请于24小时内删除").grid(sticky=tk.W)

        # authorFrame
        # TODO：复制功能
        authorLabel = tk.Label(authorFrame, text="感谢70RMUND、exex4大佬源码分享")

        authorLabel.pack(side=tk.RIGHT)

        # configFrame
        WindowWidthFrame = tk.Frame(configFrame)
        WindowHeightFrame = tk.Frame(configFrame)

        WindowWidthFrame.pack(fill=tk.X, padx=3)
        WindowHeightFrame.pack(fill=tk.X, padx=3)

        # WindowWidthFrame
        WindowWidthLabel = tk.Label(WindowWidthFrame, text="长度")
        WindowWidthEntry = ttk.Entry(WindowWidthFrame, textvariable=WindowWidthVar)
        self.WindowWidthEntry = WindowWidthEntry

        WindowWidthLabel.pack(side=tk.LEFT)
        WindowWidthEntry.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, padx=6)

        # WindowHeightFrame
        WindowHeightLabel = tk.Label(WindowHeightFrame, text="高度")
        WindowHeightEntry = ttk.Entry(WindowHeightFrame, textvariable=WindowHeightVar)
        self.WindowHeightEntry = WindowHeightEntry

        WindowHeightLabel.pack(side=tk.LEFT)
        WindowHeightEntry.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, padx=6)

        # startRadarFrame
        startRadarButton = ttk.Button(startRadarFrame, text='开启雷达', command=startRadar)
        startRadarButton.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, ipady=1.5)

        # startAimFrame
        startAimButton = ttk.Button(startAimFrame, text='开启自瞄', command=startAim)
        startAimButton.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, ipady=1.5)

        # logListFrame
        scrollBar = tk.Scrollbar(logListFrame)
        logListText = tk.Text(logListFrame, height=100, yscrollcommand=scrollBar.set)
        self.logListText = logListText
        scrollBar.config(command=logListText.yview)

        scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        logListText.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

    def showLog(self):
        while not logQueue.empty():
            content = logQueue.get()
            self.logListText.insert(tk.END, content + "\n")
            self.logListText.yview_moveto(1)
        self.window.after(100, self.showLog)

if __name__ == '__main__':
    insertLog("注意事项：")
    insertLog("1）自瞄绑定键为左ALT，自瞄部位切换键为+，后续将支持修改")
    GUI(window)

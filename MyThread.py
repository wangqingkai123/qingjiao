# _*_ coding: utf-8 _*_
__author__ = '王庆凯'
__date__ = '2020/11/18 17:13'

from PyQt5.QtCore import QThread, pyqtSignal
import xlrd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from pynput.keyboard import Key, Listener


class MyThread(QThread):
    username = ""
    password = ""
    driver = None
    infolist = []
    index_list = 0
    is_space = True
    startnum = 1
    url = 'https://www.2-class.com/'
    my_signal = pyqtSignal(int, str, str)  # 自定义信号对象。参数str就代表这个信号可以传一个字符串
    quit_signal = pyqtSignal()
    filename = ""
    is_close_weber = True

    def setIsCloseWeber(self, isclose):
        self.is_close_weber = isclose

    def setStartNum(self, num):
        self.startnum = num

    def setUsernameRC(self, row, col):
        self.usernamerow = row
        self.usernamecol = col

    def setPswRC(self, row, col):
        self.pswrow = row
        self.pswcol = col

    def setFileName(self, filename):
        self.filename = filename

    def __init__(self):
        super(MyThread, self).__init__()

    def on_release(self, key):
        if key == Key.space:
            self.next_run()

        if key == Key.esc:
            self.quit_signal.emit()


    def readExcelInfo(self):
        book = xlrd.open_workbook(self.filename, 'w')
        sheet = book.sheets()[0]
        mylist = []
        for i in range(self.usernamerow-1, sheet.nrows):
            temlist = []
            admin = sheet.cell_value(i, self.usernamecol-1)
            pwd = sheet.cell_value(i, self.pswcol-1)
            temlist.append(admin)
            temlist.append(pwd)
            mylist.append(temlist)
        self.infolist = mylist

    def caozuo(self, username, password):
        try:
            print(username)
            print(password)
            self.driver = webdriver.Firefox()
            self.driver.get(self.url)
            self.driver.maximize_window()
            self.driver.find_element_by_class_name('ant-btn').click()
            self.driver.find_element_by_id('account').click()
            self.driver.find_element_by_id('account').clear()
            self.driver.find_element_by_id('account').send_keys(username)
            self.driver.find_element_by_id('password').click()
            self.driver.find_element_by_id('password').clear()
            self.driver.find_element_by_id('password').send_keys(password)
            self.driver.find_element_by_class_name('submit-btn').click()
            time.sleep(2)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-panel"))).click()


        except:
            return

    def next_run(self):
        if self.is_close_weber:
            if self.driver is not None:
                self.driver.quit()
        index = self.index_list + self.startnum
        tem = self.infolist[index - 1]
        self.my_signal.emit(index, tem[0], tem[1])
        self.index_list += 1
        self.caozuo(tem[0], tem[1])

    def run(self):  # 线程执行函数
        self.readExcelInfo()
        self.next_run()
        with Listener(on_release=self.on_release) as listener:
            listener.join()

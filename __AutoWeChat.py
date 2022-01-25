#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
auto script for WeChat
@auto: chaney
@mail: zhangqiuqian01@gmail.com

getting start:
1. you need use WeChat(your WeChat path) to create a object of WeChat.
2. you should use msgTo(your wanna send msg to) to select a session. default send to file helper.
3. you can use sendFile(your file path) to send a file or image in your session.
4. you can use sendText(your text file path) to send a file of text in your session.
5. you can use sendText(your text file path) to send a file of text in your session.
6. you can use sendMsg(your msg) to send a short msg in your session.
"""
import os
import cv2
import time
import pyautogui
import pyperclip
from PIL import ImageGrab


class WeChat:
    def __init__(self, wxPath):
        self.wxPath = wxPath
        self.similarity = 0.85
        self.__msg = ''
        self.__text = ''
        self.__enter = 'enter'
        self.__logDir = os.path.join(os.getcwd(), 'wx_logs')
        self.__imgPath = os.path.join(os.getcwd(), 'wx_images')
        self.__searchBar = os.path.join(self.__imgPath, 'search.jpg')
        self.__fileBtn = os.path.join(self.__imgPath, 'file.jpg')
        self.__screen = os.path.join(self.__imgPath, 'screen.jpg')
        if not os.path.exists(self.__logDir):
            os.mkdir(self.__logDir)
        self.__record('init completely')

    # open WeChat
    def __openWx(self):
        pyautogui.hotkey('win', 'd')
        fp = os.popen(self.wxPath)
        time.sleep(1)
        fp.close()

    # record options
    def __record(self, option: str):
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        logName = now[: 10]
        with open(os.path.join(self.__logDir, logName)+'.log', 'a', encoding='utf-8') as fp:
            fp.write(now + '\t' + option + '\n')

    # desktop screenshots for matchTemplates
    def __scanner(self, pic='screen.jpg'):
        screen = ImageGrab.grab()
        if screen is not None:
            screen.save(os.path.join(self.__imgPath, pic))
            return os.path.join(self.__imgPath, pic)
        else:
            return 'err'

    # find coordinate of target on desktop
    def __matchTemplates(self, src, target):
        src = cv2.imread(src)
        target = cv2.imread(target)
        time.sleep(0.5)
        result = cv2.matchTemplate(src, target, cv2.TM_CCOEFF_NORMED)
        pos_start = cv2.minMaxLoc(result)[3]  # 最佳坐标maxLoc
        similarity = cv2.minMaxLoc(result)[1]  # 相似度

        if similarity < self.similarity:
            return -1, -1

        x = int(pos_start[0]) + int(target.shape[1] / 2)
        y = int(pos_start[1]) + int(target.shape[0] / 2)
        return x, y

    # find message to
    def msgTo(self, To: str = 'fileHelper'):
        self.__openWx()
        scr = self.__scanner()
        obj = self.__searchBar

        x, y = self.__matchTemplates(scr, obj)
        pyautogui.click(x, y)
        time.sleep(0.5)
        pyperclip.copy(To)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.hotkey(self.__enter)

    # send a file or image
    def sendFile(self, file: str):
        scr = self.__screen
        obj = self.__fileBtn

        x, y = self.__matchTemplates(scr, obj)
        pyautogui.click(x, y)
        time.sleep(0.5)
        pyperclip.copy(file)
        pyautogui.hotkey('ctrl', 'v')
        self.send()
        self.send()
        self.__record(f'send file {file} successfully')

    # send a short message. (you should use send() to confirm after call this)
    def sendMsg(self, msg):
        self.__msg = msg
        pyperclip.copy(self.__msg)
        pyautogui.hotkey('ctrl', 'v')

    # send content of a text file
    def sendText(self, text):
        fp = open(text, 'r', encoding='utf-8')
        self.__text = fp.read()
        fp.close()
        pyperclip.copy(self.__text)
        pyautogui.hotkey('ctrl', 'v')
        self.send()
        self.__record(f'send text {text} successfully')

    # next line
    def nextLine(self):
        pyautogui.hotkey('shift', self.__enter)

    # confirm sending
    def send(self):
        time.sleep(0.5)
        pyautogui.hotkey(self.__enter)


if __name__ == '__main__':
    wx = r'E:\Application\WeChat\WeChat.exe'
    wx = WeChat(wx)
    wx.msgTo()
    wx.sendFile(r'D:\Code\PyCode\myTools\wx_images\file.jpg')
    wx.sendText(r'D:\Code\PyCode\myTools\wx_images\text')
    wx.sendMsg('Hello world !')
    wx.nextLine()
    wx.sendMsg('以上消息来自：@微信小助手')
    wx.send()

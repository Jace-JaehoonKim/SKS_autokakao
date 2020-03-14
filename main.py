import sys
import pyautogui
import time
import pyperclip
import os
import random 
import pandas as pd
import pdb
from bs4 import BeautifulSoup 
import requests 
import re


def send_msg(repeat_number):
    for i in range(int(repeat_number)):
        time_wait = random.uniform(3, 5)
        print('Repeat Number : ', i + 1, end='')
        print(' // Time wait : ', time_wait)
        time.sleep(time_wait)
        pyautogui.keyDown('enter')
            
        url ='https://www.thebell.co.kr/free/index.asp'
        board_response=requests.get(url)
        board_html=board_response.text
        board_soup = BeautifulSoup(board_html, 'html.parser')
    
        board_name_lists = board_soup.select('#contents > div.contentSection > div > div.topNewsSection > div.content.R > ul > li > a')  

        for board_name_list in board_name_lists:
            board_name_text=board_name_list.text
            deld=re.compile('(?<=href=").*?(?=")')
            result = deld.findall(str(board_name_list))
            board_explain_text=('https://www.thebell.co.kr/'+str(result[0]))
            my_msg = "{} {} ".format(board_name_text, board_explain_text)
            pyperclip.copy(my_msg)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.keyDown('enter')

        url1 ='https://news.naver.com/main/home.nhn'
        board_response1=requests.get(url1)
        board_html1=board_response1.text
        board_soup1 = BeautifulSoup(board_html1, 'html.parser')
        board_name_lists1 = board_soup1.select('#ranking_101 li a')  

        for board_name_list in board_name_lists1:
            board_name_text=board_name_list.text

            deld2=re.compile('(?<=href=").*?(?=")')
            board_explain_text = deld2.findall(str(board_name_list)) 
    
            board_explain_text1 =  re.sub('amp;', '', board_explain_text[0])
            board_explain_text1 = ('https://news.naver.com'+board_explain_text1)
            my_msg = "{} , {} ".format(board_name_text ,board_explain_text1)
            pyperclip.copy(my_msg)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.keyDown('enter')       

        pyautogui.keyDown('esc')
        pyautogui.keyDown('down')


def filter_friend(filter_keyword, init_number):
    # 사람 아이콘 클릭
    try:
        click_img(img_path + 'person_icon.png')
        try:
            click_img(img_path + 'person_icon2.png')
        except Exception as e :
            print('e ', e)
    except Exception as e :
        print('e ', e)
    # X 버튼이 존재한다면 클릭하여 내용 삭제
    try:
        click_img(img_path + 'x.png')
    except: 
        pass
    time.sleep(1)
    # 돋보기 아이콘 오른쪽 클릭
    click_img_plus_x(img_path+'search_icon.png', 30)
    if filter_keyword == '':
        pyautogui.keyDown('esc')
    else:
        pyperclip.copy(filter_keyword)
    pyautogui.hotkey('ctrl', 'v')
    for i in range(int(init_number)-1):
        pyautogui.keyDown('down')
    time.sleep(2)


def click_img(imagePath):
    location = pyautogui.locateCenterOnScreen(imagePath, confidence = conf)
    x, y = location
    pyautogui.click(x, y)


def click_img_plus_x(imagePath, pixel):
    location = pyautogui.locateCenterOnScreen(imagePath, confidence = conf)
    x, y = location
    pyautogui.click(x + pixel, y)


def doubleClickImg (imagePath):
    location = pyautogui.locateCenterOnScreen(imagePath, confidence = conf)
    x, y = location
    pyautogui.click(x, y, clicks=2)


def set_delay():
    delay_time = input("몇 초 후에 프로그램을 실행하시겠습니까? : ")
    print(delay_time + "초 후에 프로그램을 실행합니다.")
    for remaining in range(int(delay_time), 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r프로그램 실행!\n")


def logout():
    try:
        click_img(img_path + 'menu.png')
    except Exception as e:
        print('e ', e)
    try:
        click_img(img_path + 'logout.png')
    except Exception as e:
        print('e ', e)


def bye_msg():
    input('프로그램이 종료되었습니다.')


def set_import_msg():
    with open("send_for_text.txt", "r", encoding='UTF-8') as f:
        text = f.read()
        print('======== 아래는 전송할 텍스트입니다. ========\n', text)
        return text


def initialize():
    print('Monitor size : ', end='')
    print(pyautogui.size())
    print(pyautogui.position())
    filter_keyword = input("보낼대상  : ")
    init_number = input("시작지점 : ")
    repeat_number = input("반복횟수 : ")
    print('=================')
    print('뉴스 전송 시작')
    print('=================')
    return (filter_keyword, init_number, repeat_number)


# config
img_path = os.path.dirname(os.path.realpath(__file__)) + '/img/'
conf = 0.90
pyautogui.PAUSE = 0.5

if __name__ == "__main__":
    (filter_keyword, init_number, repeat_number) = initialize()
    filter_friend(filter_keyword, init_number)
    send_msg(repeat_number)
    bye_msg()

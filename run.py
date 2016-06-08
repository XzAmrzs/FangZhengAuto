import re

import requests
from bs4 import BeautifulSoup

from captcha.Captcha_Login import login

base_url = 'http://172.18.254.101/'
username = input("请输入学号: ").strip()
password = input("请输入密码: ").strip()
user_type = '学生'

session = requests.session()
html_text = login(session, base_url, username, password, user_type)

bsobj = BeautifulSoup(html_text, "html.parser")
pattern = r'xsjxpj\.aspx\?xkkh=(.)*gnmkdm=(.)+'

for tag in bsobj.find_all("a", href=re.compile(pattern)):
    review_url = base_url + tag.get("href")
    xkkh_pattern = r'\((\d)+-(\d)+-(\d)+\)-(\d)+-(\d)+-(\d)+'
    xkkh = re.search(xkkh_pattern, review_url).group(0)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' \
                 ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
    headers = {
        "User-Agent": user_agent,
        "Accept": 'text/html, application/xhtml+xml, image/jxr, */*',
        "Accept-Language": 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
        "Referer": base_url + "/xs_main.aspx?xh=" + username
    }
    review_bsObj = BeautifulSoup(session.get(review_url, headers=headers).content, "html.parser")

    __VIEWSTATE = review_bsObj.find('input', attrs={'name': '__VIEWSTATE'})['value']

    select_pattern = r'(\w)+(\d)__(\w)+(\d)_JS2'
    # 这个number确定该课程对应的教师数量,还可优化
    number = 2 if review_bsObj.find("select", id=re.compile(select_pattern)) else 1
    print('该课程有' + str(number) + '名教师')
    post_data = {
        '__EVENTARGUMENT': '',
        '__EVENTTARGET': '',
        '__VIEWSTATE': __VIEWSTATE.encode('cp936'),
        'Button1': "保 存".encode('cp936'),
        # 评教号码
        'pjkc': xkkh.encode('cp936'),
        'pjxx': '',
        'TextBox1': '0',
        'txt1': '',
    }

    for c in range(1, number+1):
        for i in range(2, 14):
            # 优秀 # b'\xd3\xc5\xd0\xe3'
            post_data.update({'DataGrid1:_ctl' + str(i) + ':JS' + str(c): b'\xd3\xc5\xd0\xe3'})
            post_data.update({'DataGrid1:_ctl' + str(i) + ':txtjs' + str(c): ''})
            if i == 13:
                # 最后一个评个良好
                post_data.update({'DataGrid1:_ctl' + str(i + 1) + ':JS' + str(c): b'\xc1\xbc\xba\xc3'})
                post_data.update({'DataGrid1:_ctl' + str(i + 1) + ':txtjs' + str(c): ''})

    headers = {
        "User-Agent": user_agent,
        "Accept": 'text/html, application/xhtml+xml, image/jxr, */*',
        "Accept-Language": 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
        "Content-Type": 'application/x-www-form-urlencoded',
        "Referer": base_url + "xs_main.aspx?xh=" + username
    }

    session.post(review_url, data=post_data, headers=headers)
    print('课程号为' + xkkh + '的课程已经评教完成')
print('所有课程已经评教,请登陆确认')

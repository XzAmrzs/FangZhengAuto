# coding=utf-8
import requests
from bs4 import BeautifulSoup
from LianZhongDaMA.LianZhongAPI import getCaptcha

lianzhong_username = ''
lianzhong_password = ''


def login(base_url, username, password, user_type):
    session = requests.session()
    __VIEWSTATE = BeautifulSoup(session.get(base_url).content, "html.parser").find('input', attrs={
        'name': '__VIEWSTATE'})['value']
    # 获取验证码
    secretCode = getCaptcha(session, lianzhong_username,
                            lianzhong_password,
                            base_url + '/CheckCode.aspx',
                            "http://bbb4.hyslt.com/api.php?mod=php&act=upload",
                            '',
                            '',
                            '',
                            '')
    postData = {
        '__VIEWSTATE': __VIEWSTATE,
        'txtUserName': username,
        'TextBox2': password,
        'txtSecretCode': secretCode,
        'RadioButtonList1': user_type,
        'Button1': '',
        'lbLanguage': '',
        'hidPdrs': '',
        'hidsc': ''
    }
    # 请求登陆
    data = session.post(base_url + '/default2.aspx', postData)
    print(data)
    return data


if __name__ == '__main__':
    login(base_url='http://172.18.254.101',
          username='',
          password='',
          user_type='学生'
          )

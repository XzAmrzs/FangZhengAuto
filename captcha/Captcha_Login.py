from bs4 import BeautifulSoup


def get_Captcha(data):
    with open('captcha.png', "wb") as fb:
        fb.write(data)
    return input("请输入验证码: ")


def login(session, base_url, username, password, user_type):
    __VIEWSTATE = BeautifulSoup(session.get(base_url).content, "html.parser").find('input', attrs={
        'name': '__VIEWSTATE'})['value']
    data = session.get(base_url + '/CheckCode.aspx').content
    secretCode = get_Captcha(data)
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
    login_html = session.post(base_url + '/default2.aspx', postData)
    return login_html.text


if __name__ == '__main__':
    import requests
    login(session=requests.session(),
          base_url='http://172.18.254.101',
          username='',
          password='',
          user_type='学生'
          )

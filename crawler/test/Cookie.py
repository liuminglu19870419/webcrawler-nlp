#encoding: utf-8
'''
Created on 2015年12月14日

@author: lml
'''

from selenium import webdriver

if __name__ == '__main__':
    driver = webdriver.Firefox()

    driver.get("https://www.baidu.com/")
    
    cookies =[{u'domain': u'.baidu.com', u'name': u'BAIDUID', u'value': u'ACE6D3C6335FC061ED7D1B3D254677D1:FG=1', u'expiry': 3597585928, u'path': u'/', u'httpOnly': False, u'secure': False}, {u'domain': u'.baidu.com', u'name': u'BIDUPSID', u'value': u'ACE6D3C6335FC061ED7D1B3D254677D1', u'expiry': 3597585928, u'path': u'/', u'httpOnly': False, u'secure': False}, {u'domain': u'.baidu.com', u'name': u'PSTM', u'value': u'1450102280', u'expiry': 3597585928, u'path': u'/', u'httpOnly': False, u'secure': False}, {u'domain': u'www.baidu.com', u'name': u'BD_HOME', u'value': u'0', u'expiry': None, u'path': u'/', u'httpOnly': False, u'secure': False}, {u'domain': u'www.baidu.com', u'name': u'BD_UPN', u'value': u'133352', u'expiry': 1450966281, u'path': u'/', u'httpOnly': False, u'secure': False}, {u'domain': u'www.baidu.com', u'name': u'YOUDAO_MOBILE_ACCESS_TYPE', u'value': u'1', u'expiry': 1481637857, u'path': u'/', u'httpOnly': False, u'secure': False}, {u'domain': u'www.baidu.com', u'name': u'OUTFOX_SEARCH_USER_ID', u'value': u'-1289957052@221.216.217.220', u'expiry': 2396181857, u'path': u'/', u'httpOnly': False, u'secure': False}, {u'domain': u'www.baidu.com', u'name': u'lzstat_uv', u'value': u'12268340691080955571|3601912', u'expiry': 1765721058, u'path': u'/', u'httpOnly': False, u'secure': False}, {u'domain': u'www.baidu.com', u'name': u'sbt', u'value': u'1450101863777', u'expiry': None, u'path': u'/', u'httpOnly': False, u'secure': False}, {u'domain': u'www.baidu.com', u'name': u'user-from', u'value': u'web.index', u'expiry': None, u'path': u'/', u'httpOnly': False, u'secure': False}, {u'domain': u'www.baidu.com', u'name': u'from-page', u'value': u'http://www.youdao.com/', u'expiry': None, u'path': u'/', u'httpOnly': False, u'secure': False}, {u'domain': u'www.baidu.com', u'name': u'CNZZDATA1256118513', u'value': u'490837576-1450097359-%7C1450097359', u'expiry': 1465826664, u'path': u'/', u'httpOnly': False, u'secure': False}, {u'domain': u'www.baidu.com', u'name': u'lzstat_ss', u'value': u'3139652957_1_1450130664_3601912', u'expiry': None, u'path': u'/', u'httpOnly': False, u'secure': False}, {u'domain': u'www.baidu.com', u'name': u'H_PS_645EC', u'value': u'2377A3fh56e4cuV1G1yhR8ofleTwtb1e50uXznHdqzSdqmFPAqrdwnSuP3A', u'expiry': 1450104891, u'path': u'/', u'httpOnly': False, u'secure': False}, {u'domain': u'www.baidu.com', u'name': u'BD_CK_SAM', u'value': u'1', u'expiry': None, u'path': u'/', u'httpOnly': False, u'secure': False}, {u'domain': u'www.baidu.com', u'name': u'BDSVRTM', u'value': u'121', u'expiry': None, u'path': u'/', u'httpOnly': False, u'secure': False}, {u'domain': u'.baidu.com', u'name': u'H_PS_PSSID', u'value': u'18229_18285_1435_18203_18241_18156_12826_17000_17072_15819_11980_10634', u'expiry': None, u'path': u'/', u'httpOnly': False, u'secure': False}, {u'domain': u'.www.baidu.com', u'name': u'__bsi', u'value': u'16534932260588862610_00_0_I_R_124_0303_C02F_N_I_I_0', u'expiry': 1450102304, u'path': u'/', u'httpOnly': False, u'secure': False}]
 
    for cookie in cookies:
        del cookie[u'domain']
        driver.add_cookie(cookie)
        
    # 获得cookie信息
    cookies = driver.get_cookies()
    
    #将获得cookie的信息打印
    for cookie in cookies:
        print cookie
    raw_input("input anything")
    
    # 获得cookie信息
    cookies = driver.get_cookies()
    
    print cookies
    #将获得cookie的信息打印
    for cookie in cookies:
        print cookie
    driver.quit()
#encoding: utf-8
'''
Created on 2015年12月6日

@author: lml
'''
# insert into test.failed_url SELECT * FROM test.published_url where test.published_url.url not in (select url from test.successed_url) and test.published_url.url not in (select url from test.failed_url);
if __name__ == '__main__':
    pass
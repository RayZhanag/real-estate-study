# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from random import choice
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

logger = logging.getLogger('LianJia') 
class LianjiaSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result,spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
  
class RandomUserAgent(object):
    def __init__(self,user_agent):
        self.user_agent=user_agent
        
    @classmethod
    def from_crawler(cls, crawler):
        user_agent_list=crawler.settings.get('USER_AGENT_LIST')
        return cls(user_agent_list)

    #def process_request(self, request, response):
    def process_request(self, request, spider):
        user_agent=choice(self.user_agent)  
        #print("user_agent:",user_agent)
        #request.headers['User-Agent']=user_agent
        request.headers.setdefault('User-Agent',user_agent)
       
class FaillogMiddleware(object):
    def process_response(self, request, response, spider):
        """if network is valid and connection to crawled website cannot be reached,
        then restart router to get a new IP address """
        if response.status >= 400 and is_connection_valid():
            logger.info("response code:%s  restart router."%response.status)
            self.restart_router()
            return request
        return response
        
    def is_connection_valid(self):
        hosts=('www.baidu.com','www.163.com','wwww.sina.com.cn')
        host=choice(hosts)
        port=80
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            s.connect((host,port)) #test whether the network is alive
            #except (urllib.error.URLError,socket.timeout,socket.gaierror):
        except (urllib.error.URLError,socket.timeout,socket.gaierror) as e:
            logger.info("connection error:e")
            s.close()
            return False
        finally:
            s.close()
            return True 
            
    def restart_router(self):
        browser=webdriver.Chrome()
        browser.get("http://192.168.1.1")
        input_selector="span input.text"
        button_selector="div input.button"
        pw="leiz1507"
        wBrowser=WebDriverWait(browser,10)
        wBrowser.operate_by_css_selector=lambda css_sel:WebDriverWait(browser,30).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR,css_sel)))
        wBrowser.operate_by_css_selector(input_selector).send_keys(pw)
        wBrowser.operate_by_css_selector(button_selector).click()
        wBrowser.operate_by_css_selector("#menu_xtgl").click()
        wBrowser.operate_by_css_selector("#menu_restart").click()
        wBrowser.operate_by_css_selector("input.button.XL").click()
        wBrowser.until(expected_conditions.alert_is_present()).accept()
        browser.close()
    """def process_exception(self, request, exception, spider):
        self._faillog(request, u'EXCEPTION', exception, spider)
        return request

    def _faillog(self, request, errorType, reason, spider):
        with codecs.open('log/faillog.log', 'a', encoding='utf-8') as file:
            file.write("%(now)s [%(error)s] %(url)s reason: %(reason)s \r\n" %
                       {'now':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'error': errorType,
                        'url': request.url,
                        'reason': reason})"""



 


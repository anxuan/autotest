#! python3
# coding: utf-8
import time, os
from datetime import datetime as dt
from HtmlTestRunner import HTMLTestRunner
import unittest

from appium import webdriver

# # 设置路径信息
# PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

caps = dict()
# caps['platformName'] = 'Android'  # 测试平台
# caps['platformVersion'] = '7.0'   # 平台版本
# caps['deviceName'] = 'emulator-5554'  # 设备ID（可通过adb devices获取）

caps['platformName'] = 'Android' #测试平台
caps['platformVersion'] = '6.0'  #平台版本
caps['deviceName'] = '3CG4C16826000583'  #设备ID（可通过adb devices获取）


caps['autoLaunch'] = True  # 是否自动启动
caps['noReset'] = True
# for chinese
caps['unicodeKeyboard'] = True
caps['resetKeyboard'] = True

file_name = '/Users/wangxudong1129/Documents/apks/hupu/com-hupu-games-7-3-2-17891-7306-hupucom.apk'
# caps['app'] = file_name

caps['appPackage'] = 'com.hupu.games'  # 包名
caps['appActivity'] = '.activity.LaunchActivity'  # 启动的activity
# caps['newCommandTimeout'] = '20'

# 安装app
# driver.install_app('C:/Users/xianm/AndroidTesting/apps/weixin.apk')

driver = webdriver.Remote('http://localhost:4723/wd/hub', caps)
print('最多等待30秒!', dt.now())
driver.implicitly_wait(30)
print(dt.now())


class HupuAppTest(unittest.TestCase):
    """
    虎扑安卓app搜索功能测试
    """
    def setUp(self):
        print("start test")

    def tearDown(self):
        try:
            driver.quit()
        except Exception as e:
            pass
        print("end")

    def test_main_function(self):
        """
        测试主体 只能有一个test函数，不然会出错:
        selenium.common.exceptions.InvalidSessionIdException: Message: A session is either terminated or not started
        """
        {test_content}


# 用__main__时需要在外部python直接运行这个runtest.py脚本才能生成html文件
if __name__ == '__main__':
    # now = time.strftime("%Y-%m-%d_%H-%M-%S_")
    # filename = '/Users/wangxudong1129/projects/hupu/test/appium_AndroidTesting/reports/' + now + 'result.html'
    # print('filename: ' + filename)
    # fp = open(filename, 'wb')
    # fp.close()

    testunit = unittest.TestSuite()
    testunit.addTest(HupuAppTest("test_main_function"))

    runner = HTMLTestRunner(output='.')
    runner.run(testunit)
from appium.webdriver.common.mobileby import MobileBy
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages import *


class GroupLogPage(BasePage):
    """日志页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.EditGroupPageActivity'

    __locators = {
        '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
        '我发出的': (MobileBy.ACCESSIBILITY_ID, '我发出的'),
        '我收到的': (MobileBy.ACCESSIBILITY_ID, '我收到的'),
        '写日志': (MobileBy.ACCESSIBILITY_ID, '写日志'),
        # 日志类型页面
        '日报': (MobileBy.ACCESSIBILITY_ID, '日报'),
        '周报': (MobileBy.ACCESSIBILITY_ID, '周报'),
        '月报': (MobileBy.ACCESSIBILITY_ID, '月报'),

    }

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在日志"""

        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self.is_text_present('写日志')
            )
            return True
        except:
            return False

    @TestLogger.log()
    def wait_for_page_load(self, timeout=15, auto_accept_alerts=True):
        """等待日志页面加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["写日志"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log('判断页面存在元素')
    def is_exist_element(self, locator='关闭'):
        time.sleep(2)
        return self._is_element_present(self.__locators[locator])

    @TestLogger.log()
    def click_back(self, element='返回'):
        """点击返回"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_write_log(self, element='写日志'):
        """点击写日志"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_daily_log(self, element='日报'):
        """点击写日报"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_weekly_log(self, element='周报'):
        """点击写周报"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_month_log(self, element='月报'):
        """点击写月报"""
        self.click_element(self.__class__.__locators[element])


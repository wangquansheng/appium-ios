import time
from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class AttendanceCardPage(BasePage):
    """考勤打卡首页"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '返回1': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="文章"]/XCUIElementTypeOther[1]'),
        '返回2': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="文章"]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]'),
        '帮助图标': (MobileBy.XPATH, '//XCUIElementTypeStaticText[contains(@name,"Hi")]/../following-sibling::*[1]'),
        '创建考勤组按钮': (MobileBy.XPATH, '//XCUIElementTypeButton[@name="创建考勤组"]'),
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待考勤打卡首页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["帮助图标"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def is_on_attendance_card_page(self, timeout=10, auto_accept_alerts=True):
        """当前页面是否在考勤打卡首页"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["帮助图标"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_coordinates(self.__class__.__locators["返回1"])

    @TestLogger.log()
    def click_back2(self):
        """点击返回"""
        self.click_coordinates(self.__class__.__locators["返回2"])

    @TestLogger.log()
    def click_help_icon(self):
        """点击帮助图标"""
        self.click_coordinates(self.__class__.__locators["帮助图标"])

    @TestLogger.log()
    def wait_for_help_page_load(self, name):
        """等待帮助页加载"""
        try:
            self.wait_until(
                timeout=20,
                auto_accept_permission_alert=True,
                condition=lambda d: self.is_text_present(name)
            )
        except:
            raise AssertionError("帮助页加载失败")
        return self

    @TestLogger.log()
    def click_create_attendance_group_button(self):
        """点击创建考勤组按钮"""
        self.click_element(self.__class__.__locators["创建考勤组按钮"])
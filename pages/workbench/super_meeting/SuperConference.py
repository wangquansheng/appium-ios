import time
from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SuperConferencePage(BasePage):
    """超级会议首页"""

    __locators = {
        '预约会议': (MobileBy.ACCESSIBILITY_ID, "预约会议"),
        '马上开会': (MobileBy.ACCESSIBILITY_ID, "马上开会"),
        '右上角帮助图标': (MobileBy.ACCESSIBILITY_ID, "cc call groupcall profile ic q"),
        '下三角图标': (MobileBy.XPATH, "//*[@name='分钟']/following-sibling::*[1]"),
        '关闭': (MobileBy.ACCESSIBILITY_ID, 'cc h5 ic close'),
    }

    @TestLogger.log()
    def is_on_super_meeting_page(self, timeout=20, auto_accept_alerts=True):
        """当前页面是否在超级会议首页"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["预约会议"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待超级会议首页加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["预约会议"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_help_icon(self):
        """点击右上角帮助图标"""
        self.click_element(self.__class__.__locators["右上角帮助图标"])

    @TestLogger.log()
    def click_down_triangle(self):
        """点击下三角图标"""
        self.click_coordinates(self.__class__.__locators["下三角图标"])

    @TestLogger.log()
    def click_appointment_meeting(self):
        """点击预约会议"""
        self.click_element(self.__class__.__locators["预约会议"])

    @TestLogger.log()
    def click_right_off_meeting(self):
        """点击马上开会"""
        self.click_element(self.__class__.__locators["马上开会"])

    @TestLogger.log()
    def click_close(self):
        """点击关闭"""
        self.click_element(self.__class__.__locators["关闭"])
import time
from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class VoiceNotifyPage(BasePage):
    """语音通知首页"""

    __locators = {
        '创建语音通知': (MobileBy.ACCESSIBILITY_ID, "创建语音通知"),
        '发送': (MobileBy.ACCESSIBILITY_ID, "发送"),
        '通知接收人+号': (MobileBy.XPATH, "//*[@name='定时发送']/../preceding-sibling::*[1]"),
    }

    @TestLogger.log()
    def is_on_voice_notify_page(self, timeout=20, auto_accept_alerts=True):
        """当前页面是否在语音通知首页"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["创建语音通知"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待语音通知首页加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["创建语音通知"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def wait_for_create_voice_notify_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待创建语音通知页面加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["通知接收人+号"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_add_icon(self):
        """点击通知接收人+号"""
        self.click_coordinates(self.__class__.__locators["通知接收人+号"])

    @TestLogger.log()
    def click_create_voice_notify(self):
        """点击创建语音通知"""
        self.click_element(self.__class__.__locators["创建语音通知"])

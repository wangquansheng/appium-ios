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
        '本月剩余通知条数': (MobileBy.XPATH, "//*[@name='本月剩余通知']/following-sibling::*[1]"),
        '创建语音通知输入框': (MobileBy.IOS_PREDICATE, "type=='XCUIElementTypeTextView'"),
        '右上角帮助图标': (MobileBy.ACCESSIBILITY_ID, "cc call groupcall profile ic q"),
        '下三角图标': (MobileBy.XPATH, "//*[@name='我创建的']/../preceding-sibling::*[1]"),
        '上三角图标': (MobileBy.XPATH, "//*[@name='我创建的']/../preceding-sibling::*[1]/XCUIElementTypeOther"),
        '充值': (MobileBy.ACCESSIBILITY_ID, "充值"),
        '如何申请认证弹窗关闭图标': (MobileBy.XPATH, "//*[@name='如何申请认证？']/../preceding-sibling::*[1]"),
        '小键盘图标': (MobileBy.XPATH, "//*[@name='通知接收人']/../preceding-sibling::*[1]/XCUIElementTypeOther"),
        '录制语音': (MobileBy.XPATH, "//XCUIElementTypeOther[@name='创建语音通知']/XCUIElementTypeOther[1]"),
        '录制语音时长': (MobileBy.XPATH,
                   "//XCUIElementTypeOther[@name='创建语音通知']/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]/XCUIElementTypeStaticText[1]"),
        '录制语音删除按钮': (MobileBy.XPATH, "//XCUIElementTypeOther[@name='创建语音通知']/XCUIElementTypeOther[1]/XCUIElementTypeOther[3]"),
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

    @TestLogger.log()
    def get_remaining_notice(self):
        """获取剩余通知条数"""
        if self._is_element_present2(self.__class__.__locators["本月剩余通知条数"]):
            el = self.get_element(self.__class__.__locators["本月剩余通知条数"])
            return int(el.text)

    @TestLogger.log()
    def input_notice_content(self, content):
        """输入通知内容"""
        self.input_text(self.__class__.__locators["创建语音通知输入框"], content)

    @TestLogger.log()
    def click_send(self):
        """点击发送"""
        self.click_element(self.__class__.__locators["发送"])

    @TestLogger.log()
    def click_help_icon(self):
        """点击右上角帮助图标"""
        self.click_element(self.__class__.__locators["右上角帮助图标"])

    @TestLogger.log()
    def click_down_triangle(self):
        """点击下三角图标"""
        self.click_coordinates(self.__class__.__locators["下三角图标"])

    @TestLogger.log()
    def click_up_triangle(self):
        """点击上三角图标"""
        self.click_coordinates(self.__class__.__locators["上三角图标"])

    @TestLogger.log()
    def click_recharge(self):
        """点击充值"""
        self.click_element(self.__class__.__locators["充值"])

    @TestLogger.log()
    def click_popup_close_icon(self):
        """点击弹窗关闭图标"""
        self.click_element(self.__class__.__locators["如何申请认证弹窗关闭图标"])

    @TestLogger.log()
    def click_keyboard_icon(self):
        """点击小键盘图标"""
        self.click_element(self.__class__.__locators["小键盘图标"])

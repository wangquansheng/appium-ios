import time
from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class VoiceNotifyPage(BasePage):
    """语音通知首页"""

    __locators = {
        '创建语音通知': (MobileBy.ACCESSIBILITY_ID, "创建语音通知"),
        '我创建的': (MobileBy.ACCESSIBILITY_ID, "我创建的"),
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
        '话筒录制按钮': (MobileBy.XPATH, "//*[@name='cc_chat_voice_big']/following-sibling::*[1]"),
        '语音通知列表': (MobileBy.IOS_PREDICATE, "name=='发送成功' or name=='审核中'"),
    }

    @TestLogger.log()
    def is_on_voice_notify_page(self, timeout=20, auto_accept_alerts=True):
        """当前页面是否在语音通知首页"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["我创建的"])
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
                condition=lambda d: self._is_element_present(self.__class__.__locators["我创建的"])
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
        self.click_coordinates(self.__class__.__locators["小键盘图标"])

    @TestLogger.log()
    def click_microphone_button(self):
        """点击话筒录制按钮"""
        self.click_element(self.__class__.__locators["话筒录制按钮"])

    @TestLogger.log()
    def press_microphone_button(self, duration):
        """长按话筒录制按钮"""
        self.swipe_by_direction(self.__class__.__locators["话筒录制按钮"], "press", duration)

    @TestLogger.log()
    def press_slide_microphone_button(self, duration=5):
        """长按并滑动话筒录制按钮取消录制"""
        element = self.get_element(self.__class__.__locators["话筒录制按钮"])
        rect = element.rect
        left, right = int(rect['x']) + 1, int(rect['x'] + rect['width']) - 1
        top, bottom = int(rect['y']) + 1, int(rect['y'] + rect['height']) - 1
        x_start = left
        x_end = right + 100
        y_start = (top + bottom) // 2
        y_end = (top + bottom) // 2
        self.driver.execute_script("mobile:dragFromToForDuration",
                                   {"duration": duration, "element": None, "fromX": x_start,
                                    "fromY": y_start,
                                    "toX": x_end, "toY": y_end})

    @TestLogger.log()
    def click_microphone_icon(self):
        """点击话筒图标(话筒图标无法定位，暂时用坐标点击替代)"""
        self.click_coordinate(90.67, 26.7)

    @TestLogger.log()
    def is_exists_element_by_text(self, text):
        """是否存在某元素"""
        return self._is_element_present2(self.__class__.__locators[text])

    @TestLogger.log()
    def click_element_by_text(self, text):
        """点击某元素"""
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def click_voice_delete_button(self):
        """点击语音后的删除按钮"""
        self.click_coordinates(self.__class__.__locators["录制语音删除按钮"])

    @TestLogger.log()
    def get_voice_duration(self):
        """获取语音时长"""
        if self._is_element_present2(self.__class__.__locators["录制语音时长"]):
            el = self.get_element(self.__class__.__locators["录制语音时长"])
            return el.text

    @TestLogger.log()
    def clear_voice_notice(self):
        """清空语音通知"""
        current = 0
        while self._is_element_present2(self.__class__.__locators["语音通知列表"]):
            current += 1
            if current > 20:
                return
            self.click_element(self.__class__.__locators["语音通知列表"])
            self.click_accessibility_id_attribute_by_name("更多")
            self.click_accessibility_id_attribute_by_name("删除")
            self.click_accessibility_id_attribute_by_name("确定")
            self.wait_for_page_load()



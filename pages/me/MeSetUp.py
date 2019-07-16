from appium.webdriver.common.mobileby import MobileBy
from library.core.TestLogger import TestLogger
from library.core.BasePage import BasePage


class MeSetUpPage(BasePage):
    """我 -> 设置 页面"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.SettingActivity'

    __locators = {'': (MobileBy.ID, ''),
                'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                'android:id/content': (MobileBy.ID, 'android:id/content'),
                'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                '设置': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                'com.chinasofti.rcs:id/setting_sms': (MobileBy.ID, 'com.chinasofti.rcs:id/setting_sms'),
                '短信设置': (MobileBy.ID, 'com.chinasofti.rcs:id/setting_sms_text'),
                'com.chinasofti.rcs:id/default_SMS_app': (MobileBy.ID, 'com.chinasofti.rcs:id/default_SMS_app'),
                '消息通知': (MobileBy.ID, 'com.chinasofti.rcs:id/default_sms_text'),
                'com.chinasofti.rcs:id/callControl': (MobileBy.ID, 'com.chinasofti.rcs:id/callControl'),
                '来电管理': (MobileBy.ID, 'com.chinasofti.rcs:id/incoming_call_text'),
                'com.chinasofti.rcs:id/andNumberControl': (MobileBy.ID, 'com.chinasofti.rcs:id/andNumberControl'),
                '副号管理': (MobileBy.ID, 'com.chinasofti.rcs:id/second_number_text'),
                'com.chinasofti.rcs:id/manage_contact': (MobileBy.ID, 'com.chinasofti.rcs:id/manage_contact'),
                '联系人管理': (MobileBy.ID, 'com.chinasofti.rcs:id/manage_contact_text'),
                'com.chinasofti.rcs:id/font_setting': (MobileBy.ID, 'com.chinasofti.rcs:id/font_setting'),
                '字体大小': (MobileBy.ID, 'com.chinasofti.rcs:id/font_setting_text'),
                'com.chinasofti.rcs:id/outgoing_call_setting': (
                MobileBy.ID, 'com.chinasofti.rcs:id/outgoing_call_setting'),
                '拨号设置': (MobileBy.ID, 'com.chinasofti.rcs:id/outgoing_call_setting_text'),
                'com.chinasofti.rcs:id/multi_language_setting': (
                MobileBy.ID, 'com.chinasofti.rcs:id/multi_language_setting'),
                '多语言': (MobileBy.ID, 'com.chinasofti.rcs:id/multi_language_setting_text'),
                'com.chinasofti.rcs:id/upload_log_setting': (MobileBy.ID, 'com.chinasofti.rcs:id/upload_log_setting'),
                '参与体验改善计划': (MobileBy.ID, 'com.chinasofti.rcs:id/upload_log_setting_text'),
                'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),
                'android:id/navigationBarBackground': (MobileBy.ID, 'android:id/navigationBarBackground'),
                # 设置-》退出
                '确定退出？': (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message'),
                'com.chinasofti.rcs:id/btn_container': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_container'),
                '取消': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
                # 设置-》短信设置
                # 消息设置
                '消息': (MobileBy.IOS_PREDICATE, 'name == "消息"'),
                '消息送达状态显示': (MobileBy.XPATH, '//XCUIElementTypeSwitch[@name="消息送达状态显示"]'),
                '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
                }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待设置页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["消息"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_message(self):
        """点击消息设置"""
        self.click_element(self.__class__.__locators["消息"])

    @TestLogger.log()
    def click_back(self):
        """点击返回按钮"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def get_no_disturbing_btn_text(self):
        """获取消息送达状态显示"""
        if self._is_element_present2(self.__class__.__locators["消息送达状态显示"]):
            el = self.get_element(self.__class__.__locators["消息送达状态显示"])
            return el.text

    @TestLogger.log()
    def click_no_disturbing_button(self):
        """点击消息送达状态显示开关"""
        self.click_element(self.__class__.__locators["消息送达状态显示"])

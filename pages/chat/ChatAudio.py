from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatAudioPage(BasePage):
    """聊天语音页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity'

    __locators = {'': (MobileBy.ID, ''),

                  # 发送语音消息页面
                  '发送': (MobileBy.ACCESSIBILITY_ID, '发送'),
                  '退出': (MobileBy.ACCESSIBILITY_ID, '退出'),
                  '设置': (MobileBy.ACCESSIBILITY_ID, '设置'),
                  '按住说话': (MobileBy.ACCESSIBILITY_ID, 'chat voice talk'),
                  '同时发送语音+文字（语音识别）': (MobileBy.ACCESSIBILITY_ID, '同时发送语音+文字（语音识别）'),
                  '仅发送文字（语音识别）': (MobileBy.ACCESSIBILITY_ID, '仅发送文字（语音识别）'),
                  '仅发送语音': (MobileBy.ACCESSIBILITY_ID, '仅发送语音'),
                  '确定': (MobileBy.ACCESSIBILITY_ID, '确定'),

                  '17:48': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_time'),
                  'mobile952': (MobileBy.ID, 'com.chinasofti.rcs:id/text_name'),
                  '1': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
                  '无法识别，请重试': (MobileBy.ID, 'com.chinasofti.rcs:id/recoder_tip'),
                  'com.chinasofti.rcs:id/record_audio_btn': (MobileBy.ID, 'com.chinasofti.rcs:id/record_audio_btn'),

                  '取消': (MobileBy.ID, 'com.chinasofti.rcs:id/select_send_audio_type_cancel'),

                  '选项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/select_send_audio_type_root_view"]/android.widget.LinearLayout/android.widget.ImageView[@selected="true"]/../android.widget.TextView'),
                  '未选项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/select_send_audio_type_root_view"]/android.widget.LinearLayout/android.widget.ImageView[@selected="false"]/../android.widget.TextView'),
                  # 弹窗权限页面
                  '不再询问': (MobileBy.ID, 'com.lbe.security.miui:id/do_not_ask_checkbox'),
                  '要允许 和飞信 录制音频吗？': (MobileBy.ID, 'com.android.packageinstaller:id/permission_message'),
                  '拒绝': (MobileBy.ID, 'android:id/button2'),
                  '允许': (MobileBy.XPATH, "//*[contains(@text, '始终允许')]"),
                  '语音+文字选项': (MobileBy.ID, 'com.chinasofti.rcs:id/select_send_audio_and_text_icon'),
                  '我知道了': (MobileBy.XPATH, "//*[contains(@text, '我知道了')]"),
                  }

    @TestLogger.log()
    def click_voice(self, element='语音'):
        """点击语言按钮"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_send_voice(self, element='发送'):
        """点击发送语音按钮"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_voice_setting(self, element='设置'):
        """点击语音设置"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_send_voice_only(self, element='仅发送语音'):
        """点击仅发送语音按钮"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_sure(self, element='确定'):
        """点击确定按钮"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_exit(self, element='退出'):
        """点击退出按钮"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_only_text(self):
        """点击仅发送文字"""
        self.click_element(self.__class__.__locators["仅发送文字（语音识别）"])

    @TestLogger.log('设置语音界面格式为仅发送文本')
    def setting_voice_icon_in_send_text_only(self):
        self.click_send_voice()
        self.click_voice_setting()
        self.click_only_text()
        self.click_sure()
        self.click_exit()

    @TestLogger.log('设置语音界面格式为仅发送语音')
    def setting_voice_icon_in_send_voice_only(self):
        self.click_send_voice()
        self.click_voice_setting()
        self.click_send_voice_only()
        self.click_sure()
        self.click_exit()














    @TestLogger.log()
    def click_cancel(self):
        """点击取消"""
        self.click_element(self.__class__.__locators["取消"])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待聊天语音页面加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["退出"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_audio_type_select_page_load(self, timeout=2, auto_accept_alerts=False):
        """等待语音发送模式选择页面加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators['仅发送语音'])
            )
            return True
        except:
            return False


    @TestLogger.log()
    def wait_for_audio_allow_page_load(self, timeout=4, auto_accept_alerts=False):
        """等待语音权限申请允许弹窗页面加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators['要允许 和飞信 录制音频吗？'])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_allow(self):
        """点击允许"""
        self.click_element(self.__class__.__locators["允许"], auto_accept_permission_alert=False)

    @TestLogger.log()
    def click_only_voice(self):
        """点击仅发送语音"""
        self.click_element(self.__class__.__locators["仅发送语音"])



    @TestLogger.log()
    def get_audio_and_text_icon_selected(self):
        """获取语音+文字模式的选项selected状态"""
        return self.get_element(self.__class__.__locators["语音+文字选项"]).get_attribute("selected")

    @TestLogger.log()
    def click_i_know(self):
        """点击我知道了"""
        self.click_element(self.__class__.__locators["我知道了"])

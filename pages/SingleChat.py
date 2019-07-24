from appium.webdriver.common.mobileby import MobileBy
from library.core.TestLogger import TestLogger
from pages.components.BaseChat import BaseChatPage
import time


class SingleChatPage(BaseChatPage):
    """单聊会话页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity'

    __locators = {'': (MobileBy.ID, ''),
                  '聊天列表': (MobileBy.XPATH,
                           '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell'),

                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
                  '标题': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther'),
                  '打电话图标': (MobileBy.ACCESSIBILITY_ID, 'cc chat message call normal'),
                  '设置': (MobileBy.ACCESSIBILITY_ID, 'cc chat message site normal'),
                  'com.chinasofti.rcs:id/view_line': (MobileBy.ID, 'com.chinasofti.rcs:id/view_line'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/message_editor_layout': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/message_editor_layout'),
                  'com.chinasofti.rcs:id/rv_message_chat': (MobileBy.ID, 'com.chinasofti.rcs:id/rv_message_chat'),
                  'com.chinasofti.rcs:id/linearLayout': (MobileBy.ID, 'com.chinasofti.rcs:id/linearLayout'),
                  '10:57': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_time'),
                  'com.chinasofti.rcs:id/ll_msg': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_msg'),
                  'com.chinasofti.rcs:id/iv_file_icon': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_file_icon'),
                  '67.0KB': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_size'),
                  '和飞信测试用例.xlsx': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_name'),
                  'com.chinasofti.rcs:id/img_message_down_file': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/img_message_down_file'),
                  '对方离线，已提醒': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_has_read'),
                  'com.chinasofti.rcs:id/iv_send_status': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_send_status'),
                  'com.chinasofti.rcs:id/imgae_fl': (MobileBy.ID, 'com.chinasofti.rcs:id/imgae_fl'),
                  'com.chinasofti.rcs:id/layout_loading': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_loading'),
                  'com.chinasofti.rcs:id/imageview_msg_image': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_image'),
                  'hello': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
                  'com.chinasofti.rcs:id/svd_head': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
                  '选择短信': (MobileBy.IOS_PREDICATE, "name == 'ic chat message n'"),
                  '语音消息体': (MobileBy.ID, 'com.chinasofti.rcs:id/img_audio_play_icon'),
                  '消息图片': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_image'),
                  '消息视频': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_video_time'),
                  '选择照片': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_gallery_normal"'),
                  '短信发送按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'),
                  '短信输入框': (MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'),
                  '短信资费提醒': (MobileBy.XPATH, '//*[@text="资费提醒"]'),
                  "文本输入框": (MobileBy.XPATH, "//*[@type='XCUIElementTypeTextView']"),
                  "文本发送按钮": (MobileBy.ID, "cc chat send normal@2x"),
                  "消息免打扰图标": (MobileBy.ID, "com.chinasofti.rcs:id/iv_slient"),
                  '重发按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_send_failed'),
                  '确定': (MobileBy.IOS_PREDICATE, 'name == "确定"'),
                  '取消': (MobileBy.IOS_PREDICATE, 'name == "取消"'),
                  '文件名称': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_name'),
                  '语音按钮': (MobileBy.IOS_PREDICATE, 'name == "cc chat voice normal@3x"'),
                  '语音发送按钮': (MobileBy.IOS_PREDICATE, 'name == "发送"'),
                  '富媒体拍照': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_camera_normal"'),
                  '关闭GIF按钮': (MobileBy.IOS_PREDICATE, 'name == "cc chat gif close"'),
                  'GIF按钮': (MobileBy.IOS_PREDICATE, 'name == "{gif"'),
                  '表情按钮': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_icon_emoji_normal"'),
                  '视频播放按钮': (MobileBy.IOS_PREDICATE, 'name == "cc chat play@3x"'),
                  '更多加号按钮': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_ic_input_more"'),
                  '选择名片': (MobileBy.IOS_PREDICATE, 'name == "cc_chat_input_ic_business"'),
                  'gif图片': (MobileBy.XPATH,
                            '//*[@name="cc chat gif close"]/../following-sibling::*[1]/XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeImage'),
                  '最后一条文本消息': (MobileBy.XPATH,
                               "//XCUIElementTypeTable/XCUIElementTypeCell[last()]/XCUIElementTypeOther/XCUIElementTypeImage/XCUIElementTypeOther"),
                  }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待单聊会话页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["打电话图标"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)
        return self

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在单聊会话页面"""
        el = self.get_elements(self.__locators['打电话图标'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def click_add_button(self):
        """点击更多加号按钮"""
        self.click_element(self.__class__.__locators["更多加号按钮"])

    @TestLogger.log()
    def click_profile(self):
        """点击选择名片"""
        self.click_element(self.__class__.__locators["选择名片"])

    @TestLogger.log()
    def is_first_message_content(self, text):
        """获取第一条聊天记录文本中是否包含输入的内容"""
        el = self.get_element(self.__class__.__locators["第一条聊天记录"])
        if text in el.text:
            return True
        else:
            return False

    @TestLogger.log()
    def press_and_move_right_approval(self):
        """长按审批消息"""
        time.sleep(2)
        element = (MobileBy.IOS_PREDICATE, 'name CONTAINS "审批"')
        self.swipe_by_direction(element, 'right')
        time.sleep(2)

    @TestLogger.log('判断消息记录是否存在消息记录')
    def is_element_present_message(self):
        return self._is_element_present(self.__class__.__locators['聊天列表'])

    @TestLogger.log()
    def press_and_move_right_daily_log(self):
        """长按日志消息"""
        time.sleep(2)
        element = (MobileBy.IOS_PREDICATE, 'name CONTAINS "日报"')
        self.swipe_by_direction(element, 'right', duration=2)
        time.sleep(2)




    @TestLogger.log()
    def press_last_message(self, duration, text):
        """长按最后一条消息并选择转发删除撤回等"""
        self.swipe_by_direction(self.__class__.__locators["最后一条文本消息"], "press", duration)
        self.click_element((MobileBy.IOS_PREDICATE, "name CONTAINS '{}'".format(text)))

    @TestLogger.log()
    def press_video_play(self, duration, text):
        """长按聊天界面中的视频播放按钮并选择转发删除撤回等"""
        self.swipe_by_direction(self.__class__.__locators["视频播放按钮"], "press", duration)
        self.click_element((MobileBy.IOS_PREDICATE, "name CONTAINS '{}'".format(text)))

    @TestLogger.log()
    def click_voice_button(self):
        """点击语音按钮"""
        self.click_element(self.__class__.__locators["语音按钮"])

    @TestLogger.log()
    def click_send_voice(self):
        """点击发送语音录制"""
        self.click_element(self.__class__.__locators["语音发送按钮"])

    @TestLogger.log()
    def click_send_gif(self):
        """点击发送GIF图片"""
        self.click_element(self.__class__.__locators["gif图片"])

    @TestLogger.log()
    def click_take_picture(self):
        """点击选择富媒体拍照"""
        self.click_element(self.__class__.__locators["富媒体拍照"])

    @TestLogger.log()
    def click_expression_button(self):
        """点击表情按钮"""
        self.click_element(self.__class__.__locators["表情按钮"])

    @TestLogger.log()
    def click_gif_button(self):
        """点击GIF按钮"""
        self.click_element(self.__class__.__locators["GIF按钮"])

    @TestLogger.log()
    def is_exist_closegif_page(self):
        """是否存在关闭GIF按钮"""
        return self._is_element_present(self.__class__.__locators["关闭GIF按钮"])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_sms(self):
        """点击选择短信"""
        self.click_element(self.__class__.__locators["选择短信"])

    @TestLogger.log()
    def click_setting(self):
        """点击 设置"""
        self.click_element(self.__class__.__locators['设置'])

    @TestLogger.log()
    def is_audio_exist(self):
        """是否存在语音消息"""
        return self._is_element_present(self.__class__.__locators['语音消息体'])

    def is_exist_msg_videos(self):
        """当前页面是否有发视频消息"""
        el = self.get_elements(self.__class__.__locators['消息视频'])
        return len(el) > 0

    def is_exist_msg_image(self):
        """当前页面是否有发图片消息"""
        el = self.get_elements(self.__class__.__locators['消息图片'])
        return len(el) > 0

    @TestLogger.log()
    def click_picture(self):
        """点击选择照片"""
        self.click_element(self.__class__.__locators["选择照片"])

    @TestLogger.log()
    def is_exist_forward(self):
        """是否存在消息已转发"""
        return self.is_toast_exist("已转发")

    @TestLogger.log()
    def is_enabled_sms_send_btn(self):
        """短信发送按钮是否可点击"""
        return self._is_enabled(self.__class__.__locators['短信发送按钮'])

    @TestLogger.log()
    def input_sms_message(self, message):
        """输入短信信息"""
        self.input_text(self.__class__.__locators["短信输入框"], message)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def send_sms(self):
        """发送短信"""
        self.click_element(self.__class__.__locators["短信发送按钮"])
        time.sleep(1)

    @TestLogger.log()
    def is_present_sms_fee_remind(self, timeout=3, auto_accept_alerts=True):
        """是否出现短信资费提醒窗"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["短信资费提醒"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def input_text_message(self, message):
        """输入文本信息"""
        self.input_text(self.__class__.__locators["文本输入框"], message)
        # try:
        #     self.driver.hide_keyboard()
        # except:
        #     pass
        # return self

    @TestLogger.log()
    def send_text(self):
        """发送文本"""
        self.click_element(self.__class__.__locators["文本发送按钮"])
        time.sleep(1)

    def is_exist_send_button(self):
        """是否存在发送文本"""
        return self._is_element_present(self.__class__.__locators["文本发送按钮"])

    def is_exist_voice_button(self):
        """是否存在发送文本"""
        return self._is_element_present(self.__class__.__locators["语音按钮"])

    @TestLogger.log()
    def is_exist_no_disturb_icon(self):
        """是否存在消息免打扰图标"""
        return self._is_element_present(self.__class__.__locators["消息免打扰图标"])

    @TestLogger.log()
    def is_exist_file_by_type(self, file_type):
        """是否存在指定类型文件"""
        locator = (
            MobileBy.XPATH,
            '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and contains(@text,"%s")]' % file_type)
        return self._is_element_present(locator)

    @TestLogger.log()
    def is_exist_msg_send_failed_button(self):
        """是否存在重发按钮"""
        return self._is_element_present(self.__class__.__locators["重发按钮"])

    @TestLogger.log()
    def click_msg_send_failed_button(self, number):
        """点击重发按钮"""
        if self._is_element_present(self.__class__.__locators['重发按钮']):
            els = self.get_elements(self.__class__.__locators["重发按钮"])
            els[number].click()

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log()
    def click_cancel(self):
        """点击取消"""
        self.click_element(self.__class__.__locators["取消"])

    @TestLogger.log()
    def get_current_file_name(self):
        """获取刚刚发送的文件名称"""
        els = self.get_elements(self.__class__.__locators["文件名称"])
        file_name = els[-1].text
        return file_name

    @TestLogger.log("确认短信弹框页面是否有两个按键")
    def check_cmcc_msg_two_button(self):
        btn_list = [('id','com.chinasofti.rcs:id/sure_btn'),('id','com.chinasofti.rcs:id/cancle_btn')]
        for btn in btn_list:
            if not self._is_enabled(btn):
                return False
        return True
    @TestLogger.log()
    def click_action_call(self):
        """点击打电话图标"""
        self.click_element(self.__class__.__locators["打电话图标"])

    def swipe_hide_keyboard(self):
        """滑动收起键盘"""
        self.swipe_by_percent_on_screen(50, 60, 50, 10)

    @TestLogger.log()
    def press_file_by_type(self, file_type, index=-1):
        """长按指定类型文件，默认选择最后一个"""
        locator = (MobileBy.IOS_PREDICATE, 'name ENDSWITH "%s"' % file_type)
        self.swipe_by_direction2(locator, "press", index, 5)

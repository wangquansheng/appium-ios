from appium.webdriver.common.mobileby import MobileBy

from library.core.TestLogger import TestLogger
from pages.components.BaseChat import BaseChatPage


class LabelGroupingChatPage(BaseChatPage):
    """标签分组会话页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity'

    __locators = {'': (MobileBy.ACCESSIBILITY_ID, ''),

                  '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
                  '多方通话': (MobileBy.ACCESSIBILITY_ID, 'cc chat message groupcall norm'),
                  '设置': (MobileBy.ACCESSIBILITY_ID, 'cc chat message site normal'),

                  '照片': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_gallery_normal"'),
                  '拍照': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_camera_normal"'),
                  '文件': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_icon_file_normal"'),
                  '表情': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_icon_emoji_normal"'),
                  '更多': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_ic_input_more"'),
                  '名片': (MobileBy.ACCESSIBILITY_ID, 'cc_chat_input_ic_business'),
                  '位置': (MobileBy.ACCESSIBILITY_ID, 'cc_chat_input_ic_position'),
                  '红包': (MobileBy.ACCESSIBILITY_ID, 'cc_chat_input_ic_bag'),
                  '取消更多': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_ic_input_close"'),

                  '信息': (MobileBy.ACCESSIBILITY_ID, 'ic chat message n'),
                  '语音': (MobileBy.ACCESSIBILITY_ID, 'cc chat voice normal@3x'),
                  '说点什么': (MobileBy.XPATH,
                           '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeTextView'),
                  '发送按钮': (MobileBy.ACCESSIBILITY_ID, 'cc chat send normal@3x'),
                  '播放视频': (MobileBy.ACCESSIBILITY_ID, 'cc chat play@3x'),
                  '重新发送':(MobileBy.IOS_PREDICATE,'name CONTAINS "cc chat again send normal"'),

                    #
                  '': (MobileBy.ACCESSIBILITY_ID, ''),
                  '': (MobileBy.ACCESSIBILITY_ID, ''),
                  '': (MobileBy.ACCESSIBILITY_ID, ''),
                  '': (MobileBy.ACCESSIBILITY_ID, ''),



                    '刚刚': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_time'),
                  'com.chinasofti.rcs:id/ll': (MobileBy.ID, 'com.chinasofti.rcs:id/ll'),
                  '你好': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
                    '说点什么...': (MobileBy.ID, 'com.chinasofti.rcs:id/et_message'),
                  'com.chinasofti.rcs:id/ib_expression': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_expression'),
                  'com.chinasofti.rcs:id/ib_audio': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_audio'),
                  "文件名": (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_name'),
                  # 消息长按弹窗
                  '收藏': (MobileBy.XPATH, "//*[contains(@text, '收藏')]"),
                  '转发': (MobileBy.XPATH, "//*[contains(@text, '转发')]"),
                  '撤回': (MobileBy.XPATH, "//*[contains(@text, '撤回')]"),
                  '删除': (MobileBy.XPATH, "//*[contains(@text, '删除')]"),
                  '复制': (MobileBy.XPATH, "//*[contains(@text, '复制')]"),
                  '多选': (MobileBy.XPATH, "//*[contains(@text, '多选')]"),
                  }

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在标签分组聊天页"""
        el = self.get_elements(self.__locators['多方通话'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待标签分组会话页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["多方通话"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_back(self):
        """点击返回按钮"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log('点击返回')
    def is_exit_element(self,text='多方通话'):
        return self._is_element_present(self.__locators[text])

    @TestLogger.log('输入消息文本')
    def input_message_text(self, content):
        self.input_text(self.__locators['说点什么'], content)


    @TestLogger.log('点击发送按钮')
    def click_send_button(self):
        self.click_element(self.__locators['发送按钮'])


    @TestLogger.log('重新发送是否存在')
    def is_element_present_resend(self):
        return self._is_element_present(self.__locators['重新发送'])

    @TestLogger.log('点击文件')
    def click_file(self):
        self.click_element(self.__class__.__locators['文件'])

    @TestLogger.log('点击文件')
    def click_file(self):
        self.click_element(self.__class__.__locators['文件'])


    @TestLogger.log('点击设置进入分组联系人页面')
    def click_setting(self):
        self.click_element(self.__class__.__locators['设置'])

    @TestLogger.log('点击设置进入分组联系人页面')
    def select_group_contact_by_name(self,name):
        locator=(MobileBy.ACCESSIBILITY_ID,'%s' % name)
        self.click_element(locator)





    @TestLogger.log()
    def get_label_name(self):
        """获取标题名称"""
        el = self.get_element(self.__locators["lab2"])
        return el.text

    @TestLogger.log('文件是否存在')
    def is_element_present_file(self):
        return self._is_element_present(self.__locators['文件名'])

    @TestLogger.log()
    def press_file(self):
        """长按文件"""
        el = self.get_element(self.__class__.__locators['文件名'])
        self.press(el)

    @TestLogger.log()
    def press_last_file(self):
        """长按最后一个文件"""
        el = self.get_elements(self.__class__.__locators['文件名'])[-1]
        self.press(el)



    @TestLogger.log("删除当前分组发送的文件")
    def delete_group_all_file(self):
        msg_file = self.get_elements(('id', 'com.chinasofti.rcs:id/ll_msg'))
        if msg_file:
            for file in msg_file:
                self.press(file)
                self.click_element(self.__class__.__locators['删除'])
        else:
            raise AssertionError('当前窗口没有可以删除的消息')

    @TestLogger.log("撤回当前分组发送的文件")
    def recall_group_all_file(self):
        msg_file = self.get_elements(('id', 'com.chinasofti.rcs:id/ll_msg'))
        if msg_file:
            for file in msg_file:
                self.press(file)
                self.click_element(self.__class__.__locators['撤回'])
        else:
            raise AssertionError('当前窗口没有可以撤回的消息')

    @TestLogger.log()
    def get_file_name(self):
        """获取文件名称"""
        el = self.get_element(self.__locators["文件名"])
        return el.text

    @TestLogger.log()
    def get_one_file_name(self,type):
        """获取文件名称"""
        el = self.get_element(self.__locators["文件名"],type)
        return el.text
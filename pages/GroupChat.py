import traceback

from appium.webdriver.common.mobileby import MobileBy
from library.core.TestLogger import TestLogger
from pages.components.BaseChat import BaseChatPage
import time


# noinspection PyBroadException
class GroupChatPage(BaseChatPage):
    """群聊天页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity'

    __locators = {'': (MobileBy.ACCESSIBILITY_ID, ''),
                  '说点什么': (MobileBy.XPATH, '//XCUIElementTypeOther[3]/XCUIElementTypeTextView'),
                  '聊天列表': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell'),
                  '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),

                  '消息免打扰': (MobileBy.ACCESSIBILITY_ID, 'chat_list_nodisturb'),
                  '多方通话': (MobileBy.ACCESSIBILITY_ID, 'cc chat message groupcall norm'),
                  '设置': (MobileBy.IOS_PREDICATE, 'name == "cc chat message site normal"'),
                  '删除群成员确定按钮': (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="确定(1)"])[2]'),
                  '添加群成员按钮': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_groupchat_add_normal"'),
                  '删除群成员按钮': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_groupchat_delete_normal"'),
                  '添加群成员确定按钮': (MobileBy.IOS_PREDICATE, 'name CONTAINS "确定"'),
                  '图片元素数量': (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeImage"'),
                  '群消息免打扰按钮': (MobileBy.XPATH, '//XCUIElementTypeSwitch[@name="群消息免打扰"]'),
                  '群名称': (MobileBy.IOS_PREDICATE, 'name == "群名称"'),
                  '群管理': (MobileBy.IOS_PREDICATE, 'name == "群管理"'),
                  '解散群': (MobileBy.IOS_PREDICATE, 'name == "解散群"'),
                  '解散按钮': (MobileBy.IOS_PREDICATE, 'name == "解散"'),
                  '我的群昵称': (MobileBy.IOS_PREDICATE, 'name == "我的群昵称"'),
                  '我的群昵称输入框': (MobileBy.XPATH, '//XCUIElementTypeOther/XCUIElementTypeTextField'),
                  '修改群名称输入框': (MobileBy.IOS_PREDICATE, 'type == "XCUIElementTypeTextField"'),
                  '修改群名称完成按钮': (MobileBy.IOS_PREDICATE, 'name == "完成"'),
                  '选择手机联系人': (MobileBy.IOS_PREDICATE, 'name == "选择手机联系人"'),
                  '修改群名称清除文本按钮': (MobileBy.IOS_PREDICATE, 'name == "清除文本"'),

                  '14:58': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_time'),
                  'frank': (MobileBy.ID, 'com.chinasofti.rcs:id/text_name'),
                  '[呲牙1]': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
                  'com.chinasofti.rcs:id/svd_head': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
                  '呵呵': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
                  'mobile0489': (MobileBy.ID, 'com.chinasofti.rcs:id/text_name'),
                  'APP test': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
                  '选择名片': (MobileBy.IOS_PREDICATE, 'name == "cc_chat_input_ic_business"'),
                  '更多': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'),
                  '文件发送成功标志': (MobileBy.ID, 'com.chinasofti.rcs:id/img_message_down_file'),
                  '选择照片': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_gallery_normal"'),
                  '富媒体拍照': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_camera_normal"'),
                  '发送失败标识': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_send_failed'),
                  '消息图片': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_image'),
                  '消息视频': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_video_time'),
                  '收藏': (MobileBy.XPATH, "//*[contains(@text, '收藏')]"),
                  '转发': (MobileBy.XPATH, "//*[contains(@text, '转发')]"),
                  '删除': (MobileBy.XPATH, "//*[contains(@text, '删除')]"),
                  '撤回': (MobileBy.XPATH, "//*[contains(@text, '撤回')]"),
                  '多选': (MobileBy.XPATH, "//*[contains(@text, '多选')]"),
                  '复制': (MobileBy.XPATH, "//*[contains(@text, '复制')]"),
                  '收藏_c': (MobileBy.IOS_PREDICATE, "name=='收藏'"),
                  '转发_c': (MobileBy.IOS_PREDICATE, "name=='转发'"),
                  '删除_c': (MobileBy.IOS_PREDICATE, "name=='删除'"),
                  '撤回_c': (MobileBy.IOS_PREDICATE, "name=='撤回'"),
                  '多选_c': (MobileBy.IOS_PREDICATE, "name=='多选'"),
                  '复制_c': (MobileBy.IOS_PREDICATE, "name=='复制'"),
                  '我知道了': (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_btn_ok'),
                  '勾': (MobileBy.ID, 'com.chinasofti.rcs:id/img_message_down_file'),
                  '重发按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_send_failed'),
                  '重发消息确定': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
                  '语音消息体': (MobileBy.ID, 'com.chinasofti.rcs:id/img_audio_play_icon'),
                  '位置返回': (MobileBy.ID, 'com.chinasofti.rcs:id/location_back_btn'),
                  '表情按钮': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_icon_emoji_normal"'),
                  '微笑表情': (MobileBy.IOS_PREDICATE, 'name == "{awx"'),
                  '窃喜表情': (MobileBy.IOS_PREDICATE, 'name == "{aqx"'),
                  '流鼻涕表情': (MobileBy.IOS_PREDICATE, 'name == "{albt"'),
                  '更多加号按钮': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_ic_input_more"'),
                  '更多关闭按钮': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_ic_input_close"'),
                  '语音按钮': (MobileBy.IOS_PREDICATE, 'name contains "cc chat voice normal"'),
                  '退出按钮': (MobileBy.IOS_PREDICATE, 'name == "退出"'),
                  '发送按钮': (MobileBy.IOS_PREDICATE, 'name contains "cc chat send normal"'),
                  'GIF按钮': (MobileBy.IOS_PREDICATE, 'name == "{gif"'),
                  'gif图片': (MobileBy.XPATH,
                             '//*[@name="cc chat gif close"]/../following-sibling::*[1]/XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeImage'),
                  '关闭GIF按钮': (MobileBy.IOS_PREDICATE, 'name == "cc chat gif close"'),
                  '文件按钮': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_icon_file_normal"'),
                  '表情页': (MobileBy.ID, 'com.chinasofti.rcs:id/gv_expression'),
                  '表情': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_expression_image'),
                  '输入框': (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeTextView"'),
                  '视频播放按钮': (MobileBy.IOS_PREDICATE, 'name contains "cc chat play"'),
                  '关闭表情页': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_expression_keyboard'),
                  '多选返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'),
                  '多选计数': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_count'),
                  '多选选择框': (MobileBy.ID, 'com.chinasofti.rcs:id/multi_check'),
                  '多选删除': (MobileBy.ID, 'com.chinasofti.rcs:id/multi_btn_delete'),
                  '多选转发': (MobileBy.ID, 'com.chinasofti.rcs:id/multi_btn_forward'),
                  '删除已选信息': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
                  '取消删除已选信息': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                  "返回上一级": (MobileBy.ID, "com.chinasofti.rcs:id/left_back"),
                  "文本发送按钮": (MobileBy.ID, "com.chinasofti.rcs:id/ib_send"),
                  "语音小红点": (MobileBy.ID, "com.chinasofti.rcs:id/ib_record_red_dot"),
                  "粘贴": (MobileBy.ID, "com.chinasofti.rcs:id/ib_pic"),
                  "照片选择框": (MobileBy.ID, "com.chinasofti.rcs:id/iv_select"),
                  "更多小红点": (MobileBy.ID, "com.chinasofti.rcs:id/id_more_red_dot"),
                  "预览文件_返回": (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  '预览文件_更多': (MobileBy.ID, 'com.chinasofti.rcs:id/menu'),
                  '定位_地图': ('id', 'com.chinasofti.rcs:id/location_info_view'),
                  '始终允许': (MobileBy.XPATH, "//*[contains(@text, '始终允许')]"),
                  '小键盘麦克标志': (MobileBy.IOS_PREDICATE, 'name == "dictation"'),
                  '文本消息': (MobileBy.XPATH,
                           "//XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeImage/XCUIElementTypeOther"),
                  '最后一条文本消息': (MobileBy.XPATH,
                               "//XCUIElementTypeTable/XCUIElementTypeCell[last()]/XCUIElementTypeOther/XCUIElementTypeImage/XCUIElementTypeOther"),
                  '最后一条文本消息_c': (MobileBy.XPATH, "//XCUIElementTypeTable[1]/XCUIElementTypeCell[last()]"),
                  '消息记录': (MobileBy.XPATH, '//XCUIElementTypeTable/XCUIElementTypeCell'),
                  '最后一条表情消息的表情': (MobileBy.XPATH,
                               '(//XCUIElementTypeTable/XCUIElementTypeCell[last()]/XCUIElementTypeOther/XCUIElementTypeImage/XCUIElementTypeOther/XCUIElementTypeImage[@name])[last()]'),
                  '最后一条消息记录发送失败标识': (MobileBy.XPATH,
                                     '//XCUIElementTypeTable/XCUIElementTypeCell[last()]/XCUIElementTypeButton[contains(@name,"cc chat again send normal")]'),
                  '最后一条消息记录已读动态': (MobileBy.XPATH, '//XCUIElementTypeTable/XCUIElementTypeCell[last()]/XCUIElementTypeButton[not(@name)]'),
                  '多选关闭按钮': (MobileBy.IOS_PREDICATE, 'name=="cc chat checkbox close"'),
                  '多选删除按钮': (MobileBy.IOS_PREDICATE, 'name=="cc chat checkbox delete normal"'),
                  '多选转发按钮': (MobileBy.IOS_PREDICATE, 'name=="cc chat checkbox forward norma"'),
                  '已选择': (MobileBy.IOS_PREDICATE, 'name=="已选择"'),
                  '未选择': (MobileBy.IOS_PREDICATE, 'name=="未选择"'),
                  '已选择数量': (MobileBy.XPATH, '//*[@name="已选择"]/following-sibling::XCUIElementTypeStaticText[1]'),
                  '多选最后一条消息勾选框': (
                      MobileBy.XPATH, '//XCUIElementTypeTable/XCUIElementTypeCell[last()]/XCUIElementTypeButton[2]'),
                  '群短信': (MobileBy.ACCESSIBILITY_ID, 'cc_chat_input_ic_groupmassage'),
                  '群人数文本': (MobileBy.XPATH,
                          '//*[@name="back"]/../following-sibling::XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeStaticText[2]'),
                  '我的电脑-聊天记录': (MobileBy.XPATH,
                            '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeImage[1]/XCUIElementTypeOther'),
                  }

    @TestLogger.log()
    def make_sure_chatwindow_have_message(self, content='文本消息', times=1):
        """确保当前页面有文本消息记录"""
        if self.is_element_present_message():
            time.sleep(3)
        else:
            while times > 0:
                times = times - 1
                self.click_input_box()
                self.input_message_text(content)
                self.click_send_button()
                self.click_input_box()
                self.input_message_text(content)
                self.click_send_button()
                time.sleep(2)

    @TestLogger.log()
    def click_start_call_button(self):
        """点击开始呼叫按钮 """
        self.click_element((MobileBy.IOS_PREDICATE, 'name CONTAINS "呼叫"'))


    @TestLogger.log('点击输入框')
    def click_input_box(self):
        self.click_element(self.__locators['说点什么'])

    @TestLogger.log('输入消息文本')
    def input_message_text(self, content):
        """输入消息文本(清空之前文本框的文本)"""
        self.input_text(self.__locators['说点什么'], content)

    @TestLogger.log('输入消息文本')
    def input_message_text2(self, content):
        """输入消息文本--不清空之前文本框的文本"""
        self.input_text2(self.__locators['说点什么'], content)


    @TestLogger.log()
    def long_press_input_box(self):
        """长按输入框(备注：群聊使用该方法需要发送两条文本消息)"""
        self.swipe_by_direction(self.__class__.__locators['说点什么'], 'press',duration=2)
        time.sleep(2)



    @TestLogger.log('点击发送按钮')
    def click_send_button(self):
        self.click_element(self.__locators['发送按钮'])

    @TestLogger.log()
    def select_members_by_name(self, name='大佬1'):
        """通过名字选择成员"""
        locator = (MobileBy.ACCESSIBILITY_ID, '%s' % name)
        self.click_element(locator)

    @TestLogger.log()
    def get_input_message(self):
        """获取输入框的信息"""
        el = self.get_element(self.__class__.__locators["说点什么"])
        return el.text

    @TestLogger.log('发送多条文本消息')
    def send_mutiple_message(self, text='文本消息', times=15):
        while times > 0:
            times = times - 1
            self.click_input_box()
            self.input_message_text(text)
            self.click_send_button()
            time.sleep(2)


    @TestLogger.log()
    def click_send_slide_up(self, duration=5):
        """点击发送按钮并向上滑动"""
        el = self.get_element(self.__class__.__locators["发送按钮"])
        rect = el.rect
        left, right = int(rect['x']) + 1, int(rect['x'] + rect['width']) - 1
        top, bottom = int(rect['y']) + 1, int(rect['y'] + rect['height']) - 1
        x_start = (left + right) // 2
        x_end = (left + right) // 2
        y_start = bottom
        y_end = top - 200
        self.driver.execute_script("mobile:dragFromToForDuration",
                                   {"duration": duration, "element": None, "fromX": x_start,
                                    "fromY": y_start,
                                    "toX": x_end, "toY": y_end})

    @TestLogger.log()
    def click_send_slide_down(self, duration=5):
        """点击发送按钮并向下滑动"""
        el = self.get_element(self.__class__.__locators["发送按钮"])
        rect = el.rect
        left, right = int(rect['x']) + 1, int(rect['x'] + rect['width']) - 1
        top, bottom = int(rect['y']) + 1, int(rect['y'] + rect['height']) - 1
        x_start = (left + right) // 2
        x_end = (left + right) // 2
        y_start = top
        y_end = bottom + 200
        self.driver.execute_script("mobile:dragFromToForDuration",
                                   {"duration": duration, "element": None, "fromX": x_start,
                                    "fromY": y_start,
                                    "toX": x_end, "toY": y_end})

    @TestLogger.log()
    def get_width_of_last_msg(self):
        """获取最后一条文本信息框的大小"""
        el = self.get_element(self.__class__.__locators["最后一条文本消息"])
        rect = el.rect
        return rect["width"]

    @TestLogger.log()
    def get_height_of_last_msg(self):
        """获取最后一条文本信息框的大小"""
        el = self.get_element(self.__class__.__locators["最后一条文本消息"])
        rect = el.rect
        return rect["height"]

    @TestLogger.log()
    def click_exit_voice(self):
        """点击退出语音录制"""
        self.click_element(self.__class__.__locators["退出按钮"])

    @TestLogger.log()
    def is_exist_video_play_button(self):
        """是否存在视频播放按钮"""
        return self._is_element_present(self.__class__.__locators["视频播放按钮"])

    def is_exist_msg_dictation(self):
        """当前页面是否有小键盘麦克"""
        el = self.get_elements(self.__locators['小键盘麦克标志'])
        return len(el) > 0

    @TestLogger.log('判断消息记录是否存在消息记录')
    def is_element_present_message(self):
        return self._is_element_present(self.__class__.__locators['聊天列表'])

    @TestLogger.log()
    def click_message_approval(self):
        """点击审批内容"""
        self.click_element((MobileBy.IOS_PREDICATE, 'name CONTAINS "审批"'))

    @TestLogger.log()
    def press_and_move_right_approval(self):
        """长按审批消息"""
        time.sleep(2)
        element = (MobileBy.IOS_PREDICATE, 'name CONTAINS "审批"')
        self.swipe_by_direction(element, 'right')
        time.sleep(2)

    @TestLogger.log()
    def press_and_move_right_daily_log(self):
        """长按日志消息"""
        time.sleep(2)
        element = (MobileBy.IOS_PREDICATE, 'name CONTAINS "日报"')
        self.swipe_by_direction(element, 'right', duration=2)
        time.sleep(2)

    @TestLogger.log()
    def press_and_move_right_text_message(self):
        """长按文本消息(备注：群聊使用该方法需要发送两条文本消息)"""
        time.sleep(2)
        locator = (MobileBy.XPATH, "//XCUIElementTypeCell[last()]/XCUIElementTypeOther/XCUIElementTypeImage/XCUIElementTypeOther")
        self.swipe_by_direction(locator, 'left')
        time.sleep(2)


    def is_exist_msg_videos(self):
        """当前页面是否有发视频消息"""
        el = self.get_elements(self.__locators['消息视频'])
        return len(el) > 0

    def is_exist_msg_image(self):
        """当前页面是否有发图片消息"""
        el = self.get_elements(self.__locators['消息图片'])
        return len(el) > 0

    @TestLogger.log()
    def click_msg_image(self, number):
        """点击图片消息"""
        els = self.get_elements(self.__class__.__locators["消息图片"])
        els[number].click()

    @TestLogger.log()
    def is_exists_group_by_name(self, name):
        """是否存在指定群聊名"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/title" and contains(@text, "%s")]' % name)
        return self._is_element_present(locator)

    @TestLogger.log()
    def is_exist_collection(self):
        """是否存在消息已收藏"""
        return self.is_toast_exist("已收藏")

    @TestLogger.log()
    def is_exist_forward(self):
        """是否存在消息已转发"""
        return self.is_toast_exist("已转发")

    @TestLogger.log()
    def click_take_picture(self):
        """点击选择富媒体拍照"""
        self.click_element(self.__class__.__locators["富媒体拍照"])

    @TestLogger.log()
    def is_send_sucess(self):
        """当前页面是否有发送失败标识"""
        el = self.get_elements(self.__locators['发送失败标识'])
        if len(el) > 0:
            return False
        return True

    @TestLogger.log()
    def click_picture(self):
        """点击选择照片"""
        self.click_element(self.__class__.__locators["选择照片"])

    @TestLogger.log()
    def click_setting(self):
        """点击设置"""
        self.click_element(self.__class__.__locators["设置"])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待群聊页面加载"""
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
    def wait_for_group_control_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待群管理页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["解散群"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在群聊天页"""
        el = self.get_elements(self.__locators['多方通话'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def click_profile(self):
        """点击选择名片"""
        self.click_element(self.__class__.__locators["选择名片"])

    @TestLogger.log()
    def click_back(self):
        """点击返回按钮"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def is_exist_undisturb(self):
        """是否存在消息免打扰标志"""
        return self._is_element_present(self.__class__.__locators["消息免打扰"])


    @TestLogger.log()
    def press_file_to_do(self, file, text):
        """长按指定文件进行操作"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def press_file(self, file):
        """长按指定文件"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)

    @TestLogger.log()
    def is_address_text_present(self):
        """判断位置信息是否在群聊页面发送"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/lloc_famous_address_text'))
        if el:
            return True
        else:
            return False

    @TestLogger.log()
    def press_message_to_do(self, text):
        """长按指定信息进行操作"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/lloc_famous_address_text'))
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def wait_for_message_down_file(self, timeout=20, auto_accept_alerts=True):
        """等待消息发送成功"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["勾"])
            )
        except:
            message = "消息在{}s内，没有发送成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def is_exist_network(self):
        """是否存网络不可用"""
        return self.is_toast_exist("网络不可用，请检查网络设置")

    @TestLogger.log()
    def click_send_again(self):
        """点击重新发送gif"""
        self.click_element(self.__class__.__locators["发送失败标识"])
        self.click_element(self.__class__.__locators["重发消息确定"])

    @TestLogger.log()
    def is_exist_msg_send_failed_button(self):
        """判断是否有重发按钮"""
        el = self.get_elements(self.__locators['重发按钮'])
        return len(el) > 0

    @TestLogger.log()
    def click_msg_send_failed_button(self):
        """点击重发按钮"""
        self.click_element(self.__class__.__locators["重发按钮"])

    @TestLogger.log()
    def click_resend_confirm(self):
        """点击重发消息确定"""
        self.click_element(self.__class__.__locators["重发消息确定"])

    @TestLogger.log()
    def click_clean_video(self):
        """点击删除消息视频"""
        try:
            el = self.get_element(self.__class__.__locators["消息视频"])
            self.press(el)
            self.click_element(self.__class__.__locators["删除"])
        except:
                pass
        return self

    @TestLogger.log()
    def press_voice_message_to_do(self,text):
        """长按语言消息体"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/linearlayout_msg_content'))
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def get_width_of_msg_of_text(self):
        """获取文本信息框的大小"""
        el=self.get_element((MobileBy.ID,'com.chinasofti.rcs:id/tv_message'))
        rect=el.rect
        return rect["width"]

    @TestLogger.log()
    def is_call_page_load(self):
        """判断是否可以发起呼叫"""
        el = self.get_element((MobileBy.ID, 'com.android.incallui:id/endButton'))
        if el:
            return True
        else:
            return False

    @TestLogger.log()
    def click_end_call_button(self):
        """点击结束呼叫按钮 """
        self.click_element((MobileBy.ID, 'com.android.incallui:id/endButton'))

    @TestLogger.log()
    def click_location_back(self):
        """点击位置页面返回 """
        self.click_element(self.__class__.__locators['位置返回'])

    @TestLogger.log()
    def get_picture_nums(self):
        """获取当前页面图片元素数量"""
        els = self.get_elements(self.__class__.__locators['图片元素数量'])
        return len(els)

    @TestLogger.log()
    def click_add_member_button(self):
        """点击添加成员按钮"""
        self.click_element(self.__class__.__locators["添加群成员按钮"])

    @TestLogger.log()
    def click_delete_member_button(self):
        """删除成员按钮"""
        self.click_element(self.__class__.__locators["删除群成员按钮"])

    @TestLogger.log()
    def click_delete_member_sure_button(self):
        """删除成员确定按钮"""
        self.click_element(self.__class__.__locators["删除群成员确定按钮"])

    @TestLogger.log()
    def wait_for_page_setting_load(self, timeout=8, auto_accept_alerts=True):
        """等待群聊设置页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["添加群成员按钮"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_phone_contact(self):
        """点击选择手机联系人"""
        self.click_element(self.__class__.__locators["选择手机联系人"])

    @TestLogger.log()
    def no_disturbing_btn_is_enabled(self):
        """获取群消息免打扰按钮状态是否可点击"""
        return self._is_enabled(self.__class__.__locators["群消息免打扰按钮"])

    @TestLogger.log()
    def get_no_disturbing_btn_text(self):
        """获取群消息免打扰按钮状态"""
        if self._is_element_present2(self.__class__.__locators["群消息免打扰按钮"]):
            el = self.get_element(self.__class__.__locators["群消息免打扰按钮"])
            return el.text

    @TestLogger.log()
    def click_no_disturbing_button(self):
        """点击群消息免打扰开关"""
        self.click_element(self.__class__.__locators["群消息免打扰按钮"])

    @TestLogger.log()
    def click_group_name(self):
        """点击修改群名称按钮"""
        self.click_element(self.__class__.__locators["群名称"])

    @TestLogger.log()
    def input_group_name_message(self, message):
        """输入要修改的群名称"""
        self.input_text(self.__class__.__locators["修改群名称输入框"], message)
        return self

    @TestLogger.log()
    def click_group_name_complete(self):
        """点击修改群名称完成按钮"""
        self.click_element(self.__class__.__locators["修改群名称完成按钮"])

    @TestLogger.log()
    def click_group_control(self):
        """点击群管理按钮"""
        self.click_element(self.__class__.__locators["群管理"])

    @TestLogger.log()
    def click_group_dissolve(self):
        """点击解散群按钮"""
        self.click_element(self.__class__.__locators["解散群"])

    @TestLogger.log()
    def click_group_dissolve_confirm(self):
        """点击确认群解散按钮"""
        self.click_element(self.__class__.__locators["解散按钮"])

    @TestLogger.log()
    def click_add_member_confirm_button(self):
        """点击添加群成员确定按钮"""
        self.click_element(self.__class__.__locators["添加群成员确定按钮"])

    @TestLogger.log()
    def click_voice_button(self):
        """点击语音按钮"""
        self.click_element(self.__class__.__locators["语音按钮"])

    @TestLogger.log()
    def is_exist_voice_button(self):
        """是否存在语音按钮"""
        return self._is_element_present2(self.__class__.__locators["语音按钮"])

    @TestLogger.log()
    def click_send_button(self):
        """点击发送按钮"""
        self.click_element(self.__class__.__locators["发送按钮"])

    @TestLogger.log()
    def _is_enabled_send_button(self):
        """发送按钮是否可点击"""
        return self._is_enabled(self.__class__.__locators["发送按钮"])

    @TestLogger.log()
    def is_exist_send_button(self):
        """是否存在发送按钮"""
        return self._is_element_present2(self.__class__.__locators["发送按钮"])

    @TestLogger.log()
    def click_add_button(self):
        """点击更多加号按钮"""
        self.click_element(self.__class__.__locators["更多加号按钮"])

    @TestLogger.log()
    def click_file_button(self):
        """点击文件按钮"""
        self.click_element(self.__class__.__locators["文件按钮"])

    @TestLogger.log()
    def is_exist_file_button(self):
        """是否存在文件按钮"""
        return self._is_element_present(self.__class__.__locators["文件按钮"])

    @TestLogger.log()
    def click_expression_button(self):
        """点击表情按钮"""
        self.click_element(self.__class__.__locators["表情按钮"])

    @TestLogger.log()
    def click_expression_wx(self):
        """点击微笑表情"""
        self.click_element(self.__class__.__locators["微笑表情"])

    @TestLogger.log()
    def click_expression_qx(self):
        """点击窃喜表情"""
        self.click_element(self.__class__.__locators["窃喜表情"])

    @TestLogger.log()
    def click_expression_lbt(self):
        """点击流鼻涕表情"""
        self.click_element(self.__class__.__locators["流鼻涕表情"])

    @TestLogger.log()
    def click_gif_button(self):
        """点击GIF按钮"""
        self.click_element(self.__class__.__locators["GIF按钮"])

    @TestLogger.log()
    def is_exists_gif_button(self):
        """是否存在GIF按钮"""
        return self._is_element_present2(self.__class__.__locators["GIF按钮"])

    @TestLogger.log()
    def click_send_gif(self):
        """点击发送GIF图片"""
        self.click_element(self.__class__.__locators["gif图片"])

    @TestLogger.log()
    def is_exist_close_gif(self):
        """是否存在关闭GIF按钮"""
        return self._is_element_present(self.__class__.__locators["关闭GIF按钮"])

    @TestLogger.log()
    def click_close_gif(self):
        """点击关闭GIF按钮"""
        self.click_element(self.__class__.__locators["关闭GIF按钮"])

    @TestLogger.log()
    def is_exist_expression_page(self):
        """是否存在表情页"""
        return self._is_element_present(self.__class__.__locators["表情页"])

    @TestLogger.log()
    def click_expression_page_close_button(self):
        """点击表情页关闭"""
        self.click_element(self.__class__.__locators["关闭表情页"])

    @TestLogger.log()
    def get_expressions(self):
        """获取表情包"""
        els = self.get_elements(self.__locators['表情'])
        return els

    @TestLogger.log()
    def get_input_box(self):
        """获取输入框"""
        el = self.get_element(self.__locators['输入框'])
        return el

    @TestLogger.log()
    def is_enabled_of_send_button(self):
        """发送按钮状态"""
        flag = self._is_enabled((MobileBy.ID, 'com.chinasofti.rcs:id/ib_send'))
        return flag

    @TestLogger.log()
    def is_exist_multiple_selection_back(self):
        """是否存在多选【×】关闭按钮"""
        return self._is_element_present(self.__class__.__locators["多选返回"])

    @TestLogger.log()
    def is_exist_multiple_selection_count(self):
        """是否存在多选计数"""
        return self._is_element_present(self.__class__.__locators["多选计数"])

    @TestLogger.log()
    def get_multiple_selection_select_box(self):
        """获取多选选择框"""
        els=self.get_elements(self.__class__.__locators["多选选择框"])
        if els:
            return els
        else:
            raise AssertionError("没有找到多选选择框")

    @TestLogger.log()
    def is_enabled_multiple_selection_delete(self):
        """判断多选删除是否高亮展示"""
        return self._is_enabled(self.__class__.__locators["多选删除"])

    @TestLogger.log()
    def is_enabled_multiple_selection_forward(self):
        """判断多选转发是否高亮展示"""
        return self._is_enabled(self.__class__.__locators["多选转发"])

    @TestLogger.log()
    def click_multiple_selection_back(self):
        """点击多选返回"""
        self.click_element(self.__class__.__locators["多选返回"])

    @TestLogger.log()
    def is_exist_multiple_selection_select_box(self):
        """是否存在多选选择框"""
        return self._is_element_present(self.__class__.__locators["多选选择框"])

    @TestLogger.log()
    def click_multiple_selection_delete(self):
        """点击多选删除"""
        self.click_element(self.__class__.__locators["多选删除"])

    @TestLogger.log()
    def click_multiple_selection_delete_cancel(self):
        """点击取消删除已选信息"""
        self.click_element(self.__class__.__locators["取消删除已选信息"])

    @TestLogger.log()
    def click_multiple_selection_delete_sure(self):
        """点击确定删除已选信息"""
        self.click_element(self.__class__.__locators["删除已选信息"])

    @TestLogger.log()
    def click_multiple_selection_forward(self):
        """点击多选转发"""
        self.click_element(self.__class__.__locators["多选转发"])

    @TestLogger.log()
    def press_audio_to_do(self,text):
        """长按语音消息体进行操作"""
        els = self.get_elements(self.__class__.__locators["语音消息体"])
        if els:
            self.press(els[0])
            self.click_element(self.__class__.__locators[text])
        else:
            raise AssertionError("没有找到语音消息体")

    @TestLogger.log()
    def get_group_name(self):
        """在群聊页面获取群聊名称"""
        return self.get_element(self.__class__.__locators['群聊001(2)']).text

    @TestLogger.log()
    def get_multiple_selection_count(self):
        """获取多选计数框"""
        el = self.get_element(self.__class__.__locators["多选计数"])
        if el:
            return el
        else:
            raise AssertionError("没有找到多选选择框")

    @TestLogger.log()
    def press_voice_message(self):
        """长按语言消息体"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/linearlayout_msg_content'))
        self.press(el)

    @TestLogger.log()
    def click_return(self):
        """返回上一级"""
        self.click_element(self.__class__.__locators["返回上一级"])

    @TestLogger.log()
    def get_height_of_msg_of_text(self):
        """获取文本信息框的大小"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'))
        rect = el.rect
        return rect["height"]

    @TestLogger.log()
    def get_msg_of_text(self):
        """获取文本信息框的信息"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'))
        text = el.text
        return text

    @TestLogger.log()
    def input_text_message(self, message):
        """输入文本信息"""
        self.input_text(self.__class__.__locators["输入框"], message)
        return self

    @TestLogger.log()
    def send_text(self):
        """发送文本"""
        self.click_element(self.__class__.__locators["文本发送按钮"])
        time.sleep(1)

    @TestLogger.log()
    def is_exist_red_dot(self):
        """是否存在语音小红点"""
        return self._is_element_present(self.__class__.__locators["语音小红点"])

    @TestLogger.log()
    def click_long_copy_message(self):
        """输入文本信息"""
        self.click_element(self.__locators["输入框"])
        el = self.get_element(self.__locators["输入框"])
        self.press(el)
        time.sleep(1.8)
        self.click_element(self.__locators["粘贴"])

    @TestLogger.log()
    def click_long_message(self):
        """输入文本信息"""
        el = self.get_elements(self.__locators["呵呵"])
        el = el[-1]
        el.click()

    @TestLogger.log()
    def click_mutilcall(self):
        """点击多方通话"""
        self.click_element(self.__class__.__locators["多方通话"])

    @TestLogger.log()
    def select_picture(self):
        """选择照片"""
        self.click_element(self.__class__.__locators["照片选择框"])


    @TestLogger.log("文件是否发送成功")
    def check_message_resend_success(self):
        return self._is_element_present(self.__class__.__locators['文件发送成功标志'])


    @TestLogger.log("当前页面是否有发文件消息")
    def is_exist_msg_file(self):
        el = self.get_elements(('id', 'com.chinasofti.rcs:id/ll_msg'))
        return len(el) > 0

    @TestLogger.log("删除当前群聊发送的文件")
    def delete_group_all_file(self):
        msg_file = self.get_elements(('id', 'com.chinasofti.rcs:id/ll_msg'))
        if msg_file:
            for file in msg_file:
                self.press(file)
                self.click_element(self.__class__.__locators['删除'])
        else:
            print('当前窗口没有可以删除的消息')

    @TestLogger.log("撤回文件")
    def recall_file(self, file):
        el = self.wait_until(condition=lambda x:self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file)))
        self.press(el)
        self.click_element(self.__class__.__locators['撤回'])

    @TestLogger.log("点击发送的最后的文件")
    def click_last_file_send_fail(self):
        ele_list = self.get_elements(('id', 'com.chinasofti.rcs:id/ll_msg'))
        ele_list[-1].click()

    @TestLogger.log("点击预览文件返回")
    def click_file_back(self):
        self.click_element(self.__locators['预览文件_返回'])

    @TestLogger.log("预览文件里的更多按钮是否存在")
    def is_exist_more_button(self):
        return self.wait_until(condition=lambda x:self._is_element_present(self.__locators['预览文件_更多']))

    @TestLogger.log("点击预览文件里的更多按钮")
    def click_more_button(self):
        self.click_element(self.__locators['预览文件_更多'])

    @TestLogger.log("检查预览文件选项是否可用")
    def check_options_is_enable(self):
        text_list = ['转发', '收藏', '其他应用打开']
        for text in text_list:
            if not self._is_enabled(('xpath', '//*[contains(@text, "{}")]'.format(text))):
                return False
        return True

    @TestLogger.log("当前页面是否有发地图消息")
    def is_exist_loc_msg(self):
        el = self.get_elements(self.__locators['定位_地图'])
        return len(el) > 0

    @TestLogger.log("撤回文件")
    def recall_file(self, file):
        el = self.wait_until(condition=lambda x:self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file)))
        self.press(el)
        self.click_element(self.__class__.__locators['撤回'])

    @TestLogger.log("撤回位置消息")
    def recall_loc_msg(self):
        el = self.wait_until(
            condition=lambda x: self.get_elements(self.__locators['定位_地图']))
        self.press(el[-1])
        self.click_element(self.__class__.__locators['撤回'])

    @TestLogger.log()
    def is_element_exit_(self, text):
        """指定元素是否存在"""
        return self._is_element_present(self.__class__.__locators[text])

    @TestLogger.log()
    def click_element_(self, text):
        """点击元素"""
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def click_text_message_by_number(self, index=0):
        """点击某一条文本消息"""
        els = self.get_elements(self.__class__.__locators["文本消息"])
        els[index].click()

    @TestLogger.log()
    def click_last_text_message(self):
        """点击最后一条文本消息"""
        self.click_element(self.__class__.__locators["最后一条文本消息"])

    @TestLogger.log()
    def press_last_text_message(self):
        """长按最后一条文本消息"""
        self.swipe_by_direction(self.__class__.__locators["最后一条文本消息"], "press", 5)

    @TestLogger.log()
    def press_last_text_message_c(self):
        """长按最后一条文本消息"""
        self.swipe_by_direction(self.__class__.__locators["最后一条文本消息_c"], "press", 5)

    @TestLogger.log()
    def is_clear_the_input_box(self):
        """输入框是否清空"""
        if self._is_element_present2(self.__class__.__locators['输入框']):
            el = self.get_element(self.__class__.__locators['输入框'])
            text = el.text
            if text is None:
                return True
            else:
                return False

    @TestLogger.log()
    def is_exists_text_by_input_box(self, text):
        """输入框中是否存在指定文本"""
        if self._is_element_present2(self.__class__.__locators['输入框']):
            el = self.get_element(self.__class__.__locators['输入框'])
            message_text = el.text
            if text in message_text:
                return True
            else:
                return False

    @TestLogger.log()
    def get_message_record_number(self):
        """获取消息记录数量"""
        if self._is_element_present2(self.__class__.__locators['消息记录']):
            els = self.get_elements(self.__class__.__locators['消息记录'])
            return len(els)
        else:
            return 0

    @TestLogger.log()
    def get_size_of_last_expression_message(self):
        """获取最后一条表情消息表情的大小"""
        if self._is_element_present2(self.__class__.__locators['最后一条表情消息的表情']):
            el = self.get_element(self.__class__.__locators["最后一条表情消息的表情"])
            rect = el.rect
            return rect["width"], rect["height"]

    @TestLogger.log()
    def press_file_by_type(self, file_type, index=-1):
        """长按指定类型文件，默认选择最后一个"""
        locator = (MobileBy.IOS_PREDICATE, 'name ENDSWITH "%s"' % file_type)
        self.swipe_by_direction2(locator, "press", index, 5)

    @TestLogger.log()
    def click_delete_text(self):
        """修改群名称清除文本"""
        self.click_element(self.__class__.__locators["修改群名称清除文本按钮"])

    @TestLogger.log()
    def delete_text_button_is_enabled(self):
        """清除文本按钮是否可点击"""
        return self._is_clickable(self.__class__.__locators['修改群名称清除文本按钮'])

    @TestLogger.log()
    def is_exists_element_by_text(self, text):
        """是否存在指定元素"""
        return self._is_element_present2(self.__class__.__locators[text])



    @TestLogger.log()
    def is_enabled_element_by_text(self, text):
        """指定元素是否可点击"""
        return self._is_enabled(self.__class__.__locators[text])

    @TestLogger.log()
    def click_element_by_text(self, text):
        """点击指定元素"""
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def get_element_value_by_text(self, text):
        """获取指定元素的文本"""
        if self._is_element_present2(self.__class__.__locators[text]):
            el = self.get_element(self.__class__.__locators[text])
            return el.text

    @TestLogger.log()
    def click_my_group_name(self):
        """点击我的群昵称"""
        self.click_element(self.__class__.__locators["我的群昵称"])

    @TestLogger.log()
    def get_group_name_text(self):
        """获取修改我的群昵称输入框文本"""
        text = self.get_element(self.__class__.__locators["我的群昵称输入框"]).text
        return text

    @TestLogger.log()
    def is_exists_group_member_name(self, name):
        """最后一条消息是否存在群成员昵称"""
        locator = (
            MobileBy.XPATH,
            '//XCUIElementTypeTable/XCUIElementTypeCell[last()]/XCUIElementTypeStaticText[@name="%s"]' % name)
        return self._is_element_present2(locator)

    @TestLogger.log()
    def click_group_message(self):
        """点击群短信"""
        self.click_element(self.__class__.__locators["群短信"])

    @TestLogger.log()
    def is_element_exit_c(self, locator):
        """指定元素是否存在"""
        try:
            if len(self.get_elements(self.__class__.__locators[locator])) > 0:
                return True
            else:
                return False
        except Exception:
            return False

    @TestLogger.log('获取控件文本')
    def get_element_text(self, locator):
        return self.get_text(self.__class__.__locators[locator])

    @TestLogger.log()
    def press_element_by_text(self, text):
        """长按指定元素"""
        if self._is_element_present2(self.__class__.__locators[text]):
            self.swipe_by_direction(self.__class__.__locators[text], "press", 5)

    @TestLogger.log()
    def press_element_by_text2(self, text, index=-1):
        """长按指定元素，默认选择最后一个"""
        if self._is_element_present2(self.__class__.__locators[text]):
            self.swipe_by_direction2(self.__class__.__locators[text], "press", index, 5)

    @TestLogger.log('判断消息记录是否存在消息记录')
    def is_element_present_mess(self):
        return self._is_element_present(self.__class__.__locators['我的电脑-聊天记录'])
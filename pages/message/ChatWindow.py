from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.chat.ChatSelectFile import ChatSelectFilePage
from pages.components import ChatNoticeDialog
from pages.components.selectors import PictureSelector
from pages.components.BaseChat import BaseChatPage
import time


class ChatWindowPage(ChatNoticeDialog, PictureSelector, BaseChatPage, BasePage):
    """聊天窗口"""
    ACTIVITY = 'com.cmicc.module_message.ui.activity.MessageDetailActivity'

    __locators = {
        '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
        '消息免打扰图标': (MobileBy.ACCESSIBILITY_ID, 'chat_list_nodisturb'),
        # 单聊页面
        '标题': (MobileBy.XPATH,
               '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]'),
        '通话图标': (MobileBy.ACCESSIBILITY_ID, 'cc chat message call normal'),
        '群聊-通话图标': (MobileBy.ACCESSIBILITY_ID, 'cc chat message groupcall norm'),
        '设置': (MobileBy.ACCESSIBILITY_ID, 'cc chat message site normal'),

        '照片': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_gallery_normal"'),
        '拍照': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_camera_normal"'),
        '文件': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_icon_file_normal"'),
        '表情': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_icon_emoji_normal"'),
        '更多': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_chat_ic_input_more"'),

        '信息': (MobileBy.ACCESSIBILITY_ID, 'ic chat message n'),
        '语音': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc chat voice normal"'),
        '说点什么': (MobileBy.XPATH,
                 '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeTextView'),
        '发送按钮': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc chat send normal"'),
        '播放视频': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc chat play"'),

        # 发送消息列表
        '消息列表': (MobileBy.XPATH,
                 '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeImage[1]'),

        '已发送文件列表': (MobileBy.XPATH,
                    '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell'),
        '已发送位置列表': (MobileBy.XPATH,
                    '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell'),
        '已发送名片消息列表': (MobileBy.XPATH,
                      '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell'),
        '已发送网页消息列表': (MobileBy.XPATH,
                      '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeImage[1]'),
        '接收到的网页消息': (MobileBy.XPATH,
                     '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypeImage[2]'),

        '收到新消息分割线': (MobileBy.XPATH,
                     '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[26]/XCUIElementTypeOther'),

        "已读动态": (MobileBy.XPATH,
                 '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeButton'),
        '未进群提示': (MobileBy.XPATH,
                  '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[2]/XCUIElementTypeOther'),
        '还有人未进群，再次邀请': (MobileBy.XPATH,
                        '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[2]/XCUIElementTypeOther'),
        '非和飞信用户提醒': (MobileBy.XPATH,
                     '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[2]/XCUIElementTypeOther'),
        # 再次邀请页面
        '再次邀请': (MobileBy.ACCESSIBILITY_ID, '再次邀请'),

        # 更多选项
        '飞信电话': (MobileBy.ACCESSIBILITY_ID, 'cc_chat_input_ic_hefeixin'),
        '音视频通话': (MobileBy.ACCESSIBILITY_ID, 'cc_chat_input_ic_video'),
        '名片': (MobileBy.ACCESSIBILITY_ID, 'cc_chat_input_ic_business'),
        '位置': (MobileBy.ACCESSIBILITY_ID, 'cc_chat_input_ic_position'),
        '红包': (MobileBy.ACCESSIBILITY_ID, 'cc_chat_input_ic_bag'),
        # 预览文件页面
        '预览文件标题': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
        '预览文件-更多': (MobileBy.ACCESSIBILITY_ID, 'cc chat file more normal'),
        '预览文件-转发': (MobileBy.ACCESSIBILITY_ID, "转发"),
        '预览文件-收藏': (MobileBy.ACCESSIBILITY_ID, "收藏"),
        '其他应用打开': (MobileBy.ACCESSIBILITY_ID, "其他应用打开"),
        '预览文件-取消': (MobileBy.ACCESSIBILITY_ID, "取消"),
        # 选择其他应用界面
        '选择其他应用-信息': (MobileBy.ACCESSIBILITY_ID, "信息"),
        # 网页链接界面
        '网页-返回': (MobileBy.ACCESSIBILITY_ID, "back"),
        '网页-更多': (MobileBy.ACCESSIBILITY_ID, "cc chat more normal"),
        '转发给朋友': (MobileBy.ACCESSIBILITY_ID, "转发给朋友"),
        '转发给微信好友': (MobileBy.ACCESSIBILITY_ID, "转发给微信好友"),
        '转发到朋友圈': (MobileBy.ACCESSIBILITY_ID, "转发到朋友圈"),
        '转发给QQ好友': (MobileBy.ACCESSIBILITY_ID, "转发给QQ好友"),
        '在Safari中打开': (MobileBy.ACCESSIBILITY_ID, "在Safari中打开"),
        '复制链接': (MobileBy.ACCESSIBILITY_ID, "复制链接"),
        '刷新': (MobileBy.ACCESSIBILITY_ID, "刷新"),
        # 预览视频页面

        '预览视频-取消预览': (MobileBy.IOS_PREDICATE, 'name CONTAINS "watchvideo close"'),

        # 发送语音消息页面
        '发送': (MobileBy.ACCESSIBILITY_ID, '发送'),
        '退出': (MobileBy.ACCESSIBILITY_ID, '退出'),
        '设置按钮': (MobileBy.ACCESSIBILITY_ID, '设置'),
        '按住说话': (MobileBy.ACCESSIBILITY_ID, 'chat voice talk'),
        '同时发送语音+文字（语音识别）': (MobileBy.ACCESSIBILITY_ID, '同时发送语音+文字（语音识别）'),
        '仅发送文字（语音识别）': (MobileBy.ACCESSIBILITY_ID, '仅发送文字（语音识别）'),
        '仅发送语音': (MobileBy.ACCESSIBILITY_ID, '仅发送语音'),
        '确定按钮': (MobileBy.ACCESSIBILITY_ID, '确定'),
        # 通话图标页面-弹出框
        '飞信电话(免费)': (MobileBy.ACCESSIBILITY_ID, '飞信电话(免费)'),
        '多方视频': (MobileBy.ACCESSIBILITY_ID, '多方视频'),
        '取消': (MobileBy.ACCESSIBILITY_ID, "取消"),

        'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
            MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
        'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
        '返回箭头': (MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'),
        '13537795364': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
        # '消息列表': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/rv_message_chat"]'),
        '消息根节点': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/rv_message_chat"]/*'),
        '星期三 20:50': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_time'),
        '11': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
        'com.chinasofti.rcs:id/svd_head': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
        'com.chinasofti.rcs:id/ll_sms_mark': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_sms_mark'),
        '短信': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sms_mark'),

        '我已阅读': (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="smscharge unselected"])[1]'),
        '确定': (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="确定"])[1]'),

        '取消重发': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
        '确定重发': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
        '月': (MobileBy.ID, 'android:id/numberpicker_input'),
        # 手机系统设置界面-事件与日期
        '自动时间-开关按钮': (MobileBy.ID, 'android:id/switch_widget'),
        '日期': (MobileBy.XPATH, '//*[@text="日期"]/../android.widget.TextView[@resource-id="android:id/summary"]'),
        '时间': (MobileBy.XPATH, '//*[@text="时间"]/../android.widget.TextView[@resource-id="android:id/summary"]'),

        '最后一条文本消息': (MobileBy.XPATH,
                     "//XCUIElementTypeTable/XCUIElementTypeCell[last()]/XCUIElementTypeOther/XCUIElementTypeImage/XCUIElementTypeOther"),
    }

    @TestLogger.log()
    def click_message_list(self, element='消息列表'):
        """点击消息列表"""
        self.click_element(self.__class__.__locators[element])


    @TestLogger.log()
    def press_and_move_right_web_message(self):
        """长按网页消息 默认按住最后一条网页消息"""
        locator = (MobileBy.XPATH, '//XCUIElementTypeCell[last()]/XCUIElementTypeOther/XCUIElementTypeImage/XCUIElementTypeOther')
        self.swipe_by_direction(locator, 'press', duration=3)
        time.sleep(2)

    @TestLogger.log()
    def press_and_move_right_file(self, type='.docx'):
        """长按文件(向右滑动文件长按)"""
        time.sleep(2)
        element = (MobileBy.IOS_PREDICATE, 'name ENDSWITH "%s"' % type)
        self.swipe_by_direction(element, 'right')
        time.sleep(2)

    @TestLogger.log()
    def press_and_move_right_text_message(self):
        """长按文本消息(备注：群聊使用该方法需要发送两条文本消息)"""
        time.sleep(2)
        locator = (MobileBy.XPATH, "//XCUIElementTypeCell[last()]/XCUIElementTypeOther/XCUIElementTypeImage/XCUIElementTypeOther")
        self.swipe_by_direction(locator, 'left')
        time.sleep(2)

    @TestLogger.log()
    def press_and_move_right_video(self):
        """长按视频-视频"""
        time.sleep(2)
        element = (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc chat play"')
        self.swipe_by_direction(element, 'press', 2)
        time.sleep(2)

    @TestLogger.log()
    def press_and_move_right_business_card(self):
        """长按名片-名片"""
        time.sleep(2)
        locator = (MobileBy.IOS_PREDICATE, 'name CONTAINS "个人名片"')
        self.swipe_by_direction(locator, 'right')
        time.sleep(2)

    @TestLogger.log()
    def press_and_move_right_locator(self):
        """长按位置-位置"""
        time.sleep(2)
        locator = (MobileBy.IOS_PREDICATE, 'name CONTAINS "广东省"')
        self.swipe_by_direction(locator, 'right')

    @TestLogger.log()
    def click_already_read_dynamic(self, element='已读动态'):
        """点击消息列表"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_invite_again(self, element='再次邀请'):
        """点击再次邀请"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_not_heifeixin_remind(self, element='非和飞信用户提醒'):
        """点击非和飞信用户提醒"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_group_call_icon(self, element='群聊-通话图标'):
        """点击通话图标"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_feixin_call(self, element='飞信电话(免费)'):
        """点击飞信电话（原多方通话）"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_video_call(self, element='多方视频'):
        """点击多方视频"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log('判断页面存在元素')
    def is_exist_element(self, locator='转发'):
        if self._is_element_present(self.__locators[locator]):
            return True
        else:
            return False

    @TestLogger.log()
    def click_play_video(self, element='播放视频'):
        """点击播放视频"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def wait_for_page_load_play_video(self, timeout=30, auto_accept_alerts=True):
        """等待聊天窗口加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["预览视频-取消预览"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def is_exist_no_disturb_icon(self):
        """是否存在消息免打扰图标"""
        return self._is_element_present(self.__class__.__locators["消息免打扰图标"])

    @TestLogger.log()
    def click_cancel_previer_video(self, element='预览视频-取消预览'):
        """点击取消预览视频"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log('消息列表是否存在')
    def is_element_present_message_list(self):
        return self._is_element_present(self.__locators['消息列表'])

    @TestLogger.log('查看聊天窗口右方 有人@我 是否存在')
    def is_element_present_someone_tag_me(self):
        locator = (MobileBy.ACCESSIBILITY_ID, '有人@我')
        return self._is_element_present(locator)

    @TestLogger.log('查看所有未读消息是否存在')
    def is_element_present_preview_unread_message_by_number(self, number='25'):
        locator = (MobileBy.ACCESSIBILITY_ID, '%s条新消息' % number)
        return self._is_element_present(locator)

    @TestLogger.log('点击查看所有未读消息')
    def click_preview_unread_message_by_number(self, number='25'):
        locator = (MobileBy.ACCESSIBILITY_ID, '%s条新消息' % number)
        self.click_element(locator)

    @TestLogger.log('新消息分割线是否存在')
    def is_element_present_message_split_line(self):
        return self._is_element_present(self.__locators['收到新消息分割线'])

    @TestLogger.log()
    def send_voice(self, times=1):
        """发送语音"""
        while times > 0:
            times -= 1
            self.click_voice()
            if self.is_text_present('语音录制中'):
                time.sleep(5)
                self.click_send_voice()
            else:
                # 设置成发送语音模式
                self.click_send_voice()
                self.click_voice_setting()
                self.click_send_voice_only()
                self.click_sure_icon()
                # 录制语音
                time.sleep(5)
                self.click_send_voice()
                time.sleep(2)
            # 退出录音
            self.click_exit()
            time.sleep(1)

    @TestLogger.log()
    def send_pic(self):
        """发送图片"""
        from pages import ChatPicPage
        self.click_file()
        csf = ChatSelectFilePage()
        csf.click_pic()
        select_pic = ChatPicPage()
        select_pic.click_camara_picture()
        select_pic.select_first_picture()
        select_pic.click_send()
        time.sleep(3)

    @TestLogger.log()
    def send_video(self):
        """发送视频"""
        self.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_video()
        time.sleep(2)
        csf.click_select_video()

    @TestLogger.log()
    def send_file(self, type='.docx'):
        """发送文件"""
        self.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_local_file()
        time.sleep(2)
        from pages import ChatSelectLocalFilePage
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(type)
        local_file.click_send_button()
        time.sleep(2)

    @TestLogger.log()
    def send_locator(self):
        """发送位置"""
        time.sleep(2)
        self.click_more()
        self.click_locator()
        time.sleep(2)
        # 选择位置界面
        from pages import ChatLocationPage
        locator = ChatLocationPage()
        locator.wait_for_page_load()
        locator.click_send()
        time.sleep(2)

    @TestLogger.log()
    def select_members_by_name(self, name='大佬1'):
        """通过名字选择成员"""
        locator = (MobileBy.ACCESSIBILITY_ID, '%s' % name)
        self.click_element(locator)

    @TestLogger.log('点击设置')
    def click_setting(self):
        self.click_element(self.__locators['设置'])

    @TestLogger.log()
    def get_members_nickname(self):
        """获取成员昵称"""
        locator = (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeStaticText"')
        els = self.get_elements(locator)
        return els[2].text

    @TestLogger.log('判断消息记录是否存在位置列表')
    def is_element_present_locator_list(self):
        return self._is_element_present(self.__locators['已发送位置列表'])

    @TestLogger.log()
    def click_locator_list(self, element='已发送位置列表'):
        """点击位置列表"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_business_card_list(self):
        """点击已发送名片列表"""
        locator = (MobileBy.IOS_PREDICATE, 'name CONTAINS "个人名片"')
        self.click_element(locator)

    @TestLogger.log()
    def is_element_present_card_list(self):
        """是否存在分享名片列表"""
        locator = (MobileBy.IOS_PREDICATE, 'name CONTAINS "个人名片"')
        if self._is_element_present(locator):
            return True
        else:
            return False

    @TestLogger.log('判断消息记录是否存在网页消息')
    def is_element_present_web_message(self):
        return self._is_element_present(self.__class__.__locators['已发送网页消息列表'])

    @TestLogger.log('点击网页消息')
    def click_element_web_message(self):
        """点击已发送的网页消息列表（单聊可用）"""
        self.click_element(self.__class__.__locators['已发送网页消息列表'])

    @TestLogger.log('点击网页消息')
    def click_element_received_web_message(self):
        self.click_element(self.__class__.__locators['接收到的网页消息'])

    @TestLogger.log()
    def click_more_web_message(self, element='网页-更多'):
        """点击网页-更多"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_forward_to_friend(self, element='转发给朋友'):
        """点击转发给朋友"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_forward_to_weixin(self, element='转发给微信好友'):
        """点击转发给微信好友"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_forward_to_circle_of_friend(self, element='转发到朋友圈'):
        """点击转发到朋友圈"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_forward_to_qq(self, element='转发给QQ好友'):
        """转发给QQ好友"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_forward_to_qq(self, element='转发给QQ好友'):
        """转发给QQ好友"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_open_in_Safari(self, element='在Safari中打开'):
        """在Safari中打开"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_open_in_Safari(self, element='在Safari中打开'):
        """在Safari中打开"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_copy_link(self, element='复制链接'):
        """复制链接"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_refresh(self, element='刷新'):
        """点击刷新"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def clear_all_chat_record(self):
        """点击清空所有的聊天记录"""
        from pages.SingleChatSet import SingleChatSetPage
        if self.is_element_present_by_locator(locator='消息列表'):
            self.click_setting()
            set = SingleChatSetPage()
            time.sleep(1)
            set.click_clear_local_chat_record()
            time.sleep(1)
            set.click_sure_clear_local_chat_record()
            time.sleep(3)
            set.click_back()
            time.sleep(2)

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    # @TestLogger.log()
    # def page_contain_element(self,locator='设置'):
    #     """判断页面包含元素"""
    #     self.page_should_contain_element(self.__locators[locator])

    @TestLogger.log('点击文件')
    def click_file(self):
        self.click_element(self.__class__.__locators['文件'])

    @TestLogger.log('通过文件类型点击文件记录')
    def click_file_by_type(self, file_type):
        locator = (MobileBy.IOS_PREDICATE, 'name CONTAINS "%s"' % file_type)
        self.click_element(locator)

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待聊天窗口加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["设置"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_page_load_preview_file(self, timeout=8, auto_accept_alerts=True):
        """等待预览文件页面加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["预览文件-更多"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_page_load_web_message(self, timeout=30, auto_accept_alerts=True):
        """等待网页消息页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["网页-更多"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def get_file_name(self):
        """获取最近一次文件记录的 文件名称"""
        locator = (MobileBy.XPATH, '//XCUIElementTypeCell[last()]/XCUIElementTypeStaticText[1]')
        return self.get_element(locator).text

    @TestLogger.log()
    def get_prevoew_file_name(self):
        """获取预览文件页面-文件名称"""
        locator = (MobileBy.XPATH, '//XCUIElementTypeOther/XCUIElementTypeStaticText')
        return self.get_element(locator).text

    @TestLogger.log()
    def check_is_select_others_app_visionable(self):
        """判断选择其他应用页面是否吊起"""
        self.page_should_contain_element(self.__locators['选择其他应用-信息'])

    @TestLogger.log('点击我已阅读')
    def click_already_read(self):
        """点击我已阅读"""
        self.click_element(self.__locators['我已阅读'])

    @TestLogger.log('点击确定')
    def click_sure_icon(self):
        """点击确定"""
        self.click_element(self.__locators['确定按钮'])

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在聊天窗口页面"""

        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["设置"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def is_on_this_page_preview_file(self):
        """当前页面是否在预览文件"""

        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["预览文件-更多"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def is_on_this_page_web_message(self):
        """当前页面是否在网页消息页面"""

        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["网页-更多"])
            )
            return True
        except:
            return False

    @TestLogger.log('点击输入框')
    def click_input_box(self):
        self.click_element(self.__locators['说点什么'])

    @TestLogger.log('输入消息文本')
    def input_message_text(self, content):
        self.input_text(self.__locators['说点什么'], content)

    @TestLogger.log('点击发送按钮')
    def click_send_button(self):
        self.click_element(self.__locators['发送按钮'])

    @TestLogger.log()
    def get_input_message(self):
        """获取输入框的信息"""
        el = self.get_element(self.__class__.__locators["说点什么"])
        return el.text

    @TestLogger.log('发送多条文本消息')
    def send_mutiple_message(self, content='文本消息', times=15):
        while times > 0:
            times = times - 1
            self.click_input_box()
            self.input_message_text(content)
            self.click_send_button()
            time.sleep(2)

    @TestLogger.log()
    def make_sure_chatwindow_have_message(self, content='文本消息', times=1):
        """确保当前页面有文本消息记录"""
        if self.is_element_present_message_list():
            time.sleep(3)
        else:
            while times > 0:
                times = times - 1
                self.click_input_box()
                self.input_message_text(content)
                self.click_send_button()
                time.sleep(2)

    @TestLogger.log()
    def swipe_month(self, text, number):
        max_try = 30
        current = 0
        while current < max_try:
            time.sleep(1)
            new_text = self.get_elements(self.__class__.__locators["月"])[number].text
            if new_text == text:
                break
            current += 1
            self.swipe_by_direction2(self.__class__.__locators["月"], "up", number, 700)

    # @TestLogger.log('发送消息')
    # def send_message(self, content):
    #     self.input_message_text(content)
    #     self.click_send_button()

    @TestLogger.log('发送图片')
    def send_img_msgs(self, name_order_mapper):
        """
        发送图片、视频消息
        :return:
        """
        self.click_element(self.__locators['照片'])
        self.select_and_send_in_img_selector(name_order_mapper)

    @TestLogger.log('检查是否收到期望的消息内容')
    def assert_message_content_display(self, content, max_wait_time=5):
        try:
            self.wait_until(
                lambda d: self.is_text_present(content),
                timeout=max_wait_time
            )
        except TimeoutException:
            raise AssertionError('聊天界面没有收到消息：{}'.format(content))

    @TestLogger.log('获取消息发送状态')
    def get_msg_status(self, msg, most_recent_index=1):
        """
        获取消息的发送状态，如：
            1、加载中
            2、已发送
            3、发送失败
        如果传入的是定位器，默认寻找最新一条消息，没有则抛出 NoSuchElementException 异常
        :param msg: 消息（必须传入消息根节点元素或者元素的定位器）
        :param most_recent_index: 消息在列表中的序号，从消息列表底部往上数，从1开始计数
        :return:
        """
        if not isinstance(msg, WebElement):
            msgs = self.get_elements(msg)
            if msgs:
                msg = msgs[-most_recent_index]
            else:
                raise NoSuchElementException('找不到元素：{}'.format(msg))
        # 找加载中
        if msg.find_elements('xpath', '//*[@resource-id="com.chinasofti.rcs:id/progress_send_small"]'):
            return '加载中'
        elif msg.find_elements('xpath', '//*[@resource-id="com.chinasofti.rcs:id/imageview_msg_send_failed"]'):
            return '发送失败'
        else:
            return '发送成功'

    @TestLogger.log('等待消息在指定时间内状态变为“加载中”、“发送失败”、“发送成功”中的一种')
    def wait_for_msg_send_status_become_to(self, expected, max_wait_time=3, most_recent_index=1):
        self.wait_until(
            condition=lambda d: self.get_msg_status(msg=self.__locators['消息根节点'],
                                                    most_recent_index=most_recent_index) == expected,
            timeout=max_wait_time
        )

    @TestLogger.log()
    def click_resend_button(self):
        """点击重新发送"""
        self.click_element(self.__locators['重新发送'])

    @TestLogger.log('点击确定重发')
    def click_resend_sure(self):
        self.click_element(self.__locators['确定重发'])

    @TestLogger.log('点击取消重发')
    def click_resend_not(self):
        self.click_element(self.__locators['取消重发'])

    @TestLogger.log()
    def get_label_name(self):
        """获取标题名称"""
        el = self.get_element(self.__locators["13537795364"])
        return el.text

    @TestLogger.log()
    def find_element_by_swipe(self, locator, times=15):
        """找不到元素就滑动"""
        if self._is_element_present(locator):
            return self.get_element(locator)
        else:
            c = 0
            while c < times:
                self.page_up()
                if self._is_element_present(locator):
                    return self.get_element(locator)
                c += 1
            return None

    @TestLogger.log()
    def is_address_text_present(self):
        """判断位置信息是否在聊天页面发送"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/lloc_famous_address_text'))
        if el:
            return True
        else:
            return False




    TestLogger.log("开启或关闭")
    def swich_automatic_time(self, flag=True):
        time.sleep(1)
        bool = self.is_selected(self.__locators["自动时间-开关按钮"])
        if not bool and flag:
            # 打开
            self.click_element(self.__locators["自动时间-开关按钮"])
        elif bool and not flag:
            # 关闭
            self.click_element(self.__locators["自动时间-开关按钮"])
        else:
            print(bool)
            print("找不到开关")

    @TestLogger.log('点击设置界面-日期')
    def click_date_in_setting(self):
        self.click_element(self.__locators['日期'])

    @TestLogger.log('点击设置界面-时间')
    def click_time_in_setting(self):
        self.click_element(self.__locators['时间'])

    def long_press_last_text_message(self):
        self.swipe_by_direction(self.__locators['最新一条消息'], 'press', 5)

    @TestLogger.log()
    def press_last_text_message(self):
        """长按最后一条文本消息"""
        self.swipe_by_direction(self.__class__.__locators["最后一条文本消息"], "press", 5)

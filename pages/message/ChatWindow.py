from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components import ChatNoticeDialog
from pages.components.selectors import PictureSelector
from pages.components.BaseChat import BaseChatPage
import time


class ChatWindowPage(ChatNoticeDialog, PictureSelector, BaseChatPage,BasePage):
    """聊天窗口"""
    ACTIVITY = 'com.cmicc.module_message.ui.activity.MessageDetailActivity'

    __locators = {
        '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
        #单聊页面
        '标题': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]'),
        '通话图标': (MobileBy.ACCESSIBILITY_ID, 'cc chat message call normal'),
        '设置': (MobileBy.ACCESSIBILITY_ID, 'cc chat message site normal'),
        '照片': (MobileBy.ACCESSIBILITY_ID, '/var/containers/Bundle/Application/D2DC6C77-35DD-4A89-B9E9-624930C97BF1/AndFetion.app/cc_chat_gallery_normal@3x.png'),
        '拍照': (MobileBy.ACCESSIBILITY_ID, '/var/containers/Bundle/Application/D2DC6C77-35DD-4A89-B9E9-624930C97BF1/AndFetion.app/cc_chat_camera_normal@3x.png'),
        '文件': (MobileBy.ACCESSIBILITY_ID, '/var/containers/Bundle/Application/D2DC6C77-35DD-4A89-B9E9-624930C97BF1/AndFetion.app/cc_chat_icon_file_normal@3x.png'),
        '表情': (MobileBy.ACCESSIBILITY_ID, '/var/containers/Bundle/Application/D2DC6C77-35DD-4A89-B9E9-624930C97BF1/AndFetion.app/cc_chat_icon_emoji_normal@3x.png'),
        '更多': (MobileBy.ACCESSIBILITY_ID, '/var/containers/Bundle/Application/D2DC6C77-35DD-4A89-B9E9-624930C97BF1/AndFetion.app/cc_chat_ic_input_more@3x.png'),
        '信息': (MobileBy.ACCESSIBILITY_ID, 'ic chat message n'),
        '语音': (MobileBy.ACCESSIBILITY_ID, 'cc chat voice normal@3x'),
        '说点什么': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeTextView'),
        '发送按钮': (MobileBy.ACCESSIBILITY_ID, 'cc chat send normal@3x'),
        #更多选项
        '飞信电话': (MobileBy.ACCESSIBILITY_ID, 'cc_chat_input_ic_hefeixin'),
        '音视频通话': (MobileBy.ACCESSIBILITY_ID, 'cc_chat_input_ic_video'),
        '名片': (MobileBy.ACCESSIBILITY_ID, 'cc_chat_input_ic_business'),
        '位置': (MobileBy.ACCESSIBILITY_ID, 'cc_chat_input_ic_position'),

        '红包': (MobileBy.ACCESSIBILITY_ID, 'cc_chat_input_ic_bag'),


        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
            MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
        'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
        '返回箭头': (MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'),
        '13537795364': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
        'com.chinasofti.rcs:id/action_call': (MobileBy.ID, 'com.chinasofti.rcs:id/action_call'),
        'com.chinasofti.rcs:id/view_line': (MobileBy.ID, 'com.chinasofti.rcs:id/view_line'),
        'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
        'com.chinasofti.rcs:id/message_editor_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/message_editor_layout'),
        '消息列表': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/rv_message_chat"]'),
        '消息根节点': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/rv_message_chat"]/*'),
        '星期三 20:50': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_time'),
        '11': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
        'com.chinasofti.rcs:id/svd_head': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
        'com.chinasofti.rcs:id/ll_sms_mark': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_sms_mark'),
        '短信': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sms_mark'),
        'com.chinasofti.rcs:id/iv_bkg': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_bkg'),
        'com.chinasofti.rcs:id/input_and_menu': (MobileBy.ID, 'com.chinasofti.rcs:id/input_and_menu'),
        'com.chinasofti.rcs:id/ll_text_input': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_text_input'),
        'com.chinasofti.rcs:id/layout_for_message': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_for_message'),
        'com.chinasofti.rcs:id/ll_rich_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_rich_panel'),

        'GIF': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_gif'),
        'com.chinasofti.rcs:id/input_divider_inside': (MobileBy.ID, 'com.chinasofti.rcs:id/input_divider_inside'),
        'com.chinasofti.rcs:id/input_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/input_layout'),
        'com.chinasofti.rcs:id/fl_edit_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/fl_edit_panel'),
        'com.chinasofti.rcs:id/ib_expression': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_expression'),
        'com.chinasofti.rcs:id/ib_audio': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_audio'),
        'com.chinasofti.rcs:id/ib_record_red_dot': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_record_red_dot'),
        'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),

        '我已阅读': (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="smscharge unselected"])[1]'),
        '确定': (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="确定"])[1]'),

        '重新发送': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_send_failed'),
        '取消重发': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
        '确定重发': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
        '月': (MobileBy.ID, 'android:id/numberpicker_input'),
        #预览文件页面
        '预览文件标题': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
        '预览文件-更多': (MobileBy.ACCESSIBILITY_ID, 'cc chat file more normal'),
        '预览文件-转发': (MobileBy.ACCESSIBILITY_ID, "转发"),
        '预览文件-收藏': (MobileBy.ACCESSIBILITY_ID, "收藏"),
        '其他应用打开': (MobileBy.ACCESSIBILITY_ID, "其他应用打开"),
        '预览文件-取消': (MobileBy.ACCESSIBILITY_ID, "取消"),
        #选择其他应用界面
        '选择其他应用-信息': (MobileBy.ACCESSIBILITY_ID, "信息"),
        #手机系统设置界面-事件与日期
        '自动时间-开关按钮': (MobileBy.ID, 'android:id/switch_widget'),
        '日期': (MobileBy.XPATH, '//*[@text="日期"]/../android.widget.TextView[@resource-id="android:id/summary"]'),
        '时间': (MobileBy.XPATH, '//*[@text="时间"]/../android.widget.TextView[@resource-id="android:id/summary"]'),

    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log()
    def page_contain_element(self,locator='设置'):
        """判断页面包含元素"""
        self.page_should_contain_element(self.__locators[locator])


    @TestLogger.log('点击文件')
    def click_file(self):
        self.click_element(self.__class__.__locators['文件'])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
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
    def get_file_name(self):
        """获取最近一次文件记录的 文件名称"""
        locator=(MobileBy.XPATH, '//XCUIElementTypeCell/XCUIElementTypeStaticText[3]')
        return self.get_element(locator).text


    @TestLogger.log()
    def get_prevoew_file_name(self):
        """获取预览文件页面-文件名称"""
        locator=(MobileBy.XPATH, '//XCUIElementTypeOther/XCUIElementTypeStaticText')
        return self.get_element(locator).text

    @TestLogger.log('点击我已阅读')
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
        self.click_element(self.__locators['确定'])

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在通讯录"""

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



    @TestLogger.log('点击设置')
    def click_setting(self):
        self.click_element(self.__locators['设置'])


    @TestLogger.log('输入消息文本')
    def input_message_text(self, content):
        self.input_text(self.__locators['说点什么'], content)

    @TestLogger.log('点击发送按钮')
    def click_send_button(self):
        self.click_element(self.__locators['发送按钮'])

    @TestLogger.log('发送消息')
    def send_message(self, content):
        self.input_message_text(content)
        self.click_send_button()

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

    @TestLogger.log('重新发送是否存在')
    def is_element_present_resend(self):
        return self._is_element_present(self.__locators['重新发送'])

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
    def swich_automatic_time(self,flag=True):
        time.sleep(1)
        bool=self.is_selected(self.__locators["自动时间-开关按钮"])
        if not bool and flag:
            #打开
            self.click_element(self.__locators["自动时间-开关按钮"])
        elif bool and  not flag:
            #关闭
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


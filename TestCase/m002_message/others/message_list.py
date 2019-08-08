import random
import re
import time
import unittest
import uuid
import warnings

from appium.webdriver.common.mobileby import MobileBy

import preconditions
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, switch_to_mobile, current_driver
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components import BaseChatPage
from pages.groupset.GroupChatSetPicVideo import GroupChatSetPicVideoPage

from preconditions.BasePreconditions import LoginPreconditions

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    # 'Android-移动': 'single_mobile',
    'IOS-移动': 'iphone',
    'Android-电信': 'single_telecom',
    'Android-联通': 'single_union',
    'Android-移动-联通': 'mobile_and_union',
    'Android-移动-电信': '',
    'Android-移动-移动': 'double_mobile',
    'Android-XX-XX': 'others_double',
}


class Preconditions(LoginPreconditions):
    """前置条件"""

    @staticmethod
    def connect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

    @staticmethod
    def disconnect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(category)
        client.disconnect_mobile()
        return client


    @staticmethod
    def create_contacts(name, number):
        """
        导入联系人数据
        :param name:
        :param number:
        :return:
        """
        contacts_page = ContactsPage()
        detail_page = ContactDetailsPage()
        try:
            contacts_page.wait_for_page_load()
            contacts_page.open_contacts_page()
        except:
            Preconditions.make_already_in_message_page(reset=False)
            contacts_page.open_contacts_page()
        # 创建联系人
        contacts_page.click_search_box()
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword(name)
        contact_search.click_back()
        contacts_page.click_add()
        create_page = CreateContactPage()
        create_page.hide_keyboard_if_display()
        create_page.create_contact(name, number)
        detail_page.wait_for_page_load()
        detail_page.click_back_icon()

    @staticmethod
    def take_logout_operation_if_already_login():
        """已登录状态，执行登出操作"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()

        me = MePage()
        me.scroll_to_bottom()
        me.scroll_to_bottom()
        me.scroll_to_bottom()
        me.click_setting_menu()

        setting = SettingPage()
        setting.scroll_to_bottom()
        setting.click_logout()
        setting.click_ok_of_alert()

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""
        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def terminate_app():
        """
        强制关闭app,退出后台
        :return:
        """
        app_id = current_driver().desired_capability['appPackage']
        current_mobile().termiate_app(app_id)

    @staticmethod
    def background_app():
        """后台运行"""
        current_mobile().press_home_key()

    @staticmethod
    def activate_app(app_id=None):
        """激活APP"""
        if not app_id:
            app_id = current_mobile().driver.desired_capabilities['appPackage']
        current_mobile().driver.activate_app(app_id)

    @staticmethod
    def create_contacts_if_not_exits(name, number):
        """
        不存在就导入联系人数据
        :param name:
        :param number:
        :return:
        """
        contacts_page = ContactsPage()
        detail_page = ContactDetailsPage()
        try:
            contacts_page.wait_for_page_load()
            contacts_page.open_contacts_page()
        except:
            Preconditions.make_already_in_message_page(reset=False)
            contacts_page.open_contacts_page()
        # 创建联系人
        contacts_page.click_phone_contact()
        contacts_page.click_search_phone_contact()
        contacts_page.input_search_keyword(name)
        if contacts_page.is_contact_in_list():
            contacts_page.click_back()
        else:
            contacts_page.click_add()
            create_page = CreateContactPage()
            create_page.create_contact(name, number)
            time.sleep(2)
            detail_page.click_back_icon()
            contacts_page.click_back()

    @staticmethod
    def enter_single_chat_page(name):
        """进入单聊聊天会话页面"""
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击“新建消息”
        mp.click_new_message()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 进入单聊会话页面
        slc.selecting_local_contacts_by_name(name)
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            # 点击我已阅读
            bcp.click_i_have_read()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    # @staticmethod
    # def make_sure_it_have_message_list():
    #     if MessagePage().is_element_present(text='消息列表1'):
    #         time.sleep(2)
    #     else:
    #         mes=MessagePage()
    #         mes.click_search_box()
    #         time.sleep(1)
    #         mes.input_search_text('大佬1')
    #         time.sleep(2)
    #         mes.click_search_local_contact()
    #         detail=ContactDetailsPage()
    #         detail.click_message_icon()
    #         ChatWindowPage()


class MessageListText(TestCase):
    """消息列表页面"""

    def default_setUp(self):

        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_B_0003(self):
        """消息列表进入"""
        mes=MessagePage()
        #切换到联系页面
        mes.open_contacts_page()
        ContactsPage().is_on_this_page()
        time.sleep(2)
        #切换到消息页面
        ContactsPage().click_message_icon()
        mes.is_on_this_page()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_B_0004(self):
        """登录之后消息列表进入"""

        # 重启客户端
        current_mobile().launch_app()
        mp = MessagePage()
        # 1.登录客户端,等待消息列表页面加载
        mp.wait_for_page_load()
        time.sleep(2)
        # 2.底部消息图标是否高亮显示
        self.assertEquals(mp.message_icon_is_visiable(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_B_0006(self):
        """消息列表进入到会话页面"""
        msg= MessagePage()
        msg.delete_all_message_list()
        time.sleep(2)
        msg.make_sure_message_list_have_record()
        msg.click_msg_first_list()
        time.sleep(2)
        self.assertTrue(ChatWindowPage().is_on_this_page())
        #点击返回 返回到消息列表
        ChatWindowPage().click_back()
        msg.is_on_this_page()

    @tags('ALL', 'CMCC', 'msg')
    def test_msg_xiaoliping_B_0007(self):
        """消息列表消息单条删除"""
        # 1、联网正常
        # 2、已登录客户端
        # 3、当前在消息列表页面
        # Step: 1、选择消息列表任意一个消息（消息类型为会话消息、通知类消息（139邮箱助手、短信等））左滑，点击删除
        msg = MessagePage()
        Preconditions.enter_single_chat_page("大佬1")
        scp = SingleChatPage()
        text = "hello"
        # 收起键盘
        msg.swipe_by_percent_on_screen(50, 60, 50, 10)
        time.sleep(1)
        scp.input_text_message(text)
        time.sleep(1)
        scp.send_text()
        scp.click_back()
        # CheckPoit:1、该条消息被删除
        msg.left_slide_message_record_by_number()
        msg.click_msg_delete()
        msg.page_should_not_contain_text("大佬1")
        msg.page_should_not_contain_text("hello")

    @tags('ALL', 'CMCC', 'msg')
    def test_msg_xiaoliping_B_0017(self):
        """消息列表网络异常显示"""
        mp = MessagePage()
        # 设置手机网络断开
        mp.set_network_status(0)
        time.sleep(2)
        # 1.是否提示当前网络不可用，请检查网络设置或稍后重试
        self.assertEquals(mp.is_exist_network_anomaly(), True)
        # 2.等待消息页面加载
        mp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_xiaoliping_B_0017():
        """恢复网络"""
        mp = MessagePage()
        mp.set_network_status(6)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'CMCC_broken_network', 'LXD')
    def test_msg_xiaoliping_B_0019(self):
        """消息列表显示未发送成功"""
        mp = MessagePage()
        # 确保消息页面当前没有未发送成功消息标记
        if mp.is_iv_fail_status_present():
            mp.clear_fail_in_send_message()
        # 进入聊天会话页面
        name = "大佬1"
        Preconditions.enter_single_chat_page(name)
        # 设置手机网络断开
        mp.set_network_status(0)
        scp = SingleChatPage()
        text = "222"
        # 1.输入文本信息
        mp.swipe_by_percent_on_screen(50, 60, 50, 10)
        scp.input_text_message(text)
        scp.send_text()
        # 2.是否显示消息发送失败标识
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        scp.click_back()
        mp.wait_for_page_load()
        # 3.消息预览中是否显示未发送成功消息标记
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_xiaoliping_B_0019():
        """恢复网络"""
        mp = MessagePage()
        mp.set_network_status(6)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'CMCC', 'msg')
    def test_msg_xiaoliping_B_0031(self):
        """消息列表窗口右滑删除（ios）"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # Step: 1、点击窗口右滑
        msg = MessagePage()
        Preconditions.enter_single_chat_page("大佬1")
        scp = SingleChatPage()
        text = "hello"
        # 收起键盘
        msg.swipe_by_percent_on_screen(50, 60, 50, 10)
        time.sleep(1)
        scp.input_text_message(text)
        time.sleep(1)
        scp.send_text()
        scp.click_back()
        # Step: 2、选择删除
        # 左滑删除
        msg.left_slide_message_record_by_number()
        msg.click_msg_delete()
        # CheckPoit:1、该条消息被删除
        msg.page_should_not_contain_text("大佬1")
        msg.page_should_not_contain_text("hello")

    @tags('ALL', 'CMCC', 'msg')
    def test_msg_xiaoqiu_0301(self):
        """消息列表——左滑——删除会话窗口"""
        mess = MessagePage()
        mess.make_sure_message_list_have_record()
        Preconditions.make_already_in_message_page()
        name1 = mess.get_first_list_name()
        # 1、左滑消息列表的会话窗口，会展示删除功能
        mess.left_slide_message_record_by_number()
        time.sleep(2)
        self.assertTrue(mess.is_element_present(text='左滑删除'))
        self.assertTrue(mess.is_element_present(text='置顶'))
        # 2、点击删除，会直接删除此聊天会话并同时清除其中的聊天记录
        mess.click_delete_list()
        time.sleep(2)
        self.assertFalse(mess.is_text_present(name1))



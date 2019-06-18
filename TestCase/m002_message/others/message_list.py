import random
import re
import time
import unittest
import uuid

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

        mp = MessagePage()
        if mp.is_on_this_page():
            return
        else:
            # current_mobile().launch_app()
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
        time.sleep(2)
        msg.click_msg_first_list()
        time.sleep(2)
        ChatWindowPage().is_on_this_page()
        #点击返回 返回到消息列表
        ChatWindowPage().click_back()
        msg.is_on_this_page()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_B_0007(self):
        """消息列表消息单条删除"""
        msg= MessagePage()
        time.sleep(2)
        title1=msg.assert_first_message_title_in_list_is()
        msg.press_and_move_left_first_list()
        time.sleep(2)
        msg.click_delete_list()
        # msg.click_text('删除')
        time.sleep(2)
        title2=msg.assert_first_message_title_in_list_is()
        self.assertNotEqual(title1,title2)



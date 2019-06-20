import unittest
import time
import warnings
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from preconditions.BasePreconditions import LoginPreconditions
from library.core.utils.testcasefilter import tags
from pages.chat.chatfileProview import ChatfileProviewPage


from pages import *
from selenium.common.exceptions import TimeoutException

import re
import random
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile


REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    # 'Android-移动': 'single_mobile',
    'IOS-移动': 'iphone',
    'IOS-移动-移动': 'M960BDQN229CHiphone8',
}


class Preconditions(LoginPreconditions):
    """
    分解前置条件
    """
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
    def make_sure_chatwindow_exist_locator_list():
        """确保我的电脑页面有位置记录"""
        chat=ChatWindowPage()
        time.sleep(2)
        if chat.is_element_present_locator_list():
            chat.wait_for_page_load()
        else:
            chat = ChatWindowPage()
            time.sleep(2)
            chat.click_more()
            chat.click_locator()
            time.sleep(2)
            # 选择位置界面
            locator = ChatLocationPage()
            locator.wait_for_page_load()
            locator.click_send()
            time.sleep(2)

    @staticmethod
    def send_locator():
        """聊天界面-发送位置"""
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_more()
        chat.click_locator()
        time.sleep(2)
        # 选择位置界面
        locator = ChatLocationPage()
        locator.wait_for_page_load()
        locator.click_send()
        time.sleep(2)


class SingleChatLocator(TestCase):
    """单聊-位置"""

    @classmethod
    def default_setUp(self):
        """确保每个用例执行前在单聊"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        name='大佬1'
        if msg.is_text_present(name):
            msg.click_text(name)
        else:
            msg.click_search_box()
            time.sleep(1)
            msg.input_search_text(name)
            time.sleep(2)
            msg.click_search_local_contact()
            time.sleep(2)
            ContactDetailsPage().click_message_icon()

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0362(self):
        """单聊发送位置成功"""
        #勾选位置
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_more()
        chat.click_locator()
        #选择位置界面
        locator = ChatLocationPage()
        self.assertEqual(locator.is_on_this_page(),True)
        locator.click_send()
        #3.发送成功
        time.sleep(2)
        self.assertEqual(chat.is_element_present_resend(), False)
        # 返回聊天列表查看
        chat.click_back()
        msg = MessagePage()
        msg.wait_for_page_load()
        msg.page_should_contain_text('位置')

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0437(self):
        """点击位置消息体进入到位置详情页面，可以进行导航操作"""
        #确保消息列表有发送位置的记录
        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_locator_list()
        chat.page_down()
        time.sleep(2)
        chat.click_locator_list()
        time.sleep(2)
        location=ChatLocationPage()
        self.assertEqual(location.is_on_this_page_navitation_detail_page(),True)
        location.page_contain_element_navigation_button()

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0445(self):
        """在位置搜索页面选择搜索结果，网络正常时进行发送位置消息"""
        #确保消息列表有发送位置的记录
        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_locator_list()
        chat.page_down()
        time.sleep(2)
        #进入位置搜索界面
        chat.click_more()
        chat.click_locator()
        time.sleep(2)
        #搜索界面，搜索位置
        location=ChatLocationPage()
        location.wait_for_page_load()
        location.click_search_box()
        keyword='天安云谷'
        location.input_search_keyward(keyword)
        time.sleep(2)
        location.click_text('天安云谷3栋')
        location.wait_for_page_load()
        location.click_send()
        time.sleep(2)
        #判断发送成功
        self.assertEqual(chat.is_element_present_resend(), False)


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0369(self):
        """将自己发送的位置转发到普通群"""
        #确保当前页面有地址记录
        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_locator_list()
        chat.page_down()
        time.sleep(3)
        #长按转发
        # chat.long_press('广东省')
        # 调起菜单判断
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        # 点击转发
        chat.click_forward()
        time.sleep(2)
        #判断在选择联系人界面
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(),True)
        #选择一个普通群
        select.click_select_one_group()
        select_group=SelectOneGroupPage()
        self.assertEqual(select_group.is_on_this_page(),True)
        select_group.select_first_group()
        #选择群后，弹起弹框
        time.sleep(2)
        select_group.page_should_contain_text('取消')
        select_group.page_should_contain_text('确定')
        select_group.click_sure_send()
        time.sleep(2)
        #返回到聊天界面
        self.assertEqual(chat.is_on_this_page(),True)

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0370(self):
        """将自己发送的位置转发到企业群"""
        #确保当前页面有地址记录
        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_locator_list()
        chat.page_down()
        time.sleep(3)
        #长按转发
        # chat.long_press('广东省')
        # 调起菜单判断
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        # 点击转发
        chat.click_forward()
        time.sleep(2)
        #判断在选择联系人界面
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(),True)
        #选择一个企业群
        select.click_select_one_group()
        select_group=SelectOneGroupPage()
        self.assertEqual(select_group.is_on_this_page(),True)
        select_group.select_one_company_group()
        #选择群后，弹起弹框
        time.sleep(2)
        select_group.page_should_contain_text('取消')
        select_group.page_should_contain_text('确定')
        select_group.click_sure_send()
        time.sleep(2)
        #返回到聊天界面
        self.assertEqual(chat.is_on_this_page(),True)



    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0436(self):
        """长按发送出去的位置消息体进行转发、删除、收藏、撤回等操作"""
        #确保当前页面有地址记录
        chat = ChatWindowPage()
        Preconditions.send_locator()
        chat.page_down()
        time.sleep(3)
        #长按转发
        # chat.long_press('广东省')
        #调起菜单判断
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='测回')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0450(self):
        """单聊发送位置成功"""
        #勾选位置
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_more()
        chat.click_locator()
        #选择位置界面
        locator = ChatLocationPage()
        locator.wait_for_page_load()
        name1=locator.get_locator_name()
        self.assertEqual(locator.is_on_this_page(),True)
        locator.swipe_by_percent_on_screen(90, 38, 10, 38)
        # locator.press_and_move_left_on_map()
        time.sleep(2)
        name2=locator.get_locator_name()
        time.sleep(1)
        self.assertNotEqual(name1,name2)
        locator.click_send()
        #3.发送成功
        time.sleep(2)
        self.assertEqual(chat.is_element_present_resend(), False)




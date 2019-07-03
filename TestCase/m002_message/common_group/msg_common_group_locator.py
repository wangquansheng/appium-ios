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
        #删除所有的位置消息
        if chat.is_element_present_locator_list():
            chat.page_down()
            # chat.long_press('广东省')
            chat.click_delete()
            chat.click_sure_delete()

        time.sleep(2)
        chat.click_more()
        chat.click_locator()
        time.sleep(2)
        # 选择位置界面
        locator = ChatLocationPage()
        locator.wait_for_page_load()
        locator.click_send()
        time.sleep(2)



class GroupChatLocator(TestCase):
    """群聊-位置"""

    # @classmethod
    # def setUpClass(cls):
    #     Preconditions.select_mobile('IOS-移动')
    #     Preconditions.make_already_in_message_page()
    #     time.sleep(2)
    #     MessagePage().delete_all_message_list()


    @classmethod
    def default_setUp(self):
        """确保每个用例执行前在群聊"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        name='群聊1'
        if msg.is_text_present(name):
            msg.click_text(name)
        else:
            msg.click_search_box()
            time.sleep(1)
            msg.input_search_text(name)
            time.sleep(2)
            msg.click_element_first_list()
            time.sleep(2)


    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'msg', 'CMCC','common_group')
    def test_msg_weifenglian_qun_0336(self):
        """将自己发送的位置转发到手机联系人"""
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
        #选择一个手机联系人
        select.select_local_contacts()
        local_contact=SelectLocalContactsPage()
        self.assertEqual(local_contact.is_on_this_page(),True)
        local_contact.swipe_select_one_member_by_name('大佬2')
        #选择群后，弹起弹框
        time.sleep(2)
        local_contact.page_should_contain_text('取消')
        local_contact.page_should_contain_text('确定')
        local_contact.click_sure()
        time.sleep(2)
        #返回到聊天界面
        self.assertEqual(chat.is_on_this_page(),True)


    @tags('ALL', 'msg', 'CMCC','common_group')
    def test_msg_weifenglian_qun_0349(self):
        """将自己发送的位置转发到团队未置灰的联系人"""
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
        #选择一个团队未置灰的联系人
        select.click_he_contacts()
        group_contact=SelectHeContactsPage()
        group_contact.select_one_team_by_name('ateam7272')
        group_detail=SelectHeContactsDetailPage()
        group_detail.select_one_he_contact_by_name('alice')
        #选择群后，弹起弹框
        time.sleep(2)
        group_detail.page_should_contain_text('取消')
        group_detail.page_should_contain_text('确定')
        group_detail.click_sure()
        time.sleep(2)
        #返回到聊天界面
        self.assertEqual(chat.is_on_this_page(),True)

    @tags('ALL', 'msg', 'CMCC','common_group')
    def test_msg_weifenglian_qun_0369(self):
        """将自己发送的位置转发到我的电脑"""
        #确保当前页面有地址记录
        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_locator_list()
        chat.page_down()
        time.sleep(3)
        #长按转发
        # chat.long_press('广东省')
        #调起菜单判断
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        #点击转发
        chat.click_forward()
        time.sleep(2)
        #判断在选择联系人界面
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(),True)
        #选择一个搜索我的电脑
        select.click_search_contact()
        select.input_search_keyword('我的电脑')
        select.click_element_by_id(text='搜索结果列表1')
        #选择群后，弹起弹框
        time.sleep(2)
        select.page_should_contain_text('取消')
        select.page_should_contain_text('确定')
        select.click_sure_forward()
        time.sleep(2)
        #返回到聊天界面
        self.assertEqual(chat.is_on_this_page(),True)

    @tags('ALL', 'msg', 'CMCC','common_group')
    def test_msg_weifenglian_qun_0370(self):
        """将自己发送的位置转发到最近聊天联系人"""
        #确保当前页面有地址记录
        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_locator_list()
        chat.page_down()
        time.sleep(3)
        #长按转发
        # chat.long_press('广东省')
        #调起菜单判断
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        #点击转发
        chat.click_forward()
        time.sleep(2)
        #判断在选择联系人界面
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(),True)
        #选择最近聊天联系人
        select.click_recent_chat_contact()
        #选择群后，弹起弹框
        time.sleep(2)
        select.page_should_contain_text('取消')
        select.page_should_contain_text('确定')
        select.click_sure_forward()
        time.sleep(2)
        #返回到聊天界面
        self.assertEqual(chat.is_on_this_page(),True)

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_qun_0373(self):
        """对接收到的位置消息进行删除"""
        #确保当前页面有地址记录
        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_locator_list()
        chat.page_down()
        time.sleep(3)
        #长按转发
        # chat.long_press('广东省')
        #调起菜单判断
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        #点击删除
        chat.click_delete()
        time.sleep(2)
        chat.page_should_contain_text('取消')
        chat.page_should_contain_text('删除')
        chat.click_sure_delete()
        time.sleep(2)


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_qun_0374(self):
        """对自己发送出去的位置消息进行十秒内撤回"""
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
        chat.page_contain_element(locator='撤回')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        #点击撤回
        chat.click_revoke()
        time.sleep(2)
        chat.click_i_know()
        time.sleep(2)
        chat.page_down()
        chat.page_should_contain_text('你撤回了一条消息')

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_qun_0375(self):
        """对自己发送出去的位置消息进行收藏"""
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
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        #点击收藏
        chat.click_collection()
        time.sleep(2)
        #返回收藏列表查看
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        collection = MeCollectionPage()
        collection.page_should_contain_text('位置')
        collection.page_should_contain_text('广东省')

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_qun_0312(self):
        """群聊（企业群/普通群）发送位置成功"""
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



import unittest
import time
import warnings
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from preconditions.BasePreconditions import LoginPreconditions
from library.core.utils.testcasefilter import tags
from pages.chat.chatfileProview import ChatfileProviewPage
from pages.contacts.my_group import ALLMyGroup
from pages.call.multipartycall import MultipartyCallPage

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
        """断开手机连接"""
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
    def creat_group_chatwindows_with_B_and_A(name='双机群聊1'):
        """创建同时存在A、B两个手机号的群聊，且保证A、B手机都加入该群(b手机创建群-邀请A加入)"""
        # 获取A手机的电话号码
        Preconditions.select_mobile('IOS-移动')
        phone_number_A = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 切换到B手机，创建群（群成员有A B两台手机）
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        # B手机创建创建群
        msg.open_contacts_page()
        contact = ContactsPage()
        # 判断手机联系人页面是否存在手机联系人A
        contact.click_phone_contact()
        time.sleep(2)
        if contact.page_should_contain_text2(phone_number_A):
            contact.click_back()
        else:
            contact.click_add()
            creat = CreateContactPage()
            creat.create_contact(phone_number_A, phone_number_A)
            time.sleep(2)
            Preconditions.make_already_in_message_page()
            MessagePage().open_contacts_page()
        # b手机创建群聊
        ContactsPage().open_group_chat_list()
        my_group=ALLMyGroup()
        my_group.click_creat_group()
         # 选择A手机 和另外一个联系人创建群组
        select=SelectContactsPage()
        select.click_phone_contact()
        local = SelectLocalContactsPage()
        local.swipe_select_one_member_by_name('大佬1')
        local.swipe_select_one_member_by_name(phone_number_A)
        local.click_sure()
        time.sleep(2)
        my_group.click_clear_group_name()
        my_group.input_group_name(name)
        my_group.click_sure_creat()
        time.sleep(2)
        ChatWindowPage().wait_for_page_load()
        # 切换到A手机，加入群聊
        Preconditions.select_mobile("IOS-移动")
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        time.sleep(3)
        if not my_group.page_should_contain_text2(name):
            Preconditions.make_already_in_message_page()
            mess.click_text('系统消息')
            mess.click_system_message_allow()
            time.sleep(2)

    @staticmethod
    def make_sure_have_group_chat(group_name='双机群聊1'):
        """确保A手机存在群聊 并进入群聊聊天页面"""
        # Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        mess.open_contacts_page()
        ContactsPage().open_group_chat_list()
        time.sleep(2)
        my_group = ALLMyGroup()
        if my_group.page_should_contain_text2(group_name):
            my_group.select_group_by_name(group_name)
            time.sleep(2)
        else:
            Preconditions.creat_group_chatwindows_with_B_and_A(name=group_name)
            time.sleep(2)

    @staticmethod
    def send_pic_in_group_chat():
        """发送图片"""
        chat = ChatWindowPage()
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.click_pic()
        select_pic = ChatPicPage()
        select_pic.click_camara_picture()
        select_pic.select_first_picture()
        select_pic.click_send()
        time.sleep(3)

    @staticmethod
    def enter_in_group_chatwindows_with_B_to_A(group_name='双机群聊1'):
        """进入群聊对话页面"""
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.open_contacts_page()
        ContactsPage().open_group_chat_list()
        time.sleep(2)
        my_group = ALLMyGroup()
        if my_group.page_should_contain_text2(group_name):
            my_group.select_group_by_name(group_name)
            time.sleep(2)


class GroupChatDouble(TestCase):
    """群聊--双机用例"""

    # @classmethod
    # def setUpClass(cls):
    #     warnings.simplefilter('ignore', ResourceWarning)
    #     Preconditions.select_mobile('IOS-移动')
    #     Preconditions.make_sure_have_group_chat()

    def setUp_test_msg_xiaoliping_D_0023(self):
        """确保A手机收到群聊发送的图片消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        # 切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送图片
        Preconditions.send_pic_in_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0023(self):
        """群聊会话页面，转发他人发送的图片到当前会话窗口"""
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        mess.wait_for_page_load_new_message_coming()
        mess.click_text('双机群聊1')
        chat=ChatWindowPage()
        chat.wait_for_page_load()
        # 下载图片后长按
        chat = ChatWindowPage()
        chat.click_coordinate(25, 35)
        time.sleep(3)
        chat.click_coordinate(50, 50)
        time.sleep(1)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='编辑'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 3.选择最近聊天联系人-调起询问弹窗
        select.click_recent_chat_contact()
        self.assertEqual(select.is_element_present(locator='取消'),True)
        self.assertEqual(select.is_element_present(locator='确定'), True)
        # 4.点击确定，转发成功(toast未验证)
        select.click_sure_forward()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(),True)

    def tearDown_test_msg_xiaoliping_D_0023(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_xiaoliping_D_0059(self):
        """确保A手机收到群聊发送的图片消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        #切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat=ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        #发送图片
        Preconditions.send_pic_in_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0059(self):
        """群聊会话页面，转发他人发送的图片到当前会话窗口"""
        #切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        mess.wait_for_page_load_new_message_coming()
        mess.click_text('双机群聊1')
        chat=ChatWindowPage()
        chat.wait_for_page_load()
        #下载图片后长按
        chat = ChatWindowPage()
        chat.click_coordinate(25, 30)
        time.sleep(3)
        chat.click_coordinate(50, 50)
        time.sleep(1)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        #1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='编辑'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        #2.点击删除-调起弹框
        chat.click_delete()
        self.assertEqual(chat.is_element_present_by_locator(locator='确定删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='取消删除'), True)
        time.sleep(2)
        #点击确定
        chat.click_sure_delete()
        time.sleep(2)
        self.assertEqual(chat.is_element_present_by_locator(locator='消息列表'),False)
        self.assertEqual(chat.is_on_this_page(), True)

    def tearDown_test_msg_xiaoliping_D_0059(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



    def setUp_test_msg_xiaoliping_D_0063(self):
        """确保A手机收到群聊发送的视频消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，清空聊天列表
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        #切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat=ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        #发送视频
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_video()
        time.sleep(2)
        csf.click_select_video()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0063(self):
        """群聊会话页面，转发他人发送的视频给手机联系人"""
        #切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        mess.click_text('双机群聊1')
        chat=ChatWindowPage()
        chat.wait_for_page_load()
        #下载图片后长按
        chat = ChatWindowPage()
        chat.click_play_video()  # 下载文件
        chat.wait_for_page_load_play_video()
        chat.swipe_by_percent_on_screen(50, 50, 50, 60)
        chat.click_cancel_previer_video()
        time.sleep(2)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        #1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        #2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(),True)
        # 3.选择任意手机联系人
        select.select_local_contacts()
        local_contact = SelectLocalContactsPage()
        self.assertEqual(local_contact.is_on_this_page(), True)
        local_contact.swipe_select_one_member_by_name('大佬2')
        time.sleep(2)
        self.assertEqual(local_contact.is_element_exit(text='取消'), True)
        self.assertEqual(local_contact.is_element_exit(text='确定'), True)
        # 4.点击确定，转发成功(toast未验证)
        local_contact.click_sure()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(), True)

    def tearDown_test_msg_xiaoliping_D_0063(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


#群聊-位置


    def setUp_test_msg_weifenglian_qun_0377(self):
        """确保A手机收到群聊发送的位置消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，清空聊天列表
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        #切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat=ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        #发送位置
        chat.click_more()
        chat.click_locator()
        time.sleep(2)
        # 选择位置界面
        locator = ChatLocationPage()
        locator.wait_for_page_load()
        locator.click_send()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_qun_0377(self):
        """将接收到的位置转发到普通群"""
        #切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        mess.click_text('双机群聊1')
        chat=ChatWindowPage()
        chat.wait_for_page_load()
        #长按
        chat = ChatWindowPage()
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        #1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        #2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(),True)
        # 3.选择任意普通群-调起询问弹窗
        select.click_select_one_group()
        one_group = SelectOneGroupPage()
        one_group.selecting_one_group_by_name('群聊1')
        time.sleep(2)
        self.assertEqual(one_group.is_element_exit(text='取消'), True)
        self.assertEqual(one_group.is_element_exit(text='确定'), True)
        # 4.点击确定，转发成功(toast未验证)
        one_group.click_sure_send()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(), True)

    def tearDown_test_weifenglian_qun_0377(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



    def setUp_test_msg_weifenglian_qun_0378(self):
        """确保A手机收到群聊发送的位置消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，清空聊天列表
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        #切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat=ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        #发送位置
        chat.click_more()
        chat.click_locator()
        time.sleep(2)
        # 选择位置界面
        locator = ChatLocationPage()
        locator.wait_for_page_load()
        locator.click_send()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_qun_0378(self):
        """将接收到的位置转发到企业群"""
        #切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        mess.click_text('双机群聊1')
        chat=ChatWindowPage()
        chat.wait_for_page_load()
        #长按
        chat = ChatWindowPage()
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        #1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        #2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(),True)
        # 3.选择企业群-调起询问弹窗
        select.click_select_one_group()
        one_group = SelectOneGroupPage()
        one_group.select_one_company_group()
        time.sleep(2)
        self.assertEqual(one_group.is_element_exit(text='取消'), True)
        self.assertEqual(one_group.is_element_exit(text='确定'), True)
        # 4.点击确定，转发成功(toast未验证)
        one_group.click_sure_send()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(), True)


    def tearDown_test_weifenglian_qun_0378(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



    def setUp_test_msg_huangmianhua_0163(self):
        warnings.simplefilter('ignore', ResourceWarning)
        # 获取B手机号-清空所以的消息列表
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 1、聊天会话页面——超长文本消息 带有@群成员
        Preconditions.select_mobile('IOS-移动')
        # 切换到A手机，删除聊天列表
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.click_input_box()
        text='long message'*40+'@'
        chat.input_message_text(text)
        time.sleep(2)
        chat.select_members_by_name(name=phone_number_B)
        time.sleep(2)
        chat.click_send_button()
        time.sleep(2)

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0163(self):
        """普通群——聊天会话页面——超长文本消息中带有@群成员"""
        # 切换到B 手机，查看消息列表展示
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        # MessagePage().wait_for_page_load_new_message_coming()
        time.sleep(3)
        message = '有人@我'
        MessagePage().page_should_contain_text(message)

    def tearDown_test_msg_huangmianhua_0163(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_huangmianhua_0165(self):
        warnings.simplefilter('ignore', ResourceWarning)
        # 获取B手机号-清空所以的消息列表
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 1、聊天会话页面——多个@后再选要@的群成员 带有@群成员
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.click_input_box()
        chat.input_message_text('@@@@')
        chat.select_members_by_name(name=phone_number_B)
        time.sleep(2)
        chat.click_send_button()
        time.sleep(2)

    @tags('ALL', 'enterprise_group', 'CMCC_调试中')
    def test_msg_huangmianhua_0165(self):
        """群聊天会话页面——输入多个@后——再选要@的群成员查看@效果"""
        # 切换到B 手机，查看消息列表展示
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(3)
        message = '有人@我'
        MessagePage().page_should_not_contain_text(message)

    def tearDown_test_msg_huangmianhua_0165(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_huangmianhua_0166(self):
        warnings.simplefilter('ignore', ResourceWarning)
        # 获取B手机号-清空所以的消息列表
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 1、聊天会话页面——带有@多个群成员
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.click_input_box()
        text = '@'
        chat.input_message_text(text)
        time.sleep(2)
        chat.select_members_by_name(name=phone_number_B)
        chat.click_send_button()
        time.sleep(2)

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0166(self):
        """群聊天会话页面——同时@多个人——@效果展示(需要群聊需要至少有3个联系人，暂时无法实现)"""
        # 切换到B 手机，查看消息列表展示
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(3)
        message = '有人@我'
        MessagePage().page_should_contain_text(message)

    def tearDown_test_msg_huangmianhua_0166(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


# 群聊-设置

    def setUp_test_msg_xiaoqiu_0213(self):
        """确保A手机进入群聊设置页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机,进入聊天会话页面-保持消息免打扰是关闭状态
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        GroupChatPage().click_setting()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0213(self):
        """群聊设置页面——开启消息免打扰"""
        # 1、点击打开消息免打扰开关，可以开启消息免打扰的开关
        set = GroupChatSetPage()
        if set.get_switch_undisturb_value() == '0':
            set.click_switch_undisturb()
        # 2、返回到消息列表，接收到新消息时，会话窗口上方会展示红点
        Preconditions.make_already_in_message_page()
        # 确保接受到消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = GroupChatPage()
        chat.click_input_box()
        chat.input_message_text('文本消息')
        chat.click_send_button()
        time.sleep(3)
        # 切换到A手机 查看是否有消息红点
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        self.assertTrue(mess.is_exist_news_red_dot())
        # 3、进入到聊天会话窗口页面，左上角的群名称右边会同样展示一个被划掉的小铃铛
        mess.click_text('双机群聊1')
        time.sleep(2)
        self.assertTrue(chat.is_exist_undisturb())
        # 去除消息免打扰状态
        chat.click_setting()
        set = GroupChatSetPage()
        if set.get_switch_undisturb_value() == '1':
            set.click_switch_undisturb()
            time.sleep(2)

    def tearDown_test_msg_xiaoqiu_0213(self):

        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_xiaoqiu_0214(self):
        """确保A手机进入群聊设置页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机,进入聊天会话页面-保持消息免打扰是开启状态
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        if set.get_switch_undisturb_value() == '0':
            set.click_switch_undisturb()
            time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0214(self):
        """群聊设置页面——关闭消息免打扰"""
        # 1、点击关闭消息免打扰开关，可以关闭消息免打扰的开关
        set = GroupChatSetPage()
        if set.get_switch_undisturb_value() == '1':
            set.click_switch_undisturb()
            time.sleep(3)
        # 2、返回到消息列表，接收到新消息时，会话窗口上方会展示数量，不展示红点，同样开启了声音、震动提醒的也会发出提声音和震动
        Preconditions.make_already_in_message_page()
        # 确保接受到消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = GroupChatPage()
        chat.click_input_box()
        chat.input_message_text('文本消息')
        chat.click_send_button()
        time.sleep(3)
        # 切换到A手机 查看是否有新消息通知
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        self.assertTrue(mess.is_exist_unread_make_and_number())


    def tearDown_test_msg_xiaoqiu_0214(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_xiaoqiu_0225(self):
        """确保A手机进入群聊设页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机（群成员）,进入聊天会话页面-保持消息免打扰是开启状态
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0225(self):
        """聊天设置页面——删除并退出群聊——群成员(群成员3人)"""
        # 进入聊天设置页面
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        self.assertTrue(set.is_on_this_page())
        # 2、点击页面底部的“删除并退出”按钮，弹出确认弹窗
        set.click_delete_and_exit()
        self.assertTrue(set.is_exit_element(locator='取消'))
        self.assertTrue(set.is_exit_element(locator='退出'))
        # 3、点击取消或者弹窗空白处，关闭弹窗
        set.click_cancel()
        self.assertFalse(set.is_exit_element(locator='退出'))
        # 4、点击“确定”按钮，退出当前群聊返回到消息列表并收到一条系统消息：你已退出群
        set.click_delete_and_exit()
        set.click_sure_exit_group()
        time.sleep(3)
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_contain_text('你已退出群')

    def tearDown_test_msg_xiaoqiu_0225(self):
        # 移除联系人后 增加该联系人
        # 获取A的手机号码
        Preconditions.select_mobile('IOS-移动')
        phone_number_A = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 切换到B手机 添加联系人
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        set.click_add_member()
        SelectContactsPage().select_one_contact_by_name(phone_number_A)
        time.sleep(2)
        SelectContactsPage().click_sure_bottom()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoqiu_0226(self):
        """确保A手机进入群聊设页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机（群成员）,进入聊天会话页面-保持消息免打扰是开启状态
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        # 确保群成员小于3人
        GroupChatPage().click_setting()
        GroupChatSetPage().delete_member_by_name('大佬1')
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0226(self):
        """聊天设置页面——删除并退出群聊——群成员(群成员小于3人)"""
        # 切换手机-进入聊天设置页面
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        self.assertTrue(set.is_on_this_page())
        # 2、点击页面底部的“删除并退出”按钮，会退出当前群聊返回到消息列表并收到一条系统消息：你已退出群
        set.click_delete_and_exit()
        set.click_sure_exit_group()
        time.sleep(3)
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_contain_text('你已退出群')

    def tearDown_test_msg_xiaoqiu_0226(self):
        # 创建群
        Preconditions.make_sure_have_group_chat()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoqiu_0227(self):
        """确保A手机进入群聊设页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机（群成员）,进入聊天会话页面-保持消息免打扰是开启状态
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        # 确保群成员大于3人
        GroupChatPage().click_setting()
        GroupChatSetPage().add_member_by_name('大佬2')
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0227(self):
        """聊天设置页面——删除并退出群聊——群成员(群成员大于3人)"""
        # 切换手机-进入聊天设置页面
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        self.assertTrue(set.is_on_this_page())
        # 2、点击页面底部的“删除并退出”按钮，会退出当前群聊返回到消息列表并收到一条系统消息：你已退出群
        set.click_delete_and_exit()
        set.click_sure_exit_group()
        time.sleep(3)
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_contain_text('你已退出群')
        # 移除联系人后 增加该联系人
        # 获取A的手机号码
        Preconditions.select_mobile('IOS-移动')
        phone_number_A = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 切换到B手机 添加联系人
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        set.add_member_by_name(member=phone_number_A)
        set.delete_member_by_name('大佬2')

    def tearDown_test_msg_xiaoqiu_0227(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_xiaoqiu_0415(self):
        """确保A手机进入群聊设页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到B手机（群主）,进入聊天会话页面
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        # 进入设置页面
        GroupChatPage().click_setting()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0415(self):
        """群主在群设置页面——将所有群成员移出群后"""
        # B手机聊天设置页面 移除全部成员
        set = GroupChatSetPage()
        set.delete_all_member()
        # 1、群主，在消息列表会收到一条系统消息：该群已解散。在群聊会话页面会收到一条提示：该群已解散
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_contain_text('该群已解散')
        # 切换群成员手机A
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        # 2、群成员，在消息列表会收到一条系统消息：你已被请出该群。在群聊会话页面会收到一条提示：你已被请出该群，当前会话窗口不删除
        MessagePage().page_should_contain_text('你已被请出该群')

    def tearDown_test_msg_xiaoqiu_0415(self):
        # 新创建群
        Preconditions.make_sure_have_group_chat()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_xiaoqiu_0416(self):
        """确保A手机进入群聊设页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机（群成员）,进入聊天会话页面
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        # 进入设置页面
        GroupChatPage().click_setting()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0416(self):
        """群成员在群设置页面——点击删除并退出按钮后"""
        # 群成员在群设置页面——点击删除并退出按钮后
        set = GroupChatSetPage()
        set.click_delete_and_exit()
        set.click_sure_exit_group()
        # 2、退出群的成员，会收到一条系统消息：你已退出群
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_contain_text('你已退出群')
        phone_number_A = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 1、群主，XXX已退出群
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().click_text('双机群聊1')
        chat = GroupChatPage()
        self.assertTrue(chat.is_element_exit_('消息记录'))
        # 群主再添加该成员
        chat.click_setting()
        set = GroupChatSetPage()
        set.add_member_by_name(member=phone_number_A)

    def tearDown_test_msg_xiaoqiu_0416(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoqiu_0602(self):
        """确保A手机进入群聊设置页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机,进入聊天会话页面-保持消息免打扰是关闭状态
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        # 1、在当前页面点击右上角的设置按钮
        GroupChatPage().click_setting()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0602(self):
        """开启免打扰后，接收到新消息时，该消息列表窗口展示消息红点"""
        # 1、点击打开消息免打扰开关，可以开启消息免打扰的开关
        set = GroupChatSetPage()
        value = set.get_switch_undisturb_value()
        if value == '0':
            set.click_switch_undisturb()
        time.sleep(2)
        value2 = set.get_switch_undisturb_value()
        self.assertEqual(value2, '1')
        # 2、返回到消息列表，接收到新消息时，会话窗口上方会展示红点
        Preconditions.make_already_in_message_page()
        # 确保接受到消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = GroupChatPage()
        chat.send_mutiple_message(times=1)
        # 切换到A手机 查看是否有消息红点
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        self.assertTrue(mess.is_exist_news_red_dot())

    def tearDown_test_msg_xiaoqiu_0602(self):
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        # 去除消息免打扰状态
        mess.click_text('双机群聊1')
        time.sleep(2)
        chat = GroupChatPage()
        chat.click_setting()
        set = GroupChatSetPage()
        if set.get_switch_undisturb_value() == '1':
            set.click_switch_undisturb()
            time.sleep(2)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoqiu_0603(self):
        """确保A手机进入群聊设置页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机,进入聊天会话页面-保持消息免打扰是开启状态
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0603(self):
        """开启免打扰后，接收到新消息时，该消息列表窗口内容左边副标题应展示：接收到的未读新消息条数"""
        # 1、点击打开消息免打扰开关，可以开启消息免打扰的开关
        set = GroupChatSetPage()
        value = set.get_switch_undisturb_value()
        if value == '0':
            set.click_switch_undisturb()
        time.sleep(2)
        value2 = set.get_switch_undisturb_value()
        self.assertEqual(value2, '1')
        # 2、返回到消息列表，接收到新消息时，会话窗口上方会展示红点
        Preconditions.make_already_in_message_page()
        # 确保接受到消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = GroupChatPage()
        chat.send_mutiple_message(times=1)
        # 切换到A手机 查看是否有消息红点
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        self.assertTrue(mess.is_text_present('[1条]'))

    def tearDown_test_msg_xiaoqiu_0603(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoqiu_0604(self):
        """确保A手机进入群聊设置页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机,进入聊天会话页面-保持消息免打扰是关闭状态
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        # 1、在当前页面点击右上角的设置按钮
        GroupChatPage().click_setting()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0604(self):
        """开启免打扰后，有人@我时，该消息列表窗口直接展示：有人@我提示"""
        # 1、点击打开消息免打扰开关，可以开启消息免打扰的开关
        set = GroupChatSetPage()
        value = set.get_switch_undisturb_value()
        if value == '0':
            set.click_switch_undisturb()
        time.sleep(2)
        value2 = set.get_switch_undisturb_value()
        self.assertEqual(value2, '1')
        # 获取A的和飞信名称显示
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        name = MePage().get_my_name_in_hefeixin()
        # 2、返回到消息列表，接收到新消息时，会话窗口上方会展示红点
        Preconditions.make_already_in_message_page()
        # 确保接受到消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = GroupChatPage()
        chat.click_input_box()
        chat.input_message_text('@')
        chat.select_members_by_name(name)
        time.sleep(2)
        chat.click_send_button()
        # 切换到A手机 查看是否有消息红点
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.page_should_contain_text('有人@我')
        self.assertTrue(mess.is_exist_news_red_dot())

    def tearDown_test_msg_xiaoqiu_0604(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoqiu_0606(self):
        """确保A手机进入群聊设置页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机,进入聊天会话页面-保持消息免打扰是开启状态
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        GroupChatPage().click_setting()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0606(self):
        """开启免打扰后，接收到新消息时，该消息列表窗口内容左边副标题应展示：接收到的未读新消息条数"""
        # 1、点击打开消息免打扰开关，可以开启消息免打扰的开关
        set = GroupChatSetPage()
        value = set.get_switch_undisturb_value()
        if value == '0':
            set.click_switch_undisturb()
        time.sleep(2)
        value2 = set.get_switch_undisturb_value()
        self.assertEqual(value2, '1')
        # 2、返回到消息列表，接收到新消息时，会话窗口上方会展示红点
        Preconditions.make_already_in_message_page()
        # 确保接收到新消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = GroupChatPage()
        chat.send_mutiple_message(times=1)
        # 切换到A手机 查看是否有消息红点
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        time.sleep(2)
        self.assertTrue(mess.is_text_present('[1条]'))

    def tearDown_test_msg_xiaoqiu_0606(self):
        # 去除消息免打扰状态
        Preconditions.make_already_in_message_page()
        MessagePage().click_text('双机群聊1')
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        value = set.get_switch_undisturb_value()
        if value == '1':
            set.click_switch_undisturb()
        time.sleep(2)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoqiu_0607(self):
        """确保A手机进入群聊设置页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机,进入聊天会话页面-保持消息免打扰是开启状态
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        GroupChatPage().click_setting()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0607(self):
        """开启免打扰后，同时出现草稿和有人@我时，该消息列表窗口只展示：有人@我"""
        # 2、点击打开消息免打扰开关，可以开启消息免打扰的开关
        set = GroupChatSetPage()
        value = set.get_switch_undisturb_value()
        if value == '0':
            set.click_switch_undisturb()
        time.sleep(2)
        value2 = set.get_switch_undisturb_value()
        self.assertEqual(value2, '1')
        # 3、返回到会话窗口，在输入框中进行输入内容，然后点击左上角的返回按钮
        set.click_back()
        chat = GroupChatPage()
        chat.click_input_box()
        chat.input_message_text('消息文本')
        # 验证点 ：4、查看该消息列表窗口显示，窗口直接展示：草稿
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_contain_text('草稿')
        # 获取A的和飞信名称显示
        MessagePage().open_me_page()
        name = MePage().get_my_name_in_hefeixin()
        # 5、这时群里有人@我时，查看
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = GroupChatPage()
        chat.click_input_box()
        chat.input_message_text('@')
        chat.select_members_by_name(name)
        time.sleep(2)
        chat.click_send_button()
        # 验证点：5、该消息列表窗口只展示：有人@我
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.page_should_contain_text('有人@我')

    def tearDown_test_msg_xiaoqiu_0607(self):
        # 去除消息免打扰状态
        Preconditions.make_already_in_message_page()
        MessagePage().click_text('双机群聊1')
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        value = set.get_switch_undisturb_value()
        if value == '1':
            set.click_switch_undisturb()
        time.sleep(2)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoqiu_0608(self):
        """确保A手机进入群聊设置页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机,进入聊天会话页面-保持消息免打扰是开启状态
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        GroupChatPage().click_setting()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0608(self):
        """开启免打扰后，同时出现未读消息条数和有人@我时，该消息列表窗口只展示：有人@我"""
        # 2、点击打开消息免打扰开关，可以开启消息免打扰的开关
        set = GroupChatSetPage()
        mess = MessagePage()
        value = set.get_switch_undisturb_value()
        if value == '0':
            set.click_switch_undisturb()
        time.sleep(2)
        value2 = set.get_switch_undisturb_value()
        self.assertEqual(value2, '1')
        # 获取A的和飞信名称显示
        Preconditions.make_already_in_message_page()
        mess.delete_all_message_list()
        mess.open_me_page()
        name = MePage().get_my_name_in_hefeixin()
        # 3、返回到消息列表页，接收到新消息时查看
        # 确保接收到新消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = GroupChatPage()
        chat.send_mutiple_message(times=1)
        # 3、该消息列表窗口内容左边副标题应展示：接收到的未读新消息条数
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        self.assertTrue(mess.is_text_present('[1条]'))
        # 4、这时群里有人@我时，查看
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = GroupChatPage()
        chat.click_input_box()
        chat.input_message_text('@')
        chat.select_members_by_name(name)
        time.sleep(2)
        chat.click_send_button()
        # 验证点：5、该消息列表窗口只展示：有人@我
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.page_should_contain_text('有人@我')

    def tearDown_test_msg_xiaoqiu_0608(self):
        # 去除消息免打扰状态
        Preconditions.make_already_in_message_page()
        MessagePage().click_text('双机群聊1')
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        value = set.get_switch_undisturb_value()
        if value == '1':
            set.click_switch_undisturb()
        time.sleep(2)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoqiu_0609(self):
        """确保A手机进入群聊设置页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机,进入聊天会话页面-保持消息免打扰是开启状态
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        GroupChatPage().click_setting()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0609(self):
        """开启免打扰后，同时出现未读消息条数和草稿时，该消息列表窗口只展示：草稿"""
        # 2、点击打开消息免打扰开关，可以开启消息免打扰的开关
        set = GroupChatSetPage()
        value = set.get_switch_undisturb_value()
        if value == '0':
            set.click_switch_undisturb()
        time.sleep(2)
        value2 = set.get_switch_undisturb_value()
        self.assertEqual(value2, '1')
        # 3、返回到会话窗口，在输入框中进行输入内容，然后点击左上角的返回按钮
        set.click_back()
        chat = GroupChatPage()
        chat.click_input_box()
        chat.input_message_text('消息文本')
        # 验证点 ：4、查看该消息列表窗口显示，窗口直接展示：草稿
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_contain_text('草稿')
        # 获取A的和飞信名称显示
        MessagePage().open_me_page()
        name = MePage().get_my_name_in_hefeixin()
        # 5.这是接收到新的消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = GroupChatPage()
        chat.send_mutiple_message(times=1)
        # 验证点：5、该消息列表窗口只展示：草稿
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.page_should_contain_text('草稿')

    def tearDown_test_msg_xiaoqiu_0609(self):
        # 去除消息免打扰状态
        Preconditions.make_already_in_message_page()
        MessagePage().click_text('双机群聊1')
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        value = set.get_switch_undisturb_value()
        if value == '1':
            set.click_switch_undisturb()
        time.sleep(2)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoqiu_0610(self):
        """确保A手机进入群聊设置页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机,进入聊天会话页面-保持消息免打扰是开启状态
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        GroupChatPage().click_setting()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0610(self):
        """开启免打扰后，同时出现未读消息条数、草稿和有人@我时，该消息列表窗口只展示：有人@我"""
        # 2、点击打开消息免打扰开关，可以开启消息免打扰的开关
        set = GroupChatSetPage()
        value = set.get_switch_undisturb_value()
        if value == '0':
            set.click_switch_undisturb()
        time.sleep(2)
        value2 = set.get_switch_undisturb_value()
        self.assertEqual(value2, '1')
        # 3、返回到会话窗口，在输入框中进行输入内容，然后点击左上角的返回按钮
        set.click_back()
        chat = GroupChatPage()
        chat.click_input_box()
        chat.input_message_text('消息文本')
        # 验证点 ：4、查看该消息列表窗口显示，窗口直接展示：草稿
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_contain_text('草稿')
        # 获取A的和飞信名称显示
        MessagePage().open_me_page()
        name = MePage().get_my_name_in_hefeixin()
        # 5.这时接收到新的消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = GroupChatPage()
        chat.send_mutiple_message(times=1)
        # 验证点：5、该消息列表窗口只展示：草稿
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.page_should_contain_text('草稿')
        # 6、这时群里有人@我时，查看
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = GroupChatPage()
        chat.click_input_box()
        chat.input_message_text('@')
        chat.select_members_by_name(name)
        time.sleep(2)
        chat.click_send_button()
        # 验证点：6、该消息列表窗口只展示：有人@我
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.page_should_contain_text('有人@我')

    def tearDown_test_msg_xiaoqiu_0610(self):
        # 去除消息免打扰状态
        Preconditions.make_already_in_message_page()
        MessagePage().click_text('双机群聊1')
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        value = set.get_switch_undisturb_value()
        if value == '1':
            set.click_switch_undisturb()
        time.sleep(2)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoqiu_0611(self):
        """确保A手机进入群聊设置页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机,进入聊天会话页面-保持消息免打扰是开启状态
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        GroupChatPage().click_setting()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0611(self):
        """未开启免打扰，接收到新消息时，该消息列表窗口展示消息数字红点"""
        # 2、关闭消息免打扰，关闭成功
        set = GroupChatSetPage()
        value = set.get_switch_undisturb_value()
        if value == '1':
            set.click_switch_undisturb()
        time.sleep(2)
        value2 = set.get_switch_undisturb_value()
        self.assertEqual(value2, '0')
        Preconditions.make_already_in_message_page()
        # 3、返回到消息列表页，接收到新消息时查看
        # 确保接收到新消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = GroupChatPage()
        chat.send_mutiple_message(times=1)
        # 验证点：3、该消息列表窗口显示消息数字红点
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        self.assertTrue(mess.is_exist_unread_make_and_number())

    def tearDown_test_msg_xiaoqiu_0611(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoqiu_0612(self):
        """确保A手机进入群聊设置页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机,进入聊天会话页面-保持消息免打扰是开启状态
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        GroupChatPage().click_setting()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0612(self):
        """未开启免打扰，同时出现草稿和有人@我时，该消息列表窗口只展示：有人@我"""
        # 2、关闭消息免打扰，关闭成功
        set = GroupChatSetPage()
        value = set.get_switch_undisturb_value()
        if value == '1':
            set.click_switch_undisturb()
        time.sleep(2)
        value2 = set.get_switch_undisturb_value()
        self.assertEqual(value2, '0')
        Preconditions.make_already_in_message_page()
        # 3、返回到会话窗口，在输入框中进行输入内容，然后点击左上角的返回按钮
        set.click_back()
        chat = GroupChatPage()
        chat.click_input_box()
        chat.input_message_text('消息文本')
        # 验证点 ：4、查看该消息列表窗口显示，窗口直接展示：草稿
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_contain_text('草稿')
        # 获取A的和飞信名称显示
        MessagePage().open_me_page()
        name = MePage().get_my_name_in_hefeixin()
        # 5、这时群里有人@我时，查看
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = GroupChatPage()
        chat.click_input_box()
        chat.input_message_text('@')
        chat.select_members_by_name(name)
        time.sleep(2)
        chat.click_send_button()
        # 验证点：5、该消息列表窗口只展示：有人@我
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.page_should_contain_text('有人@我')

    def tearDown_test_msg_xiaoqiu_0612(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


class GroupChatDoubleMiddle(TestCase):
    """群聊--双机用例--中等级"""

    # @classmethod
    # def setUpClass(cls):
    #     warnings.simplefilter('ignore', ResourceWarning)
    #     Preconditions.select_mobile('IOS-移动')
    #     Preconditions.make_sure_have_group_chat()

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

# 转发他人发送的图片
    def setUp_test_msg_xiaoliping_D_0025(self):
        """确保A手机收到群聊发送的图片消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        # 切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送图片
        Preconditions.send_pic_in_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0025(self):
        """单聊会话页面，转发他人发送的图片到当前会话窗口"""
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        group_name = '双机群聊1'
        msg.click_text(group_name)
        time.sleep(2)
        # 下载图片后长按
        chat = ChatWindowPage()
        chat.click_coordinate(25, 35)
        time.sleep(3)
        chat.click_coordinate(50, 50)
        time.sleep(1)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='编辑'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 3.选择最近聊天联系人-调起询问弹窗
        select.click_search_contact()
        select.input_search_keyword(group_name)
        time.sleep(2)
        select.click_search_result()
        self.assertEqual(select.is_element_present(locator='取消'), True)
        self.assertEqual(select.is_element_present(locator='确定'), True)
        # 5、点击弹窗取消按钮
        select.click_cancel_forward()
        # 停留在当前页面
        self.assertTrue(select.is_text_present('选择联系人'))


    def setUp_test_msg_xiaoliping_D_0026(self):
        """确保A手机收到群聊发送的图片消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        # 切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送图片
        Preconditions.send_pic_in_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0026(self):
        """单聊会话页面，转发他人发送的图片到手机联系人"""
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        group_name = '双机群聊1'
        msg.click_text(group_name)
        time.sleep(2)
        # 下载图片后长按
        chat = ChatWindowPage()
        chat.click_coordinate(25, 35)
        time.sleep(3)
        chat.click_coordinate(50, 50)
        time.sleep(1)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='编辑'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 3.选择最近聊天联系人-调起询问弹窗
        select.click_phone_contact()
        select_local = SelectLocalContactsPage()
        name = '大佬1'
        select_local.swipe_select_one_member_by_name(name)
        time.sleep(2)
        self.assertEqual(select_local.is_element_exit(text='取消'), True)
        self.assertEqual(select_local.is_element_exit(text='确定按钮'), True)
        # 4、点击发送按钮
        select_local.click_sure_icon()
        # 4、toast提示：已转发，返回到当前会话窗口
        self.assertTrue(chat.is_on_this_page())
        # 发送成功
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_contain_text2(name)


    def setUp_test_msg_xiaoliping_D_0028(self):
        """确保A手机收到群聊发送的图片消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        # 切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送图片
        Preconditions.send_pic_in_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0028(self):
        """群聊会话页面，转发他人发送的图片到手机联系人时点击取消转发"""
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        group_name = '双机群聊1'
        msg.click_text(group_name)
        time.sleep(2)
        # 下载图片后长按
        chat = ChatWindowPage()
        chat.click_coordinate(25, 35)
        time.sleep(3)
        chat.click_coordinate(50, 50)
        time.sleep(1)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='编辑'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 3.选择最近聊天联系人-调起询问弹窗
        select.click_phone_contact()
        select_local = SelectLocalContactsPage()
        name = '大佬1'
        select_local.swipe_select_one_member_by_name(name)
        time.sleep(2)
        self.assertEqual(select_local.is_element_exit(text='取消'), True)
        self.assertEqual(select_local.is_element_exit(text='确定按钮'), True)
        # 4、点击取消发送按钮
        select_local.click_cancel_forward()
        self.assertTrue(select_local.is_on_this_page())

    def setUp_test_msg_xiaoliping_D_0029(self):
        """确保A手机收到群聊发送的图片消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        # 切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送图片
        Preconditions.send_pic_in_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0029(self):
        """单聊会话页面，转发他人发送的图片到团队联系人"""
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        group_name = '双机群聊1'
        msg.click_text(group_name)
        time.sleep(2)
        # 下载图片后长按
        chat = ChatWindowPage()
        chat.click_coordinate(25, 35)
        time.sleep(3)
        chat.click_coordinate(50, 50)
        time.sleep(1)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='编辑'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 3.选择团队联系人-调起询问弹窗
        select.click_he_contacts()
        group_contact = SelectHeContactsPage()
        group_contact.select_one_team_by_name('ateam7272')
        group_detail = SelectHeContactsDetailPage()
        name = '大佬3'
        group_detail.select_one_he_contact_by_name(name)
        self.assertEqual(group_detail.is_element_exit('取消'), True)
        self.assertEqual(group_detail.is_element_exit('确定'), True)
        # 4、点击发送按钮
        group_detail.click_sure()
        # 4、toast提示：已转发，返回到当前会话窗口
        self.assertTrue(chat.is_on_this_page())
        # 发送成功
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_contain_text2(name)


    def setUp_test_msg_xiaoliping_D_0031(self):
        """确保A手机收到群聊发送的图片消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        # 切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送图片
        Preconditions.send_pic_in_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0031(self):
        """单聊会话页面，转发他人发送的图片到团队联系人时取消转发"""
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        group_name = '双机群聊1'
        msg.click_text(group_name)
        time.sleep(2)
        # 下载图片后长按
        chat = ChatWindowPage()
        chat.click_coordinate(25, 35)
        time.sleep(3)
        chat.click_coordinate(50, 50)
        time.sleep(1)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='编辑'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 3.选择团队联系人-调起询问弹窗
        select.click_he_contacts()
        group_contact = SelectHeContactsPage()
        group_contact.select_one_team_by_name('ateam7272')
        group_detail = SelectHeContactsDetailPage()
        name = '大佬3'
        time.sleep(3)
        group_detail.select_one_he_contact_by_name(name)
        self.assertEqual(group_detail.is_element_exit('取消'), True)
        self.assertEqual(group_detail.is_element_exit('确定'), True)
        # 4、点击取消转发
        group_detail.click_cancel()
        time.sleep(2)
        # 4、停留在当前页面
        self.assertTrue(group_detail.is_on_this_page())

    def setUp_test_msg_xiaoliping_D_0032(self):
        """确保A手机收到群聊发送的图片消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        # 切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送图片
        Preconditions.send_pic_in_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0032(self):
        """单聊会话页面，转发他人发送的图片到给陌生人"""
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        group_name = '双机群聊1'
        msg.click_text(group_name)
        time.sleep(2)
        # 下载图片后长按
        chat = ChatWindowPage()
        chat.click_coordinate(25, 35)
        time.sleep(3)
        chat.click_coordinate(50, 50)
        time.sleep(1)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='编辑'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 3.选择陌生人-调起询问弹窗
        select.click_search_contact()
        number = '15570670329'
        select.input_search_keyword(number)
        time.sleep(2)
        select.click_search_result_from_internet(number)
        self.assertEqual(select.is_element_present(locator='取消'), True)
        self.assertEqual(select.is_element_present(locator='确定'), True)
        # 5、点击弹窗确定按钮
        select.click_sure_forward()
        time.sleep(2)
        # 4、toast提示：已转发，返回到当前会话窗口
        self.assertTrue(chat.is_on_this_page())
        # 发送成功
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_contain_text(number)

    def setUp_test_msg_xiaoliping_D_0034(self):
        """确保A手机收到群聊发送的图片消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        # 切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送图片
        Preconditions.send_pic_in_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0034(self):
        """单聊会话页面，转发他人发送的图片到陌生人时，取消转发"""
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        group_name = '双机群聊1'
        msg.click_text(group_name)
        time.sleep(2)
        # 下载图片后长按
        chat = ChatWindowPage()
        chat.click_coordinate(25, 35)
        time.sleep(3)
        chat.click_coordinate(50, 50)
        time.sleep(1)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='编辑'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 3.选择陌生人-调起询问弹窗
        select.click_search_contact()
        number = '15570670329'
        select.input_search_keyword(number)
        time.sleep(2)
        select.click_search_result_from_internet(number)
        self.assertEqual(select.is_element_present(locator='取消'), True)
        self.assertEqual(select.is_element_present(locator='确定'), True)
        # 5、点击弹窗取消按钮
        select.click_cancel_forward()
        time.sleep(2)
        self.assertTrue(select.page_should_contain_text2('选择联系人'))

    def setUp_test_msg_xiaoliping_D_0035(self):
        """确保A手机收到群聊发送的图片消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        # 切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送图片
        Preconditions.send_pic_in_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0035(self):
        """单聊会话页面，转发他人发送的图片到给群聊"""
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        group_name = '双机群聊1'
        msg.click_text(group_name)
        time.sleep(2)
        # 下载图片后长按
        chat = ChatWindowPage()
        chat.click_coordinate(25, 35)
        time.sleep(3)
        chat.click_coordinate(50, 50)
        time.sleep(1)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='编辑'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 3.选择一个普通群-调起询问弹窗
        select.click_select_one_group()
        name = '群聊1'
        time.sleep(2)
        one_group = SelectOneGroupPage()
        one_group.selecting_one_group_by_name(name)
        self.assertEqual(one_group.is_element_exit(text='取消'), True)
        self.assertEqual(one_group.is_element_exit(text='确定'), True)
        # 5、点击弹窗确定按钮
        one_group.click_sure_send()
        time.sleep(2)
        # 4、toast提示：已转发，返回到当前会话窗口
        self.assertTrue(chat.is_on_this_page())
        # 发送成功
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_contain_text(name)

    def setUp_test_msg_xiaoliping_D_0037(self):
        """确保A手机收到群聊发送的图片消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        # 切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送图片
        Preconditions.send_pic_in_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0037(self):
        """单聊会话页面，转发他人发送的图片到普通群时，取消转发"""
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        group_name = '双机群聊1'
        msg.click_text(group_name)
        time.sleep(2)
        # 下载图片后长按
        chat = ChatWindowPage()
        chat.click_coordinate(25, 35)
        time.sleep(3)
        chat.click_coordinate(50, 50)
        time.sleep(1)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='编辑'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 3.选择一个普通群-调起询问弹窗
        select.click_select_one_group()
        name = '群聊1'
        time.sleep(2)
        one_group = SelectOneGroupPage()
        self.assertTrue(one_group.is_on_this_page())
        one_group.selecting_one_group_by_name(name)
        self.assertEqual(one_group.is_element_exit(text='取消'), True)
        self.assertEqual(one_group.is_element_exit(text='确定'), True)
        # 4、点击弹窗取消按钮
        one_group.click_cancel_forward()
        time.sleep(2)
        self.assertTrue(select.is_text_present('选择一个群'))

    def setUp_test_msg_xiaoliping_D_0038(self):
        """确保A手机收到群聊发送的图片消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        # 切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送图片
        Preconditions.send_pic_in_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0038(self):
        """单聊会话页面，转发他人发送的图片到给企业群"""
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        group_name = '双机群聊1'
        msg.click_text(group_name)
        time.sleep(2)
        # 下载图片后长按
        chat = ChatWindowPage()
        chat.click_coordinate(25, 35)
        time.sleep(3)
        chat.click_coordinate(50, 50)
        time.sleep(1)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='编辑'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 3.选择一个企业群-调起询问弹窗
        select.click_select_one_group()
        name = '群聊1'
        time.sleep(2)
        one_group = SelectOneGroupPage()
        one_group.select_one_company_group()
        self.assertEqual(one_group.is_element_exit(text='取消'), True)
        self.assertEqual(one_group.is_element_exit(text='确定'), True)
        # 5、点击弹窗确定按钮
        one_group.click_sure_send()
        time.sleep(2)
        # 4、toast提示：已转发，返回到当前会话窗口
        self.assertTrue(chat.is_on_this_page())

    def setUp_test_msg_xiaoliping_D_0040(self):
        """确保A手机收到群聊发送的图片消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        # 切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送图片
        Preconditions.send_pic_in_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0040(self):
        """单聊会话页面，转发他人发送的图片到企业群时，点击取消转发"""
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        group_name = '双机群聊1'
        msg.click_text(group_name)
        time.sleep(2)
        # 下载图片后长按
        chat = ChatWindowPage()
        chat.click_coordinate(25, 35)
        time.sleep(3)
        chat.click_coordinate(50, 50)
        time.sleep(1)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='编辑'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 3.选择一个普通群-调起询问弹窗
        select.click_select_one_group()
        time.sleep(2)
        one_group = SelectOneGroupPage()
        self.assertTrue(one_group.is_on_this_page())
        one_group.select_one_company_group()
        self.assertEqual(one_group.is_element_exit(text='取消'), True)
        self.assertEqual(one_group.is_element_exit(text='确定'), True)
        # 4、点击弹窗取消按钮
        one_group.click_cancel_forward()
        time.sleep(2)
        self.assertTrue(select.page_should_contain_text2('选择一个群'))


    def setUp_test_msg_xiaoliping_D_0061(self):
        """确保A手机收到群聊发送的图片消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        # 切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送图片
        Preconditions.send_pic_in_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0061(self):
        """群聊会话页面，收藏他人发送的照片"""
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        group_name = '双机群聊1'
        msg.click_text(group_name)
        time.sleep(2)
        # 下载图片后长按
        chat = ChatWindowPage()
        chat.click_coordinate(25, 35)
        time.sleep(3)
        chat.click_coordinate(50, 50)
        time.sleep(1)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='编辑'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击收藏
        chat.click_collection()
        time.sleep(2)
        # 1.toast提醒收藏成功（无法验证）
        # 2.在我模块中的收藏可见
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        collection = MeCollectionPage()
        collection.page_should_contain_text('今天')

    def setUp_test_msg_xiaoliping_D_0065(self):
        """确保A手机收到群聊发送的视频消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        # 切换到B手机，发送视频
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送视频
        chat.send_video()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0065(self):
        """群聊会话页面，转发他人发送的视频给本地联系时点击取消转发"""
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        group_name = '双机群聊1'
        msg.click_text(group_name)
        time.sleep(2)
        # 下载视频后长按
        chat = ChatWindowPage()
        chat.click_play_video()  # 下载文件
        chat.wait_for_page_load_play_video()
        chat.swipe_by_percent_on_screen(50, 50, 50, 60)
        chat.click_cancel_previer_video()
        time.sleep(2)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 3.选择最近聊天联系人-调起询问弹窗
        select.click_phone_contact()
        select_local = SelectLocalContactsPage()
        name = '大佬1'
        select_local.swipe_select_one_member_by_name(name)
        time.sleep(2)
        self.assertEqual(select_local.is_element_exit(text='取消'), True)
        self.assertEqual(select_local.is_element_exit(text='确定按钮'), True)
        # 4、点击取消发送按钮
        select_local.click_cancel_forward()
        self.assertTrue(select_local.is_on_this_page())

    def setUp_test_msg_xiaoliping_D_0066(self):
        """确保A手机收到群聊发送的视频消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        # 切换到B手机，发送视频
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送视频
        chat.send_video()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0066(self):
        """群聊会话页面，转发他人发送的视频给陌生人"""
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        group_name = '双机群聊1'
        msg.click_text(group_name)
        time.sleep(2)
        # 下载视频后长按
        chat = ChatWindowPage()
        chat.click_play_video()  # 下载文件
        chat.wait_for_page_load_play_video()
        chat.swipe_by_percent_on_screen(50, 50, 50, 60)
        chat.click_cancel_previer_video()
        time.sleep(2)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 3.选择陌生人-调起询问弹窗
        select.click_search_contact()
        number = '15570670329'
        select.input_search_keyword(number)
        time.sleep(2)
        select.click_search_result_from_internet(number)
        self.assertEqual(select.is_element_present(locator='取消'), True)
        self.assertEqual(select.is_element_present(locator='确定'), True)
        # 5、点击弹窗确定按钮
        select.click_sure_forward()
        time.sleep(2)
        # 4、toast提示：已转发，返回到当前会话窗口
        self.assertTrue(chat.is_on_this_page())
        # 发送成功
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_contain_text(number)

    def setUp_test_msg_xiaoliping_D_0068(self):
        """确保A手机收到群聊发送的视频消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        # 切换到B手机，发送视频
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送视频
        chat.send_video()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0068(self):
        """群聊会话页面，转发他人发送的视频给陌生人时点击取消转发"""
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        group_name = '双机群聊1'
        msg.click_text(group_name)
        time.sleep(2)
        # 下载视频后长按
        chat = ChatWindowPage()
        chat.click_play_video()  # 下载文件
        chat.wait_for_page_load_play_video()
        chat.swipe_by_percent_on_screen(50, 50, 50, 60)
        chat.click_cancel_previer_video()
        time.sleep(2)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 3.选择陌生人-调起询问弹窗
        select.click_search_contact()
        number = '15570670329'
        select.input_search_keyword(number)
        time.sleep(2)
        select.click_search_result_from_internet(number)
        self.assertEqual(select.is_element_present(locator='取消'), True)
        self.assertEqual(select.is_element_present(locator='确定'), True)
        # 5、点击弹窗取消按钮
        select.click_cancel_forward()
        time.sleep(2)
        self.assertTrue(select.page_should_contain_text2('选择联系人'))


    def setUp_test_msg_xiaoliping_D_0078(self):
        """确保A手机收到群聊发送的视频消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        # 切换到B手机，发送视频
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送视频
        chat.send_video()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0078(self):
        """群聊会话页面，删除他人发送的视频"""
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        group_name = '双机群聊1'
        msg.click_text(group_name)
        time.sleep(2)
        # 下载视频后长按
        chat = ChatWindowPage()
        chat.click_play_video()  # 下载文件
        chat.wait_for_page_load_play_video()
        chat.swipe_by_percent_on_screen(50, 50, 50, 60)
        chat.click_cancel_previer_video()
        time.sleep(2)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击删除-弹出删除确认框
        chat.click_delete()
        self.assertTrue(chat.is_exist_element(locator='取消'))
        self.assertTrue(chat.is_exist_element(locator='确定按钮'))
        # 3.点击确定---删除成功，自己的会话界面无该视频
        chat.click_sure_icon()
        time.sleep(2)
        self.assertFalse(chat.is_exist_element(locator='消息列表'))

    def setUp_test_msg_xiaoliping_D_0080(self):
        """确保A手机收到群聊发送的视频消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        # 切换到B手机，发送视频
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送视频
        chat.send_video()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0080(self):
        """群聊会话页面，收藏他人发送的视频"""
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        group_name = '双机群聊1'
        msg.click_text(group_name)
        time.sleep(2)
        # 下载视频后长按
        chat = ChatWindowPage()
        chat.click_play_video()  # 下载文件
        chat.wait_for_page_load_play_video()
        chat.swipe_by_percent_on_screen(50, 50, 50, 60)
        chat.click_cancel_previer_video()
        time.sleep(2)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击收藏-收藏成功
        chat.click_collection()
        time.sleep(3)
        # 2.在我模块中的收藏可见
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        collection = MeCollectionPage()
        collection.page_should_contain_text2('今天')


    def setUp_test_msg_xiaoliping_D_0087(self):
        """确保A手机删除列表"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()


    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0087(self):
        """群聊会话页面，收藏未下载的图片"""
        # 切换到B手机，发送图片
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送图片
        chat.send_pic()
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        group_name = '双机群聊1'
        msg.click_text(group_name)
        time.sleep(2)
        # 不下载图片 直接收藏图片
        chat = ChatWindowPage()
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击收藏-toast提示下载图片后收藏
        chat.click_collection()
        time.sleep(3)


    def setUp_test_msg_xiaoqiu_0097(self):
        """确保A手机收到群聊发送的卡片消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到B手机，发送卡片
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送卡片
        chat.click_more()
        chat.click_name_card()
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬2')
        time.sleep(1)
        select.click_share_card()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0097(self):
        """在群聊会话页，点击分享过来的卡片消息体——进入到卡片链接页"""
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        group_name = '双机群聊1'
        msg.click_text(group_name)
        time.sleep(2)
        # 1、点击接收到的卡片消息体，是否可以进入到卡片链接页
        chat = ChatWindowPage()
        chat.click_business_card_list()
        time.sleep(2)
        self.assertTrue(ContactDetailsPage().is_on_this_page())

    def setUp_test_msg_xiaoqiu_0099(self):
        """确保A手机进入聊天页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_sure_have_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0099(self):
        """在群聊会话窗口，点击通话按钮——拨打多方电话（已加入群聊）"""
        # 群成员进入聊天会话页面
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        # 1、点击多方电话按钮，可以跳转到群成员联系人选择器页
        chat = GroupChatPage()
        chat.click_mutilcall()
        chat.click_feixin_call()
        self.assertTrue(chat.page_should_contain_text('搜索群成员'))
        # 2、任意选中几个群成员，点击右上角的呼叫按钮，可以成功发起呼叫
        chat.select_members_by_name('大佬1')
        chat.click_start_call_button()
        call = MultipartyCallPage()
        self.assertTrue(call.is_exists_element_by_text(text='红色挂断按钮'))


    def setUp_test_msg_xiaoqiu_0100(self):
        """确保A手机进入聊天页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_sure_have_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0100(self):
        """在群聊会话窗口，点击通话按钮——拨打多方视频（已加入群聊）"""
        # 群成员进入聊天会话页面
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        # 1、点击多方视频按钮，可以跳转到群成员联系人选择器页
        chat = GroupChatPage()
        chat.click_mutilcall()
        chat.click_video_call()
        self.assertTrue(chat.page_should_contain_text('搜索群成员'))
        # 2、任意选中几个群成员，点击右上角的呼叫按钮，可以成功发起呼叫
        chat.select_members_by_name('大佬1')
        chat.click_start_call_button()
        call = MultiPartyVideoPage()
        self.assertTrue(call.is_exists_element_by_text(text='红色挂断按钮'))

    def setUp_test_msg_xiaoqiu_0113(self):
        """群成员A进入聊天会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到B手机，发送卡片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()


    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0113(self):
        """在群聊设置页面，群成员展示列表，点击“>”"""
        # 确保群聊里有陌生人
        chat = GroupChatPage()
        chat.click_setting()
        set = GroupChatSetPage()
        set.click_add_member()
        select = SelectContactsPage()
        select.click_he_contacts()
        group_contact = SelectHeContactsPage()
        group_contact.select_one_team_by_name('ateam7272')
        group_detail = SelectHeContactsDetailPage()
        group_detail.select_one_he_contact_by_name('alice')
        group_detail.click_sure_icon()
        time.sleep(3)
        # 1、在群聊设置页面，点击群成员展示列表右上角的“>”按钮，可以跳转到群成员列表页
        chat.click_setting()
        set = GroupChatSetPage()
        set.click_enter_contact_list()
        self.assertTrue(set.is_text_present('群成员'))
        # 2、任意点击一个陌生的群成员头像，会跳转到陌生人详情页中并展示交换名片按钮
        set.click_text('138')
        time.sleep(2)
        set.page_should_contain_text('交换名片')

    def tearDown_test_msg_xiaoqiu_0113(self):
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        GroupChatPage().click_setting()
        # 解散群之后创建群
        GroupChatSetPage().dissolution_the_group()
        Preconditions.make_sure_have_group_chat()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoqiu_0114(self):
        """群成员A进入聊天会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0114(self):
        """群成员展示列表页，输入框输入号码——前3位搜索群成员（存在未设置群名称的成员）"""
        Preconditions.select_mobile('IOS-移动-移动')
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 进入群聊会话页面
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        # 进入群聊设置页面
        chat = GroupChatPage()
        chat.click_setting()
        # 进入群成员列表页面
        set = GroupChatSetPage()
        set.click_enter_contact_list()
        self.assertTrue(set.is_text_present('群成员'))
        # 1、在页面顶部的搜索框中，输入一个号码的前3位作为搜索条件进行搜索，可以搜索出对应的群成员信息
        set.click_search_group_contact()
        set.input_contact_name(phone_number_B[:3])
        time.sleep(3)
        self.assertTrue(set.is_exit_element(locator='搜索群成员结果'))

    def setUp_test_msg_xiaoqiu_0117(self):
        """群成员A进入聊天会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0117(self):
        """群成员展示列表页，输入框输入——中文字符搜索群成员"""
        chat = GroupChatPage()
        set = GroupChatSetPage()
        # 进入群聊会话页面
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        # 进入群聊设置页面
        chat.click_setting()
        # 进入群成员列表页面
        set.click_enter_contact_list()
        self.assertTrue(set.is_text_present('群成员'))
        # 1、在页面顶部的搜索框中，输入一个中文字符作为搜索条件进行搜索，可以搜索出对应的群成员信息
        set.click_search_group_contact()
        set.input_contact_name('大佬')
        time.sleep(3)
        self.assertTrue(set.is_exit_element(locator='搜索群成员结果'))

    def setUp_test_msg_xiaoqiu_0118(self):
        """群成员A进入聊天会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0118(self):
        """群成员展示列表页，输入框输入——英文字符搜索群成员"""
        chat = GroupChatPage()
        set = GroupChatSetPage()
        # 进入群聊会话页面
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        # 进入群聊设置页面
        chat.click_setting()
        # 进入群成员列表页面
        set.click_enter_contact_list()
        self.assertTrue(set.is_text_present('群成员'))
        # 1、在页面顶部的搜索框中，输入一个英文字符作为搜索条件进行搜索，可以搜索出对应的群成员信息
        set.click_search_group_contact()
        set.input_contact_name('dalao')
        time.sleep(3)
        self.assertTrue(set.is_exit_element(locator='搜索群成员结果'))

    def setUp_test_msg_xiaoqiu_0636(self):
        """群成员A进入聊天会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0636(self):
        """群成员展示列表页，输入搜索条件——搜索——不存在搜索结果时展示"""
        chat = GroupChatPage()
        set = GroupChatSetPage()
        # 进入群聊会话页面
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        # 进入群聊设置页面
        chat.click_setting()
        # 进入群成员列表页面
        set.click_enter_contact_list()
        self.assertTrue(set.is_text_present('群成员'))
        # 1、在页面顶部的搜索框中，输入一个字符作为搜索条件进行搜索，无搜索结果展示
        set.click_search_group_contact()
        set.input_contact_name('给个红包')
        time.sleep(3)
        # 1、展示无搜索结果，和缺省页
        self.assertFalse(set.is_exit_element(locator='搜索群成员结果'))


    def setUp_test_msg_xiaoqiu_0220(self):
        """群成员A进入聊天会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0220(self):
        """聊天设置页面——打开置顶聊天功能——置顶一个聊天会话窗口"""
        chat = GroupChatPage()
        set = GroupChatSetPage()
        mess = MessagePage()
        # 进入群聊设置页面-打开置顶聊天
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.click_setting()
        # 1、点击置顶聊天功能右边的开关，可以打开置顶聊天功能
        group_name = set.get_group_name()
        value = set.get_switch_top_value()
        if value == '0':
            set.click_switch_top()
        time.sleep(2)
        value2 = set.get_switch_top_value()
        self.assertEqual(value2, '1')
        # 2、置顶聊天功能开启后，返回到消息列表
        Preconditions.make_already_in_message_page()
        # 接收到一条消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.send_mutiple_message(times=1)
        # 置顶聊天会话窗口展示到页面顶部并且会话窗口成浅灰色展示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        first_list_name = mess.get_first_list_name()
        self.assertEqual(group_name, first_list_name)
        # 切换到A 手机 取消置顶状态
        MessagePage().click_text('双机群聊')
        chat.click_setting()
        value = set.get_switch_top_value()
        if value == '1':
            set.click_switch_top()
        time.sleep(2)


    def setUp_test_msg_xiaoqiu_0222(self):
        """群成员A进入聊天会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0222(self):
        """聊天设置页面——关闭置顶聊天"""
        chat = GroupChatPage()
        set = GroupChatSetPage()
        mess = MessagePage()
        # 进入群聊设置页面-关闭置顶聊天
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A(group_name='群聊1')
        chat.send_mutiple_message(times=1)
        chat.click_setting()
        # 1、点击置顶聊天功能右边的开关，关闭置顶聊天功能
        group_name = set.get_group_name()
        value = set.get_switch_top_value()
        if value == '1':
            set.click_switch_top()
        time.sleep(2)
        value2 = set.get_switch_top_value()
        self.assertEqual(value2, '0')
        # 2、置顶聊天功能关闭后，返回到消息列表
        Preconditions.make_already_in_message_page()
        first_list_name1 = mess.get_first_list_name()
        self.assertEqual(group_name, first_list_name1)
        # 接收到一条消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.send_mutiple_message(times=1)
        # 聊天会话窗口在消息列表展示时，会随着其他聊天窗口的新消息进行排序
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        if mess.is_exist_unread_make_and_number():
            mess.press_unread_make_and_move_down()
        first_list_name2 = mess.get_first_list_name()
        self.assertNotEqual(group_name, first_list_name2)

    def setUp_test_msg_xiaoqiu_0230(self):
        """群成员A进入聊天会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_sure_have_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0230(self):
        """聊天设置页面，删除并退出群聊——群主"""
        chat = GroupChatPage()
        set = GroupChatSetPage()
        mess = MessagePage()
        # 群主B进入群聊设置页面
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.click_setting()
        # 判断在聊天设置页面
        self.assertTrue(set.is_on_this_page())
        # 2、点击页面底部的“删除并退出”按钮，把群主转让给选择的群成员后，会退出当前群聊并返回到消息列表，收到一条系统消息：你已退出群
        set.click_delete_and_exit()
        set.click_transfer_of_group()
        set.select_contact_by_name('大佬1')
        time.sleep(3)
        self.assertFalse(set.is_on_this_page())
        Preconditions.make_already_in_message_page()
        self.assertTrue(mess.is_text_present('你已退出群'))
        # 群成员B
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.click_setting()
        set.exit_enterprise_group()

    def tearDown_test_msg_xiaoqiu_0230(self):
        Preconditions.make_sure_have_group_chat()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoqiu_0234(self):
        """群成员A进入聊天会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_sure_have_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0234(self):
        """消息列表页面——有人@我——然后撤回@消息"""
        chat = GroupChatPage()
        set = GroupChatSetPage()
        mess = MessagePage()
        # 获取A手机在群聊中的昵称
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.click_setting()
        nikname = set.get_my_name_in_this_group()
        Preconditions.make_already_in_message_page()
        # 切换到B手机 @ A手机
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.send_mutiple_message(times=1)
        chat.click_input_box()
        chat.input_message_text('@')
        chat.select_members_by_name(nikname)
        chat.click_send_button()
        time.sleep(2)
        # 切换到A手机 查看A手机的显示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess.wait_for_page_load_new_message_coming()
        mess.page_should_contain_text('有人@我')
        # 切换到B 手机 撤回发送的文本消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        mess.click_text('双机群聊1')
        chat.wait_for_page_load()
        chat.press_and_move_right_text_message()
        chat.click_revoke()
        time.sleep(2)
        # 验1、有人@我后再撤回@我的消息，查看消息列表页不会存在提示 有人@我  (仍旧存在@显示)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(3)
        self.assertTrue(mess.is_text_present('有人@我'))


    def setUp_test_msg_xiaoqiu_0236(self):
        """群成员A进入聊天会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_sure_have_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0236(self):
        """普通群——聊天会话页面——超长文本消息中带有@群成员"""
        chat = GroupChatPage()
        set = GroupChatSetPage()
        mess = MessagePage()
        # 获取A手机在群聊中的昵称
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.click_setting()
        nikname = set.get_my_name_in_this_group()
        Preconditions.make_already_in_message_page()
        # 切换到B手机 @ A手机
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.send_mutiple_message(times=1)
        chat.click_input_box()
        message = '超长文本'*20 + '@'
        chat.input_message_text2(message)
        chat.select_members_by_name(nikname)
        chat.click_send_button()
        time.sleep(2)
        # 切换到A手机 查看A手机的显示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess.wait_for_page_load_new_message_coming()
        mess.page_should_contain_text('有人@我')

    def setUp_test_msg_xiaoqiu_0237(self):
        """群成员A进入聊天会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_sure_have_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0237(self):
        """群聊天会话页面——复制粘贴的@内容"""
        chat = GroupChatPage()
        set = GroupChatSetPage()
        mess = MessagePage()
        # 获取A手机在群聊中的昵称
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.click_setting()
        nikname = set.get_my_name_in_this_group()
        Preconditions.make_already_in_message_page()
        # 切换到B手机 @ A手机
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.send_mutiple_message(times=1)
        chat.click_input_box()
        chat.input_message_text('@')
        chat.select_members_by_name(nikname)
        chat.click_send_button()
        time.sleep(2)
        # 取消A手机的@显示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess.wait_for_page_load_new_message_coming()
        mess.page_should_contain_text('有人@我')
        mess.click_text('双机群聊1')
        chat.click_back()
        # 切换到B 手机 复制@的内容 然后发送
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        mess.click_text('双机群聊1')
        chat.wait_for_page_load()
        chat.click_input_box()
        chat.press_and_move_right_text_message()
        chat.click_copy()
        time.sleep(2)
        chat.long_press_input_box()
        chat.click_paste()
        # 1、复制粘贴的@群成员内容，发送成功后，被@的联系人收到后，不存在@效果
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(3)
        self.assertFalse(mess.is_text_present('有人@我'))

    def setUp_test_msg_xiaoqiu_0238(self):
        """群成员A进入聊天会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_sure_have_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0238(self):
        """群聊天会话页面——输入多个@后——再选要@的群成员查看@效果"""
        chat = GroupChatPage()
        set = GroupChatSetPage()
        mess = MessagePage()
        # 获取A手机在群聊中的昵称
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.click_setting()
        nikname = set.get_my_name_in_this_group()
        Preconditions.make_already_in_message_page()
        # 同时@多个人
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.click_input_box()
        text = '@'
        chat.input_message_text2(text)
        chat.click_back()
        chat.click_input_box()
        chat.input_message_text2('@')
        chat.select_members_by_name(nikname)
        chat.click_send_button()
        time.sleep(2)
        # 1、同时@多群成员联系人，发送成功后，被@的联系人收到后，存在@效果
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess.wait_for_page_load_new_message_coming()
        mess.page_should_contain_text('有人@我')

    def setUp_test_msg_xiaoqiu_0239(self):
        """群成员A进入聊天会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_sure_have_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0239(self):
        """群聊天会话页面——同时@多个人——@效果展示"""
        chat = GroupChatPage()
        set = GroupChatSetPage()
        mess = MessagePage()
        # 获取A手机在群聊中的昵称
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.click_setting()
        nikname = set.get_my_name_in_this_group()
        Preconditions.make_already_in_message_page()
        # 同时@多个人
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.click_input_box()
        chat.input_message_text('@')
        chat.select_members_by_name(nikname)
        chat.click_input_box()
        chat.input_message_text('@')
        chat.select_members_by_name('大佬1')
        chat.click_send_button()
        time.sleep(2)
        # 1、同时@多群成员联系人，发送成功后，被@的联系人收到后，存在@效果
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess.wait_for_page_load_new_message_coming()
        mess.page_should_contain_text('有人@我')


    def setUp_test_msg_xiaoqiu_0221(self):
        # 群主A手机进入聊天会话页面
        warnings.simplefilter('ignore', ResourceWarning)

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_xiaoqiu_0221(self):
        """聊天设置页面——打开置顶聊天功能——置顶二个聊天会话窗口"""
        chat = GroupChatPage()
        mess = MessagePage()
        set = GroupChatSetPage()
        # 确保群聊置顶聊天功能开启
        # 打开第一个群的置顶聊天功能
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.send_mutiple_message(times=1)
        chat.click_setting()
        value = set.get_switch_top_value()
        if value == '0':
            set.click_switch_top()
        time.sleep(2)
        Preconditions.make_already_in_message_page()
        # 打开第二个群的置顶聊天功能
        mess.open_contacts_page()
        ContactsPage().open_group_chat_list()
        ALLMyGroup().select_group_by_name('给个红包1')
        chat.click_setting()
        value = set.get_switch_top_value()
        if value == '0':
            set.click_switch_top()
        time.sleep(2)
        group_name2 = set.get_group_name()
        Preconditions.make_already_in_message_page()
        # 2、打开二个群聊或者单聊的置顶聊天功能，后续接收到消息时，后面置顶的聊天会话窗口展示在第一个置顶的聊天会话窗口上方
        # b手机发送一条消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.send_mutiple_message(times=1)
        # 切换到A手机,查看消息列表第一条的标题名称
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        if mess.is_exist_unread_make_and_number():
            mess.press_unread_make_and_move_down()
        name = mess.get_first_list_name()
        self.assertEqual(group_name2, name)

    def tearDown_test_msg_xiaoqiu_0221(self):
        Preconditions.select_mobile('IOS-移动')
        # 去除给个红包1的置顶状态
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        my_group.select_group_by_name('给个红包1')
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        value = set.get_switch_top_value()
        if value == '1':
            set.click_switch_top()
        time.sleep(2)
        # 去除双机企业群的置顶状态
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        my_group.select_group_by_name('双机企业群1')
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        value = set.get_switch_top_value()
        if value == '1':
            set.click_switch_top()
        time.sleep(2)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_xiaoqiu_0252(self):
        """群成员A进入聊天会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保群聊人数2人
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_sure_have_group_chat()
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        GroupChatPage().click_setting()
        GroupChatSetPage().delete_member_by_name('大佬1')
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0252(self):
        """A被B——移除普通群——群聊存在群聊人数2人)"""
        chat = GroupChatPage()
        set = GroupChatSetPage()
        mess = MessagePage()
        # 获取A手机在群聊中的昵称
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.click_setting()
        nikname = set.get_my_name_in_this_group()
        Preconditions.make_already_in_message_page()
        # 群主B手机移除一名群成员
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.send_mutiple_message(times=1)
        chat.click_setting()
        set.delete_member_by_name(nikname)
        # 1、B使用群主权限把A从群聊中移除后，A会收到一体系统消息：你已被请出群
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess.wait_for_page_load_new_message_coming()
        mess.page_should_contain_text('你已被请出群')
        # 2、消息列表，会保存被移除群聊的会话窗口
        group_name = '双机群聊1'
        mess.page_should_contain_text(group_name)
        # 3、群聊人数小于2人时，会自动解散
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        time.sleep(2)
        self.assertFalse(my_group.is_text_present(group_name))


    def tearDown_test_msg_xiaoqiu_0252(self):
        """解散群之后新创建群"""
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        GroupChatPage().click_setting()
        GroupChatSetPage().dissolution_the_group()
        time.sleep(2)
        Preconditions.make_sure_have_group_chat()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_xiaoqiu_0253(self):
        """群成员A进入聊天会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_sure_have_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0253(self):
        """A被B——移除普通群——群聊存在群聊人数3人)"""
        chat = GroupChatPage()
        set = GroupChatSetPage()
        mess = MessagePage()
        # 获取A手机在群聊中的昵称
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.click_setting()
        nikname = set.get_my_name_in_this_group()
        Preconditions.make_already_in_message_page()
        # 群主B手机移除一名群成员
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.send_mutiple_message(times=1)
        chat.click_setting()
        set.delete_member_by_name(nikname)
        # 1、B使用群主权限把A从群聊中移除后，A会收到一体系统消息：你已被请出群
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess.wait_for_page_load_new_message_coming()
        mess.page_should_contain_text('你已被请出群')
        # 2、消息列表，会保存被移除群聊的会话窗口
        group_name = '双机群聊1'
        mess.page_should_contain_text(group_name)
        # 3、群聊人数大于2人时,不会解散
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        time.sleep(3)
        self.assertTrue(my_group.is_text_present(group_name))

    def tearDown_test_msg_xiaoqiu_0253(self):
        """解散群之后新创建群"""
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        GroupChatPage().click_setting()
        GroupChatSetPage().dissolution_the_group()
        time.sleep(2)
        Preconditions.make_sure_have_group_chat()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoqiu_0382(self):
        """群成员A进入聊天会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_sure_have_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0382(self):
        """验证群主在群设置页面点击—移除群成员A后,A收到的系统消息是否正确"""
        chat = GroupChatPage()
        set = GroupChatSetPage()
        mess = MessagePage()
        # 获取A手机在群聊中的昵称
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.click_setting()
        nikname = set.get_my_name_in_this_group()
        Preconditions.make_already_in_message_page()
        # 1、群主点击—删除A
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat.click_setting()
        set.delete_member_by_name(nikname)
        # 1、B使用群主权限把A从群聊中移除后，A会收到一体系统消息：你已被请出群
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess.wait_for_page_load_new_message_coming()
        mess.page_should_contain_text('你已被请出群')
        mess.page_should_contain_text('系统消息')



    def tearDown_test_msg_xiaoqiu_0382(self):
        """解散群之后新创建群"""
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        GroupChatPage().click_setting()
        GroupChatSetPage().dissolution_the_group()
        time.sleep(2)
        Preconditions.make_sure_have_group_chat()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_xiaoqiu_0384(self):
        """群成员A进入聊天会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_sure_have_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0384(self):
        """验证群主在群设置页面——修改群名称后——全员收到的提示"""
        chat = GroupChatPage()
        set = GroupChatSetPage()
        mess = MessagePage()
        # 连接到B手机,进入聊天会话页面
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        # 1、群主点击右上角的群设置按钮-成功进入群聊设置页面
        chat.click_setting()
        self.assertTrue(set.is_on_this_page())
        # 2、修改群名称后,点击右上角的完成按钮，返回到群设置页面
        name = '新双机群聊名'
        set.change_group_name(name)
        self.assertTrue(set.is_on_this_page())
        # 3、提示群名称已修改为 YY（名称前有空格）[验证群成员的群聊列表页面有新修改的群名]
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess.wait_for_page_load_new_message_coming()
        mess.open_contacts_page()
        ContactsPage().open_group_chat_list()
        time.sleep(2)
        my_group = ALLMyGroup()
        self.assertTrue(my_group.page_should_contain_text2(name))

    def tearDown_test_msg_xiaoqiu_0384(self):
        """修改群名后,修改回来"""
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load_new_message_coming()
        mess.open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        name = '新双机群聊名'
        if my_group.is_text_present(name):
            my_group.select_group_by_name(name)
            GroupChatPage().click_setting()
            GroupChatSetPage().change_group_name('双机群聊1')
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_xiaoqiu_0386(self):
        """群成员A进入聊天会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_sure_have_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0386(self):
        """验证群主在设置页面——点击群管理——点击解散群按钮后——全员收到的系统消息"""
        chat = GroupChatPage()
        set = GroupChatSetPage()
        mess = MessagePage()
        # 连接A手机 删除消息列表
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess.delete_all_message_list()
        # 连接到B手机,进入聊天会话页面
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        mess.delete_all_message_list()
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        #  1、群主点击右上角的群设置按钮，点击群管理，点击解散群，点击确认解散群
        chat.click_setting()
        set.dissolution_the_group()
        # 验证点: 1、成功删除群
        Preconditions.make_already_in_message_page()
        mess.page_should_contain_text('该群已解散')
        # 2、全员查看群消息提示--该群已解散
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess.page_should_contain_text('该群已解散')
        mess.page_should_contain_text('系统消息')

    def tearDown_test_msg_xiaoqiu_0386(self):
        """解散群之后新建群"""
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_sure_have_group_chat()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoqiu_0389(self):
        """群成员A进入聊天会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_sure_have_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0389(self):
        """验证群主在群设置页面——将所有群成员移出群后——群成员收到的群消息"""
        chat = GroupChatPage()
        set = GroupChatSetPage()
        mess = MessagePage()
        # 连接A手机 删除消息列表
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess.delete_all_message_list()
        # 连接到B手机,进入聊天会话页面
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        mess.delete_all_message_list()
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        #  1、群主点击右上角的群设置按钮，移除所有的群成员
        chat.click_setting()
        set.delete_all_member()
        time.sleep(2)
        # 验证点: 1、成功删除群
        Preconditions.make_already_in_message_page()
        mess.wait_for_page_load_new_message_coming()
        mess.page_should_contain_text('该群已解散')
        # 2、群成员查看群消息-- 2、提示：你已被请出该群
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess.wait_for_page_load_new_message_coming()
        mess.page_should_contain_text('你已被请出该群')
        mess.page_should_contain_text('系统消息')

    def tearDown_test_msg_xiaoqiu_0389(self):
        """解散群之后新建群"""
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_sure_have_group_chat()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

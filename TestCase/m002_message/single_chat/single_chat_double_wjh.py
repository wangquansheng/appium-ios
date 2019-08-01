import unittest
import time
import warnings

import dataproviders
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from preconditions.BasePreconditions import LoginPreconditions
from library.core.utils.testcasefilter import tags
from pages.chat.chatfileProview import ChatfileProviewPage
from pages.contacts.my_group import ALLMyGroup

from pages import *
from selenium.common.exceptions import TimeoutException

import re
import random
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile

REQUIRED_MOBILES = {
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
    def enter_phone_chatwindows_from_B_to_A(type1='IOS-移动', type2='IOS-移动-移动'):
        """从b手机进入与A手机的1v1对话框"""
        # 获取A手机的电话号码
        Preconditions.select_mobile(type1)
        phone_number_A = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 切换到B手机，进入与A手机的对话窗口
        Preconditions.select_mobile(type2)
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        # 搜索A手机，如果不存在就添加A手机为手机联系人，进入与A手机对话框
        msg.click_search_box()
        msg.input_search_text(phone_number_A)
        time.sleep(2)
        if msg.is_element_present(text='搜索结果列表1'):
            msg.click_element_first_list()
            time.sleep(2)
            ContactDetailsPage().click_message_icon()
        else:
            msg.click_back()
            msg.open_contacts_page()
            contact = ContactsPage()
            contact.click_phone_contact()
            contact.click_add()
            creat = CreateContactPage()
            creat.create_contact(phone_number_A, phone_number_A)
            time.sleep(2)
            ContactDetailsPage().click_message_icon()

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

    @staticmethod
    def creat_group_chatwindows_with_B_and_A(name='双机群聊1'):
        """创建同时存在A、B两个手机号的群聊，且保证A、B手机都加入该群(b手机创建群-邀请A加入)"""
        # 获取A手机的电话号码
        Preconditions.select_mobile('IOS-移动')
        phone_number_A = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        print(phone_number_A)
        # 切换到B手机，创建群（群成员有A B两台手机）
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        # B手机创建创建群
        msg.open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        my_group.click_creat_group()
        # 选择A手机 和另外一个联系人创建群组
        select = SelectContactsPage()
        time.sleep(2)
        select.click_search_box()
        select.input_search_text(phone_number_A)
        time.sleep(2)
        select.click_element_by_id(text='搜索结果列表1')
        # 选择另外一个联系人
        select.select_local_contacts()
        select.select_one_contact_by_name('大佬1')
        select.click_sure_bottom()
        # 输入群组名称页面
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
            mess.click_back()

    @staticmethod
    def make_sure_have_group_chat(group_name='双机群聊1'):
        """确保手机存在群聊"""
        # Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.open_contacts_page()
        ContactsPage().open_group_chat_list()
        time.sleep(2)
        my_group = ALLMyGroup()
        if my_group.is_text_present(group_name):
            my_group.click_back()
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
        if mess.is_text_present(group_name):
            mess.click_text(group_name)
        else:
            mess.click_search_box()
            mess.input_search_text(group_name)
            time.sleep(2)
            mess.click_element_first_list()
            time.sleep(1)

    @staticmethod
    def create_group_if_not_exits(name, phone1, phone2):
        Preconditions.make_already_in_message_page()
        conts = ContactsPage()
        conts.open_contacts_page()
        conts.open_group_chat_list()
        group_list = GroupListPage()
        group_chats = [(name, ['大佬1', '大佬2', '大佬3', '大佬4', phone1, phone2])]
        for group_name, members in group_chats:
            group_list.wait_for_page_load()
            group_list.create_group_chats_if_not_exits(group_name, members)
        group_list.click_back()
        conts.open_message_page()

    @staticmethod
    def check_group_if_exist(name):
        from pages import GroupListSearchPage
        group_search = GroupListSearchPage()
        group_search.input_search_keyword(name)
        if group_search.is_group_in_list(name):
            group_search.click_back()
        else:
            Preconditions.creat_group_chatwindows_with_B_and_A(name)

    @staticmethod
    def clear_all_top_double():
        Preconditions.connect_mobile('IOS-移动')
        page = MessagePage()
        page.clear_all_top()
        Preconditions.connect_mobile('IOS-移动-移动')
        page.clear_all_top()


# noinspection PyMethodMayBeStatic
class SingleChatDouble(TestCase):
    """单聊-双机用例"""

    @classmethod
    def setUpClass(cls) -> None:
        """类前置方法"""
        warnings.simplefilter('ignore', ResourceWarning)

    def default_setUp(self):
        """前置方法，屏蔽ResourceWarning提示，默认初始化手机「IOS-移动」"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')

    def default_tearDown(self):
        """后置方法，断开所有手机"""
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def send_message_to_someone(self, text, phone):
        """
        发送一条消息到指定联系人
        :param text: 要发送的消息体
        :param phone: 联系人的电话号码
        :return: None
        """
        mp = MessagePage()
        mp.click_add_icon()
        time.sleep(0.5)
        mp.click_new_message()
        time.sleep(0.5)
        cs = SelectContactsPage()
        cs.input_search_keyword(phone)
        time.sleep(0.5)
        cs.click_element_('搜索结果_第一个联系人')
        time.sleep(1)
        chat = ChatWindowPage()
        if chat.is_element_present_by_locator(locator='我已阅读'):
            chat.click_already_read()
            chat.click_sure_icon()
        chat.input_message_text(text)
        chat.click_send_button()
        self.assertEqual(chat.is_element_present_resend(), False)
        # chat.click_back()

    def send_message_to_one_group(self, text, name):
        """
        发送一条消息到指定群聊
        :param text: 要发送的消息体
        :param name: 群聊名称
        :return: None
        """
        mp = MessagePage()
        mp.click_add_icon()
        time.sleep(0.5)
        mp.click_group_chat()
        time.sleep(0.5)
        cs = SelectContactsPage()
        time.sleep(0.5)
        cs.click_select_one_group()
        time.sleep(0.5)
        gp = SelectOneGroupPage()
        gp.input_search_keyword(name)
        time.sleep(0.5)
        gp.select_first_group_c()
        time.sleep(1)
        chat = GroupChatPage()
        chat.input_message_text(text)
        chat.click_send_button()
        self.assertEqual(chat.is_element_present_resend(), False)
        # chat.click_back()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_0438(self):
        """

        :return:
        """
        chat = ChatWindowPage()
        Preconditions.select_mobile('IOS-移动-移动')
        phone = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.select_mobile('IOS-移动')
        self.send_message_to_someone('测试消息', phone)
        chat.click_back()
        Preconditions.select_mobile('IOS-移动-移动')
        page = MessagePage()
        page.click_msg_first_list()
        if chat.is_element_present_by_locator(locator='我已阅读'):
            chat.click_already_read()
            chat.click_sure_icon()
        chat.press_last_text_message()
        self.assertEqual(chat.is_text_present('撤回'), False)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_0468(self):
        """
        在群聊设置页面——打开置顶聊天功能——背景色展示	"1、网络正常
        2、已登录和飞信
        3、已加入普通群
        4、置顶聊天开关，关闭状态"	"1、在群聊设置页面，点击置顶聊天开关，打开置顶聊天功能
        2、返回到消息列表，打开置顶功能的会话窗口是否背景呈灰色展示并且其他未置顶的窗口接收到新消息后会展示在其下方"	"1、在群聊设置页面，点击置顶聊天开关，打开置顶聊天功能
        2、返回到消息列表，打开置顶功能的会话窗口背景呈灰色展示并且其他未置顶的窗口接收到新消息后会展示在其下方"
        """
        Preconditions.clear_all_top_double()
        page = MessagePage()
        page.click_contacts()
        name = "test_群聊1"
        Preconditions.select_mobile('IOS-移动-移动')
        phone2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.check_group_if_exist(name)
        Preconditions.connect_mobile('IOS-移动')
        self.send_message_to_someone('测试消息', phone2)
        ChatWindowPage().click_back()
        page.press_and_move_left('第一条聊天记录')
        page.click_list_to_be_top()
        Preconditions.connect_mobile('IOS-移动-移动')
        self.send_message_to_one_group('测试消息', name)
        GroupChatPage().click_back()
        Preconditions.connect_mobile('IOS-移动')
        text = page.get_element_text('第一条聊天记录_名称')
        self.assertEqual(text == name, False)
        Preconditions.clear_all_top_double()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_0471_01(self):
        """
        群聊会话窗口——长按——删除消息	"1、网络正常
        2、已登录和飞信
        3、已加入普通群
        4、停留在群聊会话页面"	"1、长按自己发送的消息
        2、点击删除
        3.长按对方发的信息
        4、点击删除"	"1、弹出选择框：复制、转发、撤回、删除
        2、自己的群会话窗口中显示已被删除。
        3.弹出选择框：复制、转发、撤回、删除
        4.自己的群会话窗口中显示已被删除"
        :return:
        """
        Preconditions.clear_all_top_double()
        name = "test_群聊1"
        MessagePage().click_contacts()
        Preconditions.check_group_if_exist(name)
        Preconditions.select_mobile('IOS-移动')
        import uuid
        msg = '测试消息%s' % uuid.uuid4()
        self.send_message_to_one_group(msg, name)
        chat = GroupChatPage()
        chat.press_last_text_message_c()
        time.sleep(1)
        self.assertEqual(chat.is_element_exit_c('收藏_c'), True)
        self.assertEqual(chat.is_element_exit_c('转发_c'), True)
        self.assertEqual(chat.is_element_exit_c('删除_c'), True)
        self.assertEqual(chat.is_element_exit_c('撤回_c'), True)
        chat.click_element_('删除_c')
        time.sleep(1)
        if chat.is_element_exit_c('最后一条文本消息_c'):
            self.assertEqual(chat.get_element_text('最后一条文本消息_c') == msg, False)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_0471_02(self):
        """
        群聊会话窗口——长按——删除消息	"1、网络正常
        2、已登录和飞信
        3、已加入普通群
        4、停留在群聊会话页面"	"1、长按自己发送的消息
        2、点击删除
        3.长按对方发的信息
        4、点击删除"	"1、弹出选择框：复制、转发、撤回、删除
        2、自己的群会话窗口中显示已被删除。
        3.弹出选择框：复制、转发、撤回、删除
        4.自己的群会话窗口中显示已被删除"
        :return:
        """
        Preconditions.clear_all_top_double()
        name = "test_群聊1"
        MessagePage().click_contacts()
        Preconditions.check_group_if_exist(name)
        Preconditions.select_mobile('IOS-移动')
        import uuid
        msg = '测试消息%s' % uuid.uuid4()
        self.send_message_to_one_group(msg, name)
        Preconditions.connect_mobile('IOS-移动-移动')
        MessagePage().click_msg_first_list()
        chat = GroupChatPage()
        chat.press_last_text_message_c()
        time.sleep(1)
        self.assertEqual(chat.is_element_exit_c('收藏_c'), True)
        self.assertEqual(chat.is_element_exit_c('转发_c'), True)
        self.assertEqual(chat.is_element_exit_c('删除_c'), True)
        chat.click_element_('删除_c')
        time.sleep(1)
        chat.click_name_attribute_by_name('确定')
        time.sleep(1)
        if chat.is_element_exit_c('最后一条文本消息_c'):
            self.assertEqual(chat.get_element_text('最后一条文本消息_c') == msg, False)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoqiu_0403(self):
        """
        验证群主A点击消息列表右上角的+——发起群聊/点对点建群/点击通讯录右上角，创建群后被邀请人收到的系统消息	"1、已登录客户端
        2、网络正常
        3、当前消息列表口页面"	"1、A选择联系人后进行创建群
        2、被邀请人点击查看系统消息"	"1、A选择联系人后进行创建群
        2、被邀请人点击查看系统消息"
        :return:
        """
        Preconditions.connect_mobile('IOS-移动-移动')
        phone = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.connect_mobile('IOS-移动')
        mp = MessagePage()
        mp.click_add_icon()
        time.sleep(1)
        mp.click_group_chat()
        time.sleep(1)
        cont = SelectContactsPage()
        cont.click_element_('面对面建群')
        time.sleep(1)
        import random
        num = str(random.randint(1000, 9999))
        for i in num:
            cont.click_name_attribute_by_name("cc number keypad %s" % i)
            time.sleep(3)
        while not cont.is_element_exit_:
            num = str(random.randint(1000, 9999))
            for i in num:
                cont.click_name_attribute_by_name("cc number keypad %s" % i)
                time.sleep(3)
        cont.click_element_('加入群聊')
        time.sleep(3)
        GroupChatPage().click_setting()
        time.sleep(1)
        set_page = GroupChatSetPage()
        set_page.add_member_by_phone(phone)
        Preconditions.connect_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        mp.click_text('系统消息')





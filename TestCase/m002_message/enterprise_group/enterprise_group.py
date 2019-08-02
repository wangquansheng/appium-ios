import unittest
import time
import warnings
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from pages.workbench.create_group.CreateGroup import CreateGroupPage
from pages.workbench.group_messenger.SelectCompanyContacts import SelectCompanyContactsPage
from preconditions.BasePreconditions import LoginPreconditions
from library.core.utils.testcasefilter import tags
from pages.chat.chatfileProview import ChatfileProviewPage
from pages.contacts.my_group import ALLMyGroup
from pages.chat.ChatMultipartySelectContacts import ChatmultipartySelectContacts
from pages.chat.AlreadyReadPage import AlreadyReadDynamic

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
    def disconnect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(category)
        client.disconnect_mobile()
        return client


    @staticmethod
    def enter_enterprise_group_by_name(name='测试企业群1'):
        """进入企业群聊天窗口"""
        # 进入企业群会话页面
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        MessagePage().open_contacts_page()
        con = ContactsPage()
        con.open_group_chat_list()
        my_group = ALLMyGroup()
        if my_group.is_text_present(name):
            my_group.select_group_by_name(name)
        else:
            my_group.click_back()
            con.open_workbench_page()
            Preconditions.creat_enterprise_group(name=name)

    @staticmethod
    def creat_enterprise_group(name='测试企业群1'):
        """创建企业群"""
        work = WorkbenchPage()
        work.wait_for_page_load()
        work.page_up()
        work.click_add_create_group()
        # 进入创建群页面
        cgp = CreateGroupPage()
        cgp.wait_for_page_load()
        time.sleep(7)
        cgp.click_create_group()
        # 进入选择联系人页面
        sccp = SelectCompanyContactsPage()
        sccp.click_name_attribute_by_name('大佬1', "xpath")
        sccp.click_name_attribute_by_name('大佬2', "xpath")
        sccp.click_sure_button()
        # 进入创建群命名界面
        cgp.input_group_name(name)
        # 收起键盘
        cgp.click_name_attribute_by_name("完成")
        cgp.click_create_group()
        time.sleep(6)
        # 点击【马上发起群聊-进入聊天界面
        cgp.click_name_attribute_by_name("发起群聊")
        time.sleep(2)

    @staticmethod
    def make_sure_message_list_have_record(text='测试企业群1'):
        """确保消息列表有消息记录"""
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        # 确保消息列表有消息记录
        if mess.is_text_present(text):
            time.sleep(2)
        else:
            # 进入群聊消息列表页面-发送消息 保证消息列表有消息记录
            mess.click_add_icon()
            mess.click_group_chat()
            select = SelectContactsPage()
            time.sleep(2)
            select.click_select_one_group()
            select_group = SelectOneGroupPage()
            select_group.selecting_one_group_by_name(text)
            time.sleep(2)
            chat = ChatWindowPage()
            chat.click_input_box()
            chat.input_message_text('消息记录')
            chat.click_send_button()
            Preconditions.make_already_in_message_page()


class EnterpriseGroup(TestCase):
    """企业群页面"""

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_enterprise_group_by_name()

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    def setUp_test_msg_huangmianhua_0013(self):
        # 消息页面右上角点击+--发起群聊
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0013(self):
        """消息--右上角“+”--发起群聊--选择一个群——选择一个企业群/党群"""
        # 选择联系人页面
        select = SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        select.click_select_one_group()
        # 选择一个企业群--测试企业群1
        select_group = SelectOneGroupPage()
        select_group.find_one_group_by_name(name='测试企业群1')
        time.sleep(3)
        select_group.page_should_contain_text('测试企业群')
        self.assertTrue(select_group.is_element_exit(text='企业群标志'))

    def setUp_test_msg_huangmianhua_0015(self):
        # 消息页面右上角点击+--发起群聊
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0015(self):
        """消息--右上角“+”--发起群聊--选择一个群——选择一个企业群/党群-群主在群聊设置页有拉人“+”和踢人“-”按钮"""
        # 选择联系人页面
        select = SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        select.click_select_one_group()
        # 选择一个企业群--测试企业群1
        select_group = SelectOneGroupPage()
        select_group.selecting_one_group_by_name('测试企业群1')
        time.sleep(2)
        chat = ChatWindowPage()
        chat.click_setting()
        set = GroupChatSetPage()
        time.sleep(3)
        self.assertTrue(set.is_exit_element(locator='添加成员'))
        self.assertTrue(set.is_exit_element(locator='删除成员'))

    def setUp_test_msg_huangmianhua_0018(self):
        # 消息页面右上角点击+--发起群聊
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()  # 删除所有的消息记录
        mess.click_add_icon()
        mess.click_group_chat()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0018(self):
        """消息--右上角“+”--发起群聊--选择一个群——选择一个企业群/党群-消息列表内有消息记录的和消息列表内没有消息记录的"""
        # 选择联系人页面
        select = SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        select.click_select_one_group()
        # 选择一个企业群--测试企业群1
        select_group = SelectOneGroupPage()
        select_group.selecting_one_group_by_name('测试企业群1')
        time.sleep(2)
        chat = ChatWindowPage()
        # 1.验证点：消息列表没有记录时--正常进入
        time.sleep(3)
        self.assertTrue(chat.is_on_this_page())
        # 消息列表有消息记录时
        # 确保消息列表有消息记录
        chat.click_input_box()
        chat.input_message_text('消息记录')
        chat.click_send_button()
        # 再次进入 消息列表正常显示
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        select = SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        select.click_select_one_group()
        # 选择一个企业群--测试企业群1
        select_group = SelectOneGroupPage()
        select_group.selecting_one_group_by_name('测试企业群1')
        time.sleep(2)
        chat = ChatWindowPage()
        # 2.验证点：有消息记录时，消息记录正常显示
        self.assertTrue(chat.is_element_present_message_list())

    def setUp_test_msg_huangmianhua_0020(self):
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保消息列表有消息记录
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_sure_message_list_have_record()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0020(self):
        """消息列表入口-群主在群聊设置页有拉人“+”和踢人“-”按钮"""
        mess = MessagePage()
        # 从消息列表进入
        mess.click_text('测试企业群1')
        chat = ChatWindowPage()
        time.sleep(2)
        self.assertTrue(chat.is_on_this_page())
        chat.click_setting()
        set = GroupChatSetPage()
        # 1.验证点：群主在群聊设置页有拉人“+”和踢人“-”按钮
        time.sleep(2)
        self.assertTrue(set.is_exit_element(locator='添加成员'))
        self.assertTrue(set.is_exit_element(locator='删除成员'))

    def setUp_test_msg_huangmianhua_0023(self):
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保消息列表有消息记录
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_sure_message_list_have_record()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0023(self):
        """企业群/党群在消息列表内展示"""
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        time.sleep(2)
        # 从消息列表进入
        self.assertTrue(mess.is_text_present(text='测试企业群'))
        self.assertTrue(mess.is_element_present(text='企业群标识'))
        self.assertTrue(mess.is_element_present(text='对话消息头像1'))

    def setUp_test_msg_huangmianhua_0043(self):
        warnings.simplefilter('ignore', ResourceWarning)
        # 进入企业群聊天窗口
        Preconditions.select_mobile('IOS-移动')
        name = '双机群聊1'
        if MessagePage().is_text_present(name):
            MessagePage().click_text(name)
        else:
            Preconditions.enter_enterprise_group_by_name()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0043(self):
        """企业群/党群在消息列表内展示——最新消息展示——草稿"""
        # 聊天窗口，输入消息不发送
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_input_box()
        text = 'send message'
        chat.input_message_text(text)
        chat.click_back()
        # 返回消息列表查看列表展示
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        time.sleep(2)
        mess.page_should_contain_text('草稿')
        mess.page_should_contain_text(text)


    def setUp_test_msg_huangmianhua_0066(self):
        warnings.simplefilter('ignore', ResourceWarning)
        # 创建新的企业群
        Preconditions.select_mobile('IOS-移动')
        name = '测试企业群2'
        mess = MessagePage()
        mess.open_workbench_page()
        Preconditions.creat_enterprise_group(name=name)
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0066(self):
        """通讯录——群聊入口——群聊列表入口-新加入的企业群应及时在列表展示"""
        # 从通讯录-群聊入口进入群聊列表
        mess = MessagePage()
        mess.click_contacts()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        my_group.page_should_contain_text('测试企业群2')

    def tearDown_test_msg_huangmianhua_0066(self):
        # 删除新创建的群
        chat = GroupChatPage()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        ContactsPage().open_group_chat_list()
        group = ALLMyGroup()
        text = '测试企业群2'
        if group.is_text_present(text):
            group.select_group_by_name(text)
            time.sleep(2)
            chat.click_setting()
            GroupChatSetPage().dissolution_the_group()
        time.sleep(4)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    def setUp_test_msg_huangmianhua_0068(self):
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保进入企业群聊天页面
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_enterprise_group_by_name()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0068(self):
        """通讯录——群聊入口——群聊列表入口-普通成员在群聊设置页没有拉人“+”和踢人“-”按钮"""
        # 从通讯录-群聊入口进入群聊列表
        chat = ChatWindowPage()
        chat.click_setting()
        set = GroupChatSetPage()
        # 1.验证点：群主在群聊设置页有拉人“+”和踢人“-”按钮
        time.sleep(2)
        self.assertTrue(set.is_exit_element(locator='添加成员'))
        self.assertTrue(set.is_exit_element(locator='删除成员'))

    def setUp_test_msg_huangmianhua_0071(self):
        # 消息页面右上角点击+--发起群聊
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()  # 删除所有的消息记录
        mess.click_contacts()
        ContactsPage().open_group_chat_list()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0071(self):
        """通讯录——群聊入口——群聊列表入口——选择一个企业群/党群-消息列表内有消息记录的和消息列表内没有消息记录的"""
        # 选择联系人页面
        my_group = ALLMyGroup()
        text = '测试企业群1'
        my_group.select_group_by_name(text)
        time.sleep(2)
        chat = ChatWindowPage()
        # 1.验证点：消息列表没有记录时--正常进入
        time.sleep(3)
        self.assertTrue(chat.is_on_this_page())
        # 消息列表有消息记录时
        # 确保消息列表有消息记录
        chat.click_input_box()
        chat.input_message_text('消息记录')
        chat.click_send_button()
        # 再次进入 消息列表正常显示
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.click_contacts()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        text = '测试企业群1'
        my_group.select_group_by_name(text)
        time.sleep(2)
        chat = ChatWindowPage()
        # 2.验证点：有消息记录时，消息记录正常显示
        self.assertTrue(chat.is_element_present_message_list())

    def setUp_test_msg_huangmianhua_0072(self):
        warnings.simplefilter('ignore', ResourceWarning)
        # 创建新的企业群
        Preconditions.select_mobile('IOS-移动')
        name = '测试企业群2'
        mess = MessagePage()
        mess.open_workbench_page()
        Preconditions.creat_enterprise_group(name=name)
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0072(self):
        """通讯录——群聊入口——搜索结果入口-新加入的企业群应及时在搜索展示"""
        # 从通讯录-群聊入口进入群聊列表
        mess = MessagePage()
        mess.click_contacts()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        text = '测试企业群2'
        my_group.click_search_box()
        my_group.input_search_keyword(text)
        time.sleep(2)
        self.assertTrue(my_group.is_exist_search_result())
        my_group.click_back()

    def tearDown_test_msg_huangmianhua_0072(self):
        # 删除新创建的群
        chat = GroupChatPage()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        ContactsPage().open_group_chat_list()
        group = ALLMyGroup()
        text = '测试企业群2'
        if group.is_text_present(text):
            group.select_group_by_name(text)
            time.sleep(2)
            chat.click_setting()
            GroupChatSetPage().dissolution_the_group()
        time.sleep(4)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    def setUp_test_msg_huangmianhua_0074(self):
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        # 进入企业群会话页面
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        MessagePage().open_contacts_page()
        con = ContactsPage()
        con.open_group_chat_list()
        my_group = ALLMyGroup()
        my_group.click_search_box()
        my_group.input_search_keyword('测试企业群1')
        time.sleep(2)
        my_group.click_search_result()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0074(self):
        """通讯录——群聊入口——搜索结果入口-普通成员在群聊设置页没有拉人“+”和踢人“-”按钮"""
        # 从通讯录-群聊入口进入群聊列表
        chat = ChatWindowPage()
        chat.click_setting()
        set = GroupChatSetPage()
        # 1.验证点：群主在群聊设置页有拉人“+”和踢人“-”按钮
        time.sleep(2)
        self.assertTrue(set.is_exit_element(locator='添加成员'))
        self.assertTrue(set.is_exit_element(locator='删除成员'))

    def setUp_test_msg_huangmianhua_0077(self):
        # 消息页面右上角点击+--发起群聊
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()  # 删除所有的消息记录
        mess.click_contacts()
        ContactsPage().open_group_chat_list()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0077(self):
        """通讯录——群聊入口——搜索结果入口——选择一个企业群/党群-消息列表内有消息记录的和消息列表内没有消息记录的"""
        # 点击搜索框搜索
        chat = ChatWindowPage()
        my_group = ALLMyGroup()
        my_group.click_search_box()
        my_group.input_search_keyword('测试企业群1')
        time.sleep(2)
        my_group.click_search_result()
        # 1.验证点：消息列表没有记录时--正常进入
        time.sleep(3)
        self.assertTrue(chat.is_on_this_page())
        # 确保消息列表有消息记录
        chat.click_input_box()
        chat.input_message_text('消息记录')
        chat.click_send_button()
        # 再次进入 消息列表正常显示
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.click_contacts()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        my_group.click_search_box()
        my_group.input_search_keyword('测试企业群1')
        time.sleep(2)
        my_group.click_search_result()
        time.sleep(2)
        chat = ChatWindowPage()
        # 2.验证点：有消息记录时，消息记录正常显示
        self.assertTrue(chat.is_element_present_message_list())


class EnterpriseChatpage(TestCase):
    """企业群--群内功能"""
    
    def default_setUp(self):
        """确保进入企业群会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_enterprise_group_by_name()

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0090(self):
        """企业群——群内功能-左上角“<”返回功能"""
        chat = ChatWindowPage()
        time.sleep(2)
        # 左上角有返回功能
        self.assertTrue(chat.is_exist_element(locator='返回'))
        # 点击返回按钮，正常返回
        chat.click_back()
        time.sleep(2)
        self.assertFalse(chat.is_on_this_page())

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0092(self):
        """企业群——群内功能——多方电话、多方视频入口——选择弹窗"""
        chat = ChatWindowPage()
        time.sleep(2)
        # 1、点击右上角“多方电话/多方视频”按钮
        chat.click_group_call_icon()
        # 验证点：1、“多方电话/多方视频”弹窗正常弹出
        self.assertTrue(chat.is_exist_element(locator='飞信电话(免费)'))
        self.assertTrue(chat.is_exist_element(locator='多方视频'))
        # 弹框样式正常--无法判断
        # 验证点：3、点击弹窗外区域弹窗是否收回
        chat.click_coordinate(50, 30)
        self.assertFalse(chat.is_exist_element(locator='多方视频'))

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0093(self):
        """企业群——群内功能——多方电话、多方视频入口——多方电话-正常弹出联系人选择器"""
        chat = ChatWindowPage()
        time.sleep(2)
        # 1、点击右上角“多方电话/多方视频”按钮
        chat.click_group_call_icon()
        self.assertTrue(chat.is_exist_element(locator='飞信电话(免费)'))
        self.assertTrue(chat.is_exist_element(locator='多方视频'))
        # 点击多方通话
        chat.click_feixin_call()
        # 验证点：正常弹出联系人选择器
        select = ChatmultipartySelectContacts()
        select.wait_for_page_load()
        self.assertTrue(select.is_on_this_page())

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0094(self):
        """企业群——群内功能——多方电话、多方视频入口——多方电话-功能正常"""
        chat = ChatWindowPage()
        time.sleep(2)
        # 1、点击右上角“多方电话/多方视频”按钮
        chat.click_group_call_icon()
        self.assertTrue(chat.is_exist_element(locator='飞信电话(免费)'))
        self.assertTrue(chat.is_exist_element(locator='多方视频'))
        # 点击多方通话
        chat.click_feixin_call()
        # 验证点：正常弹出联系人选择器
        select = ChatmultipartySelectContacts()
        select.wait_for_page_load()
        self.assertTrue(select.is_on_this_page())
        # 选择联系人后  可以正常呼叫(呼叫页面 页面id难以获取)
        select.select_one_contact_by_name(name='大佬1')
        select.click_call()
        time.sleep(3)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0097(self):
        """企业群——群内功能——多方电话、多方视频入口——多方视频-正常弹出联系人选择器"""
        chat = ChatWindowPage()
        time.sleep(2)
        # 1、点击右上角“多方电话/多方视频”按钮
        chat.click_group_call_icon()
        self.assertTrue(chat.is_exist_element(locator='飞信电话(免费)'))
        self.assertTrue(chat.is_exist_element(locator='多方视频'))
        # 点击多方视频
        chat.click_video_call()
        # 验证点：正常弹出联系人选择器
        select = ChatmultipartySelectContacts()
        select.wait_for_page_load()
        self.assertTrue(select.is_on_this_page())

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0098(self):
        """企业群——群内功能——多方电话、多方视频入口——多方视频-功能正常"""
        chat = ChatWindowPage()
        time.sleep(2)
        # 1、点击右上角“多方电话/多方视频”按钮
        chat.click_group_call_icon()
        self.assertTrue(chat.is_exist_element(locator='飞信电话(免费)'))
        self.assertTrue(chat.is_exist_element(locator='多方视频'))
        # 点击多方通话
        chat.click_video_call()
        # 验证点：正常弹出联系人选择器
        select = ChatmultipartySelectContacts()
        select.wait_for_page_load()
        self.assertTrue(select.is_on_this_page())
        # 选择联系人后  可以正常呼叫(呼叫页面 页面id难以获取)
        select.select_one_contact_by_name(name='大佬1')
        select.click_call()
        time.sleep(3)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0115(self):
        """企业群-群主——添加一个成员"""
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_setting()
        # 1、点击添加成员的“+”号按钮，是否可以跳转到联系人选择器页面
        set = GroupChatSetPage()
        set.click_add_member()
        select_he = SelectHeContactsDetailPage()
        # 验证点：1.可以跳转到联系人选择器页面
        self.assertTrue(select_he.is_on_this_page())
        # 2.任意选中一个联系人，点击右上角的确定按钮，是否会向邀请人发送一条消息
        select_he.select_one_he_contact_by_name(name='alice')
        select_he.click_sure_icon()
        # 验证点：2.会向邀请人发送一条消息(无法验证toast 使用判断是否跳转页面来判断)
        time.sleep(2)
        chat.wait_for_page_load()
        self.assertTrue(chat.is_on_this_page())

    def tearDown_test_msg_huangmianhua_0115(self):
        # 恢复环境 删除企业群联系人alice
        chat = ChatWindowPage()
        if chat.is_on_this_page:
            chat.click_setting()
        else:
            Preconditions.enter_enterprise_group_by_name()
            chat.click_setting()
        set = GroupChatSetPage()
        set.click_del_member()
        text = 'alice'
        if set.is_text_present(text):
            set.select_contact_by_name(text)
            set.click_sure()
            set.click_sure_icon()  #弹出框点击确定
        time.sleep(2)
        set.wait_for_page_load()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0116(self):
        """选择已在群聊中的联系人"""
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_setting()
        # 1、点击添加成员的“+”号按钮，是否可以跳转到联系人选择器页面
        set = GroupChatSetPage()
        set.click_add_member()
        select_he = SelectHeContactsDetailPage()
        # 验证点：1.可以跳转到联系人选择器页面
        self.assertTrue(select_he.is_on_this_page())
        # 2.选择一个已存在当前群聊的联系人
        select_he.select_one_he_contact_by_name(name='大佬1')
        select_he.click_sure_icon()
        # 验证点：2.弹出toast提示：该联系人不可选并且选择失败(无法验证toast 使用判断是否跳转页面来判断)
        time.sleep(2)
        set.page_should_contain_text('选择联系人')

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0117(self):
        """存在一个群成员时——点击移除成员按钮（群人数为2）"""
        # 进入群聊设置页面
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_setting()
        # 确保群人数是两人（目前群成员为3人 需删除一个成员即可）
        set = GroupChatSetPage()
        set.delete_member_by_name('大佬1')
        time.sleep(2)
        # 2、选中唯一群成员，点击右上角的确定按钮，确认移除此群成员
        set.click_del_member()
        set.click_menber_list_first_member()
        time.sleep(2)
        set.click_sure()
        time.sleep(2)
        set.click_sure_icon()
        time.sleep(2)
        # 确认移除此群成员
        self.assertTrue(set.is_on_this_page())
        # 验证点：3、群成员被移除成功后，当前群聊会自动解散并且群主会收到一条系统消息：该群已解散
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        MessagePage().page_should_contain_text('该群已解散')
        MessagePage().click_text('系统消息')
        time.sleep(2)


    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0118(self):
        """群主——移除一个群成员(群聊人数3)"""
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_setting()
        # 1、点击添加成员的“+”号按钮，是否可以跳转到联系人选择器页面
        set = GroupChatSetPage()
        set.click_del_member()
        # 验证点：1.可以跳转到移除页面
        self.assertTrue(set.is_text_present('移除群成员'))
        # 2.选择一个已存在当前群聊的联系人
        set.select_contact_by_name('大佬1')
        time.sleep(2)
        set.click_sure()
        time.sleep(2)
        set.click_sure_icon()
        # 验证点：2、群成员被移除成功后，当前群聊不会自动解散并收到一条系统消息：该群已解散（群成员>=2，不会解散）(使用判断是否跳转页面来判断)
        time.sleep(2)
        set.wait_for_page_load()
        self.assertTrue(set.is_on_this_page())

    def tearDown_test_msg_huangmianhua_0118(self):
        # 删除成员后，添加成员
        set = GroupChatSetPage()
        select_he = SelectHeContactsDetailPage()
        if set.is_text_present('大佬1'):
            pass
        else:
            set.click_add_member()
            select_he.wait_for_he_contacts_page_load()
            select_he.select_one_he_contact_by_name(name='大佬1')
            select_he.click_sure_icon()
            time.sleep(3)
            ChatWindowPage().wait_for_page_load()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0119(self):
        """群主——移除2个群成员(群聊人数3)"""
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_setting()
        # 移除群成员
        set = GroupChatSetPage()
        set.click_del_member()
        time.sleep(2)
        set.select_contact_by_name('大佬1')
        set.select_contact_by_name('大佬2')
        set.click_sure()
        time.sleep(2)
        set.click_sure_icon()
        # 验证点：群成员被移除成功后，当前群聊会自动解散并且收到一条系统消息：该群已解散
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        MessagePage().page_should_contain_text('该群已解散')
        MessagePage().click_text('系统消息')
        time.sleep(2)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0120(self):
        """群聊设置页面——查找聊天内容"""
        chat = ChatWindowPage()
        # 确保聊天页面存在文本信息
        chat.send_mutiple_message(times=1)
        # 进入查找聊天内容页面
        time.sleep(2)
        chat.click_setting()
        set = GroupChatSetPage()
        set.click_find_chat_record()
        time.sleep(2)
        # 验证点：1、点击聊天内容入口，跳转到聊天内容页面
        self.assertTrue(set.is_exit_element(locator='输入关键字快速搜索'))
        # 2、点击顶部的搜索框，调起小键盘
        set.click_input_box()
        self.assertTrue(set.is_keyboard_shown())

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0140(self):
        """在聊天会话页面，长按文本消息——转发——选择一个群作为转发对象"""
        chat = ChatWindowPage()
        # 确保聊天页面有消息记录
        time.sleep(2)
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面
        chat.swipe_by_percent_on_screen(67, 21, 80, 21)
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        select = SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        # 2、选择一个群，进入到群聊列表展示页面，任意选中一个群聊，确认转发，会在消息列表，重新产生一个新的会话窗口或者在已有窗口中增加一条记录
        select.click_select_one_group()
        one_group = SelectOneGroupPage()
        group_name = '群聊1'
        one_group.selecting_one_group_by_name(group_name)
        one_group.click_sure_send()
        time.sleep(2)
        Preconditions.make_already_in_message_page()
        self.assertTrue(MessagePage().is_text_present(group_name))
        # 3、进入到聊天会话窗口页面，转发的消息，已发送成功并正常展示
        MessagePage().click_text(group_name)
        chat.wait_for_page_load()
        time.sleep(3)
        self.assertTrue(chat.is_element_present_message_list())


    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0141(self):
        """在聊天会话页面，长按文本消息——转发——选择和通讯录联系人"""
        chat = ChatWindowPage()
        # 确保聊天页面有消息记录
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面
        chat.swipe_by_percent_on_screen(67, 21, 80, 21)
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        select = SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        # 2、选择和通讯录人联系人，确认转发，会在消息列表，重新产生一个新的会话窗口或者在已有窗口中增加一条记录
        select.click_group_contact()
        group_contact = SelectHeContactsPage()
        group_contact.select_one_team_by_name('ateam7272')
        group_detail = SelectHeContactsDetailPage()
        group_detail.wait_for_he_contacts_page_load()
        name = '13800137005'
        group_detail.select_one_he_contact_by_number(name)
        group_detail.click_sure()
        time.sleep(2)
        Preconditions.make_already_in_message_page()
        self.assertTrue(MessagePage().is_text_present(name))
        # 3、进入到聊天会话窗口页面，转发的消息，已发送成功并正常展示
        MessagePage().click_text(name)
        chat.wait_for_page_load()
        time.sleep(3)
        self.assertTrue(chat.is_element_present_message_list())

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0142(self):
        """在聊天会话页面，长按文本消息——转发——选择本地联系人"""
        chat = ChatWindowPage()
        # 确保聊天页面有消息记录
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面
        chat.swipe_by_percent_on_screen(67, 21, 80, 21)
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        select = SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        # 2、选择本地联系人，确认转发，会在消息列表，重新产生一个新的会话窗口或者在已有窗口中增加一条记录
        select.select_local_contacts()
        local_contact = SelectLocalContactsPage()
        self.assertEqual(local_contact.is_on_this_page(), True)
        name = '大佬2'
        local_contact.swipe_select_one_member_by_name(name)
        local_contact.click_sure()
        time.sleep(2)
        Preconditions.make_already_in_message_page()
        self.assertTrue(MessagePage().is_text_present(name))
        # 3、进入到聊天会话窗口页面，转发的消息，已发送成功并正常展示
        MessagePage().click_text(name)
        chat.wait_for_page_load()
        time.sleep(3)
        self.assertTrue(chat.is_element_present_message_list())

    def setUp_test_msg_huangmianhua_0143(self):
        """确保进入企业群会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        name = '测试企业群1'
        # 进入企业群会话页面
        Preconditions.make_already_in_message_page()
        # MessagePage().delete_all_message_list()
        MessagePage().open_contacts_page()
        con = ContactsPage()
        con.open_group_chat_list()
        my_group = ALLMyGroup()
        if my_group.is_text_present(name):
            my_group.select_group_by_name(name)
        else:
            my_group.click_back()
            con.open_workbench_page()
            Preconditions.creat_enterprise_group(name=name)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0143(self):
        """在聊天会话页面，长按文本消息——转发——选择最近聊天联系人"""
        chat = ChatWindowPage()
        # 确保聊天页面有消息记录
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面
        chat.swipe_by_percent_on_screen(67, 21, 80, 21)
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        select = SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        # 2、选择最近聊天联系人，确认转发，会在消息列表，重新产生一个新的会话窗口或者在已有窗口中增加一条记录
        name = select.get_recent_chat_contact_name()
        select.click_recent_chat_contact()
        select.click_sure_forward()
        time.sleep(2)
        Preconditions.make_already_in_message_page()
        self.assertTrue(MessagePage().is_text_present(name))
        # 3、进入到聊天会话窗口页面，转发的消息，已发送成功并正常展示
        MessagePage().click_text(name)
        chat.wait_for_page_load()
        time.sleep(3)
        self.assertTrue(chat.is_element_present_message_list())

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0144(self):
        """在聊天会话页面，长按文本消息——转发——收藏"""
        chat = ChatWindowPage()
        # 确保聊天页面有消息记录
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择收藏功能，弹出toast提示：已收藏（toast 暂时无法验证）
        chat.swipe_by_percent_on_screen(67, 21, 80, 21)
        time.sleep(2)
        chat.click_collection()
        time.sleep(2)
        # 2、在我的页面，点击收藏入口，检查刚收藏的消息内容，可以正常展示出来
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        collection = MeCollectionPage()
        text = '收藏记录'
        collection.page_should_contain_text(text)
        # 3、点击收藏成功的消息体，可以进入到消息展示详情页面
        collection.click_element_first_list()
        time.sleep(2)
        collection.page_should_contain_text('详情')
        collection.page_should_contain_text(text)
        # 4、左滑收藏消息体，会展示删除按钮
        collection.click_back()
        collection.swipe_left_message_first_list()
        self.assertTrue(collection.is_exist_element_delete_icon())
        # 5、点击删除按钮，可以删除收藏的消息体
        time.sleep(2)
        collection.click_element_delete_icon()
        collection.page_should_contain_text('文本消息')
        time.sleep(3)


    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0146(self):
        """企业群，发送文本消息——已读状态——未读分类展示"""
        chat = ChatWindowPage()
        # 确保聊天页面有消息记录
        chat.make_sure_chatwindow_have_message()
        time.sleep(2)
        # 1、在输入框录入内容，然后点击发送按钮，进行发送，发送成功后的消息体下方会展示：已读动态，4个字的文案
        self.assertTrue(chat.is_exist_element(locator='已读动态'))
        # 2、点击下方的已读动态，会跳转页面已读动态详情页面
        chat.click_already_read_dynamic()
        time.sleep(2)
        already_read = AlreadyReadDynamic()
        self.assertTrue(already_read.is_on_this_page())
        # 2、在已读动态详情页面，未读分类会展示，未读此条消息的用户信息并且点击其头像可以跳转到个人profile页面
        already_read.click_not_read()
        time.sleep(2)
        already_read.click_not_read_contact_first()
        time.sleep(2)
        self.assertTrue(ContactDetailsPage().is_on_this_page())


    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0148(self):
        """企业群，发送语音消息——已读状态——未读分类展示"""
        chat = ChatWindowPage()
        # 确保聊天页面有语音消息记录
        chat.send_voice()
        time.sleep(2)
        # 1、在输入框录入内容，然后点击发送按钮，进行发送，发送成功后的消息体下方会展示：已读动态，4个字的文案
        self.assertTrue(chat.is_exist_element(locator='已读动态'))
        # 2、点击下方的已读动态，会跳转页面已读动态详情页面
        chat.click_already_read_dynamic()
        time.sleep(2)
        already_read = AlreadyReadDynamic()
        self.assertTrue(already_read.is_on_this_page())
        # 2、在已读动态详情页面，未读分类会展示，未读此条消息的用户信息并且点击其头像可以跳转到个人profile页面
        already_read.click_not_read()
        already_read.click_not_read_contact_first()
        time.sleep(2)
        self.assertTrue(ContactDetailsPage().is_on_this_page())


    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0150(self):
        """企业群，发送表情消息——已读状态——未读分类展示"""
        chat = ChatWindowPage()
        # 确保聊天页面有表情消息记录
        chat.make_sure_chatwindow_have_message(content='微笑[1]')
        time.sleep(2)
        # 1、在输入框录入内容，然后点击发送按钮，进行发送，发送成功后的消息体下方会展示：已读动态，4个字的文案
        self.assertTrue(chat.is_exist_element(locator='已读动态'))
        # 2、点击下方的已读动态，会跳转页面已读动态详情页面
        chat.click_already_read_dynamic()
        time.sleep(2)
        already_read = AlreadyReadDynamic()
        self.assertTrue(already_read.is_on_this_page())
        # 2、在已读动态详情页面，未读分类会展示，未读此条消息的用户信息并且点击其头像可以跳转到个人profile页面
        already_read.click_not_read()
        already_read.click_not_read_contact_first()
        time.sleep(2)
        self.assertTrue(ContactDetailsPage().is_on_this_page())


    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0162(self):
        """普通群聊天会话页面——自己@自己"""
        chat = ChatWindowPage()
        # 聊天设置页面获取自己的名称
        chat.click_setting()
        set = GroupChatSetPage()
        time.sleep(2)
        name = set.get_first_number_name()
        set.click_back()
        # 1、在输入框输入@符号，跳转到的联系人选择页面，用户本身不会展示出来
        chat.click_input_box()
        chat.input_message_text('@')
        time.sleep(3)
        chat.page_should_contain_text('选择群成员')
        chat.page_should_not_contain_text(name)
        chat.click_back()
        # 2、在聊天会话页面长按自己，不可以发起@操作
        chat.make_sure_chatwindow_have_message()
        # 无法获取聊天人员头像 用坐标点击代替
        chat.swipe_by_percent_on_screen(90, 16, 94, 17)
        time.sleep(2)
        self.assertFalse(chat.is_exist_element(locator='发送按钮'))
























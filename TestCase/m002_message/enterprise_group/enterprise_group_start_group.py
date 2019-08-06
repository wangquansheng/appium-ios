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
from pages.chat.ChatInviteUse import ChatInvitationUse

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


class EnterpriseStartGroup(TestCase):
    """企业群--创建群"""

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    def setUp_test_msg_huangmianhua_0176(self):
        """确保每个用例执行前在单聊会话页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入单聊会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        if msg.is_text_present('大佬1'):
            msg.click_text('大佬1')
        else:
            msg.click_search_box()
            msg.input_search_text('大佬1')
            time.sleep(2)
            msg.click_search_local_contact()
            time.sleep(2)
            ContactDetailsPage().click_message_icon()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0176(self):
        """一对一聊天——点对点建群——网络正常"""
        chat = ChatWindowPage()
        chat.click_setting()
        # 1、在单聊设置页面，点击+号，可以跳转到联系人选择器页面
        set = SingleChatSetPage()
        set.wait_for_page_load()
        set.click_add_icon()
        time.sleep(2)
        select = SelectContactsPage()
        self.assertTrue(select.is_text_present('选择团队联系人'))
        # 2、选择本地联系人后，页面顶部搜索框的左边会展示已选择的联系人信息
        select.select_one_contact_by_name('大佬2')
        self.assertTrue(select.is_element_present(locator='已选择的联系人'))
        # 3、点击一下，已选择的联系人，会取消已选择的联系人的选中状态
        time.sleep(2)
        select.click_contact_which_is_selecd()
        self.assertFalse(select.is_element_present(locator='已选择的联系人'))
        # 4、点击右上角的确定按钮，会跳转到群名称设置页面
        select.select_one_contact_by_name('大佬2')
        select.click_sure_bottom()
        bulid_group = BuildGroupChatPage()
        time.sleep(2)
        self.assertTrue(bulid_group.is_on_this_page())
        # 5、群名称设置页面中的群名称，默认展示为：群聊--(ios 不是默认为群聊)
        # 6、设置完群名称，再次点击右上角的确定按钮，建群成功
        bulid_group.click_clear_button()
        name = '测试群1'
        bulid_group.input_group_chat_name(name)
        bulid_group.click_ok()
        time.sleep(2)
        self.assertTrue(chat.is_on_this_page())

    def tearDown_test_msg_huangmianhua_0176(self):
        # 删除新创建的群
        chat = GroupChatPage()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        ContactsPage().open_group_chat_list()
        group = ALLMyGroup()
        text = '测试群1'
        if group.is_text_present(text):
            group.select_group_by_name(text)
            time.sleep(2)
            chat.click_setting()
            GroupChatSetPage().dissolution_the_group()
        time.sleep(4)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    # def setUp_test_msg_huangmianhua_0178(self):
    #     """确保每个用例执行前在普通群群聊页面（且存在未进群联系人） """
    #     warnings.simplefilter('ignore', ResourceWarning)
    #     # 确保我的电脑页面有已下载的可预览文件
    #     Preconditions.select_mobile('IOS-移动')
    #     # 进入单聊会话页面
    #     Preconditions.make_already_in_message_page()
    #     time.sleep(2)
    #     msg=MessagePage()
    #     text = '群聊1'
    #     msg.click_search_box()
    #     msg.input_search_text(text)
    #     time.sleep(2)
    #     msg.click_element_first_list()
    #     time.sleep(2)
    #     # 添加未进群联系人
    #     chat = ChatWindowPage()
    #     chat.click_setting()
    #     SingleChatSetPage().click_add_icon()
    #     SelectContactsPage().select_one_contact_by_name('大佬3')
    #     SelectContactsPage().click_sure_bottom()
    #     time.sleep(3)
    #     #消息列表删除消息记录
    #     Preconditions.make_already_in_message_page()
    #     MessagePage().delete_all_message_list()
    #
    # @tags('ALL', 'enterprise_group', 'CMCC')
    # def test_msg_huangmianhua_0178(self):
    #     """普通群——聊天会话页面——未进群联系人展示"""
    #     msg = MessagePage()
    #     text = '群聊1'
    #     msg.click_search_box()
    #     msg.input_search_text(text)
    #     time.sleep(2)
    #     msg.click_element_first_list()
    #     time.sleep(2)
    #     chat = ChatWindowPage()
    #     # 1、存在未进群的联系人时，在聊天会话页面，发送一条消息，会提示：还有人未进群，再次邀请
    #     chat.send_mutiple_message(times=1)
    #     time.sleep(2)
    #     self.assertTrue(chat.is_exist_element(locator='未进群提示'))
    #     # 2、连续发送消息时，未进群提示，只会提示3次
    #     chat.send_mutiple_message(times=4)
    #     time.sleep(2)
    #
    #
    # def setUp_test_msg_huangmianhua_0179(self):
    #     """确保每个用例执行前在普通群群聊页面（且存在未进群联系人） """
    #     warnings.simplefilter('ignore', ResourceWarning)
    #     # 确保我的电脑页面有已下载的可预览文件
    #     Preconditions.select_mobile('IOS-移动')
    #     # 进入单聊会话页面
    #     Preconditions.make_already_in_message_page()
    #     time.sleep(2)
    #     msg=MessagePage()
    #     msg.delete_all_message_list()
    #     text = '群聊1'
    #     msg.click_search_box()
    #     msg.input_search_text(text)
    #     time.sleep(2)
    #     msg.click_search_local_contact()
    #     time.sleep(2)
    #
    # @tags('ALL', 'enterprise_group', 'CMCC')
    # def test_msg_huangmianhua_0179(self):
    #     """群聊设置——群成员列表——未进群提示展示"""
    #     chat = ChatWindowPage()
    #     # 1、存在未进群的联系人时，在聊天会话页面，发送一条消息，会提示：还有人未进群，再次邀请
    #     chat.send_mutiple_message(times=1)
    #     time.sleep(2)
    #     self.assertTrue(chat.is_exist_element(locator='未进群提示'))
    #     # 1、在群成员展示列表页面，点击：还有人未进群，再次邀请提示，会跳转到未进群联系人详情页
    #     chat.click_someone_notin_group_and_invite_again()
    #     time.sleep(2)
    #     chat.page_should_contain_text('再次邀请')
    #     # 2、在未进群联系人详情页面，点击再次邀请按钮，弹出toast提示：群邀请已发送并且返回到群聊天会话页
    #     chat.click_invite_again()
    #     time.sleep(3)
    #     self.assertTrue(chat)


    def setUp_test_msg_huangmianhua_0180(self):
        """确保每个用例执行前在通讯录-群聊列表页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入单聊会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        msg.click_contacts()
        ContactsPage().open_group_chat_list()
        time.sleep(3)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0180(self):
        """通讯录——发起群聊——选择本地联系人"""
        # 1、通讯录-群聊-右上角的发起群聊-联系人选择器页-选择本地联系人，点击右上角的确定按钮，创建普通群聊成功
        my_group = ALLMyGroup()
        my_group.click_creat_group()
        # 判断在选择联系人页面
        select = SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        #选择本地联系人
        select.select_local_contacts()
        local_contact = SelectLocalContactsPage()
        local_contact.swipe_select_one_member_by_name('大佬1')
        local_contact.swipe_select_one_member_by_name('大佬2')
        local_contact.click_sure()
        time.sleep(2)
        # 输入群聊名称
        name = '测试群1'
        my_group.click_clear_group_name()
        time.sleep(2)
        my_group.input_group_name(name)
        my_group.click_sure_creat()
        time.sleep(2)
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        # 验证点：可以创建普通群聊成功
        self.assertTrue(chat.is_on_this_page())
        time.sleep(2)

    def tearDown_test_msg_huangmianhua_0180(self):
        # 删除新创建的群
        chat = GroupChatPage()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        ContactsPage().open_group_chat_list()
        group = ALLMyGroup()
        text = '测试群1'
        if group.is_text_present(text):
            group.select_group_by_name(text)
            time.sleep(2)
            chat.click_setting()
            GroupChatSetPage().dissolution_the_group()
        time.sleep(4)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    def setUp_test_msg_huangmianhua_0181(self):
        """确保每个用例执行前在通讯录-群聊列表页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入单聊会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        msg.click_contacts()
        ContactsPage().open_group_chat_list()
        time.sleep(3)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0181(self):
        """通讯录——发起群聊——选择和通讯录联系人"""
        # 1、通讯录-群聊-右上角的发起群聊-联系人选择器页-选择和通讯录联系人，点击右上角的确定按钮，创建普通群聊成功
        my_group = ALLMyGroup()
        my_group.click_creat_group()
        # 判断在选择联系人页面
        select = SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        # 选择和通讯录联系人
        select.click_group_contact()
        group_contact = SelectHeContactsPage()
        time.sleep(2)
        group_contact.select_one_team_by_name('ateam7272')
        group_detail = SelectHeContactsDetailPage()
        time.sleep(2)
        group_detail.select_one_he_contact_by_name('大佬1')
        group_detail.select_one_he_contact_by_name('大佬2')
        group_detail.click_sure_icon()
        time.sleep(2)
        # 输入群聊名称
        name = '测试群2'
        my_group.click_clear_group_name()
        my_group.input_group_name(name)
        my_group.click_sure_creat()
        time.sleep(2)
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        # 验证点：可以创建普通群聊成功
        self.assertTrue(chat.is_on_this_page())
        time.sleep(2)

    def tearDown_test_msg_huangmianhua_0181(self):
        # 删除新创建的群
        chat = GroupChatPage()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        ContactsPage().open_group_chat_list()
        group = ALLMyGroup()
        text = '测试群1'
        if group.is_text_present(text):
            group.select_group_by_name(text)
            time.sleep(2)
            chat.click_setting()
            GroupChatSetPage().dissolution_the_group()
        time.sleep(4)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    def setUp_test_msg_huangmianhua_0182(self):
        """确保每个用例执行前在通讯录-群聊列表页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入单聊会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        msg.click_contacts()
        ContactsPage().open_group_chat_list()
        time.sleep(3)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0182(self):
        """通讯录——发起群聊——选择本地联系人+和通讯录联系人"""
        # 1、通讯录-群聊-右上角的发起群聊-联系人选择器页-选择和通讯录联系人，点击右上角的确定按钮，创建普通群聊成功
        my_group = ALLMyGroup()
        my_group.click_creat_group()
        # 判断在选择联系人页面
        select = SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        # 选择本地联系人
        select.select_local_contacts()
        local_contact = SelectLocalContactsPage()
        local_contact.swipe_select_one_member_by_name('大佬1')
        local_contact.click_sure()
        time.sleep(2)
        # 进入聊天界面-选择和通讯录联系人加入群聊
        chat = ChatWindowPage()
        chat.click_setting()
        SingleChatSetPage().click_add_icon()
        # 选择和通讯录联系人
        select.click_group_contact()
        group_contact = SelectHeContactsPage()
        group_contact.select_one_team_by_name('ateam7272')
        group_detail = SelectHeContactsDetailPage()
        group_detail.wait_for_he_contacts_page_load()
        group_detail.select_one_he_contact_by_name('大佬2')
        group_detail.click_sure_icon()
        time.sleep(2)
        # 输入群聊名称
        name = '测试群3'
        my_group.click_clear_group_name()
        my_group.input_group_name(name)
        my_group.click_sure_creat()
        time.sleep(2)
        chat.wait_for_page_load()
        # 验证点：可以创建普通群聊成功
        self.assertTrue(chat.is_on_this_page())
        time.sleep(2)

    def tearDown_test_msg_huangmianhua_0183(self):
        # 删除新创建的群
        chat = GroupChatPage()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        ContactsPage().open_group_chat_list()
        group = ALLMyGroup()
        text = '测试群3'
        if group.is_text_present(text):
            group.select_group_by_name(text)
            time.sleep(2)
            chat.click_setting()
            GroupChatSetPage().dissolution_the_group()
        time.sleep(4)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    def setUp_test_msg_huangmianhua_0184(self):
        """确保每个用例执行前在通讯录-群聊列表页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入单聊会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        msg.click_contacts()
        ContactsPage().open_group_chat_list()
        time.sleep(3)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0184(self):
        """通讯录——发起群聊——搜索陌生人"""
        # 1、通讯录-群聊-右上角的发起群聊-联系人选择器页-搜索选择联系人，点击右上角的确定按钮，创建普通群聊成功
        my_group = ALLMyGroup()
        my_group.click_creat_group()
        # 判断在选择联系人页面
        select = SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        # 搜索联系人大佬1  大佬2
        select.click_search_contact()
        select.input_search_keyword('17324448506')
        select.click_search_result_from_internet('17324448506')
        time.sleep(2)
        select.click_search_contact()
        select.input_search_keyword('15570670329')
        select.click_search_result_from_internet('15570670329')
        select.click_sure_bottom()
        # 输入群聊名称
        name = '测试群1'
        my_group.click_clear_group_name()
        my_group.input_group_name(name)
        my_group.click_sure_creat()
        time.sleep(2)
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        # 验证点：可以创建普通群聊成功
        self.assertTrue(chat.is_on_this_page())
        time.sleep(2)

    def tearDown_test_msg_huangmianhua_0184(self):
        # 删除新创建的群
        chat = GroupChatPage()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        ContactsPage().open_group_chat_list()
        group = ALLMyGroup()
        text = '测试群1'
        if group.is_text_present(text):
            group.select_group_by_name(text)
            time.sleep(2)
            chat.click_setting()
            GroupChatSetPage().dissolution_the_group()
        time.sleep(4)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    def setUp_test_msg_huangmianhua_0185(self):
        """确保每个用例执行前在通讯录-群聊列表页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入单聊会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        msg.click_contacts()
        ContactsPage().open_group_chat_list()
        time.sleep(3)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0185(self):
        """通讯录——发起群聊——搜索陌生人和本地联系人"""
        # 1、通讯录-群聊-右上角的发起群聊-联系人选择器页-搜索选择陌生人+本地联系人，点击右上角的确定按钮，可以创建普通群聊成功
        my_group = ALLMyGroup()
        my_group.click_creat_group()
        # 判断在选择联系人页面
        select = SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        # 搜索联系人大佬1
        select.click_search_contact()
        select.input_search_keyword('17324448506')
        select.click_search_result_from_internet('17324448506')
        # 选择本地联系人
        select.select_local_contacts()
        local_contact = SelectLocalContactsPage()
        local_contact.swipe_select_one_member_by_name('大佬1')
        local_contact.click_sure()
        time.sleep(2)
        # 输入群聊名称
        name = '测试群1'
        my_group.click_clear_group_name()
        my_group.input_group_name(name)
        my_group.click_sure_creat()
        time.sleep(2)
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        # 验证点：可以创建普通群聊成功
        self.assertTrue(chat.is_on_this_page())
        time.sleep(2)

    def tearDown_test_msg_huangmianhua_0185(self):
        # 删除新创建的群
        chat = GroupChatPage()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        ContactsPage().open_group_chat_list()
        group = ALLMyGroup()
        text = '测试群1'
        if group.is_text_present(text):
            group.select_group_by_name(text)
            time.sleep(2)
            chat.click_setting()
            GroupChatSetPage().dissolution_the_group()
        time.sleep(4)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    def setUp_test_msg_huangmianhua_0186(self):
        """确保每个用例执行前在通讯录-群聊列表页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入单聊会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        msg.click_contacts()
        ContactsPage().open_group_chat_list()
        time.sleep(3)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0186(self):
        """通讯录——发起群聊——搜索陌生人和 和通讯录联系人"""
        # 1、通讯录-群聊-右上角的发起群聊-联系人选择器页-搜索选择陌生人+和通讯录联系人，点击右上角的确定按钮，可以创建普通群聊成功
        my_group = ALLMyGroup()
        my_group.click_creat_group()
        # 判断在选择联系人页面
        select = SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        # 搜索联系人大佬1
        select.click_search_contact()
        select.input_search_keyword('17324448506')
        select.click_search_result_from_internet('17324448506')
        # 选择本地联系人
        select.click_group_contact()
        group_contact = SelectHeContactsPage()
        group_contact.select_one_team_by_name('ateam7272')
        group_detail = SelectHeContactsDetailPage()
        # group_detail.wait_for_he_contacts_page_load()
        time.sleep(3)
        group_detail.select_one_he_contact_by_name('大佬2')
        group_detail.click_sure_icon()
        time.sleep(2)
        # 输入群聊名称
        name = '测试群1'
        my_group.click_clear_group_name()
        my_group.input_group_name(name)
        my_group.click_sure_creat()
        time.sleep(2)
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        # 验证点：可以创建普通群聊成功
        self.assertTrue(chat.is_on_this_page())
        time.sleep(2)

    def tearDown_test_msg_huangmianhua_0186(self):
        # 删除新创建的群
        chat = GroupChatPage()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        ContactsPage().open_group_chat_list()
        group = ALLMyGroup()
        text = '测试群1'
        if group.is_text_present(text):
            group.select_group_by_name(text)
            time.sleep(2)
            chat.click_setting()
            GroupChatSetPage().dissolution_the_group()
        time.sleep(4)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    def setUp_test_msg_huangmianhua_0224(self):
        """确保每个用例执行前在通讯录-单聊页面，且单聊页面有消息记录 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入单聊会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        msg.delete_all_message_list()
        msg.click_contacts()
        ContactsPage().click_phone_contact()
        ContactsPage().select_contacts_by_name('大佬1')
        ContactDetailsPage().click_message_icon()
        time.sleep(3)
        chat = ChatWindowPage()
        chat.make_sure_chatwindow_have_message()
        time.sleep(2)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0224(self):
        """转发——支持转发的——默认选中项（1条）"""
        chat = ChatWindowPage()
        # 长按-弹出操作列表
        chat.press_and_move_right_text_message()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='复制'))
        self.assertTrue(chat.is_element_present_by_locator(locator='转发'))
        self.assertTrue(chat.is_element_present_by_locator(locator='删除'))
        self.assertTrue(chat.is_element_present_by_locator(locator='收藏'))
        self.assertTrue(chat.is_element_present_by_locator(locator='撤回'))
        self.assertTrue(chat.is_element_present_by_locator(locator='显示更多项目'))
        # 点击多选 2.进入聊天会话窗口的批量选择器页面
        chat.click_show_more_items()
        self.assertTrue(chat.is_element_present_by_locator(locator='多选'))
        time.sleep(2)
        chat.click_multiple_selection()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-删除'))
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-转发'))
        # 3.默认选中长按的那一条消息体
        self.assertTrue(chat.is_element_present_by_locator(locator='多选按钮'))
        # 点击转发-4.进入最近聊天选择器页面
        chat.click_multiple_selection_forward()
        select = SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        # 5.任意选择一个对象-弹出确认弹框
        select.click_recent_chat_contact()
        time.sleep(2)
        self.assertTrue(select.is_element_present(locator='取消'))
        self.assertTrue(select.is_element_present(locator='确定'))
        # 6.点击取消/弹框以外区域 -弹框消失,停留在选择联系人界面
        select.click_cancel_forward()
        self.assertFalse(select.is_element_present(locator='取消'))
        self.assertTrue(select.is_on_this_page())
        # 点击确定 7.弹框消失，自动返回原会话窗口，toast提示“已转发”(toast 暂时无法验证)
        select.click_recent_chat_contact()
        select.click_sure_forward()
        time.sleep(3)
        self.assertTrue(chat.is_on_this_page())
        # 8.显示消息体是按照时间顺序排序(难以验证)
        self.assertTrue(chat.is_element_present_message_list())

    def setUp_test_msg_huangmianhua_0226(self):
        """确保每个用例执行前在通讯录-单聊页面，且单聊页面有消息记录 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入单聊会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        msg.delete_all_message_list()
        msg.click_contacts()
        ContactsPage().click_phone_contact()
        ContactsPage().select_contacts_by_name('大佬1')
        ContactDetailsPage().click_message_icon()
        time.sleep(3)
        chat = ChatWindowPage()
        chat.make_sure_chatwindow_have_message()
        time.sleep(2)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0226(self):
        """转发默认选中项（1条）—删除"""
        chat = ChatWindowPage()
        # 长按-弹出操作列表
        number1 = chat.get_message_list_number()
        chat.press_and_move_right_text_message()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='复制'))
        self.assertTrue(chat.is_element_present_by_locator(locator='转发'))
        self.assertTrue(chat.is_element_present_by_locator(locator='删除'))
        self.assertTrue(chat.is_element_present_by_locator(locator='收藏'))
        self.assertTrue(chat.is_element_present_by_locator(locator='显示更多项目'))
        # 点击多选 2.进入聊天会话窗口的批量选择器页面
        chat.click_show_more_items()
        self.assertTrue(chat.is_element_present_by_locator(locator='多选'))
        time.sleep(2)
        chat.click_multiple_selection()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-删除'))
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-转发'))
        # 3.默认选中长按的那一条消息体
        self.assertTrue(chat.is_element_present_by_locator(locator='多选按钮'))
        # 点击删除-4.进入最近聊天选择器页面
        chat.click_multiple_delete()
        # 弹出提示框
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='取消'))
        self.assertTrue(chat.is_element_present_by_locator(locator='删除'))
        # 点击确定删除 5.删除成功，聊天会话中toast提示“删除成功”（toast 无法验证）
        chat.click_delete()
        time.sleep(2)
        # 6.删除掉的消息体已删除成功
        number2 = chat.get_message_list_number()
        self.assertNotEqual(number1, number2)


    def setUp_test_msg_huangmianhua_0227(self):
        """确保每个用例执行前在通讯录-单聊页面，且单聊页面有消息记录 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入单聊会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        msg.delete_all_message_list()
        msg.click_contacts()
        ContactsPage().click_phone_contact()
        ContactsPage().select_contacts_by_name('大佬1')
        ContactDetailsPage().click_message_icon()
        time.sleep(3)
        chat = ChatWindowPage()
        chat.make_sure_chatwindow_have_message()
        time.sleep(2)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0227(self):
        """转发默认选中项（1条）—取消删除"""
        chat = ChatWindowPage()
        # 长按-弹出操作列表
        chat.press_and_move_right_text_message()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='复制'))
        self.assertTrue(chat.is_element_present_by_locator(locator='转发'))
        self.assertTrue(chat.is_element_present_by_locator(locator='删除'))
        self.assertTrue(chat.is_element_present_by_locator(locator='收藏'))
        self.assertTrue(chat.is_element_present_by_locator(locator='显示更多项目'))
        # 点击多选 2.进入聊天会话窗口的批量选择器页面
        chat.click_show_more_items()
        self.assertTrue(chat.is_element_present_by_locator(locator='多选'))
        time.sleep(2)
        chat.click_multiple_selection()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-删除'))
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-转发'))
        # 3.默认选中长按的那一条消息体
        self.assertTrue(chat.is_element_present_by_locator(locator='多选按钮'))
        # 点击删除-4.进入最近聊天选择器页面
        chat.click_multiple_delete()
        # 弹出提示框
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='取消'))
        self.assertTrue(chat.is_element_present_by_locator(locator='删除'))
        # 点击取消删除 5.弹框关闭，停留在批量选择器页面）
        chat.click_cancle()
        time.sleep(2)
        self.assertFalse(chat.is_element_present_by_locator(locator='取消'))
        # 6.选中的消息体还是选中的状态
        self.assertTrue(chat.is_element_present_by_locator(locator='多选按钮'))

    def setUp_test_msg_huangmianhua_0228(self):
        """确保每个用例执行前在通讯录-单聊页面，且单聊页面有消息记录 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入单聊会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        msg.delete_all_message_list()
        msg.click_contacts()
        ContactsPage().click_phone_contact()
        ContactsPage().select_contacts_by_name('大佬1')
        ContactDetailsPage().click_message_icon()
        time.sleep(3)
        chat = ChatWindowPage()
        chat.make_sure_chatwindow_have_message()
        time.sleep(2)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0228(self):
        """取消默认选中项"""
        chat = ChatWindowPage()
        # 长按-弹出操作列表
        chat.press_and_move_right_text_message()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='复制'))
        self.assertTrue(chat.is_element_present_by_locator(locator='转发'))
        self.assertTrue(chat.is_element_present_by_locator(locator='删除'))
        self.assertTrue(chat.is_element_present_by_locator(locator='收藏'))
        self.assertTrue(chat.is_element_present_by_locator(locator='显示更多项目'))
        # 点击多选 2.进入聊天会话窗口的批量选择器页面
        chat.click_show_more_items()
        self.assertTrue(chat.is_element_present_by_locator(locator='多选'))
        time.sleep(2)
        chat.click_multiple_selection()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-删除'))
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-转发'))
        # 3.默认选中长按的那一条消息体
        self.assertTrue(chat.is_element_present_by_locator(locator='多选按钮'))
        # 4.默认选项被取消选中，标题变为“未选择”，
        chat.click_multiple_selected_button()
        time.sleep(2)
        chat.page_should_contain_text('未选择')
        # 点击删除/转发无效，两个操作按钮呈灰色（点击删除按钮无反应  点击转发按钮 页面未跳转）
        chat.click_multiple_delete()
        time.sleep(2)
        self.assertFalse(chat.is_element_present_by_locator(locator='取消'))
        chat.click_multiple_selection_forward()
        time.sleep(2)
        self.assertTrue(chat.is_on_this_page())


    def setUp_test_msg_huangmianhua_0229(self):
        """确保每个用例执行前在通讯录-单聊页面，且单聊页面有多条消息记录 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入单聊会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        msg.delete_all_message_list()
        msg.click_contacts()
        ContactsPage().click_phone_contact()
        ContactsPage().select_contacts_by_name('大佬1')
        ContactDetailsPage().click_message_icon()
        time.sleep(3)
        chat = ChatWindowPage()
        chat.send_mutiple_message(times=5)
        time.sleep(2)
        chat.page_down()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0229(self):
        """选择多条消息体"""
        chat = ChatWindowPage()
        time.sleep(2)
        # 长按-弹出操作列表
        chat.press_and_move_right_text_message()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='复制'))
        self.assertTrue(chat.is_element_present_by_locator(locator='转发'))
        self.assertTrue(chat.is_element_present_by_locator(locator='删除'))
        self.assertTrue(chat.is_element_present_by_locator(locator='收藏'))
        self.assertTrue(chat.is_element_present_by_locator(locator='显示更多项目'))
        # 点击多选 2.进入聊天会话窗口的批量选择器页面
        chat.click_show_more_items()
        self.assertTrue(chat.is_element_present_by_locator(locator='多选'))
        time.sleep(2)
        chat.click_multiple_selection()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-删除'))
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-转发'))
        # 3.默认选中长按的那一条消息体
        self.assertTrue(chat.is_element_present_by_locator(locator='多选按钮'))
        # 4.点击其他消息体的复选框/消息气泡/头像  被点到的相对应消息体被选中
        chat.click_selected_other_text(number=3)
        chat.page_should_contain_text('2')


    def setUp_test_msg_huangmianhua_0230(self):
        """确保每个用例执行前在通讯录-单聊页面，且单聊页面有多条消息记录 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入单聊会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        msg.delete_all_message_list()
        msg.click_contacts()
        ContactsPage().click_phone_contact()
        ContactsPage().select_contacts_by_name('大佬1')
        ContactDetailsPage().click_message_icon()
        time.sleep(3)
        chat = ChatWindowPage()
        chat.send_voice(times=1)
        chat.send_mutiple_message(times=5)
        chat.page_down()
        time.sleep(2)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0230(self):
        """当转发的消息体中包含不支持转发的类型：①未下载的图片/视频/文件  ②语音、红包、卡券等特殊消息体——网络正常"""
        chat = ChatWindowPage()
        # 长按-弹出操作列表(无法获取发送的语音 id  使用坐标比例代替)
        chat.swipe_by_percent_on_screen(70, 18, 77, 18)
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='删除'))
        self.assertTrue(chat.is_element_present_by_locator(locator='收藏'))
        self.assertTrue(chat.is_element_present_by_locator(locator='多选'))
        time.sleep(2)
        chat.click_multiple_selection()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-删除'))
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-转发'))
        # 3.默认选中长按的那一条消息体
        self.assertTrue(chat.is_element_present_by_locator(locator='多选按钮'))
        # 4.点击其他消息体的复选框/消息气泡/头像  被点到的相对应消息体被选中
        chat.click_selected_other_text(number=3)
        chat.page_should_contain_text('2')
        # 点击转发
        chat.click_multiple_selection_forward()
        time.sleep(1)
        self.assertTrue(chat.is_exist_element(locator='取消'))
        self.assertTrue(chat.is_exist_element(locator='确定按钮'))
        # 点击取消 5.停留在批量选择器页面
        chat.click_cancle()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='多选按钮'))
        # 点击确定 6.进入最近聊天选择器页面
        chat.click_multiple_selection_forward()
        time.sleep(1)
        chat.click_sure()
        select = SelectContactsPage()
        time.sleep(2)
        self.assertTrue(select.is_on_this_page())
        select.page_should_contain_text('最近聊天')
        # 5.任意选择一个对象-弹出确认弹框
        select.click_recent_chat_contact()
        time.sleep(2)
        self.assertTrue(select.is_element_present(locator='取消'))
        self.assertTrue(select.is_element_present(locator='确定'))
        # 6.点击取消/弹框以外区域 -弹框消失,停留在选择联系人界面
        select.click_cancel_forward()
        self.assertFalse(select.is_element_present(locator='取消'))
        self.assertTrue(select.is_on_this_page())
        # 点击确定 7.弹框消失，自动返回原会话窗口，toast提示“已转发”(toast 暂时无法验证)
        select.click_recent_chat_contact()
        select.click_sure_forward()
        time.sleep(2)
        self.assertTrue(chat.is_on_this_page())
        # 8.显示消息体是按照时间顺序排序
        self.assertTrue(chat.is_element_present_message_list())

    def setUp_test_msg_huangmianhua_0232(self):
        """确保每个用例执行前在通讯录-单聊页面，且单聊页面有多条消息记录 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入单聊会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        msg.delete_all_message_list()
        msg.click_contacts()
        ContactsPage().click_phone_contact()
        ContactsPage().select_contacts_by_name('大佬1')
        ContactDetailsPage().click_message_icon()
        time.sleep(3)
        chat = ChatWindowPage()
        chat.send_voice(times=3)
        chat.page_down()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0232(self):
        """当转发的消息体中包含不支持转发的类型：①未下载的图片/视频/文件  ②语音、红包、卡券等特殊消息体——网络正常"""
        chat = ChatWindowPage()
        # 长按-弹出操作列表(发送的语音 获取id时白屏  无法获取)
        # chat.press_and_move_right_voice()
        chat.swipe_by_percent_on_screen(70, 18, 77, 18)
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='删除'))
        self.assertTrue(chat.is_element_present_by_locator(locator='收藏'))
        self.assertTrue(chat.is_element_present_by_locator(locator='多选'))
        time.sleep(2)
        chat.click_multiple_selection()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-删除'))
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-转发'))
        # 3.默认选中长按的那一条消息体
        self.assertTrue(chat.is_element_present_by_locator(locator='多选按钮'))
        # 4.点击其他消息体的复选框/消息气泡/头像  被点到的相对应消息体被选中
        chat.click_selected_other_text(number=2)
        chat.page_should_contain_text('2')
        # 点击转发
        chat.click_multiple_selection_forward()
        time.sleep(2)
        self.assertTrue(chat.is_exist_element(locator='取消'))
        self.assertTrue(chat.is_exist_element(locator='确定按钮'))
        # 点击取消 5.停留在批量选择器页面
        chat.click_cancle()
        self.assertTrue(chat.is_element_present_by_locator(locator='多选按钮'))
        # 点击确定 6.弹框关闭，停留在原有的批量选择器页面
        chat.click_multiple_selection_forward()
        time.sleep(1)
        chat.click_sure()
        time.sleep(4)
        self.assertTrue(chat.is_element_present_by_locator(locator='多选按钮'))

    def setUp_test_msg_huangmianhua_0233(self):
        """确保每个用例执行前在通讯录-单聊页面，且单聊页面有多条消息记录 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入单聊会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        msg.delete_all_message_list()
        msg.click_contacts()
        ContactsPage().click_phone_contact()
        ContactsPage().select_contacts_by_name('大佬1')
        ContactDetailsPage().click_message_icon()
        time.sleep(3)
        chat = ChatWindowPage()
        chat.send_mutiple_message(times=5)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0233(self):
        """当转发的消息体是支持转发的类型--网络正常转发"""
        chat = ChatWindowPage()
        # 长按-弹出操作列表
        chat.press_and_move_right_text_message()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='转发'))
        self.assertTrue(chat.is_element_present_by_locator(locator='删除'))
        self.assertTrue(chat.is_element_present_by_locator(locator='收藏'))
        self.assertTrue(chat.is_element_present_by_locator(locator='显示更多项目'))
        # 点击多选 2.进入聊天会话窗口的批量选择器页面
        chat.click_show_more_items()
        self.assertTrue(chat.is_element_present_by_locator(locator='多选'))
        time.sleep(2)
        chat.click_multiple_selection()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-删除'))
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-转发'))
        # 3.默认选中长按的那一条消息体
        self.assertTrue(chat.is_element_present_by_locator(locator='多选按钮'))
        # 4.点击其他消息体的复选框/消息气泡/头像  被点到的相对应消息体被选中
        chat.click_selected_other_text(number=3)
        chat.page_should_contain_text('2')
        # 点击转发
        chat.click_multiple_selection_forward()
        select = SelectContactsPage()
        time.sleep(2)
        self.assertTrue(select.is_on_this_page())
        select.page_should_contain_text('最近聊天')
        # 5.任意选择一个对象-弹出确认弹框
        select.click_recent_chat_contact()
        time.sleep(2)
        self.assertTrue(select.is_element_present(locator='取消'))
        self.assertTrue(select.is_element_present(locator='确定'))
        # 6.点击取消/弹框以外区域 -弹框消失,停留在选择联系人界面
        select.click_cancel_forward()
        self.assertFalse(select.is_element_present(locator='取消'))
        self.assertTrue(select.is_on_this_page())
        # 点击确定 7.弹框消失，自动返回原会话窗口，toast提示“已转发”(toast 暂时无法验证)
        select.click_recent_chat_contact()
        select.click_sure_forward()
        time.sleep(2)
        self.assertTrue(chat.is_on_this_page())
        # 8.显示消息体是按照时间顺序排序
        self.assertTrue(chat.is_element_present_message_list())

    def setUp_test_msg_huangmianhua_0235(self):
        """确保每个用例执行前在通讯录-单聊页面，且单聊页面有多条消息记录 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入单聊会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        msg.delete_all_message_list()
        msg.click_contacts()
        ContactsPage().click_phone_contact()
        ContactsPage().select_contacts_by_name('大佬1')
        ContactDetailsPage().click_message_icon()
        time.sleep(3)
        chat = ChatWindowPage()
        chat.send_mutiple_message(times=5)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0235(self):
        """当转发的消息体中包含不支持转发的类型：①未下载的图片/视频/文件  ②语音、红包、卡券等特殊消息体——网络正常"""
        chat = ChatWindowPage()
        # 长按-弹出操作列表
        chat.press_and_move_right_text_message()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='转发'))
        self.assertTrue(chat.is_element_present_by_locator(locator='删除'))
        self.assertTrue(chat.is_element_present_by_locator(locator='收藏'))
        self.assertTrue(chat.is_element_present_by_locator(locator='显示更多项目'))
        # 点击多选 2.进入聊天会话窗口的批量选择器页面
        chat.click_show_more_items()
        self.assertTrue(chat.is_element_present_by_locator(locator='多选'))
        time.sleep(2)
        chat.click_multiple_selection()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-删除'))
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-转发'))
        # 3.默认选中长按的那一条消息体
        self.assertTrue(chat.is_element_present_by_locator(locator='多选按钮'))
        # 4.点击其他消息体的复选框/消息气泡/头像  被点到的相对应消息体被选中
        chat.click_selected_other_text(number=3)
        chat.page_should_contain_text('2')
        # 点击删除
        chat.click_multiple_delete()
        # 弹出提示框
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='取消'))
        self.assertTrue(chat.is_element_present_by_locator(locator='删除'))
        # 点击确认删除
        chat.click_multiple_delete()
        time.sleep(2)
        chat.click_delete()

    def setUp_test_msg_huangmianhua_0236(self):
        """确保每个用例执行前在通讯录-单聊页面，且单聊页面有多条消息记录 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入单聊会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        msg.delete_all_message_list()
        msg.click_contacts()
        ContactsPage().click_phone_contact()
        ContactsPage().select_contacts_by_name('大佬1')
        ContactDetailsPage().click_message_icon()
        time.sleep(3)
        chat = ChatWindowPage()
        chat.send_mutiple_message(times=5)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0236(self):
        """当转发的消息体中包含不支持转发的类型：①未下载的图片/视频/文件  ②语音、红包、卡券等特殊消息体——网络正常"""
        chat = ChatWindowPage()
        # 长按-弹出操作列表
        chat.press_and_move_right_text_message()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='转发'))
        self.assertTrue(chat.is_element_present_by_locator(locator='删除'))
        self.assertTrue(chat.is_element_present_by_locator(locator='收藏'))
        self.assertTrue(chat.is_element_present_by_locator(locator='显示更多项目'))
        # 点击多选 2.进入聊天会话窗口的批量选择器页面
        chat.click_show_more_items()
        self.assertTrue(chat.is_element_present_by_locator(locator='多选'))
        time.sleep(2)
        chat.click_multiple_selection()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-删除'))
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-转发'))
        # 3.默认选中长按的那一条消息体
        self.assertTrue(chat.is_element_present_by_locator(locator='多选按钮'))
        # 4.点击其他消息体的复选框/消息气泡/头像  被点到的相对应消息体被选中
        chat.click_selected_other_text(number=3)
        chat.page_should_contain_text('2')
        # 点击删除
        chat.click_multiple_delete()
        # 弹出提示框
        time.sleep(2)
        self.assertTrue(chat.is_element_present_by_locator(locator='取消'))
        self.assertTrue(chat.is_element_present_by_locator(locator='删除'))
        # 点击取消删除 5.弹框关闭，停留在批量选择器页面）
        chat.click_cancle()
        time.sleep(2)
        self.assertFalse(chat.is_element_present_by_locator(locator='取消'))
        self.assertTrue(chat.is_element_present_by_locator(locator='多选按钮'))

    def setUp_test_msg_huangmianhua_0265(self):
        """确保每个用例执行前在企业群会话页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入企业群会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        Preconditions.enter_enterprise_group_by_name()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0265(self):
        """已读动态——“已读动态”标识"""
        chat = ChatWindowPage()
        chat.make_sure_chatwindow_have_message()
        time.sleep(2)
        # 发出的任意消息下都有“已读动态”标识
        self.assertTrue(chat.is_exist_element(locator='已读动态'))

    def setUp_test_msg_huangmianhua_0274(self):
        """确保每个用例执行前在企业群会话页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入企业群会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        Preconditions.enter_enterprise_group_by_name(name='测试企业群2')

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0274(self):
        """已读动态——非RCS用户提醒——提示消息出现规则"""
        chat = ChatWindowPage()
        chat.make_sure_chatwindow_have_message()
        time.sleep(2)
        # 正常提示：其后每超过24后发出的消息则出提醒
        self.assertTrue(chat.is_exist_element(locator='非和飞信用户提醒'))
        time.sleep(3)

    def tearDown_test_msg_huangmianhua_0274(self):
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

    def setUp_test_msg_huangmianhua_0277(self):
        """确保每个用例执行前在企业群会话页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入企业群会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        Preconditions.enter_enterprise_group_by_name(name='测试企业群2')

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0277(self):
        """已读动态——非RCS用户提醒——提示消息文案规则"""
        chat = ChatWindowPage()
        chat.make_sure_chatwindow_have_message()
        time.sleep(2)
        # 发出的任意消息下都有“已读动态”标识
        self.assertTrue(chat.is_exist_element(locator='非和飞信用户提醒'))
        # 号码屏蔽规则：大陆号隐藏后8位，香港号屏蔽后5位（无法获取提示消息文案 故无法验证）

    def setUp_test_msg_huangmianhua_0278(self):
        """确保每个用例执行前在企业群会话页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入企业群会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        Preconditions.enter_enterprise_group_by_name(name='测试企业群2')

    @tags('ALL', 'enterprise_group', 'CMCC_debugging')
    def test_msg_huangmianhua_0278(self):
        """已读动态——非RCS用户提醒——点击“邀请他们”进入邀请页  (邀请使用按钮需使用坐标点击)"""
        chat = ChatWindowPage()
        chat.make_sure_chatwindow_have_message()
        time.sleep(2)
        # 发出的任意消息下都有“已读动态”标识
        self.assertTrue(chat.is_exist_element(locator='非和飞信用户提醒'))
        # 点击“邀请他们”进入邀请页
        chat.click_not_heifeixin_remind()
        invite_use = ChatInvitationUse()
        self.assertTrue(invite_use.is_on_this_page())
        # 1.左上方“ < ”可返回消息界面
        invite_use.click_back()
        time.sleep(2)
        chat.is_on_this_page()
        # 2.上方页面标题“未使用成员”
        chat.click_not_heifeixin_remind()
        time.sleep(3)
        self.assertTrue(invite_use.is_exist_element(locator='未使用成员'))
        self.assertTrue(invite_use.is_exist_element(locator='成员头像'))
        self.assertTrue(invite_use.is_exist_element(locator='一键邀请'))
        self.assertTrue(invite_use.is_text_present(locator='大佬1'))
        # 点击一键邀请
        invite_use.click_one_key_use()
        time.sleep(3)
        self.assertTrue(chat.is_on_this_page())

    def tearDown_test_msg_huangmianhua_0278(self):
        """解散群"""
        chat = GroupChatPage()
        if chat.is_on_this_page():
            time.sleep(2)
        else:
            Preconditions.make_already_in_message_page()
            time.sleep(2)
            Preconditions.enter_enterprise_group_by_name(name='测试企业群2')
        chat.click_setting()
        GroupChatSetPage().dissolution_the_group()

    def setUp_test_msg_huangmianhua_0279(self):
        """确保每个用例执行前在企业群会话页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入企业群会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        Preconditions.enter_enterprise_group_by_name()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0279(self):
        """企业群底部全部按钮"""
        chat = GroupChatPage()
        time.sleep(4)
        self.assertTrue(chat.is_element_present_by_locator(locator='选择图片'))
        self.assertTrue(chat.is_element_present_by_locator(locator='选择相机'))
        self.assertTrue(chat.is_element_present_by_locator(locator='文件'))
        self.assertTrue(chat.is_element_present_by_locator(locator='表情'))
        self.assertTrue(chat.is_element_present_by_locator(locator='选择更多'))
        self.assertTrue(chat.is_element_present_by_locator(locator='说点什么'))
        self.assertTrue(chat.is_element_present_by_locator(locator='语音'))


    def setUp_test_msg_huangmianhua_0280(self):
        """确保每个用例执行前在企业群会话页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入企业群会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        Preconditions.enter_enterprise_group_by_name()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0280(self):
        """企业群底部全部按钮——更多“+”"""
        chat = GroupChatPage()
        chat.click_more()
        time.sleep(4)
        self.assertTrue(chat.is_element_present_by_locator(locator='飞信电话'))
        self.assertTrue(chat.is_element_present_by_locator(locator='音视频通话'))
        self.assertTrue(chat.is_element_present_by_locator(locator='名片'))
        self.assertTrue(chat.is_element_present_by_locator(locator='位置'))
        self.assertTrue(chat.is_element_present_by_locator(locator='红包'))
        self.assertTrue(chat.is_element_present_by_locator(locator='群短信'))
        self.assertTrue(chat.is_element_present_by_locator(locator='审批'))
        self.assertTrue(chat.is_element_present_by_locator(locator='日志'))


    def setUp_test_msg_huangmianhua_0281(self):
        """确保每个用例执行前在企业群会话页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入企业群会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        Preconditions.enter_enterprise_group_by_name()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0281(self):
        """添加1个群成员，选择和通讯录联系人（用户为群主且用户在多个企业或只有一个企业但用户在企业子层级）”"""
        chat = GroupChatPage()
        chat.click_setting()
        # 1、点击添加群成员按钮-选择和通讯录联系人，跳转到页面，是否展示为所在的企业和部门
        set = GroupChatSetPage()
        number1 = set.get_group_members_number()
        set.click_add_member()
        select_he = SelectHeContactsDetailPage()
        # 验证点：1.可以跳转到联系人选择器页面
        self.assertTrue(select_he.is_on_this_page())
        # 2、点击部门，展示企业成员列表
        text = 'bm1'
        select_he.select_one_department(text)
        # 3、选中一个联系人，点击右上角的确定按钮
        member_name = select_he.get_department_first_number_name()
        select_he.click_first_he_contact()
        select_he.click_sure_icon()
        # 3、成功邀请成员
        time.sleep(2)
        chat.wait_for_page_load()
        self.assertTrue(chat.is_on_this_page())
        chat.click_setting()
        time.sleep(3)
        number2 = set.get_group_members_number()
        self.assertNotEqual(number1, number2)
        time.sleep(2)
        # 移除新添加的成员
        set.delete_member_by_name(member=member_name)

    def setUp_test_msg_huangmianhua_0289(self):
        """确保每个用例执行前在企业群会话页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入企业群会话页面
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        time.sleep(2)
        Preconditions.enter_enterprise_group_by_name()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0289(self):
        """转发聊天窗口中的可以转发的消息体，选择和通讯录联系人（用户为群主且用户在多个企业或只有一个企业但用户在企业子层级）”"""
        chat = ChatWindowPage()
        chat.make_sure_chatwindow_have_message()
        time.sleep(2)
        # 1、长按聊天窗口中可进行转发的消息体，点击转发按钮，选择和通讯录联系人，直接跳转到该企业的企业层级
        chat.press_and_move_right_text_message()
        time.sleep(2)
        chat.click_forward()
        select = SelectContactsPage()
        select.click_group_contact()
        # 2、点击该企业名称，可以进入到该企业的子层级页面
        group = SelectHeContactsPage()
        group.select_one_team_by_name('ateam7272')
        select_he = SelectHeContactsDetailPage()
        # 验证点：1.可以跳转到联系人选择器页面
        self.assertTrue(select_he.is_on_this_page())
        # 3、选中联系人，确认转发后，返回到消息列表被转发的会话窗口正常展现
        contact = '大佬2'
        select_he.select_one_he_contact_by_number(number=contact)
        select_he.click_sure_icon()
        time.sleep(2)
        # 返回到消息列表被转发的会话窗口正常展现
        Preconditions.make_already_in_message_page()
        self.assertTrue(MessagePage().is_text_present(contact))


    def setUp_test_msg_huangmianhua_0293(self):
        """确保每个用例执行前在企业群会话页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入企业群会话页面
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        time.sleep(2)
        Preconditions.enter_enterprise_group_by_name()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0293(self):
        """企业群/党群--查找聊天内容--转发聊天窗口中的可以转发的消息体，选择和通讯录联系人”"""
        chat = ChatWindowPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按查找聊天内容页面中可进行转发的消息体，点击转发按钮，选择和通讯录联系人，是否直接跳转到该企业的企业层级
        chat.click_setting()
        set = GroupChatSetPage()
        set.click_find_chat_record()
        time.sleep(2)
        self.assertTrue(set.is_exit_element(locator='输入关键字快速搜索'))
        #  点击顶部的搜索框，输入搜索文本
        set.click_input_box()
        set.input_search_keyword('消息')
        set.click_search_result_first_list()
        # 长按
        chat.swipe_by_percent_on_screen(67, 21, 80, 21)
        time.sleep(2)
        chat.click_forward()
        select = SelectContactsPage()
        select.click_group_contact()
        # 2、点击该企业名称，可以进入到该企业的子层级页面
        group = SelectHeContactsPage()
        group.select_one_team_by_name('ateam7272')
        select_he = SelectHeContactsDetailPage()
        # 验证点：1.可以跳转到联系人选择器页面
        self.assertTrue(select_he.is_on_this_page())
        # 3、选中联系人，确认转发后，返回到消息列表被转发的会话窗口正常展现
        contact = '大佬2'
        select_he.select_one_he_contact_by_name(name=contact)
        select_he.click_sure_icon()
        time.sleep(2)
        # 返回到消息列表被转发的会话窗口正常展现
        Preconditions.make_already_in_message_page()
        time.sleep(3)
        self.assertTrue(MessagePage().is_text_present(contact))


    def setUp_test_msg_huangmianhua_0297(self):
        """确保每个用例执行前在企业群会话页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入企业群会话页面
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        time.sleep(2)
        Preconditions.enter_enterprise_group_by_name()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0297(self):
        """分享网页消息--选择和通讯录联系人”"""
        chat = ChatWindowPage()
        web_message = 'www.baidu.com'
        chat.make_sure_chatwindow_have_message(content=web_message)
        # 1、通用浏览器内--点击右上方的三个点图标--点击“转发给朋友”--选择和通讯录联系人，是否直接跳转到该企业的企业层级
        chat.click_coordinate(70, 21)
        chat.wait_for_page_load_web_message()
        chat.click_more_web_message()
        time.sleep(2)
        chat.click_forward_to_friend()
        time.sleep(2)
        select = SelectContactsPage()
        select.click_group_contact()
        # 2、点击该企业名称，可以进入到该企业的子层级页面
        group = SelectHeContactsPage()
        group.select_one_team_by_name('ateam7272')
        select_he = SelectHeContactsDetailPage()
        # 验证点：1.可以跳转到联系人选择器页面
        self.assertTrue(select_he.is_on_this_page())
        # 3、选中联系人，确认转发后，返回到消息列表被转发的会话窗口正常展现
        contact = '大佬2'
        select_he.select_one_he_contact_by_name(name=contact)
        select_he.click_sure_icon()
        time.sleep(2)
        # 返回到消息列表被转发的会话窗口正常展现
        Preconditions.make_already_in_message_page()
        self.assertTrue(MessagePage().is_text_present(contact))


    def setUp_test_msg_huangmianhua_0303(self):
        """确保每个用例执行前在企业群会话页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入企业群会话页面
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        time.sleep(2)
        Preconditions.enter_enterprise_group_by_name()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0303(self):
        """群聊设置--群成员预览内非RCS用户头像置灰”"""
        chat = ChatWindowPage()
        chat.click_setting()
        # 确保当前企业群有非rcs用户
        set = GroupChatSetPage()
        text = '大佬1'
        if set.is_text_present(text):
            time.sleep(2)
        else:
            set.add_member_by_name(member=text)
        # 1、非RCS用户头像应置灰(暂时无法验证)
        # 2、能正常进入其profile页
        set.click_text(text)
        time.sleep(2)
        self.assertTrue(ContactDetailsPage().is_on_this_page())

    def setUp_test_msg_huangmianhua_0304(self):
        """确保每个用例执行前在企业群会话页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入企业群会话页面
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        time.sleep(2)
        Preconditions.enter_enterprise_group_by_name()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0304(self):
        """群聊设置--群成员列表内非RCS用户头像置灰”"""
        chat = ChatWindowPage()
        chat.click_setting()
        # 确保当前企业群有非rcs用户
        set = GroupChatSetPage()
        text = '大佬1'
        if set.is_text_present(text):
            time.sleep(2)
        else:
            set.add_member_by_name(member=text)
        # 1、群聊设置--群成员列表内非RCS用户头像置灰
        set.click_enter_contact_list()
        self.assertTrue(set.is_text_present(text))
        # 2、能正常进入其profile页
        set.click_text(text)
        time.sleep(2)
        self.assertTrue(ContactDetailsPage().is_on_this_page())

    def setUp_test_msg_huangmianhua_0305(self):
        """确保每个用例执行前在企业群会话页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入企业群会话页面
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        time.sleep(2)
        Preconditions.enter_enterprise_group_by_name()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0305(self):
        """群聊设置--群成员列表--搜索结果非RCS用户头像置灰”"""
        chat = ChatWindowPage()
        chat.click_setting()
        # 确保当前企业群有非rcs用户
        set = GroupChatSetPage()
        text = '大佬1'
        if not set.is_text_present(text):
            set.add_member_by_name(member=text)
        time.sleep(2)
        # 1、搜索结果内非RCS用户头像应置灰不再显示“未开通”且后方还有“邀请”按钮
        set.click_enter_contact_list()
        set.click_search_group_contact()
        set.input_contact_name(text)
        time.sleep(3)
        self.assertTrue(set.is_exit_element(locator='未开通'))
        self.assertTrue(set.is_exit_element(locator='邀请'))
        # 2、能正常进入其profile页
        set.click_search_group_contact_result()
        time.sleep(2)
        self.assertTrue(ContactDetailsPage().is_on_this_page())


class EnterpriseGroupSet(TestCase):
    """企业群-设置页面"""

    def default_setUp(self):
        """确保每个用例执行前在单聊会话页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入单聊会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0365(self):
        """消息--右上角“+”--发起群聊--选择一个群——选择一个企业群/党群-页面显示正常"""
        # 1、右上角“+”--发起群聊--选择一个群
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择一个企业群
        name = '测试企业群1'
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.selecting_one_group_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 2、检查群头像、企业/党群标识、群名称、等元素
        gcp.click_setting()
        set = GroupChatSetPage()
        set.wait_for_page_load()
        time.sleep(3)
        self.assertTrue(set.is_exit_element(locator='皇冠标志'))
        self.assertTrue(set.is_exit_element(locator='群成员头像'))
        self.assertTrue(set.is_exit_element(locator='群成员名字'))


    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0367(self):
        """消息--右上角“+”--发起群聊--选择一个群——选择一个企业群/党群-群主在群聊设置页有拉人“+”和踢人“-”按钮"""
        # 1、右上角“+”--发起群聊--选择一个群
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择一个企业群
        name = '测试企业群1'
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.selecting_one_group_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 2、检查群头像、企业/党群标识、群名称、等元素
        gcp.click_setting()
        set = GroupChatSetPage()
        set.wait_for_page_load()
        time.sleep(3)
        self.assertTrue(set.is_exit_element(locator='添加成员'))
        self.assertTrue(set.is_exit_element(locator='删除成员'))


    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0395(self):
        """企业群/党群在消息列表内展示——最新消息展示——草稿"""
        # 自己在输入框内填写信息未发出时展示红色“[草稿]“+消息内容
        Preconditions.enter_enterprise_group_by_name()
        chat = GroupChatPage()
        chat.click_input_box()
        text = '文本消息'
        chat.input_message_text(text)
        chat.click_back()
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        self.assertTrue(mess.is_text_present('草稿'))
        self.assertTrue(mess.is_text_present(text))

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_huangmianhua_0398(self):
        """免打扰时右下角免打扰标识"""
        # 自己在输入框内填写信息未发出时展示红色“[草稿]“+消息内容
        Preconditions.enter_enterprise_group_by_name()
        chat = GroupChatPage()
        chat.click_setting()
        set = GroupChatSetPage()
        if set.get_switch_undisturb_value() == '0':
            set.click_switch_undisturb()
        set.click_back()
        time.sleep(2)
        self.assertTrue(chat.is_element_exit_('消息免打扰'))

    def tearDown_test_msg_huangmianhua_0398(self):
        # 取消消息免打扰状态
        chat = GroupChatPage()
        if chat.is_on_this_page():
            time.sleep(2)
        else:
            Preconditions.enter_enterprise_group_by_name()
        chat.click_setting()
        if GroupChatSetPage().get_switch_undisturb_value() == '1':
            GroupChatSetPage().click_switch_undisturb()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
































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
from pages.chat.ChatInviteUse import ChatInvitationUse
from pages.groupset.GroupChatApproval import GroupChatApproval
from pages.groupset.GroupApprovalDetail import GroupChatApprovalDetail


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

    @staticmethod
    def make_sure_chatwindow_have_approval_message():
        """确保企业群当前页面有审批消息"""
        chat = GroupChatPage()
        if chat.is_text_present('审批'):
            time.sleep(3)
        else:
            # 进入审批页面
            chat = GroupChatPage()
            chat.click_more()
            chat.click_group_approval()
            time.sleep(2)
            approval = GroupChatApproval()
            approval.wait_for_page_load()
            time.sleep(3)
            # 发起通用审批流程--分享到当前群
            approval.click_general_approval()
            time.sleep(3)
            detail = GroupChatApprovalDetail()
            # 输入审批内容
            detail.click_input_application_detail()
            detail.input_application_detail('请假审批')
            # 选择审批人
            detail.add_approver(name='大佬1')
            # 开启分享至当前群按钮
            detail.click_share_to_group()
            # 返回到群聊页面
            detail.click_submit()
            time.sleep(3)
            chat.wait_for_page_load()

    @staticmethod
    def make_sure_singlehatwindow_have_approval_message(name='大佬1'):
        """确保当前单聊页面有审批消息"""
        group_chat = GroupChatPage()
        select = SelectContactsPage()
        # 确保单聊页面有审批卡片消息(企业群页面转发到单聊)
        Preconditions.make_sure_chatwindow_have_approval_message()
        group_chat.press_and_move_right_approval()
        group_chat.click_forward()
        select.select_local_contacts()
        local_contact = SelectLocalContactsPage()
        local_contact.swipe_select_one_member_by_name(name)
        local_contact.click_sure()
        time.sleep(2)
        # 进入单聊页面
        Preconditions.make_already_in_message_page()
        MessagePage().click_text(name)
        time.sleep(3)


class GroupApproval(TestCase):
    """企业群--审批"""

    def default_setUp(self):
        """确保每个用例开始之前进入企业群审批页面"""
        warnings.simplefilter('ignore',ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_enterprise_group_by_name()
        chat = GroupChatPage()
        chat.click_more()
        chat.click_group_approval()
        time.sleep(2)
        approval = GroupChatApproval()
        approval.wait_for_page_load()

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0070(self):
        """普通企业群/长ID企业群：进入审批应用后右上角“？”内部页面样式、文案及交互是否正常（本网号为例）"""
        approval = GroupChatApproval()
        time.sleep(3)
        # 点击进入1、从企业群进入审批应用后点击右上方“？”按钮
        approval.click_question_mark()
        time.sleep(2)
        # 1、正常进入审批应用问题解答页面且内部样式文案等与工作台内审批应用一致
        self.assertTrue(approval.is_exist_element(locator='返回'))
        self.assertTrue(approval.is_exist_element(locator='关闭'))
        self.assertTrue(approval.is_text_present('审批'))
        # 2、全部二级页面样式、文案及相关操作正常，关闭页面后应直接返回到群聊页面
        # 点击返回按钮，返回到审批页面
        approval.click_back()
        self.assertTrue(approval.is_on_this_page())
        # 点击关闭按钮，返回到审批页面
        approval.click_question_mark()
        time.sleep(3)
        approval.click_close_h5()
        self.assertTrue(approval.is_on_this_page())

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0074(self):
        """普通企业群/长ID企业群：发起任意审批类型时页面样式检查"""
        approval = GroupChatApproval()
        time.sleep(3)
        # 1、在企业群进入“审批”应用后点击发起任意审批类型，进入后检查页面样式是否正常
        approval.click_ask_for_level()
        time.sleep(4)
        approval.page_should_contain_text('我的请假')
        # “使用上次审批人、使用上次抄送人”按钮是否被隐藏，页面下方是否多了一个“分享至当前群”栏目且后方按钮默认关闭(按钮的状态无法获取)
        self.assertFalse(approval.is_text_present('使用上次审批人'))
        self.assertFalse(approval.is_text_present('使用上次抄送人'))
        self.assertTrue(approval.is_text_present('分享至当前群'))

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0076(self):
        """普普通企业群/长ID企业群：审批--“分享至当前群”功能验证"""
        approval = GroupChatApproval()
        time.sleep(3)
        # 1、在企业群进入“审批”应用后点击发起任意审批类型--填写完全部信息及选择了“审批人、抄送人”后开启“分享至当前群”按钮
        approval.click_general_approval()
        time.sleep(3)
        detail = GroupChatApprovalDetail()
        # 输入审批内容
        detail.click_input_application_detail()
        detail.input_application_detail('请假审批')
        # 选择审批人
        detail.add_approver(name='大佬1')
        # 开启分享至当前群按钮
        detail.click_share_to_group()
        # 2、toast提示“提交成功”、自动跳转到群聊界面且发送该审批卡片消息到群内
        detail.click_submit()
        time.sleep(3)
        chat = GroupChatPage()
        chat.wait_for_page_load()
        self.assertTrue(chat.is_on_this_page())
        self.assertTrue(chat.is_text_present('测试企业群1'))

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0079(self):
        """普通企业群/长ID企业群：审批发起人点击审批卡片消息查看详情"""
        Preconditions.make_sure_chatwindow_have_approval_message()
        # 2、详情页内容应与“工作台--我发起的--查看该审批详情”内容一致且可做相应操作：
        chat = GroupChatPage()
        chat.click_message_approval()
        time.sleep(6)
        # 如果还在审批过程中则有“催一下”和“撤销”按钮，如果已经审批完成则没有以上按钮（涉及到双机操作，）
        self.assertTrue(chat.is_element_present_by_locator(locator='撤销'))
        self.assertTrue(chat.is_element_present_by_locator(locator='催一下'))


    def setUp_test_msg_hanjiabin_0083(self):
        """确保每个用例开始之前进入企业群页面"""
        warnings.simplefilter('ignore',ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_enterprise_group_by_name()
        time.sleep(3)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0083(self):
        """普通企业群/长ID企业群：审批发起人“长按”审批卡片消息--转发"""
        Preconditions.make_sure_chatwindow_have_approval_message()
        # 1、审批发起人长按该审批卡片消息--点击“转发”--转发到一个单聊
        chat = GroupChatPage()
        select = SelectContactsPage()
        chat.press_and_move_right_approval()
        chat.click_forward()
        select.select_local_contacts()
        local_contact = SelectLocalContactsPage()
        self.assertEqual(local_contact.is_on_this_page(), True)
        local_contact.swipe_select_one_member_by_name('大佬2')
        local_contact.click_sure()
        time.sleep(2)
        # 验证点1、对方成功收到卡片消息
        Preconditions.make_already_in_message_page()
        MessagePage().click_msg_first_list()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_message())
        # 2、审批发起人长按该审批卡片消息--点击“转发”--转发到一个普通群
        chat.press_and_move_right_approval()
        chat.click_forward()
        select.click_select_one_group()
        SelectOneGroupPage().selecting_one_group_by_name('群聊1')
        SelectOneGroupPage().click_sure_send()
        time.sleep(2)
        # 验证点2、对方成功收到卡片消息
        Preconditions.make_already_in_message_page()
        MessagePage().click_msg_first_list()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_message())
        # 3、审批发起人长按该审批卡片消息--点击“转发”--转发到一个其他企业群
        chat.press_and_move_right_approval()
        chat.click_forward()
        select.click_select_one_group()
        SelectOneGroupPage().select_one_company_group()
        SelectOneGroupPage().click_sure_send()
        time.sleep(2)
        # 验证点3、对方成功收到卡片消息
        Preconditions.make_already_in_message_page()
        MessagePage().click_msg_first_list()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_message())
        # 4、审批发起人长按该审批卡片消息--点击“转发”--转发到“我的电脑”
        chat.press_and_move_right_approval()
        chat.click_forward()
        select.click_search_contact()
        select.input_search_keyword('我的电脑')
        select.click_search_result()
        select.click_sure_forward()
        time.sleep(2)
        # 验证点4、对方成功收到卡片消息
        Preconditions.make_already_in_message_page()
        MessagePage().click_msg_first_list()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_message())

    def setUp_test_msg_hanjiabin_0084(self):
        """确保每个用例开始之前进入企业群页面"""
        warnings.simplefilter('ignore',ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_enterprise_group_by_name()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0084(self):
        """普通企业群/长ID企业群：审批发起人“长按”审批卡片消息--收藏"""
        Preconditions.make_sure_chatwindow_have_approval_message()
        # 1、审批发起人长按该审批卡片消息--点击“收藏”
        chat = GroupChatPage()
        chat.press_and_move_right_approval()
        chat.click_collection()
        time.sleep(2)
        # 2、进入“我”模块--收藏内查看是否收藏成功且展示是否正常 成功收藏
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        collection = MeCollectionPage()
        collection.page_should_contain_text('通用审批')
        # 点击查看收藏详情  3、详情页内容应与“工作台--我发起的--查看该审批详情”内容一致且可做相应操作：如果还在审批过程中则有“催一下”和“撤销”按钮
        time.sleep(2)
        collection.click_element_first_list()
        time.sleep(5)
        self.assertTrue(collection.is_text_present('撤销'))
        self.assertTrue(collection.is_text_present('催一下'))
        # 如果已经审批完成则没有以上按钮（暂未验证）
        # 详情页内容应与“工作台--我发起的--查看该审批详情”内容一致且可做相应操作：
        Preconditions.make_already_in_message_page()
        MessagePage().open_workbench_page()
        work = WorkbenchPage()
        work.click_approve()
        time.sleep(3)
        approval = GroupChatApproval()
        approval.wait_for_page_load()
        self.assertTrue(approval.is_on_this_page())
        approval.click_i_initiated_approval()
        time.sleep(3)
        approval.page_should_contain_text('通用审批')


    def setUp_test_msg_hanjiabin_0085(self):
        """确保每个用例开始之前进入企业群页面"""
        warnings.simplefilter('ignore',ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_enterprise_group_by_name()
        time.sleep(3)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0085(self):
        """普通企业群/长ID企业群：审批发起人“长按”审批卡片消息--撤回"""
        Preconditions.make_sure_chatwindow_have_approval_message()
        # 1、审批发起人长按该审批卡片消息--点击“撤回”
        chat = GroupChatPage()
        chat.press_and_move_right_approval()
        chat.click_revoke()
        time.sleep(2)
        # 1、APP端发出方和接收方查看皆已正常撤回、PC端同步被撤回
        self.assertTrue(chat.is_element_present_by_locator(locator='你撤回了一条消息'))

    def setUp_test_msg_hanjiabin_0086(self):
        """确保每个用例开始之前进入企业群页面"""
        warnings.simplefilter('ignore',ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_enterprise_group_by_name()
        time.sleep(3)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0086(self):
        """普通企业群/长ID企业群：审批发起人“长按”审批卡片消息--删除"""
        Preconditions.make_sure_chatwindow_have_approval_message()
        # 1、审批发起人长按该审批卡片消息--点击“删除”
        chat = GroupChatPage()
        chat.press_and_move_right_approval()
        chat.click_delete()
        time.sleep(3)
        chat.click_sure_delete()
        # 1、自己的群聊界面内该条审批卡片消息被删除
        time.sleep(3)
        self.assertFalse(chat.is_element_present_message())

    def setUp_test_msg_hanjiabin_0100(self):
        """确保每个用例开始之前进入企业群页面"""
        warnings.simplefilter('ignore',ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_enterprise_group_by_name()
        time.sleep(3)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0100(self):
        """普通企业群/长ID企业群：审批发起人点击审批卡片消息查看详情"""
        Preconditions.make_sure_chatwindow_have_approval_message()
        chat = GroupChatPage()
        chat.click_message_approval()
        time.sleep(6)
        # 如果还在审批过程中则有“催一下”和“撤销”按钮，如果已经审批完成则没有以上按钮（涉及到双机操作，）
        self.assertTrue(chat.is_element_present_by_locator(locator='撤销'))
        self.assertTrue(chat.is_element_present_by_locator(locator='催一下'))
        # 详情页内容应与“工作台--我发起的--查看该审批详情”内容一致且可做相应操作：
        Preconditions.make_already_in_message_page()
        MessagePage().open_workbench_page()
        work = WorkbenchPage()
        work.click_approve()
        time.sleep(3)
        approval = GroupChatApproval()
        approval.wait_for_page_load()
        self.assertTrue(approval.is_on_this_page())
        approval.click_i_initiated_approval()
        time.sleep(3)
        approval.page_should_contain_text('通用审批')


    def setUp_test_msg_hanjiabin_0102(self):
        """确保每个用例开始之前进入企业群页面"""
        warnings.simplefilter('ignore',ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_enterprise_group_by_name()
        time.sleep(3)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0102(self):
        """普通企业群/长ID企业群：审批发起人“长按”审批卡片消息--转发"""
        Preconditions.make_sure_singlehatwindow_have_approval_message()
        # 1、审批发起人长按该审批卡片消息--点击“转发”--转发到一个单聊
        chat = SingleChatPage()
        chat.wait_for_page_load()
        select = SelectContactsPage()
        chat.press_and_move_right_approval()
        chat.click_forward()
        select.select_local_contacts()
        local_contact = SelectLocalContactsPage()
        self.assertEqual(local_contact.is_on_this_page(), True)
        local_contact.swipe_select_one_member_by_name('大佬2')
        local_contact.click_sure()
        time.sleep(2)
        # 验证点1、对方成功收到卡片消息
        Preconditions.make_already_in_message_page()
        MessagePage().click_msg_first_list()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_message())
        # 2、审批发起人长按该审批卡片消息--点击“转发”--转发到一个普通群
        chat.press_and_move_right_approval()
        chat.click_forward()
        select.click_select_one_group()
        SelectOneGroupPage().selecting_one_group_by_name('群聊1')
        SelectOneGroupPage().click_sure_send()
        time.sleep(2)
        # 验证点2、对方成功收到卡片消息
        Preconditions.make_already_in_message_page()
        MessagePage().click_msg_first_list()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_message())
        # 3、审批发起人长按该审批卡片消息--点击“转发”--转发到一个其他企业群
        chat.press_and_move_right_approval()
        chat.click_forward()
        select.click_select_one_group()
        SelectOneGroupPage().select_one_company_group()
        SelectOneGroupPage().click_sure_send()
        time.sleep(2)
        # 验证点3、对方成功收到卡片消息
        Preconditions.make_already_in_message_page()
        MessagePage().click_msg_first_list()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_message())
        # 4、审批发起人长按该审批卡片消息--点击“转发”--转发到“我的电脑”
        chat.press_and_move_right_approval()
        chat.click_forward()
        select.click_search_contact()
        select.input_search_keyword('我的电脑')
        select.click_search_result()
        select.click_sure_forward()
        time.sleep(2)
        # 验证点4、对方成功收到卡片消息
        Preconditions.make_already_in_message_page()
        MessagePage().click_msg_first_list()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_message())

    def setUp_test_msg_hanjiabin_0103(self):
        """确保每个用例开始之前进入企业群页面"""
        warnings.simplefilter('ignore',ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_enterprise_group_by_name()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0103(self):
        """普通企业群/长ID企业群：审批发起人“长按”审批卡片消息--收藏"""
        Preconditions.make_sure_singlehatwindow_have_approval_message()
        # 1、审批发起人长按该审批卡片消息--点击“收藏”
        chat = GroupChatPage()
        chat.press_and_move_right_approval()
        chat.click_collection()
        time.sleep(2)
        # 2、进入“我”模块--收藏内查看是否收藏成功且展示是否正常 成功收藏
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        collection = MeCollectionPage()
        collection.page_should_contain_text('通用审批')
        # 点击查看收藏详情  3、详情页内容应与“工作台--我发起的--查看该审批详情”内容一致且可做相应操作：如果还在审批过程中则有“催一下”和“撤销”按钮
        time.sleep(2)
        collection.click_element_first_list()
        time.sleep(5)
        self.assertTrue(collection.is_text_present('撤销'))
        self.assertTrue(collection.is_text_present('催一下'))
        # 如果已经审批完成则没有以上按钮（暂未验证）
        # 详情页内容应与“工作台--我发起的--查看该审批详情”内容一致且可做相应操作：
        Preconditions.make_already_in_message_page()
        MessagePage().open_workbench_page()
        work = WorkbenchPage()
        work.click_approve()
        time.sleep(3)
        approval = GroupChatApproval()
        approval.wait_for_page_load()
        self.assertTrue(approval.is_on_this_page())
        approval.click_i_initiated_approval()
        time.sleep(3)
        approval.page_should_contain_text('通用审批')


    def setUp_test_msg_hanjiabin_0104(self):
        """确保每个用例开始之前进入企业群页面"""
        warnings.simplefilter('ignore',ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_enterprise_group_by_name()
        time.sleep(3)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0104(self):
        """普通企业群/长ID企业群：审批发起人“长按”审批卡片消息--撤回"""
        Preconditions.make_sure_singlehatwindow_have_approval_message()
        # 1、审批发起人长按该审批卡片消息--点击“撤回”
        chat = GroupChatPage()
        chat.press_and_move_right_approval()
        chat.click_revoke()
        time.sleep(2)
        # 1、APP端发出方和接收方查看皆已正常撤回、PC端同步被撤回
        self.assertTrue(chat.is_element_present_by_locator(locator='你撤回了一条消息'))

    def setUp_test_msg_hanjiabin_0105(self):
        """确保每个用例开始之前进入企业群页面"""
        warnings.simplefilter('ignore',ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_enterprise_group_by_name()
        time.sleep(3)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0105(self):
        """普通企业群/长ID企业群：审批发起人“长按”审批卡片消息--删除"""
        Preconditions.make_sure_singlehatwindow_have_approval_message()
        # 1、审批发起人长按该审批卡片消息--点击“删除”
        chat = GroupChatPage()
        chat.press_and_move_right_approval()
        chat.click_delete()
        time.sleep(3)
        chat.click_sure_delete()
        # 1、自己的群聊界面内该条审批卡片消息被删除
        time.sleep(3)
        self.assertFalse(chat.is_element_present_message())

    def setUp_test_msg_hanjiabin_0106(self):
        """确保每个用例开始之前进入企业群页面"""
        warnings.simplefilter('ignore',ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_enterprise_group_by_name()
        time.sleep(3)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0106(self):
        """普通企业群/长ID企业群：审批发起人“长按”审批卡片消息--多选"""
        Preconditions.make_sure_singlehatwindow_have_approval_message()
        # 1、审批发起人长按该审批卡片消息--点击“删除”
        chat = GroupChatPage()
        chat.press_and_move_right_approval()
        time.sleep(2)
        chat.click_multiple_selection()
        time.sleep(2)
        chat.page_contain_element(locator='多选按钮')
        chat.page_contain_element(locator='多选-删除')
        chat.page_contain_element(locator='多选-转发')









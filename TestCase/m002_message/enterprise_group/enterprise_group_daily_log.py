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
from pages.groupset.GroupLog import GroupLogPage
from pages.workbench.daily_record.DailyRecord import DailyRecordPage
from pages.groupset.GroupLogDetail import GroupLogDetailPage
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
    def make_sure_chatwindow_have_daily_log_message(name='大佬1'):
        """确保企业群当前页面有审批消息"""
        chat = GroupChatPage()
        if chat.is_text_present('日报'):
            time.sleep(3)
        else:
            chat = GroupChatPage()
            chat.click_more()
            chat.click_daily_log()
            log = DailyRecordPage()
            log.wait_for_page_load()
            log = DailyRecordPage()
            # 进入日志编辑页
            time.sleep(2)
            log.click_journals()
            log.click_daily_paper()
            log.wait_log_editor_page_load()
            time.sleep(2)
            # 输入日志内容
            log.input_work_summary('测试文本')
            log.click_text('完成')
            log.click_add_icon()
            time.sleep(2)
            SelectHeContactsDetailPage().select_one_he_contact_by_name(name)
            SelectHeContactsDetailPage().click_sure_icon()
            log.click_share_to_group() #分享至当前群
            log.click_submit()
            time.sleep(3)


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
    """企业群-日志"""

    def default_setUp(self):
        """确保每个用例开始之前进入企业群日志页面"""
        warnings.simplefilter('ignore',ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_enterprise_group_by_name()
        chat = GroupChatPage()
        chat.click_more()
        chat.click_daily_log()
        log = DailyRecordPage()
        log.wait_for_page_load()

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0124(self):
        """普通企业群/长ID企业群：进入日志应用后页面样式检查（本网号为例）"""
        # 1、正常进入该企业下日志应用一级页面且页面样式及文案与工作台进入日志一致
        log = DailyRecordPage()
        time.sleep(2)
        self.assertTrue(log.is_on_daily_record_page())
        self.assertTrue(log.is_text_present('日志'))
        self.assertTrue(log.is_text_present('我发出的'))
        self.assertTrue(log.is_text_present('我收到的'))
        self.assertTrue(log.is_exist_element(locator='写日志'))
        # 从工作台进入
        Preconditions.make_already_in_message_page()
        MessagePage().open_workbench_page()
        work = WorkbenchPage()
        work.click_journal()
        log.wait_for_page_load()
        self.assertTrue(log.is_on_daily_record_page())

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0125(self):
        """普通企业群/长ID企业群：进入日志应用后能否正常返回群聊页面（本网号为例）"""
        # 1、从企业群进入日志应用后点击左上方的“<”返回按钮
        log = DailyRecordPage()
        time.sleep(2)
        log.click_back()
        # 1、正常返回进入前的群聊页面且群内“+”保持打开状态
        time.sleep(2)
        chat = GroupChatPage()
        chat.wait_for_page_load()
        time.sleep(3)
        self.assertTrue(chat.is_element_present_by_locator(locator='日志'))

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0129(self):
        """普通企业群/长ID企业群：写日志--日志编写界面样式检查（本网号为例）"""
        # 1、点击页面下方“写日志”按钮
        log = DailyRecordPage()
        time.sleep(2)
        log.click_journals()
        # 验证点 1、弹出“日报、周报、月报、取消”的选择框
        self.assertTrue(log.is_exist_element(locator='关闭'))
        self.assertTrue(log.is_exist_element(locator='日报'))
        self.assertTrue(log.is_exist_element(locator='周报'))
        self.assertTrue(log.is_exist_element(locator='月报'))
        # 2、任意选择“日报、周报、月报”中的一种
        log.click_daily_paper()
        log.wait_log_editor_page_load()
        time.sleep(2)
        # 验证点 2、正常进入日志编写界面
        self.assertTrue(log.is_on_edit_daily_page())
        # 页面样式检查 3、隐藏“添加上次联系人”按钮、“日志转聊天”按钮默认关闭、“分享至当前群”按钮默认关闭
        self.assertTrue(log.is_exist_element(locator='日志转聊天'))
        self.assertTrue(log.is_exist_element(locator='分享至当前群'))
        self.assertFalse(log.is_text_present('添加上次联系人'))
        # 4、点击左上角“<”返回按钮  返回上一级界面
        log.click_back()
        time.sleep(3)
        self.assertTrue(log.is_exist_element(locator='日报'))
        self.assertTrue(log.is_exist_element(locator='周报'))
        self.assertTrue(log.is_exist_element(locator='月报'))
        # 5、重新进入日志编辑页后点击左上角“X”关闭按钮 返回群聊页面
        log.click_daily_paper()
        log.wait_log_editor_page_load()
        time.sleep(3)
        log.click_close_h5()
        chat = GroupChatPage()
        chat.wait_for_page_load()
        self.assertTrue(chat.is_on_this_page())

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0130(self):
        """普通企业群/长ID企业群：写日志--选择接收人（本网号为例"""
        # 确保在日志编辑页面
        log = DailyRecordPage()
        time.sleep(2)
        log.click_journals()
        log.click_daily_paper()
        log.wait_log_editor_page_load()
        time.sleep(2)
        self.assertTrue(log.is_on_edit_daily_page())
        # 1、点击“接收人”下方“+”选择接收人
        log.click_add_icon()
        time.sleep(2)
        detail = SelectHeContactsDetailPage()
        self.assertTrue(detail.is_on_this_page())
        detail.select_one_he_contact_by_name('大佬1')
        detail.click_sure_icon()
        time.sleep(3)
        log.page_should_contain_text('大佬1')
        # 2、选择了接收人后再次点击下方“+”选择接收人
        log.click_add_icon()
        time.sleep(2)
        detail = SelectHeContactsDetailPage()
        self.assertTrue(detail.is_on_this_page())
        detail.select_one_he_contact_by_name('大佬2')
        detail.click_sure_icon()
        time.sleep(2)
        self.assertTrue(log.is_text_present('大佬2'))
        self.assertTrue(log.is_text_present('大佬1'))

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0134(self):
        """普通企业群/长ID企业群：日志转聊天后发送人“长按”日志卡片消息--转发（本网号为例）"""
        # 确保在群聊页面有日志信息
        Preconditions.make_sure_chatwindow_have_daily_log_message()
        chat = GroupChatPage()
        # 1、审批发起人长按该审批卡片消息--点击“转发”--转发到一个单聊
        chat = SingleChatPage()
        chat.wait_for_page_load()
        select = SelectContactsPage()
        chat.press_and_move_right_daily_log()
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
        chat.press_and_move_right_daily_log()
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
        chat.press_and_move_right_daily_log()
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
        chat.press_and_move_right_daily_log()
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

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0135(self):
        """普通企业群/长ID企业群：日志转聊天后发送人“长按”日志卡片消息--收藏（本网号为例）"""
        # 确保在群聊页面有日志信息
        Preconditions.make_sure_chatwindow_have_daily_log_message()
        chat = GroupChatPage()
        # 1、审批发起人长按该审批卡片消息--点击“收藏”
        chat.press_and_move_right_daily_log()
        chat.click_collection()
        time.sleep(2)
        # 2、进入“我”模块--收藏内查看是否收藏成功且展示是否正常
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        MePage().click_collection()
        collection = MeCollectionPage()
        collection.wait_for_page_load()
        time.sleep(3)
        collection.page_should_contain_text('日报')
        # 3、点击查看该收藏详情
        collection.click_element_first_list()
        time.sleep(4)
        self.assertTrue(collection.is_exist_element(locator='点赞'))
        self.assertTrue(collection.is_exist_element(locator='评论'))
        # 3、详情页内容应与“工作台--我发起的--查看该日志详情”内容一致且可做相应操作(可点赞 可收藏)
        Preconditions.make_already_in_message_page()
        MessagePage().open_workbench_page()
        work = WorkbenchPage()
        work.click_journal()
        log = DailyRecordPage()
        log.wait_for_page_load()
        self.assertTrue(log.is_on_daily_record_page())
        log.click_already_submit_log()
        time.sleep(4)
        self.assertTrue(log.is_exist_element(locator='点赞'))
        self.assertTrue(log.is_exist_element(locator='评论'))





    def setUp_test_msg_hanjiabin_0136(self):
        """确保每个用例开始之前进入企业群日志页面"""
        warnings.simplefilter('ignore',ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        Preconditions.enter_enterprise_group_by_name()

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0136(self):
        """普通企业群/长ID企业群：日志转聊天后发送人“长按”日志卡片消息--撤回"""
        # 确保在群聊页面有日志信息
        Preconditions.make_sure_chatwindow_have_daily_log_message()
        # 1、日志发起人长按该日志卡片消息--点击“撤回”
        chat = GroupChatPage()
        chat.press_and_move_right_daily_log()
        chat.click_revoke()
        time.sleep(2)
        # 1、APP端发出方和接收方查看皆已正常撤回、PC端同步被撤回
        self.assertTrue(chat.is_element_present_by_locator(locator='你撤回了一条消息'))

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0137(self):
        """普通企业群/长ID企业群：日志转聊天后发送人“长按”日志卡片消息--删除"""
        # 确保在群聊页面有日志信息
        Preconditions.make_sure_chatwindow_have_daily_log_message()
        # 1、日志发起人长按该日志卡片消息--点击“删除”
        chat = GroupChatPage()
        chat.press_and_move_right_daily_log()
        chat.click_delete()
        time.sleep(3)
        chat.click_sure_delete()
        # 1、自己的群聊界面内该条审批卡片消息被删除
        time.sleep(3)
        self.assertFalse(chat.is_element_present_message())

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0138(self):
        """普通企业群/长ID企业群：日志转聊天后发送人“长按”日志卡片消息--多选"""
        # 确保在群聊页面有日志信息
        Preconditions.make_sure_chatwindow_have_daily_log_message()
        # 1、日志发起人长按该日志卡片消息--点击“多选”
        chat = GroupChatPage()
        chat.press_and_move_right_daily_log()
        time.sleep(2)
        chat.click_multiple_selection()
        time.sleep(2)
        chat.page_contain_element(locator='多选按钮')
        chat.page_contain_element(locator='多选-删除')
        chat.page_contain_element(locator='多选-转发')

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0143(self):
        """普通企业群/长ID企业群：日志--“分享至当前群”功能验证"""
        # 1、在企业群进入“日志”应用后点击发起任意日志类型--填写完全部信息及选择了“接收人”后开启“分享至当前群”按钮
        log = DailyRecordPage()
        # 进入日志编辑页
        time.sleep(2)
        log.click_journals()
        log.click_daily_paper()
        log.wait_log_editor_page_load()
        time.sleep(2)
        # 输入日志内容
        log.input_work_summary('测试文本')
        log.click_add_icon()
        time.sleep(2)
        SelectHeContactsDetailPage().select_one_he_contact_by_name('大佬1')
        SelectHeContactsDetailPage().click_sure_icon()
        log.click_share_to_group()  # 分享至当前群
        # 2、点击页面下方的“提交”按钮
        log.click_submit()
        time.sleep(3)
        # 2、toast提示“提交成功”、自动跳转到群聊界面且发送该日志卡片消息到群内
        chat = GroupChatPage()
        self.assertTrue(chat.is_on_this_page())
        self.assertTrue(chat.is_element_present_message())
        # 3、日志发起人在工作台--该企业下--日志应用内--我发出的板块下出现该新增的日志
        Preconditions.make_already_in_message_page()
        MessagePage().open_workbench_page()
        work = WorkbenchPage()
        work.click_journal()
        log.wait_for_page_load()
        self.assertTrue(log.is_on_daily_record_page())
        self.assertTrue(log.is_text_present('今日工作总结'))
        # 4、日志接收人在工作台--该企业下--日志应用内--我收到的板块下出现该新增的日志（接收人涉及双机）


    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0147(self):
        """普通企业群/长ID企业群：日志转聊天后发送人“长按”日志卡片消息--转发（本网号为例）"""
        # 确保在群聊页面有日志信息
        Preconditions.make_sure_chatwindow_have_daily_log_message()
        chat = GroupChatPage()
        # 1、审批发起人长按该审批卡片消息--点击“转发”--转发到一个单聊
        chat = SingleChatPage()
        chat.wait_for_page_load()
        select = SelectContactsPage()
        chat.press_and_move_right_daily_log()
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
        chat.press_and_move_right_daily_log()
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
        chat.press_and_move_right_daily_log()
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
        chat.press_and_move_right_daily_log()
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

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0148(self):
        """普通企业群/长ID企业群：日志转聊天后发送人“长按”日志卡片消息--收藏（本网号为例）"""
        # 确保在群聊页面有日志信息
        Preconditions.make_sure_chatwindow_have_daily_log_message()
        chat = GroupChatPage()
        # 1、审批发起人长按该审批卡片消息--点击“收藏”
        chat.press_and_move_right_daily_log()
        chat.click_collection()
        time.sleep(2)
        # 2、进入“我”模块--收藏内查看是否收藏成功且展示是否正常
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        MePage().click_collection()
        collection = MeCollectionPage()
        collection.wait_for_page_load()
        time.sleep(3)
        collection.page_should_contain_text('日报')
        # 3、点击查看该收藏详情
        collection.click_element_first_list()
        time.sleep(4)
        self.assertTrue(collection.is_exist_element(locator='点赞'))
        self.assertTrue(collection.is_exist_element(locator='评论'))
        # 3、详情页内容应与“工作台--我发起的--查看该日志详情”内容一致且可做相应操作(可点赞 可收藏)
        Preconditions.make_already_in_message_page()
        MessagePage().open_workbench_page()
        work = WorkbenchPage()
        work.click_journal()
        log = DailyRecordPage()
        log.wait_for_page_load()
        self.assertTrue(log.is_on_daily_record_page())
        log.click_already_submit_log()
        time.sleep(4)
        self.assertTrue(log.is_exist_element(locator='点赞'))
        self.assertTrue(log.is_exist_element(locator='评论'))


    def setUp_test_msg_hanjiabin_0149(self):
        """确保每个用例开始之前进入企业群日志页面"""
        warnings.simplefilter('ignore',ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        Preconditions.enter_enterprise_group_by_name()
        time.sleep(3)

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0149(self):
        """普通企业群/长ID企业群：日志转聊天后发送人“长按”日志卡片消息--撤回"""
        # 确保在群聊页面有日志信息
        Preconditions.make_sure_chatwindow_have_daily_log_message()
        # 1、日志发起人长按该日志卡片消息--点击“撤回”
        chat = GroupChatPage()
        chat.press_and_move_right_daily_log()
        chat.click_revoke()
        time.sleep(2)
        # 1、APP端发出方和接收方查看皆已正常撤回、PC端同步被撤回
        self.assertTrue(chat.is_element_present_by_locator(locator='你撤回了一条消息'))

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0150(self):
        """普通企业群/长ID企业群：日志转聊天后发送人“长按”日志卡片消息--删除"""
        # 确保在群聊页面有日志信息
        Preconditions.make_sure_chatwindow_have_daily_log_message()
        # 1、日志发起人长按该日志卡片消息--点击“删除”
        chat = GroupChatPage()
        chat.press_and_move_right_daily_log()
        chat.click_delete()
        time.sleep(3)
        chat.click_sure_delete()
        # 1、自己的群聊界面内该条审批卡片消息被删除
        time.sleep(3)
        self.assertFalse(chat.is_element_present_message())

    @tags('ALL', 'enterprise_group', 'CMCC')
    def test_msg_hanjiabin_0151(self):
        """普通企业群/长ID企业群：日志转聊天后发送人“长按”日志卡片消息--多选"""
        # 确保在群聊页面有日志信息
        Preconditions.make_sure_chatwindow_have_daily_log_message()
        # 1、日志发起人长按该日志卡片消息--点击“多选”
        chat = GroupChatPage()
        chat.press_and_move_right_daily_log()
        time.sleep(2)
        chat.click_multiple_selection()
        time.sleep(2)
        chat.page_contain_element(locator='多选按钮')
        chat.page_contain_element(locator='多选-删除')
        chat.page_contain_element(locator='多选-转发')
























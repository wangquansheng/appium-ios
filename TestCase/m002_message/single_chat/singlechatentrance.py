import random
import time
import warnings

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from pages.components import BaseChatPage
from pages.message.FreeMsg import FreeMsgPage
from preconditions.BasePreconditions import LoginPreconditions
from library.core.utils.testcasefilter import tags
from pages import *
import uuid
import unittest


class Preconditions(LoginPreconditions):
    """前置条件"""

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


class MsgPrivateChatMsgList(TestCase):
    """
    模块：单聊->消息列表
    文件位置：115整理全量测试用例.xlsx
    表格：单聊
    """

    def default_setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')

    def default_tearDown(self):
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', "msg")
    def test_msg_huangcaizui_A_0273(self):
        """从全局搜索中搜索号码进入单聊"""
        # 实现准自动化
        # 1.客户端已登录
        # 2.网络正常
        # 1.点击消息首页上的全局搜索框
        mpg = MessagePage()
        mpg.click_search_box()
        # 1.调起键盘，输入框显示灰色字体“输入关键字快速搜索”
        mpg.page_should_contain_text("输入关键字快速搜索")

        # 2.输入号码进行搜索
        mpg.input_search_text("13800138005")

        # 2.显示所有有关该关键字的相关信息，如联系人、搜索我的团队、群聊、聊天记录
        mpg.page_should_contain_text("手机联系人")
        mpg.page_should_contain_text("大佬1")
        mpg.page_should_contain_text("团队联系人")

        # 3.选择任意联系人
        mpg.click_text("大佬1")

        # 3.进入单聊页面(进入联系人详情？)
        mpg.page_should_contain_text("好久不见~打个招呼吧")
        mpg.page_should_contain_text("大佬1")
        mpg.page_should_contain_text("13800138005")

    @tags('ALL', 'CMCC', "msg")
    def test_msg_huangcaizui_A_0274(self):
        """从新建消息进入单聊"""
        # 1.客户端已登录
        # 2.网络正常
        # 1.点击右上角“+”
        mpg = MessagePage()
        mpg.open_message_page()
        mpg.click_add_icon()
        # 1.弹出多功能列表
        time.sleep(1)
        mpg.page_should_contain_text("新建消息")
        mpg.page_should_contain_text("免费短信")
        mpg.page_should_contain_text("发起群聊")
        mpg.page_should_contain_text("群发助手")
        mpg.page_should_contain_text("扫一扫")
        # 2.点击新建消息
        mpg.click_new_message()
        # 2.进入联系人选择器，（可在搜索框输入联系人姓名或电话号码搜索/直接选择本地通讯录联系人/选择团队联系人
        scp = SelectContactsPage()
        scp.page_should_contain_text("选择联系人")
        scp.page_should_contain_text("搜索或输入手机号")
        slc = SelectLocalContactsPage()
        slc.input_search_keyword("13800138005")
        # 3.任意选择一联系人
        slc.selecting_local_contacts_by_name("大佬1")
        time.sleep(1)
        # 3.进入单聊页面
        self.assertTrue(SingleChatPage().is_on_this_page())

        slc.click_back()
        mpg.delete_the_first_msg()

    @tags('ALL', 'CMCC', "msg")
    def test_msg_huangcaizui_A_0275(self):
        """从发送短信进入单聊（首次）"""
        # 1.客户端已登录
        # 2.网络正常
        # 1.点击右上角“+”
        mpg = MessagePage()
        mpg.open_message_page()
        mpg.click_add_icon()
        # 1.弹出多功能列表
        time.sleep(1)
        mpg.page_should_contain_text("新建消息")
        mpg.page_should_contain_text("免费短信")
        mpg.page_should_contain_text("发起群聊")
        mpg.page_should_contain_text("群发助手")
        mpg.page_should_contain_text("扫一扫")
        # # 2.点击发送短信
        mpg.click_free_sms()
        # 2.弹出短信资费介绍页“欢迎使用免费短信！”/“欢迎使用短信”（首次才会弹出）
        if mpg.is_text_present("欢迎使用免费短信"):
            mpg.page_should_contain_text("欢迎使用免费短信")
            # 3.点击确定
            FreeMsgPage().click_sure_btn()
        time.sleep(1)
        # 3.进入联系人选择器（可在搜索框输入联系人姓名或电话号码搜索/直接选择本地通讯录联系人/选择团队联系人
        scp = SelectContactsPage()
        scp.page_should_contain_text("选择联系人")
        scp.page_should_contain_text("搜索或输入手机号")
        slc = SelectLocalContactsPage()
        slc.input_search_keyword("13800138005")
        # 4.任意选择一联系人
        slc.selecting_local_contacts_by_name("大佬1")
        time.sleep(1)

        # 5.进入短信编辑页面
        slc.page_should_contain_text("发送短信")
        self.assertTrue(SingleChatPage().is_on_this_page())

        slc.click_back()

    @tags('ALL', '异网', "msg")
    def test_msg_huangcaizui_A_0276(self):
        """从发送短信进入单聊（异网用户）"""
        # 1.客户端已登录
        # 2.网络正常
        # 3.异网用户
        # 1.点击右上角“+”
        mpg = MessagePage()
        mpg.open_message_page()
        mpg.click_add_icon()
        # 1.弹出多功能列表
        time.sleep(1)
        mpg.page_should_contain_text("新建消息")
        mpg.page_should_contain_text("免费短信")
        mpg.page_should_contain_text("发起群聊")
        mpg.page_should_contain_text("群发助手")
        mpg.page_should_contain_text("扫一扫")
        # # 2.点击发送短信
        mpg.click_free_sms()
        # 2.进入联系人选择器（可在搜索框输入联系人姓名或电话号码搜索/直接选择本地通讯录联系人/选择团队联系人
        scp = SelectContactsPage()
        scp.page_should_contain_text("选择联系人")
        scp.page_should_contain_text("搜索或输入手机号")
        slc = SelectLocalContactsPage()
        slc.input_search_keyword("13800138005")
        # 3.任意选择一联系人
        slc.selecting_local_contacts_by_name("大佬1")
        time.sleep(1)
        # 3.进入短信编辑页面
        slc.page_should_contain_text("发送短信")
        self.assertTrue(SingleChatPage().is_on_this_page())
        slc.click_back()

    @tags('ALL', 'CMCC', "msg")
    def test_msg_huangcaizui_A_0278(self):
        """从通话——通话详情——进入单聊页面"""
        # 1.客户端已登录
        # 2.网络正常
        # 3.在通话模块
        # 1.任意选择一联系人，点击右边通话详情按钮
        cpg = CallPage()
        cpg.click_call()
        cpg.create_call_entry("13800138005")
        cpg.click_dial()
        cpg.click_call_time_search_status()
        time.sleep(2)
        # 1.进入联系人详情页面
        cpg.page_should_contain_text("分享名片")
        self.assertTrue(CallContactDetailPage().is_exist_star())
        # 2.点击消息
        CallContactDetailPage().click_normal_message()
        # 2.进入单聊页面
        chatpage = BaseChatPage()
        flag = chatpage.is_exist_dialog()
        if flag:
            chatpage.click_i_have_read()
        cpg.page_should_contain_text("说点什么...")
        self.assertTrue(SingleChatPage().is_on_this_page())

    @tags('ALL', 'CMCC', "msg")
    def test_msg_huangcaizui_A_0281(self):
        """联系——选择团队联系人——进入单聊页面"""
        # 1.客户端已登录
        # 2.网络正常
        # 3.在联系模块
        MessagePage().click_contacts()
        # 1.任意选择一个团队
        cpg = ContactsPage()
        cpg.click_team_head()
        # 1.进入团队联系人
        cpg.page_should_contain_text("搜索：当前组织")
        # 2.任意选择联系人
        cpg.click_text("测试号码")
        # 2.进入联系人详情页面
        cpg.page_should_contain_text("分享名片")
        cpg.page_should_contain_text("好久不见~打个招呼吧")
        # 3.点击消息
        CallContactDetailPage().click_normal_message()

        # 3.进入单聊页面
        chatpage = BaseChatPage()
        flag = chatpage.is_exist_dialog()
        if flag:
            chatpage.click_i_have_read()
        cpg.page_should_contain_text("说点什么...")
        self.assertTrue(SingleChatPage().is_on_this_page())






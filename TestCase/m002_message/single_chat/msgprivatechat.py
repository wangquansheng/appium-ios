import random
import time
import warnings

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from pages.components import BaseChatPage
from preconditions.BasePreconditions import LoginPreconditions
from library.core.utils.testcasefilter import tags
from pages import *
import uuid


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

class MsgContactSelector(TestCase):
    """
    模块：单聊->联系人选择器
    文件位置：115全量测试用例.xlsx
    表格：单聊
    """
    def default_setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')

    def default_tearDown(self):
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'msg')
    def test_msg_huangcaizui_A_0001(self):
        """ 进入新建消息是否正常"""
        # 1.点击右上角的+
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        time.sleep(1)
        mp.page_should_contain_text("新建消息")
        mp.page_should_contain_text("免费短信")
        mp.page_should_contain_text("发起群聊")
        mp.page_should_contain_text("群发助手")
        mp.page_should_contain_text("扫一扫")
        # 点击“新建消息”
        mp.click_new_message()
        # 3.查看页面展示
        scp = SelectContactsPage()
        # 左上角标题：选择联系人；搜索栏缺省文字：搜索或输入手机号；
        # 选择和通讯录联系人；下方为本地联系人列表
        scp.page_should_contain_text("选择联系人")
        scp.page_should_contain_text("搜索或输入手机号")
        scp.page_should_contain_text("选择团队联系人")

    @tags('ALL', 'CMCC', 'msg')
    def test_msg_huangcaizui_A_0022(self):
        """免费/发送短信—选择手机联系人"""
        # 1.网络正常
        # 2.免费/发送短信—联系人选择器页面
        # Step: 1.查看手机联系人的页面展示规则
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        time.sleep(1)
        mp.click_free_sms()
        # CheckPoint: 1.页面展示：星标联系人排序在前；手机联系人；自己号码不可选，下拉可查看更多联系人
        mp.page_should_contain_text("选择联系人")

        # Step: 2.点击任意联系人
        SelectLocalContactsPage().selecting_local_contacts_by_name("香港大佬")

        # CheckPoint: 2.跳转到短信编辑页面
        mp.page_should_contain_text("你正在使用短信功能")

    @tags('ALL',  'CMCC', 'msg')
    def test_msg_huangcaizui_A_0023(self):
        """最近聊天选择器：单聊内转发消息"""
        # 1.网络正常
        # 2、存在可转发的消息
        # Step：1、在聊天会话页面，长按可转发的消息，是否可以跳转到联系人选择器页面
        Preconditions.enter_single_chat_page("香港大佬")
        chat = SingleChatPage()
        scp = SingleChatPage()
        text = "hello"
        # 收起键盘
        scp.swipe_by_percent_on_screen(50, 60, 50, 10)
        time.sleep(1)
        scp.input_text_message(text)
        scp.send_text()
        chat.press_mess('hello')
        time.sleep(1)
        chat.click_to_do('转发')
        # CheckPoint：1、在聊天会话页面，长按可转发的消息，可以跳转到联系人选择器页面
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.page_should_contain_text("选择联系人")
        for i in range(2):
            scp.click_back()
        MessagePage().delete_the_first_msg()





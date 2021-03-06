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

    @staticmethod
    def make_already_in_message_page(reset=False):
        """确保应用在消息页面"""
        # 如果在消息页，不做任何操作
        mp = MessagePage()
        if mp.is_on_this_page():
            return
        else:
            try:
                current_mobile().launch_app()
                mp.wait_for_page_load()
            except:
                # 进入一键登录页
                Preconditions.make_already_in_one_key_login_page()
                #  从一键登录页面登录
                Preconditions.login_by_one_key_login()


class SingleChatEntrance(TestCase):
    """
    模块：单聊->单聊入口
    文件位置：115整理全量测试用例.xlsx
    表格：单聊入口
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
        cpg.click_text("alice")
        # 3.进入联系人详情页面，点击消息
        time.sleep(2)
        CallContactDetailPage().click_normal_message()
        time.sleep(2)
        # 4.进入单聊页面
        scp = SingleChatPage()
        scp.wait_for_page_load()
        self.assertTrue(SingleChatPage().is_on_this_page())

    @tags('ALL', 'CMCC', "msg")
    def test_msg_huangcaizui_A_0282(self):
        """联系——搜索团队联系人——进入单聊页面"""
        # 1.客户端已登录
        # 2.网络正常
        # 3.在联系模块
        # 1.在搜索框输入姓名或号码搜索联系人
        MessagePage().click_contacts()
        cpg = ContactsPage()
        cpg.click_team_head()
        cpg.page_should_contain_text("搜索：当前组织")
        SelectHeContactsDetailPage().input_search_text("13800138005")
        time.sleep(1)
        # 1.结果匹配到相关的团队联系人
        cpg.page_should_contain_text("大佬1")
        cpg.page_should_contain_text("测试部门")
        # 2.任意选择一团队联系人
        cpg.click_text("大佬1")
        # 1.进入联系人详情页面
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

    @tags('ALL', 'CMCC', "msg")
    def test_msg_huangcaizui_A_0354(self):
        """联系——搜索手机联系人——进入单聊页面"""
        # 1.客户端已登录
        # 2.网络正常
        # 3.在联系模块
        # 1.在搜索框输入姓名或号码搜索联系人
        MessagePage().click_contacts()
        cpg = ContactsPage()
        cpg.click_phone_contact()
        cpg.page_should_contain_text("手机联系人")
        cpg.page_should_contain_text("搜索手机联系人")
        cpg.click_search_phone_contact()
        cpg.input_search_keyword("13800138005")
        # 1.结果匹配到相关的手机联系人
        # 2.任意选择一手机联系人
        cpg.click_element_contact()
        time.sleep(1)
        # 1.进入联系人详情页面
        cpg.page_should_contain_text("分享名片")
        cpg.page_should_contain_text("好久不见~打个招呼吧")
        # 3.点击消息
        CallContactDetailPage().click_normal_message()
        # 2.进入单聊页面
        chatpage = BaseChatPage()
        flag = chatpage.is_exist_dialog()
        if flag:
            chatpage.click_i_have_read()
        cpg.page_should_contain_text("说点什么...")
        self.assertTrue(SingleChatPage().is_on_this_page())

    @classmethod
    def setUp_test_msg_huangcaizui_A_0283(self):
        """进入标签分组会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        LoginPreconditions.select_mobile('IOS-移动')
        lable_group = LabelGroupingPage()
        lable_detail = LableGroupDetailPage()
        #确保在消息页面
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        MessagePage().open_contacts_page()
        contact = ContactsPage()
        contact.click_phone_contact()
        time.sleep(2)
        contact.click_label_grouping()
        #确保进入标签分组会话页面
        if not lable_group.is_element_present(locator='已建分组列表1'):
            lable_group.creat_group('aaa')
            time.sleep(2)
            # 为标签分组添加成员
            lable_group.click_first_lable_group()
            time.sleep(2)
            lable_detail.click_add_contact()
            local_contact = SelectLocalContactsPage()
            local_contact.swipe_select_one_member_by_name('大佬1')
            local_contact.swipe_select_one_member_by_name('大佬2')
            local_contact.click_sure()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', "msg")
    def test_msg_huangcaizui_A_0283(self):
        """联系——标签分组——进入单聊页面（多名成员）"""
        # 1.客户端已登录
        # 2.网络正常
        # 3.在联系模块
        # TODO
        # 预置条件中加入标签分组删除和新建
        # 1.点击上方标签分组图标
        MessagePage().click_contacts()
        cpg = ContactsPage()
        cpg.click_phone_contact()
        cpg.click_label_grouping()
        # 1.进入标签分组页面
        cpg.page_should_contain_text("标签分组")
        cpg.page_should_contain_text("新建分组")
        # 2.任意点击一存在多名成员的标签分组
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        # 2.进入成员列表页，显示该标签分组中的所有成员
        self.assertTrue(LableGroupDetailPage().is_exists_lable_group_setting())
        cpg.page_should_contain_text("大佬1")
        cpg.page_should_contain_text("大佬2")
        # 3.任意选择一标签分组中的联系人
        cpg.click_text("大佬1")
        # 3.进入联系人详情页面
        cpg.page_should_contain_text("分享名片")
        cpg.page_should_contain_text("好久不见~打个招呼吧")
        # 4.点击消息
        CallContactDetailPage().click_normal_message()
        # 4.进入单聊页面
        chatpage = BaseChatPage()
        flag = chatpage.is_exist_dialog()
        if flag:
            chatpage.click_i_have_read()
        cpg.page_should_contain_text("说点什么...")
        self.assertTrue(SingleChatPage().is_on_this_page())

    @tags('ALL', 'CMCC', "msg")
    def test_msg_huangcaizui_A_0284(self):
        """联系——标签分组——进入单聊页面（一名成员）"""
        # 1.客户端已登录
        # 2.网络正常
        # 3.在联系模块
        # TODO
        # 预置条件中加入标签分组删除和新建
        # 1.点击上方标签分组图标
        MessagePage().click_contacts()
        cpg = ContactsPage()
        cpg.click_phone_contact()
        cpg.click_label_grouping()
        # 1.进入标签分组页面
        cpg.page_should_contain_text("标签分组")
        cpg.page_should_contain_text("新建分组")
        # 2.点击只有一名成员的标签分组
        LabelGroupingPage().click_label_grouping_head(0)
        # 2.进入成员列表页面
        self.assertTrue(LableGroupDetailPage().is_exists_lable_group_setting())
        cpg.page_should_contain_text("大佬1")
        # 3.点击群发消息按钮
        LableGroupDetailPage().click_send_group_info()
        # 3.进入单聊页面
        chatpage = BaseChatPage()
        flag = chatpage.is_exist_dialog()
        if flag:
            chatpage.click_i_have_read()
        time.sleep(2)
        cpg.page_should_contain_text("说点什么...")
        self.assertTrue(LabelGroupingChatPage().is_on_this_page())

    @tags('ALL', 'CMCC', "msg")
    def test_msg_huangcaizui_A_0285(self):
        """联系——+号——添加联系人——进入单聊页面"""
        # 1.客户端已登录
        # 2.网络正常
        # 1.点击右上角“+”
        MessagePage().click_contacts()
        cpg = ContactsPage()
        cpg.click_phone_contact()
        SelectLocalContactsPage().click_add_icon()
        # 1.进入新建联系人编辑页面
        cpg.page_should_contain_text('新建联系人')
        # 2.编辑好信息，点击保存
        CreateContactPage().input_name("测试")
        CreateContactPage().input_number("13800138020")
        CreateContactPage().click_save()
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

    @staticmethod
    def tearDown_test_msg_huangcaizui_A_0285():
        """删除指定联系人"""
        Preconditions.make_already_in_message_page()
        ContactDetailsPage().delete_contact("测试")
        Preconditions.disconnect_mobile('IOS-移动')

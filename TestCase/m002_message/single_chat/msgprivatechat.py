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
    def test_msg_huangcaizui_A_0044(self):
        """消息-消息列表进入"""
        # 1、点击消息
        mess = MessagePage()
        mess.open_message_page()
        if not mess.is_on_this_page():
            raise AssertionError("未成功进入消息列表页面")

    @tags('ALL', 'CMCC', "msg")
    def test_msg_huangcaizui_A_0045(self):
        """消息-消息列表界面+功能页面元素检查"""
        # 1、点击消息
        mess = MessagePage()
        mess.open_message_page()
        # 2、点击右上角的+号按钮
        mess.click_add_icon()
        time.sleep(1)
        # 下拉出“新建消息”、“免费短信”、“发起群聊”、分组群发、“扫一扫”，入口
        mess.page_should_contain_text("新建消息")
        mess.page_should_contain_text("免费短信")
        mess.page_should_contain_text("发起群聊")
        mess.page_should_contain_text("群发助手")
        mess.page_should_contain_text("扫一扫")

    @tags('ALL', 'CMCC', "msg")
    def test_msg_huangcaizui_A_0049(self):
        """消息-消息列表界面新建消息页面返回操作"""
        # 1、点击右上角的+号按钮，成功进入新建消息界面
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        # 2、点击左上角返回按钮，退出新建消息，返回消息列表
        scp = SelectContactsPage()
        scp.wait_for_create_msg_page_load()
        scp.click_back()
        mess.wait_for_page_load()

    @tags('ALL', 'CMCC', "msg")
    def test_msg_huangcaizui_A_0052(self):
        """消息-消息列表进入到会话页面"""
        # 1、正常联网环境
        # 2、成功登录客户端
        # 3、消息列表页面有一对一会话
        # 4、当前在消息列表页面
        # 1、在消息列表点击消息记录
        Preconditions.enter_single_chat_page("香港大佬")
        scp = SingleChatPage()
        text = "hello"
        # 收起键盘
        scp.swipe_by_percent_on_screen(50, 60, 50, 10)
        time.sleep(1)
        scp.input_text_message(text)
        scp.send_text()
        scp.click_back()

        # 1、进入到会话页面
        MessagePage().click_message_session(0)
        time.sleep(1)
        if not scp.wait_for_page_load():
            raise AssertionError("未进入聊天界面")
        scp.click_back()
        MessagePage().delete_the_first_msg()

    @tags('ALL', 'CMCC', "msg")
    def test_msg_huangcaizui_A_0058(self):
        """新建消息入口首次进入一对一聊天页面是否有弹框出来"""
        # 1.正常联网
        # 2.客户端在线
        # 3.用户首次使用和飞信发送一对一消息
        # 1.进入消息模块页面
        mess = MessagePage()
        mess.open_message_page()
        # 2.点击右上角“+”
        mess.click_add_icon()
        time.sleep(1)
        # 2.弹出多功能列表
        mess.page_should_contain_text("新建消息")
        mess.page_should_contain_text("免费短信")
        mess.page_should_contain_text("发起群聊")
        mess.page_should_contain_text("群发助手")
        mess.page_should_contain_text("扫一扫")
        # 3.点击新建消息
        mess.click_new_message()
        # 3.进入联系人选择器
        scp = SelectContactsPage()
        scp.page_should_contain_text("选择联系人")
        # 4.任意选择一个联系人（搜索手机联系人、选择手机联系人或选择团队联系人）
        slc = SelectLocalContactsPage()
        slc.selecting_local_contacts_by_name("香港大佬")
        time.sleep(1)
        # 4.进入一对一聊天页面，同时弹出“使用须知”弹框
        # IOS首次使用，使用须知待实现，先实现准自动化
        # mess.page_should_contain_text("使用须知")
        if not SingleChatPage().wait_for_page_load():
            raise AssertionError("未进入聊天界面")
        SingleChatPage().click_back()
        MessagePage().delete_the_first_msg()

    @tags('ALL', 'CMCC', "msg")
    def test_msg_huangcaizui_A_0059(self):
        """观察从新建消息入口出现的弹框页面"""
        # 1.正常联网
        # 2.客户端在线
        # 3.用户首次使用和飞信发送一对一消息
        # 1.进入消息模块页面
        mess = MessagePage()
        mess.open_message_page()
        # 2.点击右上角“+”
        mess.click_add_icon()
        time.sleep(1)
        # 2.弹出多功能列表
        mess.page_should_contain_text("新建消息")
        mess.page_should_contain_text("免费短信")
        mess.page_should_contain_text("发起群聊")
        mess.page_should_contain_text("群发助手")
        mess.page_should_contain_text("扫一扫")
        # 3.点击新建消息
        mess.click_new_message()
        # 3.进入联系人选择器
        scp = SelectContactsPage()
        scp.page_should_contain_text("选择联系人")
        # 4.任意选择一个联系人（搜索手机联系人、选择手机联系人或选择团队联系人）
        slc = SelectLocalContactsPage()
        slc.selecting_local_contacts_by_name("香港大佬")
        time.sleep(1)
        # 4.进入一对一聊天页面，同时弹出“使用须知”弹框
        # IOS首次使用，使用须知待实现，先实现准自动化
        # mess.page_should_contain_text("使用须知")
        # 5.查看弹框页面
        # 5.弹框内容为消息转短的资费提醒，底部左边有单选按钮“我已阅读”，底部右下角有置灰的“确定”按钮
        # mess.page_should_contain_text("我已阅读")
        # mess.page_should_contain_text("确定")
        if not SingleChatPage().wait_for_page_load():
            raise AssertionError("未进入聊天界面")
        SingleChatPage().click_back()
        MessagePage().delete_the_first_msg()

    @tags('ALL', 'CMCC', "msg")
    def test_msg_huangcaizui_A_0061(self):
        """观察从新建消息入口出现的弹框页面"""
        # 1.正常联网
        # 2.客户端在线
        # 3.用户首次使用和飞信发送一对一消息
        # 1.进入消息模块页面
        mess = MessagePage()
        mess.open_message_page()
        # 2.点击右上角“+”
        mess.click_add_icon()
        time.sleep(1)
        # 2.弹出多功能列表
        mess.page_should_contain_text("新建消息")
        mess.page_should_contain_text("免费短信")
        mess.page_should_contain_text("发起群聊")
        mess.page_should_contain_text("群发助手")
        mess.page_should_contain_text("扫一扫")
        # 3.点击新建消息
        mess.click_new_message()
        # 3.进入联系人选择器
        scp = SelectContactsPage()
        scp.page_should_contain_text("选择联系人")
        # 4.任意选择一个联系人（搜索手机联系人、选择手机联系人或选择团队联系人）
        slc = SelectLocalContactsPage()
        slc.selecting_local_contacts_by_name("香港大佬")
        time.sleep(1)
        # IOS首次使用，使用须知待实现，先实现准自动化
        # 4.进入一对一聊天页面，同时弹出“使用须知”弹框
        # mess.page_should_contain_text("使用须知")
        # 5.查看弹框页面
        # 5.弹框内容为消息转短的资费提醒，底部左边有单选按钮“我已阅读”，底部右下角有置灰的“确定”按钮
        # mess.page_should_contain_text("我已阅读")
        # mess.page_should_contain_text("确定")
        # 6.点选我已阅读按钮
        # ChatWindowPage().click_already_read()
        # 7.点击确定按钮
        # ChatWindowPage().click_sure_icon()
        # 6.确定按钮变高亮色
        # 7.弹框消失，停留在一对一聊天会话窗口
        # time.sleep(1)
        # mess.page_should_not_contain_text("我已阅读")
        # mess.page_should_not_contain_text("确定")
        if not SingleChatPage().wait_for_page_load():
            raise AssertionError("未进入聊天界面")
        SingleChatPage().click_back()
        MessagePage().delete_the_first_msg()


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
        scp = SingleChatPage()
        text = "hello"
        # 收起键盘
        scp.swipe_by_percent_on_screen(50, 60, 50, 10)
        time.sleep(1)
        scp.input_text_message(text)
        scp.send_text()
        scp.press_mess('hello')
        time.sleep(1)
        scp.click_to_do('转发')
        # CheckPoint：1、在聊天会话页面，长按可转发的消息，可以跳转到联系人选择器页面
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.page_should_contain_text("选择联系人")
        for i in range(2):
            scp.click_back()
        MessagePage().delete_the_first_msg()


class MsgPrivateChatMsgSetting(TestCase):
    """
    模块：单聊->单聊设置
    文件位置：115整理全量测试用例.xlsx
    表格：单聊
    """

    def default_setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')

    def default_tearDown(self):
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'msg')
    def test_msg_huangcaizui_A_0064(self):
        """消息—一对一消息会话—设置"""
        # 1.正常联网
        # 2.正常登录
        # 3.消息会话界面内
        Preconditions.enter_single_chat_page("香港大佬")
        chat = SingleChatPage()
        # 1.点击右上角的c设置按钮
        chat.click_setting()
        # 1.进入聊天设置页面
        chat.page_should_contain_text("聊天设置")

    @tags('ALL', 'CMCC', 'msg')
    def test_msg_huangcaizui_A_0065(self):
        """消息—一对一消息会话—设置页面头像转跳"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前在一对一设置页面
        self.test_msg_huangcaizui_A_0064()
        # 1. 点击联系人头像
        SingleChatSetPage().click_avatar()
        # 1. 点击联系人进入到联系人详情页。
        ContactDetailsPage().page_should_contain_text("编辑")
        ContactDetailsPage().page_should_contain_text("好久不见~打个招呼吧")



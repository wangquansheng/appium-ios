import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from preconditions.BasePreconditions import WorkbenchPreconditions
from pages import *
import warnings

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    # 'Android-移动': 'single_mobile',
    'IOS-移动': 'iphone',
    'IOS-移动-移动': 'M960BDQN229CHiphone8',
}

class Preconditions(WorkbenchPreconditions):
    """前置条件"""

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

    @staticmethod
    def enter_group_messenger_page():
        """进入群发信使首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_group_messenger()

    @staticmethod
    def enter_collection_page():
        """进入收藏页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_me_page()
        me_page = MePage()
        me_page.wait_for_page_load()
        me_page.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        time.sleep(1)


class CommonGroupPress(TestCase):
    """普通群页面--长按"""

    @classmethod
    def setUpClass(cls):
        """删除消息列表的消息记录"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        # 删除消息列表
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        time.sleep(3)

    @classmethod
    def default_setUp(self):
        """确保每个用例执行前在群聊聊天界面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        name = '群聊1'
        if msg.is_text_present(name):
            msg.click_text(name)
        else:
            msg.click_search_box()
            time.sleep(1)
            msg.input_search_text(name)
            time.sleep(2)
            msg.click_element_first_list()
            time.sleep(2)

    def default_tearDown(self):
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_xiaoqiu_0051(self):
        """在聊天会话页面，长按文本消息——转发——选择一个群作为转发对象"""
        # 确保当前页面有文本消息记录
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        select = SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        # 2、选择一个群，进入到群聊列表展示页面，任意选中一个群聊，确认转发，会在消息列表，重新产生一个新的会话窗口或者在已有窗口中增加一条记录
        select.click_select_one_group()
        group = SelectOneGroupPage()
        name = '群聊2'
        group.selecting_one_group_by_name(name)
        group.click_sure_send()
        time.sleep(2)
        # 在消息列表，重新产生一个新的会话窗口
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.page_should_contain_text(name)
        # 3、进入到聊天会话窗口页面，转发的消息，已发送成功并正常展示
        mess.click_text(name)
        self.assertTrue(chat.is_element_present_message())


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_xiaoqiu_0052(self):
        """在聊天会话页面，长按文本消息——转发——选择团队联系人作为转发对象"""
        # 确保当前页面有文本消息记录
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        select = SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        # 2、选择一个群，进入到群聊列表展示页面，任意选中一个团队联系人，确认转发，会在消息列表，重新产生一个新的会话窗口或者在已有窗口中增加一条记录
        name = '大佬2'
        select.click_group_contact()
        group_contact = SelectHeContactsPage()
        group_contact.select_one_team_by_name('ateam7272')
        group_detail = SelectHeContactsDetailPage()
        time.sleep(2)
        group_detail.select_one_he_contact_by_name(name)
        group_detail.click_sure()
        time.sleep(2)
        # 在消息列表，重新产生一个新的会话窗口
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.page_should_contain_text(name)
        # 3、进入到聊天会话窗口页面，转发的消息，已发送成功并正常展示
        mess.click_text(name)
        self.assertTrue(chat.is_element_present_message())


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_xiaoqiu_0053(self):
        """在聊天会话页面，长按文本消息——转发——选择手机联系人作为转发对象"""
        # 确保当前页面有文本消息记录
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        select = SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        # 2、选择一个群，进入到群聊列表展示页面，任意选中一个手机联系人，确认转发，会在消息列表，重新产生一个新的会话窗口或者在已有窗口中增加一条记录
        name = '大佬1'
        select.select_local_contacts()
        local_contact = SelectLocalContactsPage()
        self.assertEqual(local_contact.is_on_this_page(), True)
        local_contact.swipe_select_one_member_by_name(name)
        local_contact.click_sure()
        time.sleep(2)
        # 在消息列表，重新产生一个新的会话窗口
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.page_should_contain_text(name)
        # 3、进入到聊天会话窗口页面，转发的消息，已发送成功并正常展示
        mess.click_text(name)
        self.assertTrue(chat.is_element_present_message())


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_xiaoqiu_0054(self):
        """在聊天会话页面，长按文本消息——转发——选择最近聊天作为转发对象"""
        # 确保当前页面有文本消息记录
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        select = SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        # 2、选择一个群，进入到群聊列表展示页面，任意选中最近聊天，确认转发，会在消息列表，重新产生一个新的会话窗口或者在已有窗口中增加一条记录
        name = select.get_recent_chat_contact_name()
        select.click_recent_chat_contact()
        select.click_sure_forward()
        time.sleep(2)
        # 在消息列表，重新产生一个新的会话窗口
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.page_should_contain_text(name)
        # 3、进入到聊天会话窗口页面，转发的消息，已发送成功并正常展示
        mess.click_text(name)
        self.assertTrue(chat.is_element_present_message())

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_xiaoqiu_0070(self):
        """仅发送文字模式下，输入框存在内容后，点击发送按钮"""
        # 设置语音模式为：仅发送文字模式
        chat = GroupChatPage()
        chat.click_voice()
        audio = ChatAudioPage()
        audio.setting_voice_icon_in_send_text_only()
        # 2、输入框中存在内容后，点击发送按钮，发送出去的消息是否展示为文本消息(暂时无法判断是否为文本消息)
        chat.click_input_box()
        chat.input_message_text('文本消息')
        chat.click_send_button()
        time.sleep(2)

import time

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from preconditions.BasePreconditions import WorkbenchPreconditions
import warnings
from pages import *


class Preconditions(WorkbenchPreconditions):

    @staticmethod
    def send_file_by_type(file_type):
        """发送指定类型文件"""

        cwp = ChatWindowPage()
        cwp.click_file()
        cwp.click_accessibility_id_attribute_by_name("我收到的文件")
        cslfp = ChatSelectLocalFilePage()
        cslfp.click_file_by_type(file_type)
        cslfp.click_send_button()
        time.sleep(5)


class MessagePcTest(TestCase):

    def default_setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0528(self):
        """仅语音模式——语音录制中途——点击右下角的发送按钮"""
        Preconditions.make_already_in_message_page()
        message_page = MessagePage()
        message_page.click_search_box()
        message_page.input_search_text('我的电脑')
        time.sleep(2)
        message_page.click_my_pc_button()
        # 我的电脑界面
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_pc_page_load()
        single_chat_page.set_send_voice_only()
        single_chat_page.click_voice_button()
        single_chat_page.click_send_voice()
        single_chat_page.click_back()
        time.sleep(1)
        single_chat_page.click_back()
        message_page.wait_for_page_load()
        self.assertEquals(message_page.is_first_message_content('语音'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0531(self):
        """仅语音模式——发送录制的语音消息"""
        Preconditions.make_already_in_message_page()
        message_page = MessagePage()
        message_page.click_search_box()
        message_page.input_search_text('我的电脑')
        time.sleep(2)
        message_page.click_my_pc_button()
        # 我的电脑界面
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_pc_page_load()
        single_chat_page.set_send_voice_only()
        single_chat_page.click_voice_button()
        time.sleep(8)
        single_chat_page.click_send_voice()
        single_chat_page.click_back()
        time.sleep(1)
        single_chat_page.click_back()
        message_page.wait_for_page_load()
        self.assertEquals(message_page.is_first_message_content('语音'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0532(self):
        """我的电脑会话页面——放大发送一段表情文本内容"""
        Preconditions.make_already_in_message_page()
        message_page = MessagePage()
        message_page.click_search_box()
        message_page.input_search_text('我的电脑')
        time.sleep(2)
        message_page.click_my_pc_button()
        # 我的电脑界面
        group_chat_page = GroupChatPage()
        time.sleep(2)
        # 点击输入框点击表情按钮点击微笑表情并发送
        group_chat_page.get_input_box()
        group_chat_page.click_expression_button()
        group_chat_page.click_expression_wx()
        group_chat_page.click_send_button()
        # 发送两次 第一次消息截取不到 发送窃喜表情
        group_chat_page.click_expression_qx()
        group_chat_page.click_expression_qx()
        group_chat_page.click_send_button()
        # 获取文本框大小1
        w1 = group_chat_page.get_width_of_last_msg()
        h1 = group_chat_page.get_height_of_last_msg()
        # 输入流鼻涕表情点击发送并向上滑动放大表情并发送
        group_chat_page.click_expression_lbt()
        group_chat_page.click_send_slide_up()
        # 获取文本大小2
        w2 = group_chat_page.get_width_of_last_msg()
        h2 = group_chat_page.get_height_of_last_msg()
        # 比较文本框大小 文本框1>文本框2
        self.assertEquals(int(w1) < int(w2), True)
        self.assertEquals(int(h1) < int(h2), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0533(self):
        """我的电脑聊天会话页面——缩小发送一段表情文本内容"""
        # 进入我的电脑
        Preconditions.make_already_in_message_page()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_search_box()
        message_page.input_search_text('我的电脑')
        time.sleep(2)
        message_page.click_my_pc_button()
        group_chat_page = GroupChatPage()
        time.sleep(2)
        # 点击输入框点击表情按钮点击微笑表情并发送
        group_chat_page.get_input_box()
        group_chat_page.click_expression_button()
        group_chat_page.click_expression_wx()
        group_chat_page.click_send_button()
        # 发送两次 第一次消息截取不到 发送窃喜表情
        group_chat_page.click_expression_qx()
        group_chat_page.click_send_button()
        # 获取文本框大小1
        w1 = group_chat_page.get_width_of_last_msg()
        h1 = group_chat_page.get_height_of_last_msg()
        # 输入流鼻涕表情点击发送并向下滑动缩小表情并发送
        group_chat_page.click_expression_lbt()
        group_chat_page.click_send_slide_down()
        # 获取文本大小2
        w2 = group_chat_page.get_width_of_last_msg()
        h2 = group_chat_page.get_height_of_last_msg()
        # 比较文本框大小 文本框1>文本框2
        self.assertEquals(int(w1) > int(w2), True)
        self.assertEquals(int(h1) > int(h2), True)

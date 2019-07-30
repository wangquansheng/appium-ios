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
    def test_msg_weifenglian_PC_0253(self):
        """验证在我的电脑会话窗口点击打开已下载的可预览文件时，右上角是否新增更多功能入口"""
        Preconditions.make_already_in_message_page()
        message_page = MessagePage()
        message_page.click_search_box()
        message_page.input_search_text('我的电脑')
        time.sleep(2)
        message_page.click_my_pc_button()
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_pc_page_load()
        single_chat_page.click_file_button()
        single_chat_page.click_name_attribute_by_name('我收到的文件')
        single_chat_page.click_name_attribute_by_name('录制')
        single_chat_page.click_accessibility_id_attribute_by_name('发送')
        # single_chat_page.click_name_attribute_by_name('录制')
        single_chat_page.click_file_by_type("录制.txt")
        self.assertEquals(single_chat_page.is_preview_more_exist(), True)
        self.assertEquals(single_chat_page.page_should_contain_text2('录制.txt'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_weifenglian_PC_0254(self):
        """验证在我的电脑会话窗口点击打开已下载的可预览文件时，点击右上角的更多按钮是否正常调起选项"""
        Preconditions.make_already_in_message_page()
        message_page = MessagePage()
        message_page.click_search_box()
        message_page.input_search_text('我的电脑')
        time.sleep(2)
        message_page.click_my_pc_button()
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_pc_page_load()
        single_chat_page.click_file_button()
        single_chat_page.click_name_attribute_by_name('我收到的文件')
        single_chat_page.click_name_attribute_by_name('录制')
        single_chat_page.click_accessibility_id_attribute_by_name('发送')
        # single_chat_page.click_name_attribute_by_name('录制')
        single_chat_page.wait_for_pc_page_load()
        single_chat_page.click_file_by_type("录制.txt")
        single_chat_page.click_preview_more_button()
        # 判断是否存在转发收藏其他应用打开取消按钮
        self.assertEquals(single_chat_page.is_forward_exist(), True)
        self.assertEquals(single_chat_page.is_collection_exist(), True)
        self.assertEquals(single_chat_page.is_other_app_exist(), True)
        self.assertEquals(single_chat_page.is_cancel_exist(), True)
        time.sleep(2)

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










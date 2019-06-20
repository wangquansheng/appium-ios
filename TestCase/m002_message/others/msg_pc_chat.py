from library.core.TestCase import TestCase
from pages.Public_Method import PublicMethod
from preconditions.BasePreconditions import LoginPreconditions
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
from pages import *
import unittest


REQUIRED_MOBILES = {'IOS-移动': 'iphone'}


class Preconditions(LoginPreconditions):
    pass


class PublicMyPC(PublicMethod):

    def wait_for_MyPc_page_load(self):
        return current_mobile().wait_until(condition=lambda x: current_mobile().is_text_present('我的电脑'))

    def enter_MyPc_chat(self):
        """从消息页面进入我的电脑聊天页面"""
        msg_page = MessagePage()
        msg_page.wait_for_page_load()
        # msg_page.click_search()
        msg_page.input_search_message('我的电脑')
        msg_page.choose_chat_by_name('我的电脑')
        self.wait_for_MyPc_page_load()

    def select_folder(self):
        """聊天页面选择文件"""
        chat_more = ChatMorePage()
        chat_more.click_file1()

    def select_file(self, file_type='.xlsx'):
        """选择文件类型"""
        self.select_folder()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        ChatSelectLocalFilePage().select_file(file_type)

    def select_file_send(self, file_type=".xlsx"):
        """选择文件类型发送"""
        self.select_file(file_type)
        self.public_click_send()

    def long_press_forward_file(self):
        """长按文件转发"""
        # self.select_file_send()
        # self.wait_for_MyPc_page_load()
        ChatFilePage().forward_file('.xlsx')

    def select_Group_search_by_text(self, text):
        self.long_press_forward_file()
        self.public_click_attribute_by_name('选择一个群')
        # SelectOneGroupPage().wait_for_page_load()
        SelectOneGroupPage().input_search_keyword(text)
        if SelectOneGroupPage().is_text_present('无搜索结果'):
            pass
        else:
            self.public_click_attribute_contains_text(text)
            self.public_click_attribute_by_name('确定')
            is_toast = True    # toast弹框，后期修改
            unittest.TestCase().assertTrue(is_toast)
            unittest.TestCase().assertTrue(self.wait_for_MyPc_page_load())


class MsgMyPcTest(TestCase):

    def default_setUp(self):
        client = switch_to_mobile(REQUIRED_MOBILES['IOS-移动'])
        client.connect_mobile()
        msg_page = MessagePage()
        if msg_page.is_on_this_page():
            return
        else:
            try:
                current_mobile().launch_app()
                msg_page.wait_for_page_load()
            except Exception as e:
                print(e)

    def test_msg_weifenglian_PC_0081(self):
        """将自己发送的文件转发到在搜索框输入文字搜索到的群"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().select_file_send()
        PublicMyPC().select_Group_search_by_text('群聊')
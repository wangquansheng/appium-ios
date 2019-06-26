from library.core.utils.applicationcache import current_mobile, switch_to_mobile
from library.core.TestCase import TestCase

from pages.MyPcPage import PublicMyPC
from pages import *
import time

REQUIRED_MOBILES = {'IOS-移动': 'iphone'}


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

    def test_msg_weifenglian_PC_0074(self):
        """在我的电脑将自己发送的文件转发到当前会话窗口"""
        my_pc_chat = PublicMyPC()
        # 1,确保电脑有文件消息
        my_pc_chat.enter_MyPc_chat()
        my_pc_chat.make_sure_have_file_message()
        # 2,长按并转发
        my_pc_chat.long_press_forward_file()
        my_pc_chat.public_click_attribute_by_name('我的电脑')
        my_pc_chat.public_click_sure()
        my_pc_chat.check_forward_toast_back_PC_chat_page()

    def test_msg_weifenglian_PC_0075(self):
        """将自己发送的文件转发到普通群"""
        my_pc_chat = PublicMyPC()
        # 1,确保电脑有文件消息
        my_pc_chat.enter_MyPc_chat()
        my_pc_chat.make_sure_have_file_message()
        # 2,长按并转发
        my_pc_chat.long_press_forward_file()
        # 3,选择一个群
        my_pc_chat.public_click_attribute_by_name('选择一个群')
        # 4,选择任意群
        my_pc_chat.public_click_attribute_contains_text('name', 'test')
        my_pc_chat.public_click_sure()
        my_pc_chat.check_forward_toast_back_PC_chat_page()

    def test_msg_weifenglian_PC_0076(self):
        """将自己发送的文件转发到企业群"""
        my_pc_chat = PublicMyPC()
        # 1,确保电脑有文件消息
        my_pc_chat.enter_MyPc_chat()
        my_pc_chat.make_sure_have_file_message()
        # 2,长按并转发
        my_pc_chat.long_press_forward_file()
        # 3,选择一个群
        my_pc_chat.public_click_attribute_by_name('选择一个群')
        # 4,选择任意企业群
        my_pc_chat.public_click_attribute_by_name('name', 'cc_chat_company')
        my_pc_chat.public_click_sure()
        my_pc_chat.check_forward_toast_back_PC_chat_page()

    def test_msg_weifenglian_PC_0079(self):
        """将自己发送的文件转发到普通群时点击取消转发"""
        my_pc_chat = PublicMyPC()
        # 1,确保电脑有文件消息
        my_pc_chat.enter_MyPc_chat()
        my_pc_chat.make_sure_have_file_message()
        # 2,长按并转发
        my_pc_chat.long_press_forward_file()
        # 3,选择一个群
        my_pc_chat.public_click_attribute_by_name('选择一个群')
        # 4,选择任意群
        my_pc_chat.public_click_attribute_contains_text('name', 'test')
        my_pc_chat.public_click_cancel()
        if my_pc_chat.driver.find_element_by_ios_predicate("name == '选择一个群'"):
            print('当前页面在选择一个群页面')

    def test_msg_weifenglian_PC_0080(self):
        """将自己发送的文件转发到企业群时点击取消转发"""
        my_pc_chat = PublicMyPC()
        # 1,确保电脑有文件消息
        my_pc_chat.enter_MyPc_chat()
        my_pc_chat.make_sure_have_file_message()
        # 2,长按并转发
        my_pc_chat.long_press_forward_file()
        # 3,选择一个群
        my_pc_chat.public_click_attribute_by_name('选择一个群')
        # 4,选择任意群
        my_pc_chat.public_click_attribute_contains_text('name', 'cc_chat_company')
        my_pc_chat.public_click_cancel()
        if my_pc_chat.driver.find_element_by_ios_predicate("name == '选择一个群'"):
            print('当前页面在选择一个群页面')

    def test_msg_weifenglian_PC_0081(self):
        """将自己发送的文件转发到在搜索框输入文字搜索到的群"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().select_Group_search_by_text('群聊')

    def test_msg_weifenglian_PC_0082(self):
        """将自己发送的文件转发到在搜索框输入英文字母搜索到的群"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().select_Group_search_by_text('test')

    def test_msg_weifenglian_PC_0083(self):
        """将自己发送的文件转发到在搜索框输入数字搜索到的群"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().select_Group_search_by_text('2345')

    def test_msg_weifenglian_PC_0084(self):
        """将自己发送的文件转发到在搜索框输入标点符号搜索到的群"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().select_Group_search_by_text('.;,')

    def test_msg_weifenglian_PC_0085(self):
        """将自己发送的文件转发到在搜索框输入特殊字符搜索到的群"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().select_Group_search_by_text('αβγ')

    def test_msg_weifenglian_PC_0086(self):
        """将自己发送的文件转发到在搜索框输入空格搜索到的群"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().select_Group_search_by_text('  ')

    def test_msg_weifenglian_PC_0087(self):
        """将自己发送的文件转发到在搜索框输入多种字符搜索到的群"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().select_Group_search_by_text('int123')

    def test_msg_weifenglian_PC_0088(self):
        """将自己发送的文件转发到在搜索框输入多种字符搜索到的群"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().select_Group_search_by_text('float0.123')

    def test_msg_weifenglian_PC_0090(self):
        """将自己发送的文件转发到搜索到的群时点击取消转发"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().public_click_attribute_by_name('选择一个群')
        SelectOneGroupPage().input_search_keyword('test')
        if SelectOneGroupPage().is_text_present('无搜索结果'):
            pass
        else:
            PublicMyPC().public_click_attribute_contains_text('name', 'test')
            PublicMyPC().public_click_cancel()
            self.assertTrue(PublicMyPC().public_is_on_this_page_by_element_attribute('搜索群组'))

    def test_msg_weifenglian_PC_0092(self):
        """将自己发送的文件转发到手机联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_contacts_type('选择手机联系人')
        time.sleep(2)
        PublicMyPC().public_find_elements_by_PREDICATE('type', '==', 'XCUIElementTypeCell', index=0).click()
        PublicMyPC().public_click_sure()
        PublicMyPC().check_forward_toast_back_PC_chat_page()

    def test_msg_weifenglian_PC_0093(self):
        """将自己发送的文件转发到手机联系人时点击取消转发"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_contacts_type('选择手机联系人')
        time.sleep(2)
        PublicMyPC().public_find_elements_by_PREDICATE('type', '==', 'XCUIElementTypeCell', index=0).click()
        PublicMyPC().public_click_cancel()
        self.assertTrue(PublicMyPC().public_is_on_this_page_by_element_attribute('选择联系人'))

    def test_msg_weifenglian_PC_0095(self):
        """将自己发送的文件转发到在搜索框输入多种字符搜索到的手机联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_PhoneContact_search_by_text('给个红包1')

    def test_msg_weifenglian_PC_0096(self):
        """将自己发送的文件转发到在搜索框输入数字搜索到的手机联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_PhoneContact_search_by_text('23579')

    def test_msg_weifenglian_PC_0097(self):
        """将自己发送的文件转发到在搜索框输入标点符号搜索到的手机联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_PhoneContact_search_by_text('.;,')

    def test_msg_weifenglian_PC_0098(self):
        """将自己发送的文件转发到在搜索框输入字母搜索到的手机联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_PhoneContact_search_by_text('test')

    def test_msg_weifenglian_PC_0099(self):
        """将自己发送的文件转发到在搜索框输入字母搜索到的手机联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_PhoneContact_search_by_text('   ')

    def test_msg_weifenglian_PC_0101(self):
        """将自己发送的文件转发到在搜索框输入号码搜索到的手机联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_PhoneContact_search_by_text('13800138005')

    def test_msg_weifenglian_PC_0102(self):
        """将自己发送的文件转发到在搜索框输入号码搜索到的手机联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_PhoneContact_search_by_text('13800138005', send_button='取消')

    def test_msg_weifenglian_PC_0109(self):
        """将自己发送的文件转发到在企业列表搜索框输入多种字符搜索到的团队联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_TeamListContacts_search_by_text('float0.123')

    def test_msg_weifenglian_PC_0110(self):
        """将自己发送的文件转发到在企业内搜索框输入多种字符搜索到的团队联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_TeamSingleContacts_search_by_text('float0.123')

    def test_msg_weifenglian_PC_0111(self):
        """将自己发送的文件转发到在企业列表搜索框输入数字搜索到的团队联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_TeamListContacts_search_by_text('13800138005')
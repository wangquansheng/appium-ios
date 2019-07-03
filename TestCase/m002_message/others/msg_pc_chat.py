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
        PublicMyPC().select_TeamListContacts_search_by_text('2468')

    def test_msg_weifenglian_PC_0112(self):
        """将自己发送的文件转发到在企业内搜索框输入数字搜索到的团队联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_TeamSingleContacts_search_by_text('2468')

    def test_msg_weifenglian_PC_0113(self):
        """将自己发送的文件转发到在企业列表搜索框输入标点符号搜索到的团队联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_TeamListContacts_search_by_text('.;,')

    def test_msg_weifenglian_PC_0114(self):
        """将自己发送的文件转发到在企业内搜索框输入标点符号搜索到的团队联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_TeamSingleContacts_search_by_text('.;,')

    def test_msg_weifenglian_PC_0115(self):
        """将自己发送的文件转发到在企业列表搜索框输入字母搜索到的团队联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_TeamListContacts_search_by_text('test')

    def test_msg_weifenglian_PC_0116(self):
        """将自己发送的文件转发到在企业内搜索框输入字母搜索到的团队联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_TeamSingleContacts_search_by_text('test')

    def test_msg_weifenglian_PC_0117(self):
        """将自己发送的文件转发到在企业列表搜索框输入空格搜索到的团队联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_TeamListContacts_search_by_text('   ')

    def test_msg_weifenglian_PC_0118(self):
        """将自己发送的文件转发到在企业内搜索框输入空格搜索到的团队联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_TeamSingleContacts_search_by_text('   ')

    def test_msg_weifenglian_PC_0121(self):
        """将自己发送的文件转发到在企业列表搜索框输入号码搜索到的团队联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_TeamListContacts_search_by_text('13800138005')

    def test_msg_weifenglian_PC_0122(self):
        """将自己发送的文件转发到在企业内搜索框输入号码搜索到的团队联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_TeamSingleContacts_search_by_text('13800138005')

    def test_msg_weifenglian_PC_0123(self):
        """将自己发送的文件转发到在企业列表搜索框输入号码搜索到的团队联系人"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_TeamListContacts_search_by_text('13', send_button='取消')

    def test_msg_weifenglian_PC_0124(self):
        """将自己发送的文件转发到在企业内搜索框进行搜索到的团队联系人时取消转发"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().select_TeamSingleContacts_search_by_text('13', send_button='取消')

    def test_msg_weifenglian_PC_0125(self):
        """将自己发送的文件转发到我的电脑"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().input_text(('-ios predicate string', 'value == "搜索或输入手机号"'), '我的电脑')
        PublicMyPC().public_click_attribute_by_name('我的电脑')
        PublicMyPC().public_click_sure()
        PublicMyPC().check_forward_toast_back_PC_chat_page()

    def test_msg_weifenglian_PC_0126(self):
        """将自己发送的文件转发到最近聊天"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().public_click_attribute_by_name('我的电脑')
        PublicMyPC().public_click_sure()
        PublicMyPC().check_forward_toast_back_PC_chat_page()

    def test_msg_weifenglian_PC_0127(self):
        """将自己发送的文件转发到最近聊天时点击取消转发"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_forward_file()
        PublicMyPC().public_click_attribute_by_name('我的电脑')
        PublicMyPC().public_click_cancel()
        self.assertTrue(PublicMyPC().public_is_on_this_page_by_element_attribute('选择联系人'))

    def test_msg_weifenglian_PC_0129(self):
        """对自己发送出去的文件消息进行删除"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_file('.xlsx')
        PublicMyPC().public_click_attribute_by_name('删除')
        PublicMyPC().public_click_sure()

    def test_msg_weifenglian_PC_0131(self):
        """对自己发送出去的文件消息进行收藏"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().long_press_file('.xlsx')
        PublicMyPC().public_click_attribute_by_name('收藏')
        current_mobile().launch_app()
        time.sleep(1)
        PublicMyPC().enter_collect_page()
        if PublicMyPC().public_find_element_by_PREDICATE('name', 'CONTAINS', 'xlsx'):
            print('当前收藏页面有文件')

    def test_msg_weifenglian_PC_0302(self):
        """验证在我的电脑会话窗口点击打开已下载的可预览文件时，右上角是否新增更多功能入口"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().set_network_status(0)
        el = PublicMyPC().get_elements(('-ios predicate string', 'name ENDSWITH ".xlsx"'))
        el[-1].click()
        if PublicMyPC().public_find_element_by_PREDICATE('name', '==', 'cc chat file more normal'):
            print('存在更多按钮')

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0302():
        PublicMyPC().set_network_status(6)

    def test_msg_weifenglian_PC_0303(self):
        """验证在我的电脑会话窗口点击打开已下载的可预览文件时，点击右上角的更多按钮是否正常调起选项"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().set_network_status(0)
        el = PublicMyPC().get_elements(('-ios predicate string', 'name ENDSWITH ".xlsx"'))
        el[-1].click()
        PublicMyPC().public_click_attribute_by_name('cc chat file more normal')
        button_list = ['转发', '收藏', '其他应用打开', '取消']
        for button in button_list:
            self.assertTrue(PublicMyPC().is_text_present(button))

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0303():
        PublicMyPC().set_network_status(6)

    def test_msg_weifenglian_PC_0304(self):
        """验证在我的电脑会话窗口点击打开已下载的可预览文件-右上角的更多按钮-转发-返回时页面是否正常"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().set_network_status(0)
        el = PublicMyPC().get_elements(('-ios predicate string', 'name ENDSWITH ".xlsx"'))
        el[-1].click()
        PublicMyPC().public_click_attribute_by_name('cc chat file more normal')
        PublicMyPC().public_click_attribute_by_name('转发')
        PublicMyPC().public_click_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0304():
        PublicMyPC().set_network_status(6)

    def test_msg_weifenglian_PC_0306(self):
        """验证在我的电脑会话窗口点击打开已下载的可预览文件-右上角的更多按钮-收藏时是否正常"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().set_network_status(0)
        el = PublicMyPC().get_elements(('-ios predicate string', 'name ENDSWITH ".xlsx"'))
        el[-1].click()
        PublicMyPC().public_click_attribute_by_name('cc chat file more normal')
        PublicMyPC().public_click_attribute_by_name('收藏')
        PublicMyPC().public_click_back()
        PublicMyPC().public_click_back()
        PublicMyPC().public_click_back()
        PublicMyPC().enter_collect_page()
        if PublicMyPC().public_find_element_by_PREDICATE('name', 'CONTAINS', 'xlsx'):
            print('当前收藏页面有文件')

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0306():
        PublicMyPC().set_network_status(6)

    def test_msg_weifenglian_PC_0307(self):
        """验证在我的电脑会话窗口点击打开已下载的可预览文件-右上角的更多按钮-其他应用打开时是否正常"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().set_network_status(0)
        el = PublicMyPC().get_elements(('-ios predicate string', 'name ENDSWITH ".xlsx"'))
        el[-1].click()
        PublicMyPC().public_click_attribute_by_name('cc chat file more normal')
        PublicMyPC().public_click_attribute_by_name('其他应用打开')
        self.assertTrue(PublicMyPC().public_is_on_this_page_by_element_attribute('拷贝'))

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0307():
        PublicMyPC().set_network_status(6)

    def test_msg_weifenglian_PC_0308(self):
        """验证在我的电脑会话窗口点击打开已下载的可预览文件-右上角的更多按钮-其他应用打开时是否正常"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().set_network_status(0)
        el = PublicMyPC().get_elements(('-ios predicate string', 'name ENDSWITH ".xlsx"'))
        el[-1].click()
        PublicMyPC().public_click_attribute_by_name('cc chat file more normal')
        PublicMyPC().public_click_attribute_by_name('取消')
        self.assertTrue(PublicMyPC().public_is_on_this_page_by_element_attribute('cc chat file more normal'))

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0308():
        PublicMyPC().set_network_status(6)

    def test_msg_weifenglian_PC_0309(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件时，标题显示是否正常"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().set_network_status(0)
        PublicMyPC().enter_find_file_page()
        self.assertTrue(PublicMyPC().public_is_on_this_page_by_element_attribute('测试用例.xlsx'))

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0309():
        PublicMyPC().set_network_status(6)

    def test_msg_weifenglian_PC_0310(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件时，右上角是否新增更多功能入口"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().set_network_status(0)
        PublicMyPC().enter_find_file_page()
        self.assertTrue(PublicMyPC().public_is_on_this_page_by_element_attribute('cc chat file more normal'))

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0310():
        PublicMyPC().set_network_status(6)

    def test_msg_weifenglian_PC_0311(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件时，点击右上角的更多按钮是否正常调起选项"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().set_network_status(0)
        PublicMyPC().enter_find_file_page()
        PublicMyPC().public_click_attribute_by_name('cc chat file more normal')
        button_list = ['转发', '收藏', '其他应用打开', '取消']
        for button in button_list:
            self.assertTrue(PublicMyPC().is_text_present(button))

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0311():
        PublicMyPC().set_network_status(6)

    def test_msg_weifenglian_PC_0312(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-转发-返回时页面是否正常"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().set_network_status(0)
        PublicMyPC().enter_find_file_page()
        PublicMyPC().public_click_attribute_by_name('cc chat file more normal')
        PublicMyPC().public_click_attribute_by_name('转发')
        PublicMyPC().public_click_back()
        self.assertTrue(PublicMyPC().public_is_on_this_page_by_element_attribute('cc chat file more normal'))

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0312():
        PublicMyPC().set_network_status(6)

    def test_msg_weifenglian_PC_0314(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-收藏时是否正常"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().set_network_status(0)
        PublicMyPC().enter_find_file_page()
        PublicMyPC().public_click_attribute_by_name('cc chat file more normal')
        PublicMyPC().public_click_attribute_by_name('收藏')
        PublicMyPC().is_toast_exist('已收藏')
        current_mobile().launch_app()
        PublicMyPC().enter_collect_page()
        if PublicMyPC().public_find_element_by_PREDICATE('name', 'CONTAINS', 'xlsx'):
            print('当前收藏页面有文件')

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0314():
        PublicMyPC().set_network_status(6)

    def test_msg_weifenglian_PC_0315(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-其他应用打开时是否正常"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().set_network_status(0)
        PublicMyPC().enter_find_file_page()
        PublicMyPC().public_click_attribute_by_name('cc chat file more normal')
        PublicMyPC().public_click_attribute_by_name('其他应用打开')
        self.assertTrue(PublicMyPC().public_is_on_this_page_by_element_attribute('拷贝'))

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0315():
        PublicMyPC().set_network_status(6)

    def test_msg_weifenglian_PC_0316(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-取消时是否正常"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message()
        PublicMyPC().set_network_status(0)
        PublicMyPC().enter_find_file_page()
        PublicMyPC().public_click_attribute_by_name('cc chat file more normal')
        PublicMyPC().public_click_attribute_by_name('取消')
        self.assertTrue(PublicMyPC().public_is_on_this_page_by_element_attribute('cc chat file more normal'))

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0316():
        PublicMyPC().set_network_status(6)

    def test_msg_weifenglian_PC_0317(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的不可预览文件时，页面显示是否正常"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message(file_type='.c')
        PublicMyPC().set_network_status(0)
        PublicMyPC().enter_find_file_page(file_type='.c')
        element_list = ['cc chat file more normal', '打开']
        for element in element_list:
            self.assertTrue(PublicMyPC().public_is_on_this_page_by_element_attribute(element))
        PublicMyPC().public_click_attribute_by_name('打开')
        self.assertTrue(PublicMyPC().public_is_on_this_page_by_element_attribute('拷贝'))

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0317():
        PublicMyPC().set_network_status(6)

    def test_msg_weifenglian_PC_0318(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的不可预览文件时，点击右上角的更多按钮是否正常调起选项"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message(file_type='.c')
        PublicMyPC().set_network_status(0)
        PublicMyPC().enter_find_file_page(file_type='.c')
        PublicMyPC().public_click_attribute_by_name('cc chat file more normal')
        button_list = ['转发', '收藏', '取消']
        for button in button_list:
            self.assertTrue(PublicMyPC().is_text_present(button))

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0318():
        PublicMyPC().set_network_status(6)

    def test_msg_weifenglian_PC_0319(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的不可预览文件-右上角的更多按钮-转发-返回时页面是否正常"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message(file_type='.c')
        PublicMyPC().set_network_status(0)
        PublicMyPC().enter_find_file_page(file_type='.c')
        PublicMyPC().public_click_attribute_by_name('cc chat file more normal')
        PublicMyPC().public_click_attribute_by_name('转发')
        PublicMyPC().public_click_back()
        self.assertTrue(PublicMyPC().public_is_on_this_page_by_element_attribute('cc chat file more normal'))

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0319():
        PublicMyPC().set_network_status(6)

    def test_msg_weifenglian_PC_0320(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的不可预览文件-右上角的更多按钮-转发时是否正常"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message(file_type='.c')
        PublicMyPC().set_network_status(0)
        PublicMyPC().enter_find_file_page(file_type='.c')
        PublicMyPC().public_click_attribute_by_name('cc chat file more normal')
        PublicMyPC().public_click_attribute_by_name('转发')
        PublicMyPC().public_click_attribute_by_name('我的电脑')
        PublicMyPC().public_click_sure()
        self.assertTrue(PublicMyPC().public_is_on_this_page_by_element_attribute('cc chat file more normal'))
        self.assertTrue(PublicMyPC().is_toast_exist('已转发'))
        current_mobile().launch_app()
        self.assertTrue(PublicMyPC().public_is_on_this_page_by_element_attribute('!'))

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0320():
        PublicMyPC().set_network_status(6)

    def test_msg_weifenglian_PC_0321(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的不可预览文件-右上角的更多按钮-收藏时是否正常"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message(file_type='.c')
        PublicMyPC().set_network_status(0)
        PublicMyPC().enter_find_file_page(file_type='.c')
        PublicMyPC().public_click_attribute_by_name('cc chat file more normal')
        PublicMyPC().public_click_attribute_by_name('收藏')
        PublicMyPC().is_toast_exist('已收藏')
        current_mobile().launch_app()
        PublicMyPC().enter_collect_page()
        if PublicMyPC().public_find_element_by_PREDICATE('name', 'CONTAINS', '.c'):
            print('当前收藏页面有文件')

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0321():
        PublicMyPC().set_network_status(6)

    def test_msg_weifenglian_PC_0322(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的不可预览文件-右上角的更多按钮-取消时是否正常"""
        PublicMyPC().enter_MyPc_chat()
        PublicMyPC().make_sure_have_file_message(file_type='.c')
        PublicMyPC().set_network_status(0)
        PublicMyPC().enter_find_file_page(file_type='.c')
        PublicMyPC().public_click_attribute_by_name('cc chat file more normal')
        PublicMyPC().public_click_attribute_by_name('取消')
        self.assertTrue(PublicMyPC().public_is_on_this_page_by_element_attribute('cc chat file more normal'))

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0322():
        PublicMyPC().set_network_status(6)
from pages.Public_Method import PublicMethod

from library.core.utils.applicationcache import current_mobile
from library.core.TestLogger import TestLogger

from unittest import TestCase
from pages import *
import time


class PublicMyPC(PublicMethod):

    @TestLogger.log("等待我的电脑页面加载")
    def wait_for_MyPc_page_load(self):
        return current_mobile().wait_until(condition=lambda x: current_mobile().is_text_present('我的电脑'))

    @TestLogger.log("从消息页面进入我的电脑聊天页面")
    def enter_MyPc_chat(self):
        msg_page = MessagePage()
        msg_page.wait_for_page_load()
        # msg_page.click_search()
        msg_page.input_search_message('我的电脑')
        time.sleep(2)
        msg_page.choose_chat_by_name('我的电脑')
        self.wait_for_MyPc_page_load()

    @TestLogger.log("聊天页面选择文件")
    def select_folder(self):
        chat_more = ChatMorePage()
        chat_more.click_file1()

    @TestLogger.log("选择文件类型")
    def select_file(self, file_type='.xlsx'):
        self.select_folder()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        ChatSelectLocalFilePage().select_file(file_type)

    @TestLogger.log("选择文件类型发送")
    def select_file_send(self, file_type=".xlsx"):
        self.select_file(file_type)
        self.public_click_send()
        time.sleep(2)

    @TestLogger.log("长按文件转发")
    def long_press_forward_file(self):
        ChatFilePage().forward_file('.xlsx')

    @TestLogger.log("选择一个群通过text选择发送消息")
    def select_Group_search_by_text(self, text, send_button='确定'):
        self.long_press_forward_file()
        self.public_click_attribute_by_name('选择一个群')
        SelectOneGroupPage().input_search_keyword(text)
        if SelectOneGroupPage().is_text_present('无搜索结果'):
            pass
        else:
            self.public_click_attribute_contains_text('name', text)
            self.public_click_attribute_by_name(send_button)

    @TestLogger.log("选择手机联系人通过text选择发送消息")
    def select_PhoneContact_search_by_text(self, text, send_button='确定'):
        self.public_click_attribute_by_name('选择手机联系人')
        time.sleep(2)
        self.input_text(('-ios predicate string', 'type == "XCUIElementTypeTextField"'), text)
        if SelectOneGroupPage().is_text_present('无搜索结果'):
            pass
        else:
            self.public_find_elements_by_PREDICATE('type', '==', 'XCUIElementTypeCell', 0).click()
            self.public_click_attribute_by_name(send_button)
            if send_button == '确定':
                self.check_forward_toast_back_PC_chat_page()
            elif send_button == '取消':
                TestCase().assertTrue(self.public_is_on_this_page_by_element_attribute('选择联系人'))

    @TestLogger.log("选择团队联系人通过text选择发送消息")
    def select_TeamListContacts_search_by_text(self, text, send_button='确定'):
        self.public_click_attribute_by_name('选择团队联系人')
        time.sleep(2)
        self.input_text(('-ios predicate string', 'type == "XCUIElementTypeTextField"'), text)
        if SelectOneGroupPage().is_text_present('无搜索结果'):
            pass
        else:
            # self.public_find_elements_by_PREDICATE('type', '==', 'XCUIElementTypeCell', 0).click()
            self.public_click_element_by_PREDICATE('name', 'CONTAINS', text)
            self.public_click_attribute_by_name(send_button)
            if send_button == '确定':
                self.check_forward_toast_back_PC_chat_page()
            elif send_button == '取消':
                TestCase().assertTrue(self.public_is_on_this_page_by_element_attribute('选择联系人'))

    @TestLogger.log("选择团队联系人通过text选择发送消息")
    def select_TeamSingleContacts_search_by_text(self, text, send_button='确定'):
        self.public_click_attribute_by_name('选择团队联系人')
        # 选择团队联系人。默认选择第一个团队。
        time.sleep(2)
        self.public_find_elements_by_PREDICATE('type', '==', 'XCUIElementTypeCell', index=0).click()
        time.sleep(2)
        self.input_text(('-ios predicate string', 'type == "XCUIElementTypeTextField"'), text)
        if SelectOneGroupPage().is_text_present('无搜索结果'):
            pass
        else:
            self.click_element(('xpath', '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeTable/XCUIElementTypeCell[1]'))
            self.public_click_attribute_by_name(send_button)
            if send_button == '确定':
                self.check_forward_toast_back_PC_chat_page()
            elif send_button == '取消':
                TestCase().assertTrue(self.public_is_on_this_page_by_element_attribute('选择联系人'))

    @TestLogger.log("选择联系人页面")
    def select_contacts_type(self, type):
        """在选择联系人页面选择"""
        if type == '搜索或输入手机号':
            self.public_click_attribute_by_value('搜索或输入手机号')
        else:
            self.public_click_attribute_by_name(type)

    @TestLogger.log("确保此页面有消息聊天记录")
    def make_sure_have_file_message(self, file_type='.xlsx'):
        if self.public_find_element_by_attribute_endswith(file_type):
            pass
        else:
            self.select_file_send()

    @TestLogger.log("检测已转发toast和返回我的电脑聊天页面")
    def check_forward_toast_back_PC_chat_page(self):
        TestCase().assertTrue(self.is_toast_exist('已转发'))
        TestCase().assertTrue(self.wait_for_MyPc_page_load())

    @TestLogger.log("长按文件")
    def long_press_file(self, file):
        time.sleep(3)
        el = self.get_elements(('-ios predicate string', 'name ENDSWITH "%s"' % file))
        el = el[-1]
        # self.press(el)
        from appium.webdriver.common.touch_action import TouchAction
        TouchAction(self.driver).long_press(el, duration=3000).release().perform()

    @TestLogger.log("进入收藏页面")
    def enter_collect_page(self):
        self.public_click_attribute_by_name('我')
        self.public_click_attribute_by_name('收藏')

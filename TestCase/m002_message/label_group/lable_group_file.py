

import unittest
import time
import warnings
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from preconditions.BasePreconditions import LoginPreconditions
from library.core.utils.testcasefilter import tags
from pages.chat.chatfileProview import ChatfileProviewPage


from pages import *
from selenium.common.exceptions import TimeoutException


from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile


REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    # 'Android-移动': 'single_mobile',
    'IOS-移动': 'iphone',
    'IOS-移动-移动': 'M960BDQN229CHiphone8',
}


class Preconditions(LoginPreconditions):
    """
    分解前置条件
    """
    @staticmethod
    def connect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

    @staticmethod
    def disconnect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(category)
        client.disconnect_mobile()
        return client


    @staticmethod
    def create_contacts(name, number):
        """
        导入联系人数据
        :param name:
        :param number:
        :return:
        """
        contacts_page = ContactsPage()
        detail_page = ContactDetailsPage()
        try:
            contacts_page.wait_for_page_load()
            contacts_page.open_contacts_page()
        except:
            Preconditions.make_already_in_message_page(reset=False)
            contacts_page.open_contacts_page()
        # 创建联系人
        contacts_page.click_search_box()
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword(name)
        contact_search.click_back()
        contacts_page.click_add()
        create_page = CreateContactPage()
        create_page.hide_keyboard_if_display()
        create_page.create_contact(name, number)
        detail_page.wait_for_page_load()
        detail_page.click_back_icon()

    @staticmethod
    def take_logout_operation_if_already_login():
        """已登录状态，执行登出操作"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()

        me = MePage()
        me.scroll_to_bottom()
        me.scroll_to_bottom()
        me.scroll_to_bottom()
        me.click_setting_menu()

        setting = SettingPage()
        setting.scroll_to_bottom()
        setting.click_logout()
        setting.click_ok_of_alert()

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""
        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def terminate_app():
        """
        强制关闭app,退出后台
        :return:
        """
        app_id = current_driver().desired_capability['appPackage']
        current_mobile().termiate_app(app_id)

    @staticmethod
    def background_app():
        """后台运行"""
        current_mobile().press_home_key()

    @staticmethod
    def activate_app(app_id=None):
        """激活APP"""
        if not app_id:
            app_id = current_mobile().driver.desired_capabilities['appPackage']
        current_mobile().driver.activate_app(app_id)


    @staticmethod
    def make_sure_chatwindow_exist_file(type='.docx'):
        """确保我的电脑页面有文件记录"""
        chat=ChatWindowPage()
        time.sleep(2)
        if chat.is_element_present_file():
            chat.wait_for_page_load()
        else:
            chat.click_file()
            csf = ChatSelectFilePage()
            csf.wait_for_page_load()
            time.sleep(2)
            csf.click_local_file()
            time.sleep(2)
            local_file = ChatSelectLocalFilePage()
            # type='.docx'
            local_file.select_file(type)
            local_file.click_send_button()
            time.sleep(2)

    @staticmethod
    def send_file(type='.docx'):
        """聊天界面-发送文件（默认.docx文件）"""
        chat=ChatWindowPage()
        time.sleep(2)
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_local_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(type)
        local_file.click_send_button()
        time.sleep(2)




class LableGroupTest(TestCase):
    """标签分组---文件"""

    # @classmethod
    # def setUpClass(cls):
    #     warnings.simplefilter('ignore', ResourceWarning)
    #     Preconditions.make_already_in_message_page()
    #     MessagePage().open_contacts_page()
    #     contact = ContactsPage()
    #     contact.click_phone_contact()
    #     time.sleep(2)
    #     contact.click_label_grouping()
    #     LabelGroupingPage().delete_all_label()


    @classmethod
    def default_setUp(self):
        """确保每个用例执行前在标签分组会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        lable_group=LabelGroupingPage()
        lable_detail = LableGroupDetailPage()
        chat=ChatWindowPage()
        if chat.is_on_this_page():
            time.sleep(4)
        else:
            Preconditions.make_already_in_message_page()
            MessagePage().open_contacts_page()
            contact=ContactsPage()
            contact.click_phone_contact()
            time.sleep(2)
            contact.click_label_grouping()
            if lable_group.is_element_present(locator='已建分组列表1'):
                lable_group.click_first_lable_group()
            else:
                lable_group.creat_group('aaa')
                time.sleep(2)
                #为标签分组添加成员
                lable_group.click_first_lable_group()
                time.sleep(2)
                lable_detail.click_add_contact()
                local_contact = SelectLocalContactsPage()
                local_contact.swipe_select_one_member_by_name('大佬1')
                local_contact.swipe_select_one_member_by_name('大佬2')
                local_contact.click_sure_icon()
            time.sleep(2)
            lable_detail.click_send_group_info()
            time.sleep(3)


    def default_tearDown(self):
        # ChatWindowPage().delete_file()

        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_fenzu_0001(self):
        """勾选本地文件内任意文件点击发送按钮"""
        #勾选本地文件 发送
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_file()
        #1,调转到选择文件页面-选择本地文件
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        self.assertTrue(csf.is_on_this_page())
        csf.click_local_file()
        time.sleep(2)
        #2,调转到文件列表页面
        local_file = ChatSelectLocalFilePage()
        self.assertEqual(local_file.is_on_this_page(),True)
        local_file.select_file('.docx')
        #3.发送成功
        local_file.click_send_button()
        time.sleep(2)
        self.assertEqual(chat.is_element_present_resend(), False)
        # 获取发送文件的名称
        chat = ChatWindowPage()
        time.sleep(2)
        #返回聊天列表
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.page_should_contain_text('文件')


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_fenzu_0014(self):
        """勾选本地文件内任意图片点击发送按钮"""
        #勾选本地文件 发送
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_file()
        #1,调转到选择文件页面-选择本地文件
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        self.assertTrue(csf.is_on_this_page())
        csf.click_pic()
        time.sleep(2)
        #2,调转到选择图片页面
        select_pic=ChatPicPage()
        self.assertEqual(select_pic.is_on_this_page(),True)
        select_pic.click_camara_picture()
        select_pic.select_first_picture()
        select_pic.click_send()
        #3.发送成功
        time.sleep(2)
        self.assertEqual(chat.is_element_present_resend(), False)
        # 返回聊天列表查看
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        msg.page_should_contain_text('图片')


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_fenzu_0028(self):
        """勾选本地文件内任意视频点击发送按钮"""
        #进入本地文件页面
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_file()
        #1,调转到选择文件页面-选择本地文件
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        self.assertTrue(csf.is_on_this_page())
        csf.click_video()
        time.sleep(2)
        #2,调转到选择视频页面
        self.assertEqual(csf.is_on_this_page_select_video(),True)
        csf.click_select_video()
        #3.发送成功
        time.sleep(2)
        self.assertEqual(chat.is_element_present_resend(), False)
        # 返回聊天列表查看
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        msg.page_should_contain_text('视频')

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_fenzu_0157(self):
        """标签分组发送位置成功"""
        #勾选位置
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_more()
        chat.click_locator()
        #选择位置界面
        locator = ChatLocationPage()
        self.assertEqual(locator.is_on_this_page(),True)
        locator.click_send()
        #3.发送成功
        time.sleep(2)
        self.assertEqual(chat.is_element_present_resend(), False)
        # 返回聊天列表查看
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        msg.wait_for_page_load()
        msg.page_should_contain_text('位置')


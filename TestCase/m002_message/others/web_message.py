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

import re
import random
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
    def make_sure_chatwindow_exist_web_message():
        """确保我的电脑页面有网页消息记录"""
        chat=ChatWindowPage()
        time.sleep(2)
        text='www.baidu.com'
        if chat.is_element_present_web_message():
            chat.wait_for_page_load()
        else:
            chat.input_message_text(text)
            chat.click_send_button()
            time.sleep(3)

    @staticmethod
    def send_web_message():
        """聊天界面-网页消息"""
        chat=ChatWindowPage()
        time.sleep(2)
        text = 'www.baidu.com'
        chat.input_message_text(text)
        chat.click_send_button()
        time.sleep(3)



class WebMessagePage(TestCase):
    """消息--网页消息"""

    #
    # def setUpClass(cls):
    #     """清除消息页面所以的聊天记录"""
    #     Preconditions.make_already_in_message_page()
    #     MessagePage().delete_all_message_list()
    #     time.sleep(2)
    #

    @classmethod
    def default_setUp(self):
        """确保每个用例执行前在单聊页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        if msg.is_text_present('大佬1'):
            msg.click_text('大佬1')
        else:
            msg.click_search_box()
            msg.input_search_text('大佬1')
            time.sleep(2)
            msg.click_search_local_contact()
            time.sleep(2)
            ContactDetailsPage().click_message_icon()


    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CMCC', 'web_message')
    def test_msg_hanjiabin_0212(self):
        """网页消息——发出网页消息消息界面——长按-转发"""
        #发出网页消息
        chat=ChatWindowPage()
        select=SelectContactsPage()
        Preconditions.make_sure_chatwindow_exist_web_message()
        time.sleep(3)
        #长按-转发
        # chat.long_press(text)
        chat.swipe_by_percent_on_screen(50,18,70,18)
        chat.click_forward()
        self.assertEqual(SelectContactsPage().is_on_this_page(),True)
        #转发到我的电脑
        select.click_search_contact()
        select.input_search_keyword('我的电脑')
        select.click_search_result()
        select.click_sure_forward()
        #转发到本地联系人
        chat.swipe_by_percent_on_screen(50, 18, 70, 18)
        # chat.long_press('个人名片')
        chat.click_forward()
        select.select_local_contacts()
        local_contact = SelectLocalContactsPage()
        self.assertEqual(local_contact.is_on_this_page(), True)
        local_contact.swipe_select_one_member_by_name('大佬2')
        local_contact.click_sure()
        #转发到群聊
        chat.swipe_by_percent_on_screen(50, 18, 70, 18)
        # chat.long_press('个人名片')
        chat.click_forward()
        select.click_select_one_group()
        SelectOneGroupPage().selecting_one_group_by_name('群聊1')
        SelectOneGroupPage().click_sure_send()
        #转发到团队联系人
        chat.swipe_by_percent_on_screen(50, 18, 70, 18)
        # chat.long_press('个人名片')
        chat.click_forward()
        select.click_group_contact()
        group_contact=SelectHeContactsPage()
        group_contact.select_one_team_by_name('ateam7272')
        group_detail=SelectHeContactsDetailPage()
        group_detail.wait_for_he_contacts_page_load()
        group_detail.select_one_he_contact_by_name('alice')
        group_detail.click_sure()
        #转发到企业群
        chat.swipe_by_percent_on_screen(50, 18, 70, 18)
        # chat.long_press('个人名片')
        chat.click_forward()
        select.click_select_one_group()
        SelectOneGroupPage().select_one_company_group()
        SelectOneGroupPage().click_sure_send()
        time.sleep(2)


    @tags('ALL', 'CMCC', 'web_message')
    def test_msg_hanjiabin_0213(self):
        """网页消息——发出网页消息消息界面——长按-收藏"""
        #发出网页消息
        chat=ChatWindowPage()
        select=SelectContactsPage()
        Preconditions.make_sure_chatwindow_exist_web_message()
        time.sleep(3)
        #长按-收藏
        # chat.long_press(text)
        chat.swipe_by_percent_on_screen(50,18,70,18)
        chat.click_collection()
        time.sleep(2)
        #进入收藏页面查看
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        collection = MeCollectionPage()
        collection.page_should_contain_text('今天')
        #点击进入收藏列表
        time.sleep(2)
        collection.click_list_by_name('今天')
        self.assertEqual(collection.is_element_present_collection_detail(),True)


    @tags('ALL', 'CMCC', 'web_message')
    def test_msg_hanjiabin_0214(self):
        """网页消息——发出网页消息消息界面——长按-撤回"""
        #发出网页消息
        chat=ChatWindowPage()
        select=SelectContactsPage()
        chat.clear_all_chat_record()
        Preconditions.make_sure_chatwindow_exist_web_message()
        time.sleep(3)
        #长按-撤回
        # chat.long_press(text)
        chat.swipe_by_percent_on_screen(50,18,70,18)
        chat.click_revoke()
        time.sleep(2)
        #撤回成功
        chat.page_contain_element(locator='你撤回了一条消息')
        time.sleep(2)

    @tags('ALL', 'CMCC', 'web_message')
    def test_msg_hanjiabin_0215(self):
        """网页消息——发出网页消息消息界面——长按-删除"""
        # 发出网页消息
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
        Preconditions.make_sure_chatwindow_exist_web_message()
        time.sleep(3)
        # 长按-删除
        chat.swipe_by_percent_on_screen(50, 18, 70, 18)
        chat.click_revoke()
        time.sleep(2)
        # 删除成功
        chat.click_sure_delete()
        self.assertEqual(chat.is_element_present_web_message(), False)


    @tags('ALL', 'CMCC', 'web_message')
    def test_msg_hanjiabin_0216(self):
        """网页消息——发出网页消息消息界面——长按-多选"""
        # 发出网页消息
        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_web_message()
        time.sleep(3)
        # 长按-多选
        chat.swipe_by_percent_on_screen(50, 18, 70, 18)
        chat.click_show_more_items()
        chat.click_multiple_selection()
        time.sleep(2)
        chat.page_contain_element(locator='多选按钮')
        chat.page_contain_element(locator='多选-删除')
        chat.page_contain_element(locator='多选-转发')


    @tags('ALL', 'CMCC', 'web_message')
    def test_msg_hanjiabin_0222(self):
        """网页消息——打开链接后的通用浏览器——右上角更多-转发给朋友"""
        # 发出网页消息
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
        Preconditions.make_sure_chatwindow_exist_web_message()
        time.sleep(3)
        # 点击链接进入链接详情-点击更多--点击转发给朋友
        chat.click_element_web_message()
        chat.wait_for_page_load_web_message()
        chat.click_more_web_message()
        time.sleep(2)
        chat.click_forward_to_friend()
        #选择联系人界面-正常转发
        select=SelectContactsPage()
        select.select_local_contacts()
        local_contact = SelectLocalContactsPage()
        self.assertEqual(local_contact.is_on_this_page(), True)
        local_contact.swipe_select_one_member_by_name('大佬2')
        local_contact.click_sure()
        self.assertEqual(chat.is_on_this_page_web_message(),True)
        #中断正常未验证


    @tags('ALL', 'CMCC', 'web_message')
    def test_msg_hanjiabin_0223(self):
        """网页消息——打开链接后的通用浏览器——右上角更多-转发给微信"""
        # 发出网页消息
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
        Preconditions.make_sure_chatwindow_exist_web_message()
        time.sleep(3)
        # 点击链接进入链接详情-点击更多--点击转发给微信
        chat.click_element_web_message()
        chat.wait_for_page_load_web_message()
        chat.click_more_web_message()
        time.sleep(2)
        chat.click_forward_to_weixin()
        #验证点-调起打开微信弹框
        chat.page_should_contain_text('打开')
        #中断正常未验证


    @tags('ALL', 'CMCC', 'web_message')
    def test_msg_hanjiabin_0224(self):
        """网页消息——打开链接后的通用浏览器——右上角更多-转发到朋友圈"""
        # 发出网页消息
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
        Preconditions.make_sure_chatwindow_exist_web_message()
        time.sleep(3)
        # 点击链接进入链接详情-点击更多--点击转发到朋友圈
        chat.click_element_web_message()
        chat.wait_for_page_load_web_message()
        chat.click_more_web_message()
        time.sleep(2)
        chat.click_forward_to_circle_of_friend()
        #验证点-调起打开微信弹框
        chat.page_should_contain_text('打开')
        #中断正常未验证


    @tags('ALL', 'CMCC', 'web_message')
    def test_msg_hanjiabin_0225(self):
        """网页消息——打开链接后的通用浏览器——右上角更多-转发给qq好友"""
        # 发出网页消息
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
        Preconditions.make_sure_chatwindow_exist_web_message()
        time.sleep(3)
        # 点击链接进入链接详情-点击更多--点击转发qq
        chat.click_element_web_message()
        chat.wait_for_page_load_web_message()
        chat.click_more_web_message()
        time.sleep(2)
        chat.click_forward_to_qq()


    @tags('ALL', 'CMCC', 'web_message')
    def test_msg_hanjiabin_0226(self):
        """网页消息——打开链接后的通用浏览器——右上角更多-系统浏览器打开"""
        # 发出网页消息
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
        Preconditions.make_sure_chatwindow_exist_web_message()
        time.sleep(3)
        # 点击链接进入链接详情-点击更多--系统浏览器打开
        chat.click_element_web_message()
        chat.wait_for_page_load_web_message()
        chat.click_more_web_message()
        time.sleep(2)
        chat.click_open_in_Safari()


    @tags('ALL', 'CMCC', 'web_message')
    def test_msg_hanjiabin_0227(self):
        """网页消息——打开链接后的通用浏览器——右上角更多-复制链接"""
        # 发出网页消息
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
        Preconditions.make_sure_chatwindow_exist_web_message()
        time.sleep(3)
        # 点击链接进入链接详情-点击更多--点击复制链接
        chat.click_element_web_message()
        chat.wait_for_page_load_web_message()
        chat.click_more_web_message()
        time.sleep(2)
        chat.click_copy_link()

        self.assertEqual(chat.is_on_this_page_web_message(), True)

    @tags('ALL', 'CMCC', 'web_message')
    def test_msg_hanjiabin_0228(self):
        """网页消息——打开链接后的通用浏览器——右上角更多-刷新"""
        # 发出网页消息
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
        Preconditions.make_sure_chatwindow_exist_web_message()
        time.sleep(3)
        # 点击链接进入链接详情-点击更多--点击刷新
        chat.click_element_web_message()
        chat.wait_for_page_load_web_message()
        chat.click_more_web_message()
        time.sleep(2)
        chat.click_refresh()
        self.assertEqual(chat.is_on_this_page_web_message(), True)


    @classmethod
    def setUp_msg_hanjiabin_0229(self):
        """网页消息—场景-单聊"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg = MessagePage()
        if msg.is_text_present('大佬1'):
            msg.click_text('大佬1')
        else:
            msg.click_search_box()
            msg.input_search_text('大佬1')
            time.sleep(2)
            msg.click_search_local_contact()
            time.sleep(2)
            ContactDetailsPage().click_message_icon()


    def tearDown_msg_hanjiabin_0229(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CMCC', 'web_message')
    def test_msg_hanjiabin_0229(self):
        """网页消息——场景-单聊"""
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
        time.sleep(2)
        text = 'www.baidu.com'
        chat.input_message_text(text)
        chat.click_send_button()
        time.sleep(3)
        #功能 文案正常
        self.assertEqual(chat.is_element_present_web_message(),True)


    @classmethod
    def setUp_msg_hanjiabin_0230(self):
        """网页消息—场景-群聊"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg = MessagePage()
        if msg.is_text_present('群聊1'):
            msg.click_text('群聊1')
        else:
            msg.click_search_box()
            msg.input_search_text('群聊1')
            time.sleep(2)
            msg.click_element_first_list()
            time.sleep(2)
            ContactDetailsPage().click_message_icon()


    def tearDown_msg_hanjiabin_0230(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CMCC', 'web_message')
    def test_msg_hanjiabin_0230(self):
        """网页消息——场景-群聊"""
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
        time.sleep(2)
        text = 'www.baidu.com'
        chat.input_message_text(text)
        chat.click_send_button()
        time.sleep(3)
        # 功能 文案正常
        self.assertEqual(chat.is_element_present_web_message(), True)

    @classmethod
    def setUp_msg_hanjiabin_0231(self):
        """网页消息—场景-企业群"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg = MessagePage()
        if msg.is_text_present('测试企业群'):
            msg.click_text('测试企业群')
        else:
            msg.click_search_box()
            msg.input_search_text('测试企业群')
            time.sleep(2)
            msg.click_element_first_list()
            time.sleep(2)
            ContactDetailsPage().click_message_icon()


    def tearDown_msg_hanjiabin_0231(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CMCC', 'web_message')
    def test_msg_hanjiabin_0231(self):
        """网页消息——场景-企业群"""
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
        time.sleep(2)
        text = 'www.baidu.com'
        chat.input_message_text(text)
        chat.click_send_button()
        time.sleep(3)
        # 功能 文案正常
        self.assertEqual(chat.is_element_present_web_message(), True)

    @classmethod
    def setUp_msg_hanjiabin_0232(self):
        """网页消息—场景-标签分组"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        lable_group = LabelGroupingPage()
        lable_detail = LableGroupDetailPage()
        # 确保在消息页面
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        contact = ContactsPage()
        contact.click_phone_contact()
        time.sleep(2)
        contact.click_label_grouping()
        # 确保进入标签分组会话页面
        if lable_group.is_element_present(locator='已建分组列表1'):
            lable_group.click_first_lable_group()
        else:
            lable_group.creat_group('aaa')
            time.sleep(2)
            # 为标签分组添加成员
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


    def tearDown_msg_hanjiabin_0232(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CMCC', 'web_message')
    def test_msg_hanjiabin_0232(self):
        """网页消息——场景-标签分组"""
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
        time.sleep(2)
        text = 'www.baidu.com'
        chat.input_message_text(text)
        chat.click_send_button()
        time.sleep(3)
        # 功能 文案正常
        self.assertEqual(chat.is_element_present_web_message(), True)


    @classmethod
    def setUp_msg_hanjiabin_0233(self):
        """网页消息—场景-我的电脑"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg = MessagePage()
        if msg.is_text_present('我的电脑'):
            msg.click_text('我的电脑')
        else:
            msg.click_search_box()
            msg.input_search_text('我的电脑')
            time.sleep(2)
            msg.click_element_first_list()
            time.sleep(2)
            ContactDetailsPage().click_message_icon()


    def tearDown_msg_hanjiabin_0233(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CMCC', 'web_message')
    def test_msg_hanjiabin_0233(self):
        """网页消息——场景-我的电脑"""
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
        time.sleep(2)
        text = 'www.baidu.com'
        chat.input_message_text(text)
        chat.click_send_button()
        time.sleep(3)
        # 功能 文案正常
        self.assertEqual(chat.is_element_present_web_message(), True)
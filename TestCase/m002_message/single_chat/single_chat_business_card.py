import unittest
import time
import warnings
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from preconditions.BasePreconditions import LoginPreconditions, WorkbenchPreconditions
from library.core.utils.testcasefilter import tags
from pages.chat.chatfileProview import ChatfileProviewPage
from pages.contacts.AllMyTeam import AllMyTeamPage


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


class Preconditions(WorkbenchPreconditions):
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
    def make_sure_chatwindow_exist_business_card_list():
        """确保我的电脑页面有分享名片记录"""
        chat=ChatWindowPage()
        time.sleep(2)
        if chat.is_element_present_card_list():
            chat.wait_for_page_load()
        else:
            chat.click_more()
            chat.click_name_card()
            select = SelectContactsPage()
            select.select_one_contact_by_name('大佬2')
            select.click_share_card()
            time.sleep(2)

    @staticmethod
    def send_business_card():
        """聊天界面-发送名片"""
        chat=ChatWindowPage()
        time.sleep(2)
        chat.click_more()
        chat.click_name_card()
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬2')
        time.sleep(1)
        select.click_share_card()
        time.sleep(2)




class SingleChatBusinessCard(TestCase):
    """单聊--名片"""

    @classmethod
    def setUpClass(cls):
        """删除消息列表的消息记录"""
        warnings.simplefilter('ignore', ResourceWarning)
        # Preconditions.select_mobile('IOS-移动')
        # #创建团队ateam7272
        # Preconditions.make_already_in_message_page()
        # MessagePage().delete_all_message_list()
        # Preconditions.create_team_if_not_exist_and_set_as_defalut_team()
        # # 导入团队联系人、企业部门
        # fail_time2 = 0
        # flag2 = False
        # while fail_time2 < 5:
        #     try:
        #         Preconditions.make_already_in_message_page()
        #         contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
        #         Preconditions.create_he_contacts(contact_names)
        #         contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
        #                           ('陈丹丹', "13800137004"), ('alice', "13800137005"), ('郑海', "13802883296")]
        #         Preconditions.create_he_contacts2(contact_names2)
        #         department_names = ["测试部门1", "测试部门2"]
        #         Preconditions.create_department_and_add_member(department_names)
        #         flag2 = True
        #     except:
        #         fail_time2 += 1
        #     if flag2:
        #         break

    @classmethod
    def default_setUp(self):
        """确保每个用例执行前在单聊页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        LoginPreconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        if msg.is_text_present('大佬1'):
            msg.click_text('大佬1')
        else:
            msg.open_contacts_page()
            ContactsPage().click_phone_contact()
            ContactsPage().select_contacts_by_name('大佬1')
            ContactDetailsPage().click_message_icon()
            time.sleep(2)

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0179(self):
        """名片消息——单聊——点击名片按钮进入“和通讯录+本地联系人”的联系人选择器——搜索——名称搜索-团队联系人搜索结果"""
        #单聊页面--点击名片
        chat=ChatWindowPage()
        chat.click_more()
        chat.click_name_card()
        #选择联系人页面-搜索-名称搜索
        select=SelectContactsPage()
        select.click_search_contact()
        select.input_search_keyword('大佬2')
        #点击团队联系人搜索
        select.click_search_group_contact()
        select.click_element_by_id(text='团队联系人搜索结果')
        time.sleep(2)
        #验证页面元素
        self.assertEqual(select.is_element_present(locator='分享名片左上角的X按钮'),True)
        self.assertEqual(select.is_element_present(locator='分享名片-头像'), True)
        self.assertEqual(select.is_text_present('大佬2'), True)
        self.assertEqual(select.is_text_present('13800138006'), True)
        self.assertEqual(select.is_element_present(locator='分享名片-可选项'), True)
        #点击右上角的X 可关闭弹框
        select.click_share_card_close_icon()
        select.page_should_not_contain_text('发送名片')
        time.sleep(2)


    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0180(self):
        """名片消息——单聊——点击名片按钮进入“和通讯录+本地联系人”的联系人选择器——搜索——名称搜索-本地搜索结果"""
        #单聊页面--点击名片
        chat=ChatWindowPage()
        chat.click_more()
        chat.click_name_card()
        #选择联系人页面-搜索-名称搜索
        select=SelectContactsPage()
        select.click_search_contact()
        select.input_search_keyword('大佬2')
        #点击本地联系人搜索结果
        select.click_element_by_id(text='搜索结果列表1')
        time.sleep(2)
        #验证页面元素
        self.assertEqual(select.is_element_present(locator='分享名片左上角的X按钮'),True)
        self.assertEqual(select.is_element_present(locator='分享名片-头像'), True)
        self.assertEqual(select.is_text_present('大佬2'), True)
        self.assertEqual(select.is_text_present('13800138006'), True)
        #点击右上角的X 可关闭弹框
        select.click_share_card_close_icon()
        select.page_should_not_contain_text('发送名片')
        time.sleep(2)


    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0181(self):
        """名片消息——单聊——点击名片按钮进入“和通讯录+本地联系人”的联系人选择器——搜索——号码搜索-团队搜索结果"""
        #单聊页面--点击名片
        chat=ChatWindowPage()
        chat.click_more()
        chat.click_name_card()
        #选择联系人页面-搜索-名称搜索
        select=SelectContactsPage()
        select.click_search_contact()
        select.input_search_keyword('13800138006')
        #点击团队联系人搜索
        select.click_search_group_contact()
        select.click_element_by_id(text='团队联系人搜索结果')
        time.sleep(2)
        #验证页面元素
        self.assertEqual(select.is_element_present(locator='分享名片左上角的X按钮'),True)
        self.assertEqual(select.is_element_present(locator='分享名片-头像'), True)
        self.assertEqual(select.is_text_present('大佬2'), True)
        self.assertEqual(select.is_text_present('13800138006'), True)
        self.assertEqual(select.is_element_present(locator='分享名片-可选项'), True)
        #点击右上角的X 可关闭弹框
        select.click_share_card_close_icon()
        select.page_should_not_contain_text('发送名片')
        time.sleep(2)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0182(self):
        """名片消息——单聊——点击名片按钮进入“和通讯录+本地联系人”的联系人选择器——搜索——号码搜索-本地搜索结果"""
        #单聊页面--点击名片
        chat=ChatWindowPage()
        chat.click_more()
        chat.click_name_card()
        #选择联系人页面-搜索-名称搜索
        select=SelectContactsPage()
        select.click_search_contact()
        select.input_search_keyword('13800138006')
        #点击本地联系人搜索结果
        select.click_element_by_id(text='搜索结果列表1')
        time.sleep(2)
        #验证页面元素
        self.assertEqual(select.is_element_present(locator='分享名片左上角的X按钮'),True)
        self.assertEqual(select.is_element_present(locator='分享名片-头像'), True)
        self.assertEqual(select.is_text_present('大佬2'), True)
        self.assertEqual(select.is_text_present('13800138006'), True)
        #点击右上角的X 可关闭弹框
        select.click_share_card_close_icon()
        select.page_should_not_contain_text('发送名片')
        time.sleep(2)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0183(self):
        """名片消息——单聊——点击名片按钮进入“和通讯录+本地联系人”的联系人选择器——选择和通讯录联系人"""
        #单聊页面--点击名片
        chat=ChatWindowPage()
        chat.click_more()
        chat.click_name_card()
        #选择联系人页面-选择和通讯录联系人
        select=SelectContactsPage()
        select.click_he_contacts()
        select_he=SelectHeContactsPage()
        select_he.select_one_team_by_name('ateam7272')
        #选择和通讯录联系人详情页面
        select_he_detail=SelectHeContactsDetailPage()
        time.sleep(3)
        select_he_detail.select_one_he_contact_by_name('alice')
        #验证页面元素
        self.assertEqual(select.is_element_present(locator='分享名片左上角的X按钮'),True)
        self.assertEqual(select.is_element_present(locator='分享名片-头像'), True)
        self.assertEqual(select.is_text_present('大佬2'), True)
        self.assertEqual(select.is_text_present('13800138006'), True)
        self.assertEqual(select.is_element_present(locator='分享名片-可选项'), True)
        #点击右上角的X 可关闭弹框
        select.click_share_card_close_icon()
        select.page_should_not_contain_text('发送名片')
        time.sleep(2)


    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0184(self):
        """名片消息——单聊——点击名片按钮进入“和通讯录+本地联系人”的联系人选择器——选择本地联系人"""
        #单聊页面--点击名片
        chat=ChatWindowPage()
        chat.click_more()
        chat.click_name_card()
        #选择联系人页面-选择本地联系人
        select=SelectContactsPage()
        select.select_one_contact_by_name('大佬2')
        #验证页面元素
        self.assertEqual(select.is_element_present(locator='分享名片左上角的X按钮'),True)
        self.assertEqual(select.is_element_present(locator='分享名片-头像'), True)
        self.assertEqual(select.is_text_present('大佬2'), True)
        self.assertEqual(select.is_text_present('13800138006'), True)
        # self.assertEqual(select.is_element_present(locator='分享名片-可选项'), True)
        #点击右上角的X 可关闭弹框
        select.click_share_card_close_icon()
        select.page_should_not_contain_text('发送名片')
        time.sleep(2)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0189(self):
        """名片消息——单聊——发出名片后--消息界面——点击查看-已在本地"""
        #单聊页面--点击名片
        chat=ChatWindowPage()
        chat.click_more()
        chat.click_name_card()
        #选择联系人页面-选择本地联系人-发送名片
        select=SelectContactsPage()
        select.select_one_contact_by_name('大佬2')
        select.click_share_card()
        time.sleep(2)
        #点击名片消息，查看
        chat.click_business_card_list()
        contact_detail=ContactDetailsPage()
        self.assertEqual(contact_detail.is_on_this_page(),True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0190(self):
        """名片消息——单聊——发出名片后--消息界面——点击查看-未在本地"""
        #单聊页面--点击名片
        chat=ChatWindowPage()
        chat.click_more()
        chat.click_name_card()
        #选择联系人页面-选择未保存在本地的联系人(和通讯录联系人)
        select=SelectContactsPage()
        select.click_he_contacts()
        select_he=SelectHeContactsPage()
        select_he.select_one_team_by_name('ateam7272')
        #选择和通讯录联系人详情页面
        select_he_detail=SelectHeContactsDetailPage()
        time.sleep(3)
        select_he_detail.select_one_he_contact_by_name('alice')
        select.click_share_card()
        time.sleep(2)
        #点击名片消息，查看
        chat.click_business_card_list()
        time.sleep(3)
        contact_detail=ContactDetailsPage()
        self.assertEqual(contact_detail.is_on_this_page(),True)
        contact_detail.page_should_contain_text('保存到通讯录')


    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0191(self):
        """名片消息——单聊——发出名片后--消息界面——长按"""
        #单聊页面--点击名片
        chat=ChatWindowPage()
        select = SelectContactsPage()
        Preconditions.make_sure_chatwindow_exist_business_card_list()
        time.sleep(2)
        chat.press_and_move_right_business_card()
        chat.click_forward()
        #转发到我的电脑
        select.click_search_contact()
        select.input_search_keyword('我的电脑')
        select.click_search_result()
        select.click_sure_forward()
        #转发到群聊
        chat.press_and_move_right_business_card()
        chat.click_forward()
        select.click_select_one_group()
        SelectOneGroupPage().selecting_one_group_by_name('群聊1')
        SelectOneGroupPage().click_sure_send()
        #转发到团队联系人
        chat.press_and_move_right_business_card()
        chat.click_forward()
        select.click_group_contact()
        group_contact=SelectHeContactsPage()
        group_contact.select_one_team_by_name('ateam7272')
        group_detail=SelectHeContactsDetailPage()
        group_detail.wait_for_he_contacts_page_load()
        group_detail.select_one_he_contact_by_name('alice')
        group_detail.click_sure()
        #转发到本地联系人
        chat.press_and_move_right_business_card()
        chat.click_forward()
        select.select_local_contacts()
        local_contact = SelectLocalContactsPage()
        time.sleep(2)
        self.assertEqual(local_contact.is_on_this_page(), True)
        local_contact.swipe_select_one_member_by_name('大佬2')
        local_contact.click_sure()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0192(self):
        """名片消息——单聊——发出名片后--消息界面——长按-收藏"""
        #单聊页面--点击名片
        chat=ChatWindowPage()
        chat.clear_all_chat_record()
        Preconditions.make_sure_chatwindow_exist_business_card_list()
        time.sleep(2)
        chat.press_and_move_right_business_card()
        chat.click_collection()
        time.sleep(2)
        #进入收藏页面查看
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        collection = MeCollectionPage()
        collection.page_should_contain_text('名片')
        time.sleep(2)
        collection.click_list_by_name('名片')
        collection.page_should_contain_text('大佬2')
        collection.page_should_contain_text('13800138006')

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0193(self):
        """名片消息——单聊——发出名片后--消息界面——长按-撤回"""
        #单聊页面--点击名片
        chat=ChatWindowPage()
        chat.clear_all_chat_record()
        Preconditions.send_business_card()
        time.sleep(2)
        chat.press_and_move_right_business_card()
        #点击撤回
        chat.click_revoke()
        time.sleep(2)
        chat.page_contain_element(locator='你撤回了一条消息')


    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0194(self):
        """名片消息——单聊——发出名片后--消息界面——长按-删除"""
        #单聊页面--点击名片
        chat=ChatWindowPage()
        Preconditions.send_business_card()
        time.sleep(2)
        chat.press_and_move_right_business_card()
        #点击删除
        chat.click_delete()
        time.sleep(2)
        chat.click_sure_delete()
        self.assertEqual(chat.is_element_present_web_message(),False)



    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0195(self):
        """名片消息——单聊——发出名片后--消息界面——多选"""
        #单聊页面--点击名片
        chat=ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_business_card_list()
        time.sleep(2)
        chat.press_and_move_right_business_card()
        #点击多选
        chat.click_multiple_selection()
        time.sleep(2)
        chat.page_contain_element(locator='多选按钮')
        chat.page_contain_element(locator='多选-删除')
        chat.page_contain_element(locator='多选-转发')


    @classmethod
    def setUp_test_msg_hanjiabin_0202(self):
        """名片消息—场景-单聊"""
        warnings.simplefilter('ignore', ResourceWarning)
        LoginPreconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        if msg.is_text_present('大佬1'):
            msg.click_text('大佬1')
        else:
            msg.open_contacts_page()
            ContactsPage().click_phone_contact()
            ContactsPage().select_contacts_by_name('大佬1')
            ContactDetailsPage().click_message_icon()
            time.sleep(2)
            SingleChatPage().click_i_have_read()

    def tearDown_test_msg_hanjiabin_0202(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0202(self):
        """名片消息—场景-单聊"""
        chat = ChatWindowPage()
        chat.click_more()
        chat.click_name_card()
        select = SelectContactsPage()
        time.sleep(3)
        select.page_contain_element('选择团队联系人')
        select.page_contain_element('联系人列表')
        select.page_contain_element('搜索或输入手机号')
        #功能正常
        # select.select_local_contacts()
        local_contact = SelectLocalContactsPage()
        self.assertEqual(local_contact.is_on_this_page(), True)
        local_contact.swipe_select_one_member_by_name('大佬2')
        local_contact.click_share_card()


    @classmethod
    def setUp_test_msg_hanjiabin_0203(self):
        """名片消息—场景-普通群"""
        warnings.simplefilter('ignore', ResourceWarning)
        LoginPreconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        msg.delete_all_message_list()
        if msg.is_text_present('群聊1'):
            msg.click_text('群聊1')
        else:
            msg.click_search_box()
            msg.input_search_text('群聊1')
            time.sleep(2)
            msg.click_element_first_list()
            time.sleep(2)
            # ContactDetailsPage().click_message_icon()

    def tearDown_test_msg_hanjiabin_0203(self):

        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0203(self):
        """名片消息—场景-群聊"""
        chat = ChatWindowPage()
        chat.click_more()
        chat.click_name_card()
        #文案正常
        select = SelectContactsPage()
        time.sleep(3)
        select.page_contain_element('选择团队联系人')
        select.page_contain_element('联系人列表')
        select.page_contain_element('搜索或输入手机号')
        #功能正常
        select.select_one_contact_by_name('大佬2')
        select.click_share_card()
        time.sleep(2)
        self.assertEqual(chat.is_on_this_page(), True)
        self.assertEqual(chat.is_element_present_resend(), False)


    @classmethod
    def setUp_test_msg_hanjiabin_0204(self):
        """名片消息—场景-企业群"""
        warnings.simplefilter('ignore', ResourceWarning)
        LoginPreconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        msg.delete_all_message_list()
        if msg.is_text_present('测试企业群'):
            msg.click_text('测试企业群')
        else:
            msg.click_search_box()
            msg.input_search_text('测试企业群')
            time.sleep(2)
            msg.click_element_first_list()
            time.sleep(2)
            # ContactDetailsPage().click_message_icon()

    def tearDown_test_msg_hanjiabin_0204(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0204(self):
        """名片消息—场景-企业群"""
        chat = ChatWindowPage()
        chat.click_more()
        chat.click_name_card()
        select = SelectContactsPage()
        time.sleep(3)
        select.page_contain_element('选择团队联系人')
        select.page_contain_element('联系人列表')
        select.page_contain_element('搜索或输入手机号')
        # 功能正常-发送名片成功
        select.select_one_contact_by_name('大佬2')
        select.click_share_card()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(), True)
        self.assertEqual(chat.is_element_present_resend(), False)


    @classmethod
    def setUp_test_msg_hanjiabin_0205(self):
        """名片消息—场景-标签分组"""
        warnings.simplefilter('ignore', ResourceWarning)
        LoginPreconditions.select_mobile('IOS-移动')
        lable_group = LabelGroupingPage()
        lable_detail = LableGroupDetailPage()
        #确保在消息页面
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        MessagePage().open_contacts_page()
        contact = ContactsPage()
        contact.click_phone_contact()
        time.sleep(2)
        contact.click_label_grouping()
        #确保进入标签分组会话页面
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
            local_contact.click_sure()
        time.sleep(2)
        lable_detail.click_send_group_info()
        time.sleep(3)

    def tearDown_test_msg_hanjiabin_0205(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0205(self):
        """名片消息—场景-标签分组"""
        chat = ChatWindowPage()
        chat.click_more()
        chat.click_name_card()
        select = SelectContactsPage()
        time.sleep(3)
        select.page_contain_element('选择团队联系人')
        select.page_contain_element('联系人列表')
        select.page_contain_element('搜索或输入手机号')
        # 功能正常-发送名片成功
        select.select_one_contact_by_name('大佬2')
        select.click_share_card()
        time.sleep(2)
        self.assertEqual(chat.is_on_this_page(), True)
        self.assertEqual(chat.is_element_present_resend(), False)



    @classmethod
    def setUp_test_msg_hanjiabin_0206(self):
        """名片消息—场景-我的电脑"""
        warnings.simplefilter('ignore', ResourceWarning)
        LoginPreconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        if msg.is_text_present('我的电脑'):
            msg.click_text('我的电脑')
        else:
            msg.click_search_box()
            msg.input_search_text('我的电脑')
            time.sleep(2)
            msg.click_element_first_list()
            time.sleep(2)


    def tearDown_test_msg_hanjiabin_0206(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_hanjiabin_0206(self):
        """名片消息—场景-我的电脑"""
        chat = ChatWindowPage()
        chat.click_more()
        chat.click_name_card()
        select = SelectContactsPage()
        time.sleep(3)
        select.page_contain_element('选择团队联系人')
        select.page_contain_element('联系人列表')
        select.page_contain_element('搜索或输入手机号')
        # 功能正常-发送名片成功
        select.select_one_contact_by_name('大佬2')
        select.click_share_card()
        time.sleep(2)
        self.assertEqual(chat.is_on_this_page(), True)
        self.assertEqual(chat.is_element_present_resend(), False)


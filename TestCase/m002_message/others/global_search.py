
import unittest
import uuid
import time

from pages.contacts.AllMyTeam import AllMyTeamPage
from preconditions.BasePreconditions import LoginPreconditions
from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.contacts.EditContactPage import EditContactPage
from pages import *
import warnings

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
    def create_contacts_if_not_exits(name, number):
        """
        不存在就导入联系人数据
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
        contacts_page.click_phone_contact()
        contacts_page.click_search_phone_contact()
        contacts_page.input_search_keyword(name)
        if contacts_page.is_contact_in_list():
            contacts_page.click_back()
        else:
            contacts_page.click_add()
            create_page = CreateContactPage()
            create_page.create_contact(name, number)
            time.sleep(2)
            detail_page.click_back_icon()
            contacts_page.click_back()


class GloableSearchContacts(TestCase):
    """
    搜索-全局搜索-黄彩最

    """

    def default_setUp(self):
        """确保每个用例运行前在消息页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.delete_all_message_list()

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'CMCC', 'msg')
    def test_msg_huangcaizui_E_0001(self):
        """消息-消息列表界面搜索框显示"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 验证是否存在搜索框显示
        self.assertTrue(mess.is_element_present(text="搜索"))

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0002(self):
        """搜索框正常弹起和收起"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击搜索
        mess.click_search_box()
        # 2.验证是否存在
        self.assertTrue(mess.is_element_present(text="输入关键字快速搜索"))
        # 3.点击其它区域
        mess.click_coordinate()
        # 4.验证键盘是否收起
        self.assertFalse(mess.is_element_present_key())

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0003(self):
        """搜索联系人"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击搜索
        mess.click_search_box()
        # 2.输入搜索联系人
        mess.input_search_text("陈")
        time.sleep(3)
        # 3.验证有没有搜索结果
        self.assertTrue(mess.is_element_present(text="搜索结果列表1"))

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0006(self):
        """搜索关键字-精准搜索"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击搜索
        mess.click_search_box()
        # 2.输入搜索关键字精准搜索
        mess.input_search_text("大佬1")
        time.sleep(3)
        # 3.验证有没有搜索结果
        self.assertTrue(mess.is_element_present(text="搜索结果列表1"))

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0007(self):
        """搜索关键字-中文模糊搜索"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击搜索
        mess.click_search_box()
        # 2.输入搜索关键字-中文模糊搜索
        mess.input_search_text("大佬")
        time.sleep(3)
        # 3.验证有没有搜索结果
        self.assertTrue(mess.is_element_present(text="搜索结果列表1"))

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0015(self):
        """搜索聊天记录排序"""
        # 1.进入群聊页面
        Preconditions.enter_group_chat_page("给个红包1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 2.发送消息确保有记录
        gcp.input_message_text("聊天记录测试")
        gcp.click_send_button()
        # 3.点击返回消息页面
        gcp.click_back()
        # 4.再次进入群聊页面
        Preconditions.enter_group_chat_page("给个红包2")
        gcp.wait_for_page_load()
        # 5.发送消息确保有记录
        gcp.input_message_text("聊天记录测试")
        gcp.click_send_button()
        # 6.点击返回消息页面
        gcp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 7.点击搜索
        mess.click_search_box()
        # 8.输入消息记录关键字
        mess.input_search_text("记录测试")
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0016(self):
        """搜索聊天记录排序"""
        # 1.进入群聊页面
        Preconditions.enter_group_chat_page("给个红包1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 2.发送消息确保有记录
        gcp.input_message_text("聊天记录测试")
        gcp.click_send_button()
        # 3.点击返回消息页面
        gcp.click_back()
        # 4.进入单聊会话页面
        Preconditions.enter_single_chat_page("大佬1")
        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 5.发送消息确保有记录
        scp.input_message("聊天记录测试")
        scp.send_text()
        # 6.点击返回消息页面
        scp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 7.点击搜索
        mess.click_search_box()
        # 8.输入消息记录关键字
        mess.input_search_text("记录测试")
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0017(self):
        """查看更多联系人"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击搜索
        mess.click_search_box()
        # 2.输入联系人关键字
        mess.input_search_text("大佬")
        time.sleep(3)
        # 3.点击更多
        mess.click_accessibility_id_attribute_by_name("查看更多")
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0020(self):
        """查看更多群聊"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击搜索
        mess.click_search_box()
        # 2.输入群聊关键字
        mess.input_search_text("群")
        time.sleep(3)
        # 3.点击更多
        mess.click_accessibility_id_attribute_by_name("查看更多")
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0024(self):
        """查看更多聊天记录"""
        # 1.进入群聊页面
        Preconditions.enter_group_chat_page("给个红包1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 2.发送消息确保有多条记录
        for i in range(2):
            gcp.input_message_text("查看更多聊天记录测试")
            gcp.click_send_button()
            time.sleep(5)
        # 3.点击返回消息页面
        gcp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 4.点击搜索
        mess.click_search_box()
        # 5.输入群聊关键字
        mess.input_search_text("查看更多聊天记录测试")
        time.sleep(2)
        # 6.验证是否显示对应聊天记录的数量
        self.assertTrue(mess.page_should_contain_text2("2 条相关的聊天记录"))

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0027(self):
        """搜索关键字"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击搜索
        mess.click_search_box()
        # 2.输入群聊关键字
        mess.input_search_text("群")
        time.sleep(3)
        self.assertTrue(mess.page_should_contain_text2("手机联系人"))
        self.assertTrue(mess.page_should_contain_text2("群聊"))

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0028(self):
        """搜索行业消息"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击搜索
        mess.click_search_box()
        # 2.输入考勤打卡
        mess.input_search_text("考勤打卡")
        time.sleep(3)
        self.assertTrue(mess.page_should_contain_text2("无搜索结果"))

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0029(self):
        """已使用过pc版和飞信搜索我的电脑"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击搜索
        mess.click_search_box()
        # 2.输入我的电脑
        mess.input_search_text("我的电脑")
        time.sleep(3)
        # 3.点击搜索结果
        mess.click_accessibility_id_attribute_by_name("我的电脑")
        time.sleep(2)
        # 4.验证是否在我的电脑会话页面
        cwp = ChatWindowPage()
        self.assertTrue(cwp.page_should_contain_text2("我的电脑"))
        self.assertTrue(cwp.is_on_this_page())




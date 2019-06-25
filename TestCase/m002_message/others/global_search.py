
import unittest
import uuid
import time
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
        MessagePage().wait_for_page_load()
        MessagePage().click_contacts()
        ContactsPage().click_phone_contact()

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_E_0001(self):
        '''
        消息-消息列表界面搜索框显示
        author:darcy

        :return:
        '''
        lcontact=ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('138005')
        lcontact.page_contain_element(text='列表项')


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0002(self):
        '''
        搜索框正常弹起和收起
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('138')
        time.sleep(3)
        els=lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els)>1)
        lcontact.page_contain_element(text='联系人头像')


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0003(self):
        '''
        搜索联系人
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('13800138005')
        time.sleep(3)
        els=lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els) == 1)
        lcontact.page_contain_element(text='联系人头像')
        lcontact.page_should_contain_text('大佬1')

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0006(self):
        '''
        搜索关键字-精准搜索
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('大佬')
        time.sleep(3)
        els=lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els)>1)
        lcontact.page_contain_element(text='联系人头像')


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0007(self):
        '''
        搜索关键字-中文模糊搜索
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('dalao')
        time.sleep(3)
        els=lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els)>1)
        lcontact.page_contain_element(text='联系人头像')

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0015(self):
        '''
        搜索聊天记录排序
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('#')
        time.sleep(3)
        els=lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els)>1)
        lcontact.page_contain_element(text='联系人头像')

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0016(self):
        '''
        搜索聊天记录排序
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('大佬1')
        time.sleep(3)
        els=lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els) == 1)
        lcontact.page_contain_element(text='联系人头像')
        lcontact.page_should_contain_text('大佬1')
        lcontact.page_should_contain_text('13800138005')


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0017(self):
        '''
        查看更多联系人
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('sim联系人')
        time.sleep(3)
        els=lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els) == 1)
        lcontact.page_contain_element(text='联系人头像')
        lcontact.page_should_contain_text('大佬1')
        lcontact.page_should_contain_text('13800138005')


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0020(self):
        '''
        查看更多群聊
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('大佬1')
        time.sleep(3)
        els=lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els) == 1)
        lcontact.click_element_contact()
        time.sleep(2)
        ContactDetailsPage().is_on_this_page()


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0024(self):
        '''
        查看更多聊天记录
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('+86')
        time.sleep(3)
        els=lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els) == 1)
        lcontact.click_element_contact()
        time.sleep(2)
        ContactDetailsPage().is_on_this_page()


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0027(self):
        '''
        搜索关键字
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('+852')
        time.sleep(3)
        els=lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els) == 1)
        lcontact.click_element_contact()
        time.sleep(2)
        ContactDetailsPage().is_on_this_page()

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0028(self):
        '''
        搜索行业消息
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('大佬1')
        time.sleep(2)
        lcontact.click_element_contact()
        detail=ContactDetailsPage()
        time.sleep(2)
        detail.is_on_this_page()
        detail.click_invitation_use()
        detail.page_should_contain_text('短信')
        detail.page_should_contain_text('微信')

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_huangcaizui_E_0029(self):
        '''
        已使用过pc版和飞信搜索我的电脑
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('大佬1')
        time.sleep(2)
        lcontact.click_element_contact()
        detail=ContactDetailsPage()
        time.sleep(2)
        detail.is_on_this_page()




if __name__=="__main__":
    unittest.main()


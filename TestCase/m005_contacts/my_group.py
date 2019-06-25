import unittest
import uuid
import time
from preconditions.BasePreconditions import LoginPreconditions
from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.contacts.EditContactPage import EditContactPage
from pages.contacts.local_contact import localContactPage
import preconditions
from dataproviders import contact2

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




class shareContactpage(TestCase):
    """分享名片"""

    @staticmethod
    def setUp_test_contacts_quxinli_0196():
        #进入通讯录页面
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().click_phone_contact()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('大佬1')
        ContactListSearchPage().click_contact('大佬1')
        time.sleep(2)

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0196(self):
        """在联系人选择器页面，选择一个群"""
        ContactListSearchPage().click_share_card()
        SelectContactsPage().click_select_one_group()
        #搜索框文本显示'搜索群组'
        SelectOneGroupPage().is_text_present('搜索群组')
        #不存在搜索结果时,显示"无搜索结果
        SelectOneGroupPage().click_search_group()
        SelectOneGroupPage().input_search_keyword('wanduzi')
        SelectOneGroupPage().hide_keyboard()
        SelectOneGroupPage().page_should_contain_text('无搜索结果')
        #存在搜索结果时,搜索结果包含关键字
        time.sleep(2)
        SelectOneGroupPage().click_back_icon()
        SelectOneGroupPage().click_search_group()
        SelectOneGroupPage().input_search_keyword('群聊1')
        # SelectOneGroupPage().is_group_in_list('群聊1')
        SelectOneGroupPage().select_one_group_by_name('群聊1')
        time.sleep(2)
        SelectOneGroupPage().click_share_business_card()
        SelectOneGroupPage().click_back_by_android(times=5)

    @staticmethod
    def setUp_test_contacts_quxinli_0197():
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().click_phone_contact()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('大佬1')
        ContactListSearchPage().click_contact('大佬1')
        time.sleep(2)

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0197(self):
        """在联系人选择器页面，选择一个群"""
        ContactListSearchPage().click_share_card()
        SelectContactsPage().click_select_one_group()
        SelectOneGroupPage().selecting_one_group_by_name('群聊1')
        SelectOneGroupPage().is_text_present('发送名片')
        SelectOneGroupPage().click_share_business_card()
        #返回通讯录页面
        ContactDetailsPage().click_back_icon()
        ContactListSearchPage().click_back()

    @staticmethod
    def setUp_test_contacts_quxinli_0198():
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().click_phone_contact()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('大佬1')
        ContactListSearchPage().click_contact('大佬1')
        ContactDetailsPage().click_share_business_card()

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0198(self):
        """在联系人选择器页面，选择本地联系人"""
        SelectContactsPage().select_local_contacts()
        SelectContactsPage().page_should_contain_text('选择联系人')
        SelectContactsPage().page_should_contain_text('搜索或输入手机号')
        #无搜索结果时,下方是否展示：无搜索结果
        SelectContactsPage().click_search_keyword()
        SelectContactsPage().input_search_keyword('wanduzi')
        SelectContactsPage().is_text_present('无搜索结果')
        time.sleep(2)
        #存在搜索结果时,判断显示是否正确
        SelectContactsPage().click_x_icon()
        time.sleep(1)
        SelectContactsPage().input_search_keyword('大佬2')
        SelectContactsPage().select_one_contact_by_name('大佬2')
        SelectContactsPage().click_share_card()

        #返回通讯录页面
        ContactDetailsPage().click_back_icon()
        ContactListSearchPage().click_back()

    @staticmethod
    def setUp_test_contacts_quxinli_0199():
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().click_phone_contact()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('大佬1')
        ContactListSearchPage().click_contact('大佬1')
        time.sleep(2)

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0199(self):
        """在联系人选择器页面，选择本地联系人"""
        ContactDetailsPage().click_share_business_card()
        time.sleep(2)
        select_contact=SelectContactsPage()
        select_contact.select_local_contacts()
        select_contact.click_one_contact('大佬2')
        time.sleep(2)
        select_contact.page_should_contain_text('发送名片')
        SelectOneGroupPage().click_share_business_card()
        SelectOneGroupPage().click_back_by_android(times=5)
        #返回通讯录页面

    @staticmethod
    #和飞信联系人里面已经有超过3个已测试开始的联系人,同时有超过3个群名称包含测试字段的群组
    def setUp_test_contacts_quxinli_0208():
        Preconditions.select_mobile('IOS-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('大佬1')
        ContactListSearchPage().click_contact('大佬1')
        ContactDetailsPage().click_share_business_card()

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0208(self):
        """在联系人选择器页面，搜索联系人"""
        select_contacts=SelectContactsPage()
        #输入'测试'进行搜索,搜索结果显示情况
        select_contacts.click_search_keyword()
        select_contacts.input_search_keyword('给个红包')
        select_contacts.hide_keyboard()
        time.sleep(2)
        select_contacts.page_should_contain_text('搜索团队联系人')
        select_contacts.page_should_contain_text('手机联系人')
        select_contacts.page_should_contain_text('查看更多')
        select_contacts.page_should_contain_text('群聊')
        #选择本地联系人是否会弹出弹框 #是否弹出弹框未检测
        select_contacts.click_one_contact('给个红包1')
        select_contacts.is_text_present('发送名片')
        select_contacts.click_share_card()
        #选择群联系人是否会出现弹框  是否弹出弹框未检测
        ContactDetailsPage().click_share_business_card()
        select_contacts.click_search_keyword()
        select_contacts.input_search_keyword('给个红包1')
        select_contacts.hide_keyboard()
        select_contacts.select_one_group_by_name('给个红包1')
        select_contacts.is_text_present('发送名片')
        select_contacts.click_share_card()
        #点击查看按钮,是否会展示折叠的搜索结果
        ContactDetailsPage().click_share_business_card()
        select_contacts.click_search_keyword()
        select_contacts.input_search_keyword('给个红包')
        select_contacts.hide_keyboard()
        select_contacts.click_read_more()
        time.sleep(2)
        select_contacts.page_should_contain_text('给个红包4')
        select_contacts.click_one_contact('给个红包4')
        select_contacts.click_share_card()
        #返回通讯录页面
        ContactDetailsPage().click_back_icon()
        ContactListSearchPage().click_back()

    @staticmethod
    def setUp_test_contacts_quxinli_0209():
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().click_phone_contact()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('大佬1')
        ContactListSearchPage().click_contact('大佬1')
        ContactListSearchPage().click_share_card()

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0209(self):
        """在联系人选择器页面，选择最近聊天联系人"""
        select_contacts = SelectContactsPage()
        select_contacts.select_one_recently_contact_by_name('大佬2')
        time.sleep(1)
        select_contacts.page_should_contain_text('发送名片')
        select_contacts.click_share_card()
        #返回通讯录页面
        ContactDetailsPage().click_back_icon()
        ContactListSearchPage().click_back()

    @staticmethod
    def setUp_test_contacts_quxinli_0210():
        Preconditions.select_mobile('IOS-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('大佬1')
        ContactListSearchPage().click_contact('大佬1')
        ContactListSearchPage().click_share_card()

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0210(self):
        """在联系人选择器页面，选择最近聊天群聊"""
        select_contacts = SelectContactsPage()
        time.sleep(1)
        select_contacts.click_select_one_group()
        time.sleep(2)
        SelectOneGroupPage().click_one_contact("给个红包1")
        time.sleep(1)
        select_contacts.page_should_contain_text('发送名片')
        select_contacts.click_share_card()
        #返回通讯录页面
        time.sleep(1)
        ContactDetailsPage().click_back_icon()
        ContactListSearchPage().click_back()

    @staticmethod
    def setUp_test_contacts_quxinli_0211():
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().click_phone_contact()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('大佬1')
        ContactListSearchPage().click_contact('大佬1')
        ContactListSearchPage().click_share_card()

    @tags('ALL','CMCC')
    def test_contacts_quxinli_0211(self):
        """在联系人选择器页面，搜索我的电脑"""
        time.sleep(1)
        SelectContactsPage().click_search_contact()
        SelectContactsPage().input_search_keyword('我的电脑')
        SelectContactsPage().hide_keyboard()
        time.sleep(2)
        #返回通讯录页面
        SelectContactsPage().click_back()
        SelectContactsPage().click_back()
        ContactDetailsPage().click_back()
        ContactListSearchPage().click_back()

    @staticmethod
    def setUp_test_contacts_quxinli_0212():
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().click_phone_contact()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('大佬1')
        ContactListSearchPage().click_contact('大佬1')
        ContactListSearchPage().click_share_card()

    @tags('ALL','CMCC')
    def test_contacts_quxinli_0212(self):
        """在联系人选择器页面，搜索11位陌生号码"""
        time.sleep(1)
        select_contact=SelectContactsPage()
        select_contact.click_search_contact()
        select_contact.input_search_keyword('15575256658')
        select_contact.hide_keyboard()
        time.sleep(2)
        select_contact.get_element_text_net_name('未知号码')
        select_contact.get_element_text_net_number('tel:+86')
        time.sleep(2)
        #返回消息页面
        SelectContactsPage().click_back()
        SelectContactsPage().click_back()
        ContactDetailsPage().click_back()
        ContactListSearchPage().click_back()

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


class myGroupContacts(TestCase):
    """通讯录-我的团队"""

    class SearchLocalContacts(TestCase):
        """
        搜索-我的团队-曲新莉

        """

    def default_setUp(self):
        """确保每个用例运行前在我的团队页面"""
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load()
        MessagePage().click_contacts()
        ContactsPage().click_phone_contact()

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0049(self):
        '''
        我的团队-精确搜索
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('13800138005')
        time.sleep(3)
        els = lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els) == 1)
        lcontact.page_contain_element(text='联系人头像')
        lcontact.page_should_contain_text('大佬1')


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0056(self):
        '''
        搜索我的团队联系人结果展示
        author:darcy

        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('138005')
        lcontact.page_contain_element(text='列表项')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0051(self):
        '''
        我的团队-数字模糊搜索
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('138')
        time.sleep(3)
        els = lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els) > 1)
        lcontact.page_contain_element(text='联系人头像')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0052(self):
        '''
        我的团队-数字精确搜索
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('13800138005')
        time.sleep(3)
        els = lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els) == 1)
        lcontact.page_contain_element(text='联系人头像')
        lcontact.page_should_contain_text('大佬1')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0053(self):
        '''
        我的团队-中文模糊搜索
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('大佬')
        time.sleep(3)
        els = lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els) > 1)
        lcontact.page_contain_element(text='联系人头像')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0053(self):
        '''
        我的团队-英文模糊搜索
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('dalao')
        time.sleep(3)
        els = lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els) > 1)
        lcontact.page_contain_element(text='联系人头像')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0054(self):
        '''
        我的团队-非法字符搜索
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('#')
        time.sleep(3)
        els = lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els) > 1)
        lcontact.page_contain_element(text='联系人头像')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0060(self):
        '''
        我的团队长ID企业-中文模糊搜索
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('大佬1')
        time.sleep(3)
        els = lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els) == 1)
        lcontact.page_contain_element(text='联系人头像')
        lcontact.page_should_contain_text('大佬1')
        lcontact.page_should_contain_text('13800138005')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0063(self):
        '''
        点击搜索结果已保存到本地的RCS用户进入Profile页
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('sim联系人')
        time.sleep(3)
        els = lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els) == 1)
        lcontact.page_contain_element(text='联系人头像')
        lcontact.page_should_contain_text('大佬1')
        lcontact.page_should_contain_text('13800138005')


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0148(self):
        """进入我的团队用户的Profile页-消息"""
        # 添加联系人是星标联系人
        ContactsPage().select_contacts_by_name('测试2')
        glp = GroupListPage()
        ContactDetailsPage().click_message_icon()
        time.sleep(2)
        if ChatWindowPage().is_text_present("用户须知"):
            # 如果存在用户须知,就点击已阅读,然后点击返回.如果不存在,就直接点击返回
            ChatWindowPage().click_already_read()
            ChatWindowPage().click_sure_icon()
        SingleChatPage().is_on_this_page()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0150(self):
        """进入我的团队用户的Profile页-电话"""
        ContactsPage().select_contacts_by_name('测试2')
        cdp = ContactDetailsPage()
        cdp.click_call_icon()
        cdp.click_calling()
        time.sleep(4)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0151(self):
        """进入我的团队RCS用户的Profile页-语音通话"""
        ContactsPage().select_contacts_by_name('测试2')
        cdp = ContactDetailsPage()
        cdp.click_voice_call_icon()
        time.sleep(3)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0152(self):
        """进入我的团队RCS用户的Profile页-视频通话"""
        ContactsPage().select_contacts_by_name('测试2')
        cdp = ContactDetailsPage()
        cdp.click_video_call_icon()
        # if cdp.is_text_present('"和飞信"想访问您的相机'):
        #     cdp.
        time.sleep(3)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0153(self):
        """进入我的团队非RCS用户的Profile页-语音通话"""
        ContactsPage().select_contacts_by_name('测试2')
        cdp = ContactDetailsPage()
        cdp.click_voice_call_icon()
        time.sleep(3)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0154(self):
        """进入我的团队非RCS用户的Profile页-视频通话"""
        ContactsPage().select_contacts_by_name('测试2')
        cdp = ContactDetailsPage()
        cdp.click_video_call_icon()
        # if cdp.is_text_present('"和飞信"想访问您的相机'):
        #     cdp.
        time.sleep(3)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0155(self):
        """本网登录用户进入我的团队用户的Profile页-首次拨打和飞信电话"""
        ContactsPage().select_contacts_by_name('测试2')
        cdp = ContactDetailsPage()
        cdp.click_hefeixin_call_menu()
        time.sleep(3)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0156(self):
        """本网登录用户进入我的团队用户的Profile页-非首次拨打和飞信电话"""
        ContactsPage().select_contacts_by_name('测试2')
        cdp = ContactDetailsPage()
        cdp.click_hefeixin_call_menu()
        # if cdp.is_text_present('"和飞信"想访问您的相机'):
        #     cdp.
        time.sleep(3)

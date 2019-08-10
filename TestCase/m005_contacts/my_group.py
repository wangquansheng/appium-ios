import unittest
import uuid
import time
import warnings

from pages.contacts.AllMyTeam import AllMyTeamPage
from preconditions.BasePreconditions import WorkbenchPreconditions
from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *


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


class ShareContactpage(TestCase):
    """分享名片"""

    def default_setUp(self):
        """用户已进入分享名片的联系人选择器"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        MessagePage().wait_for_page_load()
        MessagePage().click_contacts()
        ContactsPage().click_phone_contact()
        ContactsPage().select_contacts_by_name("大佬2")
        ContactDetailsPage().click_share_card_icon()

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0196(self):
        """在联系人选择器页面，选择一个群"""
        scp = SelectContactsPage()
        # 1.点击选择一个群
        scp.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        # 2.搜索框文本显示'搜索群组'
        sog.is_text_present('搜索群组')
        # 3.不存在搜索结果时,显示"无搜索结果
        sog.input_search_keyword('wanduzi')
        self.assertTrue(sog.page_should_contain_text2('无搜索结果'))
        # 4.存在搜索结果时，显示搜索结果
        sog.input_search_keyword('群聊1')
        time.sleep(2)
        self.assertTrue(sog.is_element_present_result())
        # 5.点击搜索结果
        sog.click_search_result()
        # 6.点击发送名片
        time.sleep(1)
        sog.click_accessibility_id_attribute_by_name("发送名片")

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0197(self):
        """在联系人选择器页面，选择一个群"""
        scp = SelectContactsPage()
        # 1.点击选择一个群
        scp.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        # 2.根据名字选择一个群
        sog.selecting_one_group_by_name("群聊2")
        # 3.点击发送名片
        time.sleep(1)
        sog.click_accessibility_id_attribute_by_name("发送名片")

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0198(self):
        """在联系人选择器页面，选择本地联系人"""
        scp = SelectContactsPage()
        self.assertTrue(scp.page_should_contain_text2("选择联系人"))
        # 1.点击选择手机联系人
        scp.click_phone_contacts()
        scl = SelectLocalContactsPage()
        scl.wait_for_page_load()
        # 2.搜索不存在结果
        scl.input_search_keyword("wanduzi")
        self.assertTrue(scl.page_should_contain_text2('无搜索结果'))
        # 3.搜索存在结果
        scl.input_search_keyword("大佬3")
        # 4.点击搜索结果
        scl.click_search_result()
        # 5.点击发送名片
        time.sleep(1)
        scl.click_accessibility_id_attribute_by_name("发送名片")

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0199(self):
        """在联系人选择器页面，选择本地联系人"""
        scp = SelectContactsPage()
        # 1.点击选择手机联系人
        scp.click_phone_contacts()
        scl = SelectLocalContactsPage()
        scl.wait_for_page_load()
        # 2.根据名字搜索联系人
        scl.selecting_local_contacts_by_name("大佬3")
        # 3.点击发送名片
        time.sleep(1)
        scl.click_accessibility_id_attribute_by_name("发送名片")

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0208(self):
        """在联系人选择器页面，搜索联系人"""
        scp = SelectContactsPage()
        # 1.点击选择手机联系人
        scp.click_phone_contacts()
        scl = SelectLocalContactsPage()
        scl.wait_for_page_load()
        # 2.搜索存在结果
        scl.input_search_keyword("大佬")
        # 3.点击搜索结果
        scl.click_search_result()
        # 4.点击发送名片
        time.sleep(1)
        scl.click_accessibility_id_attribute_by_name("发送名片")

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0209(self):
        """在联系人选择器页面，选择最近聊天联系人"""
        scp = SelectContactsPage()
        # 1.点击选择手机联系人
        scp.click_phone_contacts()
        scl = SelectLocalContactsPage()
        scl.wait_for_page_load()
        # 2.根据名字搜索联系人
        scl.selecting_local_contacts_by_name("大佬3")
        # 3.点击发送名片
        time.sleep(1)
        scl.click_accessibility_id_attribute_by_name("发送名片")
        # 4.点击分享名片
        ContactDetailsPage().click_share_card_icon()
        # 5.选择最近联系人
        scp.click_recent_chat_contact()
        # 6.确定分享
        time.sleep(1)
        scp.click_accessibility_id_attribute_by_name("发送名片")

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0210(self):
        """在联系人选择器页面，选择最近聊天群聊"""
        scp = SelectContactsPage()
        # 1.点击选择一个群
        scp.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        # 2.根据名字选择一个群
        sog.selecting_one_group_by_name("群聊2")
        # 3.点击发送名片
        time.sleep(1)
        sog.click_accessibility_id_attribute_by_name("发送名片")
        # 4.点击分享名片
        ContactDetailsPage().click_share_card_icon()
        # 5.选择最近联系人
        scp.click_recent_chat_contact()
        # 6.确定分享
        time.sleep(1)
        scp.click_accessibility_id_attribute_by_name("发送名片")

    @tags('ALL','CMCC')
    def test_contacts_quxinli_0211(self):
        """在联系人选择器页面，搜索我的电脑"""
        scp = SelectContactsPage()
        scp.click_search_contact()
        scp.input_search_keyword('我的电脑')
        time.sleep(3)

    @tags('ALL','CMCC')
    def test_contacts_quxinli_0212(self):
        """在联系人选择器页面，搜索11位陌生号码"""
        scp = SelectContactsPage()
        # 1.点击搜索框输入11位陌生号码
        scp.click_search_contact()
        scp.input_search_keyword('13813813813')
        time.sleep(2)
        # 2.验证是否显示未知号码
        self.assertTrue(scp.page_should_contain_text2("未知号码"))
        self.assertTrue(scp.page_should_contain_text2("tel:+8613813813813"))


class myGroupContacts(TestCase):
    """通讯录-我的团队"""

    class SearchLocalContacts(TestCase):
        """
        搜索-我的团队-曲新莉

        """

    @classmethod
    def setUpClass(cls):
        """删除消息列表的消息记录"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        # 创建团队ateam7272
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        Preconditions.create_team_if_not_exist_and_set_as_defalut_team()
        # 导入团队联系人、企业部门
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
                                  ('陈丹丹', "13800137004"), ('alice', "13800137005"), ('郑海', "13802883296")]
                Preconditions.create_he_contacts2(contact_names2)
                department_names = ["测试部门1", "测试部门2"]
                Preconditions.create_department_and_add_member(department_names)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

    def default_setUp(self):
        """确保每个用例运行前在我的团队页面"""
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load()
        MessagePage().click_contacts()
        ContactsPage().click_all_my_team()

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0049(self):
        '''
        我的团队-精确搜索
        auther:darcy
        :return:
        '''
        amt = AllMyTeamPage()
        time.sleep(10)
        # lcontact = ContactsPage()
        # lcontact.click_search_phone_contact()
        # time.sleep(1)
        # lcontact.input_search_keyword('13800138005')
        # time.sleep(3)
        # els = lcontact.get_page_elements(text='列表项')
        # self.assertTrue(len(els) == 1)
        # lcontact.page_contain_element(text='联系人头像')
        # lcontact.page_should_contain_text('大佬1')


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

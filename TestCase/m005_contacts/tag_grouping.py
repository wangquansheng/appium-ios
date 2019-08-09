import unittest
import uuid
from library.core.common.simcardtype import CardType
import time

from pages.chat.ChatGroupSMSExpenses import ChatGroupSMSExpensesPage
from preconditions.BasePreconditions import LoginPreconditions
from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.contacts.EditContactPage import EditContactPage
from pages.contacts.local_contact import localContactPage
import preconditions
from dataproviders import contact2
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


class TagGrouping(TestCase):
    """标签分组"""

    def default_setUp(self):
        """确保每个用例执行前在标签分组页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        MessagePage().click_contacts()
        time.sleep(2)
        ContactsPage().click_phone_contact()
        ContactsPage().click_label_grouping()
        LabelGroupingPage().delete_all_label()

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    def test_contacts_quxinli_0352(self):
        lg = LabelGroupingPage()
        lg.delete_all_label()
        lg.page_should_contain_text('标签分组')
        lg.page_should_contain_text('新建分组')
        lg.page_should_contain_text('暂无分组')


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0353(self):
        """新建分组"""
        lg=LabelGroupingPage()
        time.sleep(2)
        lg.click_new_create_group()
        time.sleep(4)
        lg.page_should_contain_text('为你的分组创建一个名称')
        lg.page_should_contain_text('请输入标签分组名称')
        lg.page_should_contain_text('新建分组')
        lg.page_contain_element(text='确定')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0355(self):
        """新建分组,标签分组名称输入空格"""
        lg = LabelGroupingPage()
        text = ' '
        lg.click_new_create_group()
        time.sleep(1)
        lg.click_input_box()
        time.sleep(1)
        lg.input_search_text(text)
        lg.click_sure()
        SelectContactsPage().check_if_element_not_exist(text='搜索或输入手机号')


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0356(self):
        """新建分组,标签分组名称输入9个汉字"""
        lg = LabelGroupingPage()
        text = '祝一路顺风幸福美满'
        # GroupListPage().delete_group(name=text)
        lg.click_new_create_group()
        time.sleep(1)
        lg.click_input_box()
        time.sleep(1)
        lg.input_search_text(text)
        lg.click_sure()
        time.sleep(2)
        self.assertTrue(SelectContactsPage().is_element_present(locator='搜索或输入手机号'))

    @tags('ALL', 'debug', 'CMCC')
    def tearDown_test_contacts_quxinli_0356(self):
        SelectContactsPage().click_back()
        time.sleep(1)
        LabelGroupingPage().click_back()
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])



    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0357(self):
        """新建分组,标签分组名称输入10个汉字"""
        GroupPage = GroupListPage()
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(3)
        GroupPage.input_content(text="祝一路顺风和幸福美满")
        GroupPage.click_sure_element()
        GroupPage.click_allow_button()
        self.assertTrue(SelectContactsPage().is_element_present(locator='搜索或输入手机号'))

    def tearDown_test_contacts_quxinli_0357(self):
        SelectContactsPage().click_back()
        LabelGroupingPage().click_back()
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0358(self):
        """新建分组,标签分组名称输入11个汉字"""
        GroupPage = GroupListPage()
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(3)
        GroupPage.input_content(text="祝一路顺风和幸福美满啊")
        GroupPage.click_sure_element()
        GroupPage.click_allow_button()
        self.assertTrue(SelectContactsPage().is_element_present(locator='搜索或输入手机号'))

    def tearDown_test_contacts_quxinli_0358(self):
        SelectContactsPage().click_back()
        LabelGroupingPage().click_back()
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0359(self):
        """新建分组,标签分组名称输入29个数字"""
        GroupPage = GroupListPage()
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(3)
        self.group='1'*29
        GroupPage.input_content(text=self.group)
        GroupPage.click_sure_element()
        GroupPage.click_allow_button()
        self.assertTrue(SelectContactsPage().is_element_present(locator='搜索或输入手机号'))

    def tearDown_test_contacts_quxinli_0359(self):
        SelectContactsPage().click_back()
        LabelGroupingPage().click_back()
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0360(self):
        """新建分组,标签分组名称输入30个数字"""
        GroupPage = GroupListPage()
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(3)
        self.group='1'*30
        GroupPage.input_content(text=self.group)
        GroupPage.click_sure_element()
        GroupPage.click_allow_button()
        self.assertTrue(SelectContactsPage().is_element_present(locator='搜索或输入手机号'))

    def tearDown_test_contacts_quxinli_0360(self):
        SelectContactsPage().click_back()
        LabelGroupingPage().click_back()
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0361(self):
        """新建分组,标签分组名称输入31个数字"""
        GroupPage = GroupListPage()
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(3)
        self.group = '1'*31
        GroupPage.input_content(text=self.group)
        time.sleep(2)
        text = GroupPage.get_input_box_text()
        self.assertNotEqual(text, self.group)
        GroupPage.click_sure_element()
        GroupPage.click_allow_button()
        time.sleep(2)
        SelectContactsPage().check_if_element_exist(text='搜索或输入手机号')

    def tearDown_test_contacts_quxinli_0361(self):
        SelectContactsPage().click_back()
        LabelGroupingPage().click_back()
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0362(self):
        """新建分组,标签分组名称输入29个字母"""
        GroupPage = GroupListPage()
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(3)
        self.group='a'*29
        GroupPage.input_content(text=self.group)
        GroupPage.click_sure_element()
        GroupPage.click_allow_button()
        self.assertTrue(SelectContactsPage().is_element_present(locator='搜索或输入手机号'))

    def tearDown_test_contacts_quxinli_0362(self):
        SelectContactsPage().click_back()
        LabelGroupingPage().click_back()
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0363(self):
        """新建分组,标签分组名称输入30个字母"""
        GroupPage = GroupListPage()
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(3)
        self.group='a'*30
        GroupPage.input_content(text=self.group)
        GroupPage.click_sure_element()
        GroupPage.click_allow_button()
        self.assertTrue(SelectContactsPage().is_element_present(locator='搜索或输入手机号'))

    def tearDown_test_contacts_quxinli_0363(self):
        SelectContactsPage().click_back()
        time.sleep(1)
        LabelGroupingPage().click_back()
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0364(self):
        """新建分组,标签分组名称输入31个字母"""
        GroupPage = GroupListPage()
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(3)
        self.group='a'*31
        GroupPage.input_content(text=self.group)
        GroupPage.click_sure_element()
        GroupPage.click_allow_button()
        self.assertTrue(SelectContactsPage().is_element_present(locator='搜索或输入手机号'))

    def tearDown_test_contacts_quxinli_0364(self):
        SelectContactsPage().click_back()
        time.sleep(1)
        LabelGroupingPage().click_back()
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'debug', 'CMCC')
    def test_contacts_quxinli_0365(self):
        """新建分组,标签分组名称输入29个字符：汉字、数字、英文字母、空格和特殊字符组合"""
        lg = LabelGroupingPage()
        lg.click_new_create_group()
        time.sleep(1)
        lg.click_input_box()
        time.sleep(1)
        text = 'aa111@@@文 aaa111@@@文 aaaa'
        lg.input_search_text(text)
        lg.click_sure()
        self.assertTrue(SelectContactsPage().is_element_present(locator='搜索或输入手机号'))

    @tags('ALL', 'debug', 'CMCC')
    def tearDown_test_contacts_quxinli_0365(self):
        SelectContactsPage().click_back()
        LabelGroupingPage().click_back()
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'debug', 'CMCC')
    def test_contacts_quxinli_0366(self):
        """新建分组,标签分组名称输入30个字符：汉字、数字、英文字母、空格和特殊字符组合"""
        lg = LabelGroupingPage()
        lg.click_new_create_group()
        time.sleep(1)
        lg.click_input_box()
        time.sleep(1)
        text = 'aa111@@@文 aaa111@@@文 aaaaa'
        lg.input_search_text(text)
        lg.click_sure()
        self.assertTrue(SelectContactsPage().is_element_present(locator='搜索或输入手机号'))

    @tags('ALL', 'debug', 'CMCC')
    def tearDown_test_contacts_quxinli_0366(self):
        SelectContactsPage().click_back()
        LabelGroupingPage().click_back()
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0367(self):
        """新建分组,标签分组名称输入31个字符：汉字、数字、英文字母、空格和特殊字符组合"""
        GroupPage = GroupListPage()
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(3)
        self.group='aa111@@@文 aaa111@@@文 aaaaaa'
        GroupPage.input_content(text=self.group)
        GroupPage.click_sure_element()
        GroupPage.click_allow_button()
        self.assertTrue(SelectContactsPage().is_element_present(locator='搜索或输入手机号'))

    def tearDown_test_contacts_quxinli_0367(self):
        SelectContactsPage().click_back()
        LabelGroupingPage().click_back()
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0371(self):
        """新建分组,分组详情操作界面"""

        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.new_group()
        time.sleep(1)
        LabelGroupingPage().click_first_lable_group()
        time.sleep(2)
        detail = LableGroupDetailPage()
        detail.click_cancel()
        time.sleep(1)
        GroupPage.page_contain_element()
        GroupPage.page_contain_element('群发消息')
        GroupPage.page_contain_element('飞信电话')
        GroupPage.page_contain_element('多方视频')
        GroupPage.page_contain_element('设置')
        # GroupPage.page_contain_element('aaa')

    def tearDown_test_contacts_quxinli_0371(self):
        LabelGroupingPage().click_back()
        time.sleep(1)
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0372(self):
        """新建分组,标签分组添加成员页面"""

        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.new_group()
        time.sleep(1)
        LabelGroupingPage().click_first_lable_group()
        time.sleep(2)
        LableGroupDetailPage().click_add_contact()
        time.sleep(1)
        GroupPage.page_contain_element('选择联系人标题')
        GroupPage.page_contain_element('搜索或输入手机号2')
        GroupPage.page_contain_element('联系人头像1')
        GroupPage.page_contain_element('确定')


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0373(self):
        """标签分组添加成员-搜索结果页面"""
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.creat_group()
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail=LableGroupDetailPage()
        detail.click_add_contact()
        time.sleep(1)
        #搜索框输入搜索文本
        select=SelectContactsPage()
        select.click_search_box()
        select.input_search_text(text='测试')
        select.check_if_element_exist(text='联系人列表')
        select.check_if_element_exist(text='清空搜索文本')
        #清空搜索文本
        select.click_x_icon()
        time.sleep(1)
        select.check_if_element_not_exist(text='清空搜索文本')
        #点击搜索结果
        select.input_search_text(text='测试')
        select.page_down()
        time.sleep(1)
        select.click_search_result()
        time.sleep(2)
        select.check_if_element_exist(text='已选择的联系人')
        select.check_if_element_not_exist(text='清空搜索文本')
        #点击搜索结果中已选择的联系人
        select.click_contact_which_is_selecd()
        time.sleep(2)
        select.check_if_element_not_exist(text='已选择的联系人')

    def tearDown_test_contacts_quxinli_0373(self):
        select=SelectContactsPage()
        select.click_back()
        LableGroupDetailPage().click_back()
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0374(self):
        """标签分组添加成员-搜索陌生号码"""
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.creat_group()
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail=LableGroupDetailPage()
        detail.click_add_contact()
        time.sleep(1)
        LabelGroupingPage()
        #搜索框输入陌生联系人 不显示搜索结果
        select=SelectContactsPage()
        select.click_search_box()
        text='13802885230'
        select.input_search_text(text)
        time.sleep(3)
        select.check_if_element_not_exist(text='联系人列表')

    def tearDown_test_contacts_quxinli_0374(self):
        select=SelectContactsPage()
        select.click_back()
        select.click_back()
        LableGroupDetailPage().click_back()
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0375(self):
        """标签分组添加成员-选择本地联系人"""
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.creat_group()
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail=LableGroupDetailPage()
        detail.click_add_contact()
        time.sleep(1)
        #点击本地联系人
        select=SelectContactsPage()
        select.select_one_contact_by_name('大佬1')
        #点击已选择的联系人
        select.click_contact_which_is_selecd()
        time.sleep(1)
        select.check_if_element_not_exist(text='已选择的联系人')
        #点击两次键盘的删除键（暂时无法实现）

    def tearDown_test_contacts_quxinli_0375(self):
        select=SelectContactsPage()
        select.click_back()
        LableGroupDetailPage().click_back()
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @staticmethod
    def setUp_test_contacts_quxinli_0376():
        Preconditions.select_mobile('IOS-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        #预置联系人本机
        con=ContactsPage()
        con.click_phone_contact()
        con.click_search_phone_contact()
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)
        con.input_search_keyword(phone_number)
        if con.is_element_present_by_id('本地联系人搜索结果'):
            con.click_back()
        else:
            con.click_add()
            time.sleep(2)
            creat=CreateContactPage()
            creat.click_input_name()
            creat.input_name('本机')
            creat.click_input_number()
            creat.input_number(phone_number[0])
            creat.click_save()
            time.sleep(2)
            ContactDetailsPage().click_back()
            con.click_back()
        #进入标签分组页面
        con.click_phone_contact()
        time.sleep(2)
        con.click_label_grouping()
        time.sleep(2)


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0376(self):
        """标签分组添加成员-选择本地联系人不可选成员"""
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.creat_group()
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail=LableGroupDetailPage()
        detail.click_add_contact()
        time.sleep(1)
        #选择自己
        select=SelectContactsPage()
        select.select_one_contact_by_name('本机')
        time.sleep(2)
        select.check_if_element_not_exist(text='已选择的联系人')
        #选择联系人中的无号码联系人（无手机号联系人暂时无法创建）

    def tearDown_test_contacts_quxinli_0376(self):
        select = SelectContactsPage()
        select.click_back()
        LableGroupDetailPage().click_back()
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0388(self):
        """分组详情操作界面-分组只有一个人员点击群发消息"""
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.creat_group()
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail = LableGroupDetailPage()
        detail.click_add_contact()
        time.sleep(1)
        # 选择自己
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬1')
        select.click_sure_bottom()
        #进入群发消息页面
        time.sleep(2)
        detail.click_send_group_info()
        chat=ChatWindowPage()
        time.sleep(2)
        chat.page_should_contain_text('大佬1')
        self.assertTrue(chat.is_on_this_page())


    def tearDown_test_contacts_quxinli_0388(self):
        ChatWindowPage().click_back()
        LableGroupDetailPage().click_back()
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0389(self):
        """分组详情操作界面-分组有多个人员点击群发消息"""
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.creat_group()
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail = LableGroupDetailPage()
        detail.click_add_contact()
        time.sleep(1)
        # 选择多个联系人
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬1')
        time.sleep(1)
        select.select_one_contact_by_name('大佬2')
        select.click_sure_bottom()
        time.sleep(2)
        #进入群发消息页面  验证页面元素
        detail.click_send_group_info()
        lable_chat=LabelGroupingChatPage()
        time.sleep(3)
        self.assertTrue(lable_chat.is_on_this_page())
        self.assertTrue(lable_chat.is_exit_element(text='多方通话'))
        self.assertTrue(lable_chat.is_exit_element(text='设置'))


    def tearDown_test_contacts_quxinli_0389(self):
        LabelGroupingChatPage().click_back()
        LableGroupDetailPage().click_back()
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])



    @tags('ALL', 'CONTACT', 'CMCC-')
    def test_contacts_quxinli_0390(self):
        """分组详情操作界面-群发消息-发送消息"""
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.creat_group()
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail = LableGroupDetailPage()
        detail.click_add_contact()
        time.sleep(1)
        # 选择多个联系人
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬1')
        time.sleep(1)
        select.select_one_contact_by_name('大佬2')
        select.click_sure_bottom()
        time.sleep(2)
        #进入群发消息页面
        detail.click_send_group_info()
        lable_chat=LabelGroupingChatPage()
        time.sleep(3)
        #发送纯文本
        text='消息'
        lable_chat.input_message_text(text)
        lable_chat.click_send_button()
        time.sleep(3)
        self.assertFalse(lable_chat.is_element_present_resend())
        # 发送长文本
        text = '消息'*20
        lable_chat.input_message_text(text)
        lable_chat.click_send_button()
        time.sleep(3)
        self.assertFalse(lable_chat.is_element_present_resend())
        # 发送文本加空格
        text = '消    息'
        lable_chat.input_message_text(text)
        lable_chat.click_send_button()
        time.sleep(3)
        self.assertFalse(lable_chat.is_element_present_resend())
        # 发送表情
        text = '[微笑1]'
        lable_chat.input_message_text(text)
        lable_chat.click_send_button()
        time.sleep(3)
        self.assertFalse(lable_chat.is_element_present_resend())
        # 发送文字+表情
        text = '[微笑1]笑脸'
        lable_chat.input_message_text(text)
        lable_chat.click_send_button()
        time.sleep(3)
        self.assertFalse(lable_chat.is_element_present_resend())
        #发送文件
        lable_chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_local_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('docx')
        local_file.click_send_button()
        time.sleep(2)
        self.assertFalse(lable_chat.is_element_present_resend())
        #发送图片
        lable_chat.click_file()
        csf = ChatSelectFilePage()
        csf.click_pic()
        select_pic = ChatPicPage()
        select_pic.click_camara_picture()
        select_pic.select_first_picture()
        select_pic.click_send()
        self.assertFalse(lable_chat.is_element_present_resend())
        #发送视频
        lable_chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_video()
        time.sleep(2)
        csf.click_select_video()
        #发送名片
        time.sleep(2)
        lable_chat.click_more()
        lable_chat.click_name_card()
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬2')
        time.sleep(1)
        select.click_share_card()
        time.sleep(2)
        self.assertFalse(lable_chat.is_element_present_resend())
        #发送位置
        time.sleep(2)
        lable_chat.click_more()
        lable_chat.click_locator()
        time.sleep(2)
        locator = ChatLocationPage()
        locator.wait_for_page_load()
        locator.click_send()
        time.sleep(2)
        self.assertFalse(lable_chat.is_element_present_resend())
        #不能发送红包
        time.sleep(2)
        lable_chat.click_more()
        self.assertFalse(lable_chat.is_exit_element(text='红包'))


    def tearDown_test_contacts_quxinli_0390(self):
        LabelGroupingChatPage().click_back()
        LableGroupDetailPage().click_back()
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0394(self):
        """分组联系人进入Profile页-星标"""
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.creat_group()
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail = LableGroupDetailPage()
        detail.click_add_contact()
        time.sleep(1)
        # 选择多个联系人
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬1')
        time.sleep(1)
        select.select_one_contact_by_name('大佬2')
        select.click_sure_bottom()
        time.sleep(2)
        #进入群发页面
        detail.click_send_group_info()
        lable_chat = LabelGroupingChatPage()
        time.sleep(3)
        lable_chat.click_setting()
        lable_chat.select_group_contact_by_name('大佬1')
        time.sleep(2)
        #进入联系人详情页面
        contact_detail=ContactDetailsPage()
        contact_detail.click_star_icon()
        time.sleep(2)
        #进入手机通讯录页面
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().click_phone_contact()
        ContactsPage().page_contain_element(text='星标')


    def tearDown_test_contacts_quxinli_0394(self):
        #去除大佬1的星标
        ContactsPage().select_contacts_by_name('大佬1')
        ContactDetailsPage().click_yellow_star_icon()
        time.sleep(1)
        #删除群组
        ContactDetailsPage().click_back_button()
        time.sleep(2)
        ContactsPage().click_label_grouping()
        time.sleep(1)
        LabelGroupingPage().delete_label_groups()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0395(self):
        """分组联系人进入Profile页-编辑"""
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.creat_group()
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail = LableGroupDetailPage()
        detail.click_add_contact()
        time.sleep(1)
        # 选择多个联系人
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬1')
        time.sleep(1)
        select.select_one_contact_by_name('大佬2')
        select.click_sure_bottom()
        time.sleep(2)
        #进入群发页面-分组联系人
        detail.click_send_group_info()
        lable_chat = LabelGroupingChatPage()
        time.sleep(3)
        lable_chat.click_setting()
        lable_chat.select_group_contact_by_name('大佬1')
        # 进入联系人详情页面
        contact_detail = ContactDetailsPage()
        contact_detail.click_edit_contact()
        edit=EditContactPage()
        edit.input_company('中软国际')
        edit.click_sure()
        time.sleep(2)
        contact_detail.page_should_contain_text('中软国际')

    def tearDown_test_contacts_quxinli_0395(self):
        # 恢复环境
        if not ContactDetailsPage().is_on_this_page():
            Preconditions.make_already_in_message_page()
            MessagePage().open_contacts_page()
            ContactsPage().click_phone_contact()
            ContactsPage().select_contacts_by_name('大佬1')
            time.sleep(2)
        ContactDetailsPage().click_edit_contact()
        time.sleep(1)
        EditContactPage().click_input_company()
        EditContactPage().input_company(' ')
        time.sleep(1)
        EditContactPage().click_sure()
        time.sleep(2)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0396(self):
        """分组联系人进入Profile页-编辑-删除联系人"""
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.creat_group()
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail = LableGroupDetailPage()
        detail.click_add_contact()
        time.sleep(1)
        # 选择多个联系人
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬1')
        time.sleep(1)
        select.select_one_contact_by_name('大佬2')
        select.click_sure_bottom()
        time.sleep(2)
        #进入群发页面-分组联系人
        detail.click_send_group_info()
        lable_chat = LabelGroupingChatPage()
        time.sleep(3)
        lable_chat.click_setting()
        lable_chat.select_group_contact_by_name('大佬1')
        # 进入联系人详情页面
        contact_detail = ContactDetailsPage()
        contact_detail.click_edit_contact()
        edit=EditContactPage()
        edit.click_delete_contact()
        edit.click_sure_delete()
        time.sleep(1)
        ContactsPage().page_should_not_contain_text('大佬1')


    def tearDown_test_contacts_quxinli_0396(self):
        #添加联系人
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().click_phone_contact()
        ContactsPage().click_add()
        creat=CreateContactPage()
        creat.create_contact('大佬1','13800138005')
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACT', '多方通话-跳过')
    def test_contacts_quxinli_0397(self):
        """“分组详情操作”界面-多方电话"""
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.creat_group()
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail = LableGroupDetailPage()
        detail.click_add_contact()
        time.sleep(1)
        # 选择多个联系人
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬2')
        time.sleep(1)
        select.select_one_contact_by_name('大佬3')
        select.click_sure_bottom()
        time.sleep(2)
        #进入飞信电话
        detail.click_multi_tel()
        time.sleep(1)
        detail.click_text('大佬2')
        detail.click_to_call()
        detail.call_box_processing()
        # detail.wait_for_page_load()


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0398(self):
        """“分组详情操作”界面-多方视频"""
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.creat_group()
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail = LableGroupDetailPage()
        detail.click_add_contact()
        time.sleep(1)
        # 选择多个联系人
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬2')
        time.sleep(1)
        select.select_one_contact_by_name('大佬3')
        select.click_sure_bottom()
        time.sleep(2)
        #点击多方视频
        detail.click_multiparty_videos()
        time.sleep(1)
        detail.click_text('大佬2')
        detail.click_to_call()
        detail.video_call_box_processing()



    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0407(self):
        """“分组设置-特殊符号标签名称
        auther:darcy
        """
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.creat_group()
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail = LableGroupDetailPage()
        detail.click_cancel()
        detail.open_setting_menu()
        detail.change_lable_group_name(name='*@!#')
        #名称修改成功
        time.sleep(2)
        detail.page_should_contain_text('*@!#')


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0408(self):
        """“分组设置-各种标签名称
        auther:darcy
        """
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.creat_group()
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail = LableGroupDetailPage()
        detail.click_cancel()
        detail.open_setting_menu()
        detail.change_lable_group_name(name='*@!#123好')
        # 名称修改成功
        time.sleep(2)
        GroupPage.page_should_contain_text(text='*@!#123好')


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0409(self):
        """“分组设置-各种标签名称删除
        auther:darcy
        """
        #进入标签分组设置界面
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.creat_group()
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail = LableGroupDetailPage()
        detail.click_cancel()
        detail.open_setting_menu()
        #点击进入修改标签名称页面
        detail.click_chang_lable_group_name()
        detail.page_should_contain_text('修改标签名称')
        #修改名称能正常输入英文 能正常清空输入框
        text='bbb'
        detail.input_group_new_name(name=text)
        detail.page_should_contain_text(text)
        detail.clear_group_name()
        detail.page_should_contain_text('请输入标签分组名称')
        # 修改名称能正常输入中文 能正常清空输入框
        text = '新名字'
        detail.input_group_new_name(name=text)
        detail.page_should_contain_text(text)
        detail.clear_group_name()
        detail.page_should_contain_text('请输入标签分组名称')
        # 修改名称能正常输入数字 能正常清空输入框
        text = '123'
        detail.input_group_new_name(name=text)
        detail.page_should_contain_text(text)
        detail.clear_group_name()
        detail.page_should_contain_text('请输入标签分组名称')
        # 修改名称能正常输入符号 能正常清空输入框
        text = '。。。'
        detail.input_group_new_name(name=text)
        detail.page_should_contain_text(text)
        detail.clear_group_name()
        detail.page_should_contain_text('请输入标签分组名称')
        # 修改名称能正常输入特殊符号 能正常清空输入框
        text = '#@'
        detail.input_group_new_name(name=text)
        detail.page_should_contain_text(text)
        detail.clear_group_name()
        detail.page_should_contain_text('请输入标签分组名称')
        # 修改名称能正常输入表情 能正常清空输入框
        text = '[微笑1]'
        detail.input_group_new_name(name=text)
        detail.page_should_contain_text(text)
        detail.clear_group_name()
        detail.page_should_contain_text('请输入标签分组名称')


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0412(self):
        """分组设置-移除成员选择
        auther:darcy
        """
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.creat_group()
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail = LableGroupDetailPage()
        detail.click_add_contact()
        time.sleep(1)
        # 选择多个联系人
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬2')
        time.sleep(1)
        select.select_one_contact_by_name('大佬3')
        select.click_sure_bottom()
        time.sleep(2)
        #移除成员
        detail.open_setting_menu()
        detail.click_move_label_contact()
        name='大佬2'
        detail.move_label_contact_first_name()
        detail.click_sure()
        detail.page_should_not_contain_text(name)


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0414(self):
        """分组设置-搜索移除成员
        auther:darcy
        """
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.creat_group()
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail = LableGroupDetailPage()
        detail.click_add_contact()
        time.sleep(1)
        # 选择多个联系人
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬2')
        time.sleep(1)
        select.select_one_contact_by_name('大佬3')
        select.click_sure_bottom()
        time.sleep(2)
        # 移除成员
        detail.open_setting_menu()
        detail.click_move_label_contact()
        name = '大佬2'
        detail.click_search_box_move_label_contact()
        detail.input_search_text_move_lable(name)
        detail.move_label_contact_first_name()
        detail.click_sure()
        time.sleep(2)
        #判断成员移除成功
        detail.clear_search_text()
        self.assertFalse(detail.is_text_present(name))


    @tags('ALL', 'CONTACT-debug', 'CMCC')
    def test_contacts_quxinli_0415(self):
        """分组设置-删除标签
        auther:darcy
        """
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.creat_group()
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail = LableGroupDetailPage()
        detail.click_cancel()
        #删除标签分组
        detail.open_setting_menu()
        detail.delete_lable_group()
        self.assertTrue(detail.is_exit_element(text='取消'))
        self.assertTrue(detail.is_exit_element(text='删除'))
        #点击取消 弹窗关闭
        detail.click_cancel_delete()
        self.assertFalse(detail.is_exit_element(text='删除'))
        #点击确定
        detail.delete_lable_group()
        time.sleep(1)
        detail.click_sure_delete()
        time.sleep(2)
        LabelGroupingPage().page_should_contain_text('新建分组')


    # @tags('ALL', 'CONTACT-debug', 'CMCC')
    # def test_contacts_quxinli_0416(self):
    #     """分组详情操作页面进入Profile页"""
    #     GroupPage = LabelGroupingPage()
    #     time.sleep(1)
    #     GroupPage.delete_all_label()
    #     GroupPage.creat_group()
    #     LabelGroupingPage().click_first_lable_group()
    #     time.sleep(1)
    #     detail = LableGroupDetailPage()
    #     detail.click_add_contact()
    #     time.sleep(1)
    #     # 选择多个联系人
    #     select = SelectContactsPage()
    #     select.select_one_contact_by_name('大佬2')
    #     time.sleep(1)
    #     select.select_one_contact_by_name('大佬3')
    #     select.click_sure_bottom()
    #     time.sleep(2)
    #     #选择任意一个联系人
    #     detail.click_text('大佬2')
    #     time.sleep(2)
    #     contact_detail=ContactDetailsPage()
    #     self.assertTrue(contact_detail.is_exit_element(locator=''))
    #
    #

    @tags('ALL', 'CONTACT-debug', 'CMCC')
    def test_contacts_quxinli_0417(self):
        """分组详情操作页面进入Profile页_星标
        auther:darcy"""
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.creat_group()
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail = LableGroupDetailPage()
        detail.click_add_contact()
        time.sleep(1)
        # 选择多个联系人
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬2')
        time.sleep(1)
        select.select_one_contact_by_name('大佬3')
        select.click_sure_bottom()
        time.sleep(2)
        #选择任意一个联系人
        detail.click_text('大佬2')
        time.sleep(2)
        contact_detail=ContactDetailsPage()
        contact_detail.click_star_icon()
        #手机通讯录页面显示该用户
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().click_phone_contact()
        ContactsPage().page_contain_element(text='星标')


    def tearDown_test_contacts_quxinli_0417(self):
        # 去除大佬1的星标
        ContactsPage().select_contacts_by_name('大佬2')
        time.sleep(2)
        ContactDetailsPage().click_yellow_star_icon()
        time.sleep(1)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_quxinli_0392(self):
        """分组详情操作界面-群发消息-分组联系人图标"""
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        # 1.删除全部分组
        GroupPage.delete_all_label()
        # 2.创建分组
        GroupPage.creat_group()
        # 3.点击第一个分组
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail = LableGroupDetailPage()
        # 4.添加联系人
        detail.click_add_contact()
        time.sleep(1)
        # 5.选择多个联系人
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬2')
        time.sleep(1)
        select.select_one_contact_by_name('大佬3')
        select.click_sure_bottom()
        time.sleep(2)
        # 6.点击群发
        detail.click_send_group_info()
        # 7.点击右上角的分组联系人图标
        lable_chat = LabelGroupingChatPage()
        time.sleep(2)
        lable_chat.click_setting()
        time.sleep(2)
        # 8.验证是否显示头像，名字号码
        self.assertTrue(detail.is_exit_element("分组联系人头像"))
        self.assertTrue(detail.is_exit_element("分组联系人名字号码"))

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_quxinli_0393(self):
        """分组联系人进入Profile页"""
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        # 1.删除全部分组
        GroupPage.delete_all_label()
        # 2.创建分组
        GroupPage.creat_group()
        # 3.点击第一个分组
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail = LableGroupDetailPage()
        # 4.添加联系人
        detail.click_add_contact()
        time.sleep(1)
        # 5.选择多个联系人
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬2')
        time.sleep(1)
        select.select_one_contact_by_name('大佬3')
        select.click_sure_bottom()
        time.sleep(2)
        # 6.点击群发
        detail.click_send_group_info()
        # 7.验证是否在群发页面
        lable_chat = LabelGroupingChatPage()
        time.sleep(2)
        self.assertTrue(lable_chat.is_on_this_page())
        # 8.点击右上角的分组联系人图标
        lable_chat.click_setting()
        time.sleep(2)
        detail.click_text('大佬2')
        time.sleep(2)
        contact_detail = ContactDetailsPage()
        # 9.验证是否显示用户的详情信息
        self.assertTrue(contact_detail.is_exists_contacts_image())
        self.assertTrue(contact_detail.is_exists_contacts_name())
        self.assertTrue(contact_detail.is_exists_contacts_number())
        self.assertTrue(contact_detail.is_exists_message_icon())
        self.assertTrue(contact_detail.is_exists_call_icon())
        self.assertTrue(contact_detail.is_exists_voice_call_icon())
        self.assertTrue(contact_detail.is_exists_video_call_icon())
        self.assertTrue(contact_detail.is_exists_dial_hefeixin_icon())
        self.assertTrue(contact_detail.is_exists_share_card_icon())
        self.assertTrue(contact_detail.is_exit_element())
        self.assertTrue(contact_detail.is_exists_edit())
        time.sleep(2)
        # 10.点击分享名片
        contact_detail.click_share_card_icon()
        time.sleep(2)
        # 11.验证是否跳转联系人选择器页面
        scp = SelectContactsPage()
        self.assertTrue(scp.is_on_this_page())
        # 12.点击返回个人详情页面,点击邀请使用
        scp.click_back()
        time.sleep(2)
        contact_detail.click_invitation_use()
        time.sleep(2)
        contact_detail.click_message()
        cgsm = ChatGroupSMSExpensesPage()
        time.sleep(2)
        # 13.点击发送
        cgsm.click_send()
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_quxinli_0418(self):
        """分组详情操作界面进入Profile页-编辑"""
        GroupPage = LabelGroupingPage()
        time.sleep(1)
        # 1.删除全部分组
        GroupPage.delete_all_label()
        # 2.创建分组
        GroupPage.creat_group()
        # 3.点击第一个分组
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        detail = LableGroupDetailPage()
        # 4.添加联系人
        detail.click_add_contact()
        time.sleep(1)
        # 5.选择多个联系人
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬2')
        time.sleep(1)
        select.select_one_contact_by_name('大佬3')
        select.click_sure_bottom()
        time.sleep(2)
        # 6.点击联系人进入用户详情页
        detail.click_text('大佬2')
        contact_detail = ContactDetailsPage()
        # 7.点击编辑
        contact_detail.click_edit_contact()
        time.sleep(2)
        edit = EditContactPage()
        # 8.输入修改信息
        edit.input_company('中软国际')
        time.sleep(2)
        edit.click_sure()
        time.sleep(2)
        # 9.验证页面是否显示修改后的信息
        contact_detail.page_should_contain_text('中软国际')
        # 10.点击编辑，清空公司名
        contact_detail.click_edit_contact()
        time.sleep(2)
        edit = EditContactPage()
        edit.click_input_company()
        edit.click_clear_text()
        time.sleep(2)
        edit.click_sure()
        time.sleep(2)




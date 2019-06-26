import unittest
import uuid
from library.core.common.simcardtype import CardType
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


class TagGrouping(TestCase):
    """标签分组"""


    def default_setUp(self):
        """确保每个用例执行前在标签分组页面"""
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        MessagePage().click_contacts()
        time.sleep(2)
        ContactsPage().click_phone_contact()
        ContactsPage().click_label_grouping()

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
        SelectContactsPage().is_element_present(locator='搜索或输入手机号')

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
        SelectContactsPage().is_element_present(locator='搜索或输入手机号')

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
        SelectContactsPage().is_element_present(locator='搜索或输入手机号')

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
        SelectContactsPage().is_element_present(locator='搜索或输入手机号')

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
        SelectContactsPage().is_element_present(locator='搜索或输入手机号')

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
        self.group='1'*31
        GroupPage.input_content(text=self.group)
        GroupPage.click_sure_element()
        GroupPage.click_allow_button()
        SelectContactsPage().check_if_element_not_exist(text='搜索或输入手机号')

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
        SelectContactsPage().is_element_present(locator='搜索或输入手机号')

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
        SelectContactsPage().is_element_present(locator='搜索或输入手机号')

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
        SelectContactsPage().is_element_present(locator='搜索或输入手机号')

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
        SelectContactsPage().is_element_present(locator='搜索或输入手机号')

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
        SelectContactsPage().is_element_present(locator='搜索或输入手机号')

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
        SelectContactsPage().is_element_present(locator='搜索或输入手机号')

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
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_all_label()
        GroupPage.new_group()
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.click_text('添加成员')
        time.sleep(1)
        LabelGroupingPage().click_first_lable_group()
        time.sleep(1)
        GroupPage.input_search_text(text='测试')
        GroupPage.hide_keyboard()
        time.sleep(1)
        GroupPage.page_contain_element(locator='搜索框-搜索结果')
        #删除搜索文本
        GroupPage.page_should_contain_element1(locator="删除-搜索")
        GroupPage.clear_input_box()
        time.sleep(1)
        GroupPage.is_element_present()
        #再次输入内容搜索
        GroupPage.input_search_text(text='测试')
        GroupPage.hide_keyboard()
        time.sleep(1)
        GroupPage.page_contain_element(locator='搜索框-搜索结果')
        GroupPage.click_text('测试号码1')
        time.sleep(2)
        GroupPage.hide_keyboard()
        #跳转成功
        GroupPage.page_should_contain_text('搜索或输入号码')
        GroupPage.page_should_contain_text('选择联系人')
        #点击搜索结果
        SelectLocalContactsPage().swipe_select_one_member_by_name('测试号码1')
        GroupPage.is_element_present(locator='已选择的联系人')

    def tearDown_test_contacts_quxinli_0373(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')



    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0374(self):
        """标签分组添加成员-搜索陌生号码"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.click_text('添加成员')
        time.sleep(1)
        GroupPage.click_search_box()
        time.sleep(1)
        GroupPage.input_search_text(text='13802885230')
        GroupPage.hide_keyboard()
        time.sleep(1)
        GroupPage.page_should_contain_text('搜索团队联系人')
        GroupPage.is_element_present(locator='联系人头像')

    def tearDown_test_contacts_quxinli_0374(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0375(self):
        """标签分组添加成员-选择本地联系人"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        slcp.swipe_select_one_member_by_name('大佬1')
        GroupPage.is_element_present(locator='已选择的联系人')
        GroupPage.sure_icon_is_checkable()
        #再次点击已选择的联系人
        slcp.swipe_select_one_member_by_name('大佬1')
        GroupPage.is_element_present(locator='已选择的联系人')
        #点击已选择联系人的头像,取消选择
        slcp.swipe_select_one_member_by_name('大佬1')
        GroupPage.click_selected_contacts()
        GroupPage.is_element_present(locator='已选择的联系人')
        #选择人员,添加成员成功
        slcp.swipe_select_one_member_by_name('大佬1')
        slcp.click_sure()
        time.sleep(1)

    def tearDown_test_contacts_quxinli_0375(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button()
        GroupPage.delete_group(name='aaa')

    @staticmethod
    def setUp_test_contacts_quxinli_0376():
        Preconditions.select_mobile('IOS-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        GroupListPage().open_contacts_page()
        time.sleep(2)
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('本机')
        time.sleep(1)
        if ContactListSearchPage().is_contact_in_list('本机'):
            ContactListSearchPage().click_back()
        else:
        # 创建联系人 本机
            ContactListSearchPage().click_back()
            ContactsPage().click_phone_contact()
            ContactsPage().click_add()
            creat_contact2 = CreateContactPage()
            creat_contact2.click_input_name()
            creat_contact2.input_name('本机')
            creat_contact2.click_input_number()
            phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)
            creat_contact2.input_number(phone_number[0])
            creat_contact2.save_contact()
            time.sleep(2)
            ContactDetailsPage().click_back_icon()


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0376(self):
        """标签分组添加成员-选择本地联系人不可选成员"""
        GroupPage = GroupListPage()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        slcp.swipe_select_one_member_by_name('本机')
        slcp.page_should_contain_text('该联系人不可选择')

    def tearDown_test_contacts_quxinli_0376(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0388(self):
        """分组详情操作界面-分组只有一个人员点击群发消息"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        slcp.swipe_select_one_member_by_name('大佬1')
        slcp.click_sure()
        time.sleep(2)
        GroupPage.send_message_to_group()
        time.sleep(1)
        SingleChatPage().is_on_this_page()
        GroupPage.page_should_contain_text('大佬1')

    def tearDown_test_contacts_quxinli_0388(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')



    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0389(self):
        """分组详情操作界面-分组有多个人员点击群发消息"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        # 添加联系人大佬1 大佬2
        time.sleep(2)
        GroupPage.click_text('aaa')
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        slcp.swipe_select_one_member_by_name('大佬1')
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬2')
        slcp.click_sure()
        time.sleep(2)
        #验证页面元素
        GroupPage.send_message_to_group()
        time.sleep(1)
        GroupPage.page_contain_element(locator='多方通话_图标')
        GroupPage.page_contain_element(locator='分组联系人')
        GroupPage.page_contain_element(locator='富媒体面板')
        GroupPage.page_contain_element(locator='aaa')

    def tearDown_test_contacts_quxinli_0389(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')



    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0390(self):
        """分组详情操作界面-群发消息-发送消息"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        #添加小组成员
        GroupPage.click_text('aaa')
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        time.sleep(2)
        slcp.swipe_select_one_member_by_name('大佬1')
        slcp.click_sure()
        time.sleep(2)
        message='aa aa'*20
        GroupPage.send_message_to_group(message)
        time.sleep(1)
        GroupPage.page_contain_element('已转短信送达')
        #发送纯文本
        GroupPage.click_back_button()
        time.sleep(1)
        message = 'aaaa'
        GroupPage.send_message_to_group(message)
        time.sleep(5)
        GroupPage.page_contain_element('已转短信送达')
        #发送文本 空格
        GroupPage.click_back_button()
        time.sleep(1)
        message = 'aa aa'
        GroupPage.send_message_to_group(message)
        time.sleep(5)
        GroupPage.page_contain_element('已转短信送达')
        #发送表情
        GroupPage.click_back_button()
        time.sleep(1)
        GroupPage.send_express_to_group()
        time.sleep(1)
        GroupPage.page_not_contain_element('发送失败')
        #发送图片
        GroupPage.click_back_button()
        time.sleep(1)
        GroupPage.send_picture_to_group()
        time.sleep(2)
        GroupPage.page_not_contain_element('发送失败')
        time.sleep(1)

    def tearDown_test_contacts_quxinli_0390(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0394(self):
        """分组联系人进入Profile页-星标"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        #添加成员
        GroupPage.click_text('aaa')
        time.sleep(2)
        LabelGroupingChatPage().click_text('添加成员')
        time.sleep(2)
        slcp = SelectLocalContactsPage()
        slcp.swipe_select_one_member_by_name('大佬1')
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬2')
        slcp.click_sure()
        time.sleep(1)
        #进入群发页面
        GroupPage.enter_group_message()
        GroupPage.click_divide_group_icon()
        time.sleep(1)
        GroupPage.page_contain_element(locator='分组联系人_标题')
        GroupPage.click_text("大佬1")
        # time.sleep(1)
        # GroupPage.click_star_icon()
        time.sleep(1)
        GroupPage.click_star_icon()
        if GroupPage.is_toast_exist('已成功添加为星标联系人'):
            time.sleep(2)
        else:
            time.sleep(1)
            GroupPage.click_star_icon()
            GroupPage.is_toast_exist("已成功添加为星标联系人")
        time.sleep(1)
        GroupPage.click_star_icon()
        GroupPage.is_toast_exist("已取消添加为星标联系人")
        #再次点击星标
        GroupPage.click_star_icon()
        GroupPage.click_back_button(times=3)
        time.sleep(2)
        GroupPage.click_back_button(times=2)
        time.sleep(1)
        GroupPage.page_contain_star('大佬1')

    def tearDown_test_contacts_quxinli_0394(self):
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        ContactsPage().click_phone_contact()
        #去除大佬1的星标
        ContactsPage().select_contacts_by_name('大佬1')
        GroupPage = GroupListPage()
        GroupPage.click_star_icon()
        if GroupPage.is_toast_exist('已取消添加为星标联系人'):
            time.sleep(2)
        else:
            time.sleep(1)
            GroupPage.click_star_icon()
        time.sleep(1)
        #删除群组
        GroupPage.click_back_button()
        time.sleep(2)
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0395(self):
        """分组联系人进入Profile页-编辑"""
        GroupPage = GroupListPage()
        cdp=ContactDetailsPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        time.sleep(2)
        slcp.swipe_select_one_member_by_name('大佬1')
        slcp.swipe_select_one_member_by_name('大佬2')
        slcp.click_sure()
        time.sleep(1)
        GroupPage.enter_group_message()
        GroupPage.click_divide_group_icon()
        time.sleep(1)
        GroupPage.page_contain_element(locator='分组联系人_标题')
        GroupPage.click_text("大佬1")
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        number=CreateContactPage().get_contant_number()
        if number == '13800138789':
            CreateContactPage().click_back()
        else:
            cdp.change_mobile_number()
            time.sleep(1)
            cdp.click_sure_icon()
            time.sleep(1)
            GroupPage.is_toast_exist("保存成功")
            cdp.is_text_present('13800138789')

    def tearDown_test_contacts_quxinli_0395(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')
        #恢复修改的联系人号码
        GroupPage.click_back_button()
        ContactsPage().select_contacts_by_name('大佬1')
        ContactDetailsPage().click_edit_contact()
        time.sleep(1)
        EditContactPage().click_contact_number()
        EditContactPage().input_number('13800138005')
        time.sleep(1)
        EditContactPage().click_sure()
        time.sleep(2)


    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0396(self):
        """分组联系人进入Profile页-编辑-删除联系人"""
        GroupPage = GroupListPage()
        cdp=ContactDetailsPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        #进入分组 添加成员
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.tap_sure_box()
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        time.sleep(2)
        slcp.swipe_select_one_member_by_name('大佬1')
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬2')
        slcp.click_sure()
        time.sleep(1)
        #进入群发消息页面
        GroupPage.enter_group_message()
        GroupPage.click_divide_group_icon()
        time.sleep(1)
        GroupPage.page_contain_element(locator='分组联系人_标题')
        GroupPage.click_text("大佬2")
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        cdp.hide_keyboard()
        cdp.page_up()
        cdp.change_delete_number()
        cdp.click_sure_delete()
        time.sleep(1)
        GroupPage.is_toast_exist("删除成功")
        time.sleep(1)

    def tearDown_test_contacts_quxinli_0396(self):
        GroupPage = GroupListPage()
     #   GroupPage.click_back_button(times=2)
        GroupPage.click_back_by_android(times=2)
        GroupPage.delete_group(name='aaa')
        time.sleep(2)
        #删除该联系人后添加联系人
        LabelGroupingPage().click_back()
        time.sleep(2)
        ContactsPage().click_add()
        ccp=CreateContactPage()
        ccp.click_input_name()
        ccp.input_name('大佬2')
        ccp.click_input_number()
        ccp.input_number('13800138006')
        ccp.click_save()
        CallContactDetailPage().click_back()


    @tags('ALL', 'CONTACT', '多方通话-跳过')
    def test_contacts_quxinli_0397(self):
        """“分组详情操作”界面-多方电话"""
        GroupPage = GroupListPage()
        cdp=ContactDetailsPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        #进入群组,添加联系人
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        time.sleep(2)
        slcp.swipe_select_one_member_by_name('大佬1')
        slcp.swipe_select_one_member_by_name('大佬3')
        slcp.click_sure()
        time.sleep(1)
        #多方通话
        GroupPage.enter_mutil_call()
        time.sleep(1)
        GroupPage.click_text("大佬1")
        cdp.send_call_number()
        if GroupPage.is_text_present('我知道了'):
            time.sleep(2)
            GroupPage.click_text('我知道了')
        if GroupPage.is_text_present('发起多方电话失败'):
            pass
        else:
            # cdp.send_call_number()
            cdp.cancel_permission()
            time.sleep(3)
            cdp.cancel_hefeixin_call()
            time.sleep(2)

    def tearDown_test_contacts_quxinli_0397(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button()
        GroupPage.delete_group(name='aaa')



    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0398(self):
        """“分组详情操作”界面-多方视频"""
        GroupPage = GroupListPage()
        cdp = ContactDetailsPage()

        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')

        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬1')
        time.sleep(1)
        slcp.click_sure()
        time.sleep(1)
        GroupPage.enter_mutil_video_call()
        time.sleep(2)
        while GroupPage.is_text_present('始终允许'):
            GroupPage.click_text('始终允许')
        time.sleep(1)
        GroupPage.click_text("大佬1")
        time.sleep(2)
        cdp.send_call_number()
        if cdp.is_text_present('暂不开启'):
            cdp.cancel_permission()
        cdp.end_video_call()

    def tearDown_test_contacts_quxinli_0398(self):
        GroupPage = GroupListPage()
        time.sleep(1)
        SelectOneGroupPage().click_back_by_android()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')



    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0407(self):
        """“分组设置-特殊符号标签名称
        auther:darcy
        """
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.update_label_name(name='*@!#')
        GroupPage.click_back_button(times=2)
        GroupPage.page_should_contain_text(text='*@!#')

    def tearDown_test_contacts_quxinli_0407(self):
        GroupPage = GroupListPage()
        GroupPage.delete_group(name='*@!#')



    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0408(self):
        """“分组设置-各种标签名称
        auther:darcy
        """
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.update_label_name(name='*@!#123好')
        GroupPage.click_back_button(times=2)
        GroupPage.page_should_contain_text(text='*@!#123好')

    def tearDown_test_contacts_quxinli_0408(self):
        GroupPage = GroupListPage()
        GroupPage.delete_group(name='*@!#123好')



    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0409(self):
        """“分组设置-各种标签名称删除
        auther:darcy
        """
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.delete_label_name(name='*@!#123好')
        GroupPage.page_should_contain_text(text="请输入标签分组名称")
        GroupPage.click_back_button(times=3)

    def tearDown_test_contacts_quxinli_0409(self):
        GroupPage = GroupListPage()
        GroupPage.delete_group(name='*@!#123好')



    @tags('ALL', 'CONTACT-debug', 'CMCC')
    def test_contacts_quxinli_0414(self):
        """分组设置-搜索移除成员
        auther:darcy
        """
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        #添加成员
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬1')
        slcp.click_sure()
        time.sleep(2)
        #移除成员
        GroupPage.click_settings_button()
        GroupPage.click_move_label()
        time.sleep(1)
        GroupPage.search_menber_text(text='dalao1')
        time.sleep(1)
        GroupPage.click_text('大佬1')
        time.sleep(1)
        GroupPage.click_sure_element()
        time.sleep(1)
        GroupPage.click_move_label()
        time.sleep(1)
        GroupPage.page_should_not_contain_text("大佬1")

    def tearDown_test_contacts_quxinli_0414(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=3)
        GroupPage.delete_group(name='aaa')



    @tags('ALL', 'CONTACT-debug', 'CMCC')
    def test_contacts_quxinli_0415(self):
        """分组设置-删除标签
        auther:darcy
        """
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.new_group(name='ccc')
        GroupPage.delete_group(name='ccc')
        GroupPage.click_back_by_android(times=2)


    @tags('ALL', 'CONTACT-debug', 'CMCC')
    def test_contacts_quxinli_0416(self):
        """分组详情操作页面进入Profile页"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        #添加成员
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬3')
        # slcp.select_one_member_by_name('大佬2')
        slcp.swipe_select_one_member_by_name('大佬4')
        slcp.click_sure()
        time.sleep(2)
        LableGroupDetailPage().click_send_group_info()
        time.sleep(2)
        GroupPage.click_divide_group_icon()
        time.sleep(1)
        GroupPage.page_contain_element(locator='分组联系人_标题')
        GroupPage.click_text("大佬3")
        time.sleep(1)
        GroupPage.page_contain_element(locator='语音通话')
        GroupPage.page_contain_element(locator='视频通话')
        GroupPage.page_contain_element(locator='分享名片')
        GroupPage.click_share_button()
        time.sleep(1)
        SelectContactsPage().click_select_one_group()
        time.sleep(1)
        SelectOneGroupPage().click_search_group()
        SelectOneGroupPage().input_search_keyword('给个红包1')
        SelectOneGroupPage().selecting_one_group_by_name('给个红包1')
        SelectOneGroupPage().click_share_business_card()
        time.sleep(2)


    @tags('ALL', 'CONTACT-debug', 'CMCC')
    def test_contacts_quxinli_0417(self):
        """分组详情操作页面进入Profile页_星标
        auther:darcy"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        #添加成员
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬3')
        slcp.swipe_select_one_member_by_name('大佬4')
        slcp.click_sure()
        time.sleep(2)

        GroupPage.enter_group_message()
        time.sleep(1)
        GroupPage.click_divide_group_icon()
        time.sleep(1)
        GroupPage.page_contain_element(locator='分组联系人_标题')
        GroupPage.click_text("大佬3")
        time.sleep(1)
        GroupPage.click_star_icon()
        GroupPage.is_toast_exist("已成功添加为星标联系人")
        time.sleep(1)
        GroupPage.click_star_icon()
        GroupPage.is_toast_exist("已取消添加为星标联系人")
        GroupPage.click_star_icon()
       # GroupPage.click_back_button(times=3)
        GroupPage.click_back_by_android(times=3)
        time.sleep(2)
       # GroupPage.click_back_button(times=2)
        GroupPage.click_back_by_android(times=2)

        time.sleep(1)
        GroupPage.page_contain_star('大佬3')

    def tearDown_test_contacts_quxinli_0417(self):
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        ContactsPage().click_phone_contact()
        #去除大佬1的星标
        ContactsPage().select_contacts_by_name('大佬3')
        time.sleep(1)
        GroupPage = GroupListPage()
        GroupPage.click_star_icon()
        if GroupPage.is_text_present('已取消添加为星标联系人'):
            GroupPage.click_back_button()
        elif GroupPage.is_text_present('已成功添加为星标联系人'):
            GroupPage.click_star_icon()
            GroupPage.click_back_button()
        #删除群组
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')

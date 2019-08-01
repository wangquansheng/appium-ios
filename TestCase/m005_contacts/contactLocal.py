import unittest
import uuid
import time

from pages.contacts.GroupAssistant import GroupAssistantPage
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


    # @staticmethod
    # def create_contacts_if_not_exits(name, number):
    #     """
    #     不存在就导入联系人数据
    #     :param name:
    #     :param number:
    #     :return:
    #     """
    #     contacts_page = ContactsPage()
    #     detail_page = ContactDetailsPage()
    #     # 创建联系人
    #     contacts_page.click_phone_contact()
    #     time.sleep(2)
    #     contacts_page.click_search_phone_contact()
    #     contacts_page.input_search_keyword(name)
    #     if contacts_page.is_contact_in_list():
    #         contacts_page.click_back()
    #     else:
    #         contacts_page.click_add()
    #         create_page = CreateContactPage()
    #         create_page.create_contact(name, number)
    #         time.sleep(2)
    #         detail_page.click_back_icon()
    #         contacts_page.click_back()
    #
    #



class ContactsLocalhigh(TestCase):
    """
    模块：联系-本地联系人
    文件位置：全量/115全量测试用例-联系(1322).xlsx--高等级用例(优先编写)
    表格：通讯录-本地通讯录
    author: 余梦思
    """

    @classmethod
    def setUpClass(cls):

        Preconditions.select_mobile('IOS-移动')
        # 导入测试联系人、群聊
        fail_time1 = 0
        flag1 = False
        import dataproviders
        while fail_time1 < 3:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                Preconditions.make_already_in_message_page()
                conts.open_contacts_page()
                for name, number in required_contacts:
                    # 创建联系人
                    conts.create_contacts_if_not_exits(name, number)
                required_group_chats = dataproviders.get_preset_group_chats()
                conts.open_group_chat_list()
                group_list = GroupListPage()
                for group_name, members in required_group_chats:
                    group_list.wait_for_page_load()
                    # 创建群
                    group_list.create_group_chats_if_not_exits(group_name, members)
                group_list.click_back()
                conts.open_message_page()
                flag1 = True
            except:
                fail_time1 += 1
            if flag1:
                break


    def default_setUp(self):
        """确保每个用例执行前在通讯录页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        MessagePage().click_contacts()
        time.sleep(2)
        ContactsPage().click_phone_contact()

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0130(self):
        """测试表单字段，姓名非空校验"""
        ContactsPage().click_add()
        time.sleep(1)
        creat_contact = CreateContactPage()
        creat_contact.click_input_name()
        creat_contact.click_input_number()
        # toast提示 姓名不能为空，请重新输入(无法验证toast，使用其他方式验证)
        # 使用 点击保存按钮无反应
        creat_contact.click_save()
        self.assertTrue(creat_contact.is_on_this_page())
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0137(self):
        """测试表单字段，手机号非空校验"""
        ContactsPage().click_add()
        time.sleep(1)
        creat_contact=CreateContactPage()
        creat_contact.click_input_name()
        creat_contact.input_name('ceshi')
        creat_contact.click_input_number()
        creat_contact.click_input_name()
        # toast提示 电话不能为空，请重新输入(无法验证toast，使用其他方式验证)
        # 使用 点击保存按钮无反应
        creat_contact.click_save()
        self.assertTrue(creat_contact.is_on_this_page())
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0138(self):
        """测试表单字段，手机号码长度校验，小于3个字符"""
        ContactsPage().click_add()
        time.sleep(1)
        creat_contact=CreateContactPage()
        creat_contact.click_input_name()
        creat_contact.input_name('ceshi')
        creat_contact.click_input_number()
        creat_contact.input_number('12')
        # toast提示 号码输入有误，请重新输入(无法验证toast，使用其他方式验证)
        # 使用 点击保存按钮无反应
        creat_contact.click_save()
        self.assertTrue(creat_contact.is_on_this_page())
        time.sleep(2)


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0140(self):
        """测试表单字段，手机号码长度边界值校验，3个字符"""
        ContactsPage().click_add()
        time.sleep(1)
        creat_contact=CreateContactPage()
        creat_contact.click_input_name()
        creat_contact.input_name('ceshi')
        creat_contact.click_input_number()
        creat_contact.input_number('123')
        creat_contact.click_save()
        time.sleep(2)
        ContactDetailsPage().page_should_contain_text('飞信电话')
        time.sleep(2)

    def tearDown_test_contacts_chenjixiang_0140(self):
        contant_detail = ContactDetailsPage()
        if contant_detail.is_on_this_page():
            time.sleep(3)
        else:
            Preconditions.make_already_in_message_page()
            MessagePage().click_contacts()
            ContactsPage().click_phone_contact()
            ContactsPage().select_contacts_by_name('ceshi')
            time.sleep(2)
        contant_detail.click_edit_contact()
        time.sleep(2)
        # contant_detail.page_up()
        contant_detail.change_delete_number()
        contant_detail.click_sure_delete()
        time.sleep(3)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0147(self):
        """测试表单字段，公司边界值校验，输入1个字符"""
        ContactsPage().click_add()
        time.sleep(1)
        creat_contact=CreateContactPage()
        creat_contact.click_input_name()
        creat_contact.input_name('ceshi')
        creat_contact.click_input_number()
        creat_contact.input_number('123')
        creat_contact.click_input_company()
        creat_contact.input_company('a')
        creat_contact.click_save()
        time.sleep(2)
        ContactDetailsPage().page_should_contain_text('飞信电话')
        time.sleep(2)

    def tearDown_test_contacts_chenjixiang_0147(self):
        contant_detail = ContactDetailsPage()
        if contant_detail.is_on_this_page():
            time.sleep(3)
        else:
            Preconditions.make_already_in_message_page()
            MessagePage().click_contacts()
            ContactsPage().click_phone_contact()
            ContactsPage().select_contacts_by_name('ceshi')
            time.sleep(2)
        contant_detail.click_edit_contact()
        time.sleep(2)
        # contant_detail.page_up()
        contant_detail.change_delete_number()
        contant_detail.click_sure_delete()
        time.sleep(3)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0154(self):
        """测试表单字段，职位边界值校验，输入1个字符"""
        ContactsPage().click_add()
        time.sleep(1)
        creat_contact=CreateContactPage()
        creat_contact.click_input_name()
        creat_contact.input_name('ceshi')
        creat_contact.click_input_number()
        creat_contact.input_number('123')
        creat_contact.page_down()
        creat_contact.click_input_position()
        creat_contact.input_position('a')
        creat_contact.click_save()
        time.sleep(2)
        ContactDetailsPage().page_should_contain_text('飞信电话')
        time.sleep(2)

    def tearDown_test_contacts_chenjixiang_0154(self):
        contant_detail = ContactDetailsPage()
        contant_detail.click_edit_contact()
        time.sleep(2)
        # contant_detail.page_up()
        contant_detail.change_delete_number()
        contant_detail.click_sure_delete()
        time.sleep(3)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0161(self):
        """测试表单字段，邮箱边界值校验，输入1个字符"""
        ContactsPage().click_add()
        time.sleep(1)
        creat_contact=CreateContactPage()
        creat_contact.click_input_name()
        creat_contact.input_name('ceshi')
        creat_contact.click_input_number()
        creat_contact.input_number('123')
        creat_contact.page_down()
        creat_contact.click_input_email()
        creat_contact.input_email_address('a')
        creat_contact.click_save()
        time.sleep(2)
        ContactDetailsPage().page_should_contain_text('飞信电话')
        time.sleep(2)

    def tearDown_test_contacts_chenjixiang_0161(self):
        contant_detail = ContactDetailsPage()
        contant_detail.click_edit_contact()
        time.sleep(2)
        # contant_detail.page_up()
        contant_detail.change_delete_number()
        contant_detail.click_sure_delete()
        time.sleep(3)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])



    # @tags('ALL', 'CONTACTS', 'CMCC')
    # def test_contacts_chenjixiang_0166(self):
    #     """测试和飞信新建联系人，名称和本地通讯录联系人一样，手机号码不一样"""
    #     # old_number=ContactsPage().get_all_phone_number()
    #     ContactsPage().click_add()
    #     time.sleep(1)
    #     creat_contact=CreateContactPage()
    #     creat_contact.click_input_name()
    #     input_name='大佬1'
    #     creat_contact.input_name(input_name)
    #     creat_contact.click_input_number()
    #     input_number='12345678901'
    #     creat_contact.input_number(input_number)
    #     creat_contact.click_save()
    #     time.sleep(2)
    #     contact_detail=ContactDetailsPage()
    #     contact_detail.page_should_contain_text('飞信电话')
    #     time.sleep(1)
    #     contact_name1=contact_detail.get_people_name()
    #     contact_number1=contact_detail.get_people_number()
    #     time.sleep(1)
    #     #原本的大佬1
    #     contact_detail.click_back_icon()
    #     time.sleep(1)
    #     ContactsPage().select_contacts_by_number('13800138005')
    #     time.sleep(2)
    #     contact_name2 = contact_detail.get_people_name()
    #     contact_number2 = contact_detail.get_people_number()
    #     #判断新增名称一样,号码与头像不一样
    #     time.sleep(1)
    #     self.assertEqual(contact_name1,contact_name2)
    #     self.assertNotEqual(contact_number1, contact_number2)
    #
    # def tearDown_test_contacts_chenjixiang_0166(self):
    #     Preconditions.make_already_in_message_page()
    #     MessagePage().click_contacts()
    #     contact = ContactsPage()
    #     if contact.is_exit_element_by_text_swipe('12345678901'):
    #         contact.select_contacts_by_number('12345678901')
    #         contant_detail = ContactDetailsPage()
    #         contant_detail.click_edit_contact()
    #         time.sleep(2)
    #         contant_detail.hide_keyboard()
    #         contant_detail.change_delete_number()
    #         contant_detail.click_sure_delete()
    #     else:
    #         pass

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0175(self):
        """测试页面信息展示，名称正常长度显示"""
        text = '大佬1'
        ContactsPage().select_contacts_by_name(text)
        cdp = ContactDetailsPage()
        time.sleep(2)
        contact_name=cdp.get_people_name(text)
        self.assertEqual(contact_name,text)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0177(self,):
        """测试页面信息展示，手机号码正常长度显示"""
        text='大佬1'
        ContactsPage().select_contacts_by_name(text)
        cdp = ContactDetailsPage()
        time.sleep(2)
        number='13800138005'
        contact_number=cdp.get_people_number(number)
        self.assertEqual(contact_number,number)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0179(self):
        """测试页面信息展示，未上传头像"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.page_should_contain_element_first_letter()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0180(self):
        """测试页面信息展示，已上传头像"""
        ContactsPage().select_contacts_by_name('测试号码')
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        time.sleep(2)
        cdp.page_contain_contacts_avatar()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0181(self):
        """测试点击联系人头像，未上传头像"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        time.sleep(2)
        cdp.click_avatar()
        cdp.is_exists_big_avatar()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0182(self):
        """测试点击联系人头像，已上传头像"""
        ContactsPage().select_contacts_by_name('测试号码')
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        time.sleep(2)
        cdp.click_avatar()
        cdp.is_exists_big_avatar()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0193(self):
        """测试编辑联系人信息，正常"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        #编辑手机号码
        creat_contact=EditContactPage()
        creat_contact.change_mobile_number(text='13800138789')
        creat_contact.click_sure()
        time.sleep(2)
        #查看改变后的联系人
        cdp.click_back_icon()
        ContactsPage().select_contacts_by_name('大佬1')
        ContactDetailsPage().page_should_contain_text('13800138789')


    def tearDown_test_contacts_chenjixiang_0193(self):
        if ContactDetailsPage().is_text_present('13800138005'):
            ContactDetailsPage().click_back_icon()
        else:
            ContactDetailsPage().click_edit_contact()
            creat_contact = EditContactPage()
            creat_contact.change_mobile_number(text='13800138005')
            creat_contact.click_sure()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0194(self):
        """测试表单字段，姓名非空校验"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        # 姓名为空,保存按钮不可点击
        creat_contact = EditContactPage()
        creat_contact.click_contact_name()
        creat_contact.click_clear_text()
        # creat_contact.is_sure_icon_is_clickable()
        # 姓名为必填项
        creat_contact.click_contact_number()
        # toast提示 姓名不能为空，请重新输入(无法验证toast，使用其他方式验证)
        # 使用 点击保存按钮无反应
        creat_contact.click_sure()
        self.assertTrue(creat_contact.is_on_this_page())
        time.sleep(2)
        creat_contact.click_back()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0201(self):
        """个人profile页,编辑联系人-手机号码不为空"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        # 手机号为空,保存按钮不可点击
        creat_contact = EditContactPage()
        creat_contact.click_contact_number()
        creat_contact.click_clear_text()
        # toast提示 号码不能为空，请重新输入(无法验证toast，使用其他方式验证)
        # 使用 点击保存按钮无反应
        creat_contact.click_sure()
        self.assertTrue(creat_contact.is_on_this_page())
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0206(self):
        """测试表单字段，手机号码特殊字符输入"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        # 姓名为空,保存按钮不可点击
        creat_contact = EditContactPage()
        creat_contact.click_contact_number()
        creat_contact.click_clear_text()
        creat_contact.input_number('#')
        # toast提示 号码输入有误，请重新输入(无法验证toast，使用其他方式验证)
        # 获取输入框文本判断
        number = creat_contact.get_phone_number()
        self.assertEqual(number, '输入号码')
        creat_contact.click_back()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0209(self):
        """测试表单字段，公司非必填"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        # 公司为空 可点
        creat_contact = EditContactPage()
        creat_contact.click_input_company()
        creat_contact.click_contact_number()
        creat_contact.click_sure()
        time.sleep(3)
        self.assertTrue(cdp.is_on_this_page())

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0214(self):
        """测试表单字段，公司字段，组合输入"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        # 手机号为空,保存按钮不可点击
        creat_contact = EditContactPage()
        creat_contact.click_input_company()
        creat_contact.input_company('#sa123')
        creat_contact.click_sure()
        time.sleep(3)
        self.assertTrue(cdp.is_on_this_page())


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0216(self):
        """测试表单字段，职位非必填"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        # 职位为空 可点
        creat_contact = EditContactPage()
        creat_contact.click_input_position()
        creat_contact.click_contact_number()
        creat_contact.click_sure()
        time.sleep(3)
        self.assertTrue(cdp.is_on_this_page())

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0223(self):
        """测试表单字段，邮箱非必填"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        # 邮箱为空 可点
        creat_contact = EditContactPage()
        creat_contact.click_input_email()
        creat_contact.page_up()
        creat_contact.click_input_company()
        # creat_contact.is_sure_icon_is_clickable()
        creat_contact.click_sure()
        time.sleep(2)
        self.assertTrue(cdp.is_on_this_page())


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0228(self):
        """测试表单字段，邮箱字段，组合输入"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        # 手机号为空,保存按钮不可点击
        creat_contact = EditContactPage()
        creat_contact.click_input_email()
        creat_contact.input_email_address('#sa123')
        # self.assertTrue(creat_contact.is_sure_icon_is_clickable())
        creat_contact.click_sure()
        time.sleep(3)
        self.assertTrue(cdp.is_on_this_page())

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0230(self):
        """测试删除联系人"""
        ContactsPage().select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        #删除联系人
        creat_contact = EditContactPage()
        creat_contact.click_delete_contact()
        creat_contact.click_sure_delete()
        time.sleep(2)
        self.assertFalse(ContactsPage().is_contacts_exist_by_name('大佬1'))

    def tearDown_test_contacts_chenjixiang_0230(self):

        ContactsPage().click_add()
        creat_contact = CreateContactPage()
        creat_contact.click_input_name()
        creat_contact.input_name('大佬1')
        creat_contact.click_input_number()
        creat_contact.input_number('13800138005')
        creat_contact.click_save()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0232(self):
        """测试“邀请使用”按钮跳转"""
        ContactsPage().select_contacts_by_name('大佬2')
        cdp = ContactDetailsPage()
        cdp.click_invitation_use()
        time.sleep(2)
        cdp.page_should_contain_text('取消')
        cdp.page_should_contain_text('短信')
        cdp.page_should_contain_text('微信')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0237(self):
        """测试分享名片，跳转到联系人选择器"""
        ContactsPage().select_contacts_by_name('大佬2')
        cdp = ContactDetailsPage()
        cdp.click_share_business_card()
        select=SelectContactsPage()
        select.page_should_contain_text('选择联系人')
        select.page_should_contain_text('搜索或输入手机号')
        select.page_should_contain_text('选择一个群')
        select.page_should_contain_text('选择团队联系人')
        select.page_should_contain_text('选择手机联系人')
        if select.is_element_present(locator='最近聊天列表'):
            select.page_should_contain_text('最近聊天')


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0238(self):
        """测试和飞信电话，登录本网卡显示，可拨打成功"""
        ContactsPage().select_contacts_by_name('大佬2')
        cdp = ContactDetailsPage()
        cdp.click_hefeixin_call_menu()
        if cdp.is_text_present('我知道了'):
            cdp.click_text('我知道了')
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    #星标无法定位
    def test_contacts_chenjixiang_0242(self):
        """测试星标点击"""
        ContactsPage().select_contacts_by_name('大佬2')
        glp =ContactDetailsPage()
        time.sleep(2)
        glp.click_star_icon()
        glp.is_toast_exist('已成功添加为星标联系人')
        #取消星标
        time.sleep(2)
        glp.click_star_icon()

    @tags('ALL', 'CONTACTS', 'CMCC')
    # 星标无法定位
    def test_contacts_chenjixiang_0243(self):
        """测试取消星标"""
        #添加联系人是星标联系人
        ContactsPage().select_contacts_by_name('大佬2')
        glp =ContactDetailsPage()
        time.sleep(2)
        glp.click_star_icon()
        glp.is_toast_exist('已成功添加为星标联系人')
        #取消添加星标联系人
        glp.click_star_icon()
        glp.is_toast_exist('已取消添加为星标联系人')


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0246(self):
        """测试消息，点击消息，跳转到对话框"""
        #添加联系人是星标联系人
        ContactsPage().select_contacts_by_name('大佬2')
        glp = GroupListPage()
        ContactDetailsPage().click_message_icon()
        time.sleep(2)
        if ChatWindowPage().is_text_present("用户须知"):
            #如果存在用户须知,就点击已阅读,然后点击返回.如果不存在,就直接点击返回
            ChatWindowPage().click_already_read()
            ChatWindowPage().click_sure_icon()
        self.assertTrue(SingleChatPage().is_on_this_page())

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0247(self):
        """测试电话，点击后调用系统通话，拨打电话"""
        ContactsPage().select_contacts_by_name('大佬2')
        cdp = ContactDetailsPage()
        cdp.click_call_icon()
        cdp.click_calling()
        time.sleep(4)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0248(self):
        """测试语音通话，点击后弹出语音通话框"""
        ContactsPage().select_contacts_by_name('大佬2')
        cdp = ContactDetailsPage()
        cdp.click_voice_call_icon()
        time.sleep(3)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0250(self):
        """测试视频通话，点击后弹出语音通话框"""
        ContactsPage().select_contacts_by_name('大佬2')
        cdp = ContactDetailsPage()
        cdp.click_video_call_icon()
        # if cdp.is_text_present('"和飞信"想访问您的相机'):
        #     cdp.
        time.sleep(3)



class SearchLocalContacts(TestCase):
    """
    搜索-本地通讯录--陈继祥
    author: 余梦思

    """

    def default_setUp(self):
        """确保每个用例运行前在通讯录-手机联系人页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load()
        MessagePage().click_contacts()
        ContactsPage().click_phone_contact()

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0001(self):
        '''
        搜索输入框校验，通过手机号码搜索，输入数字模糊查询（只搜索一条记录）
        author:darcy

        :return:
        '''
        lcontact=ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('138005')
        lcontact.page_contain_element(text='列表项')


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0002(self):
        '''
        搜索输入框校验，通过手机号码搜索，输入数字模糊查询（搜索多条记录）
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('138')
        time.sleep(3)
        lcontact.page_down()
        els=lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els)>1)
        lcontact.page_contain_element(text='联系人头像')


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0003(self):
        '''
        搜索输入框校验，通过手机号码搜索，输入手机号码全匹配查询
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('13800138005')
        time.sleep(3)
        lcontact.page_down()
        els=lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els) == 1)
        lcontact.page_contain_element(text='联系人头像')
        lcontact.page_should_contain_text('大佬1')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0004(self):
        '''
        搜索输入框校验，通过名称（中文）搜索，输入名称模糊查询（搜索多条记录）
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('大佬')
        time.sleep(3)
        lcontact.page_down()
        els=lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els)>1)
        lcontact.page_contain_element(text='联系人头像')


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0005(self):
        '''
        搜索输入框校验，通过名称（英文）搜索，输入名称模糊查询（搜索多条记录）
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('dalao')
        time.sleep(3)
        lcontact.page_down()
        els=lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els)>1)
        lcontact.page_contain_element(text='联系人头像')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0006(self):
        '''
        搜索输入框校验，通过名称（特殊字符）搜索，输入名称模糊查询（搜索多条记录）
        auther:darcy
        :return:
        '''
        lcontact = ContactsPage()
        lcontact.click_search_phone_contact()
        time.sleep(1)
        lcontact.input_search_keyword('#')
        lcontact.page_down()
        time.sleep(3)
        els=lcontact.get_page_elements(text='列表项')
        self.assertTrue(len(els)>1)
        lcontact.page_contain_element(text='联系人头像')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0007(self):
        '''
        搜索输入框校验，通过名称搜索，输入名称全匹配搜索（搜索多条记录）
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



    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0030(self):
        '''
        测试搜索结果点击后跳转到profile页面
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
        self.assertTrue(ContactDetailsPage().is_on_this_page())


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0046(self):
        '''
        测试+86的手机号码，通过+86搜索
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
        self.assertTrue(ContactDetailsPage().is_on_this_page())


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0053(self):
        '''
        测试+852的手机号码，通过+852搜索
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
        self.assertTrue(ContactDetailsPage().is_on_this_page())

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0079(self):
        '''
        测试邀请按钮跳转，自动调用系统短信，自动填入短信模板内容
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

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0083(self):
        '''
        测试点击联系人跳转到profile页
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
        self.assertTrue(detail.is_on_this_page())



class SearchAllcontacts(TestCase):
    """通讯录-全局搜索"""

    def default_setUp(self):
        """确保每个用例运行前在通讯录-手机联系人页面"""
        warnings.simplefilter('ignore',ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load()
        MessagePage().click_contacts()
        time.sleep(2)


    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0733(self):
        """进入搜索页面，原“本地通讯录”和“和通讯录”分标签搜索，修改为APP联系人全局搜索，光标停留在搜索框，不展示搜索无结果缺省页。"""
        contact=ContactsPage()
        contact.click_search_box()
        time.sleep(2)
        contact.page_should_contain_text('输入关键字快速搜索')
        contact.page_should_not_contain_text('本地通讯录')
        contact.page_should_not_contain_text('和通讯录')
        contact.page_should_not_contain_text('无搜索结果')


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0734(self):
        """搜索框提示语为'输入关键词快速搜索'。  """
        contact=ContactsPage()
        contact.click_search_box()
        time.sleep(2)
        contact.page_should_contain_text('输入关键字快速搜索')
        contact.page_contain_element(text='输入关键字快速搜索')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0735(self):
        """点击返回退出搜索页面"""
        contact=ContactsPage()
        contact.click_search_box()
        time.sleep(2)
        contact.page_should_contain_text('输入关键字快速搜索')
        contact.click_back()
        contact.page_contain_element(text='手机联系人')
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0736(self):
        """输入其他字符，比如特殊字符（范围：`~!@#$%^&*()_+-=[]{}\|;:'"<,>.?/）等，支持模糊查询，正常搜索出结果"""
        contact=ContactsPage()
        contact.click_search_box()
        time.sleep(1)
        contact.input_search_text('#')
        time.sleep(2)
        contact.page_should_contain_text('团队联系人')
        contact.page_contain_element(text='搜索结果-团队联系人头像')


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0737(self):
        """本地联系人搜索结果标签小于3等于条记录时，不显示“查看更多”按钮"""
        contact=ContactsPage()
        contact.click_search_box()
        time.sleep(1)
        contact.input_search_text('大佬1')
        time.sleep(2)
        contact.page_down()
        contact.page_contain_element(text='手机联系人头像')
        contact.page_not_contain_element(text='查看更多2')


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0738(self):
        """本地联系人搜索结果标签大于3条记录时，显示“查看更多”按钮，点击查看更多之后，按关键词分页展示剩余匹配结果"""
        contact=ContactsPage()
        contact.click_search_box()
        time.sleep(1)
        contact.input_search_text('大佬')
        time.sleep(2)
        contact.page_down()
        contact.page_contain_element(text='手机联系人头像')
        contact.page_contain_element(text='查看更多2')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0739(self):
        """团队联系人搜索结果标签小于3等于条记录时，不显示“查看更多”按钮"""
        contact=ContactsPage()
        contact.click_search_box()
        time.sleep(1)
        contact.input_search_text('大佬1')
        time.sleep(2)
        contact.page_down()
        contact.page_contain_element(text='搜索结果-团队联系人头像')
        contact.page_not_contain_element(text='查看更多1')


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0740(self):
        """团队联系人搜索结果标签大于3条记录时，显示“查看更多”按钮，点击查看更多之后，按关键词分页展示剩余匹配结果"""
        contact=ContactsPage()
        contact.click_search_box()
        time.sleep(1)
        contact.input_search_text('大佬')
        time.sleep(2)
        contact.page_down()
        contact.page_contain_element(text='搜索结果-团队联系人头像')
        contact.page_contain_element(text='查看更多1')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0741(self):
        """群聊搜索结果标签小于3等于条记录时，不显示“查看更多”按钮"""
        contact = ContactsPage()
        contact.click_search_box()
        time.sleep(1)
        contact.input_search_text('给个红包1')
        time.sleep(2)
        contact.page_down()
        contact.page_contain_element(text='群聊联系人头像')
        contact.page_not_contain_element(text='查看更多2')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0742(self):
        """群聊搜索结果标签大于3条记录时，显示“查看更多”按钮，点击查看更多之后，按关键词分页展示剩余匹配结果"""
        contact = ContactsPage()
        contact.click_search_box()
        time.sleep(1)
        contact.input_search_text('给个红包')
        time.sleep(2)
        contact.page_down()
        contact.page_contain_element(text='群聊联系人头像')
        contact.page_contain_element(text='查看更多2')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0743(self):
        """公众号搜索结果标签小于3等于条记录时，不显示“查看更多”按钮"""
        contact = ContactsPage()
        contact.click_search_box()
        time.sleep(1)
        contact.input_search_text('和飞信新闻')
        time.sleep(2)
        contact.page_down()
        contact.page_contain_element(text='和飞信新闻公众号头像')
        contact.page_not_contain_element(text='查看更多2')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0744(self):
        """公众号搜索结果标签大于3条记录时，显示“查看更多”按钮，点击查看更多之后，按关键词分页展示剩余匹配结果"""
        contact = ContactsPage()
        contact.click_search_box()
        time.sleep(1)
        contact.input_search_text('和飞信')
        time.sleep(2)
        contact.page_down()
        contact.page_contain_element(text='和飞信新闻公众号头像')
        contact.page_contain_element(text='查看更多2')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0759(self):
        """本地联系人为空的情况，搜索时，不展示手机联系人搜索结果标签"""
        contact = ContactsPage()
        contact.click_search_box()
        time.sleep(1)
        contact.input_search_text('群聊')
        time.sleep(2)
        contact.page_down()
        contact.page_should_not_contain_text('手机联系人')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0760(self):
        """没有企业的或者企业通讯录无返回结果的情况，搜索时，不展示和通讯录搜索结果标签"""
        contact = ContactsPage()
        contact.click_search_box()
        time.sleep(1)
        contact.input_search_text('给个红包')
        time.sleep(2)
        contact.page_down()
        contact.page_should_not_contain_text('团队联系人')


class GroupAssistant(TestCase):
    """通讯录-群发助手"""

    def default_setUp(self):
        """确保每个用例运行前在消息人页面"""
        warnings.simplefilter('ignore',ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load()

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_chenjixiang_0529(self):
        """测试群发助手消息窗口，内容输入框有内容时，发送按钮状态"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击+
        mess.click_add_icon()
        time.sleep(1)
        # 2.点击群发助手
        mess.click_group_assistant()
        gap = GroupAssistantPage()
        # 3.若在资费介绍页，点击确定
        if gap.is_on_group_assistant_tariff():
            gap.click_sure()
        # 4.输入框输入内容
        gap.click_input_box()
        gap.input_message_text("群发助手发送测试")
        # 5.选择收件人
        gap.click_addressee()
        time.sleep(2)
        gap.select_contacts_by_name("大佬1")
        # 6.点击确定
        gap.click_sure()
        # 7.点击发送
        gap.click_send()
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_chenjixiang_0533(self):
        """测试联系人选择器，搜索框校验，输入多位数字进行搜索"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击+
        mess.click_add_icon()
        time.sleep(1)
        # 2.点击群发助手
        mess.click_group_assistant()
        gap = GroupAssistantPage()
        # 3.若在资费介绍页，点击确定
        if gap.is_on_group_assistant_tariff():
            gap.click_sure()
        # 4.选择收件人
        gap.click_addressee()
        time.sleep(2)
        # 5.输入多位数字进行搜索
        gap.input_search_message("13800138005")
        # 6.验证是否存在匹配结果
        self.assertTrue(gap.is_text_contain_present("13800138005"))
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_chenjixiang_0534(self):
        """测试联系人选择器，搜索框校验，输入中文字符进行搜索"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击+
        mess.click_add_icon()
        time.sleep(1)
        # 2.点击群发助手
        mess.click_group_assistant()
        gap = GroupAssistantPage()
        # 3.若在资费介绍页，点击确定
        if gap.is_on_group_assistant_tariff():
            gap.click_sure()
        # 4.选择收件人
        gap.click_addressee()
        time.sleep(2)
        # 5.输入中文字符进行搜索
        gap.input_search_message("飞信电话")
        # 6.验证是否存在匹配结果
        self.assertTrue(gap.is_text_contain_present("飞信电话"))
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_chenjixiang_0535(self):
        """测试联系人选择器，搜索框校验，输入英文字符进行搜索"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击+
        mess.click_add_icon()
        time.sleep(1)
        # 2.点击群发助手
        mess.click_group_assistant()
        gap = GroupAssistantPage()
        # 3.若在资费介绍页，点击确定
        if gap.is_on_group_assistant_tariff():
            gap.click_sure()
        # 4.选择收件人
        gap.click_addressee()
        time.sleep(2)
        # 5.输入多个英文字符
        gap.input_search_message("English")
        # 6.验证是否存在匹配结果
        self.assertTrue(gap.is_text_contain_present("English"))
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_chenjixiang_0536(self):
        """测试联系人选择器，搜索框校验，输入其他特殊字符进行搜索"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击+
        mess.click_add_icon()
        time.sleep(1)
        # 2.点击群发助手
        mess.click_group_assistant()
        gap = GroupAssistantPage()
        # 3.若在资费介绍页，点击确定
        if gap.is_on_group_assistant_tariff():
            gap.click_sure()
        # 4.选择收件人
        gap.click_addressee()
        time.sleep(2)
        # 5.输入特殊字符
        gap.input_search_message("!@$")
        # 6.验证是否存在匹配结果
        self.assertTrue(gap.is_text_contain_present("特殊!@$"))
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_chenjixiang_0537(self):
        """测试联系人选择器，搜索框校验，输入组合字符（中英文、数字、特殊字符）进行搜索"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击+
        mess.click_add_icon()
        time.sleep(1)
        # 2.点击群发助手
        mess.click_group_assistant()
        gap = GroupAssistantPage()
        # 3.若在资费介绍页，点击确定
        if gap.is_on_group_assistant_tariff():
            gap.click_sure()
        # 4.选择收件人
        gap.click_addressee()
        time.sleep(2)
        # 5.输入组合字符
        gap.input_search_message("Li@1大佬")
        # 6.验证是否存在匹配结果
        self.assertTrue(gap.is_text_contain_present("Li@1大佬"))
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_chenjixiang_0672(self):
        """测试群发消息输入框录入页面，发送成功后跳转到历史记录页"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击+
        mess.click_add_icon()
        time.sleep(1)
        # 2.点击群发助手
        mess.click_group_assistant()
        gap = GroupAssistantPage()
        # 3.若在资费介绍页，点击确定
        if gap.is_on_group_assistant_tariff():
            gap.click_sure()
        # 4.输入框输入内容
        gap.click_input_box()
        gap.input_message_text("群发助手发送测试")
        # 5.选择收件人
        gap.click_addressee()
        time.sleep(2)
        gap.select_contacts_by_name("大佬1")
        gap.select_contacts_by_name("大佬2")
        # 6.点击确定
        gap.click_sure()
        # 7.点击发送
        gap.click_send()
        # 8.验证是否在消息记录页面
        self.assertTrue(gap.is_on_message_record_page())
        time.sleep(2)


if __name__=="__main__":
    unittest.main()

import unittest
import time
import warnings
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from pages.workbench.create_group.CreateGroup import CreateGroupPage
from pages.workbench.group_messenger.SelectCompanyContacts import SelectCompanyContactsPage
from preconditions.BasePreconditions import LoginPreconditions,WorkbenchPreconditions
from library.core.utils.testcasefilter import tags
from pages.chat.chatfileProview import ChatfileProviewPage
from pages.contacts.my_group import ALLMyGroup

from pages import *
from selenium.common.exceptions import TimeoutException

import re
import random
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from pages.contacts.AllMyTeam import AllMyTeamPage




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
    def enter_enterprise_group_chatwindow_with_AB(type='IOS-移动', name='双机企业群1'):
        """
        确保进入双机企业群聊天会话页面（A 手机是群主 B手机是群成员）
        默认入口关系：消息列表-->通讯录群聊入口-->创建企业群
        """
        # 连接A手机 判断是否存在双机群聊（不存在就创建双机企业群）
        Preconditions.select_mobile(type)
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        if mess.is_text_present(name):
            mess.click_text(name)
        else:
            Preconditions.creat_enterprise_group()

    @staticmethod
    def make_sure_message_list_have_enterprise_group_record(name='双机企业群1'):
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        time.sleep(2)
        if mess.is_text_present(name):
            mess.wait_for_page_load()
        else:
            mess.click_add_icon()
            # 点击发起群聊
            mess.click_group_chat()
            scg = SelectContactsPage()
            scg.wait_for_page_load()
            scg.click_select_one_group()
            sog = SelectOneGroupPage()
            # 等待“选择一个群”页面加载
            sog.wait_for_page_load()
            # 选择一个普通群
            sog.selecting_one_group_by_name('双机企业群1')
            gcp = GroupChatPage()
            gcp.wait_for_page_load()
            gcp.send_mutiple_message(times=1)
            Preconditions.make_already_in_message_page()


    @staticmethod
    def creat_enterprise_group(type1='IOS-移动', type2='IOS-移动-移动', name='双机企业群1'):
        """创建双机企业群(A 是群主 B是群成员)-没有就创建（有就进入聊天页面）"""
        # 连接B手机 获取B手机的电话号码
        Preconditions.select_mobile(type2)
        Preconditions.make_already_in_message_page()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 切换到A手机创建群聊
        Preconditions.select_mobile(type1)
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        MessagePage().open_contacts_page()
        con = ContactsPage()
        con.open_group_chat_list()
        my_group = ALLMyGroup()
        if my_group.page_should_contain_text2(name):
            my_group.select_group_by_name(name)
        else:
            my_group.click_back()
            con.open_workbench_page()
            work = WorkbenchPage()
            work.wait_for_page_load()
            work.page_up()
            work.click_add_create_group()
            # 进入创建群页面
            cgp = CreateGroupPage()
            cgp.wait_for_page_load()
            time.sleep(7)
            cgp.click_create_group()
            # 进入选择联系人页面
            sccp = SelectCompanyContactsPage()
            sccp.click_name_attribute_by_name('大佬1', "xpath")
            sccp.click_name_attribute_by_name(phone_number_B, "xpath")
            sccp.click_sure_button()
            # 进入创建群命名界面
            cgp.input_group_name(name)
            # 收起键盘
            cgp.click_name_attribute_by_name("完成")
            cgp.click_create_group()
            time.sleep(2)
            # 点击【马上发起群聊-进入聊天界面
            cgp.click_name_attribute_by_name("发起群聊")
            time.sleep(2)


class EnterpriseGroupDouble(TestCase):
    """企业群--双机用例"""

    @classmethod
    def setUpClass(cls):
        """企业群添加联系人 备用手机的手机号"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 连接B手机 获取B手机的电话号码
        Preconditions.select_mobile("IOS-移动-移动")
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 进入A手机的团队联系人列表
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        # 为团队 ateam7272 添加联系人
        Preconditions.make_already_in_message_page()
        contact = [(phone_number_B, phone_number_B)]
        Preconditions.create_he_contacts2(contact)
        # 创建群双机企业群
        Preconditions.creat_enterprise_group()


    def setUp_test_msg_huangmianhua_0002(self):
        # A手机创建企业群-双机企业群1
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_enterprise_group_chatwindow_with_AB()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0002(self):
        """全局搜索入口——搜索企业群/党群名称默认的三个结果,普通成员在群聊设置页没有拉人“+”和踢人“-”按钮"""
        # B手机进入企业群，查看页面展示
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        msg.click_search_box()
        name = '双机企业群1'
        msg.input_search_text(name)
        msg.click_element_first_list()
        time.sleep(2)
        # B（普通成员）进入聊天界面-设置界面
        chat = ChatWindowPage()
        chat.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        # 验证点：没有拉人+ 和踢人的 - 按钮（有添加按钮 无删除联系人按钮）
        time.sleep(2)
        self.assertTrue(group_set.is_exit_element(locator='添加成员'))
        self.assertFalse(group_set.is_exit_element(locator='删除成员'))

    def tearDown_test_msg_huangmianhua_0002(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_huangmianhua_0014(self):
        # A手机创建企业群-双机企业群1
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_enterprise_group_chatwindow_with_AB()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0014(self):
        """消息--右上角“+”--发起群聊--选择一个群——选择一个企业群/党群,普通成员在群聊设置页没有拉人“+”和踢人“-”按钮"""
        # B手机消息页面右上角点击'+'，进入企业群
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        name = '双机企业群1'
        msg.click_add_icon()
        msg.click_group_chat()
        select = SelectContactsPage()
        select.click_select_one_group()
        select_group = SelectOneGroupPage()
        select_group.wait_for_page_load()
        select_group.selecting_one_group_by_name(name)
        time.sleep(2)
        # B（普通成员）进入聊天界面-设置界面
        chat = ChatWindowPage()
        chat.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        # 验证点：没有拉人+ 和踢人的 - 按钮（有添加按钮 无删除联系人按钮）
        time.sleep(2)
        self.assertTrue(group_set.is_exit_element(locator='添加成员'))
        self.assertFalse(group_set.is_exit_element(locator='删除成员'))

    def tearDown_test_msg_huangmianhua_0014(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_huangmianhua_0019(self):
        # A手机创建企业群-双机企业群1
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_enterprise_group_chatwindow_with_AB()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0019(self):
        """消息列表入口,普通成员在群聊设置页没有拉人“+”和踢人“-”按钮"""
        # 确保B手机有消息记录
        chat = ChatWindowPage()
        chat.click_input_box()
        chat.input_message_text('群聊消息')
        chat.click_send_button()
        # B手机从消息列表进入
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        msg.wait_for_page_load_new_message_coming()
        name = '双机企业群1'
        msg.click_text(name)
        time.sleep(2)
        # B（普通成员）进入聊天界面-设置界面
        chat = ChatWindowPage()
        chat.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        # 验证点：没有拉人+ 和踢人的 - 按钮（有添加按钮 无删除联系人按钮）
        time.sleep(2)
        self.assertTrue(group_set.is_exit_element(locator='添加成员'))
        self.assertFalse(group_set.is_exit_element(locator='删除成员'))


    def tearDown_test_msg_huangmianhua_0019(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



    def setUp_test_msg_huangmianhua_0030(self):
        # A手机创建企业群-双机企业群1
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_enterprise_group_chatwindow_with_AB()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0030(self):
        """企业群/党群在消息列表内展示——最新消息展示"""
        # 自己发出消息，查看消息列表显示
        chat = ChatWindowPage()
        chat.click_input_box()
        text = '企业群消息'
        chat.input_message_text(text)
        chat.click_send_button()
        # 查看消息列表展示
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        time.sleep(2)
        self.assertTrue(msg.is_message_content_match_message_name(text))
        # B（普通成员）进入聊天界面-发送文本消息，查看A收到消息时，列表显示
        chat = ChatWindowPage()
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        MessagePage().click_text('双机企业群1')
        time.sleep(2)
        message = '消息'
        chat.input_message_text(message)
        chat.click_send_button()
        # 切换到A手机，查看A手机的列表显示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load_new_message_coming()
        text=phone_number_B[:2]
        MessagePage().page_should_contain_text(text)
        MessagePage().page_should_contain_text(message)

    def tearDown_test_msg_huangmianhua_0030(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_huangmianhua_0032(self):
        # A手机创建企业群-双机企业群1
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_enterprise_group_chatwindow_with_AB()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0032(self):
        """企业群/党群在消息列表内展示——最新消息展示——语音消息"""
        # 自己发出语言消息，查看消息列表显示
        chat = ChatWindowPage()
        chat.send_voice()
        # 查看消息列表展示
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        time.sleep(2)
        msg.page_should_contain_text('语音')
        msg.page_should_contain_text('我:')
        # B（普通成员）进入聊天界面-发送语音消息，查看A收到消息时，列表显示
        chat = ChatWindowPage()
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        MessagePage().click_text('双机企业群1')
        time.sleep(2)
        chat.send_voice()
        # 切换到A手机，查看A手机的列表显示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load_new_message_coming()
        text=phone_number_B[:2]
        MessagePage().page_should_contain_text(text)
        MessagePage().page_should_contain_text('语音')

    def tearDown_test_msg_huangmianhua_0032(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_huangmianhua_0033(self):
        # A手机创建企业群-双机企业群1
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_enterprise_group_chatwindow_with_AB()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0033(self):
        """企业群/党群在消息列表内展示——最新消息展示——图片消息"""
        # 自己发出图片消息，查看消息列表显示
        chat = ChatWindowPage()
        chat.send_pic()
        # 查看消息列表展示
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        time.sleep(2)
        msg.page_should_contain_text('图片')
        msg.page_should_contain_text('我:')
        # B（普通成员）进入聊天界面-发送图片消息，查看A收到消息时，列表显示
        chat = ChatWindowPage()
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        MessagePage().click_text('双机企业群1')
        time.sleep(2)
        chat.send_voice()
        # 切换到A手机，查看A手机的列表显示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load_new_message_coming()
        text = phone_number_B[:2]
        MessagePage().page_should_contain_text(text)
        MessagePage().page_should_contain_text('图片')

    def tearDown_test_msg_huangmianhua_0033(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_huangmianhua_0034(self):
        # A手机创建企业群-双机企业群1
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_enterprise_group_chatwindow_with_AB()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0034(self):
        """企业群/党群在消息列表内展示——最新消息展示——表情消息"""
        # 自己发出表情消息，查看消息列表显示
        chat = ChatWindowPage()
        chat.send_mutiple_message(content='[微笑1]', times=1)
        # 查看消息列表展示
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        time.sleep(2)
        msg.page_should_contain_text('[微笑1]')
        msg.page_should_contain_text('我:')
        # B（普通成员）进入聊天界面-发送表情消息，查看A收到消息时，列表显示
        chat = ChatWindowPage()
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        MessagePage().click_text('双机企业群1')
        time.sleep(2)
        chat.send_voice()
        # 切换到A手机，查看A手机的列表显示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load_new_message_coming()
        text = phone_number_B[:2]
        MessagePage().page_should_contain_text(text)
        MessagePage().page_should_contain_text('[微笑1]')

    def tearDown_test_msg_huangmianhua_0034(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_huangmianhua_0035(self):
        # A手机创建企业群-双机企业群1
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_enterprise_group_chatwindow_with_AB()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0035(self):
        """企业群/党群在消息列表内展示——最新消息展示——表情消息"""
        # 自己发出表情消息，查看消息列表显示
        chat = ChatWindowPage()
        chat.send_video()
        time.sleep(2)
        # 查看消息列表展示
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        time.sleep(2)
        msg.page_should_contain_text('视频')
        msg.page_should_contain_text('我:')
        # B（普通成员）进入聊天界面-发送表情消息，查看A收到消息时，列表显示
        chat = ChatWindowPage()
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        MessagePage().click_text('双机企业群1')
        time.sleep(2)
        chat.send_voice()
        # 切换到A手机，查看A手机的列表显示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load_new_message_coming()
        text = phone_number_B[:2]
        MessagePage().page_should_contain_text(text)
        MessagePage().page_should_contain_text('视频')

    def tearDown_test_msg_huangmianhua_0035(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_huangmianhua_0036(self):
        # A手机创建企业群-双机企业群1
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_enterprise_group_chatwindow_with_AB()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0036(self):
        """企业群/党群在消息列表内展示——最新消息展示——富媒体-本地文件"""
        # 自己发出语言消息，查看消息列表显示
        chat = ChatWindowPage()
        chat.send_file()
        time.sleep(2)
        file_name = chat.get_file_name()
        # 查看消息列表展示
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        time.sleep(2)
        msg.page_should_contain_text('文件')
        msg.page_should_contain_text('我:')
        msg.page_should_contain_text(file_name)
        # B（普通成员）进入聊天界面-发送图片消息，查看A收到消息时，列表显示
        chat = ChatWindowPage()
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        MessagePage().click_text('双机企业群1')
        time.sleep(2)
        chat.send_file()
        time.sleep(2)
        file_name2 = chat.get_file_name()
        # 切换到A手机，查看A手机的列表显示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load_new_message_coming()
        text=phone_number_B[:2]
        MessagePage().page_should_contain_text(text)
        MessagePage().page_should_contain_text('文件')
        msg.page_should_contain_text(file_name)

    def tearDown_test_msg_huangmianhua_0036(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_huangmianhua_0037(self):
        # A手机创建企业群-双机企业群1
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_enterprise_group_chatwindow_with_AB()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0037(self):
        """企业群/党群在消息列表内展示——最新消息展示——富媒体-视频"""
        # 自己发出语言消息，查看消息列表显示
        chat = ChatWindowPage()
        chat.send_video()
        # 查看消息列表展示
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        time.sleep(2)
        msg.page_should_contain_text('视频')
        msg.page_should_contain_text('我:')
        # B（普通成员）进入聊天界面-发送图片消息，查看A收到消息时，列表显示
        chat = ChatWindowPage()
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        MessagePage().click_text('双机企业群1')
        time.sleep(2)
        chat.send_video()
        # 切换到A手机，查看A手机的列表显示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load_new_message_coming()
        text=phone_number_B[:2]
        MessagePage().page_should_contain_text(text)
        MessagePage().page_should_contain_text('视频')

    def tearDown_test_msg_huangmianhua_0037(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_huangmianhua_0038(self):
        # A手机创建企业群-双机企业群1
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_enterprise_group_chatwindow_with_AB()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0038(self):
        """企业群/党群在消息列表内展示——最新消息展示——富媒体-图片、拍照"""
        # 自己发出语言消息，查看消息列表显示
        chat = ChatWindowPage()
        chat.send_pic()
        # 查看消息列表展示
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        time.sleep(2)
        msg.page_should_contain_text('图片')
        msg.page_should_contain_text('我:')
        # B（普通成员）进入聊天界面-发送图片消息，查看A收到消息时，列表显示
        chat = ChatWindowPage()
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        MessagePage().click_text('双机企业群1')
        time.sleep(2)
        chat.send_pic()
        # 切换到A手机，查看A手机的列表显示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load_new_message_coming()
        text=phone_number_B[:2]
        MessagePage().page_should_contain_text(text)
        MessagePage().page_should_contain_text('图片')

    def tearDown_test_msg_huangmianhua_0038(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_huangmianhua_0039(self):
        # A手机创建企业群-双机企业群1
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_enterprise_group_chatwindow_with_AB()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0039(self):
        """企业群/党群在消息列表内展示——最新消息展示——富媒体-音乐"""
        # 自己发出语言消息，查看消息列表显示
        chat = ChatWindowPage()
        chat.send_file(type='.mp3')
        time.sleep(2)
        file_name = chat.get_file_name()
        # 查看消息列表展示
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        time.sleep(2)
        msg.page_should_contain_text('文件')
        msg.page_should_contain_text('我:')
        msg.page_should_contain_text(file_name)
        # B（普通成员）进入聊天界面-发送音乐消息，查看A收到消息时，列表显示
        chat = ChatWindowPage()
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        MessagePage().click_text('双机企业群1')
        time.sleep(2)
        chat.send_file(type='.mp3')
        time.sleep(2)
        file_name2 = chat.get_file_name()
        # 切换到A手机，查看A手机的列表显示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load_new_message_coming()
        text=phone_number_B[:2]
        MessagePage().page_should_contain_text(text)
        MessagePage().page_should_contain_text('文件')
        msg.page_should_contain_text(file_name)

    def tearDown_test_msg_huangmianhua_0039(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_huangmianhua_0040(self):
        # A手机创建企业群-双机企业群1
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_enterprise_group_chatwindow_with_AB()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0040(self):
        """企业群/党群在消息列表内展示——最新消息展示——位置"""
        # 自己发出语言消息，查看消息列表显示
        chat = ChatWindowPage()
        chat.send_locator()
        time.sleep(2)
        # 查看消息列表展示
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        time.sleep(2)
        msg.page_should_contain_text('位置')
        msg.page_should_contain_text('我:')
        # B（普通成员）进入聊天界面-发送位置消息，查看A收到消息时，列表显示
        chat = ChatWindowPage()
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        MessagePage().click_text('双机企业群1')
        time.sleep(2)
        chat.send_locator()
        # 切换到A手机，查看A手机的列表显示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load_new_message_coming()
        text=phone_number_B[:2]
        MessagePage().page_should_contain_text(text)
        MessagePage().page_should_contain_text('位置')

    def tearDown_test_msg_huangmianhua_0040(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0042(self):
        """企业群/党群在消息列表内展示——最新消息展示——被艾特"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 获取B手机号
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 切换到A手机 进入A手机的聊天窗口
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_enterprise_group_chatwindow_with_AB()
        # 切换到A手机@B 手机，查看消息列表显示
        chat = ChatWindowPage()
        chat.click_input_box()
        chat.input_message_text('@')
        time.sleep(2)
        chat.select_members_by_name(name=phone_number_B)
        time.sleep(2)
        chat.click_send_button()
        time.sleep(2)
        nickname = chat.get_members_nickname()
        # 切换到B 手机，查看消息列表展示
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load_new_message_coming()
        time.sleep(3)
        MessagePage().page_should_contain_text('有人@我')
        MessagePage().page_should_contain_text(nickname)

    def tearDown_test_msg_huangmianhua_0042(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_huangmianhua_0044(self):
        # A手机创建企业群-双机企业群1
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_enterprise_group_chatwindow_with_AB()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0044(self):
        """企业群/党群在消息列表内展示——最新消息展示——撤回"""
        # 自己发出消息后撤回，查看消息列表显示
        chat = ChatWindowPage()
        chat.send_file()
        time.sleep(2)
        nickname = chat.get_members_nickname()
        #长按撤回
        chat.swipe_by_percent_on_screen(50, 30, 70, 30)
        chat.click_revoke()
        time.sleep(2)
        # 查看消息列表展示
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        time.sleep(2)
        msg.page_should_contain_text('你撤回了一条消息')
        # B（普通成员）进入聊天界面，查看列表显示
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load_new_message_coming()
        MessagePage().page_should_contain_text('撤回了一条消息')
        MessagePage().page_should_contain_text(nickname)

    def tearDown_test_msg_huangmianhua_0044(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_huangmianhua_0067(self):
        # 群成员进入聊天会话页面
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        my_group.select_group_by_name('双机企业群1')
        time.sleep(2)

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0067(self):
        """通讯录——群聊入口——群聊列表入口,普通成员在群聊设置页没有拉人“+”和踢人“-”按钮"""
        # B（普通成员）进入聊天界面-设置界面
        chat = ChatWindowPage()
        chat.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        # 验证点：没有拉人+ 和踢人的 - 按钮（有添加按钮 无删除联系人按钮）
        time.sleep(2)
        self.assertTrue(group_set.is_exit_element(locator='添加成员'))
        self.assertFalse(group_set.is_exit_element(locator='删除成员'))

    def tearDown_test_msg_huangmianhua_0067(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_huangmianhua_0073(self):
        # 群成员B手机进入聊天会话页面
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0073(self):
        """通讯录——群聊入口——搜索群组结果入口,普通成员在群聊设置页没有拉人“+”和踢人“-”按钮"""
        # 通讯录——群聊入口——搜索群组结果入口
        MessagePage().open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group=ALLMyGroup()
        my_group.click_search_box()
        my_group.input_search_keyword('双机企业群1')
        time.sleep(2)
        my_group.click_search_result()
        # B（普通成员）进入聊天界面-设置界面
        chat = ChatWindowPage()
        chat.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        # 验证点：没有拉人+ 和踢人的 - 按钮（有添加按钮 无删除联系人按钮）
        time.sleep(2)
        self.assertTrue(group_set.is_exit_element(locator='添加成员'))
        self.assertFalse(group_set.is_exit_element(locator='删除成员'))

    def tearDown_test_msg_huangmianhua_0073(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_huangmianhua_0121(self):
        # A手机创建企业群-双机企业群1
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_enterprise_group_chatwindow_with_AB()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0121(self):
        """群聊设置页面——开启消息免打扰"""
        # 群聊设置页面 开启消息免打扰
        chat = ChatWindowPage()
        chat.click_setting()
        set = GroupChatSetPage()
        if set.get_switch_undisturb_value() == '0':
            set.click_switch_undisturb()
        Preconditions.make_already_in_message_page()
        # # 1、点击打开消息免打扰开关，可以开启消息免打扰的开关
        mess = MessagePage()
        # 切换到B手机，发送消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        mess.open_contacts_page()
        con = ContactsPage()
        con.open_group_chat_list()
        my_group = ALLMyGroup()
        group_name = '双机企业群1'
        my_group.select_group_by_name(group_name)
        time.sleep(2)
        chat.send_mutiple_message(times=1)
        # 2、返回到消息列表，接收到新消息时，会话窗口上方会展示红点,不展示数量并且还会有一个被划掉的小铃铛
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(6)
        self.assertTrue(mess.is_exist_news_red_dot())
        self.assertFalse(mess.is_exist_unread_make_and_number())
        # 3、进入到聊天会话窗口页面，左上角的群名称右边会同样展示一个被划掉的小铃铛
        mess.click_text(group_name)
        time.sleep(2)
        self.assertTrue(chat.is_exist_no_disturb_icon())
        chat.click_back()
        self.assertTrue(mess.is_exist_no_disturb_icon())
        # 去除A手机的消息免打扰
        mess.click_text(group_name)
        chat.click_setting()
        time.sleep(2)
        if set.get_switch_undisturb_value() == '1':
            set.click_switch_undisturb()
        time.sleep(2)

    def tearDown_test_msg_huangmianhua_0121(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_huangmianhua_0122(self):
        # A手机创建企业群-双机企业群1
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_enterprise_group_chatwindow_with_AB()
        # 开启手机的消息免打扰
        chat = ChatWindowPage()
        chat.click_setting()
        set = GroupChatSetPage()
        if set.get_switch_undisturb_value() == '0':
            set.click_switch_undisturb()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0122(self):
        """群聊设置页面——开启消息免打扰"""
        chat = ChatWindowPage()
        # 群聊设置页面 关闭消息免打扰
        time.sleep(2)
        set = GroupChatSetPage()
        if set.get_switch_undisturb_value() == '1':
            set.click_switch_undisturb()
        Preconditions.make_already_in_message_page()
        # # 1、点击打开消息免打扰开关，可以开启消息免打扰的开关
        mess = MessagePage()
        # 切换到B手机，发送消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        mess.open_contacts_page()
        con = ContactsPage()
        con.open_group_chat_list()
        my_group = ALLMyGroup()
        group_name = '双机企业群1'
        my_group.select_group_by_name(group_name)
        time.sleep(2)
        chat.send_mutiple_message(times=1)
        # 2、返回到消息列表，接收到新消息时，会话窗口上方会展示数量，不展示红点，同样开启了声音、震动提醒的也会发出提声音和震动
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        self.assertFalse(mess.is_exist_news_red_dot())
        self.assertTrue(mess.is_exist_unread_make_and_number())

    def tearDown_test_msg_huangmianhua_0122(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0158(self):
        """群聊天会话页面——输入框输入@字符——@联系人"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 获取B手机号
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 切换到A手机 进入A手机的聊天窗口
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_enterprise_group_chatwindow_with_AB()
        # 1、在群聊天会话窗口页面
        chat = ChatWindowPage()
        self.assertTrue(chat.is_on_this_page())
        # 2、在输入框中，输入@字符，会调起联系人选择器页面
        chat.click_input_box()
        chat.input_message_text('@')
        time.sleep(2)
        chat.page_should_contain_text('选择群成员')
        chat.select_members_by_name(name=phone_number_B)
        time.sleep(2)
        # 3、选择一个联系人后，会自动返回到聊天会话页面并且在输入框中展示选中联系人的信息
        self.assertTrue(chat.is_on_this_page())
        text = '@' + phone_number_B + ' '
        message = chat.get_input_message()
        self.assertEqual(text, message)
        # 4、点击右边的发送按钮，发送出去后，被@的联系人会在消息列表收到@提示
        chat.click_send_button()
        time.sleep(2)
        nickname = chat.get_members_nickname()
        # 切换到B 手机，查看消息列表展示
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load_new_message_coming()
        time.sleep(3)
        MessagePage().page_should_contain_text('有人@我')
        MessagePage().page_should_contain_text(nickname)

    def tearDown_test_msg_huangmianhua_0158(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0159(self):
        """群聊天会话页面——长按聊天会话窗口中发送消息的联系人头像——可以发起@"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 获取A手机的手机号
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_enterprise_group_chatwindow_with_AB()
        # 确保手机聊天界面有消息记录
        chat = ChatWindowPage()
        chat.click_input_box()
        chat.input_message_text('message')
        time.sleep(2)
        chat.click_send_button()
        time.sleep(2)
        nick_name = chat.get_members_nickname()
        # 切换到B 手机，查看消息列表展示
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load_new_message_coming()
        time.sleep(3)
        MessagePage().click_text('双机企业群1')
        # 2、长按消息发送人的头像，可以调起@功能并把@内容展示到输入框中
        chat.swipe_by_percent_on_screen(7, 16, 10, 17)
        text = '@' + nick_name + ' '
        message = chat.get_input_message()
        self.assertEqual(text, message)

    def tearDown_test_msg_huangmianhua_0159(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0160(self):
        """消息列表页面——有人@我——会话窗口状态展示"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 获取B手机号
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 1、在消息列表有人 @ 我的时，是否会在消息列表 @ 我的会话窗口展示红色字体提示：有人 @ 我
        # 切换到A手机 @B手机
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_enterprise_group_chatwindow_with_AB()
        chat = ChatWindowPage()
        chat.click_input_box()
        chat.input_message_text('@')
        time.sleep(2)
        chat.select_members_by_name(name=phone_number_B)
        time.sleep(2)
        chat.click_send_button()
        chat.send_mutiple_message()
        time.sleep(2)
        # 切换到B 手机，查看消息列表展示
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        # MessagePage().wait_for_page_load_new_message_coming()
        time.sleep(3)
        message = '有人@我'
        MessagePage().page_should_contain_text(message)
        # 2、进入到聊天会话页面，是否会在会话页面右边栏展示有人 @ 我的快捷定位方式，点击即可定位到 @ 我的页面（判断是否定位到@我页面无法判断，发送文本的ID 无法获取）
        MessagePage().click_text('双机企业群1')
        time.sleep(2)
        chat.page_should_contain_text(message)
        time.sleep(1)
        chat.click_text(message)
        time.sleep(2)
        # 3、多人@我时，进入到聊天会话页面，可以定位所有@我的位置---涉及到多机操作，暂时无法实现
        # 4、有人@我，另一个人发一条消息再撤回，查看消息列表页面  有人@我 提示会消失---涉及到多机操作，暂时无法实现

    def tearDown_test_msg_huangmianhua_0160(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_huangmianhua_0161(self):
        warnings.simplefilter('ignore', ResourceWarning)
        # 获取B手机号
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 1、在消息列表有人 @ 我的时，是否会在消息列表 @ 我的会话窗口展示红色字体提示：有人 @ 我
        # 切换到A手机 @B手机
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_enterprise_group_chatwindow_with_AB()
        chat = ChatWindowPage()
        chat.click_input_box()
        chat.input_message_text('@')
        time.sleep(2)
        chat.select_members_by_name(name=phone_number_B)
        time.sleep(2)
        chat.click_send_button()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0161(self):
        """消息列表页面——有人@我——然后撤回@消息"""
        time.sleep(2)
        # 切换到B 手机，查看消息列表展示
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        # MessagePage().wait_for_page_load_new_message_coming()
        time.sleep(3)
        message = '有人@我'
        MessagePage().page_should_contain_text(message)
        # 切换到A手机，撤回消息
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().click_text('双机企业群1')
        time.sleep(2)
        chat = ChatWindowPage()
        chat.swipe_by_percent_on_screen(85, 20, 93, 20)
        time.sleep(2)
        chat.click_revoke()
        time.sleep(2)
        # 1、验证点变动：有人@我后再撤回@我的消息，查看消息列表页不会存在提示 有人@我----存在提示
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_contain_text('撤回了一条消息')

    def tearDown_test_msg_huangmianhua_0161(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_huangmianhua_0163(self):
        warnings.simplefilter('ignore', ResourceWarning)
        # 获取B手机号
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 1、在消息列表有人 @ 我的时，是否会在消息列表 @ 我的会话窗口展示红色字体提示：有人 @ 我
        # 切换到A手机 @B手机
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_enterprise_group_chatwindow_with_AB()
        chat = ChatWindowPage()
        chat.click_input_box()
        chat.input_message_text('@')
        time.sleep(2)
        chat.select_members_by_name(name=phone_number_B)
        time.sleep(2)
        chat.click_send_button()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0163(self):
        """消息列表页面——有人@我——然后撤回@消息"""
        time.sleep(2)
        # 切换到B 手机，查看消息列表展示
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        # MessagePage().wait_for_page_load_new_message_coming()
        time.sleep(3)
        message = '有人@我'
        MessagePage().page_should_contain_text(message)
        # 切换到A手机，撤回消息
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().click_text('双机企业群1')
        time.sleep(2)
        chat = ChatWindowPage()
        chat.swipe_by_percent_on_screen(85, 20, 93, 20)
        time.sleep(2)
        chat.click_revoke()
        time.sleep(2)
        # 1、验证点变动：有人@我后再撤回@我的消息，查看消息列表页不会存在提示 有人@我----存在提示
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_contain_text('撤回了一条消息')

    def tearDown_test_msg_huangmianhua_0163(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_huangmianhua_0366(self):
        # 群成员进入聊天会话页面
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.click_add_icon()
        # 点击发起群聊
        mess.click_group_chat()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name('双机企业群1')
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0366(self):
        """消息-右上角-选择一个群-选择一个企业群,普通成员在群聊设置页没有拉人“+”和踢人“-”按钮"""
        # B（普通成员）进入聊天界面-设置界面
        chat = ChatWindowPage()
        chat.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        # 验证点：没有拉人+ 和踢人的 - 按钮（有添加按钮 无删除联系人按钮）
        time.sleep(2)
        self.assertTrue(group_set.is_exit_element(locator='添加成员'))
        self.assertFalse(group_set.is_exit_element(locator='删除成员'))

    def tearDown_test_msg_huangmianhua_0366(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_huangmianhua_0371(self):
        # 群成员B手机进入聊天会话页面
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_sure_message_list_have_enterprise_group_record()

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0371(self):
        """消息列表入口,普通成员在群聊设置页没有拉人“+”和踢人“-”按钮"""
        # 从消息列表入口进入
        MessagePage().click_text('双机企业群1')
        # B（普通成员）进入聊天界面-设置界面
        chat = ChatWindowPage()
        chat.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        # 验证点：没有拉人+ 和踢人的 - 按钮（有添加按钮 无删除联系人按钮）
        time.sleep(2)
        self.assertTrue(group_set.is_exit_element(locator='添加成员'))
        self.assertFalse(group_set.is_exit_element(locator='删除成员'))

    def tearDown_test_msg_huangmianhua_0371(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_huangmianhua_0382(self):
        # 群主A手机进入聊天会话页面
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_enterprise_group_chatwindow_with_AB('IOS-移动-移动')

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0382(self):
        """企业群/党群在消息列表内展示——最新消息展示"""
        # 1.自己发出不展示自己姓名(iOS显示为“我：<消息内容>”)
        chat = GroupChatPage()
        mess = MessagePage()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        chat.send_mutiple_message(text='文本消息', times=1)
        Preconditions.make_already_in_message_page()
        mess.page_should_contain_text('我')
        mess.page_should_contain_text('文本消息')
        # 2.别人发出展示群昵称(没昵称时显示隐藏号码)
        Preconditions.select_mobile('IOS-移动')
        mess.wait_for_page_load()
        name = phone_number_B[:3] + '*'*8
        mess.page_should_contain_text(name)
        mess.page_should_contain_text('文本消息')

    def tearDown_test_msg_huangmianhua_0382(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_huangmianhua_0394(self):
        # 群主A手机进入聊天会话页面
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_enterprise_group_chatwindow_with_AB(type='IOS-移动')

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0394(self):
        """企业群/党群在消息列表内展示——最新消息展示"""
        # 1.自己发出不展示自己姓名(iOS显示为“我：<消息内容>”)
        chat = GroupChatPage()
        mess = MessagePage()
        # 获取A手机的和飞信显示名称
        chat.click_setting()
        name = GroupChatSetPage().get_my_name_in_this_group()
        # 切换到B手机 输入框@A手机
        Preconditions.enter_enterprise_group_chatwindow_with_AB(type='IOS-移动-移动')
        chat.click_setting()
        name_B = GroupChatSetPage().get_my_name_in_this_group()
        GroupChatSetPage().click_back()
        chat.click_input_box()
        chat.input_message_text('@')
        chat.select_members_by_name(name)
        time.sleep(2)
        chat.click_send_button()
        # 有人艾特我的未读消息展示：红色的“[有人@我]”标识+对方群昵称+消息内容（消息内容为：@+本人群昵称）（收）
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess.wait_for_page_load()
        time.sleep(3)
        mess.page_should_contain_text('有人@我')
        name = name_B[:3] + '*' * 8
        mess.page_should_contain_text(name)


    def tearDown_test_msg_huangmianhua_0394(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


import unittest
import time
import warnings
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from preconditions.BasePreconditions import LoginPreconditions
from library.core.utils.testcasefilter import tags
from pages.chat.chatfileProview import ChatfileProviewPage
from pages.contacts.my_group import ALLMyGroup


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
        """断开手机连接"""
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
    def creat_group_chatwindows_with_B_and_A(name='双机群聊1'):
        """创建同时存在A、B两个手机号的群聊，且保证A、B手机都加入该群(b手机创建群-邀请A加入)"""
        # 获取A手机的电话号码
        Preconditions.select_mobile('IOS-移动')
        phone_number_A = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 切换到B手机，创建群（群成员有A B两台手机）
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        # B手机创建创建群
        msg.open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group=ALLMyGroup()
        my_group.click_creat_group()
        # 选择A手机 和另外一个联系人创建群组
        select=SelectContactsPage()
        time.sleep(2)
        select.click_search_box()
        select.input_search_text(phone_number_A)
        time.sleep(2)
        select.click_search_result_from_internet(phone_number_A)
        # 选择另外一个联系人
        select.select_local_contacts()
        select.select_one_contact_by_name('大佬1')
        select.click_sure_bottom()
        # 输入群组名称页面
        my_group.click_clear_group_name()
        my_group.input_group_name(name)
        my_group.click_sure_creat()
        time.sleep(2)
        ChatWindowPage().wait_for_page_load()
        # 切换到A手机，加入群聊
        Preconditions.select_mobile("IOS-移动")
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        mess.click_text('系统消息')
        mess.click_system_message_allow()
        time.sleep(2)
        mess.click_back()

    @staticmethod
    def make_sure_have_group_chat(group_name='双机群聊1'):
        """确保进入A手机存在群聊"""
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        mess.open_contacts_page()
        ContactsPage().open_group_chat_list()
        time.sleep(2)
        my_group = ALLMyGroup()
        if my_group.is_text_present(group_name):
            my_group.click_back()
            time.sleep(2)
        else:
            Preconditions.creat_group_chatwindows_with_B_and_A(name=group_name)
            time.sleep(2)

    @staticmethod
    def send_pic_in_group_chat():
        """发送图片"""
        chat = ChatWindowPage()
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.click_pic()
        select_pic = ChatPicPage()
        select_pic.click_camara_picture()
        select_pic.select_first_picture()
        select_pic.click_send()
        time.sleep(3)

    @staticmethod
    def enter_in_group_chatwindows_with_B_to_A(group_name='双机群聊1'):
        """进入群聊对话页面"""
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        if mess.is_text_present(group_name):
            mess.click_text(group_name)
        else:
            mess.click_search_box()
            mess.input_search_text(group_name)
            time.sleep(2)
            mess.click_element_first_list()
            time.sleep(1)
            # ContactDetailsPage().click_message_icon()


class GroupChatDouble(TestCase):
    """群聊--双机用例"""

    # @classmethod
    # def setUpClass(cls):
    #     warnings.simplefilter('ignore', ResourceWarning)
    #     Preconditions.select_mobile('IOS-移动')
    #     Preconditions.make_sure_have_group_chat()

    def setUp_test_msg_xiaoliping_D_0023(self):
        """确保A手机收到群聊发送的图片消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        # 切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送图片
        Preconditions.send_pic_in_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0023(self):
        """群聊会话页面，转发他人发送的图片到当前会话窗口"""
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        mess.wait_for_page_load_new_message_coming()
        mess.click_text('双机群聊1')
        chat=ChatWindowPage()
        chat.wait_for_page_load()
        # 下载图片后长按
        chat = ChatWindowPage()
        chat.click_coordinate(25, 35)
        time.sleep(3)
        chat.click_coordinate(50, 50)
        time.sleep(1)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='编辑'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(),True)
        # 3.选择最近聊天联系人-调起询问弹窗
        select.click_recent_chat_contact()
        self.assertEqual(select.is_element_present(locator='取消'),True)
        self.assertEqual(select.is_element_present(locator='确定'), True)
        # 4.点击确定，转发成功(toast未验证)
        select.click_sure_forward()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(),True)

    def tearDown_test_msg_xiaoliping_D_0023(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



    def setUp_test_msg_xiaoliping_D_0059(self):
        """确保A手机收到群聊发送的图片消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        #切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat=ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        #发送图片
        Preconditions.send_pic_in_group_chat()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0059(self):
        """群聊会话页面，转发他人发送的图片到当前会话窗口"""
        #切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        mess.wait_for_page_load_new_message_coming()
        mess.click_text('双机群聊1')
        chat=ChatWindowPage()
        chat.wait_for_page_load()
        #下载图片后长按
        chat = ChatWindowPage()
        chat.click_coordinate(25, 30)
        time.sleep(3)
        chat.click_coordinate(50, 50)
        time.sleep(1)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        #1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='编辑'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        #2.点击删除-调起弹框
        chat.click_delete()
        self.assertEqual(chat.is_element_present_by_locator(locator='确定删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='取消删除'), True)
        time.sleep(2)
        #点击确定
        chat.click_sure_delete()
        time.sleep(2)
        self.assertEqual(chat.is_element_present_by_locator(locator='消息列表'),False)
        self.assertEqual(chat.is_on_this_page(), True)

    def tearDown_test_msg_xiaoliping_D_0059(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



    def setUp_test_msg_xiaoliping_D_0063(self):
        """确保A手机收到群聊发送的视频消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，清空聊天列表
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        #切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat=ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        #发送视频
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_video()
        time.sleep(2)
        csf.click_select_video()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_D_0063(self):
        """群聊会话页面，转发他人发送的视频给手机联系人"""
        #切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        mess.click_text('双机群聊1')
        chat=ChatWindowPage()
        chat.wait_for_page_load()
        #下载图片后长按
        chat = ChatWindowPage()
        chat.click_play_video()  # 下载文件
        chat.wait_for_page_load_play_video()
        chat.swipe_by_percent_on_screen(50, 50, 50, 60)
        chat.click_cancel_previer_video()
        time.sleep(2)
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        #1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        #2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(),True)
        # 3.选择任意手机联系人
        select.select_local_contacts()
        local_contact = SelectLocalContactsPage()
        self.assertEqual(local_contact.is_on_this_page(), True)
        local_contact.swipe_select_one_member_by_name('大佬2')
        time.sleep(2)
        self.assertEqual(local_contact.is_element_exit(text='取消'), True)
        self.assertEqual(local_contact.is_element_exit(text='确定'), True)
        # 4.点击确定，转发成功(toast未验证)
        local_contact.click_sure()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(), True)

    def tearDown_test_msg_xiaoliping_D_0063(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


#群聊-位置


    def setUp_test_msg_weifenglian_qun_0377(self):
        """确保A手机收到群聊发送的位置消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，清空聊天列表
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        #切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat=ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        #发送位置
        chat.click_more()
        chat.click_locator()
        time.sleep(2)
        # 选择位置界面
        locator = ChatLocationPage()
        locator.wait_for_page_load()
        locator.click_send()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_qun_0377(self):
        """将接收到的位置转发到普通群"""
        #切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        mess.click_text('双机群聊1')
        chat=ChatWindowPage()
        chat.wait_for_page_load()
        #长按
        chat = ChatWindowPage()
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        #1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        #2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(),True)
        # 3.选择任意普通群-调起询问弹窗
        select.click_select_one_group()
        one_group = SelectOneGroupPage()
        one_group.selecting_one_group_by_name('群聊1')
        time.sleep(2)
        self.assertEqual(one_group.is_element_exit(text='取消'), True)
        self.assertEqual(one_group.is_element_exit(text='确定'), True)
        # 4.点击确定，转发成功(toast未验证)
        one_group.click_sure_send()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(), True)

    def tearDown_test_weifenglian_qun_0377(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



    def setUp_test_msg_weifenglian_qun_0378(self):
        """确保A手机收到群聊发送的位置消息"""
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到A手机，清空聊天列表
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        #切换到B手机，发送图片消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat=ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        #发送位置
        chat.click_more()
        chat.click_locator()
        time.sleep(2)
        # 选择位置界面
        locator = ChatLocationPage()
        locator.wait_for_page_load()
        locator.click_send()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_qun_0378(self):
        """将接收到的位置转发到企业群"""
        #切换到A手机，转发图片
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        mess.click_text('双机群聊1')
        chat=ChatWindowPage()
        chat.wait_for_page_load()
        #长按
        chat = ChatWindowPage()
        chat.swipe_by_percent_on_screen(25, 30, 25, 40)
        time.sleep(3)
        #1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        #2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(),True)
        # 3.选择企业群-调起询问弹窗
        select.click_select_one_group()
        one_group = SelectOneGroupPage()
        one_group.select_one_company_group()
        time.sleep(2)
        self.assertEqual(one_group.is_element_exit(text='取消'), True)
        self.assertEqual(one_group.is_element_exit(text='确定'), True)
        # 4.点击确定，转发成功(toast未验证)
        one_group.click_sure_send()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(), True)


    def tearDown_test_weifenglian_qun_0378(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



    def setUp_test_msg_huangmianhua_0163(self):
        warnings.simplefilter('ignore', ResourceWarning)
        # 获取B手机号-清空所以的消息列表
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 1、聊天会话页面——超长文本消息 带有@群成员
        Preconditions.select_mobile('IOS-移动')
        # 切换到A手机，删除聊天列表
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.delete_all_message_list()
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.click_input_box()
        text='long message'*40+'@'
        chat.input_message_text(text)
        time.sleep(2)
        chat.select_members_by_name(name=phone_number_B)
        time.sleep(2)
        chat.click_send_button()
        time.sleep(2)

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0163(self):
        """普通群——聊天会话页面——超长文本消息中带有@群成员"""
        # 切换到B 手机，查看消息列表展示
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        # MessagePage().wait_for_page_load_new_message_coming()
        time.sleep(3)
        message = '有人@我'
        MessagePage().page_should_contain_text(message)

    def tearDown_test_msg_huangmianhua_0163(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_huangmianhua_0165(self):
        warnings.simplefilter('ignore', ResourceWarning)
        # 获取B手机号-清空所以的消息列表
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 1、聊天会话页面——多个@后再选要@的群成员 带有@群成员
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.click_input_box()
        chat.input_message_text('@@@@')
        chat.select_members_by_name(name=phone_number_B)
        time.sleep(2)
        chat.click_send_button()
        time.sleep(2)

    @tags('ALL', 'enterprise_group', 'CMCC_调试中')
    def test_msg_huangmianhua_0165(self):
        """群聊天会话页面——输入多个@后——再选要@的群成员查看@效果"""
        # 切换到B 手机，查看消息列表展示
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(3)
        message = '有人@我'
        MessagePage().page_should_not_contain_text(message)

    def tearDown_test_msg_huangmianhua_0165(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_huangmianhua_0166(self):
        warnings.simplefilter('ignore', ResourceWarning)
        # 获取B手机号-清空所以的消息列表
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 1、聊天会话页面——带有@多个群成员
        Preconditions.select_mobile('IOS-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.click_input_box()
        text = '@'
        chat.input_message_text(text)
        time.sleep(2)
        chat.select_members_by_name(name=phone_number_B)
        chat.click_send_button()
        time.sleep(2)

    @tags('ALL', 'enterprise_group', 'CMCC_double')
    def test_msg_huangmianhua_0166(self):
        """群聊天会话页面——同时@多个人——@效果展示(需要群聊需要至少有3个联系人，暂时无法实现)"""
        # 切换到B 手机，查看消息列表展示
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(3)
        message = '有人@我'
        MessagePage().page_should_contain_text(message)

    def tearDown_test_msg_huangmianhua_0166(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])















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
    def enter_phone_chatwindows_from_B_to_A(type1='IOS-移动', type2='IOS-移动-移动'):
        """从b手机进入与A手机的1v1对话框"""
        #获取A手机的电话号码
        Preconditions.select_mobile(type1)
        phone_number_A = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到B手机，进入与A手机的对话窗口
        Preconditions.select_mobile(type2)
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        # 搜索A手机，如果不存在就添加A手机为手机联系人，进入与A手机对话框
        msg.click_search_box()
        msg.input_search_text(phone_number_A)
        time.sleep(3)
        if msg.is_element_present(text='搜索结果列表1'):
            msg.click_element_first_list()
            time.sleep(2)
            ContactDetailsPage().click_message_icon()
        else:
            msg.click_back()
            msg.open_contacts_page()
            contact = ContactsPage()
            contact.click_phone_contact()
            contact.click_add()
            creat = CreateContactPage()
            creat.create_contact(phone_number_A, phone_number_A)
            time.sleep(2)
            ContactDetailsPage().click_message_icon()

    @staticmethod
    def send_locator():
        """聊天界面-发送位置"""
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_more()
        chat.click_locator()
        time.sleep(2)
        # 选择位置界面
        locator = ChatLocationPage()
        locator.wait_for_page_load()
        locator.click_send()
        time.sleep(2)

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
         #选择A手机 和另外一个联系人创建群组
        select=SelectContactsPage()
        time.sleep(2)
        select.click_search_box()
        select.input_search_text(phone_number_A)
        time.sleep(2)
        select.click_element_by_id(text='搜索结果列表1')
          #选择另外一个联系人
        select.select_local_contacts()
        select.select_one_contact_by_name('大佬1')
        select.click_sure_bottom()
        #输入群组名称页面
        my_group.click_clear_group_name()
        my_group.input_group_name(name)
        my_group.click_sure_creat()
        time.sleep(2)
        ChatWindowPage().wait_for_page_load()
        #切换到A手机，加入群聊
        Preconditions.select_mobile("IOS-移动")
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        time.sleep(3)
        if not my_group.page_should_contain_text2(name):
            Preconditions.make_already_in_message_page()
            mess.click_text('系统消息')
            mess.click_system_message_allow()
            time.sleep(2)
            mess.click_back()

    @staticmethod
    def make_sure_have_group_chat(group_name='双机群聊1'):
        """确保手机存在群聊"""
        # Preconditions.select_mobile('IOS-移动-移动')
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
        mess=MessagePage()
        if mess.is_text_present(group_name):
            mess.click_text(group_name)
        else:
            mess.click_search_box()
            mess.input_search_text(group_name)
            time.sleep(2)
            mess.click_element_first_list()
            time.sleep(1)


class SingleChatDouble(TestCase):
    """单聊-双机用例-高等级"""

    def setUp_test_msg_xiaoliping_C_0023(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送图片
        chat=ChatWindowPage()
        chat.send_pic()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_C_0023(self):
        """单聊会话页面，转发他人发送的图片到当前会话窗口"""
        # 获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        # 长按图片--先下载图片
        chat= ChatWindowPage()
        chat.click_coordinate(40,30)
        time.sleep(3)
        chat.click_coordinate(50,50)
        time.sleep(1)
        chat.press_and_move_right_file(type='.jpg')
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
        self.assertEqual(select.is_on_this_page(), True)
        # 3.选择最近聊天联系人-调起询问弹窗
        select.click_recent_chat_contact()
        self.assertEqual(select.is_element_present(locator='取消'), True)
        self.assertEqual(select.is_element_present(locator='确定'), True)
        # 4.点击确定，转发成功(toast未验证)
        select.click_sure_forward()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(), True)
        # 清空聊天记录-恢复环境
        chat.clear_all_chat_record()

    def tearDown_test_msg_xiaoliping_C_0023(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoliping_C_0035(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        # 进入与A手机的对话窗口，发送文件
        chat = ChatWindowPage()
        chat.send_file(type='.docx')
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_C_0035(self):
        """单聊会话页面，转发他人发送的文件到普通群"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按文件
        chat=ChatWindowPage()
        chat.click_file_by_type('.docx')  #下载文件
        time.sleep(2)
        chat.press_and_move_right_file(type='.docx')
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
        #3.选择任意普通群-调起询问弹窗
        select.click_select_one_group()
        one_group=SelectOneGroupPage()
        one_group.selecting_one_group_by_name('群聊1')
        time.sleep(2)
        self.assertEqual(one_group.is_element_exit(text='取消'),True)
        self.assertEqual(one_group.is_element_exit(text='确定'), True)
        #4.点击确定，转发成功(toast未验证)
        one_group.click_sure_send()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(),True)
        #清空聊天记录-恢复环境
        chat.clear_all_chat_record()

    def tearDown_test_msg_xiaoliping_C_0035(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



    def setUp_test_msg_xiaoliping_C_0038(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        # 进入与A手机的对话窗口，发送文件
        chat = ChatWindowPage()
        chat.send_file(type='.docx')
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_C_0038(self):
        """单聊会话页面，转发他人发送的文件到企业群"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按文件
        chat = ChatWindowPage()
        chat.click_file_by_type('.docx')  # 下载文件
        time.sleep(2)
        chat.press_and_move_right_file(type='.docx')
        time.sleep(3)
        #1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        #2 .点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(),True)
        #3.选择企业群-调起询问弹窗
        select.click_select_one_group()
        one_group = SelectOneGroupPage()
        one_group.select_one_company_group()
        time.sleep(2)
        self.assertEqual(one_group.is_element_exit(text='取消'), True)
        self.assertEqual(one_group.is_element_exit(text='确定'), True)
        #4.点击确定，转发成功(toast未验证)
        one_group.click_sure_send()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(),True)
        #清空聊天记录-恢复环境
        chat.clear_all_chat_record()

    def tearDown_test_msg_xiaoliping_C_0038(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoliping_C_0059(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送图片
        chat=ChatWindowPage()
        chat.send_pic()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_C_0059(self):
        """单聊会话页面，删除他人发送的图片"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按图片
        chat=ChatWindowPage()
        chat.click_coordinate(40, 30)
        time.sleep(2)
        chat.click_coordinate(50, 50)
        time.sleep(1)
        chat.press_and_move_right_file(type='.jpg')
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

    def tearDown_test_msg_xiaoliping_C_0059(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



    def setUp_test_msg_xiaoliping_C_0061(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送图片
        chat=ChatWindowPage()
        chat.send_pic()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_C_0061(self):
        """单聊会话页面，收藏他人发送的图片"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按图片
        chat=ChatWindowPage()
        chat.click_coordinate(40, 30)
        time.sleep(2)
        chat.click_coordinate(50, 50)
        time.sleep(1)
        chat.press_and_move_right_file(type='.jpg')
        time.sleep(3)
        #1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='编辑'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        #2.点击收藏-toast提示收藏成功（toast未验证）
        chat.click_collection()
        time.sleep(2)
        #清空聊天记录-恢复环境
        chat.clear_all_chat_record()
        # 进入收藏页面查看-可见
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        collection = MeCollectionPage()
        time.sleep(2)
        collection.page_should_contain_text('今天')


    def tearDown_test_msg_xiaoliping_C_0061(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_xiaoliping_C_0063(self):
        # 1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        # 进入与A手机的对话窗口，发送视频
        chat = ChatWindowPage()
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_video()
        time.sleep(2)
        csf.click_select_video()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_C_0063(self):
        """单聊会话页面，转发他人发送的视频给手机联系人"""
        # 获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按文件
        chat=ChatWindowPage()
        chat.click_play_video()  #下载文件
        chat.wait_for_page_load_play_video()
        chat.swipe_by_percent_on_screen(50, 50, 50, 60)
        chat.click_cancel_previer_video()
        time.sleep(2)
        chat.press_and_move_right_video()
        time.sleep(3)
        #1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        # self.assertEqual(chat.is_element_present_by_locator(locator='编辑'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        #2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(),True)
        #3.选择任意手机联系人
        select.select_local_contacts()
        local_contact = SelectLocalContactsPage()
        self.assertEqual(local_contact.is_on_this_page(), True)
        local_contact.swipe_select_one_member_by_name('大佬2')
        time.sleep(2)
        self.assertEqual(local_contact.is_element_exit(text='取消'),True)
        self.assertEqual(local_contact.is_element_exit(text='确定'), True)
        #4.点击确定，转发成功(toast未验证)
        local_contact.click_sure()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(),True)
        #清空聊天记录-恢复环境
        chat.clear_all_chat_record()

    def tearDown_test_msg_xiaoliping_C_0063(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_xiaoliping_C_0069(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送视频
        chat=ChatWindowPage()
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_video()
        time.sleep(2)
        csf.click_select_video()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_C_0069(self):
        """单聊会话页面，删除他人发送的视频"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按文件
        chat=ChatWindowPage()
        chat.click_play_video()  #下载文件
        chat.wait_for_page_load_play_video()
        chat.swipe_by_percent_on_screen(50,50,50,60)
        chat.click_cancel_previer_video()
        time.sleep(2)
        chat.press_and_move_right_video()
        time.sleep(3)
        #1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        #2.点击删除
        chat.click_delete()
        self.assertEqual(chat.is_element_present_by_locator(locator='确定删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='取消删除'), True)
        time.sleep(2)
        # 点击确定
        chat.click_sure_delete()
        time.sleep(2)
        self.assertEqual(chat.is_element_present_by_locator(locator='消息列表'), False)
        self.assertEqual(chat.is_on_this_page(), True)

    def tearDown_test_msg_xiaoliping_C_0069(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])
#单聊--文件

    def setUp_test_msg_weifenglian_1V1_0274(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送文件
        chat=ChatWindowPage()
        chat.send_file()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_1V1_0274(self):
        """验证在单聊会话窗口点击打开已下载的可预览文件-右上角的更多按钮-转发时是否正常"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #下载文件后打开文件
        chat=ChatWindowPage()
        chat.click_file_by_type()
        time.sleep(2)
        chat.click_file_by_type('.docx')
        #1.正常打开预览文件
        time.sleep(2)
        proview_file=ChatfileProviewPage()
        self.assertEqual(proview_file.is_on_this_page(),True)
        #2.点击更多  调起更多选项
        proview_file.click_more_Preview()
        time.sleep(3)
        self.assertEqual(proview_file.is_exist_element(locator='预览文件-转发'),True)
        self.assertEqual(proview_file.is_exist_element(locator='预览文件-收藏'), True)
        self.assertEqual(proview_file.is_exist_element(locator='其他应用打开'), True)
        self.assertEqual(proview_file.is_exist_element(locator='预览文件-取消'), True)
        #2.点击转发-调起联系人选择器
        proview_file.click_forward_Preview()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(),True)
        #3.选择任意联系人-调起询问弹窗
        select.select_local_contacts()
        local_contact = SelectLocalContactsPage()
        local_contact.swipe_select_one_member_by_name('大佬2')
        #4.点击确定，转发成功(toast未验证)
        local_contact.click_send()
        time.sleep(3)
        self.assertEqual(proview_file.is_on_this_page(),True)
        #清空聊天记录-恢复环境
        chat.clear_all_chat_record()

    def tearDown_test_msg_weifenglian_1V1_0274(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_weifenglian_1V1_0133(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送文件
        chat=ChatWindowPage()
        chat.send_file()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_1V1_0133(self):
        """将接收到的文件转发到普通群"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按文件
        chat=ChatWindowPage()
        chat.click_file_by_type('.docx')  #下载文件
        time.sleep(2)
        chat.press_and_move_right_file()
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
        #3.选择任意普通群-调起询问弹窗
        select.click_select_one_group()
        one_group=SelectOneGroupPage()
        one_group.selecting_one_group_by_name('群聊1')
        time.sleep(2)
        self.assertEqual(one_group.is_element_exit(text='取消'),True)
        self.assertEqual(one_group.is_element_exit(text='确定'), True)
        #4.点击确定，转发成功(toast未验证)
        one_group.click_sure_send()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(),True)
        #清空聊天记录-恢复环境
        chat.clear_all_chat_record()

    def tearDown_test_msg_weifenglian_1V1_0133(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_weifenglian_1V1_0134(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送文件
        chat=ChatWindowPage()
        chat.send_file()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_1V1_0134(self):
        """将接收到的文件转发到企业群"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按文件
        chat = ChatWindowPage()
        chat.click_file_by_type('.docx')  # 下载文件
        time.sleep(2)
        chat.press_and_move_right_file()
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
        #3.选择企业群-调起询问弹窗
        select.click_select_one_group()
        one_group = SelectOneGroupPage()
        one_group.select_one_company_group()
        time.sleep(2)
        self.assertEqual(one_group.is_element_exit(text='取消'), True)
        self.assertEqual(one_group.is_element_exit(text='确定'), True)
        #4.点击确定，转发成功(toast未验证)
        one_group.click_sure_send()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(),True)
        #清空聊天记录-恢复环境
        chat.clear_all_chat_record()

    def tearDown_test_msg_weifenglian_1V1_0134(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_weifenglian_1V1_0163(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送文件
        chat=ChatWindowPage()
        chat.send_file()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_1V1_0163(self):
        """将接收到的文件转发到将接收到的文件转发到团队未置灰的联系人"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按文件
        chat = ChatWindowPage()
        chat.click_file_by_type('.docx')  # 下载文件
        time.sleep(2)
        chat.press_and_move_right_file()
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
        #3.选择团队未置灰的联系人-调起询问弹窗
        select.click_group_contact()
        group_contact = SelectHeContactsPage()
        group_contact.select_one_team_by_name('ateam7272')
        group_detail = SelectHeContactsDetailPage()
        group_detail.wait_for_he_contacts_page_load()
        group_detail.select_one_he_contact_by_name('alice')
        time.sleep(2)
        self.assertEqual(group_detail.is_element_exit('取消'), True)
        self.assertEqual(group_detail.is_element_exit('确定'), True)
        #4.点击确定，转发成功(toast未验证)
        group_detail.click_sure()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(),True)
        #清空聊天记录-恢复环境
        chat.clear_all_chat_record()

    def tearDown_test_msg_weifenglian_1V1_0163(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_weifenglian_1V1_0183(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送文件
        chat=ChatWindowPage()
        chat.send_file()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_1V1_0183(self):
        """将接收到的文件转发到将接收到的文件转发到我的电脑"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按文件
        chat = ChatWindowPage()
        chat.click_file_by_type('.docx')  # 下载文件
        time.sleep(2)
        chat.press_and_move_right_file()
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
        #3.选择到我的电脑
        select.click_search_contact()
        select.input_search_keyword('我的电脑')
        select.page_down()
        time.sleep(1)
        select.click_search_result_my_PC()
        self.assertEqual(select.is_element_present(locator='取消'), True)
        self.assertEqual(select.is_element_present(locator='确定'), True)
        #4.点击确定，转发成功(toast未验证)
        select.click_sure_forward()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(),True)
        #清空聊天记录-恢复环境
        chat.clear_all_chat_record()

    def tearDown_test_msg_weifenglian_1V1_0183(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_weifenglian_1V1_0184(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送文件
        chat=ChatWindowPage()
        chat.send_file()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_1V1_0184(self):
        """将接收到的文件转发到将接收到的文件转发到最近聊天"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按文件
        chat = ChatWindowPage()
        chat.click_file_by_type('.docx')  # 下载文件
        time.sleep(2)
        chat.press_and_move_right_file()
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
        time.sleep(1)
        self.assertEqual(select.is_on_this_page(),True)
        #3.选择最近聊天
        select.click_recent_chat_contact()
        self.assertEqual(select.is_element_present(locator='取消'), True)
        self.assertEqual(select.is_element_present(locator='确定'), True)
        #4.点击确定，转发成功(toast未验证)
        select.click_sure_forward()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(),True)
        #清空聊天记录-恢复环境
        chat.clear_all_chat_record()

    def tearDown_test_msg_weifenglian_1V1_0184(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_weifenglian_1V1_0187(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送文件
        chat=ChatWindowPage()
        chat.send_file()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_1V1_0187(self):
        """对接收到的文件消息进行删除"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按文件
        chat = ChatWindowPage()
        chat.click_file_by_type('.docx')  # 下载文件
        time.sleep(2)
        chat.press_and_move_right_file()
        time.sleep(3)
        #1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        #2.点击删除
        chat.click_delete()
        self.assertEqual(chat.is_element_present_by_locator(locator='确定删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='取消删除'), True)
        time.sleep(2)
        #点击确定
        chat.click_sure_delete()
        time.sleep(2)
        self.assertEqual(chat.is_element_present_by_locator(locator='消息列表'),False)
        self.assertEqual(chat.is_on_this_page(), True)

    def tearDown_test_msg_weifenglian_1V1_0187(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



    def setUp_test_msg_weifenglian_1V1_0188(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送文件
        chat=ChatWindowPage()
        chat.send_file()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_1V1_0188(self):
        """对接收到的已下载文件消息进行收藏"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按文件
        chat = ChatWindowPage()
        chat.click_file_by_type('.docx')  # 下载文件
        time.sleep(2)
        chat.press_and_move_right_file()
        time.sleep(3)
        #1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        #2.点击收藏-toast提示收藏成功（toast未验证）
        chat.click_collection()
        time.sleep(2)
        #清空聊天记录-恢复环境
        chat.clear_all_chat_record()
        # 进入收藏页面查看-可见
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        collection = MeCollectionPage()
        time.sleep(2)
        collection.page_should_contain_text('今天')

    def tearDown_test_msg_weifenglian_1V1_0188(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



    def setUp_test_msg_weifenglian_1V1_0189(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送文件
        chat=ChatWindowPage()
        chat.send_file()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_1V1_0189(self):
        """对接收到的未下载文件消息进行收藏"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按文件（未下载）
        chat = ChatWindowPage()
        chat.press_and_move_right_file()
        time.sleep(3)
        #1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        #2.点击收藏-toast提示先下载文件（toast未验证）
        chat.click_collection()
        time.sleep(2)
        self.assertEqual(chat.is_on_this_page(),True)
        #清空聊天记录-恢复环境
        chat.clear_all_chat_record()

    def tearDown_test_msg_weifenglian_1V1_0189(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_weifenglian_1V1_0212(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送文件
        chat=ChatWindowPage()
        chat.send_file()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_1V1_0212(self):
        """单聊聊天文件列表页面点击未下载文件进入详情页进行下载"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #进入文件详情页面下载文件
        chat=ChatWindowPage()
        chat.click_setting()
        setting = SingleChatSetPage()
        setting.search_chat_record()
        setting.click_file()
        # 预览文件-跳转到文件详情页面
        chat_file = ChatFilePage()
        chat_file.open_file_by_type('.docx')
        file_proview = ChatfileProviewPage()
        self.assertEqual(file_proview.is_exist_element(locator='下载'),True)
        #点击下载-下载成功（下载进度与网络有关，无法获取）
        file_proview.click_download()
        time.sleep(3)
        file_proview.wait_for_page_load_download_file_success()
        self.assertEqual(file_proview.is_exist_element(locator='打开'), True)
        #下载失败暂时无法实现
        #清空聊天记录
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        chat.clear_all_chat_record()

    def tearDown_test_msg_weifenglian_1V1_0212(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_weifenglian_1V1_0213(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送文件
        chat=ChatWindowPage()
        chat.send_file()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_1V1_0213(self):
        """单聊聊天文件列表页面点击已下载文件进入详情页进行下载"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #下载文件
        chat = ChatWindowPage()
        chat.click_file_by_type('.docx')  # 下载文件
        time.sleep(1)
        #进入文件详情页面下载文件
        chat.click_setting()
        setting = SingleChatSetPage()
        setting.search_chat_record()
        setting.click_file()
        # 预览文件-直接打开文件
        chat_file = ChatFilePage()
        chat_file.open_file_by_type('.docx')
        file_proview = ChatfileProviewPage()
        time.sleep(2)
        self.assertEqual(file_proview.is_exist_element(locator='预览文件-更多'),True)
        self.assertEqual(file_proview.is_exist_element(locator='下载'),False)
        #下载失败暂时无法实现
        #清空聊天记录
        # file_proview.click_back()
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        chat.clear_all_chat_record()

    def tearDown_test_msg_weifenglian_1V1_0213(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


#单聊--位置

    def setUp_test_msg_weifenglian_1V1_0386(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送位置
        Preconditions.send_locator()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_1V1_0386(self):
        """将接收到的位置转发到手机联系人"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按位置记录-转发
        chat = ChatWindowPage()
        chat.press_and_move_right_locator()
        time.sleep(2)
        #转发到手机联系人
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select = SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
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
        # 清空聊天记录-恢复环境
        chat.clear_all_chat_record()

    def tearDown_test_msg_weifenglian_1V1_0386(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_weifenglian_1V1_0399(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送位置
        Preconditions.send_locator()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_1V1_0399(self):
        """将接收到的位置转发到团队未置灰的联系人"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按位置记录-转发
        chat = ChatWindowPage()
        chat.press_and_move_right_locator()
        time.sleep(2)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select = SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 3.选择团队未置灰的联系人-调起询问弹窗
        select.click_group_contact()
        group_contact = SelectHeContactsPage()
        group_contact.select_one_team_by_name('ateam7272')
        group_detail = SelectHeContactsDetailPage()
        group_detail.wait_for_he_contacts_page_load()
        group_detail.select_one_he_contact_by_name('alice')
        time.sleep(2)
        self.assertEqual(group_detail.is_element_exit('取消'), True)
        self.assertEqual(group_detail.is_element_exit('确定'), True)
        # 4.点击确定，转发成功(toast未验证)
        group_detail.click_sure()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(), True)
        # 清空聊天记录-恢复环境
        chat.clear_all_chat_record()

    def tearDown_test_msg_weifenglian_1V1_0399(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_weifenglian_1V1_0419(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送位置
        Preconditions.send_locator()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_1V1_0419(self):
        """将接收到的位置转发到我的电脑"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按位置记录-转发
        chat = ChatWindowPage()
        chat.press_and_move_right_locator()
        time.sleep(2)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select = SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 3.选择到我的电脑
        select.click_search_contact()
        select.input_search_keyword('我的电脑')
        select.page_down()
        time.sleep(1)
        select.click_search_result_my_PC()
        self.assertEqual(select.is_element_present(locator='取消'), True)
        self.assertEqual(select.is_element_present(locator='确定'), True)
        # 4.点击确定，转发成功(toast未验证)
        select.click_sure_forward()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(), True)
        # 清空聊天记录-恢复环境
        chat.clear_all_chat_record()

    def tearDown_test_msg_weifenglian_1V1_0419(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_weifenglian_1V1_0420(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送位置
        Preconditions.send_locator()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_1V1_0420(self):
        """将接收到的位置转发到最近聊天"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按位置记录-转发
        chat = ChatWindowPage()
        chat.press_and_move_right_locator()
        time.sleep(2)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select = SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 3.选择最近聊天联系人-调起询问弹窗
        select.click_recent_chat_contact()
        self.assertEqual(select.is_element_present(locator='取消'), True)
        self.assertEqual(select.is_element_present(locator='确定'), True)
        # 4.点击确定，转发成功(toast未验证)
        select.click_sure_forward()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(), True)
        # 清空聊天记录-恢复环境
        chat.clear_all_chat_record()

    def tearDown_test_msg_weifenglian_1V1_0420(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



    def setUp_test_msg_weifenglian_1V1_0423(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送位置
        Preconditions.send_locator()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_1V1_0423(self):
        """将接收到的位置消息进行删除"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按位置记录-转发
        chat = ChatWindowPage()
        chat.press_and_move_right_locator()
        time.sleep(2)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击删除
        chat.click_delete()
        self.assertEqual(chat.is_element_present_by_locator(locator='确定删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='取消删除'), True)
        time.sleep(2)
        # 点击确定
        chat.click_sure_delete()
        time.sleep(2)
        self.assertEqual(chat.is_element_present_by_locator(locator='消息列表'), False)
        self.assertEqual(chat.is_on_this_page(), True)

    def tearDown_test_msg_weifenglian_1V1_0423(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_weifenglian_1V1_0424(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送位置
        Preconditions.send_locator()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_1V1_0424(self):
        """将接收到的位置消息进行收藏"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按位置记录-转发
        chat = ChatWindowPage()
        chat.press_and_move_right_locator()
        time.sleep(2)
        # 1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 2.点击收藏-toast提示收藏成功（toast未验证）
        chat.click_collection()
        time.sleep(2)
        # 清空聊天记录-恢复环境
        chat.clear_all_chat_record()
        # 进入收藏页面查看-可见
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        collection = MeCollectionPage()
        time.sleep(2)
        collection.page_should_contain_text('今天')

    def tearDown_test_msg_weifenglian_1V1_0424(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_weifenglian_1V1_0439(self):
        # 1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        # 进入与A手机的对话窗口，发送位置
        Preconditions.send_locator()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_weifenglian_1V1_0439(self):
        """将接收到的位置消息进行收藏"""
        # 获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        # 长按位置记录
        chat = ChatWindowPage()
        chat.press_and_move_right_locator()
        time.sleep(2)
        # 1.正常调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        # 转发功能正常
        chat.click_forward()
        self.assertTrue(SelectContactsPage().is_on_this_page())
        SelectContactsPage().click_back()
        # 2.点击收藏-toast提示收藏成功（toast未验证）
        chat.press_and_move_right_locator()
        chat.click_collection()
        time.sleep(2)
        self.assertTrue(chat.is_on_this_page())
        # 3.多选功能正常
        chat.press_and_move_right_locator()
        chat.click_multiple_selection()
        self.assertTrue(chat.is_element_present_by_locator(locator='多选-删除'))
        chat.click_cancel_multiple_selection()
        # 点击删除
        chat.press_and_move_right_locator()
        chat.click_delete()
        chat.click_sure_delete()
        self.assertFalse(chat.is_exist_element(locator='消息列表'))

    def tearDown_test_msg_weifenglian_1V1_0439(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


#消息--名片

    def setUp_test_msg_hanjiabin_0196(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送名片
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_more()
        chat.click_name_card()
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬2')
        time.sleep(1)
        select.click_share_card()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_hanjiabin_0196(self):
        """名片消息——单聊——收到名片后--消息界面——点击查看-已在本地名片"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #点击名片消息
        chat = ChatWindowPage()
        chat.click_business_card_list()
        time.sleep(2)
        detail=ContactDetailsPage()
        self.assertEqual(detail.is_on_this_page(),True)
        # 清空消息记录
        detail.click_back()
        chat.clear_all_chat_record()

    def tearDown_test_msg_hanjiabin_0196(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



    def setUp_test_msg_hanjiabin_0197(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送名片
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_more()
        chat.click_name_card()
        select = SelectContactsPage()
        select.click_he_contacts()
        select_he = SelectHeContactsPage()
        select_he.select_one_team_by_name('ateam7272')
        # 选择和通讯录联系人详情页面
        select_he_detail = SelectHeContactsDetailPage()
        time.sleep(3)
        select_he_detail.select_one_he_contact_by_name('alice')
        select.click_share_card()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_hanjiabin_0197(self):
        """名片消息——单聊——收到名片后--消息界面——点击查看-未保存在本地名片"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #点击名片消息
        chat = ChatWindowPage()
        chat.click_business_card_list()
        time.sleep(2)
        detail=ContactDetailsPage()
        self.assertEqual(detail.is_on_this_page(),True)
        detail.page_should_contain_text('保存到通讯录')

        # 清空消息记录
        detail.click_back()
        chat.clear_all_chat_record()

    def tearDown_test_msg_hanjiabin_0197(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



    def setUp_test_msg_hanjiabin_0198(self):
        # 1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        # 进入与A手机的对话窗口，发送名片
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_more()
        chat.click_name_card()
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬2')
        time.sleep(1)
        select.click_share_card()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_hanjiabin_0198(self):
        """名片消息——单聊——收到名片后--消息界面——长按-转发"""
        # 获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        # 长按-转发
        chat = ChatWindowPage()
        chat.press_and_move_right_business_card()
        time.sleep(2)
        chat.click_forward()
        #转发到我的电脑
        select = SelectContactsPage()
        select.click_search_contact()
        select.input_search_keyword('我的电脑')
        select.click_search_result()
        select.click_sure_forward()
        time.sleep(2)
        #转发到群聊
        chat.press_and_move_right_business_card()
        chat.click_forward()
        select.click_select_one_group()
        SelectOneGroupPage().selecting_one_group_by_name('群聊1')
        SelectOneGroupPage().click_sure_send()
        time.sleep(2)
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
        time.sleep(2)
        #转发到本地联系人
        chat.press_and_move_right_business_card()
        chat.click_forward()
        select.select_local_contacts()
        local_contact = SelectLocalContactsPage()
        self.assertEqual(local_contact.is_on_this_page(), True)
        local_contact.swipe_select_one_member_by_name('大佬2')
        local_contact.click_sure()
        time.sleep(2)

    def tearDown_test_msg_hanjiabin_0198(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



    def setUp_test_msg_hanjiabin_0199(self):
        # 1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        # 进入与A手机的对话窗口，发送名片
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_more()
        chat.click_name_card()
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬2')
        time.sleep(1)
        select.click_share_card()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_hanjiabin_0199(self):
        """名片消息——单聊——收到名片后--消息界面——长按-收藏"""
        # 获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        # 点击长按-收藏
        chat = ChatWindowPage()
        chat.press_and_move_right_business_card()
        time.sleep(2)
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
        #清空聊天记录
        Preconditions.make_already_in_message_page()
        MessagePage().click_text(phone_number_B)
        time.sleep(2)
        chat.clear_all_chat_record()

    def tearDown_test_msg_hanjiabin_0199(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_hanjiabin_0200(self):
        # 1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        # 进入与A手机的对话窗口，发送名片
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_more()
        chat.click_name_card()
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬2')
        time.sleep(1)
        select.click_share_card()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_hanjiabin_0200(self):
        """名片消息——单聊——收到名片后--消息界面——长按-删除"""
        # 获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        # 点击长按-删除
        chat = ChatWindowPage()
        chat.press_and_move_right_business_card()
        time.sleep(2)
        #点击删除
        chat.click_delete()
        time.sleep(2)
        chat.click_sure_delete()
        self.assertEqual(chat.is_element_present_card_list(), False)
        time.sleep(2)

    def tearDown_test_msg_hanjiabin_0200(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_hanjiabin_0201(self):
        # 1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        # 进入与A手机的对话窗口，发送名片
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_more()
        chat.click_name_card()
        select = SelectContactsPage()
        select.select_one_contact_by_name('大佬2')
        time.sleep(1)
        select.click_share_card()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_hanjiabin_0201(self):
        """名片消息——单聊——收到名片后--消息界面——长按-多选"""
        # 获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        # 点击长按-多选
        chat = ChatWindowPage()
        chat.press_and_move_right_business_card()
        time.sleep(2)
        # 点击多选
        chat.click_multiple_selection()
        time.sleep(2)
        chat.page_contain_element(locator='多选按钮')
        chat.page_contain_element(locator='多选-删除')
        chat.page_contain_element(locator='多选-转发')
        #清空记录
        chat.click_cancel_multiple_selection()
        time.sleep(2)
        chat.clear_all_chat_record()

    def tearDown_test_msg_hanjiabin_0201(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

#消息-网页消息

    def setUp_test_msg_hanjiabin_0217(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送名片
        chat = ChatWindowPage()
        time.sleep(2)
        text = 'www.baidu.com'
        chat.input_message_text(text)
        chat.click_send_button()
        time.sleep(3)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_hanjiabin_0217(self):
        """网页消息——收到网页消息"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        #点击网页消息
        chat = ChatWindowPage()
        chat.click_element_received_web_message()
        time.sleep(3)
        chat.wait_for_page_load_web_message()
        # 清空消息记录
        chat.click_back()
        time.sleep(2)
        chat.clear_all_chat_record()

    def tearDown_test_msg_hanjiabin_0217(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_hanjiabin_0218(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送名片
        chat = ChatWindowPage()
        time.sleep(2)
        text = 'www.baidu.com'
        chat.input_message_text(text)
        chat.click_send_button()
        time.sleep(3)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_hanjiabin_0218(self):
        """网页消息——收到网页消息消息界面——长按-转发"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按 转发
        chat = ChatWindowPage()
        chat.press_and_move_right_web_message()
        time.sleep(2)
        chat.click_forward()
        #转发到我的电脑
        select = SelectContactsPage()
        select.click_search_contact()
        select.input_search_keyword('我的电脑')
        select.click_search_result()
        select.click_sure_forward()
        time.sleep(3)
        #转发到群聊
        chat.press_and_move_right_web_message()
        chat.click_forward()
        select.click_select_one_group()
        SelectOneGroupPage().selecting_one_group_by_name('群聊1')
        SelectOneGroupPage().click_sure_send()
        time.sleep(2)
        #转发到团队联系人
        chat.press_and_move_right_web_message()
        chat.click_forward()
        select.click_group_contact()
        group_contact=SelectHeContactsPage()
        group_contact.select_one_team_by_name('ateam7272')
        group_detail=SelectHeContactsDetailPage()
        group_detail.wait_for_he_contacts_page_load()
        group_detail.select_one_he_contact_by_name('alice')
        group_detail.click_sure()
        time.sleep(2)
        #转发到本地联系人
        chat.press_and_move_right_web_message()
        chat.click_forward()
        select.select_local_contacts()
        local_contact = SelectLocalContactsPage()
        self.assertEqual(local_contact.is_on_this_page(), True)
        local_contact.swipe_select_one_member_by_name('大佬2')
        local_contact.click_sure()
        time.sleep(3)
        # 清空消息记录
        chat.clear_all_chat_record()

    def tearDown_test_msg_hanjiabin_0218(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



    def setUp_test_msg_hanjiabin_0219(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送名片
        chat = ChatWindowPage()
        time.sleep(2)
        text = 'www.baidu.com'
        chat.input_message_text(text)
        chat.click_send_button()
        time.sleep(3)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_hanjiabin_0219(self):
        """网页消息——收到网页消息消息界面——长按-收藏"""
        #获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        msg.click_text(phone_number_B)
        time.sleep(2)
        #长按 收藏
        chat = ChatWindowPage()
        chat.press_and_move_right_web_message()
        time.sleep(3)
        chat.click_collection()
        time.sleep(2)
        # 进入收藏页面查看
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        collection = MeCollectionPage()
        self.assertTrue(collection.is_exist_element(locator='收藏列表1'))
        time.sleep(2)
        collection.click_element_first_list()
        self.assertTrue(collection.is_element_present_collection_detail())
        # 清空聊天记录
        Preconditions.make_already_in_message_page()
        MessagePage().click_text(phone_number_B)
        time.sleep(2)
        chat.clear_all_chat_record()

    def tearDown_test_msg_hanjiabin_0219(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_hanjiabin_0220(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送名片
        chat = ChatWindowPage()
        time.sleep(2)
        text = 'www.baidu.com'
        chat.input_message_text(text)
        chat.click_send_button()
        time.sleep(3)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_hanjiabin_0220(self):
        """网页消息——收到网页消息消息界面——长按-删除"""
        # 获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        # 长按 删除
        chat = ChatWindowPage()
        chat.press_and_move_right_web_message()
        time.sleep(2)
        # 点击删除
        chat.click_delete()
        time.sleep(2)
        chat.click_sure_delete()
        self.assertEqual(chat.is_element_present_web_message(),False)
        time.sleep(2)

    def tearDown_test_msg_hanjiabin_0220(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_hanjiabin_0221(self):
        # 1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        # 进入与A手机的对话窗口，发送名片
        chat = ChatWindowPage()
        time.sleep(2)
        text = 'www.baidu.com'
        chat.input_message_text(text)
        chat.click_send_button()
        time.sleep(3)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_hanjiabin_0221(self):
        """网页消息——收到网页消息消息界面——长按-多选"""
        # 获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        # 长按-删除
        chat = ChatWindowPage()
        chat.press_and_move_right_web_message()
        time.sleep(2)
        # 点击多选
        chat.click_multiple_selection()
        time.sleep(2)
        chat.page_contain_element(locator='多选按钮')
        chat.page_contain_element(locator='多选-删除')
        chat.page_contain_element(locator='多选-转发')
        # 清空记录
        chat.click_cancel_multiple_selection()
        time.sleep(2)
        chat.clear_all_chat_record()

    def tearDown_test_msg_hanjiabin_0221(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


#消息列表

    def setUp_test_msg_xiaoliping_B_0008(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        msg.delete_all_message_list()
        # 切换到B手机-发送消息
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        chat = ChatWindowPage()
        chat.click_input_box()
        chat.input_message_text('消息')
        chat.click_send_button()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_B_0008(self):
        """消息列表未读消息清空"""
        # 切换到A手机 查看消息展示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load_new_message_coming()
        self.assertTrue(mess.is_exist_unread_make_and_number(number='1'))
        time.sleep(5)
        # 拖动取消红点
        mess.press_unread_make_and_move_down()
        time.sleep(5)
        # 判断消息红点消失
        self.assertFalse(mess.is_exist_unread_make_and_number(number='1'))

    def tearDown_test_msg_xiaoliping_B_0008(self):

        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_xiaoliping_B_0009(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        #进入A手机 单聊设置界面
        Preconditions.enter_phone_chatwindows_from_B_to_A(type1='IOS-移动-移动',type2='IOS-移动')
        chat=ChatWindowPage()
        chat.click_setting()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_B_0009(self):
        """消息列表界面单聊消息免打扰图标显示"""
        # A手机开启消息免打扰
        setting = SingleChatSetPage()
        icon = setting.get_switch_undisturb_value()
        if icon == '0':
            setting.click_msg_undisturb_switch()
        time.sleep(2)
        # 判断消息免打扰开启成功
        Preconditions.make_already_in_message_page()
        self.assertTrue(MessagePage().is_exist_no_disturb_icon())
        time.sleep(2)
        # 切换到B手机-发送消息
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        chat=ChatWindowPage()
        chat.click_input_box()
        chat.input_message_text('消息')
        chat.click_send_button()
        # 切换到A手机
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(4)
        self.assertTrue(MessagePage().is_exist_news_red_dot())
        MessagePage().click_text(phone_number_B)
        chat.click_setting()
        icon = setting.get_switch_undisturb_value()
        if icon == '1':
            setting.click_msg_undisturb_switch()
        time.sleep(3)

    def tearDown_test_msg_xiaoliping_B_0009(self):

        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_xiaoliping_B_0016(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        # A手机删除所有的列表
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        msg.delete_all_message_list()
        # 切换到B手机-发送消息
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        chat = ChatWindowPage()
        chat.click_input_box()
        chat.input_message_text('消息')
        chat.click_send_button()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_B_0016(self):
        """消息列表未读气泡展示"""
        #切换到A手机 查看消息展示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        mess.wait_for_page_load_new_message_coming()
        self.assertTrue(mess.is_exist_unread_make_and_number(number='1'))
        time.sleep(2)
        #超过99条未验证

    def tearDown_test_msg_xiaoliping_B_0016(self):

        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_xiaoliping_B_0021(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        # A手机删除所有的列表
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        msg.delete_all_message_list()
        # 切换到B手机-发送消息
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        chat = ChatWindowPage()
        chat.send_mutiple_message(times=25)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_B_0021(self):
        """进入到会话查看未读消息"""
        # 切换到A手机 查看消息展示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        time.sleep(3)
        self.assertTrue(mess.is_exist_unread_make_and_number(number='25'))
        time.sleep(2)
        # 点击进入消息界面-显示可浏览全部未读消息按钮
        mess.click_msg_first_list()
        chat=ChatWindowPage()
        time.sleep(2)
        self.assertTrue(chat.is_element_present_preview_unread_message_by_number(number=25))
        # 点击浏览全部未读消息按钮 进入最上一屏
        chat.click_preview_unread_message_by_number(number='25')
        time.sleep(2)
        self.assertTrue(chat.is_element_present_message_split_line())
        # 返回消息列表 不显示该未读数
        chat.click_back()
        time.sleep(3)
        self.assertFalse(mess.is_exist_unread_make_and_number(number='25'))

    def tearDown_test_msg_xiaoliping_B_0021(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_xiaoliping_B_0032(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        #切换到A手机 删除所有的聊天记录
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()


    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_B_0032(self):
        """消息列表未读气泡窗口右滑删除（ios）
        备注：ipone8p手机 左滑删除不能进行左滑删除操作
        """
        #切换到B手机-发送消息
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        chat=ChatWindowPage()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        chat.click_input_box()
        chat.input_message_text('消息')
        chat.click_send_button()
        #切换到A手机-判断存在未读消息
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(4)
        mess=MessagePage()
        self.assertTrue(mess.is_element_present_all_unread_message_number())
        #左滑删除，未读消息消失
        mess.swipe_by_percent_on_screen(70,20,30,20)
        time.sleep(1)
        mess.click_delete_list()
        self.assertFalse(mess.is_element_present_all_unread_message_number())

    def tearDown_test_msg_xiaoliping_B_0032(self):

        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_xiaoliping_B_0042(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        #进入A手机 单聊设置界面-开启消息免打扰
        Preconditions.enter_phone_chatwindows_from_B_to_A(type1='IOS-移动-移动',type2='IOS-移动')
        chat=ChatWindowPage()
        chat.click_setting()
        time.sleep(2)
        # A手机开启消息免打扰
        setting = SingleChatSetPage()
        icon = setting.get_switch_undisturb_value()
        if icon == '0':
            setting.click_msg_undisturb_switch()
        time.sleep(2)
        #删除所有的聊天记录
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_B_0042(self):
        """红点消息不计入未读数量"""
        # 切换到B手机-发送消息
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        chat=ChatWindowPage()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        chat.click_input_box()
        chat.input_message_text('消息')
        chat.click_send_button()
        # 切换到A手机-判断是否存在未读消息
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(4)
        mess=MessagePage()
        self.assertFalse(mess.is_element_present_all_unread_message_number())
        # 去除消息免打扰状态
        mess.click_text(phone_number_B)
        chat.click_setting()
        setting = SingleChatSetPage()
        icon = setting.get_switch_undisturb_value()
        if icon == '1':
            setting.click_msg_undisturb_switch()
        time.sleep(2)


    def tearDown_test_msg_xiaoliping_B_0042(self):

        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_xiaoliping_B_0043(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        #进入A手机 单聊设置界面
        Preconditions.enter_phone_chatwindows_from_B_to_A(type1='IOS-移动-移动',type2='IOS-移动')
        chat=ChatWindowPage()
        chat.click_setting()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_B_0043(self):
        """消息列表界面单聊消息免打扰图标显示"""
        #A手机开启消息免打扰
        setting = SingleChatSetPage()
        icon = setting.get_switch_undisturb_value()
        if icon == '0':
            setting.click_msg_undisturb_switch()
        time.sleep(2)
        #判断消息免打扰开启成功
        Preconditions.make_already_in_message_page()
        self.assertTrue(MessagePage().is_exist_no_disturb_icon())
        time.sleep(2)
        #切换到B手机-发送消息
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        chat=ChatWindowPage()
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        chat.click_input_box()
        chat.input_message_text('消息')
        chat.click_send_button()
        #切换到A手机-判断是否存在消息红点
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(4)
        mess=MessagePage()
        self.assertTrue(mess.is_exist_news_red_dot())
        #按住消息红点拖动-消息红点未消失
        mess.press_new_message_red_icon()
        time.sleep(2)
        self.assertTrue(mess.is_exist_news_red_dot())
        #进入消息对话框-顶部标题后方存在消息免打扰（ios不涉及）
        #去除消息免打扰状态
        mess.click_text(phone_number_B)
        chat.click_setting()
        setting = SingleChatSetPage()
        icon = setting.get_switch_undisturb_value()
        if icon == '1':
            setting.click_msg_undisturb_switch()
        time.sleep(2)


    def tearDown_test_msg_xiaoliping_B_0043(self):

        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



    def setUp_test_msg_xiaoliping_B_0045(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        msg.delete_all_message_list()
        # 切换到B手机-发送消息
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        chat = ChatWindowPage()
        chat.click_input_box()
        chat.input_message_text('消息')
        chat.click_send_button()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_B_0045(self):
        """未开启免打扰的单聊，收到一条新消息"""
        #切换到A手机 查看消息展示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        time.sleep(2)
        mess.wait_for_page_load_new_message_coming()
        #判断出现新消息提醒
        self.assertTrue(mess.is_exist_unread_make_and_number(number='1'))
        time.sleep(5)
        #拖动取消红点
        mess.press_unread_make_and_move_down()
        time.sleep(5)
        #判断消息红点消失
        self.assertFalse(mess.is_exist_unread_make_and_number(number='1'))

    def tearDown_test_msg_xiaoliping_B_0045(self):

        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoliping_B_0046(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        # 切换到B手机-发送消息
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        chat = ChatWindowPage()
        chat.send_mutiple_message(times=100)

    @tags('ALL', 'msg', 'CMCC_double_99')
    def test_msg_xiaoliping_B_0046(self):
        """未开启免打扰的单聊，收到超过99条新消息"""
        #切换到A手机 查看消息展示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        time.sleep(3)
        self.assertTrue(mess.is_exist_unread_make_and_number(number='99+'))
        time.sleep(2)
        #拖拽气泡消除
        mess.press_unread_make_and_move_down(number='99+')
        time.sleep(2)
        self.assertFalse(mess.is_exist_unread_make_and_number(number='99+'))
        #点击进入消息界面-清除红点
        mess.click_msg_first_list()
        time.sleep(2)

    def tearDown_test_msg_xiaoliping_B_0046(self):

        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])


    def setUp_test_msg_xiaoliping_B_0047(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保有群聊
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        Preconditions.make_sure_have_group_chat()
        # 进入b手机 B开启群聊的免打扰模式
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat=ChatWindowPage()
        chat.click_setting()
        time.sleep(2)
        group_set=GroupChatSetPage()
        time.sleep(2)
        icon = group_set.get_switch_undisturb_value()
        if icon == '0':
            group_set.click_switch_undisturb()
            time.sleep(2)
        group_set.click_back()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_B_0047(self):
        """已开启免打扰的群聊，接收到新消息"""
        # A手机收到B手机发送过来的消息
        chat = ChatWindowPage()
        chat.click_input_box()
        chat.input_message_text('群聊消息')
        chat.click_send_button()
        # 切换到A手机，查看消息显示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(3)
        mess=MessagePage()
        self.assertTrue(mess.is_exist_unread_make_and_number(number='1'))
        # 按住拖动红点
        mess.press_unread_make_and_move_down()
        time.sleep(5)
        # 判断消息红点消失
        self.assertFalse(mess.is_exist_unread_make_and_number(number='1'))
        # 进入消息列表 消息标题后面不存在消息免打扰icon（ios不涉及）
        mess.click_text('双机群聊1')
        time.sleep(2)
        # 去除b手机群聊的消息免打扰状态
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        mess.wait_for_page_load_new_message_coming()
        mess.click_text('双机群聊1')
        time.sleep(2)
        chat.click_setting()
        group_set = GroupChatSetPage()
        time.sleep(2)
        icon = group_set.get_switch_undisturb_value()
        if icon == '1':
            group_set.click_switch_undisturb()
        time.sleep(2)

    def tearDown_test_msg_xiaoliping_B_0047(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoliping_B_0049(self):
        # 1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保有群聊
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_sure_have_group_chat()
        # 进入b手机 B开启群聊的免打扰模式
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        #群聊页面 发送消息
        chat = ChatWindowPage()
        chat.click_input_box()
        chat.input_message_text('群聊消息')
        chat.click_send_button()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_B_0049(self):
        """未开启免打扰的群聊，收到一条新消息"""
        # 切换到A手机，查看消息显示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(3)
        mess=MessagePage()
        self.assertTrue(mess.is_exist_unread_make_and_number(number='1'))
        # 按住拖动红点
        mess.press_unread_make_and_move_down()
        time.sleep(5)
        # 判断消息红点消失
        self.assertFalse(mess.is_exist_unread_make_and_number(number='1'))
        # 进入消息列表 消息标题后面不存在消息免打扰icon（ios不涉及）
        mess.click_text('双机群聊1')
        time.sleep(2)

    def tearDown_test_msg_xiaoliping_B_0049(self):

        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoliping_B_0050(self):
        # 1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保有群聊
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_sure_have_group_chat()
        # 进入b手机 发送超过99条消息
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()
        chat = ChatWindowPage()
        chat.send_mutiple_message(times=100)

    @tags('ALL', 'msg', 'CMCC_double_99')
    def test_msg_xiaoliping_B_0050(self):
        """未开启免打扰的单聊，收到超过99条新消息"""
        #切换到A手机 查看消息展示
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        time.sleep(3)
        self.assertTrue(mess.is_exist_unread_make_and_number(number='99+'))
        time.sleep(2)
        #拖拽气泡消除
        mess.press_unread_make_and_move_down(number='99+')
        time.sleep(2)
        self.assertFalse(mess.is_exist_unread_make_and_number(number='99+'))
        #点击进入消息界面-清除红点
        mess.click_msg_first_list()
        time.sleep(2)

    def tearDown_test_msg_xiaoliping_B_0050(self):

        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])

    def setUp_test_msg_xiaoliping_B_0051(self):
        # 1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        # 从B手机进入与A手机的对话页面
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.enter_in_group_chatwindows_with_B_to_A()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_B_0051(self):
        """在消息列表页面，接收到新的系统消息"""
        # 确保收到系统消息（b手机解散群之后会收到系统消息）
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        set.dissolution_the_group()
        time.sleep(2)
        # 切换到A 手机 会收到系统消息
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        time.sleep(2)
        mess.wait_for_page_load_new_message_coming()
        # 判断出现新消息提醒
        self.assertTrue(mess.is_exist_unread_make_and_number(number='1'))
        time.sleep(5)
        # 拖动取消红点
        mess.press_unread_make_and_move_down()
        time.sleep(5)
        # 判断消息红点消失
        self.assertFalse(mess.is_exist_unread_make_and_number(number='1'))

    def tearDown_test_msg_xiaoliping_B_0051(self):
        Preconditions.creat_group_chatwindows_with_B_and_A()
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



class SingleChatDoubleMiddle(TestCase):
    """单聊-双机用例-中等级"""

    def setUp_test_msg_xiaoliping_C_0025(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送图片
        chat=ChatWindowPage()
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.click_pic()
        select_pic=ChatPicPage()
        select_pic.click_camara_picture()
        select_pic.select_first_picture()
        select_pic.click_send()

    @tags('ALL', 'msg', 'CMCC_double')
    def test_msg_xiaoliping_C_0025(self):
        """单聊会话页面，转发他人发送的图片到当前会话窗口"""
        # 获取B手机的电话号码
        phone_number_B = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 切换到A手机，
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load_new_message_coming()
        time.sleep(2)
        msg.click_text(phone_number_B)
        time.sleep(2)
        # 长按图片--先下载图片
        chat= ChatWindowPage()
        chat.click_file_by_type('.jpg')
        time.sleep(3)
        chat.click_coordinate(50, 50)
        time.sleep(1)
        chat.press_and_move_right_file(type='.jpg')
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
        self.assertEqual(select.is_on_this_page(), True)
        # 3.选择最近聊天联系人-调起询问弹窗
        select.click_search_contact()
        select.input_search_keyword(phone_number_B)
        time.sleep(2)
        select.click_search_result()
        self.assertEqual(select.is_element_present(locator='取消'), True)
        self.assertEqual(select.is_element_present(locator='确定'), True)
        # 5、点击弹窗取消按钮
        select.click_cancel_forward()
        # 停留在当前页面
        self.assertTrue(select.is_text_present('选择联系人'))
        # 清空环境
        Preconditions.make_already_in_message_page()
        msg.click_text(phone_number_B)
        time.sleep(2)
        chat.clear_all_chat_record()

    def tearDown_test_msg_xiaoliping_C_0025(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])






















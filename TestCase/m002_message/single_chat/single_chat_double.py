import unittest
import time
import warnings
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from preconditions.BasePreconditions import LoginPreconditions
from library.core.utils.testcasefilter import tags
from pages.chat.chatfileProview import ChatfileProviewPage


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
    def enter_phone_chatwindows_from_B_to_A():
        """从b手机进入与A手机的1v1对话框"""
        #获取A手机的电话号码
        Preconditions.select_mobile('IOS-移动')
        phone_number_A = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        #切换到B手机，进入与A手机的对话窗口
        Preconditions.select_mobile('IOS-移动-移动')
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        # 搜索A手机，如果不存在就添加A手机为手机联系人，进入与A手机对话框
        msg.click_search_box()
        msg.input_search_text(phone_number_A)
        time.sleep(2)
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



class SingleChatDouble(TestCase):
    """单聊-双机用例"""


    def setUp_test_msg_xiaoliping_C_0023(self):
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
    def test_msg_xiaoliping_C_0023(self):
        """单聊会话页面，转发他人发送的图片到当前会话窗口"""
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
        #长按图片--先下载图片
        chat=ChatWindowPage()
        chat.click_coordinate(40,30)
        time.sleep(3)
        chat.click_coordinate(50,50)
        time.sleep(1)
        chat.swipe_by_percent_on_screen(25,20,25,30)
        time.sleep(3)
        #1.调起功能菜单
        self.assertEqual(chat.is_element_present_by_locator(locator='转发'),True)
        self.assertEqual(chat.is_element_present_by_locator(locator='删除'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='收藏'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='编辑'), True)
        self.assertEqual(chat.is_element_present_by_locator(locator='多选'), True)
        #2.点击转发-调起联系人选择器
        chat.click_forward()
        time.sleep(2)
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(),True)
        #3.选择最近聊天联系人-调起询问弹窗
        select.click_recent_chat_contact()
        self.assertEqual(select.is_element_present(locator='取消'),True)
        self.assertEqual(select.is_element_present(locator='确定'), True)
        #4.点击确定，转发成功(toast未验证)
        select.click_sure_forward()
        time.sleep(3)
        self.assertEqual(chat.is_on_this_page(),True)
        #清空聊天记录-恢复环境
        chat.clear_all_chat_record()

    def tearDown_test_msg_xiaoliping_C_0023(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



    def setUp_test_msg_xiaoliping_C_0035(self):
        #1.从b手机进入与A手机的对话框
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.enter_phone_chatwindows_from_B_to_A()
        #进入与A手机的对话窗口，发送文件
        chat=ChatWindowPage()
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_local_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.docx')
        local_file.click_send_button()
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
        chat.click_coordinate(40,30)  #下载文件
        time.sleep(2)
        chat.swipe_by_percent_on_screen(25,20,25,30)
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
        #进入与A手机的对话窗口，发送文件
        chat=ChatWindowPage()
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_local_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.docx')
        local_file.click_send_button()
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
        chat=ChatWindowPage()
        chat.click_coordinate(40, 30)  # 下载文件
        chat.swipe_by_percent_on_screen(25,20,25,30)
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

    def tearDown_test_msg_xiaoliping_C_0038(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动-移动'])



    def setUp_test_msg_xiaoliping_C_0059(self):
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
        chat.swipe_by_percent_on_screen(25,20,25,30)
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
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.click_pic()
        select_pic=ChatPicPage()
        select_pic.click_camara_picture()
        select_pic.select_first_picture()
        select_pic.click_send()

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
        chat.swipe_by_percent_on_screen(25,20,25,30)
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
    def test_msg_xiaoliping_C_0063(self):
        """单聊会话页面，转发他人发送的视频给手机联系人"""
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
        chat.swipe_by_percent_on_screen(25,20,25,30)
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
        chat.swipe_by_percent_on_screen(25,20,25,30)
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
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_local_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.docx')
        local_file.click_send_button()
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
        chat.click_coordinate(40,30)  #下载文件
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
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_local_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.docx')
        local_file.click_send_button()
        time.sleep(2)

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
        chat.click_coordinate(40,30)  #下载文件
        time.sleep(2)
        chat.swipe_by_percent_on_screen(25,20,25,30)
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
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_local_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.docx')
        local_file.click_send_button()
        time.sleep(2)

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
        chat=ChatWindowPage()
        chat.click_coordinate(40, 30)  # 下载文件
        time.sleep(3)
        chat.swipe_by_percent_on_screen(25,20,25,30)
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
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_local_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.docx')
        local_file.click_send_button()
        time.sleep(2)

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
        chat=ChatWindowPage()
        chat.click_coordinate(40, 30)  # 下载文件
        time.sleep(3)
        chat.swipe_by_percent_on_screen(25,20,25,30)
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
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_local_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.docx')
        local_file.click_send_button()
        time.sleep(2)

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
        chat=ChatWindowPage()
        chat.click_coordinate(40, 30) # 下载文件
        time.sleep(3)
        chat.swipe_by_percent_on_screen(25,20,25,30)
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
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_local_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.docx')
        local_file.click_send_button()
        time.sleep(2)

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
        chat=ChatWindowPage()
        chat.click_coordinate(40, 30)  # 下载文件
        time.sleep(3)
        chat.swipe_by_percent_on_screen(25,20,25,30)
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
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_local_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.docx')
        local_file.click_send_button()
        time.sleep(2)

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
        chat=ChatWindowPage()
        chat.click_coordinate(40, 30)  # 下载文件
        time.sleep(3)
        chat.swipe_by_percent_on_screen(25,20,25,30)
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
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_local_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.docx')
        local_file.click_send_button()
        time.sleep(2)

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
        chat=ChatWindowPage()
        chat.click_coordinate(40, 30)  # 下载文件
        time.sleep(3)
        chat.swipe_by_percent_on_screen(25,20,25,30)
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
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_local_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.docx')
        local_file.click_send_button()
        time.sleep(2)

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
        chat=ChatWindowPage()
        # chat.click_coordinate(40, 30)  # 下载文件
        chat.swipe_by_percent_on_screen(25,20,25,30)
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
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_local_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.docx')
        local_file.click_send_button()
        time.sleep(2)

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
        MessagePage.click_text(phone_number_B)
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
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_local_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.docx')
        local_file.click_send_button()
        time.sleep(2)

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
        chat.click_coordinate(40, 30)
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
        chat.swipe_by_percent_on_screen(25, 20, 25, 30)
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
        chat.swipe_by_percent_on_screen(25, 30, 40, 30)
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
        chat.swipe_by_percent_on_screen(25, 30, 40, 30)
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
        chat.swipe_by_percent_on_screen(25, 30, 40, 30)
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
        chat.swipe_by_percent_on_screen(25, 30, 40, 30)
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
        chat.swipe_by_percent_on_screen(25, 30, 40, 30)
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


#单聊--名片

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
        chat.swipe_by_percent_on_screen(25, 30, 40, 30)
        time.sleep(2)
        chat.click_forward()
        #转发到我的电脑
        select = SelectContactsPage()
        select.click_search_contact()
        select.input_search_keyword('我的电脑')
        select.click_search_result()
        select.click_sure_forward()
        #转发到群聊
        chat.swipe_by_percent_on_screen(25, 30, 40, 30)
        # chat.long_press('个人名片')
        chat.click_forward()
        select.click_select_one_group()
        SelectOneGroupPage().selecting_one_group_by_name('群聊1')
        SelectOneGroupPage().click_sure_send()
        #转发到团队联系人
        chat.swipe_by_percent_on_screen(25, 30, 40, 30)
        # chat.long_press('个人名片')
        chat.click_forward()
        select.click_group_contact()
        group_contact=SelectHeContactsPage()
        group_contact.select_one_team_by_name('ateam7272')
        group_detail=SelectHeContactsDetailPage()
        group_detail.wait_for_he_contacts_page_load()
        group_detail.select_one_he_contact_by_name('alice')
        group_detail.click_sure()
        #转发到本地联系人
        chat.swipe_by_percent_on_screen(25, 30, 40, 30)
        # chat.long_press('个人名片')
        chat.click_forward()
        select.select_local_contacts()
        local_contact = SelectLocalContactsPage()
        self.assertEqual(local_contact.is_on_this_page(), True)
        local_contact.swipe_select_one_member_by_name('大佬2')
        local_contact.click_sure()

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
        chat.swipe_by_percent_on_screen(25, 30, 40, 30)
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


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
    def make_sure_chatwindow_exist_file(type='.docx'):
        """确保我的电脑页面有文件记录"""
        chat=ChatWindowPage()
        time.sleep(2)
        if chat.is_element_present_file():
            chat.wait_for_page_load()
        else:
            chat.click_file()
            csf = ChatSelectFilePage()
            csf.wait_for_page_load()
            time.sleep(2)
            csf.click_local_file()
            time.sleep(2)
            local_file = ChatSelectLocalFilePage()
            # type='.docx'
            local_file.select_file(type)
            local_file.click_send_button()
            time.sleep(2)

    @staticmethod
    def send_file(type='.docx'):
        """聊天界面-发送文件（默认.docx文件）"""
        chat=ChatWindowPage()
        time.sleep(2)
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_local_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(type)
        local_file.click_send_button()
        time.sleep(2)



class SingleChatFile(TestCase):
    """单聊--文件页面"""

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()

    def default_setUp(self):
        """确保每个用例执行前在单聊会话页面 """
        warnings.simplefilter('ignore', ResourceWarning)
        # 确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        # 进入单聊会话页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        if msg.is_text_present('大佬1'):
            msg.click_text('大佬1')
        else:
            msg.open_contacts_page()
            ContactsPage().click_phone_contact()
            ContactsPage().select_contacts_by_name('大佬1')
            ContactDetailsPage().click_message_icon()
            time.sleep(2)
            SingleChatPage().click_i_have_read()

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0075(self):
        """将自己发送的文件转发到普通群"""
        # 确保聊天界面有文件记录
        chat=ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        time.sleep(3)
        # 长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        # 点击转发
        chat.click_forward()
        time.sleep(2)
        # 判断在选择联系人界面
        select = SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 选择一个普通群
        select.click_select_one_group()
        select_group = SelectOneGroupPage()
        self.assertEqual(select_group.is_on_this_page(), True)
        select_group.selecting_one_group_by_name('群聊1')
        # 选择群后，弹起弹框
        time.sleep(2)
        select_group.page_should_contain_text('取消')
        select_group.page_should_contain_text('确定')
        select_group.click_sure_send()
        time.sleep(2)
        # 返回到聊天界面
        self.assertEqual(chat.is_on_this_page(), True)

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0076(self):
        """将自己发送的文件转发到企业群"""
        # 确保聊天界面有文件记录
        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        time.sleep(3)
        # 长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        # 点击转发
        chat.click_forward()
        time.sleep(2)
        # 判断在选择联系人界面
        select = SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 选择一个企业群
        select.click_select_one_group()
        select_group = SelectOneGroupPage()
        self.assertEqual(select_group.is_on_this_page(), True)
        select_group.select_one_company_group()
        # 选择群后，弹起弹框
        time.sleep(2)
        select_group.page_should_contain_text('取消')
        select_group.page_should_contain_text('确定')
        select_group.click_sure_send()
        time.sleep(2)
        # 返回到聊天界面
        self.assertEqual(chat.is_on_this_page(), True)


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0106(self):
        """将自己发送的文件转发到团队置灰的联系人"""
        # 确保聊天界面有文件记录
        chat = ChatWindowPage()
        phone_number= current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.make_sure_chatwindow_exist_file()
        time.sleep(2)
        # 长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        # 点击转发
        chat.click_forward()
        time.sleep(2)
        # 判断在选择联系人界面
        select = SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 选择一个团队未置灰的联系人
        select.click_he_contacts()
        group_contact = SelectHeContactsPage()
        group_contact.select_one_team_by_name('ateam7272')
        group_detail = SelectHeContactsDetailPage()
        group_detail.select_one_he_contact_by_name(phone_number)


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0125(self):
        """将自己发送的文件转发到我的电脑"""
        # 确保聊天界面有文件记录
        chat = ChatWindowPage()
        phone_number= current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.make_sure_chatwindow_exist_file()
        time.sleep(2)
        # 长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        # 点击转发
        chat.click_forward()
        time.sleep(2)
        # 判断在选择联系人界面
        select = SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 选择一个搜索我的电脑
        select.click_search_contact()
        select.input_search_keyword('我的电脑')
        select.click_element_by_id(text='搜索结果列表1')
        # 选择群后，弹起弹框
        time.sleep(2)
        select.page_should_contain_text('取消')
        select.page_should_contain_text('确定')
        select.click_sure_forward()
        time.sleep(2)
        # 返回到聊天界面
        self.assertEqual(chat.is_on_this_page(), True)


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0126(self):
        """将自己发送的文件转发到最近聊天"""
        # 确保聊天界面有文件记录
        chat = ChatWindowPage()
        phone_number= current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.make_sure_chatwindow_exist_file()
        time.sleep(2)
        # 长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        # 点击转发
        chat.click_forward()
        time.sleep(2)
        # 判断在选择联系人界面
        select = SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 选择最近聊天联系人
        select.click_recent_chat_contact()
        # 选择群后，弹起弹框
        time.sleep(2)
        select.page_should_contain_text('取消')
        select.page_should_contain_text('确定')
        select.click_sure_forward()
        time.sleep(2)
        # 返回到聊天界面
        self.assertEqual(chat.is_on_this_page(), True)


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0129(self):
        """将自己发送的文件进行删除"""
        # 确保聊天界面有文件记录
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
        Preconditions.make_sure_chatwindow_exist_file()
        time.sleep(2)
        # 长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        # 点击删除
        chat.click_delete()
        time.sleep(2)
        chat.page_should_contain_text('取消')
        chat.page_should_contain_text('删除')
        chat.click_sure_delete()
        time.sleep(2)
        self.assertEqual(chat.is_element_present_by_locator(locator='消息列表'),False)
        self.assertEqual(chat.is_on_this_page(), True)


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0130(self):
        """将自己发送的文件进行十秒内撤回"""
        # 确保聊天界面有文件记录
        chat = ChatWindowPage()
        if chat.is_element_present_by_locator(locator='消息列表'):
            chat.clear_all_chat_record()
        Preconditions.send_file()
        time.sleep(2)
        # 长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='撤回')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        # 点击撤回
        chat.click_revoke()
        time.sleep(2)
        chat.click_i_know()
        time.sleep(2)
        chat.page_down()
        self.assertTrue(chat.is_element_present_by_locator(locator='你撤回了一条消息'))


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0131(self):
        """将自己发送的文件进行收藏"""
        # 确保聊天界面有文件记录
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
        Preconditions.send_file()
        time.sleep(2)
        file_name=chat.get_file_name()
        # 长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        # 点击收藏
        chat.click_collection()
        time.sleep(2)
        # 返回收藏列表查看
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        collection = MeCollectionPage()
        collection_name=collection.get_first_file_name_in_collection()
        time.sleep(3)
        self.assertEqual(file_name, collection_name)


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0202(self):
        """在收藏列表中打开视频文件"""
        # 确保收藏列表有收藏的视频文件
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
          #聊天窗口 发送视频文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_video()
        time.sleep(2)
        csf.click_select_video()
           #长按收藏
        chat.press_and_move_right_video()
        time.sleep(2)
        chat.click_collection()
        time.sleep(2)
        # 返回收藏列表查看
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        #1.收藏页面 直接打开文件 可以正常查看
        collection = MeCollectionPage()
        collection.click_element_first_list()
        time.sleep(3)
        collection.page_should_contain_text('详情')
        collection.click_back()


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0203(self):
        """在收藏列表中打开音频文件"""
        # 确保收藏列表有收藏的音频文件
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
          #聊天窗口 发送音乐文件
        Preconditions.send_file(type='.mp3')
           #长按收藏
        chat.press_and_move_right_file(type='.mp3')
        time.sleep(2)
        chat.click_collection()
        time.sleep(2)
        # 返回收藏列表查看
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        #1.收藏页面 直接打开文件 可以正常查看
        collection = MeCollectionPage()
        collection.click_element_first_list()
        time.sleep(3)
        collection.page_should_contain_text('详情')
        collection.click_back()

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0204(self):
        """在收藏列表中打开图片文件"""
        # 确保收藏列表有收藏的图片文件
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
          #聊天窗口 发送图片文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_pic()
        time.sleep(2)
        select_pic=ChatPicPage()
        select_pic.click_camara_picture()
        select_pic.select_first_picture()
        select_pic.click_send()
        time.sleep(3)
           #长按收藏
        chat.press_and_move_right_file(type='.jpg')
        time.sleep(2)
        chat.click_collection()
        time.sleep(2)
        # 返回收藏列表查看
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        #1.收藏页面 直接打开文件 可以正常查看
        collection = MeCollectionPage()
        collection.click_element_first_list()
        time.sleep(3)
        collection.page_should_contain_text('详情')
        collection.click_back()

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0205(self):
        """在收藏列表中打开文本文件(点击文件格式为.txt .rtf .doc )"""
        # 确保收藏列表有收藏的音频文件
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
          #聊天窗口 发送音乐文件
        Preconditions.send_file(type='.txt')
           #长按收藏
        chat.press_and_move_right_file(type='.txt')
        time.sleep(2)
        chat.click_collection()
        time.sleep(2)
        # 返回收藏列表查看
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        #1.收藏页面 直接打开文件 可以正常查看
        collection = MeCollectionPage()
        collection.click_element_first_list()
        time.sleep(3)
        preview=ChatfileProviewPage()
        preview.page_contain_element(locator='预览文件-更多')

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0207(self):
        """在收藏页面打开表格格式为.xls  .xlsx"""
        # 确保收藏列表有收藏的音频文件
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
          #聊天窗口 发送音乐文件
        Preconditions.send_file(type='.xls')
           #长按收藏
        chat.press_and_move_right_file(type='.xls')
        time.sleep(2)
        chat.click_collection()
        time.sleep(2)
        # 返回收藏列表查看
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        #1.收藏页面 直接打开文件 可以正常查看
        collection = MeCollectionPage()
        collection.click_element_first_list()
        time.sleep(3)
        preview=ChatfileProviewPage()
        preview.page_contain_element(locator='预览文件-更多')


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0208(self):
        """在收藏页面打开表格格式为.pdf"""
        # 确保收藏列表有收藏的音频文件
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
          # 聊天窗口 发送音乐文件
        Preconditions.send_file(type='.pdf')
           #长按收藏
        chat.press_and_move_right_file(type='.pdf')
        time.sleep(2)
        chat.click_collection()
        time.sleep(2)
        # 返回收藏列表查看
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        # 1.收藏页面 直接打开文件 可以正常查看
        collection = MeCollectionPage()
        collection.click_element_first_list()
        time.sleep(3)
        preview=ChatfileProviewPage()
        preview.page_contain_element(locator='预览文件-更多')

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_1V1_0228(self):
        """发送文件"""
        # 1.点击文件列表中的其中一文件
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
        time.sleep(2)
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_local_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('docx')
        # 1.文件右边单选按钮变高亮，底部下方左边显示文件的大小，如：60.0B，底部右边发送按钮高亮(ios不涉及)
        # 2.点击发送
        local_file.click_send_button()
        # 2.自动跳转回消息页面，显示文件发送进度
        time.sleep(2)
        self.assertTrue(chat.is_on_this_page())

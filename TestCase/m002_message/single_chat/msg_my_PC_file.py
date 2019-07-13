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

    @staticmethod
    def make_sure_my_pc_have_file(type='.docx'):
        #从大佬1页面转发文件给我的电脑
        chat = ChatWindowPage()
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg = MessagePage()
        if msg.is_text_present('文件'):
            msg.click_text('文件')
        else:
            msg.click_search_box()
            msg.input_search_text('大佬1')
            msg.click_element_first_list()
            time.sleep(2)
            ContactDetailsPage().click_message_icon()
            Preconditions.send_file(type)
        #聊天窗口 转发文件给我的电脑
        chat.swipe_by_percent_on_screen(50,25,70,25)
        chat.click_forward()
        select=SelectContactsPage()
        select.click_search_contact()
        select.input_search_keyword('我的电脑')
        select.click_search_result()
        select.click_sure_forward()
        time.sleep(2)



# @unittest.skip('本地调试 不执行，双机用例写成单机，后期调整')
class MsgMyPCChatingDouble(TestCase):
    """
    表格：消息-我的电脑-文件

    """

    @classmethod
    def setUpClass(cls):
        """删除消息列表的消息记录"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()

    def default_setUp(self):
        """确保每个用例执行前在我的电脑聊天页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        #确保我的电脑页面有已下载的可预览文件
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_sure_my_pc_have_file()
        #进入消息页面
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        if msg.is_text_present('我的电脑'):
            msg.click_text('我的电脑')
        else:
            msg.click_search_box()
            msg.input_search_text('我的电脑')
            msg.click_element_first_list()

    def default_tearDown(self):
        #清空聊天记录
        Preconditions.make_already_in_message_page()
        MessagePage().click_text('我的电脑')
        ChatWindowPage().clear_all_chat_record()
        time.sleep(2)
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_msg_weifenglian_PC_0253(self):
        """验证在我的电脑会话窗口点击打开已下载的可预览文件时，右上角是否新增更多功能入口"""
        #确保当前页面有文件记录，默认.docx文件
        chat = ChatWindowPage()
        file_name=chat.get_file_name()
        chat.open_file_in_chat_page('.docx')
        time.sleep(2)
        preview_title=chat.get_prevoew_file_name()
        #验证点
        self.assertEqual(file_name,preview_title)
        chat.page_contain_element_more()
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_msg_weifenglian_PC_0254(self):
        """验证在我的电脑会话窗口点击打开已下载的可预览文件时，点击右上角的更多按钮是否正常调起选项"""
        chat=ChatWindowPage()
        chat.open_file_in_chat_page('.docx')
        time.sleep(2)
        chat.page_contain_element_more()
        #点击更多 吊起元素
        chat.click_more_Preview()
        chat.page_contain_element(locator='预览文件-转发')
        chat.page_contain_element(locator='预览文件-收藏')
        chat.page_contain_element(locator='其他应用打开')
        chat.page_contain_element(locator='预览文件-取消')
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_msg_weifenglian_PC_0256(self):
        """验证在我的电脑会话窗口点击打开已下载的可预览文件-右上角的更多按钮-转发时是否正常"""
        chat=ChatWindowPage()
        chat.open_file_in_chat_page('.docx')
        time.sleep(2)
        chat.page_contain_element_more()
        #点击更多 吊起元素
        chat.click_more_Preview()
        chat.page_contain_element(locator='预览文件-转发')
        chat.page_contain_element(locator='预览文件-收藏')
        chat.page_contain_element(locator='其他应用打开')
        chat.page_contain_element(locator='预览文件-取消')
        time.sleep(2)
        #点击转发,吊起联系人选择器
        chat.click_forward_Preview()
        select=SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        #选择联系人(toast)
        select.click_search_contact()
        select.input_search_keyword('大佬1')
        select.click_element_by_id(text='搜索结果列表1')
        select.click_sure_send()
        #检查回到预览文件页面（toast未验证）
        chat.wait_for_page_load_preview_file()
        chat.page_contain_element_more()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_msg_weifenglian_PC_0257(self):
        """验证在我的电脑会话窗口点击打开已下载的可预览文件-右上角的更多按钮-收藏时是否正常"""
        chat=ChatWindowPage()
        chat.open_file_in_chat_page('.docx')
        time.sleep(2)
        chat.page_contain_element_more()
        #点击更多 吊起元素
        chat.click_more_Preview()
        chat.page_contain_element(locator='预览文件-转发')
        chat.page_contain_element(locator='预览文件-收藏')
        chat.page_contain_element(locator='其他应用打开')
        chat.page_contain_element(locator='预览文件-取消')
        time.sleep(2)
        #点击收藏(toast无法验证)
        chat.click_collection_Preview()
        preview_name=chat.get_prevoew_file_name()
        #进入收藏列表-收藏列表显示该收藏文件
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me=MePage()
        me.click_collection()
        collection=MeCollectionPage()
        collection_file_name=collection.get_first_file_name_in_collection()
        self.assertEqual(preview_name,collection_file_name)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_msg_weifenglian_PC_0258(self):
        """验证在我的电脑会话窗口点击打开已下载的可预览文件-右上角的更多按钮-其他应用打开时是否正常"""
        chat=ChatWindowPage()

        chat.open_file_in_chat_page('.docx')
        time.sleep(2)
        chat.page_contain_element_more()
        #点击更多 吊起元素
        chat.click_more_Preview()
        chat.page_contain_element(locator='预览文件-转发')
        chat.page_contain_element(locator='预览文件-收藏')
        chat.page_contain_element(locator='其他应用打开')
        chat.page_contain_element(locator='预览文件-取消')
        time.sleep(2)
        #点击其他应用打开
        chat.click_other_App_open()
        time.sleep(2)
        chat.check_is_select_others_app_visionable()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_msg_weifenglian_PC_0261(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件时，右上角是否新增更多功能入口"""
        # 确保当前页面有文件记录，默认.docx文件

        chat = ChatWindowPage()
        #进入我的电脑-查找聊天文件页面-聊天文件页面
        chat.click_setting()
        setting=SingleChatSetPage()
        setting.search_chat_record()
        setting.click_file()
        #聊天文件页面
        chat_file=ChatFilePage()
        file_name=chat_file.get_file_name()
        chat_file.open_file_by_type('.docx')
        file_proview=ChatfileProviewPage()
        preview_name=file_proview.get_preview_file_name()
        #文件标题展示一样，成功打开文件
        self.assertEqual(file_name,preview_name)
        file_proview.page_contain_element_more()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_msg_weifenglian_PC_0264(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-转发时是否正常"""
        # 确保当前页面有文件记录，默认.docx文件

        chat = ChatWindowPage()
        #进入我的电脑-查找聊天文件页面-聊天文件页面
        chat.click_setting()
        setting=SingleChatSetPage()
        setting.search_chat_record()
        time.sleep(2)
        setting.click_file()
        #预览文件
        chat_file=ChatFilePage()
        chat_file.open_file_by_type('.docx')
        # 点击更多-判断页面的展示
        file_proview=ChatfileProviewPage()
        file_proview.click_more_Preview()
        chat.page_contain_element(locator='预览文件-转发')
        chat.page_contain_element(locator='预览文件-收藏')
        chat.page_contain_element(locator='其他应用打开')
        chat.page_contain_element(locator='预览文件-取消')
        # 点击转发文件
        file_proview.click_forward_Preview()
        select=SelectContactsPage()
        self.assertTrue(select.is_on_this_page())
        #选择联系人(toast)
        select.click_search_contact()
        select.input_search_keyword('大佬1')
        select.click_element_by_id(text='搜索结果列表1')
        select.click_sure_send()
        #检查回到预览文件页面（toast未验证）
        chat.wait_for_page_load_preview_file()
        self.assertTrue(file_proview.is_on_this_page())

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_msg_weifenglian_PC_0265(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-收藏时是否正常"""
        # 确保当前页面有文件记录，默认.docx文件

        chat = ChatWindowPage()
        #进入我的电脑-查找聊天文件页面-聊天文件页面
        chat.click_setting()
        setting=SingleChatSetPage()
        setting.search_chat_record()
        setting.click_file()
        #预览文件
        chat_file=ChatFilePage()
        chat_file.open_file_by_type('.docx')
        # 点击更多-判断页面的展示
        file_proview=ChatfileProviewPage()
        preview_name = file_proview.get_preview_file_name()
        file_proview.click_more_Preview()
        file_proview.page_contain_element(locator='预览文件-转发')
        file_proview.page_contain_element(locator='预览文件-收藏')
        file_proview.page_contain_element(locator='其他应用打开')
        file_proview.page_contain_element(locator='预览文件-取消')
        # 点击收藏文件(toast未验证)
        file_proview.click_collection_Preview()
        #判断收藏列表的展示
        Preconditions.make_already_in_message_page()
        #进入收藏列表-收藏列表显示该收藏文件
        MessagePage().open_me_page()
        me=MePage()
        me.click_collection()
        collection=MeCollectionPage()
        collection_file_name=collection.get_first_file_name_in_collection()
        time.sleep(2)
        self.assertEqual(preview_name,collection_file_name)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_msg_weifenglian_PC_0266(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-其他应用打开时是否正常"""
        # 确保当前页面有文件记录，默认.docx文件

        chat = ChatWindowPage()
        #进入我的电脑-查找聊天文件页面-聊天文件页面
        chat.click_setting()
        setting=SingleChatSetPage()
        setting.search_chat_record()
        setting.click_file()
        #预览文件
        chat_file=ChatFilePage()
        chat_file.open_file_by_type('.docx')
        # 点击更多-判断页面的展示
        file_proview=ChatfileProviewPage()
        file_proview.click_more_Preview()
        chat.page_contain_element(locator='预览文件-转发')
        chat.page_contain_element(locator='预览文件-收藏')
        chat.page_contain_element(locator='其他应用打开')
        chat.page_contain_element(locator='预览文件-取消')
        # 点击其他app打开
        file_proview.click_other_App_open()
        time.sleep(2)
        file_proview.check_is_select_others_app_visionable()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_msg_weifenglian_PC_0268(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的不可预览文件时，页面显示是否正常"""
        # 确保当前页面有不可预览文件
        Preconditions.send_file(type='.c')
        chat = ChatWindowPage()
        #点击进入查找聊天内容-文件页面
        chat.click_setting()
        setting = SingleChatSetPage()
        setting.search_chat_record()
        setting.click_file()
        #查找聊天内容页面-点击打开不可预览文件
        chat_file = ChatFilePage()
        chat_file.open_file_by_type('.c')
        time.sleep(2)
        #查看页面展示
        file_proview = ChatfileProviewPage()
        self.assertEqual(file_proview.is_exist_element(locator='不可预览文件-打开'),True)
        self.assertEqual(file_proview.is_exist_element(locator='预览文件-更多'), True)
        #点击打开按钮-调起应用选择器
        file_proview.click_open_icon()


    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_msg_weifenglian_PC_0272(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的不可预览文件-右上角的更多按钮-收藏时是否正常"""
        # 确保当前页面有不可预览文件
        Preconditions.send_file(type='.c')
        chat = ChatWindowPage()
        #点击进入查找聊天内容-文件页面
        chat.click_setting()
        setting = SingleChatSetPage()
        setting.search_chat_record()
        setting.click_file()
        #查找聊天内容页面-点击打开不可预览文件
        chat_file = ChatFilePage()
        chat_file.open_file_by_type('.c')
        time.sleep(2)
        #查看页面展示
        file_proview = ChatfileProviewPage()
        preview_name=file_proview.get_preview_file_name()
        file_proview.click_more_Preview()
        time.sleep(2)
        file_proview.page_contain_element(locator='预览文件-转发')
        file_proview.page_contain_element(locator='预览文件-收藏')
        file_proview.page_contain_element(locator='其他应用打开')
        file_proview.page_contain_element(locator='预览文件-取消')
        # 点击收藏文件(toast未验证)
        file_proview.click_collection_Preview()
        # 判断收藏列表的展示
        Preconditions.make_already_in_message_page()
        # 进入收藏列表-收藏列表显示该收藏文件
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        collection = MeCollectionPage()
        collection_file_name = collection.get_first_file_name_in_collection()
        time.sleep(2)
        self.assertEqual(preview_name, collection_file_name)



class MsgMyPCfile(TestCase):
    """我的电脑 文件"""

    @classmethod
    def setUpClass(cls):
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        msg.delete_all_message_list()

    @classmethod
    def default_setUp(self):
        """确保每个用例执行前在我的电脑聊天页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        if msg.is_text_present('我的电脑'):
            msg.click_text('我的电脑')
        else:
            msg.click_search_box()
            msg.input_search_text('我的电脑')
            msg.click_element_first_list()

    def default_tearDown(self):
        # ChatWindowPage().delete_file()

        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_PC_0001(self):
        """勾选本地文件内任意文件点击发送按钮"""
        #勾选本地文件 发送
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_file()
        #1,调转到选择文件页面-选择本地文件
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        self.assertTrue(csf.is_on_this_page())
        csf.click_local_file()
        time.sleep(2)
        #2,调转到文件列表页面
        local_file = ChatSelectLocalFilePage()
        self.assertEqual(local_file.is_on_this_page(),True)
        local_file.select_file('.docx')
        #3.发送成功
        local_file.click_send_button()
        time.sleep(2)
        self.assertEqual(chat.is_element_present_resend(), False)
        # 获取发送文件的名称
        chat = ChatWindowPage()
        time.sleep(2)
        #返回聊天列表
        chat.click_back()
        msg=MessagePage()
        msg.page_should_contain_text('文件')

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_PC_0014(self):
        """勾选本地文件内任意图片点击发送按钮"""
        #勾选本地文件 发送
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_file()
        #1,调转到选择文件页面-选择本地文件
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        self.assertTrue(csf.is_on_this_page())
        csf.click_pic()
        time.sleep(2)
        #2,调转到选择图片页面
        select_pic=ChatPicPage()
        self.assertEqual(select_pic.is_on_this_page(),True)
        select_pic.click_camara_picture()
        select_pic.select_first_picture()
        select_pic.click_send()
        #3.发送成功
        time.sleep(2)
        self.assertEqual(chat.is_element_present_resend(), False)
        # 返回聊天列表查看
        chat.click_back()
        msg=MessagePage()
        msg.wait_for_page_load()
        msg.page_should_contain_text('图片')

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_PC_0028(self):
        """勾选本地文件内任意视频点击发送按钮"""
        #进入本地文件页面
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_file()
        #1,调转到选择文件页面-选择本地文件
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        self.assertTrue(csf.is_on_this_page())
        csf.click_video()
        time.sleep(2)
        #2,调转到选择视频页面
        self.assertEqual(csf.is_on_this_page_select_video(),True)
        csf.click_select_video()
        #3.发送成功
        time.sleep(2)
        self.assertEqual(chat.is_element_present_resend(), False)
        # 返回聊天列表查看
        chat.click_back()
        msg=MessagePage()
        msg.wait_for_page_load()
        msg.page_should_contain_text('视频')


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_PC_0336(self):
        """我的电脑发送位置成功"""
        #勾选位置
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_more()
        chat.click_locator()
        #选择位置界面
        locator = ChatLocationPage()
        self.assertEqual(locator.is_on_this_page(),True)
        locator.click_send()
        #3.发送成功
        time.sleep(2)
        self.assertEqual(chat.is_element_present_resend(), False)
        # 返回聊天列表查看
        chat.click_back()
        msg = MessagePage()
        msg.wait_for_page_load()
        msg.page_should_contain_text('位置')





class LableGroupTest(TestCase):
    """标签分组---文件"""

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        contact = ContactsPage()
        contact.click_phone_contact()
        time.sleep(2)
        contact.click_label_grouping()
        LabelGroupingPage().delete_all_label()


    @classmethod
    def default_setUp(self):
        """确保每个用例执行前在标签分组会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        lable_group=LabelGroupingPage()
        lable_detail = LableGroupDetailPage()
        chat=ChatWindowPage()
        if chat.is_on_this_page():
            time.sleep(4)
        else:
            Preconditions.make_already_in_message_page()
            MessagePage().open_contacts_page()
            contact=ContactsPage()
            contact.click_phone_contact()
            time.sleep(2)
            contact.click_label_grouping()
            if lable_group.is_element_present(locator='已建分组列表1'):
                lable_group.click_first_lable_group()
            else:
                lable_group.creat_group('aaa')
                time.sleep(2)
                #为标签分组添加成员
                lable_group.click_first_lable_group()
                time.sleep(2)
                lable_detail.click_add_contact()
                local_contact = SelectLocalContactsPage()
                local_contact.swipe_select_one_member_by_name('大佬1')
                local_contact.swipe_select_one_member_by_name('大佬2')
                local_contact.click_sure()
            time.sleep(2)
            lable_detail.click_send_group_info()
            time.sleep(3)


    def default_tearDown(self):
        # ChatWindowPage().delete_file()

        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_fenzu_0001(self):
        """勾选本地文件内任意文件点击发送按钮"""
        #勾选本地文件 发送
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_file()
        #1,调转到选择文件页面-选择本地文件
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        self.assertTrue(csf.is_on_this_page())
        csf.click_local_file()
        time.sleep(2)
        #2,调转到文件列表页面
        local_file = ChatSelectLocalFilePage()
        self.assertEqual(local_file.is_on_this_page(),True)
        local_file.select_file('.docx')
        #3.发送成功
        local_file.click_send_button()
        time.sleep(2)
        self.assertEqual(chat.is_element_present_resend(), False)
        # 获取发送文件的名称
        chat = ChatWindowPage()
        time.sleep(2)
        #返回聊天列表
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.page_should_contain_text('文件')


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_fenzu_0014(self):
        """勾选本地文件内任意图片点击发送按钮"""
        #勾选本地文件 发送
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_file()
        #1,调转到选择文件页面-选择本地文件
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        self.assertTrue(csf.is_on_this_page())
        csf.click_pic()
        time.sleep(2)
        #2,调转到选择图片页面
        select_pic=ChatPicPage()
        self.assertEqual(select_pic.is_on_this_page(),True)
        select_pic.click_camara_picture()
        select_pic.select_first_picture()
        select_pic.click_send()
        #3.发送成功
        time.sleep(2)
        self.assertEqual(chat.is_element_present_resend(), False)
        # 返回聊天列表查看
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        msg.page_should_contain_text('图片')


    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_fenzu_0028(self):
        """勾选本地文件内任意视频点击发送按钮"""
        #进入本地文件页面
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_file()
        #1,调转到选择文件页面-选择本地文件
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        self.assertTrue(csf.is_on_this_page())
        csf.click_video()
        time.sleep(2)
        #2,调转到选择视频页面
        self.assertEqual(csf.is_on_this_page_select_video(),True)
        csf.click_select_video()
        #3.发送成功
        time.sleep(2)
        self.assertEqual(chat.is_element_present_resend(), False)
        # 返回聊天列表查看
        Preconditions.make_already_in_message_page()
        msg=MessagePage()
        msg.wait_for_page_load()
        msg.page_should_contain_text('视频')

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_fenzu_0157(self):
        """标签分组发送位置成功"""
        #勾选位置
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_more()
        chat.click_locator()
        #选择位置界面
        locator = ChatLocationPage()
        self.assertEqual(locator.is_on_this_page(),True)
        locator.click_send()
        #3.发送成功
        time.sleep(2)
        self.assertEqual(chat.is_element_present_resend(), False)
        # 返回聊天列表查看
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        msg.wait_for_page_load()
        msg.page_should_contain_text('位置')


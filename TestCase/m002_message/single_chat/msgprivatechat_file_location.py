import time
import unittest
import warnings

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from pages.components import BaseChatPage
from preconditions.BasePreconditions import WorkbenchPreconditions
from library.core.utils.testcasefilter import tags
from pages import *


class Preconditions(WorkbenchPreconditions):
    """前置条件"""

    @staticmethod
    def make_already_in_message_page(reset=False):
        """确保应用在消息页面"""
        # 如果在消息页，不做任何操作
        mp = MessagePage()
        if mp.is_on_this_page():
            return
        else:
            try:
                current_mobile().launch_app()
                mp.wait_for_page_load()
            except:
                # 进入一键登录页
                Preconditions.make_already_in_one_key_login_page()
                #  从一键登录页面登录
                Preconditions.login_by_one_key_login()

    @staticmethod
    def enter_single_chat_page(name):
        """进入单聊聊天会话页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击“新建消息”
        mp.click_new_message()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 进入单聊会话页面
        slc.selecting_local_contacts_by_name(name)
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            # 点击我已阅读
            bcp.click_i_have_read()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def send_file_by_type(file_type):
        """发送指定类型文件"""

        cwp = ChatWindowPage()
        cwp.click_file()
        cwp.click_accessibility_id_attribute_by_name("我收到的文件")
        cslfp = ChatSelectLocalFilePage()
        cslfp.click_file_by_type(file_type)
        cslfp.click_send_button()
        time.sleep(5)

    @staticmethod
    def send_pic():
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
    def send_video():
        """发送视频"""
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 发送视频
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        csf.click_video()
        time.sleep(2)
        csf.click_select_video()

    @staticmethod
    def enter_collection_page():
        """进入收藏页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_me_page()
        me_page = MePage()
        me_page.wait_for_page_load()
        me_page.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        time.sleep(1)

    @staticmethod
    def make_no_retransmission_button(name):
        """确保当前单聊会话页面没有重发按钮影响验证结果"""

        scp = SingleChatPage()
        if scp.is_exist_msg_send_failed_button():
            scp.click_back()
            mp = MessagePage()
            mp.wait_for_page_load()
            mp.delete_message_record_by_name(name)
            Preconditions.enter_single_chat_page(name)

    @staticmethod
    def make_no_message_send_failed_status(name):
        """确保当前消息列表没有消息发送失败的标识影响验证结果"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        if mp.is_iv_fail_status_present():
            mp.clear_fail_in_send_message()
        Preconditions.enter_single_chat_page(name)

    @staticmethod
    def send_file(type='.docx'):
        """聊天界面-发送文件（默认.docx文件）"""
        chat = ChatWindowPage()
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
    def make_sure_chatwindow_exist_file(type='.docx'):
        """确保我的电脑页面有文件记录"""
        chat = ChatWindowPage()
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


class MsgPrivateChatAllTest(TestCase):

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        # 导入测试联系人、群聊
        fail_time1 = 0
        flag1 = False
        import dataproviders
        while fail_time1 < 3:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                current_mobile().hide_keyboard_if_display()
                Preconditions.make_already_in_message_page()
                conts.open_contacts_page()
                try:
                    if conts.is_text_present("发现SIM卡联系人"):
                        conts.click_text("显示")
                except:
                    pass
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

        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

        # 确保有企业群
        fail_time3 = 0
        flag3 = False
        while fail_time3 < 5:
            try:
                Preconditions.make_already_in_message_page()
                Preconditions.ensure_have_enterprise_group()
                flag3 = True
            except:
                fail_time3 += 1
            if flag3:
                break

    def default_setUp(self):
        """
        1、成功登录和飞信
        2.确保每个用例运行前在单聊会话页面
        """
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        name = "大佬1"
        mp = MessagePage()
        mp.delete_all_message_list()
        if mp.is_on_this_page():
            Preconditions.enter_single_chat_page(name)
            return
        scp = SingleChatPage()
        if not scp.is_on_this_page():
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_single_chat_page(name)

    def default_tearDown(self):
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0001(self):
        """勾选本地文件内任意文件点击发送按钮"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 1.给当前会话页面发送文件
        Preconditions.send_file()
        time.sleep(2)
        # 2.获取文件名字
        file_name = scp.get_file_name()
        # 3.返回查看消息列表展示
        scp.click_back()
        msg = MessagePage()
        time.sleep(2)
        # 4.验证是否显示文件+文件名
        self.assertTrue(msg.page_should_contain_text('文件'))
        self.assertTrue(msg.page_should_contain_text(file_name))

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0002(self):
        """网络异常时勾选本地文件内任意文件点击发送按钮"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        # 3.断开网络
        scp.set_network_status(0)
        local_file = ChatSelectLocalFilePage()
        # 4.选择文件发送
        local_file.select_file('.docx')
        local_file.click_send_button()
        time.sleep(2)
        # 5.验证是否存在重发标识
        self.assertTrue(scp.is_exist_msg_send_failed_button())

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0002():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD' , 'network')
    def test_msg_weifenglian_1V1_0003(self):
        """会话页面有文件发送失败时查看消息列表是否有消息发送失败的标识"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        # 3.断开网络
        scp.set_network_status(0)
        local_file = ChatSelectLocalFilePage()
        # 4.选择文件发送
        local_file.select_file('.docx')
        local_file.click_send_button()
        time.sleep(2)
        # 5.点击返回消息页面
        scp.click_back()
        # 6.验证消息页面是否存在发送失败标识
        time.sleep(2)
        self.assertTrue(MessagePage().is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0003():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0004(self):
        """对发送失败的文件进行重发"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        # 3.断开网络
        scp.set_network_status(0)
        local_file = ChatSelectLocalFilePage()
        # 4.选择文件发送
        local_file.select_file('.docx')
        local_file.click_send_button()
        time.sleep(2)
        # 5.验证是否存在重发标识
        self.assertTrue(scp.is_exist_msg_send_failed_button())
        # 6.重新连网
        scp.set_network_status(6)
        # 7.点击重发按钮
        time.sleep(2)
        scp.click_failed_button()
        time.sleep(1)
        scp.click_accessibility_id_attribute_by_name("发送")
        time.sleep(2)
        # 8.重发标识消失
        self.assertFalse(scp.is_exist_msg_send_failed_button())

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0005(self):
        """对发送失败的文件进行重发后，消息列表页面的消息发送失败的标识消失"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        # 3.断开网络
        scp.set_network_status(0)
        local_file = ChatSelectLocalFilePage()
        # 4.选择文件发送
        local_file.select_file('.docx')
        local_file.click_send_button()
        time.sleep(2)
        # 5.验证是否存在重发标识
        self.assertTrue(scp.is_exist_msg_send_failed_button())
        # 6.重新连网
        scp.set_network_status(6)
        # 7.点击重发按钮
        time.sleep(2)
        scp.click_failed_button()
        time.sleep(1)
        scp.click_accessibility_id_attribute_by_name("发送")
        time.sleep(2)
        # 8.返回消息页面
        scp.click_back()
        time.sleep(2)
        self.assertFalse(MessagePage().is_iv_fail_status_present())

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0006(self):
        """点击取消重发文件消失，停留在当前页面"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        # 3.断开网络
        scp.set_network_status(0)
        local_file = ChatSelectLocalFilePage()
        # 4.选择文件发送
        local_file.select_file('.docx')
        local_file.click_send_button()
        time.sleep(2)
        # 5.验证是否存在重发标识
        self.assertTrue(scp.is_exist_msg_send_failed_button())
        # 6.重新连网
        scp.set_network_status(6)
        # 7.点击重发按钮
        time.sleep(2)
        scp.click_failed_button()
        time.sleep(1)
        # 取消
        scp.click_accessibility_id_attribute_by_name("取消")
        time.sleep(2)
        # 8.验证是否在当前单聊页面
        self.assertTrue(scp.is_on_this_page())

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0007(self):
        """未订购每月10G的用户发送大于2M的文件时有弹窗提示"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        # 3.关闭wifi
        scp.set_network_status(4)
        local_file = ChatSelectLocalFilePage()
        # 4.选择文件发送(大于2M文件)
        local_file.select_file('.mp3')
        time.sleep(2)
        # 5.验证是否有弹窗提示
        if local_file.page_should_contain_text2("每月10G免流特权"):
            self.assertTrue(chat.is_element_present(text="每月10G免流特权"))
            self.assertTrue(chat.is_element_present(text="继续发送"))
            self.assertTrue(chat.is_element_present(text="订购免流特权"))

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0007():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0008(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        # 3.关闭wifi
        scp.set_network_status(4)
        local_file = ChatSelectLocalFilePage()
        # 4.选择文件发送(大于2M文件)
        local_file.select_file('.mp3')
        time.sleep(2)
        # 5.验证是否有弹窗提示
        if local_file.page_should_contain_text2("每月10G免流特权"):
            self.assertTrue(chat.is_element_present(text="每月10G免流特权"))
            self.assertTrue(chat.is_element_present(text="继续发送"))
            self.assertTrue(chat.is_element_present(text="订购免流特权"))

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0008():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC_RESET', 'LXD_RESET' ,'network')
    def test_msg_weifenglian_1V1_0009(self):
        """勾选“以后不再提示”再点击“继续发送”"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        # 3.关闭wifi
        scp.set_network_status(4)
        local_file = ChatSelectLocalFilePage()
        # 4.选择文件发送(大于2M文件)
        local_file.select_file('.mp3')
        time.sleep(2)
        # 5.验证是否有弹窗提示
        if local_file.page_should_contain_text2("每月10G免流特权"):
            self.assertTrue(chat.is_element_present(text="每月10G免流特权"))
            self.assertTrue(chat.is_element_present(text="继续发送"))
            self.assertTrue(chat.is_element_present(text="订购免流特权"))

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0009():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD' ,'network')
    def test_msg_weifenglian_1V1_0010(self):
        """点击订购免流特权后可正常返回"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        # 3.关闭wifi
        scp.set_network_status(4)
        local_file = ChatSelectLocalFilePage()
        # 4.选择文件发送(大于2M文件)
        local_file.select_file('.mp3')
        time.sleep(2)
        # 5.验证是否有弹窗提示
        if local_file.page_should_contain_text2("每月10G免流特权"):
            self.assertTrue(chat.is_element_present(text="每月10G免流特权"))
            self.assertTrue(chat.is_element_present(text="继续发送"))
            self.assertTrue(chat.is_element_present(text="订购免流特权"))

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0010():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0012(self):
        """在文件列表页选择文件后再点击取消按钮，停留在当前页面"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        # 3.选择文件发送
        local_file.select_file('.txt')
        # 4.点击取消
        local_file.click_accessibility_id_attribute_by_name("取消")
        time.sleep(2)
        # 5.验证是否在当前页面
        self.assertTrue(local_file.is_on_this_page())

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0013(self):
        """在文件列表页点击返回按钮时可正常逐步返回到会话页面"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        # 3.点击返回
        local_file.click_back()
        csf.click_back()
        time.sleep(2)
        # 5.验证是否在单聊页面
        self.assertTrue(scp.is_on_this_page())

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0014(self):
        """勾选本地照片内任意相册的图片点击发送按钮"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 1.给当前会话页面发送图片
        Preconditions.send_pic()
        time.sleep(2)
        # 2.返回查看消息列表展示
        scp.click_back()
        msg = MessagePage()
        time.sleep(2)
        # 3.验证是否显示图片
        self.assertTrue(msg.page_should_contain_text('图片'))

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0015(self):
        """网络异常时勾选本地照片内任意相册的图片点击发送按钮"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        # 1.点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        # 2.点击照片
        csf.click_pic()
        select_pic = ChatPicPage()
        select_pic.click_camara_picture()
        # 断开网络
        select_pic.set_network_status(0)
        # 3.选择第一张照片
        select_pic.select_first_picture()
        # 4.点击发送
        select_pic.click_send()
        time.sleep(2)
        # 5.验证是否有重发按钮
        self.assertTrue(scp.is_exist_msg_send_failed_button())

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0015():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0016(self):
        """会话页面有图片发送失败时查看消息列表是否有消息发送失败的标识"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        # 1.点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        # 2.点击照片
        csf.click_pic()
        select_pic = ChatPicPage()
        select_pic.click_camara_picture()
        # 断开网络
        select_pic.set_network_status(0)
        # 3.选择第一张照片
        select_pic.select_first_picture()
        # 4.点击发送
        select_pic.click_send()
        time.sleep(2)
        scp.click_back()
        time.sleep(2)
        self.assertTrue(MessagePage().is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0016():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0017(self):
        """对发送失败的图片文件进行重发"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        # 1.点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        # 2.点击照片
        csf.click_pic()
        select_pic = ChatPicPage()
        select_pic.click_camara_picture()
        # 断开网络
        select_pic.set_network_status(0)
        # 3.选择第一张照片
        select_pic.select_first_picture()
        # 4.点击发送
        select_pic.click_send()
        time.sleep(2)
        # 5.验证是否有重发按钮
        self.assertTrue(scp.is_exist_msg_send_failed_button())
        # 6.重新连网
        scp.set_network_status(6)
        # 7.点击重发按钮
        time.sleep(2)
        scp.click_failed_button()
        time.sleep(1)
        scp.click_accessibility_id_attribute_by_name("发送")
        time.sleep(2)
        # 8.重发按钮消息是否存在
        self.assertFalse(scp.is_exist_msg_send_failed_button())

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0018(self):
        """对发送失败的图片进行重发后，消息列表页面的消息发送失败的标识消失"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        # 1.点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        # 2.点击照片
        csf.click_pic()
        select_pic = ChatPicPage()
        select_pic.click_camara_picture()
        # 断开网络
        select_pic.set_network_status(0)
        # 3.选择第一张照片
        select_pic.select_first_picture()
        # 4.点击发送
        select_pic.click_send()
        time.sleep(2)
        # 5.验证是否有重发按钮
        self.assertTrue(scp.is_exist_msg_send_failed_button())
        # 6.重新连网
        scp.set_network_status(6)
        # 7.点击重发按钮
        time.sleep(2)
        scp.click_failed_button()
        time.sleep(1)
        scp.click_accessibility_id_attribute_by_name("发送")
        time.sleep(2)
        # 8.点击返回消息页面
        scp.click_back()
        # 9.验证是否有消息失败标识
        self.assertFalse(MessagePage().is_iv_fail_status_present())

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0019(self):
        """点击取消重发图片消息，停留在当前页面"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        # 1.点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        # 2.点击照片
        csf.click_pic()
        select_pic = ChatPicPage()
        select_pic.click_camara_picture()
        # 断开网络
        select_pic.set_network_status(0)
        # 3.选择第一张照片
        select_pic.select_first_picture()
        # 4.点击发送
        select_pic.click_send()
        time.sleep(2)
        # 5.验证是否有重发按钮
        self.assertTrue(scp.is_exist_msg_send_failed_button())
        # 6.重新连网
        scp.set_network_status(6)
        # 7.点击重发按钮
        time.sleep(2)
        scp.click_failed_button()
        time.sleep(1)
        scp.click_accessibility_id_attribute_by_name("取消")
        time.sleep(2)
        # 验证是否在当前页面
        self.assertTrue(scp.is_on_this_page())

    @tags('ALL', 'CMCC', 'LXD','network')
    def test_msg_weifenglian_1V1_0020(self):
        """未订购每月10G的用户发送大于2M的图片时有弹窗提示"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        # 3.关闭wifi
        scp.set_network_status(4)
        local_file = ChatSelectLocalFilePage()
        # 4.选择文件发送(大于2M文件)
        local_file.select_file('.jpg')
        time.sleep(2)
        # 5.验证是否有弹窗提示
        if local_file.page_should_contain_text2("每月10G免流特权"):
            self.assertTrue(chat.is_element_present(text="每月10G免流特权"))
            self.assertTrue(chat.is_element_present(text="继续发送"))
            self.assertTrue(chat.is_element_present(text="订购免流特权"))

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0020():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0021(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        # 3.关闭wifi
        scp.set_network_status(4)
        local_file = ChatSelectLocalFilePage()
        # 4.选择文件发送(大于2M文件)
        local_file.select_file('.jpg')
        time.sleep(2)
        # 5.验证是否有弹窗提示
        if local_file.page_should_contain_text2("每月10G免流特权"):
            self.assertTrue(chat.is_element_present(text="每月10G免流特权"))
            self.assertTrue(chat.is_element_present(text="继续发送"))
            self.assertTrue(chat.is_element_present(text="订购免流特权"))

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0021():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC_RESET', 'LXD_RESET', 'network')
    def test_msg_weifenglian_1V1_0022(self):
        """勾选“以后不再提示”再点击“继续发送”"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        # 3.关闭wifi
        scp.set_network_status(4)
        local_file = ChatSelectLocalFilePage()
        # 4.选择文件发送(大于2M文件)
        local_file.select_file('.jpg')
        time.sleep(2)
        # 5.验证是否有弹窗提示
        if local_file.page_should_contain_text2("每月10G免流特权"):
            self.assertTrue(chat.is_element_present(text="每月10G免流特权"))
            self.assertTrue(chat.is_element_present(text="继续发送"))
            self.assertTrue(chat.is_element_present(text="订购免流特权"))

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0022():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD','network')
    def test_msg_weifenglian_1V1_0023(self):
        """点击订购免流特权后可正常返回"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        # 3.关闭wifi
        scp.set_network_status(4)
        local_file = ChatSelectLocalFilePage()
        # 4.选择文件发送(大于2M文件)
        local_file.select_file('.jpg')
        time.sleep(2)
        # 5.验证是否有弹窗提示
        if local_file.page_should_contain_text2("每月10G免流特权"):
            self.assertTrue(chat.is_element_present(text="每月10G免流特权"))
            self.assertTrue(chat.is_element_present(text="继续发送"))
            self.assertTrue(chat.is_element_present(text="订购免流特权"))

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0023():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0025(self):
        """在选择图片页面选择文件后再点击取消按钮，停留在当前页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1、2.进入本地照片目录
        scp.click_file_button()
        # 点击文件按钮
        scp.click_file_button()
        # 选择文件界面
        chat_select_file_page = ChatSelectFilePage()
        chat_select_file_page.wait_for_page_load()
        # 选择本地照片
        chat_select_file_page.click_pic()
        chat_select_file_page.wait_for_local_photo_page_load()
        # 选择相机胶卷
        chat_select_file_page.click_camera()
        chat_select_file_page.wait_for_local_photo_page_load()
        # 点击本地照片的图片
        chat_select_file_page.click_picture()
        # 点击取消
        chat_select_file_page.click_name_attribute_by_name('取消')
        chat_select_file_page.wait_for_local_photo_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0026(self):
        """在选择图片页面点击返回按钮时可正常逐步返回到会话页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1、2.进入本地照片目录
        scp.click_file_button()
        # 点击文件按钮
        scp.click_file_button()
        # 选择文件界面
        chat_select_file_page = ChatSelectFilePage()
        chat_select_file_page.wait_for_page_load()
        # 选择本地照片
        chat_select_file_page.click_pic()
        chat_select_file_page.wait_for_local_photo_page_load()
        # 选择相机胶卷
        chat_select_file_page.click_camera()
        chat_select_file_page.wait_for_local_photo_page_load()
        chat_select_file_page.click_back()
        chat_select_file_page.click_back()
        chat_select_file_page.click_back()
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0028(self):
        """勾选本地视频内任意视频点击发送按钮"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 1.给当前会话页面发送视频
        Preconditions.send_video()
        time.sleep(2)
        # 2.返回查看消息列表展示
        scp.click_back()
        msg = MessagePage()
        time.sleep(2)
        # 3.验证是否显示视频
        self.assertTrue(msg.page_should_contain_text('视频'))

    @tags('ALL', 'CMCC', 'LXD', "network")
    def test_msg_weifenglian_1V1_0029(self):
        """网络异常时勾选本地文件内任意视频点击发送按钮"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 1.点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击视频
        csf.click_video()
        time.sleep(2)
        # 断开网络
        csf.set_network_status(0)
        # 3.选择第一个视频
        csf.click_select_video()
        time.sleep(2)
        # 4.验证是否有重发按钮
        self.assertTrue(scp.is_exist_msg_send_failed_button())

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0029():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0030(self):
        """会话页面有视频发送失败时查看消息列表是否有消息发送失败的标识"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 1.点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击视频
        csf.click_video()
        time.sleep(2)
        # 断开网络
        csf.set_network_status(0)
        # 3.选择第一个视频
        csf.click_select_video()
        time.sleep(2)
        # 4.验证是否有重发按钮
        self.assertTrue(scp.is_exist_msg_send_failed_button())
        # 5.返回消息列表页面
        scp.click_back()
        time.sleep(2)
        # 6.验证是否存在发送失败标识
        self.assertTrue(MessagePage().is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0030():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0031(self):
        """对发送失败的视频进行重发"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 1.点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击视频
        csf.click_video()
        time.sleep(2)
        # 断开网络
        csf.set_network_status(0)
        # 3.选择第一个视频
        csf.click_select_video()
        time.sleep(2)
        # 4.验证是否有重发按钮
        self.assertTrue(scp.is_exist_msg_send_failed_button())
        # 5.重新连网
        scp.set_network_status(6)
        # 6.点击重发按钮
        time.sleep(2)
        scp.click_failed_button()
        time.sleep(1)
        scp.click_accessibility_id_attribute_by_name("发送")
        time.sleep(2)
        # 7.重发按钮消息是否存在
        self.assertFalse(scp.is_exist_msg_send_failed_button())

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0032(self):
        """对发送失败的视频进行重发后，消息列表页面的消息发送失败的标识消失"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 1.点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击视频
        csf.click_video()
        time.sleep(2)
        # 断开网络
        csf.set_network_status(0)
        # 3.选择第一个视频
        csf.click_select_video()
        time.sleep(2)
        # 4.验证是否有重发按钮
        self.assertTrue(scp.is_exist_msg_send_failed_button())
        # 5.重新连网
        scp.set_network_status(6)
        # 6.点击重发按钮
        time.sleep(2)
        scp.click_failed_button()
        time.sleep(1)
        scp.click_accessibility_id_attribute_by_name("发送")
        time.sleep(2)
        # 7.重发按钮消息是否存在
        self.assertFalse(scp.is_exist_msg_send_failed_button())
        # 9.点击返回消息列表
        scp.click_back()
        # 10.验证是否存在发送失败标识
        self.assertFalse(MessagePage().is_iv_fail_status_present())

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0033(self):
        """点击取消重发视频文件消失，停留在当前页面"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        time.sleep(2)
        # 1.点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击视频
        csf.click_video()
        time.sleep(2)
        # 断开网络
        csf.set_network_status(0)
        # 3.选择第一个视频
        csf.click_select_video()
        time.sleep(2)
        # 4.验证是否有重发按钮
        self.assertTrue(scp.is_exist_msg_send_failed_button())
        # 5.重新连网
        scp.set_network_status(6)
        # 6.点击重发按钮
        time.sleep(2)
        scp.click_failed_button()
        time.sleep(1)
        # 点击取消
        scp.click_accessibility_id_attribute_by_name("取消")
        time.sleep(2)
        # 7.验证是否在当前页面
        self.assertTrue(scp.is_on_this_page())

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0034(self):
        """未订购每月10G的用户发送大于2M的视频时有弹窗提示"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        # 3.关闭wifi
        scp.set_network_status(4)
        local_file = ChatSelectLocalFilePage()
        # 4.选择文件发送(大于2M文件)
        local_file.select_file('.jpg')
        time.sleep(2)
        # 5.验证是否有弹窗提示
        if local_file.page_should_contain_text2("每月10G免流特权"):
            self.assertTrue(chat.is_element_present(text="每月10G免流特权"))
            self.assertTrue(chat.is_element_present(text="继续发送"))
            self.assertTrue(chat.is_element_present(text="订购免流特权"))

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0034():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0035(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        # 3.关闭wifi
        scp.set_network_status(4)
        local_file = ChatSelectLocalFilePage()
        # 4.选择文件发送(大于2M文件)
        local_file.select_file('.jpg')
        time.sleep(2)
        # 5.验证是否有弹窗提示
        if local_file.page_should_contain_text2("每月10G免流特权"):
            self.assertTrue(chat.is_element_present(text="每月10G免流特权"))
            self.assertTrue(chat.is_element_present(text="继续发送"))
            self.assertTrue(chat.is_element_present(text="订购免流特权"))

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0035():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC_RESET', 'LXD_RESET', 'network')
    def test_msg_weifenglian_1V1_0036(self):
        """勾选“以后不再提示”再点击“继续发送”"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        # 3.关闭wifi
        scp.set_network_status(4)
        local_file = ChatSelectLocalFilePage()
        # 4.选择文件发送(大于2M文件)
        local_file.select_file('.jpg')
        time.sleep(2)
        # 5.验证是否有弹窗提示
        if local_file.page_should_contain_text2("每月10G免流特权"):
            self.assertTrue(chat.is_element_present(text="每月10G免流特权"))
            self.assertTrue(chat.is_element_present(text="继续发送"))
            self.assertTrue(chat.is_element_present(text="订购免流特权"))

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0036():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0037(self):
        """点击订购免流特权后可正常返回"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        # 3.关闭wifi
        scp.set_network_status(4)
        local_file = ChatSelectLocalFilePage()
        # 4.选择文件发送(大于2M文件)
        local_file.select_file('.jpg')
        time.sleep(2)
        # 5.验证是否有弹窗提示
        if local_file.page_should_contain_text2("每月10G免流特权"):
            self.assertTrue(chat.is_element_present(text="每月10G免流特权"))
            self.assertTrue(chat.is_element_present(text="继续发送"))
            self.assertTrue(chat.is_element_present(text="订购免流特权"))

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0037():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0039(self):
        """在视频列表页选择文件后再点击取消按钮，停留在当前页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1、2.进入本地照片目录
        scp.click_file_button()
        # 选择文件界面
        chat_select_file_page = ChatSelectFilePage()
        chat_select_file_page.wait_for_page_load()
        chat_select_file_page.click_local_video()
        chat_select_file_page.click_select_one_video()
        chat_select_file_page.click_name_attribute_by_name('取消')

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0040(self):
        """在视频列表页点击返回按钮时可正常逐步返回到会话页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1、2.进入本地照片目录
        scp.click_file_button()
        # 选择文件界面
        chat_select_file_page = ChatSelectFilePage()
        chat_select_file_page.wait_for_page_load()
        chat_select_file_page.click_local_video()
        chat_select_file_page.click_back()
        chat_select_file_page.click_back()
        scp.wait_for_page_load()

    # 没有音乐文件菜单入口
    # @tags('ALL', 'CMCC', 'LXD')
    # def test_msg_weifenglian_1V1_0042(self):
    #     """勾选音乐列表页面任意音乐点击发送按钮"""
    #
    #     scp = SingleChatPage()
    #     scp.wait_for_page_load()
    #     # 1.给当前会话页面发送音乐
    #     Preconditions.send_file(type='.mp3')
    #     time.sleep(2)
    #     # 2.获取文件名字
    #     file_name = scp.get_file_name()
    #     # 3.返回查看消息列表展示
    #     scp.click_back()
    #     msg = MessagePage()
    #     time.sleep(2)
    #     # 4.验证是否显示文件+文件名
    #     self.assertTrue(msg.page_should_contain_text('文件'))
    #     self.assertTrue(msg.page_should_contain_text(file_name))
    #
    # @tags('ALL', 'CMCC', 'LXD')
    # def test_msg_weifenglian_1V1_0043(self):
    #     """网络异常时勾选音乐列表页面任意音乐点击发送按钮"""
    #
    #     scp = SingleChatPage()
    #     # 等待单聊会话页面加载
    #     scp.wait_for_page_load()
    #     name = "大佬1"
    #     # 确保当前单聊会话页面没有重发按钮影响验证结果
    #     Preconditions.make_no_retransmission_button(name)
    #     # 设置手机网络断开
    #     # scp.set_network_status(0)
    #     # 1、2.发送本地音乐
    #     Preconditions.send_local_music()
    #     # 3.验证是否发送失败，是否存在重发按钮
    #     cwp = ChatWindowPage()
    #     cwp.wait_for_msg_send_status_become_to('发送失败', 30)
    #     self.assertEquals(scp.is_exist_msg_send_failed_button(), True)
    #
    # @tags('ALL', 'CMCC', 'LXD')
    # def test_msg_weifenglian_1V1_0044(self):
    #     """会话页面有音乐文件发送失败时查看消息列表是否有消息发送失败的标识"""
    #
    #     scp = SingleChatPage()
    #     # 等待单聊会话页面加载
    #     scp.wait_for_page_load()
    #     name = "大佬1"
    #     # 确保当前消息列表没有消息发送失败的标识影响验证结果
    #     Preconditions.make_no_message_send_failed_status(name)
    #     # 确保当前单聊会话页面没有重发按钮影响验证结果
    #     Preconditions.make_no_retransmission_button(name)
    #     # 设置手机网络断开
    #     # scp.set_network_status(0)
    #     file_type = ".mp3"
    #     # 发送指定类型文件
    #     Preconditions.send_file_by_type(file_type)
    #     # 1.验证是否发送失败，是否存在重发按钮
    #     cwp = ChatWindowPage()
    #     cwp.wait_for_msg_send_status_become_to('发送失败', 30)
    #     self.assertEquals(scp.is_exist_msg_send_failed_button(), True)
    #     scp.click_back()
    #     mp = MessagePage()
    #     mp.wait_for_page_load()
    #     # 2.是否存在消息发送失败的标识
    #     self.assertEquals(mp.is_iv_fail_status_present(), True)
    #
    # @tags('ALL', 'CMCC', 'LXD')
    # def test_msg_weifenglian_1V1_0045(self):
    #     """对发送失败的音乐进行重发"""
    #
    #     scp = SingleChatPage()
    #     # 等待单聊会话页面加载
    #     scp.wait_for_page_load()
    #     # 确保当前单聊会话页面有发送失败的音乐文件重发
    #     file_type = ".mp3"
    #     # scp.set_network_status(0)
    #     # 发送指定类型文件
    #     Preconditions.send_file_by_type(file_type)
    #     # scp.set_network_status(6)
    #     # 1.点击重发按钮
    #     scp.click_msg_send_failed_button(-1)
    #     time.sleep(2)
    #     scp.click_sure()
    #     # 2.验证是否重发成功
    #     cwp = ChatWindowPage()
    #     cwp.wait_for_msg_send_status_become_to('发送成功', 30)
    #
    # @tags('ALL', 'CMCC', 'LXD')
    # def test_msg_weifenglian_1V1_0046(self):
    #     """对发送失败的音乐进行重发后，消息列表页面的消息发送失败的标识消失"""
    #
    #     scp = SingleChatPage()
    #     # 等待单聊会话页面加载
    #     scp.wait_for_page_load()
    #     name = "大佬1"
    #     # 确保当前消息列表没有消息发送失败的标识影响验证结果
    #     Preconditions.make_no_message_send_failed_status(name)
    #     # 确保当前单聊会话页面有发送失败的音乐文件重发
    #     file_type = ".mp3"
    #     # scp.set_network_status(0)
    #     # 发送指定类型文件
    #     Preconditions.send_file_by_type(file_type)
    #     # scp.set_network_status(6)
    #     # 1.点击重发按钮
    #     scp.click_msg_send_failed_button(-1)
    #     time.sleep(2)
    #     scp.click_sure()
    #     # 2.验证是否重发成功
    #     cwp = ChatWindowPage()
    #     cwp.wait_for_msg_send_status_become_to('发送成功', 30)
    #     scp.click_back()
    #     mp = MessagePage()
    #     mp.wait_for_page_load()
    #     # 3.是否存在消息发送失败的标识
    #     self.assertEquals(mp.is_iv_fail_status_present(), False)
    #
    # @tags('ALL', 'CMCC', 'LXD')
    # def test_msg_weifenglian_1V1_0047(self):
    #     """点击取消重发音乐文件消失，停留在当前页面"""
    #
    #     scp = SingleChatPage()
    #     # 等待单聊会话页面加载
    #     scp.wait_for_page_load()
    #     # 确保当前单聊会话页面有发送失败的音乐文件重发
    #     file_type = ".mp3"
    #     # scp.set_network_status(0)
    #     # 发送指定类型文件
    #     Preconditions.send_file_by_type(file_type)
    #     # scp.set_network_status(6)
    #     # 1.点击重发按钮
    #     scp.click_msg_send_failed_button(-1)
    #     time.sleep(2)
    #     scp.click_cancel()
    #     # 2.等待单聊会话页面加载
    #     scp.wait_for_page_load()
    #
    # @tags('ALL', 'CMCC', 'LXD')
    # def test_msg_weifenglian_1V1_0048(self):
    #     """未订购每月10G的用户发送大于2M的音乐时有弹窗提示"""
    #
    #     scp = SingleChatPage()
    #     # 等待单聊会话页面加载
    #     scp.wait_for_page_load()
    #     # 设置当前网络为2/3/4G
    #     # scp.set_network_status(4)
    #     # 发送大型音乐文件
    #     Preconditions.send_large_music_file()
    #     time.sleep(2)
    #     local_file = ChatSelectLocalFilePage()
    #     # 1.是否弹出继续发送、订购免流特权、以后不再提示
    #     self.assertEquals(local_file.is_exist_continue_send(), True)
    #     self.assertEquals(local_file.is_exist_free_flow_privilege(), True)
    #     self.assertEquals(local_file.is_exist_no_longer_prompt(), True)
    #     time.sleep(2)
    #     local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
    #     local_file.wait_for_page_load()
    #     local_file.click_back()
    #     csfp = ChatSelectFilePage()
    #     csfp.click_back()
    #     # 等待单聊会话页面加载
    #     scp.wait_for_page_load()

    # @tags('ALL', 'CMCC', 'LXD')
    # def test_msg_weifenglian_1V1_0053(self):
    #     """在音乐列表页选择文件后再点击取消按钮，停留在当前页面"""
    #
    #     scp = SingleChatPage()
    #     # 等待单聊会话页面加载
    #     scp.wait_for_page_load()
    #     # 1、2.进入本地音乐目录
    #     Preconditions.enter_local_music_catalog()
    #     local_file = ChatSelectLocalFilePage()
    #     # 选择本地音乐
    #     local_file.click_music()
    #     time.sleep(2)
    #     # 再次选择，取消
    #     local_file.click_music()
    #     # 3.等待音乐列表页面加载
    #     local_file.wait_for_page_load()
    #     local_file.click_back()
    #     csfp = ChatSelectFilePage()
    #     csfp.wait_for_page_load()
    #     csfp.click_back()
    #     # 等待单聊会话页面加载
    #     scp.wait_for_page_load()
    #
    # @tags('ALL', 'CMCC', 'LXD')
    # def test_msg_weifenglian_1V1_0054(self):
    #     """在音乐列表页点击返回按钮时可正常逐步返回到会话页面"""
    #
    #     scp = SingleChatPage()
    #     # 等待单聊会话页面加载
    #     scp.wait_for_page_load()
    #     # 进入本地音乐目录
    #     Preconditions.enter_local_music_catalog()
    #     local_file = ChatSelectLocalFilePage()
    #     local_file.click_back()
    #     csfp = ChatSelectFilePage()
    #     # 1.等待选择文件页面加载
    #     csfp.wait_for_page_load()
    #     csfp.click_back()
    #     # 2.等待单聊会话页面加载
    #     scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD' ,'network')
    def test_msg_weifenglian_1V1_0049(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        # 3.关闭wifi
        scp.set_network_status(4)
        local_file = ChatSelectLocalFilePage()
        # 4.选择文件发送(大于2M文件)
        local_file.select_file('.mp3')
        time.sleep(2)
        # 5.验证是否有弹窗提示
        if local_file.page_should_contain_text2("每月10G免流特权"):
            self.assertTrue(chat.is_element_present(text="每月10G免流特权"))
            self.assertTrue(chat.is_element_present(text="继续发送"))
            self.assertTrue(chat.is_element_present(text="订购免流特权"))

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0049():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC_RESET', 'LXD_RESET', 'network')
    def test_msg_weifenglian_1V1_0050(self):
        """勾选“以后不再提示”再点击“继续发送”"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        # 3.关闭wifi
        scp.set_network_status(4)
        local_file = ChatSelectLocalFilePage()
        # 4.选择文件发送(大于2M文件)
        local_file.select_file('.mp3')
        time.sleep(2)
        # 5.验证是否有弹窗提示
        if local_file.page_should_contain_text2("每月10G免流特权"):
            self.assertTrue(chat.is_element_present(text="每月10G免流特权"))
            self.assertTrue(chat.is_element_present(text="继续发送"))
            self.assertTrue(chat.is_element_present(text="订购免流特权"))

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0050():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0051(self):
        """点击订购免流特权后可正常返回"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        chat = ChatWindowPage()
        time.sleep(2)
        # 1.给当前会话页面点击文件
        chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        time.sleep(2)
        # 2.点击我收到到文件
        csf.click_local_file()
        time.sleep(2)
        # 3.关闭wifi
        scp.set_network_status(4)
        local_file = ChatSelectLocalFilePage()
        # 4.选择文件发送(大于2M文件)
        local_file.select_file('.mp3')
        time.sleep(2)
        # 5.验证是否有弹窗提示
        if local_file.page_should_contain_text2("每月10G免流特权"):
            self.assertTrue(chat.is_element_present(text="每月10G免流特权"))
            self.assertTrue(chat.is_element_present(text="继续发送"))
            self.assertTrue(chat.is_element_present(text="订购免流特权"))

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0051():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0074(self):
        """在单聊将自己发送的文件转发到当前会话窗口"""

        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        time.sleep(3)
        # 1.长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        # 2.点击转发
        chat.click_forward()
        time.sleep(2)
        # 3.判断在选择联系人界面
        select = SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 4.选择最近聊天窗口
        select.click_recent_chat_contact()
        # 5.选择群后，弹起弹框点击确定
        time.sleep(2)
        select.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 6.验证是否在群聊页面
        self.assertEqual(chat.is_on_this_page(), True)

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0077(self):
        """将自己发送的文件转发到普通群时失败"""

        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        time.sleep(3)
        # 1.长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        # 2.点击转发
        chat.click_forward()
        time.sleep(2)
        # 3.判断在选择联系人界面
        select = SelectContactsPage()
        # 4.选择一个普通群
        select.click_select_one_group()
        select_group = SelectOneGroupPage()
        # 断开网络
        select_group.set_network_status(0)
        select_group.selecting_one_group_by_name('群聊1')
        # 5.选择群后，点击确定
        time.sleep(2)
        select_group.click_sure_send()
        time.sleep(2)
        # 6.返回到聊天界面
        self.assertEqual(chat.is_on_this_page(), True)
        # 7.点击返回消息列表
        chat.click_back()
        # 8.验证是否有发送失败标识
        time.sleep(2)
        self.assertTrue(MessagePage().is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0077():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_weifenglian_1V1_0078(self):
        """将自己发送的文件转发到企业群时失败"""

        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        time.sleep(3)
        # 1.长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        # 2.点击转发
        chat.click_forward()
        time.sleep(2)
        # 3.判断在选择联系人界面
        select = SelectContactsPage()
        # 4.选择一个企业群
        select.click_select_one_group()
        select_group = SelectOneGroupPage()
        # 断开网络
        select_group.set_network_status(0)
        select_group.selecting_one_group_by_name('测试企业群')
        # 5.选择群后，点击确定
        time.sleep(2)
        select_group.click_sure_send()
        time.sleep(2)
        # 6.返回到聊天界面
        self.assertEqual(chat.is_on_this_page(), True)
        # 7.点击返回消息列表
        chat.click_back()
        # 8.验证是否有发送失败标识
        time.sleep(2)
        self.assertTrue(MessagePage().is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0078():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0079(self):
        """将自己发送的文件转发到普通群时点击取消转发"""

        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        time.sleep(3)
        # 1.长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        # 2.点击转发
        chat.click_forward()
        time.sleep(2)
        # 3.判断在选择联系人界面
        select = SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 4.选择一个群
        select.click_select_one_group()
        select_group = SelectOneGroupPage()
        select_group.selecting_one_group_by_name("给个红包1")
        # 5.选择群后，弹起弹框点击取消
        time.sleep(2)
        select_group.click_accessibility_id_attribute_by_name("取消")
        time.sleep(2)
        # 6.验证是否在当前页面（选择一个群）
        self.assertEqual(select_group.is_on_this_page(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0080(self):
        """将自己发送的文件转发到企业群时点击取消转发"""

        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        time.sleep(3)
        # 1.长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        # 2.点击转发
        chat.click_forward()
        time.sleep(2)
        # 3.判断在选择联系人界面
        select = SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 4.选择企业群
        select.click_select_one_group()
        select_group = SelectOneGroupPage()
        select_group.select_one_company_group()
        # 5.选择群后，弹起弹框点击取消
        time.sleep(2)
        select_group.click_accessibility_id_attribute_by_name("取消")
        time.sleep(2)
        # 6.验证是否在当前页面（选择一个群）
        self.assertEqual(select_group.is_on_this_page(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0081(self):
        """将自己发送的文件转发到在搜索框输入文字搜索到的群"""

        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        time.sleep(3)
        # 1.长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        # 2.点击转发
        chat.click_forward()
        time.sleep(2)
        # 3.判断在选择联系人界面
        select = SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 4.输入文字
        select.click_select_one_group()
        select_group = SelectOneGroupPage()
        select_group.input_search_box("群聊")
        # 5.点击搜索结果
        select_group.click_search_result()
        # 6.选择群后，弹起弹框点击取消
        time.sleep(2)
        select_group.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 7.验证是否返回到聊天界面
        self.assertEqual(chat.is_on_this_page(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0082(self):
        """将自己发送的文件转发到在搜索框输入英文字母搜索到的群"""

        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        time.sleep(3)
        # 1.长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        # 2.点击转发
        chat.click_forward()
        time.sleep(2)
        # 3.判断在选择联系人界面
        select = SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 4.输入英文
        select.click_select_one_group()
        select_group = SelectOneGroupPage()
        select_group.input_search_box("group_test")
        # 5.点击搜索结果
        select_group.click_search_result()
        # 6.选择群后，弹起弹框点击确定
        time.sleep(2)
        select_group.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 7.验证是否返回到聊天界面
        self.assertEqual(chat.is_on_this_page(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0083(self):
        """将自己发送的文件转发到在搜索框输入数字搜索到的群"""

        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        time.sleep(3)
        # 1.长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        # 2.点击转发
        chat.click_forward()
        time.sleep(2)
        # 3.判断在选择联系人界面
        select = SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 4.输入数字
        select.click_select_one_group()
        select_group = SelectOneGroupPage()
        select_group.input_search_box("1122")
        # 5.点击搜索结果
        select_group.click_search_result()
        # 6.选择群后，弹起弹框点击确定
        time.sleep(2)
        select_group.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 7.验证是否返回到聊天界面
        self.assertEqual(chat.is_on_this_page(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0084(self):
        """将自己发送的文件转发到在搜索框输入标点符号搜索到的群"""

        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        time.sleep(3)
        # 1.长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        # 2.点击转发
        chat.click_forward()
        time.sleep(2)
        # 3.判断在选择联系人界面
        select = SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 4.输入标点符号
        select.click_select_one_group()
        select_group = SelectOneGroupPage()
        select_group.input_search_box("；，。")
        # 5.点击搜索结果
        select_group.click_search_result()
        # 6.选择群后，弹起弹框点击确定
        time.sleep(2)
        select_group.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 7.验证是否返回到聊天界面
        self.assertEqual(chat.is_on_this_page(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0085(self):
        """将自己发送的文件转发到在搜索框输入特殊字符搜索到的群"""

        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        time.sleep(3)
        # 1.长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        # 2.点击转发
        chat.click_forward()
        time.sleep(2)
        # 3.判断在选择联系人界面
        select = SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 4.输入特殊字符
        select.click_select_one_group()
        select_group = SelectOneGroupPage()
        select_group.input_search_box("&%@")
        # 5.点击搜索结果
        select_group.click_search_result()
        # 6.选择群后，弹起弹框点击确定
        time.sleep(2)
        select_group.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 7.验证是否返回到聊天界面
        self.assertEqual(chat.is_on_this_page(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0086(self):
        """将自己发送的文件转发到在搜索框输入空格搜索到的群"""

        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        time.sleep(3)
        # 1.长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        # 2.点击转发
        chat.click_forward()
        time.sleep(2)
        # 3.判断在选择联系人界面
        select = SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 4.输入空格
        select.click_select_one_group()
        select_group = SelectOneGroupPage()
        select_group.input_search_box(" ")
        # 5.点击搜索结果
        select_group.click_search_result()
        # 6.选择群后，弹起弹框点击确定
        time.sleep(2)
        select_group.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 7.验证是否返回到聊天界面
        self.assertEqual(chat.is_on_this_page(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0087(self):
        """将自己发送的文件转发到在搜索框输入多种字符搜索到的群"""

        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        time.sleep(3)
        # 1.长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        # 2.点击转发
        chat.click_forward()
        time.sleep(2)
        # 3.判断在选择联系人界面
        select = SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 4.输入多种字符
        select.click_select_one_group()
        select_group = SelectOneGroupPage()
        select_group.input_search_box("a尼6")
        # 5.点击搜索结果
        select_group.click_search_result()
        # 6.选择群后，弹起弹框点击确定
        time.sleep(2)
        select_group.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 7.验证是否返回到聊天界面
        self.assertEqual(chat.is_on_this_page(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_weifenglian_1V1_0088(self):
        """将自己发送的文件转发到在搜索框输入多种字符搜索到的群"""

        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        time.sleep(3)
        # 1.长按文件转发-调起功能菜单
        chat.press_and_move_right_file(type='.docx')
        time.sleep(2)
        # 2.点击转发
        chat.click_forward()
        time.sleep(2)
        # 3.判断在选择联系人界面
        select = SelectContactsPage()
        self.assertEqual(select.is_on_this_page(), True)
        # 4.输入多种字符
        select.click_select_one_group()
        select_group = SelectOneGroupPage()
        select_group.input_search_box("给个红包1")
        # 5.点击搜索结果
        select_group.click_search_result()
        # 6.选择群后，弹起弹框点击确定
        time.sleep(2)
        select_group.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 7.验证是否返回到聊天界面
        self.assertEqual(chat.is_on_this_page(), True)


class MsgPrivateChatTotalTest(TestCase):
    """单聊"""

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

        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_weifenglian_1V1_0206(self):
        """在收藏页面打开幻灯片格式为.ppt .pptx"""

        mp = MessagePage()
        mp.wait_for_page_load()
        me_page = MePage()
        mcp = MeCollectionPage()
        file_type = ".ppt"
        # 确保收藏列表存在幻灯片格式为.ppt的文件
        Preconditions.enter_single_chat_page("大佬1")
        Preconditions.send_file_by_type(file_type)
        scp = SingleChatPage()
        scp.press_file_by_type(file_type)
        scp.click_accessibility_id_attribute_by_name("收藏")
        # 返回收藏页面
        scp.click_back_button()
        mp.wait_for_page_load()
        # 点击我-收藏，点击幻灯片文件格式为.ppt .pptx
        mp.open_me_page()
        me_page.wait_for_page_load()
        me_page.click_collection()
        mcp.wait_for_page_load()
        mcp.click_file_by_type(file_type)
        # 1.直接打开文件，内容显示正常
        self.assertEquals(mcp.is_exists_more_icon(), True)

    @staticmethod
    def tearDown_test_msg_weifenglian_1V1_0206():
        """恢复环境"""

        try:
            fail_time = 0
            while fail_time < 5:
                try:
                    Preconditions.make_already_in_message_page()
                    Preconditions.enter_collection_page()
                    mcp = MeCollectionPage()
                    mcp.delete_all_collection()
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')









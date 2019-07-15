import random
import time
import re
import warnings

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver
from pages.components import BaseChatPage
from preconditions.BasePreconditions import WorkbenchPreconditions
from library.core.utils.testcasefilter import tags
from pages import *
import unittest

class Preconditions(WorkbenchPreconditions):
    """前置条件"""

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
    def make_already_have_my_picture():
        """确保当前页面已有图片"""

        # 1.点击输入框左上方的相册图标
        scp = SingleChatPage()
        cpp = ChatPicPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        if scp.is_exist_msg_image():
            return
        else:
            # 2.进入相片页面,选择一张片相发送
            time.sleep(2)
            scp.click_picture()
            cpp.wait_for_page_load()
            cpp.select_pic_fk(1)
            cpp.click_send()
            time.sleep(5)

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
    def make_no_message_send_failed_status():
        """确保当前消息列表没有消息发送失败的标识影响验证结果"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        if mp.is_iv_fail_status_present():
            mp.clear_fail_in_send_message()

    @staticmethod
    def if_exists_multiple_enterprises_enter_single_chat():
        """选择团队联系人时存在多个团队时返回获取当前团队名，再进入单聊转发图片"""

        shc = SelectHeContactsDetailPage()
        # 测试号码是否存在多个团队
        if not shc.is_exist_corporate_grade():
            mp = MessagePage()
            scg = SelectContactsPage()
            scp = SingleChatPage()
            shc.click_back()
            scg.wait_for_page_load()
            scg.click_back()
            scp.wait_for_page_load()
            scp.click_back()
            mp.wait_for_page_load()
            mp.open_workbench_page()
            wbp = WorkbenchPage()
            wbp.wait_for_workbench_page_load()
            time.sleep(2)
            # 获取当前团队名
            workbench_name = wbp.get_workbench_name()
            mp.open_message_page()
            mp.wait_for_page_load()
            single_name = "大佬1"
            Preconditions.enter_single_chat_page(single_name)
            scp.forward_pic()
            scg.wait_for_page_load()
            scg.click_he_contacts()
            shc.wait_for_he_contacts_page_load()
            # 选择当前团队
            shc.click_department_name(workbench_name)

# lxd_debug
class MsgPrivateChatVideoPicAllTest(TestCase):

    # @classmethod
    # def setUpClass(cls):
    #
    #     Preconditions.select_mobile('IOS-移动')
    #     # 导入测试联系人、群聊
    #     fail_time1 = 0
    #     flag1 = False
    #     import dataproviders
    #     while fail_time1 < 3:
    #         try:
    #             required_contacts = dataproviders.get_preset_contacts()
    #             conts = ContactsPage()
    #             current_mobile().hide_keyboard_if_display()
    #             Preconditions.make_already_in_message_page()
    #             conts.open_contacts_page()
    #             try:
    #                 if conts.is_text_present("发现SIM卡联系人"):
    #                     conts.click_text("显示")
    #             except:
    #                 pass
    #             for name, number in required_contacts:
    #                 # 创建联系人
    #                 conts.create_contacts_if_not_exits(name, number)
    #             required_group_chats = dataproviders.get_preset_group_chats()
    #             conts.open_group_chat_list()
    #             group_list = GroupListPage()
    #             for group_name, members in required_group_chats:
    #                 group_list.wait_for_page_load()
    #                 # 创建群
    #                 group_list.create_group_chats_if_not_exits(group_name, members)
    #             group_list.click_back()
    #             conts.open_message_page()
    #             flag1 = True
    #         except:
    #             fail_time1 += 1
    #         if flag1:
    #             break
    #
    #     # 导入团队联系人
    #     fail_time2 = 0
    #     flag2 = False
    #     while fail_time2 < 5:
    #         try:
    #             Preconditions.make_already_in_message_page()
    #             contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
    #             Preconditions.create_he_contacts(contact_names)
    #             flag2 = True
    #         except:
    #             fail_time2 += 1
    #         if flag2:
    #             break
    #
    #     # 确保有企业群
    #     fail_time3 = 0
    #     flag3 = False
    #     while fail_time3 < 5:
    #         try:
    #             Preconditions.make_already_in_message_page()
    #             Preconditions.ensure_have_enterprise_group()
    #             flag3 = True
    #         except:
    #             fail_time3 += 1
    #         if flag3:
    #             break

    def default_setUp(self):
        """
        1、成功登录和飞信
        2.确保每个用例运行前在单聊会话页面
        """
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        name = "香港大佬"
        mp = MessagePage()
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

    @tags('ALL', 'CMCC', "msg")
    def test_msg_xiaoliping_C_0001(self):
        """单聊会话页面，不勾选相册内图片点击发送按钮"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.不选择照片时，发送按钮是否置灰展示并且不可点击
        flag = cpg.send_btn_is_enabled()
        print(flag)
        self.assertEquals(flag, False)
        # 回到聊天回话页面
        for i in range(3):
            cpg.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'CMCC', "msg")
    def test_msg_xiaoliping_C_0002(self):
        """单聊会话页面，勾选相册内一张图片发送"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，点击右下角高亮展示的发送按钮，发送此照片
        cpg.select_picture()
        # 发送按钮可点击
        self.assertTrue(cpg.send_btn_is_enabled())
        cpg.click_send()
        chat.wait_for_page_load()
        self.assertTrue(chat.is_on_this_page)

    @tags('ALL', 'CMCC', "msg")
    def test_msg_xiaoliping_C_0003(self):
        """单聊会话页面，预览相册内图片"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，点击左下角的预览按钮
        cpg.select_picture()
        cpg.click_preview()
        time.sleep(1)
        cpg.page_should_contain_text("预览(1/1)")

    @tags('ALL', 'CMCC', "msg")
    def test_msg_xiaoliping_C_0004(self):
        """单聊会话页面，预览相册内图片，不勾选原图发送"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，点击左下角的预览按钮
        cpg.select_picture()
        cpg.click_preview()
        time.sleep(1)
        cpg.page_should_contain_text("预览(1/1)")
        cppp = ChatPicPreviewPage()
        # 3.直接点击发送按钮
        cppp.click_send()
        chat.wait_for_page_load()
        self.assertTrue(chat.is_on_this_page)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0041(self):
        """单聊会话页面，转发自己发送的图片到当前会话窗口"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 给当前会话页面发送一张图片,确保最近聊天中有记录
        cpp = ChatPicPage()
        time.sleep(2)
        scp.click_picture()
        cpp.wait_for_page_load()
        cpp.select_pic_fk(1)
        cpp.click_send()
        time.sleep(5)
        contact_name = "大佬1"
        # 解决发送图片后，最近聊天窗口没有记录，需要退出刷新的问题
        scp.click_back()
        # 返回时做一个判断，避免被别的模块影响执行
        mp = MessagePage()
        if not mp.is_on_this_page():
            cdp = ContactDetailsPage()
            cdp.click_back_icon()
            cp = ContactsPage()
            cp.wait_for_contacts_page_load()
            mp.open_message_page()
            Preconditions.enter_single_chat_page(contact_name)
            scp.click_picture()
            cpp.wait_for_page_load()
            cpp.select_pic_fk(1)
            cpp.click_send()
            time.sleep(5)
            scp.click_back()
        Preconditions.enter_single_chat_page(contact_name)
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 3.选择最近聊天中的当前会话窗口
        scg.select_recent_chat_by_name(contact_name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0042(self):
        """单聊会话页面，转发自己发送的图片到当前会话窗口时失败"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 给当前会话页面发送一张图片,确保最近聊天中有记录
        cpp = ChatPicPage()
        time.sleep(2)
        scp.click_picture()
        cpp.wait_for_page_load()
        cpp.select_pic_fk(1)
        cpp.click_send()
        time.sleep(5)
        scp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        contact_name = "大佬1"
        Preconditions.enter_single_chat_page(contact_name)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置手机网络断开
        # scp.set_network_status(0)
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 3.选择最近聊天中的当前会话窗口
        scg.select_recent_chat_by_name(contact_name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0043(self):
        """单聊会话页面，转发自己发送的图片到当前会话窗口时点击取消转发"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 给当前会话页面发送一张图片,确保最近聊天中有记录
        cpp = ChatPicPage()
        time.sleep(2)
        scp.click_picture()
        cpp.wait_for_page_load()
        cpp.select_pic_fk(1)
        cpp.click_send()
        time.sleep(5)
        # 解决发送图片后，最近聊天窗口没有记录，需要退出刷新的问题
        scp.click_back()
        contact_name = "大佬1"
        Preconditions.enter_single_chat_page(contact_name)
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 3.选择最近聊天中的当前会话窗口
        scg.select_recent_chat_by_name(contact_name)
        # 取消转发
        scg.click_cancel_forward()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 返回单聊会话页面
        scg.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0044(self):
        """单聊会话页面，转发自己发送的图片给手机联系人"""

        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择本地联系人”菜单
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        name = "大佬2"
        # 3.选择一个手机联系人
        slc.selecting_local_contacts_by_name(name)
        # 确定转发
        slc.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        time.sleep(2)
        mp = MessagePage()
        if not mp.is_on_this_page():
            cdp = ContactDetailsPage()
            cdp.click_back_icon()
            cp = ContactsPage()
            cp.wait_for_page_load()
            cp.open_message_page()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 选择刚发送消息的聊天页
        mp.choose_chat_by_name(name)
        time.sleep(2)
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            # 点击我已阅读
            bcp.click_i_have_read()
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 返回消息页
        scp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0045(self):
        """单聊会话页面，转发自己发送的图片到手机联系人时失败"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        scp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        contact_name = "大佬1"
        Preconditions.enter_single_chat_page(contact_name)
        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置手机网络断开
        # scp.set_network_status(0)
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择本地联系人”菜单
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        name = "大佬2"
        # 3.选择一个手机联系人
        slc.selecting_local_contacts_by_name(name)
        # 确定转发
        slc.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0046(self):
        """单聊会话页面，转发自己发送的图片到手机联系人时点击取消转发"""

        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择本地联系人”菜单
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        name = "大佬2"
        # 3.选择一个手机联系人
        slc.selecting_local_contacts_by_name(name)
        # 取消转发
        slc.click_cancel_forward()
        # 4.等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        # 返回单聊会话页面
        slc.click_back()
        scg.wait_for_page_load()
        scg.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0047(self):
        """单聊会话页面，转发自己发送的图片给团队联系人"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择和通讯录联系人”菜单
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        # 等待选择联系人->和通讯录联系人 页面加载
        shc.wait_for_he_contacts_page_load()
        # 3.选择一个团队联系人
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_enter_single_chat()
        name = "大佬3"
        shc.selecting_he_contacts_by_name(name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        mp = MessagePage()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 选择刚发送消息的聊天页
        mp.choose_chat_by_name(name)
        time.sleep(2)
        chat = BaseChatPage()
        if chat.is_exist_dialog():
            # 点击我已阅读
            chat.click_i_have_read()
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 返回消息页
        scp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0048(self):
        """单聊会话页面，转发自己发送的图片到团队联系人时失败"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        scp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        contact_name = "大佬1"
        Preconditions.enter_single_chat_page(contact_name)
        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        # 设置手机网络断开
        # scp.set_network_status(0)
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择和通讯录联系人”菜单
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        # 等待选择联系人->和通讯录联系人 页面加载
        shc.wait_for_he_contacts_page_load()
        # 3.选择一个团队联系人
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_enter_single_chat()
        name = "大佬3"
        shc.selecting_he_contacts_by_name(name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0049(self):
        """单聊会话页面，转发自己发送的图片到团队联系人时点击取消转发"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择和通讯录联系人”菜单
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        # 等待选择联系人->和通讯录联系人 页面加载
        shc.wait_for_he_contacts_page_load()
        # 3.选择一个团队联系人
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_enter_single_chat()
        name = "大佬3"
        shc.selecting_he_contacts_by_name(name)
        # 取消转发
        scg.click_cancel_forward()
        # 4.等待选择联系人->和通讯录联系人 页面加载
        shc.wait_for_he_contacts_page_load()
        # 返回单聊会话页面
        shc.click_back()
        shc.click_back()
        scg.wait_for_page_load()
        scg.click_back()
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0050(self):
        """单聊会话页面，转发自己发送的图片给陌生人"""

        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        number = "13855558888"
        # 输入陌生手机号码
        scg.input_search_keyword(number)
        time.sleep(2)
        current_mobile().hide_keyboard_if_display()
        # 3.选择陌生号码转发
        scg.click_unknown_member()
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        mp = MessagePage()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 选择刚发送消息的陌生联系人
        mp.choose_chat_by_name(number)
        time.sleep(2)
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            # 点击我已阅读
            bcp.click_i_have_read()
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 返回消息页
        scp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0051(self):
        """单聊会话页面，转发自己发送的图片到陌生人时失败"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        scp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        contact_name = "大佬1"
        Preconditions.enter_single_chat_page(contact_name)
        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置手机网络断开
        # scp.set_network_status(0)
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        number = "13855558888"
        # 输入陌生手机号码
        scg.input_search_keyword(number)
        time.sleep(2)
        current_mobile().hide_keyboard_if_display()
        # 3.选择陌生号码转发
        scg.click_unknown_member()
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0052(self):
        """单聊会话页面，转发自己发送的图片到陌生人时点击取消转发"""

        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        number = "13855558888"
        # 输入陌生手机号码
        scg.input_search_keyword(number)
        time.sleep(2)
        current_mobile().hide_keyboard_if_display()
        # 3.选择陌生号码转发
        scg.click_unknown_member()
        # 取消转发
        scg.click_cancel_forward()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 返回单聊会话页面
        scg.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0053(self):
        """单聊会话页面，转发自己发送的图片到普通群"""

        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        name = "群聊1"
        # 3.选择一个普通群
        sog.selecting_one_group_by_name(name)
        # 确定转发
        sog.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        time.sleep(2)
        mp = MessagePage()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 选择刚发送消息的聊天页
        mp.choose_chat_by_name(name)
        time.sleep(2)
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 返回消息页
        scp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0054(self):
        """单聊会话页面，转发自己发送的图片到普通群时失败"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        scp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        contact_name = "大佬1"
        Preconditions.enter_single_chat_page(contact_name)
        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置手机网络断开
        # scp.set_network_status(0)
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        group_name = "群聊1"
        # 3.选择一个普通群
        sog.selecting_one_group_by_name(group_name)
        # 确定转发
        sog.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0055(self):
        """单聊会话页面，转发自己发送的图片到普通群时点击取消转发"""

        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        name = "群聊1"
        # 3.选择一个普通群
        sog.selecting_one_group_by_name(name)
        # 取消转发
        sog.click_cancel_forward()
        # 4.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        sog.click_back()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 返回单聊会话页面
        scg.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0056(self):
        """单聊会话页面，转发自己发送的图片到企业群"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 3.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 4.选择一个企业群
        name = sog.select_one_enterprise_group()
        # 确定转发
        sog.click_sure_forward()
        # 5.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        time.sleep(2)
        mp = MessagePage()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 选择刚发送消息的聊天页
        mp.choose_chat_by_name(name)
        time.sleep(2)
        # 验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 返回消息页
        scp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0057(self):
        """单聊会话页面，转发自己发送的图片到企业群时失败"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        scp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        contact_name = "大佬1"
        Preconditions.enter_single_chat_page(contact_name)
        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置手机网络断开
        # scp.set_network_status(0)
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 3.选择一个企业群
        sog.select_one_enterprise_group()
        # 确定转发
        sog.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0058(self):
        """单聊会话页面，转发自己发送的图片到企业群时点击取消转发"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 3.选择一个企业群
        sog.select_one_enterprise_group()
        # 取消转发
        sog.click_cancel_forward()
        # 4.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        sog.click_back()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 返回单聊会话页面
        scg.click_back()


class MsgPrivateChatSessionPageTest(TestCase):

    # @classmethod
    # def setUpClass(cls):
    #
    #     Preconditions.select_mobile('IOS-移动')
    #     # 导入测试联系人、群聊
    #     fail_time1 = 0
    #     flag1 = False
    #     import dataproviders
    #     while fail_time1 < 3:
    #         try:
    #             required_contacts = dataproviders.get_preset_contacts()
    #             conts = ContactsPage()
    #             Preconditions.make_already_in_message_page()
    #             conts.open_contacts_page()
    #             for name, number in required_contacts:
    #                 # 创建联系人
    #                 conts.create_contacts_if_not_exits(name, number)
    #             required_group_chats = dataproviders.get_preset_group_chats()
    #             conts.open_group_chat_list()
    #             group_list = GroupListPage()
    #             for group_name, members in required_group_chats:
    #                 group_list.wait_for_page_load()
    #                 # 创建群
    #                 group_list.create_group_chats_if_not_exits(group_name, members)
    #             group_list.click_back()
    #             conts.open_message_page()
    #             flag1 = True
    #         except:
    #             fail_time1 += 1
    #         if flag1:
    #             break

    def default_setUp(self):
        """
        1、成功登录和飞信
        2.确保每个用例运行前在单聊会话页面
        """
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        name = "大佬1"
        Preconditions.make_already_in_message_page()
        Preconditions.enter_single_chat_page(name)

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    def test_msg_xiaoliping_C_0005(self):
        """单聊会话页面，预览相册数量与发送按钮数量一致"""
        # 等待界面加载
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        # 点击选择照片
        single_chat_page.click_picture()
        # 选择图片页面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择多张图片
        chat_pic_page.select_pictures(3)
        # 点击预览
        chat_pic_page.click_preview()
        # 预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        # 获取预览数文本
        text1 = chat_pic_preview_page.get_preview_text()
        # 获取发送按钮文本
        text2 = chat_pic_preview_page.get_send_text()
        # 判断预览数与发送数是否相等
        self.assertEquals(text1, text2)

    def test_msg_xiaoliping_C_0006(self):
        """"""





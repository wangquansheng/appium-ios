import time
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
        name = "大佬1"
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
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.press_and_move_right_file(type='.jpg')
        time.sleep(3)
        # 3.点击转发
        scp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 5.选择最近聊天中的当前会话窗口
        scg.selecting_local_contacts_by_name("大佬1")
        time.sleep(2)
        # 6.点击确定转发
        scg.click_sure_forward()
        # 验证是否提示已转发
        # self.assertTrue(scp.page_should_contain_text2("已转发"))
        # 8.验证当前页面在单聊页面
        self.assertTrue(scp.is_on_this_page())
        time.sleep(2)


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
        # 等待界面加载
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        single_chat_page.click_back()
        message_page = MessagePage()
        # 进入我-设置-消息 将消息送达状态显示开关关闭
        message_page.click_me_button()
        me_page = MePage()
        me_page.wait_for_page_load()
        me_page.click_setting_other()
        time.sleep(2)
        me_set_up_page = MeSetUpPage()
        me_set_up_page.click_message()
        # 点击消息送达状态显示开关 开启状态将其关闭
        if me_set_up_page.get_no_disturbing_btn_text() == "1":
            me_set_up_page.click_no_disturbing_button()
        # 点击两次返回
        me_set_up_page.click_back()
        me_set_up_page.click_back()
        me_page.wait_for_page_load()
        # 在我界面点击消息回到消息界面
        me_page.click_message_button()
        message_page.wait_for_page_load()
        Preconditions.enter_single_chat_page('大佬1')
        # 选择图片页面 先发送文字 在发送图片第一次发送的消息捕捉不到
        single_chat_page.input_text_message('测试文本')
        single_chat_page.click_send_btn()
        single_chat_page.click_picture()
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_pictures(1)
        # 点击发送
        chat_pic_page.click_send()
        single_chat_page.wait_for_page_load()
        # 长按图片
        single_chat_page.press_last_message(2, '转发')
        self.assertEquals(single_chat_page.page_should_contain_text2('选择联系人'), True)
        single_chat_page.click_name_attribute_by_name('大佬1')
        single_chat_page.click_name_attribute_by_name('取消')
        # 点击返回然
        single_chat_page.click_back()
        single_chat_page.wait_for_page_load()

    def tearDown_test_msg_xiaoliping_C_0043(self):
        """恢复环境，将用例开启的消息状态送达开关开启"""

        try:
            # 进入我-设置-消息 将消息送达状态显示开关关闭
            Preconditions.make_already_in_message_page()
            message_page = MessagePage()
            message_page.click_me_button()
            me_page = MePage()
            me_page.wait_for_page_load()
            me_page.click_setting_other()
            time.sleep(2)
            me_set_up_page = MeSetUpPage()
            me_set_up_page.click_message()
            # 点击消息送达状态显示开关 开启状态将其关闭
            if me_set_up_page.get_no_disturbing_btn_text() == "0":
                me_set_up_page.click_no_disturbing_button()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')


    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0044(self):
        """单聊会话页面，转发自己发送的图片给手机联系人"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.press_and_move_right_file(type='.jpg')
        time.sleep(3)
        # 3.点击转发
        scp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        time.sleep(2)
        # 4.点击选择一个手机联系人
        scg.click_phone_contact()
        time.sleep(2)
        slp = SelectLocalContactsPage()
        slp.selecting_local_contacts_by_name("大佬2")
        # 5.点击确定转发
        slp.click_sure()
        time.sleep(2)
        # 6.验证当前页面在单聊页面
        self.assertTrue(scp.is_on_this_page())
        time.sleep(2)

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
        # 等待界面加载
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        single_chat_page.click_back()
        message_page = MessagePage()
        # 进入我-设置-消息 将消息送达状态显示开关关闭
        message_page.click_me_button()
        me_page = MePage()
        me_page.wait_for_page_load()
        me_page.click_setting_other()
        time.sleep(2)
        me_set_up_page = MeSetUpPage()
        me_set_up_page.click_message()
        # 点击消息送达状态显示开关 开启状态将其关闭
        if me_set_up_page.get_no_disturbing_btn_text() == "1":
            me_set_up_page.click_no_disturbing_button()
        # 点击两次返回
        me_set_up_page.click_back()
        me_set_up_page.click_back()
        me_page.wait_for_page_load()
        # 在我界面点击消息回到消息界面
        me_page.click_message_button()
        message_page.wait_for_page_load()
        Preconditions.enter_single_chat_page('大佬1')
        # 选择图片页面 先发送文字 在发送图片第一次发送的消息捕捉不到
        single_chat_page.input_text_message('测试文本')
        single_chat_page.click_send_btn()
        single_chat_page.click_picture()
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_pictures(1)
        # 点击发送
        chat_pic_page.click_send()
        single_chat_page.wait_for_page_load()
        # 长按图片
        single_chat_page.press_last_message(2, '转发')
        self.assertEquals(single_chat_page.page_should_contain_text2('选择联系人'), True)
        single_chat_page.click_name_attribute_by_name('大佬1')
        single_chat_page.click_name_attribute_by_name('取消')
        # 点击返回然
        single_chat_page.click_back()
        single_chat_page.wait_for_page_load()

    def tearDown_test_msg_xiaoliping_C_0046(self):
        """恢复环境，将用例开启的消息状态送达开关开启"""

        try:
            # 进入我-设置-消息 将消息送达状态显示开关关闭
            Preconditions.make_already_in_message_page()
            message_page = MessagePage()
            message_page.click_me_button()
            me_page = MePage()
            me_page.wait_for_page_load()
            me_page.click_setting_other()
            time.sleep(2)
            me_set_up_page = MeSetUpPage()
            me_set_up_page.click_message()
            # 点击消息送达状态显示开关 开启状态将其关闭
            if me_set_up_page.get_no_disturbing_btn_text() == "0":
                me_set_up_page.click_no_disturbing_button()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0047(self):
        """单聊会话页面，转发自己发送的图片给团队联系人"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.press_and_move_right_file(type='.jpg')
        time.sleep(3)
        # 3.点击转发
        scp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        time.sleep(2)
        # 4.点击选择团队联系人
        scg.click_group_contact()
        time.sleep(2)
        shp = SelectHeContactsPage()
        shp.input_search_text("大佬1")
        time.sleep(2)
        shp.click_element_by_id()
        time.sleep(2)
        # 5.点击确定转发
        shp.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 6.验证当前页面在单聊页面
        self.assertTrue(scp.is_on_this_page())
        time.sleep(2)



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
        # 等待界面加载
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        single_chat_page.click_back()
        message_page = MessagePage()
        # 进入我-设置-消息 将消息送达状态显示开关关闭
        message_page.click_me_button()
        me_page = MePage()
        me_page.wait_for_page_load()
        me_page.click_setting_other()
        time.sleep(2)
        me_set_up_page = MeSetUpPage()
        me_set_up_page.click_message()
        # 点击消息送达状态显示开关 开启状态将其关闭
        if me_set_up_page.get_no_disturbing_btn_text() == "1":
            me_set_up_page.click_no_disturbing_button()
        # 点击两次返回
        me_set_up_page.click_back()
        me_set_up_page.click_back()
        me_page.wait_for_page_load()
        # 在我界面点击消息回到消息界面
        me_page.click_message_button()
        message_page.wait_for_page_load()
        Preconditions.enter_single_chat_page('大佬1')
        # 选择图片页面 先发送文字 在发送图片第一次发送的消息捕捉不到
        single_chat_page.input_text_message('测试文本')
        single_chat_page.click_send_btn()
        single_chat_page.click_picture()
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_pictures(1)
        # 点击发送
        chat_pic_page.click_send()
        single_chat_page.wait_for_page_load()
        # 长按图片
        single_chat_page.press_last_message(2, '转发')
        self.assertEquals(single_chat_page.page_should_contain_text2('选择联系人'), True)
        single_chat_page.click_name_attribute_by_name('团队联系人')
        single_chat_page.click_name_attribute_by_name('我的团队')
        single_chat_page.click_name_attribute_by_name('测试1')
        single_chat_page.click_name_attribute_by_name('取消')

    def tearDown_test_msg_xiaoliping_C_0049(self):
        """恢复环境，将用例开启的消息状态送达开关开启"""

        try:
            # 进入我-设置-消息 将消息送达状态显示开关关闭
            Preconditions.make_already_in_message_page()
            message_page = MessagePage()
            message_page.click_me_button()
            me_page = MePage()
            me_page.wait_for_page_load()
            me_page.click_setting_other()
            time.sleep(2)
            me_set_up_page = MeSetUpPage()
            me_set_up_page.click_message()
            # 点击消息送达状态显示开关 开启状态将其关闭
            if me_set_up_page.get_no_disturbing_btn_text() == "0":
                me_set_up_page.click_no_disturbing_button()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0050(self):
        """单聊会话页面，转发自己发送的图片给陌生人"""
        # 等待界面加载
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        single_chat_page.click_back()
        message_page = MessagePage()
        # 进入我-设置-消息 将消息送达状态显示开关关闭
        message_page.click_me_button()
        me_page = MePage()
        me_page.wait_for_page_load()
        me_page.click_setting_other()
        time.sleep(2)
        me_set_up_page = MeSetUpPage()
        me_set_up_page.click_message()
        # 点击消息送达状态显示开关 开启状态将其关闭
        if me_set_up_page.get_no_disturbing_btn_text() == "1":
            me_set_up_page.click_no_disturbing_button()
        # 点击两次返回
        me_set_up_page.click_back()
        me_set_up_page.click_back()
        me_page.wait_for_page_load()
        # 在我界面点击消息回到消息界面
        me_page.click_message_button()
        message_page.wait_for_page_load()
        Preconditions.enter_single_chat_page('大佬1')
        # 选择图片页面 先发送文字 在发送图片第一次发送的消息捕捉不到
        single_chat_page.input_text_message('测试文本')
        single_chat_page.click_send_btn()
        single_chat_page.click_picture()
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_pictures(1)
        # 点击发送
        chat_pic_page.click_send()
        single_chat_page.wait_for_page_load()
        # 长按图片
        single_chat_page.press_last_message(2, '转发')
        select_contacts_page = SelectContactsPage()
        select_contacts_page.input_search_text('13333333333')
        time.sleep(2)
        single_chat_page.click_name_attribute_by_name('13333333333（未知号码）')
        single_chat_page.click_name_attribute_by_name('确定')
        single_chat_page.wait_for_page_load()

    def tearDown_test_msg_xiaoliping_C_0050(self):
        """恢复环境，将用例开启的消息状态送达开关开启"""

        try:
            # 进入我-设置-消息 将消息送达状态显示开关关闭
            Preconditions.make_already_in_message_page()
            message_page = MessagePage()
            message_page.click_me_button()
            me_page = MePage()
            me_page.wait_for_page_load()
            me_page.click_setting_other()
            time.sleep(2)
            me_set_up_page = MeSetUpPage()
            me_set_up_page.click_message()
            # 点击消息送达状态显示开关 开启状态将其关闭
            if me_set_up_page.get_no_disturbing_btn_text() == "0":
                me_set_up_page.click_no_disturbing_button()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

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

        # 等待界面加载
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        single_chat_page.click_back()
        message_page = MessagePage()
        # 进入我-设置-消息 将消息送达状态显示开关关闭
        message_page.click_me_button()
        me_page = MePage()
        me_page.wait_for_page_load()
        me_page.click_setting_other()
        time.sleep(2)
        me_set_up_page = MeSetUpPage()
        me_set_up_page.click_message()
        # 点击消息送达状态显示开关 开启状态将其关闭
        if me_set_up_page.get_no_disturbing_btn_text() == "1":
            me_set_up_page.click_no_disturbing_button()
        # 点击两次返回
        me_set_up_page.click_back()
        me_set_up_page.click_back()
        me_page.wait_for_page_load()
        # 在我界面点击消息回到消息界面
        me_page.click_message_button()
        message_page.wait_for_page_load()
        Preconditions.enter_single_chat_page('大佬1')
        # 选择图片页面 先发送文字 在发送图片第一次发送的消息捕捉不到
        single_chat_page.input_text_message('测试文本')
        single_chat_page.click_send_btn()
        single_chat_page.click_picture()
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_pictures(1)
        # 点击发送
        chat_pic_page.click_send()
        single_chat_page.wait_for_page_load()
        # 长按图片
        single_chat_page.press_last_message(2, '转发')
        select_contacts_page = SelectContactsPage()
        select_contacts_page.input_search_text('13333333333')
        time.sleep(2)
        single_chat_page.click_name_attribute_by_name('13333333333（未知号码）')
        single_chat_page.click_name_attribute_by_name('取消')

    def tearDown_test_msg_xiaoliping_C_0052(self):
        """恢复环境，将用例开启的消息状态送达开关开启"""

        try:
            # 进入我-设置-消息 将消息送达状态显示开关关闭
            Preconditions.make_already_in_message_page()
            message_page = MessagePage()
            message_page.click_me_button()
            me_page = MePage()
            me_page.wait_for_page_load()
            me_page.click_setting_other()
            time.sleep(2)
            me_set_up_page = MeSetUpPage()
            me_set_up_page.click_message()
            # 点击消息送达状态显示开关 开启状态将其关闭
            if me_set_up_page.get_no_disturbing_btn_text() == "0":
                me_set_up_page.click_no_disturbing_button()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0053(self):
        """单聊会话页面，转发自己发送的图片到普通群"""

        # 等待界面加载
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        single_chat_page.click_back()
        message_page = MessagePage()
        # 进入我-设置-消息 将消息送达状态显示开关关闭
        message_page.click_me_button()
        me_page = MePage()
        me_page.wait_for_page_load()
        me_page.click_setting_other()
        time.sleep(2)
        me_set_up_page = MeSetUpPage()
        me_set_up_page.click_message()
        # 点击消息送达状态显示开关 开启状态将其关闭
        if me_set_up_page.get_no_disturbing_btn_text() == "1":
            me_set_up_page.click_no_disturbing_button()
        # 点击两次返回
        me_set_up_page.click_back()
        me_set_up_page.click_back()
        me_page.wait_for_page_load()
        # 在我界面点击消息回到消息界面
        me_page.click_message_button()
        message_page.wait_for_page_load()
        Preconditions.enter_single_chat_page('大佬1')
        # 选择图片页面 先发送文字 在发送图片第一次发送的消息捕捉不到
        single_chat_page.input_text_message('测试文本')
        single_chat_page.click_send_btn()
        single_chat_page.click_picture()
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_pictures(1)
        # 点击发送
        chat_pic_page.click_send()
        single_chat_page.wait_for_page_load()
        # 长按图片
        single_chat_page.press_last_message(2, '转发')
        select_contacts_page = SelectContactsPage()
        select_contacts_page.click_select_one_group()
        select_contacts_page.selecting_one_group_by_name('群聊1')
        time.sleep(2)
        single_chat_page.click_name_attribute_by_name('确定')
        single_chat_page.wait_for_page_load()

    def tearDown_test_msg_xiaoliping_C_0053(self):
        """恢复环境，将用例开启的消息状态送达开关开启"""

        try:
            # 进入我-设置-消息 将消息送达状态显示开关关闭
            Preconditions.make_already_in_message_page()
            message_page = MessagePage()
            message_page.click_me_button()
            me_page = MePage()
            me_page.wait_for_page_load()
            me_page.click_setting_other()
            time.sleep(2)
            me_set_up_page = MeSetUpPage()
            me_set_up_page.click_message()
            # 点击消息送达状态显示开关 开启状态将其关闭
            if me_set_up_page.get_no_disturbing_btn_text() == "0":
                me_set_up_page.click_no_disturbing_button()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

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

        # 等待界面加载
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        single_chat_page.click_back()
        message_page = MessagePage()
        # 进入我-设置-消息 将消息送达状态显示开关关闭
        message_page.click_me_button()
        me_page = MePage()
        me_page.wait_for_page_load()
        me_page.click_setting_other()
        time.sleep(2)
        me_set_up_page = MeSetUpPage()
        me_set_up_page.click_message()
        # 点击消息送达状态显示开关 开启状态将其关闭
        if me_set_up_page.get_no_disturbing_btn_text() == "1":
            me_set_up_page.click_no_disturbing_button()
        # 点击两次返回
        me_set_up_page.click_back()
        me_set_up_page.click_back()
        me_page.wait_for_page_load()
        # 在我界面点击消息回到消息界面
        me_page.click_message_button()
        message_page.wait_for_page_load()
        Preconditions.enter_single_chat_page('大佬1')
        # 选择图片页面 先发送文字 在发送图片第一次发送的消息捕捉不到
        single_chat_page.input_text_message('测试文本')
        single_chat_page.click_send_btn()
        single_chat_page.click_picture()
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_pictures(1)
        # 点击发送
        chat_pic_page.click_send()
        single_chat_page.wait_for_page_load()
        # 长按图片
        single_chat_page.press_last_message(2, '转发')
        select_contacts_page = SelectContactsPage()
        select_contacts_page.click_select_one_group()
        select_contacts_page.selecting_one_group_by_name('群聊1')
        time.sleep(2)
        single_chat_page.click_name_attribute_by_name('取消')

    def tearDown_test_msg_xiaoliping_C_0055(self):
        """恢复环境，将用例开启的消息状态送达开关开启"""

        try:
            # 进入我-设置-消息 将消息送达状态显示开关关闭
            Preconditions.make_already_in_message_page()
            message_page = MessagePage()
            message_page.click_me_button()
            me_page = MePage()
            me_page.wait_for_page_load()
            me_page.click_setting_other()
            time.sleep(2)
            me_set_up_page = MeSetUpPage()
            me_set_up_page.click_message()
            # 点击消息送达状态显示开关 开启状态将其关闭
            if me_set_up_page.get_no_disturbing_btn_text() == "0":
                me_set_up_page.click_no_disturbing_button()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0056(self):
        """单聊会话页面，转发自己发送的图片到企业群"""
        # 等待界面加载
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        single_chat_page.click_back()
        message_page = MessagePage()
        # 进入我-设置-消息 将消息送达状态显示开关关闭
        message_page.click_me_button()
        me_page = MePage()
        me_page.wait_for_page_load()
        me_page.click_setting_other()
        time.sleep(2)
        me_set_up_page = MeSetUpPage()
        me_set_up_page.click_message()
        # 点击消息送达状态显示开关 开启状态将其关闭
        if me_set_up_page.get_no_disturbing_btn_text() == "1":
            me_set_up_page.click_no_disturbing_button()
        # 点击两次返回
        me_set_up_page.click_back()
        me_set_up_page.click_back()
        me_page.wait_for_page_load()
        # 在我界面点击消息回到消息界面
        me_page.click_message_button()
        message_page.wait_for_page_load()
        Preconditions.enter_single_chat_page('大佬1')
        # 选择图片页面 先发送文字 在发送图片第一次发送的消息捕捉不到
        single_chat_page.input_text_message('测试文本')
        single_chat_page.click_send_btn()
        single_chat_page.click_picture()
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_pictures(1)
        # 点击发送
        chat_pic_page.click_send()
        single_chat_page.wait_for_page_load()
        # 长按图片
        single_chat_page.press_last_message(2, '转发')
        select_contacts_page = SelectContactsPage()
        select_contacts_page.click_select_one_group()
        select_contacts_page.selecting_one_group_by_name('测试企业群')
        time.sleep(2)
        single_chat_page.click_name_attribute_by_name('确定')
        single_chat_page.wait_for_page_load()

    def tearDown_test_msg_xiaoliping_C_0056(self):
        """恢复环境，将用例开启的消息状态送达开关开启"""

        try:
            # 进入我-设置-消息 将消息送达状态显示开关关闭
            Preconditions.make_already_in_message_page()
            message_page = MessagePage()
            message_page.click_me_button()
            me_page = MePage()
            me_page.wait_for_page_load()
            me_page.click_setting_other()
            time.sleep(2)
            me_set_up_page = MeSetUpPage()
            me_set_up_page.click_message()
            # 点击消息送达状态显示开关 开启状态将其关闭
            if me_set_up_page.get_no_disturbing_btn_text() == "0":
                me_set_up_page.click_no_disturbing_button()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

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

        # 等待界面加载
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        single_chat_page.click_back()
        message_page = MessagePage()
        # 进入我-设置-消息 将消息送达状态显示开关关闭
        message_page.click_me_button()
        me_page = MePage()
        me_page.wait_for_page_load()
        me_page.click_setting_other()
        time.sleep(2)
        me_set_up_page = MeSetUpPage()
        me_set_up_page.click_message()
        # 点击消息送达状态显示开关 开启状态将其关闭
        if me_set_up_page.get_no_disturbing_btn_text() == "1":
            me_set_up_page.click_no_disturbing_button()
        # 点击两次返回
        me_set_up_page.click_back()
        me_set_up_page.click_back()
        me_page.wait_for_page_load()
        # 在我界面点击消息回到消息界面
        me_page.click_message_button()
        message_page.wait_for_page_load()
        Preconditions.enter_single_chat_page('大佬1')
        # 选择图片页面 先发送文字 在发送图片第一次发送的消息捕捉不到
        single_chat_page.input_text_message('测试文本')
        single_chat_page.click_send_btn()
        single_chat_page.click_picture()
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_pictures(1)
        # 点击发送
        chat_pic_page.click_send()
        single_chat_page.wait_for_page_load()
        # 长按图片
        single_chat_page.press_last_message(2, '转发')
        select_contacts_page = SelectContactsPage()
        select_contacts_page.click_select_one_group()
        select_contacts_page.selecting_one_group_by_name('测试企业群')
        time.sleep(2)
        single_chat_page.click_name_attribute_by_name('取消')

    def tearDown_test_msg_xiaoliping_C_0058(self):
        """恢复环境，将用例开启的消息状态送达开关开启"""

        try:
            # 进入我-设置-消息 将消息送达状态显示开关关闭
            Preconditions.make_already_in_message_page()
            message_page = MessagePage()
            message_page.click_me_button()
            me_page = MePage()
            me_page.wait_for_page_load()
            me_page.click_setting_other()
            time.sleep(2)
            me_set_up_page = MeSetUpPage()
            me_set_up_page.click_message()
            # 点击消息送达状态显示开关 开启状态将其关闭
            if me_set_up_page.get_no_disturbing_btn_text() == "0":
                me_set_up_page.click_no_disturbing_button()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')


class MsgPrivateChatSessionPageTest(TestCase):

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

    @tags('ALL', 'CMCC', 'ZHM')
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

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_C_0006(self):
        """单聊会话页面，编辑图片发送"""
        # 等待界面加载
        message_page = MessagePage()
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        # 点击选择照片
        single_chat_page.click_picture()
        # 选择图片页面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_pictures(1)
        # 点击预览
        chat_pic_page.click_preview()
        # 图片预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        # 点击编辑
        chat_pic_preview_page.click_edit()
        # 图片编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        # 滑动进行涂鸦
        chat_pic_edit_page.do_doodle()
        # 点击马赛克按钮
        chat_pic_edit_page.click_mosaic()
        # 滑动进行马赛克操作
        chat_pic_edit_page.do_mosaic()
        # 点击文本编辑按钮
        chat_pic_edit_page.click_text_edit_btn()
        # 文本编辑
        chat_pic_edit_page.input_pic_text()
        # 点击完成
        chat_pic_edit_page.click_done()
        # 点击发送
        chat_pic_edit_page.click_send()
        # 等待页面加载
        single_chat_page.wait_for_page_load()
        # 点击返回按钮
        single_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_C_0014(self):
        """单聊会话页面，勾选9张相册内图片发送"""
        # 等待界面加载
        message_page = MessagePage()
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        # 点击选择照片
        single_chat_page.click_picture()
        # 选择图片页面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_pictures(9)
        # 点击发送
        chat_pic_page.click_send()
        # 等待页面加载
        single_chat_page.wait_for_page_load()
        # 点击返回按钮
        single_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（发送图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_C_0015(self):
        """单聊会话页面，勾选超9张相册内图片发送"""
        # 等待界面加载
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        # 点击选择照片
        single_chat_page.click_picture()
        # 选择图片页面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_pictures(9)
        # 判断第十个置灰图片的点击按钮是否不可点击
        self.assertEquals(chat_pic_page.grey_picture_btn_is_enabled(), False)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_C_0017(self):
        """单聊会话页面，使用拍照功能并发送照片"""
        # 等待界面加载
        message_page = MessagePage()
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        single_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击拍照
        chat_photo_page.take_photo()
        # 点击发送
        chat_photo_page.send_photo()
        # 等待页面加载
        single_chat_page.wait_for_page_load()
        # 点击返回按钮
        single_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（发送图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_C_0022(self):
        """单聊会话页面，打开拍照，拍照之后返回会话窗口"""
        # 等待界面加载
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        single_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击返回
        chat_photo_page.take_photo_back()
        # 判断当前页面是否在单聊页面
        self.assertEquals(single_chat_page.is_on_this_page(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_C_0165(self):
        """在单聊会话窗，验证点击趣图搜搜入口"""
        # 等待界面加载
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        # 点击表情按钮
        single_chat_page.click_expression_button()
        single_chat_page.wait_for_page_load()
        # 点击gif按钮
        single_chat_page.click_gif_button()
        single_chat_page.wait_for_page_load()
        # 判断当前页面时候有关闭gif按钮
        single_chat_page.is_exist_closegif_page()

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_C_0166(self):
        """在单聊会话窗，网络正常发送表情搜搜"""
        # 等待界面加载
        message_page = MessagePage()
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        # 点击表情按钮
        single_chat_page.click_expression_button()
        single_chat_page.wait_for_page_load()
        # 点击gif按钮
        single_chat_page.click_gif_button()
        single_chat_page.wait_for_page_load()
        # 点击发送GIF图片
        single_chat_page.click_send_gif()
        # 等待页面加载
        single_chat_page.wait_for_page_load()
        # 点击返回按钮
        single_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 判断第一条消息是否为表情
        self.assertEquals(message_page.is_first_message_expression(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0496(self):
        """仅语音模式下——语音录制中途——点击下角的发送按钮"""
        # 等待界面加载
        message_page = MessagePage()
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        # 设置成仅发送语音模式
        single_chat_page.set_send_voice_only()
        # 点击语音按钮
        single_chat_page.click_voice_button()
        # 判断当前界面是否有文本'语音录制中'
        self.assertEquals(single_chat_page.page_should_contain_text2('语音录制中'), True)
        # 点击发送按钮
        single_chat_page.click_send_voice()
        # 等待页面加载
        single_chat_page.wait_for_page_load()
        # 点击返回按钮
        single_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 判断第一条消息是否为表情
        self.assertEquals(message_page.is_first_message_content('[语音]'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_C_0060(self):
        """单聊会话页面，删除自己发送的图片"""
        # 等待界面加载
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        single_chat_page.click_back()
        message_page = MessagePage()
        # 进入我-设置-消息 将消息送达状态显示开关关闭
        message_page.click_me_button()
        me_page = MePage()
        me_page.wait_for_page_load()
        me_page.click_setting_menu()
        time.sleep(2)
        me_set_up_page = MeSetUpPage()
        me_set_up_page.click_message()
        # 点击消息送达状态显示开关 开启状态将其关闭
        if me_set_up_page.get_no_disturbing_btn_text() == "1":
            me_set_up_page.click_no_disturbing_button()
        # 点击两次返回
        me_set_up_page.click_back()
        me_set_up_page.click_back()
        me_page.wait_for_page_load()
        # 在我界面点击消息回到消息界面
        me_page.click_message_button()
        message_page.wait_for_page_load()
        Preconditions.enter_single_chat_page('大佬1')
        # 选择图片页面 先发送文字 在发送图片第一次发送的消息捕捉不到
        single_chat_page.input_text_message('测试文本')
        single_chat_page.click_send_btn()
        single_chat_page.click_picture()
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_pictures(1)
        # 点击发送
        chat_pic_page.click_send()
        single_chat_page.wait_for_page_load()
        # 长按图片
        single_chat_page.press_last_message(2, '删除')
        # 点击确定
        single_chat_page.click_sure()
        # 点击返回
        single_chat_page.click_back()
        message_page.wait_for_page_load()
        # 判断最后一条消息是否为图片
        self.assertEquals(message_page.is_first_message_content('图片'), False)

    def tearDown_test_msg_xiaoliping_C_0060(self):
        """恢复环境，将用例开启的消息状态送达开关开启"""

        try:
            # 进入我-设置-消息 将消息送达状态显示开关关闭
            message_page = MessagePage()
            message_page.click_me_button()
            me_page = MePage()
            me_page.wait_for_page_load()
            me_page.click_setting_menu()
            time.sleep(2)
            me_set_up_page = MeSetUpPage()
            me_set_up_page.click_message()
            # 点击消息送达状态显示开关 开启状态将其关闭
            if me_set_up_page.get_no_disturbing_btn_text() == "0":
                me_set_up_page.click_no_disturbing_button()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_C_0070(self):
        """单聊会话页面，删除自己发送的视频"""
        # 等待界面加载
        message_page = MessagePage()
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        # 选择图片页面 先发送一条文本消息 再发送视频
        single_chat_page.input_text_message('测试文本')
        single_chat_page.click_send_btn()
        chat_pic_page = ChatPicPage()
        single_chat_page.click_picture()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_one_video()
        # 点击发送
        chat_pic_page.click_send()
        time.sleep(15)
        # 长按视频
        single_chat_page.press_video_play(3, '删除')
        # 点击确定
        single_chat_page.click_sure()
        # 点击返回
        single_chat_page.click_back()
        message_page.wait_for_page_load()
        # 判断最后一条消息是否为视频
        self.assertEquals(message_page.is_first_message_content('视频'), False)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_C_0073(self):
        """单聊会话页面，发送相册内的视频"""
        # 等待界面加载
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        # 点击选择照片
        single_chat_page.click_picture()
        # 选择图片页面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一个视频
        chat_pic_page.select_one_video()
        # 判断视频时长文本是否包含'：'
        self.assertEquals(chat_pic_page.get_video_text(), True)
        # 判断发送按钮enabled是否为false
        self.assertEquals(chat_pic_page.send_btn_is_enabled(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_C_0062(self):
        """单聊会话页面，收藏自己发送的照片"""
        # 等待界面加载
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        single_chat_page.click_back()
        message_page = MessagePage()
        # 进入我-设置-消息 将消息送达状态显示开关关闭
        message_page.click_me_button()
        me_page = MePage()
        me_page.wait_for_page_load()
        me_page.click_setting_menu()
        time.sleep(2)
        me_set_up_page = MeSetUpPage()
        me_set_up_page.click_message()
        # 点击消息送达状态显示开关 开启状态将其关闭
        if me_set_up_page.get_no_disturbing_btn_text() == "1":
            me_set_up_page.click_no_disturbing_button()
        # 点击两次返回
        me_set_up_page.click_back()
        me_set_up_page.click_back()
        me_page.wait_for_page_load()
        # 在我界面点击消息回到消息界面
        me_page.click_message_button()
        message_page.wait_for_page_load()
        Preconditions.enter_single_chat_page('大佬1')
        # 选择图片页面 先发送文字 在发送图片第一次发送的消息捕捉不到
        single_chat_page.input_text_message('测试文本')
        single_chat_page.click_send_btn()
        single_chat_page.click_picture()
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_pictures(1)
        # 点击发送
        chat_pic_page.click_send()
        single_chat_page.wait_for_page_load()
        # 长按图片
        single_chat_page.press_last_message(2, '收藏')
        # 判断是否有文本'已收藏'
        self.assertEquals(single_chat_page.page_should_contain_text2('已收藏'), True)
        # 点击返回然后到我-收藏
        single_chat_page.click_back()
        message_page.wait_for_page_load()
        message_page.click_me_button()
        me_page.click_collection()
        # 判断是否有'今天'文本
        self.assertEquals(me_page.page_should_contain_text2('今天'), True)

    def tearDown_test_msg_xiaoliping_C_0062(self):
        """恢复环境，将用例开启的消息状态送达开关开启"""

        try:
            # 进入我-设置-消息 将消息送达状态显示开关关闭
            Preconditions.make_already_in_message_page()
            message_page = MessagePage()
            message_page.click_me_button()
            me_page = MePage()
            me_page.wait_for_page_load()
            me_page.click_setting_menu()
            time.sleep(2)
            me_set_up_page = MeSetUpPage()
            me_set_up_page.click_message()
            # 点击消息送达状态显示开关 开启状态将其关闭
            if me_set_up_page.get_no_disturbing_btn_text() == "0":
                me_set_up_page.click_no_disturbing_button()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_C_0068(self):
        """单聊会话页面，转发自己发送的视频给陌生人"""
        # 等待界面加载
        message_page = MessagePage()
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        # 选择图片页面 先发送一条文本消息 再发送视频
        single_chat_page.input_text_message('测试文本')
        single_chat_page.click_send_btn()
        chat_pic_page = ChatPicPage()
        single_chat_page.click_picture()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_one_video()
        # 点击发送
        chat_pic_page.click_send()
        time.sleep(10)
        # 长按视频
        single_chat_page.press_video_play(2, '转发')
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.selecting_local_contacts_by_name('大佬1')
        select_contacts_page.click_confirm_button()
        # # 判断页面是否有'已转发'文本 抓取不到文本 暂不使用
        # self.assertEquals(single_chat_page.page_should_contain_text2('已转发'), True)
        # 间接验证 判断第一条消息是否为视频
        single_chat_page.click_back()
        message_page.wait_for_page_load()
        self.assertEquals(message_page.is_first_message_content('视频'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_A_0289(self):
        """单聊/群聊会话页面点击名片进入单聊页面"""
        # 等待界面加载
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        # 选择名片
        single_chat_page.click_add_button()
        single_chat_page.click_profile()
        select_contacts_page = SelectContactsPage()
        select_contacts_page.click_name_attribute_by_name('测试号码')
        select_contacts_page.click_send_card()
        # 单聊页面点击名片跳转
        single_chat_page.wait_for_page_load()
        single_chat_page.click_name_attribute_by_name('测试号码')
        contact_details_page = ContactDetailsPage()
        contact_details_page.wait_for_page_load()
        contact_details_page.click_message_icon()
        # 判断是否在测试号码单聊页面
        self.assertEquals(single_chat_page.page_should_contain_text2('测试号码'), True)


class MsgPrivateChatSessionTest(TestCase):

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

        """
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_B_0061(self):
        """进入免费/发送短信查看展示页面"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击免费短信
        message_page.click_free_sms()
        # 判断当前界面是否在联系人选择器界面
        select_contacts_page = SelectContactsPage()
        self.assertEquals(select_contacts_page.page_should_contain_text2('选择联系人'), True)
        self.assertEquals(select_contacts_page.is_exist_search_phone_number(), True)
        self.assertEquals(select_contacts_page.page_should_contain_text2('选择团队联系人'), True)
        self.assertEquals(select_contacts_page.page_should_contain_text2('大佬1'), True)

















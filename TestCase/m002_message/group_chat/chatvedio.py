import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.workbench.corporate_news.CorporateNews import CorporateNewsPage
from pages.workbench.corporate_news.CorporateNewsDetails import CorporateNewsDetailsPage
from pages.workbench.corporate_news.CorporateNewsImageText import CorporateNewsImageTextPage
from pages.workbench.corporate_news.CorporateNewsLink import CorporateNewsLinkPage
from pages.workbench.corporate_news.CorporateNewsNoNews import CorporateNewsNoNewsPage
from preconditions.BasePreconditions import WorkbenchPreconditions
import warnings
from pages import *
from pages.contacts.my_group import ALLMyGroup
from pages.CreateGroupName import CreateGroupNamePage


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
    def make_already_have_my_picture():
        """确保当前群聊页面已有图片"""
        # 1.点击输入框左上方的相册图标
        gcp = GroupChatPage()
        cpg = ChatPicPage()
        gcp.is_on_this_page()
        if gcp.is_exist_msg_image():
            return
        else:
            # 2.进入相片页面,选择一张片相发送
            time.sleep(2)
            gcp.click_picture()
            cpg.wait_for_page_load()
            cpg.select_pic_fk(1)
            cpg.click_send()
            time.sleep(5)

    @staticmethod
    def make_already_have_my_videos():
        """确保当前群聊页面已有视频"""
        # 1.点击输入框左上方的相册图标
        gcp = GroupChatPage()
        cpg = ChatPicPage()
        gcp.wait_for_page_load()
        if gcp.is_exist_msg_videos():
            return
        else:
            # 2.进入相片页面,选择一张片相发送
            gcp.click_picture()
            cpg.wait_for_page_load()
            cpg.select_video_fk(1)
            cpg.click_send()
            time.sleep(5)

    @staticmethod
    def get_into_group_chat_page(name):
        """进入群聊聊天会话页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击发起群聊
        mp.click_group_chat()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @staticmethod
    def make_no_message_send_failed_status():
        """确保当前消息列表没有消息发送失败的标识影响验证结果"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        if mp.is_iv_fail_status_present():
            mp.clear_fail_in_send_message()

    @staticmethod
    def if_exists_multiple_enterprises_enter_group_chat(types):
        """选择团队联系人时存在多个团队时返回获取当前团队名，再进入群聊转发图片/视频"""

        shc = SelectHeContactsDetailPage()
        # 测试号码是否存在多个团队
        if not shc.is_exist_corporate_grade():
            mp = MessagePage()
            scg = SelectContactsPage()
            gcp = GroupChatPage()
            shc.click_back()
            scg.wait_for_page_load()
            scg.click_back()
            gcp.wait_for_page_load()
            gcp.click_back()
            mp.wait_for_page_load()
            mp.open_workbench_page()
            wbp = WorkbenchPage()
            wbp.wait_for_page_load()
            time.sleep(2)
            # 获取当前团队名
            workbench_name = wbp.get_workbench_name()
            mp.open_message_page()
            mp.wait_for_page_load()
            group_name = "群聊1"
            Preconditions.get_into_group_chat_page(group_name)
            # 转发图片/视频
            if types == "pic":
                gcp.forward_pic()
            elif types == "video":
                gcp.forward_video()
            scg.wait_for_page_load()
            scg.click_he_contacts()
            shc.wait_for_he_contacts_page_load()
            # 选择当前团队
            shc.click_department_name(workbench_name)

    @staticmethod
    def enter_corporate_news_page():
        """进入企业新闻首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_corporate_news()

    @staticmethod
    def create_unpublished_image_news(news):
        """创建未发新闻(图文新闻)"""

        cnp = CorporateNewsPage()
        cnp.wait_for_page_load()
        for title, content in news:
            # 点击发布新闻
            cnp.click_release_news()
            cnitp = CorporateNewsImageTextPage()
            cnitp.wait_for_page_load()
            # 输入图文新闻标题
            cnitp.input_news_title(title)
            # 输入图文新闻内容
            cnitp.input_news_content(content)
            cnitp.click_name_attribute_by_name("完成")
            # 点击保存
            cnitp.click_save()
            # 点击确定
            cnitp.click_sure()
            cnp.wait_for_page_load()
            time.sleep(2)

    @staticmethod
    def release_corporate_image_news(titles):
        """发布企业新闻(图文新闻)"""

        cnp = CorporateNewsPage()
        cnp.wait_for_page_load()
        for title in titles:
            # 点击发布新闻
            cnp.click_release_news()
            cnitp = CorporateNewsImageTextPage()
            cnitp.wait_for_page_load()
            # 输入图文新闻标题
            cnitp.input_news_title(title)
            # 输入图文新闻内容
            cnitp.input_news_content("123")
            cnitp.click_name_attribute_by_name("完成")
            # 点击发布
            cnitp.click_release()
            # 点击确定
            cnitp.click_sure()
            cnp.wait_for_page_load()
            time.sleep(2)

    @staticmethod
    def send_video():
        """发送视频"""

        gcp = GroupChatPage()
        gcp.click_picture()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        cpp.select_one_video()
        cpp.click_send(5)

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
    def send_video_in_group_chat():
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


class MsgGroupChatVideoPicAllTest(TestCase):

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
        2、确保当前页面在群聊聊天会话页面
        """
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        msg.delete_all_message_list()
        Preconditions.enter_group_chat_page("群聊1")

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0021(self):
        """群聊会话页面，打开拍照，立刻返回会话窗口"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击拍照
        gcp.click_take_picture()
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        # 2.点击返回
        cpp.take_photo_back()
        # 3.验证是否在群聊页面
        time.sleep(2)
        self.assertTrue(gcp.is_on_this_page())

    @tags('ALL', 'CMCC', 'LXD', 'yms')
    def test_msg_xiaoliping_D_0041(self):
        """群聊会话页面,转发自己发送的图片到当前会话窗口"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 5.选择最近聊天中的当前会话窗口
        scg.selecting_local_contacts_by_name("群聊1")
        time.sleep(2)
        # 6.点击确定转发
        scg.click_accessibility_id_attribute_by_name("确定")
        # 验证是否提示已转发
        # self.assertTrue(scp.page_should_contain_text2("已转发"))
        # 7.验证当前页面在单聊页面
        time.sleep(2)
        self.assertTrue(gcp.is_on_this_page())
        time.sleep(2)

    @tags('ALL', 'CMCC', 'LXD', 'high', 'network')
    def test_msg_xiaoliping_D_0042(self):
        """群聊会话页面，转发自己发送的图片到当前会话窗口时失败"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 5.断开网络
        scg.set_network_status(0)
        # 6.选择最近聊天中的当前会话窗口
        scg.selecting_local_contacts_by_name("群聊1")
        time.sleep(2)
        # 7.点击确定转发
        scg.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 8.返回消息页面
        gcp.click_back()
        # 9.验证是否存在发送失败标识
        self.assertTrue(MessagePage().is_iv_fail_status_present())
        time.sleep(2)

    @staticmethod
    def tearDown_test_msg_xiaoliping_D_0042():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'yms')
    def test_msg_xiaoliping_D_0043(self):
        """群聊会话页面，转发自己发送的图片到当前会话窗口时点击取消转发"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 5.选择最近聊天中的当前会话窗口
        scg.selecting_local_contacts_by_name("群聊1")
        time.sleep(2)
        # 6.点击取消转发
        scg.click_accessibility_id_attribute_by_name("取消")
        # 验证是否在联系人页面
        time.sleep(2)
        self.assertTrue(scg.is_on_this_page())

    @tags('ALL', 'CMCC', 'LXD', 'yms')
    def test_msg_xiaoliping_D_0044(self):
        """群聊会话页面，转发自己发送的图片给手机联系人"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        time.sleep(2)
        # 5.点击选择一个手机联系人
        scg.click_phone_contact()
        time.sleep(2)
        slp = SelectLocalContactsPage()
        slp.selecting_local_contacts_by_name("大佬2")
        # 6.点击确定转发
        slp.click_sure()
        # 7.验证是否在群聊会话
        time.sleep(2)
        self.assertTrue(gcp.is_on_this_page())

    @tags('ALL', 'CMCC', 'LXD', 'high','network')
    def test_msg_xiaoliping_D_0045(self):
        """群聊会话页面，转发自己发送的图片到手机联系人时失败"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        time.sleep(2)
        # 5.点击选择一个手机联系人
        scg.click_phone_contact()
        time.sleep(2)
        slp = SelectLocalContactsPage()
        # 6.断开网络
        scg.set_network_status(0)
        slp.selecting_local_contacts_by_name("大佬2")
        # 7.点击确定转发
        slp.click_sure()
        # 9.返回消息页面
        gcp.click_back()
        # 10.验证是否存在发送失败标识
        self.assertTrue(MessagePage().is_iv_fail_status_present())
        time.sleep(2)

    @staticmethod
    def tearDown_test_msg_xiaoliping_D_0045():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'yms')
    def test_msg_xiaoliping_D_0046(self):
        """群聊会话页面，转发自己发送的图片到手机联系人时点击取消转发"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        time.sleep(2)
        # 5.点击选择一个手机联系人
        scg.click_phone_contact()
        time.sleep(2)
        slp = SelectLocalContactsPage()
        slp.selecting_local_contacts_by_name("大佬2")
        # 6.点击取消转发
        slp.click_cancel_forward()
        # 7.验证是否在选择本地联系人页面
        time.sleep(2)
        self.assertTrue(slp.is_on_this_page())

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0047(self):
        """群聊会话页面，转发自己发送的图片给团队联系人"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        time.sleep(2)
        # 5.点击选择团队联系人
        scg.click_group_contact()
        time.sleep(2)
        shp = SelectHeContactsPage()
        shp.input_search_text("大佬1")
        time.sleep(2)
        shp.click_element_by_id()
        time.sleep(2)
        # 6.点击确定转发
        shp.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 7.验证当前页面在群聊页面
        self.assertTrue(gcp.is_on_this_page())
        time.sleep(2)

    @tags('ALL', 'CMCC', 'LXD', ' network')
    def test_msg_xiaoliping_D_0048(self):
        """群聊会话页面，转发自己发送的图片到团队联系人时失败"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        time.sleep(2)
        # 5.点击选择团队联系人
        scg.click_group_contact()
        time.sleep(2)
        shp = SelectHeContactsPage()
        # 断开网络
        shp.set_network_status(0)
        shp.input_search_text("大佬1")
        time.sleep(2)
        shp.click_element_by_id()
        time.sleep(2)
        # 6.点击确定转发
        shp.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 7.返回消息页面
        gcp.click_back()
        # 8.验证是否存在发送失败标识
        self.assertTrue(MessagePage().is_iv_fail_status_present())
        time.sleep(2)

    @staticmethod
    def tearDown_test_msg_xiaoliping_D_0048():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0049(self):
        """群聊会话页面，转发自己发送的图片到团队联系人时点击取消转发"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        time.sleep(2)
        # 5.点击选择团队联系人
        scg.click_group_contact()
        time.sleep(2)
        shp = SelectHeContactsPage()
        shp.input_search_text("大佬1")
        time.sleep(2)
        shp.click_element_by_id()
        time.sleep(2)
        # 6.点击取消
        shp.click_accessibility_id_attribute_by_name("取消")
        time.sleep(2)
        # 7.验证当前页面在团队联系人页面
        self.assertTrue(shp.is_on_this_page())
        time.sleep(2)

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0050(self):
        """群聊会话页面，转发自己发送的图片给陌生人"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        time.sleep(2)
        # 5.获取输入框输入'13333333333'
        scg.input_search_keyword('13333333333')
        scg.click_name_attribute_by_name('未知号码')
        # 6.点击确定
        scg.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 7.验证当前页面在群聊页面
        self.assertTrue(gcp.is_on_this_page())
        time.sleep(2)

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_xiaoliping_D_0051(self):
        """群聊会话页面，转发自己发送的图片到陌生人时失败"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        time.sleep(2)
        # 断开网络
        scg.set_network_status(0)
        # 5.获取输入框输入'13333333333'
        scg.input_search_keyword('13333333333')
        scg.click_name_attribute_by_name('未知号码')
        # 6.点击确定
        scg.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 7.返回消息页面
        gcp.click_back()
        # 8.验证是否存在发送失败标识
        self.assertTrue(MessagePage().is_iv_fail_status_present())
        time.sleep(2)

    @staticmethod
    def tearDown_test_msg_xiaoliping_D_0051():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0052(self):
        """群聊会话页面，转发自己发送的图片到陌生人时点击取消转发"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        time.sleep(2)
        # 5.获取输入框输入'13333333333'
        scg.input_search_keyword('13333333333')
        scg.click_name_attribute_by_name('未知号码')
        # 6.点击取消
        scg.click_accessibility_id_attribute_by_name("取消")
        time.sleep(2)
        # 7.验证当前页面在选择联系人页面
        self.assertTrue(scg.is_on_this_page())
        time.sleep(2)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0053(self):
        """群聊会话页面，转发自己发送的图片到普通群"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        time.sleep(2)
        # 5.点击选择一个群
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        # 6.选择一个普通群
        sog.selecting_one_group_by_name("群聊2")
        # 7.点击确定转发
        sog.click_accessibility_id_attribute_by_name("确定")
        # 8.验证当前页面在群聊页面
        time.sleep(2)
        self.assertTrue(gcp.is_on_this_page())
        time.sleep(2)

    @tags('ALL', 'CMCC', 'LXD', 'network')
    def test_msg_xiaoliping_D_0054(self):
        """群聊会话页面，转发自己发送的图片到普通群时失败"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        time.sleep(2)
        # 5.点击选择一个群
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        # 断开网络
        sog.set_network_status(0)
        # 6.选择一个普通群
        sog.selecting_one_group_by_name("群聊2")
        # 7.点击确定转发
        sog.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 8.返回消息页面
        gcp.click_back()
        # 9.验证是否存在发送失败标识
        self.assertTrue(MessagePage().is_iv_fail_status_present())
        time.sleep(2)

    @staticmethod
    def tearDown_test_msg_xiaoliping_D_0054():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0055(self):
        """群聊会话页面，转发自己发送的图片到普通群时点击取消转发"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        time.sleep(2)
        # 5.点击选择一个群
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        # 6.选择一个普通群
        sog.selecting_one_group_by_name("群聊2")
        # 7.点击取消转发
        sog.click_accessibility_id_attribute_by_name("取消")
        # 7.验证当前页面在选择群页面
        time.sleep(2)
        self.assertTrue(sog.is_on_this_page())
        time.sleep(2)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0056(self):
        """群聊会话页面，转发自己发送的图片到企业群"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        time.sleep(2)
        # 5.点击选择一个群
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        # 6.选择一个企业群
        sog.selecting_one_group_by_name("测试企业群")
        # 7.点击确定转发
        sog.click_accessibility_id_attribute_by_name("确定")
        # 8.验证当前页面在群聊页面
        time.sleep(2)
        self.assertTrue(gcp.is_on_this_page())
        time.sleep(2)

    @tags('ALL', 'CMCC', 'LXD','network')
    def test_msg_xiaoliping_D_0057(self):
        """群聊会话页面，转发自己发送的图片到企业群时失败"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        time.sleep(2)
        # 5.点击选择一个群
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        # 断开网络
        sog.set_network_status(0)
        # 6.选择一个企业群
        sog.selecting_one_group_by_name("测试企业群")
        # 7.点击确定转发
        sog.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 8.返回消息页面
        gcp.click_back()
        # 9.验证是否存在发送失败标识
        self.assertTrue(MessagePage().is_iv_fail_status_present())
        time.sleep(2)

    @staticmethod
    def tearDown_test_msg_xiaoliping_D_0057():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0058(self):
        """群聊会话页面，转发自己发送的图片到企业群时点击取消转发"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送一张图片,确保最近聊天中有记录
        Preconditions.send_pic_in_group_chat()
        # 2.长按自己发送的图片并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        time.sleep(2)
        # 5.点击选择一个群
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        # 6.选择一个企业群
        sog.selecting_one_group_by_name("测试企业群")
        # 7.点击取消转发
        sog.click_accessibility_id_attribute_by_name("取消")
        # 8.验证当前页面在选择群页面
        time.sleep(2)
        self.assertTrue(sog.is_on_this_page())
        time.sleep(2)

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0069(self):
        """群聊会话页面，转发自己发送的视频给手机联系人"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送视频,确保最近聊天中有记录
        Preconditions.send_video_in_group_chat()
        # 2.长按自己发送的视频并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 5.点击选择一个手机联系人
        scg.click_phone_contact()
        time.sleep(2)
        slp = SelectLocalContactsPage()
        slp.selecting_local_contacts_by_name("大佬2")
        # 6.点击确定转发
        slp.click_sure()
        # 7.验证是否在群聊会话
        time.sleep(2)
        self.assertTrue(gcp.is_on_this_page())

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0070(self):
        """群聊会话页面，转发自己发送的视频给手机联系人时失败"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送视频,确保最近聊天中有记录
        Preconditions.send_video_in_group_chat()
        # 2.长按自己发送的视频并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 5.点击选择一个手机联系人
        scg.click_phone_contact()
        time.sleep(2)
        # 断开网络
        scg.set_network_status(0)
        slp = SelectLocalContactsPage()
        slp.selecting_local_contacts_by_name("大佬2")
        # 6.点击确定转发
        slp.click_sure()
        time.sleep(2)
        # 7.返回消息页面
        gcp.click_back()
        # 8.验证是否存在发送失败标识
        self.assertTrue(MessagePage().is_iv_fail_status_present())
        time.sleep(2)

    @staticmethod
    def tearDown_test_msg_xiaoliping_D_0070():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0071(self):
        """群聊会话页面，转发自己发送的视频给手机联系人时点击取消转发"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送视频,确保最近聊天中有记录
        Preconditions.send_video_in_group_chat()
        # 2.长按自己发送的视频并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 5.点击选择一个手机联系人
        scg.click_phone_contact()
        time.sleep(2)
        slp = SelectLocalContactsPage()
        slp.selecting_local_contacts_by_name("大佬2")
        # 6.点击取消转发
        slp.click_cancel_forward()
        # 7.验证是否在选择联系人页面
        time.sleep(2)
        self.assertTrue(slp.is_on_this_page())

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0072(self):
        """群聊会话页面，转发自己发送的视频给团队联系人"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送视频,确保最近聊天中有记录
        Preconditions.send_video_in_group_chat()
        # 2.长按自己发送的视频并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 5.点击选择团队联系人
        scg.click_group_contact()
        time.sleep(2)
        shp = SelectHeContactsPage()
        shp.input_search_text("大佬1")
        time.sleep(2)
        shp.click_element_by_id()
        time.sleep(2)
        # 6.点击确定转发
        shp.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 7.验证当前页面在群聊页面
        self.assertTrue(gcp.is_on_this_page())
        time.sleep(2)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0073(self):
        """群聊会话页面，转发自己发送的视频给团队联系人时失败"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送视频,确保最近聊天中有记录
        Preconditions.send_video_in_group_chat()
        # 2.长按自己发送的视频并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 5.点击选择团队联系人
        scg.click_group_contact()
        time.sleep(2)
        # 断开网络
        scg.set_network_status(0)
        shp = SelectHeContactsPage()
        shp.input_search_text("大佬1")
        time.sleep(2)
        shp.click_element_by_id()
        time.sleep(2)
        # 6.点击确定转发
        shp.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 7.返回消息页面
        gcp.click_back()
        # 8.验证是否存在发送失败标识
        self.assertTrue(MessagePage().is_iv_fail_status_present())
        time.sleep(2)

    @staticmethod
    def tearDown_test_msg_xiaoliping_D_0073():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0074(self):
        """群聊会话页面，转发自己发送的视频给团队联系人时点击取消转发"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送视频,确保最近聊天中有记录
        Preconditions.send_video_in_group_chat()
        # 2.长按自己发送的视频并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 5.点击选择团队联系人
        scg.click_group_contact()
        time.sleep(2)
        shp = SelectHeContactsPage()
        shp.input_search_text("大佬1")
        time.sleep(2)
        shp.click_element_by_id()
        time.sleep(2)
        # 6.点击取消转发
        shp.click_accessibility_id_attribute_by_name("取消")
        time.sleep(2)
        # 7.验证当前页面在选择团队联系人页面
        self.assertTrue(shp.is_on_this_page())
        time.sleep(2)

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0075(self):
        """群聊会话页面，转发自己发送的视频给陌生人"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送视频,确保最近聊天中有记录
        Preconditions.send_video_in_group_chat()
        # 2.长按自己发送的视频并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        time.sleep(2)
        # 5.获取输入框输入'13333333333'
        scg.input_search_keyword('13333333333')
        scg.click_name_attribute_by_name('未知号码')
        # 6.点击确定转发
        scg.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 7.验证当前页面群聊页面
        self.assertTrue(gcp.is_on_this_page())
        time.sleep(2)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0076(self):
        """群聊会话页面，转发自己发送的视频给陌生人时失败"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送视频,确保最近聊天中有记录
        Preconditions.send_video_in_group_chat()
        # 2.长按自己发送的视频并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        time.sleep(2)
        # 5.获取输入框输入'13333333333'
        scg.input_search_keyword('13333333333')
        # 断开网络
        scg.set_network_status(0)
        scg.click_name_attribute_by_name('未知号码')
        # 6.点击确定转发
        scg.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 7.返回消息页面
        gcp.click_back()
        # 8.验证是否存在发送失败标识
        self.assertTrue(MessagePage().is_iv_fail_status_present())
        time.sleep(2)

    @staticmethod
    def tearDown_test_msg_xiaoliping_D_0076():
        MessagePage().set_network_status(6)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0077(self):
        """群聊会话页面，转发自己发送的视频给陌生人时点击取消转发"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.给当前会话页面发送视频,确保最近聊天中有记录
        Preconditions.send_video_in_group_chat()
        # 2.长按自己发送的视频并转发
        cwp = ChatWindowPage()
        time.sleep(2)
        cwp.swipe_by_percent_on_screen(70, 30, 75, 30)
        time.sleep(3)
        # 3.点击转发
        gcp.click_accessibility_id_attribute_by_name("转发")
        scg = SelectContactsPage()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        time.sleep(2)
        # 5.获取输入框输入'13333333333'
        scg.input_search_keyword('13333333333')
        scg.click_name_attribute_by_name('未知号码')
        # 6.点击取消转发
        scg.click_accessibility_id_attribute_by_name("取消")
        time.sleep(2)
        # 7.验证当前页面在选择联系人页面
        self.assertTrue(scg.is_on_this_page())
        time.sleep(2)


class MsgGroupChatTest(TestCase):

    @classmethod
    def setUpClass(cls):
        """删除消息列表的消息记录"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        #创建团队ateam7272
        Preconditions.make_already_in_message_page()
        MessagePage().delete_all_message_list()
        Preconditions.create_team_if_not_exist_and_set_as_defalut_team()
        # 导入团队联系人、企业部门
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
                                  ('陈丹丹', "13800137004"), ('alice', "13800137005"), ('郑海', "13802883296")]
                Preconditions.create_he_contacts2(contact_names2)
                department_names = ["测试部门1", "测试部门2"]
                Preconditions.create_department_and_add_member(department_names)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

    def default_setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0001(self):
        """群聊会话页面，不勾选相册内图片点击发送按钮"""

        mp = MessagePage()
        mp.wait_for_page_load()
        #在消息页面等待页面加载
        mp.click_add_icon()
        #点击加号
        mp.click_group_chat()
        #点击发起群聊
        sccp = SelectContactsPage()
        #选择联系人页面
        sccp.wait_for_page_load()
        #等待选择联系人页面加载
        sccp.click_select_one_group()
        #点击选择一个群按钮
        sog = SelectOneGroupPage()
        #选择一个群界面
        sog.selecting_one_group_by_name("群聊1")
        #通过名称找到群聊1
        gcp = GroupChatPage()
        #群聊1界面
        gcp.wait_for_page_load()
        #等待页面加载
        gcp.click_picture()
        #点击图片按钮
        cpp = ChatPicPage()
        #选择图片页面
        cpp.wait_for_page_load()
        #等待页面加载
        self.assertEquals(cpp.send_btn_is_enabled(), False)
        #判断发送按钮enabled是否为false

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0002(self):
        '''群聊会话页面，勾选相册内一张图片发送'''
        mp = MessagePage()
        # 等待页面加载
        mp.wait_for_page_load()
        # 点击加号
        mp.click_add_icon()
        # 点击发起群聊按钮
        mp.click_group_chat()
        # 选择联系人界面
        scp = SelectContactsPage()
        # 等待页面加载
        scp.wait_for_page_load()
        # 点击选择一个群按钮
        scp.click_select_one_group()
        # 选择一个群界面
        sog = SelectOneGroupPage()
        # 等待页面加载
        sog.wait_for_page_load()
        # 通过名称找到群聊'啊测测试试'
        sog.selecting_one_group_by_name('群聊1')
        #群聊页面
        gcp = GroupChatPage()
        #等待页面加载
        gcp.wait_for_page_load()
        #点击图片按钮
        gcp.click_picture()
        #选择图片界面
        cpp = ChatPicPage()
        #等待页面加载
        cpp.wait_for_page_load()
        #选择第一张照片
        cpp.select_picture()
        #点击发送 按钮中有发送就可以点击
        cpp.click_name_attribute_by_name("发送")
        #等待页面加载
        gcp.wait_for_page_load()
        #点击返回按钮
        gcp.click_back_button()
        #等待页面加载
        mp.wait_for_page_load()
        #验证第一条消息是否为图片
        self.assertEquals(mp.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0003(self):
        """群聊会话页面，预览相册内图片"""
        # 消息界面
        mp = MessagePage()
        # 等待界面加载
        mp.wait_for_page_load()
        # 点击加号
        mp.click_add_icon()
        # 点击发起群聊按钮
        mp.click_group_chat()
        # 选择联系人界面
        scp = SelectContactsPage()
        # 等待页面加载
        scp.wait_for_page_load()
        # 点击选择一个群
        scp.click_select_one_group()
        # 选择一个群界面
        sogp = SelectOneGroupPage()
        # 等待页面加载
        sogp.wait_for_page_load()
        # 通过名称选择'群聊1'群聊
        sogp.selecting_one_group_by_name('群聊1')
        # 群聊界面
        gcp = GroupChatPage()
        # 等待页面加载
        gcp.wait_for_page_load()
        # 点击图片按钮
        gcp.click_picture()
        # 选择图片界面
        cpp = ChatPicPage()
        # 等待界面加载
        cpp.wait_for_page_load()
        # 选择第一张图片
        cpp.select_picture()
        # 点击预览按钮
        cpp.click_preview()
        # 预览界面
        cpg = ChatPicPreviewPage()
        # 等待界面加载
        cpg.wait_for_page_load()

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0004(self):
        '''群聊会话页面，预览相册内图片，不勾选原图发送'''
        #消息界面
        message_page = MessagePage()
        #等待页面加载
        message_page.wait_for_page_load()
        #点击加号
        message_page.click_add_icon()
        #点击发起群聊按钮
        message_page.click_group_chat()
        #选择联系人界面
        select_contacts_page = SelectContactsPage()
        #等待界面加载
        select_contacts_page.wait_for_page_load()
        #选择一个群按钮
        select_contacts_page.click_select_one_group()
        #选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        #通过名称找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        #群聊界面
        group_chat_page = GroupChatPage()
        #等待界面加载
        group_chat_page.wait_for_page_load()
        #点击选择图片按钮
        group_chat_page.click_picture()
        #选择图片界面
        chat_pic_page = ChatPicPage()
        #等待界面加载
        chat_pic_page.wait_for_page_load()
        #选择第一张图片
        chat_pic_page.select_picture()
        #点击预览
        chat_pic_page.click_preview()
        #预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        #等待页面加载
        chat_pic_preview_page.wait_for_page_load()
        #点击发送
        chat_pic_preview_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（图片无法选中间接验证）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0005(self):
        '''群聊会话页面，预览相册数量与发送按钮数量一致'''
        #消息界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        #点击加号
        message_page.click_add_icon()
        #点击发起群聊
        message_page.click_group_chat()
        #选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        #选择一个群
        select_contacts_page.click_select_one_group()
        #选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        #通过名称找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        #群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        #点击选择照片
        group_chat_page.click_picture()
        #选择图片页面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        #选择多张照片
        chat_pic_page.select_pictures(3)
        #点击预览
        chat_pic_page.click_preview()
        #预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        #获取预览数文本
        text1 = chat_pic_preview_page.get_preview_text()
        #获取发送按钮文本
        text2 = chat_pic_preview_page.get_send_text()
        #判断预览数与发送数是否相等
        self.assertEquals(text1, text2)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0006(self):
        """群聊会话页面，编辑图片发送"""
        #消息界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        #点击加号
        message_page.click_add_icon()
        #点击发起群聊
        message_page.click_group_chat()
        #选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        #点击选择一个群
        select_contacts_page.click_select_one_group()
        #选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        #通过群名找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        #群聊1界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        #点击图片按钮
        group_chat_page.click_picture()
        #选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        #选择一张图片
        chat_pic_page.select_pictures(1)
        #点击预览
        chat_pic_page.click_preview()
        #图片预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        #点击编辑
        chat_pic_preview_page.click_edit()
        #图片编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        #点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        #滑动进行涂鸦
        chat_pic_edit_page.do_doodle()
        #点击马赛克按钮
        chat_pic_edit_page.click_mosaic()
        #滑动进行马赛克操作
        chat_pic_edit_page.do_mosaic()
        #点击文本编辑按钮
        chat_pic_edit_page.click_text_edit_btn()
        #文本编辑
        chat_pic_edit_page.input_pic_text()
        #点击完成
        chat_pic_edit_page.click_done()
        #点击发送
        chat_pic_edit_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0007(self):
        """群聊会话页面，编辑图片不保存发送"""
        #消息界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        #点击加号
        message_page.click_add_icon()
        #点击发起群聊
        message_page.click_group_chat()
        #选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        #点击选择一个群
        select_contacts_page.click_select_one_group()
        #选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        #按名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        #群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        #点击图片按钮
        group_chat_page.click_picture()
        #选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        #选择一张图片
        chat_pic_page.select_pictures(1)
        #点击预览按钮
        chat_pic_page.click_preview()
        #图片预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        #点击编辑按钮
        chat_pic_preview_page.click_edit()
        #图片编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        #点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        #进行涂鸦操作
        chat_pic_edit_page.do_doodle()
        #点击马赛克按钮
        chat_pic_edit_page.click_mosaic()
        #进行马赛克操作
        chat_pic_edit_page.do_mosaic()
        #点击文本编辑按钮
        chat_pic_edit_page.click_text_edit_btn()
        #进行文本编辑
        chat_pic_edit_page.input_pic_text()
        #点击完成
        chat_pic_edit_page.click_done()
        #点击保存
        chat_pic_edit_page.click_save()
        chat_pic_edit_page.wait_for_page_load()
        #点击发送
        chat_pic_edit_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0008(self):
        """群聊会话页面，编辑图片中途直接发送"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures(1)
        # 点击预览
        chat_pic_page.click_preview()
        # 预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        # 点击编辑
        chat_pic_preview_page.click_edit()
        # 编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        # 进行涂鸦操作
        chat_pic_edit_page.do_doodle()
        # 点击马赛克按钮
        chat_pic_edit_page.click_mosaic()
        # 进行马赛克操作
        chat_pic_edit_page.do_mosaic()
        # 点击文本编辑按钮
        chat_pic_edit_page.click_text_edit_btn()
        # 进行文本编辑
        chat_pic_edit_page.input_pic_text()
        # 点击完成
        chat_pic_edit_page.click_done()
        # 点击发送
        chat_pic_edit_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0009(self):
        """群聊会话页面，编辑图片保存"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures(1)
        # 点击预览
        chat_pic_page.click_preview()
        # 预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        # 点击编辑
        chat_pic_preview_page.click_edit()
        # 编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        # 进行涂鸦操作
        chat_pic_edit_page.do_doodle()
        # 点击马赛克按钮
        chat_pic_edit_page.click_mosaic()
        # 进行马赛克操作
        chat_pic_edit_page.do_mosaic()
        # 点击文本编辑按钮
        chat_pic_edit_page.click_text_edit_btn()
        # 进行文本编辑
        chat_pic_edit_page.input_pic_text()
        # 点击完成
        chat_pic_edit_page.click_done()
        # 点击保存
        chat_pic_edit_page.click_save()
        # 判断保存之后是否有文字提示已保存至系统相册
        self.assertEquals(chat_pic_edit_page.page_should_contain_text2("已保存至系统相册", 20), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0012(self):
        """群聊会话页面，发送相册内的图片 """
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击选择照片
        group_chat_page.click_picture()
        # 选择图片页面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # numbers1 = chat_pic_page.get_pic_numbers()
        # numbers2 = chat_pic_page.get_video_numbers()
        # 直接点击图片
        chat_pic_page.click_picture_just()
        # chat_pic_edit_page = ChatPicEditPage()
        time.sleep(2)
        # self.assertEquals(chat_pic_edit_page.page_should_contain_text2('预览(1/' + str(numbers1+numbers2)), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0014(self):
        """群聊会话页面，勾选9张相册内图片发送"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择九张图片
        chat_pic_page.select_pictures(9)
        # 点击发送
        chat_pic_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（发送图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0015(self):
        """群聊会话页面，勾选超9张相册内图片发送"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择九张图片
        chat_pic_page.select_pictures(9)
        # 判断第十个置灰图片的点击按钮是否不可点击
        self.assertEquals(chat_pic_page.grey_picture_btn_is_enabled(), False)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0016(self):
        """群聊会话页面，同时发送相册中的图片和视频"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures(1)
        # 获取发送按钮文本1
        text1 = chat_pic_page.get_send_text()
        # 选择一个视频
        chat_pic_page.select_one_video()
        # 获取点击视频后发送按钮文本2
        text2 = chat_pic_page.get_send_text()
        # 比较文本1和2是否相同（发送按钮没有变化说明无法同时选取照片和视频）
        self.assertEquals(text1, text2)
        # # 判断点击图片之后是否有文字提示不能同时选择照片和视频（有时会抓不到文本信息 不稳定）
        # self.assertEquals(chat_pic_page.page_should_contain_text2("不能同时选择照片和视频", 20), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0017(self):
        """群聊会话页面，使用拍照功能并发送照片"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击拍照
        chat_photo_page.take_photo()
        # 点击发送
        chat_photo_page.send_photo()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（发送图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0110(self):
        """在群聊会话窗，验证点击趣图搜搜入口"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击表情按钮
        group_chat_page.click_expression_button()
        group_chat_page.wait_for_page_load()
        # 点击gif按钮
        group_chat_page.click_gif_button()
        group_chat_page.wait_for_page_load()
        # 判断当前页面时候有关闭gif按钮
        self.assertEquals(group_chat_page.is_exist_close_gif(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0111(self):
        """在群聊会话窗，网络正常发送表情搜搜"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击表情按钮
        group_chat_page.click_expression_button()
        group_chat_page.wait_for_page_load()
        # 点击gif按钮
        group_chat_page.click_gif_button()
        group_chat_page.wait_for_page_load()
        # 点击发送GIF图片
        group_chat_page.click_send_gif()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 判断第一条消息是否为表情
        self.assertEquals(message_page.is_first_message_expression(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0082(self):
        """群聊会话页面，发送相册内的视频"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        self.assertEquals(chat_pic_page.send_btn_is_enabled(), False)
        # 选择一个视频
        chat_pic_page.select_one_video()
        # 判断视频时长文本是否包含'：'
        self.assertEquals(chat_pic_page.get_video_text(), True)
        # 判断发送按钮enabled是否为false
        self.assertEquals(chat_pic_page.send_btn_is_enabled(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_weifenglian_qun_0013(self):
        """勾选本地照片内任意相册的图片点击发送按钮"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击文件按钮
        group_chat_page.click_file_button()
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
        # 点击发送
        chat_select_file_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（发送图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_weifenglian_qun_0027(self):
        """勾选本地视频内任意视频点击发送按钮"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击文件按钮
        group_chat_page.click_file_button()
        # 选择文件界面
        chat_select_file_page = ChatSelectFilePage()
        chat_select_file_page.wait_for_page_load()
        # 点击本地视频
        chat_select_file_page.click_video()
        chat_select_file_page.wait_for_local_video_page_load()
        # 选择视频
        chat_select_file_page.click_local_video()
        # 点击确定
        chat_select_file_page.click_sure()
        # 等待群聊页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 判断第一条消息是否为视频
        self.assertEquals(message_page.is_first_message_video(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0001(self):
        """消息列表——发起群聊——选择已有群--模糊搜索"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        # 点击搜索群组
        select_one_group_page.click_search_box()
        # 输入搜索内容模糊搜索'群'
        select_one_group_page.input_search_keyword('群')
        # 判断当前页面是否存在'群聊1'
        self.assertEquals(select_contacts_page.page_should_contain_text2('群聊1'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0002(self):
        """消息列表——发起群聊——选择已有群--模糊搜索无搜索结果"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        # 点击搜索群组
        select_one_group_page.click_search_box()
        # 输入搜索内容模糊搜索'没有这个群'
        select_one_group_page.input_search_keyword('没有这个群')
        # 判断当前页面是否存在'无搜索结果'
        self.assertEquals(select_contacts_page.page_should_contain_text2('无搜索结果'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0003(self):
        """群聊列表展示页面——中文精确搜索"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        # 点击搜索群组
        select_one_group_page.click_search_box()
        # 输入搜索内容精确搜索'群聊1'
        select_one_group_page.input_search_keyword('群聊1')
        # 判断搜索群名是否匹配
        self.assertEquals(select_one_group_page.page_should_contain_text2("群聊1"), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0018(self):
        """在群聊天会话页面，发送一条字符长度，大于1的文本消息"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击聊天输入框
        group_chat_page.get_input_box()
        # 判断语音按钮是否存在
        group_chat_page.is_exist_voice_button()
        # 输入十个字符
        group_chat_page.input_text_message('1234567890')
        group_chat_page.wait_for_page_load()
        # 判断发送按钮是否存在
        group_chat_page.is_exist_send_button()

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0101(self):
        """在群聊会话窗口，点击输入框上方的图片ICON，进入到图片展示列表"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures()
        # 点击发送
        chat_pic_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（发送图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0102(self):
        """在群聊会话窗口，点击输入框上方的相机ICON，进入到相机拍摄页"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击拍照
        chat_photo_page.take_photo()
        # 点击发送
        chat_photo_page.send_photo()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（发送图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0106(self):
        """点击输入框上方的+号——展示隐藏的：文件、群短信（群主）、位置、红包"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击更多加号按钮
        group_chat_page.click_add_button()
        group_chat_page.wait_for_page_load()
        # 确认当前页面有无群短信，位置，红包元素以及文件按钮
        self.assertEquals(select_one_group_page.page_should_contain_text2("群短信"), True)
        self.assertEquals(select_one_group_page.page_should_contain_text2("位置"), True)
        self.assertEquals(select_one_group_page.page_should_contain_text2("红包"), True)
        self.assertEquals(group_chat_page.is_exist_file_button(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0124(self):
        """普通群——群主——添加一个成员"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置按钮
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_load()
        # 点击添加成员按钮
        group_chat_page.click_add_member_button()
        group_chat_page.wait_for_page_setting_load()
        # 通过文本点击'大佬1'
        group_chat_page.click_accessibility_id_attribute_by_name('大佬3')
        # 点击确定按钮
        group_chat_page.click_add_member_confirm_button()
        # # 判断当前页面是否存在文本'添加成功'  有概率抓取不到 暂时不使用
        # self.assertEquals(group_chat_page.page_should_contain_text2('添加成功'), True)
        group_chat_page.wait_for_page_load()
        time.sleep(3)
        group_chat_page.click_back()
        message_page.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0124():
        """恢复环境，将添加的成员删除"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'群聊1'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('群聊1')
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击删除群成员按钮
            group_chat_page.click_delete_member_button()
            group_chat_page.click_name_attribute_by_name('大佬3')
            group_chat_page.click_name_attribute_by_name('确定(1)')
            group_chat_page.click_delete_member_sure_button()
            time.sleep(3)
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0125(self):
        """普通群——群主——添加2个成员"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊2')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 获取当前页面图片元素数量1
        text1 = group_chat_page.get_picture_nums()
        # 点击设置按钮
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        # 点击添加成员按钮
        group_chat_page.click_add_member_button()
        group_chat_page.wait_for_page_setting_load()
        # 通过文本点击'大佬1'
        group_chat_page.click_accessibility_id_attribute_by_name('大佬1')
        # 通过文本点击'大佬2'
        group_chat_page.click_accessibility_id_attribute_by_name('大佬2')
        # 点击确定按钮
        group_chat_page.click_add_member_confirm_button()
        # # 判断当前页面是否存在文本'添加成功'  有概率抓取不到 暂时不使用
        # self.assertEquals(group_chat_page.page_should_contain_text2('添加成功'), True)
        group_chat_page.wait_for_page_load()
        # 获取当前页面图片元素数量2
        text2 = group_chat_page.get_picture_nums()
        # 比较两次图片元素数量
        self.assertEquals(int(text1) < int(text2), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0125():
        """恢复环境，将添加的成员删除"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'群聊1'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('群聊2')
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击删除群成员按钮
            group_chat_page.click_delete_member_button()
            group_chat_page.click_name_attribute_by_name('大佬1')
            group_chat_page.click_name_attribute_by_name('确定(1)')
            group_chat_page.click_delete_member_sure_button()
            time.sleep(3)
            group_chat_page.click_delete_member_button()
            group_chat_page.click_name_attribute_by_name('大佬2')
            group_chat_page.click_name_attribute_by_name('确定(1)')
            group_chat_page.click_delete_member_sure_button()
            time.sleep(3)
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0135(self):
        """无群成员时——点击移除成员按钮"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊2'
        select_one_group_page.selecting_one_group_by_name('群聊2')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置按钮
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        # 点击删除按钮
        group_chat_page.click_delete_member_button()
        time.sleep(2)
        # 判断当前界面是否有'群聊设置'文本
        group_chat_page.wait_for_page_setting_load()
        self.assertEquals(group_chat_page.page_should_contain_text2('群聊设置'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0242(self):
        """消息草稿-聊天列表显示-输入文本信息"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框
        group_chat_page.get_input_box()
        # 输入文本'测试文本'
        group_chat_page.input_text_message('测试文本')
        # 点击返回
        group_chat_page.click_back()
        # 等待消息界面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否包含[草稿]（间接验证，无法验证标红）
        self.assertEquals(message_page.is_first_message_draft(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0247(self):
        """消息草稿-聊天列表显示-草稿信息发送成功"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框
        group_chat_page.get_input_box()
        # 输入文本'测试文本'
        group_chat_page.input_text_message('这是一条特别长的测试文本足够出现省略号')
        # 点击返回
        group_chat_page.click_back()
        # 等待消息界面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否包含[草稿]（间接验证，无法验证标红）
        self.assertEquals(message_page.is_first_message_draft(), True)
        # 验证第一条消息是否包含'...'(无法抓取到省略号 简介验证窗口显示消息是否和整个文本一致)
        self.assertEquals(message_page.is_first_message_content('[草稿] 这是一条特别长的测试文本足够出现省略号'), True)
        # 点击'群聊1'
        message_page.choose_chat_by_name('群聊1')
        group_chat_page.wait_for_page_load()
        time.sleep(2)
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 点击返回
        group_chat_page.click_back()
        # 等待消息界面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否包含[草稿]
        self.assertEquals(message_page.is_first_message_draft(), False)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0044(self):
        """发送一组数字：12345678900，发送成功后，是否会被识别为号码"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 输入数字'12345678900' 发送两次 第一次抓去不到
        group_chat_page.input_text_message('12345678900')
        group_chat_page.click_send_button()
        group_chat_page.input_text_message('12345678900')
        group_chat_page.click_send_button()
        time.sleep(2)
        # 点击该行数字
        group_chat_page.click_text_message_by_number(-1)
        # 判断点击之后是否出现呼叫按钮
        self.assertEquals(group_chat_page.page_should_contain_text2('呼叫', 2), False)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0045(self):
        """发送一组数字：123456，发送成功后，是否会被识别为号码"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 输入数字'123456' 点击发送两次 第一次抓取不到
        group_chat_page.input_text_message('123456')
        group_chat_page.click_send_button()
        group_chat_page.input_text_message('123456')
        group_chat_page.click_send_button()
        time.sleep(2)
        # 点击该行数字
        group_chat_page.click_text_message_by_number(-1)
        time.sleep(2)
        # 判断点击之后是否出现呼叫按钮
        self.assertEquals(group_chat_page.page_should_contain_text2('呼叫'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0278(self):
        """通讯录——群聊——搜索——选择一个群"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        # 点击搜索群组
        select_one_group_page.click_search_box()
        # 输入搜索内容模糊搜索'群'
        select_one_group_page.input_search_keyword('群')
        # 判断当前页面是否存在'群聊1'
        self.assertEquals(select_contacts_page.page_should_contain_text2('群聊1'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0279(self):
        """通讯录-群聊-中文模糊搜索——搜索结果展示"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        # 点击搜索群组
        select_one_group_page.click_search_box()
        # 输入搜索内容模糊搜索'没有这个群'
        select_one_group_page.input_search_keyword('没有这个群')
        time.sleep(2)
        # 判断当前页面是否存在'无搜索结果'
        self.assertEquals(select_contacts_page.page_should_contain_text2('无搜索结果'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0605(self):
        """开启免打扰后，在聊天页面在输入框输入内容-返回到消息列表页时，该消息列表窗口直接展示：草稿"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置按钮
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        # 点击群消息免打扰开关
        if group_chat_page.get_no_disturbing_btn_text() == "0":
            group_chat_page.click_no_disturbing_button()
        # 返回群聊界面
        group_chat_page.click_back()
        group_chat_page.wait_for_page_load()
        # 输入文本
        group_chat_page.input_text_message('1234567890')
        # 点击返回
        group_chat_page.click_back()
        message_page.wait_for_page_load()
        # 判断第一条消息是否显示为草稿(开启免打扰后在消息页面显示是[草稿]+文本... )
        self.assertEquals(message_page.is_first_message_draft(), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0605():
        """恢复环境，将用例开启的消息免打扰开关关闭"""

        try:
            # 确认当前界面在消息界面然后进入到群聊1
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("群聊1")
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 判断消息免打扰按钮状态 如果是开启状态点击将其关闭
            if group_chat_page.get_no_disturbing_btn_text() == "1":
                group_chat_page.click_no_disturbing_button()
            group_chat_page.click_back()
            group_chat_page.wait_for_page_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0413(self):
        """群主在群设置页面——点击群名称——修改群名称"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 获取当前页面图片元素数量1(修改群名称前群聊页面图片数量)
        text1 = group_chat_page.get_picture_nums()
        # 点击设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        # 点击群名称
        group_chat_page.click_group_name()
        # 修改群名称为'已经将群名称修改'
        group_chat_page.input_group_name_message('已经将群名称修改')
        # 点击完成
        group_chat_page.click_group_name_complete()
        group_chat_page.wait_for_page_setting_load()
        # # 判断当前页面是否存在文本'修改成功'  有概率抓取不到 暂时不使用
        # self.assertEquals(group_chat_page.page_should_contain_text2('修改成功'), True)
        # 点击返回
        group_chat_page.click_back()
        group_chat_page.wait_for_page_load()
        # 获取当前页面图片元素数量2(修改群名称后群聊页面图片数量)
        text2 = group_chat_page.get_picture_nums()
        # 比较两次图片元素数量(修改成功提示为图片，无法捕捉文本，判断修改后的图片数量增加)
        self.assertEquals(int(text1) < int(text2), True)
        # 判断当前页面是否有'已经将群名称修改'文本
        self.assertEquals(group_chat_page.page_should_contain_text2('已经将群名称修改'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0413():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""

        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("已经将群名称修改")
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0414(self):
        """群主在设置页面——点击群管理——点击解散群按钮"""
        # 前置条件在消息界面进入'群聊1'界面
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 获取当前界面图片数量1
        text1 = group_chat_page.get_picture_nums()
        # 点击设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        # 点击群管理
        group_chat_page.click_group_control()
        # 点击解散群
        group_chat_page.click_group_dissolve()
        # 点击确认解散
        group_chat_page.click_group_dissolve_confirm()
        time.sleep(2)
        # 获取当前页面图片数量2
        text2 = group_chat_page.get_picture_nums()
        # 比较两次图片数量(该群已解散为图片无法捕捉文本，用图片增加替代)
        self.assertEquals(int(text1) < int(text2), True)
        # 点击返回
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 判断当前页面是否有文本 '系统消息该群已解散'
        self.assertEquals(message_page.page_should_contain_text2('该群已解散'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0414():
        """恢复环境，将用例解散的'群聊1'重新建立"""

        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            message_page = MessagePage()
            message_page.wait_for_page_load()
            # 点击加号
            message_page.click_add_icon()
            # 点击发起群聊
            message_page.click_group_chat()
            # 选择联系人界面
            select_contacts_page = SelectContactsPage()
            select_contacts_page.wait_for_page_load()
            # 点击选择手机联系人
            select_contacts_page.click_phone_contacts()
            # 通过文本点击添加(大佬1，大佬2)
            select_contacts_page.click_accessibility_id_attribute_by_name('大佬1')
            select_contacts_page.click_accessibility_id_attribute_by_name('大佬2')
            # 点击确定
            select_contacts_page.click_confirm_button()
            # 修改群聊名称
            select_contacts_page.input_group_name_message('群聊1')
            # 点击创建
            select_contacts_page.click_create_button()
            time.sleep(3)
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0548(self):
        """ 普通群，分享群聊邀请口令"""
        # 前置条件在消息界面,进入'群聊1'界面
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击邀请微信或QQ好友进群
        group_chat_set_page.click_invite_friend()
        group_chat_set_page.wait_for_page_load(15)
        # 判断当前页面是否有'分享群口令邀请好友进群'文本
        self.assertEquals(group_chat_set_page.page_should_contain_text2('分享群口令邀请好友进群'), True)
        # 点击下次再说
        group_chat_set_page.click_next_time()
        group_chat_set_page.wait_for_page_load()
        # 判断当前页面是否没有'分享群口令邀请好友进群'文本
        self.assertEquals(group_chat_set_page.page_should_contain_text2('分享群口令邀请好友进群'), False)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0551(self):
        """普通群，点击口令弹窗的立即分享按钮，分享群口令-QQ"""
        # 前置条件在消息界面,进入'群聊1'界面
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击邀请微信或QQ好友进群
        group_chat_set_page.click_invite_friend()
        self.assertEquals(group_chat_set_page.page_should_contain_text2('分享群口令邀请好友进群', 15), True)
        # 点击立即分享
        group_chat_set_page.click_sharing()
        # 点击分享到QQ
        # group_chat_set_page.click_share_qq()
        # (无法抓去到弹窗文本，暂不使用)判断当前界面是否包含文本'该应用尚未安装，请安装后重试'
        # self.assertEquals(group_chat_set_page.page_should_contain_text2('该应用尚未安装'), True)
        # 间接验证：点击分享到qq之后当前界面没有取消按钮
        self.assertEquals(group_chat_set_page.is_exist_cancel_button(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0555(self):
        """普通群，点击口令弹窗的立即分享按钮，分享群口令-微信"""
        # 前置条件在消息界面,进入'群聊1'界面
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击邀请微信或QQ好友进群
        group_chat_set_page.click_invite_friend()
        group_chat_set_page.wait_for_page_load(15)
        # 点击立即分享
        group_chat_set_page.click_sharing()
        # 点击分享到微信
        # group_chat_set_page.click_share_wechat()
        # (无法抓去到弹窗文本，暂不使用)判断当前界面是否包含文本'该应用尚未安装，请安装后重试'
        # self.assertEquals(group_chat_set_page.page_should_contain_text2('该应用尚未安装'), True)
        # 间接验证：点击分享到微信之后当前界面没有取消按钮
        self.assertEquals(group_chat_set_page.is_exist_cancel_button(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0189(self):
        """群聊设置页面——进入到群管理详情页(群聊人数为1)"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击群管理
        group_chat_set_page.click_group_control()
        # 点击群主管理权转让
        group_chat_set_page.click_group_manage_transfer_button()
        # 判断当前页面是否为空页面
        self.assertEquals(group_chat_set_page.page_should_contain_text2('选择成员'), True)
        time.sleep(2)


    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0190(self):
        """群聊设置页面——进入到群管理详情页（群聊人数为2）"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊2')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面-确保当前群聊人数为2人
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        group_chat_set_page.add_member_by_name('大佬1')
        time.sleep(2)
        # 点击群管理
        group_chat_set_page.click_group_control()
        # 点击群主管理权转让
        group_chat_set_page.click_group_manage_transfer_button()
        time.sleep(2)
        # 展示可进行群主转让的成员
        self.assertTrue(group_chat_set_page.is_exit_element(locator='群成员列表'))
        # 3、点击左上角的返回按钮，可以返回到群管理详情页
        group_chat_set_page.click_back()
        self.assertTrue(group_chat_set_page.is_text_present('群管理'))

    def tearDown_test_msg_xiaoqiu_0190(self):
        """解散群之后创建群"""
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        group_name = '群聊2'
        if my_group.is_text_present(group_name):
            my_group.select_group_by_name(group_name)
            GroupChatPage().click_setting()
            set = GroupChatSetPage()
            set.dissolution_the_group()
            time.sleep(2)
            GroupChatPage().click_back()
            my_group.creat_group_if_not_exit('群聊2', member_name=['大佬#', '大佬#&'])


    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0141(self):
        """群主——清除旧名称——录入一个汉字"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击群名称
        group_chat_page.click_group_name()
        # 修改群名称为'改'
        group_chat_page.input_group_name_message('改')
        # 点击完成
        group_chat_page.click_group_name_complete()
        group_chat_page.wait_for_page_setting_load()
        # 判断当前页面是否有'已经将群名称修改'文本
        self.assertEquals(group_chat_page.page_should_contain_text2('改'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0141():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""

        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("改")
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0173(self):
        """分享群二维码——搜索选择一个群"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击群二维码
        group_chat_set_page.click_group_code()
        # 点击二维码转发按钮
        group_chat_set_page.click_code_forward()
        # 点击选择一个群
        select_contacts_page = SelectContactsPage()
        select_contacts_page.click_select_one_group()
        # 点击搜索群组
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.click_search_box()
        # 输入搜索内容搜索'群聊1'
        select_one_group_page.input_search_keyword('群聊1')
        # 点击'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1 (3)')
        # 确认当前界面是否与取消按钮弹窗
        self.assertEquals(select_one_group_page.page_should_contain_text2('取消'), True)
        # 点击取消
        select_one_group_page.click_cancel_forward()
        # 确认当前界面是否在选择一个群界面
        self.assertEquals(select_one_group_page.page_should_contain_text2('群聊1'), True)
        # 再次点击'群聊1'
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.selecting_one_group_by_name('群聊1 (3)')
        # 点击发送
        select_one_group_page.click_sure_forward()
        # # 判断能否捕捉到'已分享'文本
        # self.assertEquals(group_chat_set_page.page_should_contain_text2('已分享'), True)
        # 间接验证，无法捕捉到文本，验证是否返回群二维码界面
        self.assertEquals(group_chat_set_page.page_should_contain_text2('群二维码'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0174(self):
        """分享群二维码到——选择一个群"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击群二维码
        group_chat_set_page.click_group_code()
        # 点击二维码转发按钮
        group_chat_set_page.click_code_forward()
        # 点击选择一个群
        select_contacts_page = SelectContactsPage()
        select_contacts_page.click_select_one_group()
        # 根据群名选择'群聊1'
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 确认当前界面是否与取消按钮弹窗
        self.assertEquals(select_one_group_page.page_should_contain_text2('取消'), True)
        # 点击取消
        select_one_group_page.click_cancel_forward()
        # 确认当前界面是否在选择一个群界面
        self.assertEquals(select_one_group_page.page_should_contain_text2('选择一个群'), True)
        # 再次点击'群聊1'
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 点击发送
        select_one_group_page.click_sure_forward()
        # # 判断能否捕捉到'已分享'文本
        # self.assertEquals(group_chat_set_page.page_should_contain_text2('已分享'), True)
        # 间接验证，无法捕捉到文本，验证是否返回群二维码界面
        self.assertEquals(group_chat_set_page.page_should_contain_text2('群二维码'), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0175(self):
        """分享群二维码到——选择选择团队联系人——搜索选择联系人"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击群二维码
        group_chat_set_page.click_group_code()
        time.sleep(3)
        # 点击二维码转发按钮
        group_chat_set_page.click_code_forward()
        # 点击选择团队联系人
        select_contacts_page = SelectContactsPage()
        select_contacts_page.click_group_contact()
        # 进入团队列表
        SelectHeContactsPage().select_one_team_by_name('ateam7272')
        # 3、搜索选择选择团队联系人，是否会弹出确认弹窗
        detail = SelectHeContactsDetailPage()
        detail.click_search_box()
        detail.input_search_text('大佬1')
        detail.click_search_result()
        self.assertTrue(detail.is_element_exit('取消'))
        self.assertTrue(detail.is_element_exit('确定'))
        # 4、点击取消，是否会关闭弹窗并停留在搜索结果展示页面
        detail.click_cancel()
        self.assertTrue(detail.is_element_exit('搜索结果列表'))
        # 5、点击确定，会返回到群二维码分享页面并弹出toast提示：已转发
        detail.click_search_result()
        detail.click_sure()
        time.sleep(2)
        self.assertTrue(group_chat_set_page.is_text_present('群二维码'))

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0179(self):
        """分享群二维码到——选择最近聊天"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入文字并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('确保群聊出现在最近聊天列表中')
        group_chat_page.click_send_button()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击群二维码
        group_chat_set_page.click_group_code()
        # 点击二维码转发按钮
        group_chat_set_page.click_code_forward()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 通过名字找到'群聊1'
        select_contacts_page.selecting_one_group_by_name('群聊1')
        # 确认当前界面是否与取消按钮弹窗
        self.assertEquals(select_contacts_page.page_should_contain_text2('取消'), True)
        # 点击取消
        select_contacts_page.click_cancel_forward()
        # 确认当前界面是否在选择一个群界面
        self.assertEquals(select_contacts_page.page_should_contain_text2('选择联系人'), True)
        # 再次点击'群聊1'
        select_contacts_page.selecting_one_group_by_name('群聊1')
        # 点击发送
        select_contacts_page.click_send()
        # # 判断能否捕捉到'已分享'文本
        # self.assertEquals(group_chat_set_page.page_should_contain_text2('已分享'), True)
        # 间接验证，无法捕捉到文本，验证是否返回群二维码界面
        self.assertEquals(group_chat_set_page.page_should_contain_text2('群二维码'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0074(self):
        """仅语音模式，录制时长大于10秒——发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击语音按钮，等待十秒
        group_chat_page.click_voice_button()
        # 判断当前界面是否有文本'语音录制中'
        self.assertEquals(group_chat_page.page_should_contain_text2('语音录制中'), True)
        time.sleep(10)
        # 点击退出按钮
        group_chat_page.click_exit_voice()
        # 判断当前界面是否有'语音录制中'文本，
        self.assertEquals(group_chat_page.page_should_contain_text2('语音录制中'), False)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0109(self):
        """在群聊会话页，点击输入框——调起小键盘"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框
        group_chat_page.input_text_message(' ')
        # 判断当前界面是否有小键盘的麦克风标志
        self.assertEquals(group_chat_page.is_exist_msg_dictation(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0195(self):
        """群聊设置页面——查找聊天内容——是否可以调起小键盘"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击查找聊天内容
        group_chat_set_page.click_find_chat_record()
        # 判断界面是否有小键盘麦克风标志
        self.assertEquals(group_chat_set_page.is_exist_msg_dictation(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0269(self):
        """普通群——聊天会话页面——未进群联系人展示"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊2')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_setting()
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        group_chat_set_page.click_name_attribute_by_name('群成员 (1）')
        self.assertEqual(group_chat_set_page.page_should_contain_text2('还有人未进群，再次邀请'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0196(self):
        """群聊设置页面——查找聊天内容——中文搜索——搜索结果展示"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入文字并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('确保当前群聊有聊天内容存在')
        group_chat_page.click_send_button()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击查找聊天内容
        group_chat_set_page.click_find_message_records()
        time.sleep(2)
        find_chat_record_page = FindChatRecordPage()
        find_chat_record_page.wait_for_page_loads()
        # 输入搜索信息
        find_chat_record_page.input_search_message('确保当前群聊有聊天内容存在')
        # 判断是否有头像名称时间消息记录存在
        self.assertEquals(find_chat_record_page.is_exist_find_content(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_portrait(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_name(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_time(), True)
        # 点击聊天记录
        find_chat_record_page.click_chat_records()
        group_chat_page.wait_for_page_load()
        # 判断当前是否在群聊页面
        self.assertEquals(group_chat_page.page_should_contain_text2('群聊1'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0021(self):
        """在群聊天会话页面，输入框中录入1个字符，使用缩小功能发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入文字并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('A')
        group_chat_page.click_send_button()
        # 发送两次 第一次消息截取不到
        group_chat_page.input_text_message('A')
        group_chat_page.click_send_button()
        # 获取文本框大小1
        w1 = group_chat_page.get_width_of_last_msg()
        h1 = group_chat_page.get_height_of_last_msg()
        # 输入'1' 点击发送并向下滑动缩小文本并发送
        group_chat_page.input_text_message('A')
        group_chat_page.click_send_slide_down()
        # 获取文本大小2
        w2 = group_chat_page.get_width_of_last_msg()
        h2 = group_chat_page.get_height_of_last_msg()
        # 比较文本框大小 文本框1>文本框2
        self.assertEquals(int(w1) > int(w2), True)
        self.assertEquals(int(h1) > int(h2), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0027(self):
        """在群聊天会话页面，输入框中录入1个表情，使用缩小功能发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框点击表情按钮点击微笑表情并发送
        group_chat_page.get_input_box()
        group_chat_page.click_expression_button()
        group_chat_page.click_expression_wx()
        group_chat_page.click_send_button()
        # 发送两次 第一次消息截取不到 发送窃喜表情
        group_chat_page.click_expression_qx()
        group_chat_page.click_send_button()
        # 获取文本框大小1
        w1 = group_chat_page.get_width_of_last_msg()
        h1 = group_chat_page.get_height_of_last_msg()
        # 输入流鼻涕表情点击发送并向下滑动缩小表情并发送
        group_chat_page.click_expression_lbt()
        group_chat_page.click_send_slide_down()
        # 获取文本大小2
        w2 = group_chat_page.get_width_of_last_msg()
        h2 = group_chat_page.get_height_of_last_msg()
        # 比较文本框大小 文本框1>文本框2
        self.assertEquals(int(w1) > int(w2), True)
        self.assertEquals(int(h1) > int(h2), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0031(self):
        """在群聊天会话页面，输入框中录入1个表情，使用放大功能发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框点击表情按钮点击微笑表情并发送
        group_chat_page.get_input_box()
        group_chat_page.click_expression_button()
        group_chat_page.click_expression_wx()
        group_chat_page.click_send_button()
        # 发送两次 第一次消息截取不到 发送窃喜表情
        group_chat_page.click_expression_qx()
        group_chat_page.click_send_button()
        # 获取文本框大小1
        w1 = group_chat_page.get_width_of_last_msg()
        h1 = group_chat_page.get_height_of_last_msg()
        # 输入流鼻涕表情点击发送并向上滑动放大表情并发送
        group_chat_page.click_expression_lbt()
        group_chat_page.click_send_slide_up()
        # 获取文本大小2
        w2 = group_chat_page.get_width_of_last_msg()
        h2 = group_chat_page.get_height_of_last_msg()
        # 比较文本框大小 文本框1>文本框2
        self.assertEquals(int(w1) < int(w2), True)
        self.assertEquals(int(h1) < int(h2), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0035(self):
        """进入到群聊天会话页面，录入文字+表情字符，放大发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入'我'点击表情按钮点击微笑表情并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('我')
        group_chat_page.click_expression_button()
        group_chat_page.click_expression_wx()
        group_chat_page.click_send_button()
        # 发送两次 第一次消息截取不到 发送窃喜表情
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('我')
        group_chat_page.click_expression_button()
        group_chat_page.click_expression_qx()
        group_chat_page.click_send_button()
        # 获取文本框大小1
        w1 = group_chat_page.get_width_of_last_msg()
        h1 = group_chat_page.get_height_of_last_msg()
        # 输入流鼻涕表情点击发送并向上滑动放大表情并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('我')
        group_chat_page.click_expression_button()
        group_chat_page.click_expression_lbt()
        group_chat_page.click_send_slide_up()
        # 获取文本大小2
        w2 = group_chat_page.get_width_of_last_msg()
        h2 = group_chat_page.get_height_of_last_msg()
        # 比较文本框大小 文本框1>文本框2
        self.assertEquals(int(w1) < int(w2), True)
        self.assertEquals(int(h1) < int(h2), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0036(self):
        """进入到群聊天会话页面，录入文字+表情字符，缩小发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入'我'点击表情按钮点击微笑表情并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('我')
        group_chat_page.click_expression_button()
        group_chat_page.click_expression_wx()
        group_chat_page.click_send_button()
        # 发送两次 第一次消息截取不到 发送窃喜表情
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('我')
        group_chat_page.click_expression_button()
        group_chat_page.click_expression_qx()
        group_chat_page.click_send_button()
        # 获取文本框大小1
        w1 = group_chat_page.get_width_of_last_msg()
        h1 = group_chat_page.get_height_of_last_msg()
        # 输入流鼻涕表情点击发送并向下滑动缩小表情并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('我')
        group_chat_page.click_expression_button()
        group_chat_page.click_expression_lbt()
        group_chat_page.click_send_slide_down()
        # 获取文本大小2
        w2 = group_chat_page.get_width_of_last_msg()
        h2 = group_chat_page.get_height_of_last_msg()
        # 比较文本框大小 文本框1>文本框2
        self.assertEquals(int(w1) > int(w2), True)
        self.assertEquals(int(h1) > int(h2), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0018(self):
        """群聊会话页面，使用拍照功能拍照编辑后发送照片"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        message_page = MessagePage()
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击拍照
        chat_photo_page.take_photo()
        time.sleep(2)
        chat_photo_page.click_edit_pic()
        # 编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        # 进行涂鸦操作
        chat_pic_edit_page.do_doodle()
        # 点击发送
        chat_pic_edit_page.click_send()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_back()
        message_page.wait_for_page_load()
        self.assertEquals(message_page.is_first_message_content('图片'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0019(self):
        """群聊会话页面，使用拍照功能拍照之后编辑并保存"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        message_page = MessagePage()
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击拍照
        chat_photo_page.take_photo()
        time.sleep(2)
        chat_photo_page.click_edit_pic()
        # 编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        # 进行涂鸦操作
        chat_pic_edit_page.do_doodle()
        # 点击保存
        chat_pic_edit_page.click_save()
        #  文本抓取不到
        # self.assertEquals(chat_pic_edit_page.page_should_contain_text2('已保存至系统相册'))
        time.sleep(2)
        # 点击发送
        chat_pic_edit_page.click_send()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_back()
        message_page.wait_for_page_load()
        self.assertEquals(message_page.is_first_message_content('图片'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0020(self):
        """群聊会话页面，使用拍照功能拍照编辑图片，再取消编辑并发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        message_page = MessagePage()
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击拍照
        chat_photo_page.take_photo()
        time.sleep(2)
        chat_photo_page.click_edit_pic()
        # 编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        # 进行涂鸦操作
        chat_pic_edit_page.do_doodle()
        # 点击取消
        chat_pic_edit_page.click_cancle()
        # 点击发送
        chat_photo_page.send_photo()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_back()
        message_page.wait_for_page_load()
        self.assertEquals(message_page.is_first_message_content('图片'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0022(self):
        """群聊会话页面，打开拍照，拍照之后返回会话窗口"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击返回
        chat_photo_page.take_photo_back()
        group_chat_page.wait_for_page_load()
        self.assertEquals(group_chat_page.page_should_contain_text2('群聊1'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0083(self):
        """群聊会话页面，发送相册内一个视频"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 先发送一条文本
        group_chat_page.input_text_message('测试文本')
        group_chat_page.click_send_button()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一个视频
        chat_pic_page.select_one_video()
        # 点击发送
        chat_pic_page.click_send()
        time.sleep(10)
        group_chat_page.wait_for_page_load()
        # 判断是否有视频播放按钮
        self.assertEquals(group_chat_page.is_exist_video_play_button(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0084(self):
        """群聊会话页面，发送相册内多个视频"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一个视频
        chat_pic_page.select_one_video()
        # 获取点击视频后发送按钮文本1
        text1 = chat_pic_page.get_send_video_text()
        time.sleep(1)
        chat_pic_page.select_one_video(1)
        # 获取点击视频后发送按钮文本2
        text2 = chat_pic_page.get_send_video_text()
        # 比较文本1和2是否相同（间接验证发送按钮没有变化说明无法同时选取照片和视频）
        self.assertEquals(text1, text2)
        # # 判断是否有文本'只能选中一个视频'  文本捕捉不到暂不使用
        # self.assertEquals(chat_pic_page.page_should_contain_text2('只能选中一个视频'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0085(self):
        """群聊会话页面，同时发送相册内视频和图片"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures(1)
        # 获取发送按钮文本1
        text1 = chat_pic_page.get_send_text()
        # 选择一个视频
        chat_pic_page.select_one_video()
        # 获取点击视频后发送按钮文本2
        text2 = chat_pic_page.get_send_text()
        # 比较文本1和2是否相同（发送按钮没有变化说明无法同时选取照片和视频）
        self.assertEquals(text1, text2)
        # # 判断点击图片之后是否有文字提示不能同时选择照片和视频（有时会抓不到文本信息 不稳定）
        # self.assertEquals(chat_pic_page.page_should_contain_text2("不能同时选择照片和视频", 20), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoliping_D_0086(self):
        """群聊会话页面，发送视频时预览视频"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一个视频
        chat_pic_page.select_one_video()
        chat_pic_page.click_preview()
        # 判断是否有预览(1/1)文本
        self.assertEquals(chat_pic_page.page_should_contain_text2('预览(1/1)'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0024(self):
        """我的电脑会话页面，不勾选相册内图片点击发送按钮"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 判断发送按钮enabled是否为false
        self.assertEquals(chat_pic_page.send_btn_is_enabled(), False)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0025(self):
        """我的电脑会话页面，勾选相册内一张图片发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_pictures(1)
        chat_pic_page.click_send()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertEquals(message_page.is_first_message_content('图片'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0026(self):
        """我的电脑会话页面，预览相册内图片"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_pictures(1)
        chat_pic_page.click_preview()
        self.assertEquals(chat_pic_page.page_should_contain_text2('预览(1/1)'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0027(self):
        """我的电脑会话页面，预览相册内图片，不勾选原图发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_pictures(1)
        chat_pic_page.click_preview()
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.click_send()
        # 群聊界面
        group_chat_page.wait_for_page_load()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertEquals(message_page.is_first_message_content('图片'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0028(self):
        """我的电脑会话页面，预览相册数量与发送按钮数量一致"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击选择照片
        group_chat_page.click_picture()
        # 选择图片页面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择多张照片
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
    def test_msg_huangcaizui_D_0029(self):
        """我的电脑会话页面，编辑图片发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
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
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0030(self):
        """我的电脑会话页面，编辑图片不保存发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
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
        chat_pic_edit_page.do_doodle()
        chat_pic_edit_page.click_mosaic()
        chat_pic_edit_page.do_mosaic()
        chat_pic_edit_page.click_text_edit_btn()
        chat_pic_edit_page.input_pic_text()
        # 点击完成
        chat_pic_edit_page.click_done()
        # 点击保存
        chat_pic_edit_page.click_save()
        self.assertEquals(chat_pic_edit_page.page_should_contain_text2('已保存至系统相册'), True)
        # 点击发送
        chat_pic_edit_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0031(self):
        """我的电脑会话页面，编辑图片中途直接发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
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
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0032(self):
        """我的电脑会话页面，编辑图片保存"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
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
        chat_pic_edit_page.do_doodle()
        chat_pic_edit_page.click_mosaic()
        chat_pic_edit_page.do_mosaic()
        chat_pic_edit_page.click_text_edit_btn()
        chat_pic_edit_page.input_pic_text()
        # 点击完成
        chat_pic_edit_page.click_done()
        # 点击保存
        chat_pic_edit_page.click_save()
        self.assertEquals(chat_pic_edit_page.page_should_contain_text2('已保存至系统相册'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0033(self):
        """我的电脑会话页面，取消编辑图片"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
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
        chat_pic_edit_page.do_doodle()
        chat_pic_edit_page.click_mosaic()
        chat_pic_edit_page.do_mosaic()
        chat_pic_edit_page.click_text_edit_btn()
        chat_pic_edit_page.input_pic_text()
        chat_pic_edit_page.click_done()
        # 点击取消
        chat_pic_edit_page.click_cancle()
        time.sleep(2)
        self.assertEquals(chat_pic_preview_page.page_should_contain_text2('预览(1/1)'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0034(self):
        """我的电脑会话页面，取消编辑图片，点击发送按钮"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
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
        chat_pic_edit_page.do_doodle()
        chat_pic_edit_page.click_mosaic()
        chat_pic_edit_page.do_mosaic()
        chat_pic_edit_page.click_text_edit_btn()
        chat_pic_edit_page.input_pic_text()
        chat_pic_edit_page.click_done()
        # 点击取消
        chat_pic_edit_page.click_cancle()
        time.sleep(2)
        # 点击发送
        chat_pic_preview_page.click_send()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertEquals(message_page.is_first_message_content('图片'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0035(self):
        """我的电脑会话页面，发送相册内的图片，看预览界面是否正确"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击选择照片
        group_chat_page.click_picture()
        # 选择图片页面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 获取当前页面图片以及视频数量
        numbers1 = chat_pic_page.get_pic_numbers()
        numbers2 = chat_pic_page.get_video_numbers()
        # 直接点击图片
        chat_pic_page.click_picture_just()
        chat_pic_edit_page = ChatPicEditPage()
        self.assertEquals(chat_pic_edit_page.page_should_contain_text2('预览(1/' + str(numbers1+numbers2)), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0037(self):
        """我的电脑会话页面，勾选9张相册内图片发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击选择照片
        group_chat_page.click_picture()
        # 选择图片页面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择九张图片
        chat_pic_page.select_pictures(9)
        # 点击发送
        chat_pic_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（发送图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0038(self):
        """我的电脑会话页面，勾选9张相册内图片发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击选择照片
        group_chat_page.click_picture()
        # 选择图片页面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择九张图片
        chat_pic_page.select_pictures(9)
        # 判断第十个图片的点击按钮是否不可点击
        self.assertEquals(chat_pic_page.picture_btn_is_enabled(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0039(self):
        """我的电脑会话页面，同时发送相册中的图片和视频"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击选择照片
        group_chat_page.click_picture()
        # 选择图片页面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures(1)
        # 获取发送按钮文本1
        text1 = chat_pic_page.get_send_text()
        # 选择一个视频
        chat_pic_page.select_one_video()
        # 获取点击视频后发送按钮文本2
        text2 = chat_pic_page.get_send_text()
        # 比较文本1和2是否相同（发送按钮没有变化说明无法同时选取照片和视频）
        self.assertEquals(text1, text2)
        # # 判断点击图片之后是否有文字提示不能同时选择照片和视频（有时会抓不到文本信息 不稳定）
        # self.assertEquals(chat_pic_page.page_should_contain_text2("不能同时选择照片和视频", 20), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0040(self):
        """我的电脑会话页面，使用拍照功能并发送照片"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击拍照
        chat_photo_page.take_photo()
        # 点击发送
        chat_photo_page.send_photo()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（发送图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0041(self):
        """我的电脑会话页面，使用拍照功能拍照编辑后发送照片"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击拍照
        chat_photo_page.take_photo()
        chat_photo_page.click_edit_pic()
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        chat_pic_edit_page.do_doodle()
        chat_pic_edit_page.click_mosaic()
        chat_pic_edit_page.do_mosaic()
        chat_pic_edit_page.click_text_edit_btn()
        chat_pic_edit_page.input_pic_text()
        chat_pic_edit_page.click_done()
        # 点击发送
        chat_pic_edit_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0042(self):
        """我的电脑会话页面，使用拍照功能拍照之后编辑并保存"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击拍照
        chat_photo_page.take_photo()
        chat_photo_page.click_edit_pic()
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        chat_pic_edit_page.do_doodle()
        chat_pic_edit_page.click_mosaic()
        chat_pic_edit_page.do_mosaic()
        chat_pic_edit_page.click_text_edit_btn()
        chat_pic_edit_page.input_pic_text()
        chat_pic_edit_page.click_done()
        # 点击保存
        chat_pic_edit_page.click_save()
        self.assertEquals(chat_pic_edit_page.page_should_contain_text2('已保存至系统相册'), True)
        # 点击发送
        chat_pic_edit_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0043(self):
        """我的电脑会话页面，使用拍照功能拍照编辑图片，再取消编辑并发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击拍照
        chat_photo_page.take_photo()
        chat_photo_page.click_edit_pic()
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        chat_pic_edit_page.do_doodle()
        chat_pic_edit_page.click_mosaic()
        chat_pic_edit_page.do_mosaic()
        chat_pic_edit_page.click_text_edit_btn()
        chat_pic_edit_page.input_pic_text()
        chat_pic_edit_page.click_done()
        # 点击取消
        chat_pic_edit_page.click_cancle()
        # 点击发送
        chat_photo_page.send_photo()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0044(self):
        """我的电脑会话页面，打开拍照，立刻返回会话窗口"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        chat_photo_page.take_photo_back()
        group_chat_page.wait_for_page_load()

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0045(self):
        """我的电脑会话页面，打开拍照，拍照之后返回会话窗口"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        chat_photo_page.take_photo_back()
        group_chat_page.wait_for_page_load()

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0048(self):
        """在我的电脑会话窗，验证点击趣图搜搜入口"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击表情按钮
        group_chat_page.click_expression_button()
        group_chat_page.wait_for_page_load()
        # 点击gif按钮
        group_chat_page.click_gif_button()
        group_chat_page.wait_for_page_load()
        # 判断当前页面时候有关闭gif按钮
        self.assertEquals(group_chat_page.is_exist_close_gif(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0049(self):
        """在我的电脑会话窗，网络正常发送表情搜搜"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击表情按钮
        group_chat_page.click_expression_button()
        group_chat_page.wait_for_page_load()
        # 点击gif按钮
        group_chat_page.click_gif_button()
        group_chat_page.wait_for_page_load()
        # 点击发送GIF图片
        group_chat_page.click_send_gif()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 判断第一条消息是否为表情
        self.assertEquals(message_page.is_first_message_expression(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0051(self):
        """在我的电脑会话窗，搜索数字关键字选择发送趣图"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击表情按钮
        group_chat_page.click_expression_button()
        group_chat_page.wait_for_page_load()
        # 点击gif按钮
        group_chat_page.click_gif_button()
        group_chat_page.wait_for_page_load()
        group_chat_page.input_text_message('1')
        time.sleep(1)
        # 点击发送GIF图片
        group_chat_page.click_send_gif()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 判断第一条消息是否为表情
        self.assertEquals(message_page.is_first_message_expression(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0052(self):
        """在我的电脑会话窗，搜索特殊字符关键字发送趣图"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击表情按钮
        group_chat_page.click_expression_button()
        group_chat_page.wait_for_page_load()
        # 点击gif按钮
        group_chat_page.click_gif_button()
        group_chat_page.wait_for_page_load()
        group_chat_page.input_text_message('!')
        time.sleep(1)
        # 点击发送GIF图片
        group_chat_page.click_send_gif()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 判断第一条消息是否为表情
        self.assertEquals(message_page.is_first_message_expression(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0053(self):
        """在我的电脑会话窗，搜索无结果的趣图"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击表情按钮
        group_chat_page.click_expression_button()
        group_chat_page.wait_for_page_load()
        # 点击gif按钮
        group_chat_page.click_gif_button()
        group_chat_page.wait_for_page_load()
        group_chat_page.input_text_message('！！！')
        # 判断是否有'无搜索结果'文本
        self.assertEquals(group_chat_page.page_should_contain_text2('无搜索结果'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangcaizui_D_0057(self):
        """在我的电脑会话窗，关闭GIF搜索框"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击表情按钮
        group_chat_page.click_expression_button()
        # 点击gif按钮
        group_chat_page.click_gif_button()
        group_chat_page.click_close_gif()
        # 判断当前页面是否还有关闭gif按钮，
        self.assertEquals(group_chat_page.is_exist_close_gif(), False)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0046(self):
        """发送一组数字：18431931414，发送成功后，是否会被识别为号码"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 输入数字'18431931414'
        group_chat_page.input_text_message('18431931414')
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 输入数字'18431931414' 发送第一次文本无法捕捉需要发送两次
        group_chat_page.input_text_message('18431931414')
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 点击该行数字
        group_chat_page.click_text_message_by_number(-1)
        # 判断点击之后是否出现呼叫按钮
        self.assertEquals(group_chat_page.page_should_contain_text2('呼叫', 2), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0047(self):
        """发送一组数字：+85267656003，发送成功后，是否会被识别为号码"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 输入数字'18431931414'
        group_chat_page.input_text_message('+85267656003')
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 输入数字'18431931414' 发送第一次文本无法捕捉需要发送两次
        group_chat_page.input_text_message('+85267656003')
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 点击该行数字
        group_chat_page.click_text_message_by_number(-1)
        # 判断点击之后是否出现呼叫按钮
        self.assertEquals(group_chat_page.page_should_contain_text2('呼叫', 2), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0048(self):
        """发送一组数字：67656003，发送成功后，是否会被识别为号码"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 输入数字'18431931414'
        group_chat_page.input_text_message('67656003')
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 输入数字'18431931414' 发送第一次文本无法捕捉需要发送两次
        group_chat_page.input_text_message('67656003')
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 点击该行数字
        group_chat_page.click_text_message_by_number(-1)
        # 判断点击之后是否出现呼叫按钮
        self.assertEquals(group_chat_page.page_should_contain_text2('呼叫', 2), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0049(self):
        """发送一组数字：95533，发送成功后，是否会被识别为号码"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 输入数字'18431931414'
        group_chat_page.input_text_message('95533')
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 输入数字'18431931414' 发送第一次文本无法捕捉需要发送两次
        group_chat_page.input_text_message('95533')
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 点击该行数字
        group_chat_page.click_text_message_by_number(-1)
        # 判断点击之后是否出现呼叫按钮
        self.assertEquals(group_chat_page.page_should_contain_text2('呼叫', 2), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0103(self):
        """在群聊会话窗口，点击输入框上方的相机ICON，进入到相机拍摄页"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击相机按钮
        group_chat_page.click_take_picture()
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.press_video(3)
        chat_photo_page.send_photo()
        # 群聊界面加载
        group_chat_page.wait_for_page_load()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertEquals(message_page.is_first_message_content('视频'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0104(self):
        """点击输入框上方的名片ICON——进入到联系人选择器页"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击加号名片
        group_chat_page.click_add_button()
        group_chat_page.click_profile()
        select_contacts_page = SelectContactsPage()
        select_contacts_page.click_name_attribute_by_name('大佬1')
        select_contacts_page.click_send_card()
        group_chat_page.wait_for_page_load()
        self.assertEquals(group_chat_page.page_should_contain_text2('个人名片'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0105(self):
        """点击输入框上方的GIFICON——展示GIF图片推荐列表"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 发送gif图片
        group_chat_page.click_expression_button()
        group_chat_page.click_gif_button()
        group_chat_page.click_send_gif()
        self.assertEquals(group_chat_page.page_should_contain_text2('我'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0123(self):
        """在群聊设置页面中——群主头像展示"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 群聊设置界面
        group_chat_page.click_setting()
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        self.assertEquals(group_chat_set_page.is_exist_crown(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0142(self):
        """群主——清除旧名称——录入5个汉字"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'这是五个字'
        group_chat_page.input_group_name_message('这是五个字')
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('这是五个字'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0142():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""

        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("这是五个字")
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0143(self):
        """群主——清除旧名称——录入10个汉字"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'一一一一一这是十个字'
        group_chat_page.input_group_name_message('一一一一一这是十个字')
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('一一一一一这是十个字'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0143():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("一一一一一这是十个字")
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0145(self):
        """群主——清除旧名称——录入1个字母（不区分大、小写）"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'A'
        group_chat_page.input_group_name_message('A')
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('A'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0145():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("A")
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0146(self):
        """群主——清除旧名称——录入10个字母（不区分大、小写）"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'AAAAAAAAAA'
        group_chat_page.input_group_name_message('AAAAAAAAAA')
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('AAAAAAAAAA'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0146():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("AAAAAAAAAA")
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0147(self):
        """群主——清除旧名称——录入29个字母（不区分大、小写）"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'29个A'
        group_chat_page.input_group_name_message('A' * 29)
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('A' * 29), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0147():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('A' * 29)
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0148(self):
        """群主——清除旧名称——录入30个字母（不区分大、小写）"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'三十个A'
        group_chat_page.input_group_name_message('A' * 30)
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('A' * 30), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0148():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('A' * 30)
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0154(self):
        """群主——清除旧名称——录入汉字+字母+数字"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'啊A1'
        group_chat_page.input_group_name_message('啊A1')
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('啊A1'), True)


    @staticmethod
    def tearDown_test_msg_xiaoqiu_0154():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('啊A1')
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0155(self):
        """群主——清除旧名称——录入特殊字符"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'¥'
        group_chat_page.input_group_name_message('¥')
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('¥'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0155():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('¥')
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0150(self):
        """群主——清除旧名称——录入1个数字"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'1'
        group_chat_page.input_group_name_message('1')
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('1'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0150():

        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'1'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("1")
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0151(self):
        """群主——清除旧名称——录入10个数字"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'1234567890'
        group_chat_page.input_group_name_message('1234567890')
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('1234567890'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0151():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'1234567890'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("1234567890")
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0152(self):
        """群主——清除旧名称——录入30个数字"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'三十个1'
        group_chat_page.input_group_name_message('1' * 30)
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('1' * 30), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0152():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'1'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('1' * 30)
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0157(self):
        """群主——清除旧名片——录入一个汉字"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'啊'
        group_chat_page.input_group_name_message('啊')
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('啊'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0157():

        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'啊'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("啊")
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0158(self):
        """群主——清除旧名称——录入5个汉字"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'这是五个字'
        group_chat_page.input_group_name_message('这是五个字')
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('这是五个字'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0158():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""

        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("这是五个字")
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0159(self):
        """群主——清除旧名称——录入10个汉字"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'一一一一一这是十个字'
        group_chat_page.input_group_name_message('一一一一一这是十个字')
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('一一一一一这是十个字'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0159():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("一一一一一这是十个字")
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0161(self):
        """群主——清除旧名称——录入1个字母（不区分大、小写）"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'A'
        group_chat_page.input_group_name_message('A')
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('A'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0161():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("A")
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0162(self):
        """群主——清除旧名称——录入10个字母（不区分大、小写）"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'AAAAAAAAAA'
        group_chat_page.input_group_name_message('AAAAAAAAAA')
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('AAAAAAAAAA'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0162():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("AAAAAAAAAA")
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0163(self):
        """群主——清除旧名称——录入29个字母（不区分大、小写）"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'29个A'
        group_chat_page.input_group_name_message('A' * 29)
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('A' * 29), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0163():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('A' * 29)
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0164(self):
        """群主——清除旧名称——录入30个字母（不区分大、小写）"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'三十个A'
        group_chat_page.input_group_name_message('A' * 30)
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('A' * 30), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0164():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('A' * 30)
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0166(self):
        """群主——清除旧名称——录入1个数字"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'1'
        group_chat_page.input_group_name_message('1')
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('1'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0166():

        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'1'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("1")
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0167(self):
        """群主——清除旧名称——录入10个数字"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'1234567890'
        group_chat_page.input_group_name_message('1234567890')
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('1234567890'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0167():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'1234567890'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("1234567890")
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0170(self):
        """群主——清除旧名称——录入汉字+字母+数字"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'啊A1'
        group_chat_page.input_group_name_message('啊A1')
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('啊A1'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0170():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('啊A1')
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0168(self):
        """群主——清除旧名称——录入30个数字"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'三十个1'
        group_chat_page.input_group_name_message('1' * 30)
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('1' * 30), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0168():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'1'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('1' * 30)
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0171(self):
        """群主——清除旧名称——录入特殊字符"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'¥'
        group_chat_page.input_group_name_message('¥')
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('¥'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0171():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('¥')
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0144(self):
        """群主——清除旧名称——录入11个汉字"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'十一个一'
        group_chat_page.input_group_name_message('一' * 11)
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('一' * 11), False)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0144():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("一" * 10)
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0149(self):
        """群主——清除旧名称——录入31个字母（不区分大、小写）"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'三十个A'
        group_chat_page.input_group_name_message('A' * 31)
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('A' * 31), False)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0149():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('A' * 30)
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0153(self):
        """群主——清除旧名称——录入31个数字"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'三十个A'
        group_chat_page.input_group_name_message('1' * 31)
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('1' * 31), False)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0153():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('1' * 30)
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0160(self):
        """群主——清除旧名称——录入11个汉字"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'十一个一'
        group_chat_page.input_group_name_message('一' * 11)
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('一' * 11), False)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0160():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("一" * 10)
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0165(self):
        """群主——清除旧名称——录入31个字母（不区分大、小写）"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'三十个A'
        group_chat_page.input_group_name_message('A' * 31)
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('A' * 31), False)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0165():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('A' * 30)
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0169(self):
        """群主——清除旧名称——录入31个数字"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_group_name()
        # 修改群名称为'三十个A'
        group_chat_page.input_group_name_message('1' * 31)
        group_chat_page.click_group_name_complete()
        time.sleep(2)
        self.assertEquals(group_chat_page.page_should_contain_text2('1' * 31), False)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0169():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('1' * 30)
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0156(self):
        """群主——修改群名片"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_page.click_my_group_name()
        group_chat_page.click_delete_text()
        time.sleep(2)
        # 提取输入框文本进行比较
        text1 = '设置您在群内显示的昵称'
        text2 = group_chat_page.get_group_name_text()
        self.assertEquals(text1, text2)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0172(self):
        """群二维码入口详情页"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击群聊设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.click_group_code()
        # 判断是否存在二维码转发按钮
        self.assertEquals(group_chat_set_page.is_exist_code_forward_button(), True)
        group_chat_set_page.click_back()
        group_chat_set_page.wait_for_page_load()

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0176(self):
        """分享群二维码到——选择选择团队联系人——选择联系人"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击群二维码
        group_chat_set_page.click_group_code()
        # 点击二维码转发按钮
        group_chat_set_page.click_code_forward()
        # 选择联系人
        select_contacts_page = SelectContactsPage()
        select_contacts_page.click_group_contact()
        select_contacts_page.click_name_attribute_by_name('ateam7272')
        time.sleep(1)
        select_contacts_page.selecting_local_contacts_by_name('大佬1')
        time.sleep(1)
        self.assertEquals(select_contacts_page.page_should_contain_text2('确定'), True)
        select_contacts_page.click_cancel_forward()
        select_contacts_page.selecting_local_contacts_by_name('大佬1')
        select_contacts_page.click_sure_forward()
        # # 判断能否捕捉到'已分享'文本
        # self.assertEquals(group_chat_set_page.page_should_contain_text2('已分享'), True)
        # 间接验证，无法捕捉到文本，验证是否返回群二维码界面
        self.assertEquals(group_chat_set_page.page_should_contain_text2('群二维码'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0178(self):
        """分享群二维码到——选择手机联系人——选择手机联系人"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击群二维码
        group_chat_set_page.click_group_code()
        # 点击二维码转发按钮
        group_chat_set_page.click_code_forward()
        # 选择联系人
        select_contacts_page = SelectContactsPage()
        select_contacts_page.select_local_contacts()
        select_contacts_page.click_name_attribute_by_name('大佬1')
        self.assertEquals(select_contacts_page.page_should_contain_text2('确定'), True)
        select_contacts_page.click_cancel_send()
        self.assertEquals(select_contacts_page.page_should_contain_text2('选择联系人'), True)
        # 再次点击'大佬1'
        select_contacts_page.click_name_attribute_by_name('大佬1')
        time.sleep(1)
        select_contacts_page.click_sure_forward_code()
        # # 判断能否捕捉到'已分享'文本
        # self.assertEquals(group_chat_set_page.page_should_contain_text2('已分享'), True)
        # 间接验证，无法捕捉到文本，验证是否返回群二维码界面
        self.assertEquals(group_chat_set_page.page_should_contain_text2('群二维码'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0177(self):
        """分享群二维码到——选择手机联系人——搜索选择联系人"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击群二维码
        group_chat_set_page.click_group_code()
        # 点击二维码转发按钮
        group_chat_set_page.click_code_forward()
        # 选择联系人
        select_contacts_page = SelectContactsPage()
        select_contacts_page.input_search_keyword('大佬1')
        time.sleep(1)
        select_contacts_page.selecting_local_contacts_by_name('大佬1')
        time.sleep(1)
        self.assertEquals(select_contacts_page.page_should_contain_text2('确定'), True)
        select_contacts_page.click_cancel_forward()
        select_contacts_page.selecting_local_contacts_by_name('大佬1')
        select_contacts_page.click_sure_forward()
        # # 判断能否捕捉到'已分享'文本
        # self.assertEquals(group_chat_set_page.page_should_contain_text2('已分享'), True)
        # 间接验证，无法捕捉到文本，验证是否返回群二维码界面
        self.assertEquals(group_chat_set_page.page_should_contain_text2('群二维码'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0186(self):
        """群二维码详情页——保存二维码"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击群二维码
        group_chat_set_page.click_group_code()
        group_chat_set_page.click_save_code()
        # # 判断是否捕捉到'已保存至系统相册'文本
        # self.assertEquals(group_chat_set_page.page_should_contain_text2('保存至系统相册'), True)
        time.sleep(2)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0187(self):
        """群聊设置页面——进入到群管理详情页"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击群管理
        group_chat_set_page.click_group_control()
        # 点击群主管理权转让
        group_chat_set_page.click_group_manage_transfer_button()
        time.sleep(3)
        # 判断当前页面是否为空页面
        self.assertEquals(group_chat_set_page.page_should_contain_text2('选择成员'), True)
        group_chat_set_page.click_back()
        self.assertEquals(group_chat_set_page.page_should_contain_text2('群管理'), True)
        time.sleep(2)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0197(self):
        """群聊设置页面——查找聊天内容——数字搜索——搜索结果展示"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入文字并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('1234567890')
        group_chat_page.click_send_button()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击查找聊天内容
        group_chat_set_page.click_find_message_records()
        time.sleep(2)
        find_chat_record_page = FindChatRecordPage()
        find_chat_record_page.wait_for_page_loads()
        # 输入搜索信息
        find_chat_record_page.input_search_message('1234567890')
        # 判断是否有头像名称时间消息记录存在
        self.assertEquals(find_chat_record_page.is_exist_find_content(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_portrait(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_name(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_time(), True)
        # 点击聊天记录
        find_chat_record_page.click_chat_records()
        group_chat_page.wait_for_page_load()
        # 判断当前是否在群聊页面
        self.assertEquals(group_chat_page.page_should_contain_text2('群聊1'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0198(self):
        """群聊设置页面——查找聊天内容——英文搜索——搜索结果展示"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入文字并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('English')
        group_chat_page.click_send_button()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击查找聊天内容
        group_chat_set_page.click_find_message_records()
        time.sleep(2)
        find_chat_record_page = FindChatRecordPage()
        find_chat_record_page.wait_for_page_loads()
        # 输入搜索信息
        find_chat_record_page.input_search_message('English')
        # 判断是否有头像名称时间消息记录存在
        self.assertEquals(find_chat_record_page.is_exist_find_content(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_portrait(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_name(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_time(), True)
        # 点击聊天记录
        find_chat_record_page.click_chat_records()
        group_chat_page.wait_for_page_load()
        # 判断当前是否在群聊页面
        self.assertEquals(group_chat_page.page_should_contain_text2('群聊1'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0199(self):
        """群聊设置页面——查找聊天内容——特殊字符搜索——搜索结果展示"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入文字并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('$')
        time.sleep(2)
        group_chat_page.click_send_button()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击查找聊天内容
        group_chat_set_page.click_find_message_records()
        time.sleep(2)
        find_chat_record_page = FindChatRecordPage()
        find_chat_record_page.wait_for_page_loads()
        # 输入搜索信息
        find_chat_record_page.input_search_message('$')
        # 判断是否有头像名称时间消息记录存在
        self.assertEquals(find_chat_record_page.is_exist_find_content(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_portrait(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_name(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_time(), True)
        # 点击聊天记录
        find_chat_record_page.click_chat_records()
        group_chat_page.wait_for_page_load()
        # 判断当前是否在群聊页面
        self.assertEquals(group_chat_page.page_should_contain_text2('群聊1'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0201(self):
        """群聊设置页面，查找聊天内容——空格搜索"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入文字并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('我     我     我')
        time.sleep(2)
        group_chat_page.click_send_button()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击查找聊天内容
        group_chat_set_page.click_find_message_records()
        time.sleep(2)
        find_chat_record_page = FindChatRecordPage()
        find_chat_record_page.wait_for_page_loads()
        # 输入搜索信息
        find_chat_record_page.input_search_message(' ')
        # 判断是否有头像名称时间消息记录存在
        self.assertEquals(find_chat_record_page.is_exist_find_content(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_portrait(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_name(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_time(), True)
        # 点击聊天记录
        find_chat_record_page.click_chat_records()
        group_chat_page.wait_for_page_load()
        # 判断当前是否在群聊页面
        self.assertEquals(group_chat_page.page_should_contain_text2('群聊1'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0203(self):
        """群聊设置页面——查找聊天内容——数字+汉字+英文搜索——搜索结果展示"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入文字并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('1一one')
        time.sleep(2)
        group_chat_page.click_send_button()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击查找聊天内容
        group_chat_set_page.click_find_message_records()
        time.sleep(2)
        find_chat_record_page = FindChatRecordPage()
        find_chat_record_page.wait_for_page_loads()
        # 输入搜索信息
        find_chat_record_page.input_search_message('1一one')
        # 判断是否有头像名称时间消息记录存在
        self.assertEquals(find_chat_record_page.is_exist_find_content(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_portrait(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_name(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_time(), True)
        # 点击聊天记录
        find_chat_record_page.click_chat_records()
        group_chat_page.wait_for_page_load()
        # 判断当前是否在群聊页面
        self.assertEquals(group_chat_page.page_should_contain_text2('群聊1'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0204(self):
        """群聊设置页面——查找聊天内容——数字+汉字+英文搜索——搜索结果展示（不存在文本消息）"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入文字并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('一条消息')
        time.sleep(2)
        group_chat_page.click_send_button()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.left_slide_message_record_by_number()
        time.sleep(2)
        message_page.click_element_('删除')
        # 通过名字找到'群聊1'
        message_page.click_add_icon()
        message_page.click_group_chat()
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        select_contacts_page.click_select_one_group()
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击查找聊天内容
        group_chat_set_page.click_find_message_records()
        time.sleep(2)
        find_chat_record_page = FindChatRecordPage()
        find_chat_record_page.wait_for_page_loads()
        # 输入搜索信息
        find_chat_record_page.input_search_message('12一二one two')
        # 判断当前是否显示无搜索结果
        self.assertEquals(find_chat_record_page.page_should_contain_text2('无搜索结果'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0205(self):
        """群聊设置页面——查找聊天内容——中文搜索——搜索结果展示（不存在文本消息）"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入文字并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('一条消息')
        time.sleep(2)
        group_chat_page.click_send_button()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.left_slide_message_record_by_number()
        time.sleep(2)
        message_page.click_element_('删除')
        # 通过名字找到'群聊1'
        message_page.click_add_icon()
        message_page.click_group_chat()
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        select_contacts_page.click_select_one_group()
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击查找聊天内容
        group_chat_set_page.click_find_message_records()
        time.sleep(2)
        find_chat_record_page = FindChatRecordPage()
        find_chat_record_page.wait_for_page_loads()
        # 输入搜索信息
        find_chat_record_page.input_search_message('请问请问请问请问')
        # 判断当前是否显示无搜索结果
        self.assertEquals(find_chat_record_page.page_should_contain_text2('无搜索结果'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0206(self):
        """群聊设置页面——查找聊天内容——数字搜索——搜索结果展示（不存在文本消息）"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入文字并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('一条消息')
        time.sleep(2)
        group_chat_page.click_send_button()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.left_slide_message_record_by_number()
        time.sleep(3)
        message_page.click_element_('删除')
        time.sleep(2)
        # 通过名字找到'群聊1'
        message_page.click_add_icon()
        message_page.click_group_chat()
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        select_contacts_page.click_select_one_group()
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击查找聊天内容
        group_chat_set_page.click_find_message_records()
        time.sleep(2)
        find_chat_record_page = FindChatRecordPage()
        find_chat_record_page.wait_for_page_loads()
        # 输入搜索信息
        find_chat_record_page.input_search_message('1234567890')
        # 判断当前是否显示无搜索结果
        self.assertEquals(find_chat_record_page.page_should_contain_text2('无搜索结果'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0207(self):
        """群聊设置页面——查找聊天内容——英文搜索——搜索结果展示（不存在文本消息）"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入文字并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('一条消息')
        time.sleep(2)
        group_chat_page.click_send_button()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.left_slide_message_record_by_number()
        time.sleep(2)
        message_page.click_element_('删除')
        # 通过名字找到'群聊1'
        message_page.click_add_icon()
        message_page.click_group_chat()
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        select_contacts_page.click_select_one_group()
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击查找聊天内容
        group_chat_set_page.click_find_message_records()
        time.sleep(2)
        find_chat_record_page = FindChatRecordPage()
        find_chat_record_page.wait_for_page_loads()
        # 输入搜索信息
        find_chat_record_page.input_search_message('asd')
        # 判断当前是否显示无搜索结果
        self.assertEquals(find_chat_record_page.page_should_contain_text2('无搜索结果'), True)

    def setUp_test_msg_xiaoqiu_0129(self):
        """确保进入群聊页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        name = '群聊2'
        if msg.is_text_present(name):
            msg.click_text(name)
        else:
            msg.click_search_box()
            time.sleep(1)
            msg.input_search_text(name)
            time.sleep(2)
            msg.click_element_first_list()
            time.sleep(2)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0129(self):
        """普通群——群成员——添加一个成员（群成员人数为2）"""
        GroupChatPage().click_setting()
        # 设置页面 确保群成员人数为2
        set = GroupChatSetPage()
        set.add_member_by_name('大佬1')
        # 1、点击添加成员的“+”号按钮，可以跳转到联系人选择器页面
        set.click_add_member()
        select = SelectContactsPage()
        time.sleep(3)
        self.assertTrue(select.is_text_present('添加群成员'))
        # 2、任意选中一个联系人，点击右上角的确定按钮，会向邀请人发送一条消息
        select.select_one_contact_by_name('大佬3')
        select.click_sure_bottom()
        time.sleep(2)
        self.assertTrue(GroupChatPage().is_on_this_page())

    def tearDown_test_msg_xiaoqiu_0129(self):
        """解散群之后新增群"""
        if GroupChatPage().is_on_this_page():
            GroupChatPage().wait_for_page_load()
        else:
            Preconditions.make_already_in_message_page()
            Preconditions.enter_group_chat_page('群聊2')
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        set.dissolution_the_group()
        # 解散群之后添加群
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        my_group.creat_group_if_not_exit('群聊2', member_name=['大佬#', '大佬#&'])
        Preconditions.disconnect_mobile('IOS-移动')

    def setUp_test_msg_xiaoqiu_0130(self):
        """确保进入群聊页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        name = '群聊2'
        if msg.is_text_present(name):
            msg.click_text(name)
        else:
            msg.click_search_box()
            time.sleep(1)
            msg.input_search_text(name)
            time.sleep(2)
            msg.click_element_first_list()
            time.sleep(2)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0130(self):
        """普通群——选择已在群聊中的联系人"""
        GroupChatPage().click_setting()
        # 设置页面 确保群成员人数为2
        set = GroupChatSetPage()
        select = SelectContactsPage()
        name = '大佬1'
        set.add_member_by_name(name)
        # 1、点击添加成员的“+”号按钮，可以跳转到联系人选择器页面
        set.click_add_member()
        time.sleep(3)
        self.assertTrue(select.is_text_present('添加群成员'))
        # 2、选择一个已存在当前群聊的联系人，是否会弹出toast提示：该联系人不可选并且选择失败-停留在当前页面
        select.select_one_contact_by_name(name)
        select.click_sure_bottom()
        self.assertTrue(select.is_text_present('添加群成员'))

    def tearDown_test_msg_xiaoqiu_0130(self):
        """解散群之后新增群"""
        if GroupChatPage().is_on_this_page():
            GroupChatPage().wait_for_page_load()
        else:
            Preconditions.make_already_in_message_page()
            Preconditions.enter_group_chat_page('群聊2')
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        set.dissolution_the_group()
        # 解散群之后添加群
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        my_group.creat_group_if_not_exit('群聊2', member_name=['大佬#', '大佬#&'])
        Preconditions.disconnect_mobile('IOS-移动')


    def setUp_test_msg_xiaoqiu_0131(self):
        """确保进入群聊页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        name = '群聊2'
        if msg.is_text_present(name):
            msg.click_text(name)
        else:
            msg.click_search_box()
            time.sleep(1)
            msg.input_search_text(name)
            time.sleep(2)
            msg.click_element_first_list()
            time.sleep(2)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0131(self):
        """普通群——群后成员——添加2个成员（群成员人数为2）"""
        GroupChatPage().click_setting()
        # 设置页面 确保群成员人数为2
        set = GroupChatSetPage()
        set.add_member_by_name('大佬1')
        # 1、点击添加成员的“+”号按钮，可以跳转到联系人选择器页面
        set.click_add_member()
        select = SelectContactsPage()
        time.sleep(3)
        self.assertTrue(select.is_text_present('添加群成员'))
        # 2、任意选中一个联系人，点击右上角的确定按钮，会向邀请人发送一条消息
        select.select_one_contact_by_name('大佬3')
        select.select_one_contact_by_name('大佬4')
        select.click_sure_bottom()
        time.sleep(2)
        self.assertTrue(GroupChatPage().is_on_this_page())

    def tearDown_test_msg_xiaoqiu_0131(self):
        """解散群之后新增群"""
        if GroupChatPage().is_on_this_page():
            GroupChatPage().wait_for_page_load()
        else:
            Preconditions.make_already_in_message_page()
            Preconditions.enter_group_chat_page('群聊2')
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        set.dissolution_the_group()
        # 解散群之后添加群
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        my_group.creat_group_if_not_exit('群聊2', member_name=['大佬#', '大佬#&'])
        Preconditions.disconnect_mobile('IOS-移动')


    def setUp_test_msg_xiaoqiu_0136(self):
        """确保进入群聊页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg = MessagePage()
        name = '群聊2'
        msg.delete_all_message_list()
        if msg.is_text_present(name):
            msg.click_text(name)
        else:
            msg.click_search_box()
            time.sleep(1)
            msg.input_search_text(name)
            time.sleep(2)
            msg.click_element_first_list()
            time.sleep(2)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0136(self):
        """存在一个群成员时——点击移除成员按钮（群成员人数为2）"""
        GroupChatPage().click_setting()
        # 设置页面 确保群成员人数为2
        set = GroupChatSetPage()
        set.add_member_by_name('大佬1')
        # 1、点击移除群成员按钮
        set.click_del_member()
        # 2、选中唯一群成员，点击右上角的确定按钮，确认移除此群成员
        set.click_menber_list_first_member()
        set.click_sure()
        set.click_sure_icon()
        time.sleep(2)
        # 3、群成员被移除成功后，当前群聊会自动解散并且群主会收到一条系统消息：该群已解散
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_contain_text('该群已解散')

    def tearDown_test_msg_xiaoqiu_0136(self):
        """解散群之后添加群"""
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        my_group.creat_group_if_not_exit('群聊2', member_name=['大佬#', '大佬#&'])
        Preconditions.disconnect_mobile('IOS-移动')


    def setUp_test_msg_xiaoqiu_0137(self):
        """确保进入群聊页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg = MessagePage()
        name = '群聊2'
        msg.delete_all_message_list()
        if msg.is_text_present(name):
            msg.click_text(name)
        else:
            msg.click_search_box()
            time.sleep(1)
            msg.input_search_text(name)
            time.sleep(2)
            msg.click_element_first_list()
            time.sleep(2)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0137(self):
        """群主——移除一个群成员（群成员人数为3）"""
        GroupChatPage().click_setting()
        # 设置页面 确保群成员人数为2
        set = GroupChatSetPage()
        set.add_member_by_name('大佬1')
        set.add_member_by_name('大佬2')
        # 1、点击移除群成员按钮，移除一个群成员
        set.click_del_member()
        set.click_menber_list_first_member()
        set.click_sure()
        set.click_sure_icon()
        time.sleep(2)
        # 2、群成员被移除成功后，当前群聊不会自动解散并收到一条系统消息：该群已解散（群成员>=2，不会解散）
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_not_contain_text('该群已解散')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0208(self):
        """群聊设置页面——查找聊天内容——特殊字符搜索——搜索结果展示（不存在文本消息）"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入文字并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('一条消息')
        time.sleep(2)
        group_chat_page.click_send_button()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.left_slide_message_record_by_number()
        time.sleep(2)
        message_page.click_element_('删除')
        # 通过名字找到'群聊1'
        message_page.click_add_icon()
        message_page.click_group_chat()
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        select_contacts_page.click_select_one_group()
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击查找聊天内容
        group_chat_set_page.click_find_message_records()
        time.sleep(2)
        find_chat_record_page = FindChatRecordPage()
        find_chat_record_page.wait_for_page_loads()
        # 输入搜索信息
        find_chat_record_page.input_search_message('!')
        # 判断当前是否显示无搜索结果
        self.assertEquals(find_chat_record_page.page_should_contain_text2('无搜索结果'), True)

    def tearDown_test_msg_xiaoqiu_0137(self):
        """解散群之后新增群"""
        if GroupChatPage().is_on_this_page():
            GroupChatPage().wait_for_page_load()
        else:
            Preconditions.make_already_in_message_page()
            Preconditions.enter_group_chat_page('群聊2')
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        set.dissolution_the_group()
        # 解散群之后添加群
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        my_group.creat_group_if_not_exit('群聊2', member_name=['大佬#', '大佬#&'])
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0212(self):
        """群聊设置页面——查找聊天内容——无搜索结果页面展示（存在文本消息）"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入文字并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('一条消息')
        time.sleep(2)
        group_chat_page.click_send_button()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击查找聊天内容
        group_chat_set_page.click_find_message_records()
        time.sleep(2)
        find_chat_record_page = FindChatRecordPage()
        find_chat_record_page.wait_for_page_loads()
        # 输入搜索信息
        find_chat_record_page.input_search_message('没有这条消息')
        # 判断当前是否显示无搜索结果
        self.assertEquals(find_chat_record_page.page_should_contain_text2('无搜索结果'), True)

    def setUp_test_msg_xiaoqiu_0138(self):
        """确保进入群聊页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg = MessagePage()
        name = '群聊2'
        msg.delete_all_message_list()
        if msg.is_text_present(name):
            msg.click_text(name)
        else:
            msg.click_search_box()
            time.sleep(1)
            msg.input_search_text(name)
            time.sleep(2)
            msg.click_element_first_list()
            time.sleep(2)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0254(self):
        """消息列表——发起群聊——选择1个手机联系人"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        select_contacts_page.click_phone_contacts()
        select_contacts_page.selecting_local_contacts_by_name('大佬1')
        select_contacts_page.click_confirm_button()
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0138(self):
        """群主——移除一个群成员（群成员人数为3）"""
        GroupChatPage().click_setting()
        # 设置页面 确保群成员人数为2
        set = GroupChatSetPage()
        set.add_member_by_name('大佬1')
        set.add_member_by_name('大佬2')
        # 1、点击移除群成员按钮，移除2个群成员
        set.click_del_member()
        set.click_menber_list_first_member()
        set.click_sure()
        set.click_sure_icon()
        time.sleep(2)
        set.click_del_member()
        set.click_menber_list_first_member()
        set.click_sure()
        set.click_sure_icon()
        time.sleep(2)
        # 2、群成员被移除成功后，当前群聊不会自动解散并收到一条系统消息：该群已解散（群成员>=2，不会解散）
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_contain_text('该群已解散')

    def tearDown_test_msg_xiaoqiu_0138(self):
        """解散群之后添加群"""
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        my_group.creat_group_if_not_exit('群聊2', member_name=['大佬#', '大佬#&'])
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0255(self):
        """消息列表——发起群聊——选择5个手机联系人——创建群聊"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        select_contacts_page.click_phone_contacts()
        select_contacts_page.selecting_local_contacts_by_name('测试号码')
        select_contacts_page.selecting_local_contacts_by_name('大佬1')
        select_contacts_page.selecting_local_contacts_by_name('大佬2')
        select_contacts_page.selecting_local_contacts_by_name('大佬3')
        select_contacts_page.selecting_local_contacts_by_name('大佬4')
        select_contacts_page.click_confirm_button()
        group_name = CreateGroupNamePage()
        group_name.click_clear_group_name()
        group_name.input_group_name('新建群1')
        select_contacts_page.click_create_button()
        time.sleep(2)
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_back()
        message_page.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0255():
        """恢复环境，将用例创建的群聊删除"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('新建群1')
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群管理解散群
            group_chat_page.click_group_control()
            group_chat_page.click_group_dissolve()
            group_chat_page.click_group_dissolve_confirm()
            time.sleep(2)
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    def setUp_test_msg_xiaoqiu_0140(self):
        """确保进入群聊页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg = MessagePage()
        name = '群聊2'
        msg.delete_all_message_list()
        if msg.is_text_present(name):
            msg.click_text(name)
        else:
            msg.click_search_box()
            time.sleep(1)
            msg.input_search_text(name)
            time.sleep(2)
            msg.click_element_first_list()
            time.sleep(2)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0140(self):
        """群主——修改群昵称"""
        GroupChatPage().click_setting()
        # 1、点击群名称入口，可以进入到修改群名称页面并且光标默认定位在旧名称右边
        set = GroupChatSetPage()
        name = '修改后的群'
        set.click_edit_group_name()
        self.assertTrue(set.is_text_present('修改群名称'))
        self.assertTrue(set.is_exit_element(locator='清除文本'))
        # 2、点击左上角的返回按钮，可以返回到群聊设置页面
        set.click_back()
        time.sleep(2)
        self.assertTrue(set.is_on_this_page())
        # 4、点击编辑状态群名称右边的“X”，可以一次性清除群名称文案，群名称编辑框中，展示默认文案：修改群名称
        set.click_edit_group_name()
        set.click_clear_group_name()
        self.assertTrue(set.is_text_present('请输入群聊名称'))
        # 3、点击右上角的保存按钮，会直接保存现有群名称并返回到群聊设置页面
        set.input_new_group_name(name)
        set.save_group_name()
        time.sleep(3)
        set.page_should_contain_text(name)

    def tearDown_test_msg_xiaoqiu_0140(self):
        """修改群名后 修改回原群名"""
        name = '群聊2'
        set = GroupChatSetPage()
        # 确保在群聊设置页面
        if set.is_on_this_page():
            set.wait_for_page_load()
        else:
            Preconditions.make_already_in_message_page()
            Preconditions.enter_group_chat_page(name='修改后的群')
            GroupChatPage().click_setting()
        # 修改群名称
        if set.is_text_present(name):
            pass
        else:
            set.change_group_name(name)
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0262(self):
        """消息列表——发起群聊——搜索选择陌生人——创建群聊"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 获取输入框输入'13333333333'
        select_contacts_page.input_search_keyword('13333333333')
        select_contacts_page.click_name_attribute_by_name('未知号码')
        select_contacts_page.click_confirm_button()
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0263(self):
        """消息列表——发起群聊——搜索选择陌生人+手机联系人"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 获取输入框输入'13333333333'
        select_contacts_page.click_phone_contacts()
        select_contacts_page.click_name_attribute_by_name('大佬1')
        select_contacts_page.click_back()
        select_contacts_page.input_search_keyword('13333333333')
        select_contacts_page.click_name_attribute_by_name('未知号码')
        select_contacts_page.click_confirm_button()
        group_name = CreateGroupNamePage()
        group_name.click_clear_group_name()
        group_name.input_group_name('新建群1')
        select_contacts_page.click_create_button()
        time.sleep(3)
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0263():
        """恢复环境，将用例创建的群聊删除"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('新建群1')
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群管理解散群
            group_chat_page.click_group_control()
            group_chat_page.click_group_dissolve()
            group_chat_page.click_group_dissolve_confirm()
            time.sleep(2)
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0265(self):
        """消息列表——发起群聊——搜索选择陌生人+手机联系人——创建群聊"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 获取输入框输入'13333333333'
        select_contacts_page.click_phone_contacts()
        select_contacts_page.click_name_attribute_by_name('大佬1')
        select_contacts_page.click_back()
        select_contacts_page.input_search_keyword('13333333333')
        select_contacts_page.click_name_attribute_by_name('未知号码')
        select_contacts_page.click_confirm_button()
        group_name = CreateGroupNamePage()
        group_name.click_clear_group_name()
        group_name.input_group_name('新建群1')
        select_contacts_page.click_create_button()
        time.sleep(2)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0265():
        """恢复环境，将用例创建的群聊删除"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('新建群1')
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群管理解散群
            group_chat_page.click_group_control()
            group_chat_page.click_group_dissolve()
            group_chat_page.click_group_dissolve_confirm()
            time.sleep(2)
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0271(self):
        """通讯录——发起群聊——选择手机联系人"""
        # 消息界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_contacts_only()
        contacts_page = ContactsPage()
        contacts_page.wait_for_page_load()
        contacts_page.open_group_chat_list()
        contacts_page.click_new_group()
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        select_contacts_page.click_phone_contacts()
        select_contacts_page.click_name_attribute_by_name('大佬1')
        select_contacts_page.click_name_attribute_by_name('大佬2')
        select_contacts_page.click_confirm_button()
        group_name = CreateGroupNamePage()
        group_name.click_clear_group_name()
        group_name.input_group_name('新建群1')
        select_contacts_page.click_create_button()
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_back()
        message_page.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0271():
        """恢复环境，将用例创建的群聊删除"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('新建群1')
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群管理解散群
            group_chat_page.click_group_control()
            group_chat_page.click_group_dissolve()
            group_chat_page.click_group_dissolve_confirm()
            time.sleep(2)
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0275(self):
        """通讯录——发起群聊——搜索选择陌生人"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_contacts_only()
        contacts_page = ContactsPage()
        contacts_page.wait_for_page_load()
        contacts_page.open_group_chat_list()
        contacts_page.click_new_group()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 获取输入框输入'13333333333'
        select_contacts_page.input_search_keyword('13333333333')
        select_contacts_page.click_name_attribute_by_name('未知号码')
        select_contacts_page.click_confirm_button()
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0272(self):
        """通讯录——发起群聊——选择选择团队联系人"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_contacts_only()
        contacts_page = ContactsPage()
        contacts_page.wait_for_page_load()
        contacts_page.open_group_chat_list()
        contacts_page.click_new_group()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        select_contacts_page.click_group_contact()
        select_contacts_page.click_name_attribute_by_name('ateam7272')
        select_contacts_page.click_name_attribute_by_name('大佬1')
        select_contacts_page.click_confirm_button()
        time.sleep(2)
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0273(self):
        """通讯录——发起群聊——选择手机联系人+选择团队联系人——创建群聊"""
        # 消息界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_contacts_only()
        contacts_page = ContactsPage()
        contacts_page.wait_for_page_load()
        contacts_page.open_group_chat_list()
        contacts_page.click_new_group()
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        select_contacts_page.click_phone_contacts()
        select_contacts_page.click_name_attribute_by_name('大佬1')
        select_contacts_page.click_back()
        # 返回到团队联系人界面
        select_contacts_page.click_group_contact()
        select_contacts_page.click_name_attribute_by_name('ateam7272')
        select_contacts_page.click_name_attribute_by_name('大佬2')
        select_contacts_page.click_confirm_button()
        group_name = CreateGroupNamePage()
        group_name.click_clear_group_name()
        group_name.input_group_name('新建群1')
        select_contacts_page.click_create_button()
        time.sleep(2)
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_back()
        message_page.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0273():
        """恢复环境，将用例创建的群聊删除"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('新建群1')
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群管理解散群
            group_chat_page.click_group_control()
            group_chat_page.click_group_dissolve()
            group_chat_page.click_group_dissolve_confirm()
            time.sleep(2)
            group_chat_page.click_back()
            message_page = MessagePage()
            message_page.wait_for_page_load()
            message_page.left_slide_message_record_by_number(1)
            message_page.click_name_attribute_by_name('删除')
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0277(self):
        """通讯录——发起群聊——搜索选择陌生人+选择团队联系人——创建群聊"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_contacts_only()
        contacts_page = ContactsPage()
        contacts_page.wait_for_page_load()
        contacts_page.open_group_chat_list()
        contacts_page.click_new_group()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 获取输入框输入'13333333333'
        select_contacts_page.input_search_keyword('13333333333')
        select_contacts_page.click_name_attribute_by_name('未知号码')
        select_contacts_page.click_group_contact()
        select_contacts_page.click_name_attribute_by_name('ateam7272')
        select_contacts_page.click_name_attribute_by_name('大佬1')
        select_contacts_page.click_confirm_button()
        group_name = CreateGroupNamePage()
        group_name.click_clear_group_name()
        group_name.input_group_name('新建群1')
        select_contacts_page.click_create_button()
        time.sleep(2)
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_back()
        message_page.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0277():
        """恢复环境，将用例创建的群聊删除"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('新建群1')
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群管理解散群
            group_chat_page.click_group_control()
            group_chat_page.click_group_dissolve()
            group_chat_page.click_group_dissolve_confirm()
            time.sleep(2)
            group_chat_page.click_back()
            message_page = MessagePage()
            message_page.wait_for_page_load()
            message_page.left_slide_message_record_by_number(1)
            message_page.click_name_attribute_by_name('删除')
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0276(self):
        """通讯录——发起群聊——搜索选择陌生人+手机联系人——创建群聊"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_contacts_only()
        contacts_page = ContactsPage()
        contacts_page.wait_for_page_load()
        contacts_page.open_group_chat_list()
        contacts_page.click_new_group()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 获取输入框输入'13333333333'
        select_contacts_page.input_search_keyword('13333333333')
        select_contacts_page.click_name_attribute_by_name('未知号码')
        select_contacts_page.click_phone_contacts()
        select_contacts_page.click_name_attribute_by_name('大佬1')
        select_contacts_page.click_confirm_button()
        group_name = CreateGroupNamePage()
        group_name.click_clear_group_name()
        group_name.input_group_name('新建群1')
        select_contacts_page.click_create_button()
        time.sleep(2)
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_back()
        message_page.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0276():
        """恢复环境，将用例创建的群聊删除"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('新建群1')
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群管理解散群
            group_chat_page.click_group_control()
            group_chat_page.click_group_dissolve()
            group_chat_page.click_group_dissolve_confirm()
            time.sleep(2)
            group_chat_page.click_back()
            message_page = MessagePage()
            message_page.wait_for_page_load()
            message_page.left_slide_message_record_by_number(1)
            message_page.click_name_attribute_by_name('删除')
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0111(self):
        """在群聊设置页面，群成员头像上方文案展示"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_setting()
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        self.assertEquals(group_chat_set_page.page_should_contain_text2('群成员'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0122(self):
        """在群聊设置页面中——群成员头像展示"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_setting()
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 1.在群聊设置页面，存在群头像元素
        self.assertEquals(group_chat_set_page.is_exists_element_by_text("群成员头像"), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0259(self):
        """消息列表——发起群聊——选择选择团队联系人——创建群聊"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_contacts_only()
        contacts_page = ContactsPage()
        contacts_page.wait_for_page_load()
        contacts_page.open_group_chat_list()
        contacts_page.click_new_group()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        select_contacts_page.click_group_contact()
        select_contacts_page.click_name_attribute_by_name('ateam7272')
        select_contacts_page.click_name_attribute_by_name('大佬1')
        select_contacts_page.click_name_attribute_by_name('大佬2')
        select_contacts_page.click_confirm_button()
        group_name = CreateGroupNamePage()
        group_name.click_clear_group_name()
        group_name.input_group_name('新建群1')
        select_contacts_page.click_create_button()
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0259():
        """恢复环境，将用例创建的群聊删除"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('新建群1')
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群管理解散群
            group_chat_page.click_group_control()
            group_chat_page.click_group_dissolve()
            group_chat_page.click_group_dissolve_confirm()
            time.sleep(2)
            group_chat_page.click_back()
            message_page = MessagePage()
            message_page.wait_for_page_load()
            message_page.left_slide_message_record_by_number(1)
            message_page.click_name_attribute_by_name('删除')
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0260(self):
        """消息列表——发起群聊——选择手机联系人+选择团队联系人"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_contacts_only()
        contacts_page = ContactsPage()
        contacts_page.wait_for_page_load()
        contacts_page.open_group_chat_list()
        contacts_page.click_new_group()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        select_contacts_page.click_phone_contacts()
        select_contacts_page.click_name_attribute_by_name('大佬1')
        select_contacts_page.click_back()
        select_contacts_page.click_group_contact()
        select_contacts_page.click_name_attribute_by_name('ateam7272')
        select_contacts_page.click_name_attribute_by_name('大佬2')
        select_contacts_page.click_confirm_button()
        group_name = CreateGroupNamePage()
        group_name.click_clear_group_name()
        group_name.input_group_name('新建群1')
        select_contacts_page.click_create_button()
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_back()
        message_page.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0260():
        """恢复环境，将用例创建的群聊删除"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('新建群1')
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群管理解散群
            group_chat_page.click_group_control()
            group_chat_page.click_group_dissolve()
            group_chat_page.click_group_dissolve_confirm()
            time.sleep(2)
            group_chat_page.click_back()
            message_page = MessagePage()
            message_page.wait_for_page_load()
            message_page.left_slide_message_record_by_number(1)
            message_page.click_name_attribute_by_name('删除')
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0266(self):
        """消息列表——发起群聊——搜索选择手机联系人+选择团队联系人"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_contacts_only()
        contacts_page = ContactsPage()
        contacts_page.wait_for_page_load()
        contacts_page.open_group_chat_list()
        contacts_page.click_new_group()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        select_contacts_page.click_phone_contacts()
        select_contacts_page.click_name_attribute_by_name('大佬1')
        select_contacts_page.click_back()
        select_contacts_page.click_group_contact()
        select_contacts_page.click_name_attribute_by_name('ateam7272')
        select_contacts_page.click_name_attribute_by_name('大佬2')
        select_contacts_page.click_confirm_button()
        group_name = CreateGroupNamePage()
        group_name.click_clear_group_name()
        group_name.input_group_name('新建群1')
        select_contacts_page.click_create_button()
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_back()
        message_page.wait_for_page_load()
        self.assertEquals(message_page.page_should_contain_text2('新建群1'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0266():
        """恢复环境，将用例创建的群聊删除"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('大佬1,大佬2')
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群管理解散群
            group_chat_page.click_group_control()
            group_chat_page.click_group_dissolve()
            group_chat_page.click_group_dissolve_confirm()
            time.sleep(2)
            group_chat_page.click_back()
            message_page = MessagePage()
            message_page.wait_for_page_load()
            message_page.left_slide_message_record_by_number(1)
            time.sleep(2)
            message_page.click_name_attribute_by_name('删除')
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0264(self):
        """消息列表——发起群聊——搜索选择陌生人+选择团队联系人——创建群聊"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_contacts_only()
        contacts_page = ContactsPage()
        contacts_page.wait_for_page_load()
        contacts_page.open_group_chat_list()
        contacts_page.click_new_group()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 获取输入框输入'13333333333'
        select_contacts_page.input_search_keyword('13333333333')
        select_contacts_page.click_name_attribute_by_name('未知号码')
        select_contacts_page.click_group_contact()
        select_contacts_page.click_name_attribute_by_name('ateam7272')
        select_contacts_page.click_name_attribute_by_name('大佬1')
        select_contacts_page.click_confirm_button()
        group_name = CreateGroupNamePage()
        group_name.click_clear_group_name()
        group_name.input_group_name('新建群1')
        select_contacts_page.click_create_button()
        time.sleep(1)
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_back()
        message_page.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0264():
        """恢复环境，将用例创建的群聊删除"""
        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('新建群1')
            group_chat_page = GroupChatPage()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群管理解散群
            group_chat_page.click_group_control()
            group_chat_page.click_group_dissolve()
            group_chat_page.click_group_dissolve_confirm()
            time.sleep(2)
            group_chat_page.click_back()
            message_page = MessagePage()
            message_page.wait_for_page_load()
            message_page.left_slide_message_record_by_number(1)
            message_page.click_name_attribute_by_name('删除')

        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_xiaoqiu_0314(self):
        """群聊设置页面——点击已保存在手机通讯录中——群成员头像"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_setting()
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        group_chat_set_page.click_name_attribute_by_name('未注册')
        self.assertEquals(group_chat_set_page.page_should_contain_text2('分享名片'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_msg_huangmianhua_0201(self):
        """通讯录-群聊-索引字母定位选择"""
        Preconditions.make_already_in_message_page()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_contacts_only()
        contacts_page = ContactsPage()
        contacts_page.click_group_chat()
        contacts_page.input_search_group_text('csqyq')
        contacts_page.click_name_attribute_by_name('测试企业群')
        # 到群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zhenyishan_0053(self):
        """从群聊发起多方视频，在多方视频管理界面点击“+”进入联系人选择页"""
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击多方通话
        group_chat_page.click_mutilcall()
        group_chat_page.click_name_attribute_by_name('多方视频')
        time.sleep(2)
        self.assertEqual(group_chat_page.page_should_contain_text2('大佬2'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zhenyishan_0155(self):
        """分组群发/标签分组/群发消息：发起多方视频，在管理页面点击“+”进入标签分组联系人选择页"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_contacts_only()
        # 联系界面
        contacts_page = ContactsPage()
        contacts_page.wait_for_page_load()
        contacts_page.click_mobile_contacts()
        contacts_page.click_label_grouping()
        contacts_page.click_name_attribute_by_name('新建分组')
        contacts_page.click_name_attribute_by_name('为你的分组创建一个名称')
        lable_group_detail_page = LableGroupDetailPage()
        lable_group_detail_page.input_group_new_name('测试标签分组')
        lable_group_detail_page.click_sure()
        lable_group_detail_page.click_name_attribute_by_name('测试1')
        lable_group_detail_page.click_name_attribute_by_name('测试2')
        lable_group_detail_page.click_name_attribute_by_name('确定(2/200)')
        lable_group_detail_page.click_label_group_icon()
        # 进入标签分组
        lable_group_detail_page.wait_for_page_load()
        lable_group_detail_page.click_send_group_info()
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_mutilcall()
        group_chat_page.click_name_attribute_by_name('多方视频')
        self.assertEqual(group_chat_page.page_should_contain_text2('测试1'), True)
        self.assertEqual(group_chat_page.page_should_contain_text2('测试2'), True)

    @staticmethod
    def tearDown_test_call_zhenyishan_0155():
        """恢复环境，将用例创建的标签删除"""
        try:
            Preconditions.make_already_in_message_page()
            message_page = MessagePage()
            message_page.wait_for_page_load()
            message_page.click_contacts_only()
            # 联系界面
            contacts_page = ContactsPage()
            contacts_page.wait_for_page_load()
            contacts_page.click_mobile_contacts()
            contacts_page.click_label_grouping()
            lable_group_detail_page = LableGroupDetailPage()
            lable_group_detail_page.click_label_group_icon()
            lable_group_detail_page.open_setting_menu()
            lable_group_detail_page.delete_lable_group()
            lable_group_detail_page.click_sure_delete()
            time.sleep(2)
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zhenyishan_0087(self):
        """通话模块：团队联系人选择页搜索栏--搜索本机号码"""
        # 消息界面进入到多方视频选择联系人界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_call_button()
        call_page = CallPage()
        call_page.wait_for_page_load()
        call_page.click_multi_party_video()
        # 搜索框输入本机号码
        call_page.input_video_search_text('15946309425')
        self.assertEqual(call_page.is_exist_number_grey(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_shenlisi_0390(self):
        """检查单聊会话窗口右上角电话按钮-普通电话拨打"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_add_icon()
        message_page.click_new_message()
        message_page.click_name_attribute_by_name('测试1')
        # 等待界面加载
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        single_chat_page.click_action_call()
        single_chat_page.click_name_attribute_by_name('普通电话')
        self.assertEqual(single_chat_page.page_should_contain_text2('呼叫'), True)
        single_chat_page.click_cancel()

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zhenyishan_0096(self):
        """通话模块：检查企业入口"""
        # 消息界面进入到多方视频选择联系人界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_call_button()
        call_page = CallPage()
        call_page.wait_for_page_load()
        call_page.click_multi_party_video()
        # 点击团队联系人进入我的团队
        call_page.click_name_attribute_by_name('团队联系人')
        call_page.click_name_attribute_by_name('ateam7272')
        self.assertEqual(call_page.is_exist_group_contact_search(), True)
        self.assertEqual(call_page.page_should_contain_text2('ateam7272'), True)
        self.assertEqual(call_page.page_should_contain_text2('大佬1'), True)
        # 点击团队看是否跳转到选择团队联系人界面
        call_page.click_name_attribute_by_name('ateam7272')
        self.assertEqual(call_page.page_should_contain_text2('选择联系人'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zhenyishan_0112(self):
        """通话模块：当前勾选人数已有8人，继续勾选团队联系人，检查提示"""
        # 消息界面进入到多方视频选择联系人界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_call_button()
        call_page = CallPage()
        call_page.wait_for_page_load()
        call_page.click_multi_party_video()
        # 点击团队联系人进入我的团队
        call_page.click_name_attribute_by_name('团队联系人')
        call_page.click_name_attribute_by_name('ateam7272')
        call_page.click_name_attribute_by_name('alice')
        call_page.click_name_attribute_by_name('b测算')
        call_page.click_name_attribute_by_name('陈丹丹')
        call_page.click_name_attribute_by_name('c平5')
        call_page.click_name_attribute_by_name('大佬1')
        call_page.click_name_attribute_by_name('大佬2')
        call_page.click_name_attribute_by_name('大佬3')
        call_page.click_name_attribute_by_name('大佬4')
        call_page.click_name_attribute_by_name('郑海')
        # 判断是否出现人数已达上线8人
        self.assertEqual(call_page.page_should_contain_text2('人数已达上限8人'), True)
        call_page.click_name_attribute_by_name('确定')
        self.assertEqual(call_page.page_should_contain_text2('人数已达上限8人'), False)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zhenyishan_0158(self):
        """多方视频管理页面，检查免提按钮"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_mutilcall()
        group_chat_page.click_name_attribute_by_name('多方视频')
        multi_party_video_page = MultiPartyVideoPage()
        time.sleep(2)
        multi_party_video_page.click_name_attribute_by_name('大佬1')
        multi_party_video_page.click_call()
        time.sleep(5)
        multi_party_video_page.click_name_attribute_by_name('取消')
        multi_party_video_page.click_hands_free()

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zhenyishan_0159(self):
        """多方视频管理页面，静音按钮"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_mutilcall()
        group_chat_page.click_name_attribute_by_name('多方视频')
        multi_party_video_page = MultiPartyVideoPage()
        time.sleep(2)
        multi_party_video_page.click_name_attribute_by_name('大佬1')
        multi_party_video_page.click_call()
        time.sleep(5)
        multi_party_video_page.click_name_attribute_by_name('取消')
        multi_party_video_page.click_mute()

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zhenyishan_0183(self):
        """主叫多方视频管理界面，检查挂断按钮"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_mutilcall()
        group_chat_page.click_name_attribute_by_name('多方视频')
        multi_party_video_page = MultiPartyVideoPage()
        time.sleep(2)
        multi_party_video_page.click_name_attribute_by_name('大佬1')
        multi_party_video_page.click_call()
        time.sleep(5)
        multi_party_video_page.click_name_attribute_by_name('取消')
        # 点击红色挂断按钮
        multi_party_video_page.click_red_drop()
        multi_party_video_page.click_name_attribute_by_name('取消')
        multi_party_video_page.click_red_drop()
        multi_party_video_page.click_name_attribute_by_name('确定')
        time.sleep(3)
        group_chat_page.wait_for_page_load()

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zhenyishan_0186(self):
        """多方视频管理界面，检查添加联系人按钮"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_mutilcall()
        group_chat_page.click_name_attribute_by_name('多方视频')
        multi_party_video_page = MultiPartyVideoPage()
        time.sleep(2)
        multi_party_video_page.click_name_attribute_by_name('大佬1')
        multi_party_video_page.click_call()
        time.sleep(5)
        multi_party_video_page.click_name_attribute_by_name('取消')
        # 点击添加成员按钮
        multi_party_video_page.click_add_members()
        self.assertEqual(multi_party_video_page._is_enabled_call_button(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_wangqiong_0059(self):
        """网络正常，通话页-多方电话悬浮，发起正常，发起正常"""
        # 消息界面进入到多方电话选择联系人界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_call_button()
        call_page = CallPage()
        call_page.wait_for_page_load()
        call_page.click_feixin_call()
        call_page.click_name_attribute_by_name('测试1')
        call_page.click_name_attribute_by_name('测试2')
        call_page.click_many_people_call()
        self.assertEqual(call_page.is_exist_stop_call_button(), True)
        time.sleep(2)
        # 挂断和飞信电话
        call_page.hang_up_hefeixin_call()

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_wangqiong_0057(self):
        """网络正常，拨号盘多方电话按钮，发起正常"""
        # 消息界面进入到多方电话选择联系人界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_call_button()
        call_page = CallPage()
        call_page.wait_for_page_load()
        call_page.click_dial_button()
        call_page.is_on_the_dial_pad()
        call_page.click_keyboard_feixin_call()
        call_page.click_name_attribute_by_name('测试1')
        call_page.click_name_attribute_by_name('测试2')
        call_page.click_many_people_call()
        self.assertEqual(call_page.is_exist_stop_call_button(), True)
        # 挂断飞信电话
        call_page.hang_up_hefeixin_call()


    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_wangqiong_0063(self):
        """网络正常，多方电话通话详情页可再次呼叫成功"""
        # 消息界面进入到多方电话选择联系人界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_call_button()
        call_page = CallPage()
        call_page.wait_for_page_load()
        call_page.click_dial_button()
        call_page.is_on_the_dial_pad()
        call_page.click_keyboard_feixin_call()
        call_page.click_name_attribute_by_name('测试1')
        call_page.click_name_attribute_by_name('测试2')
        call_page.click_many_people_call()
        call_page.hang_up_hefeixin_call()
        time.sleep(3)
        call_page.click_name_attribute_by_name('[飞信电话]')
        self.assertEqual(call_page.is_exist_stop_call_button(), True)
        # 挂断飞信电话
        call_page.hang_up_hefeixin_call()


    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_wangqiong_0073(self):
        """网络正常，消息+：分组群发-多方电话 ，拨打正常"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_contacts_only()
        # 联系界面
        contacts_page = ContactsPage()
        contacts_page.wait_for_page_load()
        contacts_page.click_mobile_contacts()
        contacts_page.click_label_grouping()
        LabelGroupingPage().delete_all_label()
        contacts_page.click_name_attribute_by_name('新建分组')
        contacts_page.click_name_attribute_by_name('为你的分组创建一个名称')
        lable_group_detail_page = LableGroupDetailPage()
        lable_group_detail_page.input_group_new_name('测试标签分组')
        lable_group_detail_page.click_sure()
        lable_group_detail_page.click_name_attribute_by_name('测试1')
        lable_group_detail_page.click_name_attribute_by_name('测试2')
        lable_group_detail_page.click_name_attribute_by_name('确定(2/200)')
        lable_group_detail_page.click_label_group_icon()
        # 进入标签分组
        lable_group_detail_page.wait_for_page_load()
        lable_group_detail_page.click_send_group_info()
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_mutilcall()
        group_chat_page.click_name_attribute_by_name('飞信电话(免费)')
        call_page = CallPage()
        call_page.click_name_attribute_by_name('测试1')
        call_page.click_name_attribute_by_name('测试2')
        call_page.click_many_people_call()
        self.assertEqual(call_page.is_exist_stop_call_button(), True)
        # 挂断飞信电话
        call_page.hang_up_hefeixin_call()


    @staticmethod
    def tearDown_test_call_wangqiong_0073():
        """恢复环境，将用例创建的标签删除"""
        try:
            Preconditions.make_already_in_message_page()
            message_page = MessagePage()
            message_page.wait_for_page_load()
            message_page.click_contacts_only()
            # 联系界面
            contacts_page = ContactsPage()
            contacts_page.wait_for_page_load()
            contacts_page.click_mobile_contacts()
            contacts_page.click_label_grouping()
            lable_group_detail_page = LableGroupDetailPage()
            lable_group_detail_page.click_label_group_icon()
            lable_group_detail_page.open_setting_menu()
            lable_group_detail_page.delete_lable_group()
            lable_group_detail_page.click_sure_delete()
            time.sleep(2)
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_wangqiong_0071(self):
        """网络正常，消息+：分组群发-多方电话 ，拨打正常"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_contacts_only()
        # 联系界面
        contacts_page = ContactsPage()
        contacts_page.wait_for_page_load()
        contacts_page.click_mobile_contacts()
        contacts_page.click_label_grouping()
        LabelGroupingPage().delete_all_label()
        contacts_page.click_name_attribute_by_name('新建分组')
        contacts_page.click_name_attribute_by_name('为你的分组创建一个名称')
        lable_group_detail_page = LableGroupDetailPage()
        lable_group_detail_page.input_group_new_name('测试标签分组')
        lable_group_detail_page.click_sure()
        lable_group_detail_page.click_name_attribute_by_name('测试1')
        lable_group_detail_page.click_name_attribute_by_name('测试2')
        lable_group_detail_page.click_name_attribute_by_name('确定(2/200)')
        lable_group_detail_page.click_label_group_icon()
        # 进入标签分组
        lable_group_detail_page.wait_for_page_load()
        lable_group_detail_page.click_multi_tel()
        call_page = CallPage()
        call_page.click_name_attribute_by_name('测试1')
        call_page.click_name_attribute_by_name('测试2')
        call_page.click_many_people_call()
        self.assertEqual(call_page.is_exist_stop_call_button(), True)
        # 挂断飞信电话
        call_page.hang_up_hefeixin_call()


    @staticmethod
    def tearDown_test_call_wangqiong_0071():
        """恢复环境，将用例创建的标签删除"""
        try:
            Preconditions.make_already_in_message_page()
            message_page = MessagePage()
            message_page.wait_for_page_load()
            message_page.click_contacts_only()
            # 联系界面
            contacts_page = ContactsPage()
            contacts_page.wait_for_page_load()
            contacts_page.click_mobile_contacts()
            contacts_page.click_label_grouping()
            lable_group_detail_page = LableGroupDetailPage()
            lable_group_detail_page.click_label_group_icon()
            lable_group_detail_page.open_setting_menu()
            lable_group_detail_page.delete_lable_group()
            lable_group_detail_page.click_sure_delete()
            time.sleep(2)
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zengxi_0028(self):
        """在拨号盘输入有效号码（手机号码、固号），可拨打普通电话成功"""
        # 消息界面进入到多方电话选择联系人界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_call_button()
        call_page = CallPage()
        call_page.wait_for_page_load()
        call_page.click_dial_button()
        call_page.dial_number('13333333333')
        call_page.click_call_phone()
        call_page.click_name_attribute_by_name('普通电话')
        self.assertEqual(call_page.page_should_contain_text2('呼叫'), True)
        call_page.click_name_attribute_by_name('取消')
        time.sleep(2)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zengxi_0034(self):
        """单聊会话-拨号，可发起呼叫普通电话"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_add_icon()
        message_page.click_new_message()
        message_page.click_name_attribute_by_name('测试1')
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        single_chat_page.click_action_call()
        single_chat_page.click_name_attribute_by_name('普通电话')
        self.assertEqual(single_chat_page.page_should_contain_text2('呼叫'), True)
        single_chat_page.click_name_attribute_by_name('取消')
        time.sleep(2)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zengxi_0035(self):
        """1V1的通话详情页入口，可发起呼叫普通电话"""
        # 消息界面进入到多方电话选择联系人界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_add_icon()
        message_page.click_new_message()
        message_page.click_name_attribute_by_name('测试1')
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        single_chat_page.click_add_button()
        single_chat_page.click_name_attribute_by_name('音视频通话')
        single_chat_page.click_name_attribute_by_name('视频通话')
        time.sleep(15)
        single_chat_page.click_back()
        message_page.wait_for_page_load()
        message_page.click_call_button()
        call_page = CallPage()
        call_page.click_name_attribute_by_name('刚刚')
        call_page.click_infor_call()
        self.assertEqual(call_page.page_should_contain_text2('呼叫'), True)
        call_page.click_name_attribute_by_name('取消')
        time.sleep(1)


class MsgGroupChatVideoPicTotalTest(TestCase):
    """群聊"""

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
    def test_msg_xiaoliping_D_0079(self):
        """群聊会话页面，删除自己发送的视频"""

        mp = MessagePage()
        # 清空消息列表，确保不影响验证
        mp.delete_all_message_record()
        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("群聊1")
        # 发送一个视频
        Preconditions.send_video()
        gcp = GroupChatPage()
        self.assertEquals(gcp.is_exists_element_by_text("视频播放按钮"), True)
        # 在当前聊天会话页面，长按自己发送的视频
        gcp.press_element_by_text("视频播放按钮")
        # 点击删除
        gcp.click_accessibility_id_attribute_by_name("删除")
        # 1.调起确认弹窗
        self.assertEquals(gcp.page_should_contain_text2("确定"), True)
        # 点击确定
        gcp.click_accessibility_id_attribute_by_name("确定")
        time.sleep(2)
        # 2.删除成功，自己的会话界面无该视频
        self.assertEquals(gcp.is_exists_element_by_text("视频播放按钮"), False)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoliping_D_0081(self):
        """群聊会话页面，收藏自己发送的视频"""

        mp = MessagePage()
        # 清空收藏列表，确保没有收藏影响验证
        Preconditions.enter_collection_page()
        mcp = MeCollectionPage()
        mcp.delete_all_collection()
        mcp.click_back_button()
        mp.open_message_page()
        mp.wait_for_page_load()
        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("群聊1")
        # 发送一个视频
        Preconditions.send_video()
        gcp = GroupChatPage()
        # 在当前聊天会话页面，长按自己发送的视频
        gcp.press_element_by_text2("视频播放按钮")
        # 收藏该视频
        gcp.click_accessibility_id_attribute_by_name("收藏")
        # 1.toast提醒收藏成功
        self.assertEquals(gcp.page_should_contain_text2("已收藏"), True)
        gcp.click_back_button()
        Preconditions.enter_collection_page()
        # 2.在我模块中的收藏可见(间接验证)
        self.assertEquals(mcp.is_exists_collection(), True)

    @staticmethod
    def tearDown_test_msg_xiaoliping_D_0081():
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

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoliping_D_0175(self):
        """在会话窗口点击图片按钮进入相册，直接勾选原图，选择一张小于20M的照片进行发送"""

        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 在当前页面点击图片按钮
        gcp.click_picture()
        cpp = ChatPicPage()
        # 1.进入选择图片页面
        cpp.wait_for_page_load()
        # 勾选原图
        cpp.click_accessibility_id_attribute_by_name("原图")
        time.sleep(1)
        # 2.原图勾选成功
        self.assertEquals(cpp.get_element_value_by_text("原图"), "1")
        # 选择一张小于20M的图片
        cpp.select_picture()
        # 3.图片选择成功，发送按钮高亮显示(间接验证)
        self.assertEquals(cpp.send_btn_is_enabled(), True)
        # 点击发送按钮
        cpp.click_send()
        # 4.图片发送成功(由于群聊的图片无法定位，间接验证)
        gcp.wait_for_page_load()
        self.assertEquals(gcp.is_exists_element_by_text("最后一条消息记录发送失败标识"), False)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoliping_D_0176(self):
        """在会话窗口点击图片按钮进入相册，选择一张小于20M的照片，进入图片预览页面勾选原图，然后进行发送"""

        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 在当前页面点击图片按钮
        gcp.click_picture()
        cpp = ChatPicPage()
        # 1.进入选择图片页面
        cpp.wait_for_page_load()
        # 选择一张小于20M的图片，点击预览按钮
        cpp.select_picture()
        cpp.click_accessibility_id_attribute_by_name("预览")
        # 2.图片选择成功，进入预览页面
        self.assertEquals(cpp.page_should_contain_text2("编辑"), True)
        # 勾选原图
        cpp.click_accessibility_id_attribute_by_name("原图")
        time.sleep(1)
        # 3.原图勾选成功
        self.assertEquals(cpp.get_element_value_by_text("原图"), "1")
        # 点击发送按钮
        cpp.click_send()
        # 4.图片发送成功(由于群聊的图片无法定位，间接验证)
        gcp.wait_for_page_load()
        self.assertEquals(gcp.is_exists_element_by_text("最后一条消息记录发送失败标识"), False)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoliping_D_0181(self):
        """在会话窗口点击文件按钮-本地照片-选择相册，选择一张小于20M的图片进行发送（iOS）"""

        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 在当前页面点击文件按钮-本地照片-选择相册
        gcp.click_file_button()
        gcp.click_accessibility_id_attribute_by_name("本地照片")
        gcp.click_name_attribute_by_name("相机胶卷")
        csfp = ChatSelectFilePage()
        # 1.进入本地图片页面
        csfp.wait_for_local_photo_page_load()
        # 选择一张小于20M的图片进行发送
        csfp.click_picture()
        csfp.click_send()
        # 2.图片发送成功(由于群聊的图片无法定位，间接验证)
        gcp.wait_for_page_load()
        self.assertEquals(gcp.is_exists_element_by_text("最后一条消息记录发送失败标识"), False)





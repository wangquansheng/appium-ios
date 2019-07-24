import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import ChatPhotoPage
from pages import ChatPicPage
from pages import ChatSelectLocalFilePage
from pages import ChatWindowPage
from pages import ContactDetailsPage
from pages import ContactsPage
from pages import GroupChatPage
from pages import GroupChatSetPage
from pages import GroupListPage
from pages import GroupListSearchPage
from pages import MeCollectionPage
from pages import MePage
from pages import MessagePage
from pages import MultiPartyVideoPage
from pages import SelectContactsPage
from pages import SelectOneGroupPage
from pages.call.multipartycall import MultipartyCallPage
from preconditions.BasePreconditions import WorkbenchPreconditions


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
    def send_file_by_type(file_type):
        """发送指定类型文件"""

        cwp = ChatWindowPage()
        cwp.click_file()
        cwp.click_accessibility_id_attribute_by_name("我收到的文件")
        cslfp = ChatSelectLocalFilePage()
        cslfp.click_file_by_type(file_type)
        cslfp.click_send_button()
        time.sleep(5)


class EnterpriseGroupTotalTest(TestCase):
    """企业群"""

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

        # 导入企业群
        fail_time3 = 0
        flag3 = False
        while fail_time3 < 5:
            try:
                Preconditions.make_already_in_message_page()
                group_chats = ["中文测试企业群", "test_enterprise_group", "好好 企业群", "198891", "*#@"]
                Preconditions.create_enterprise_group_if_not_exists(group_chats)
                flag3 = True
            except:
                fail_time3 += 1
            if flag3:
                break

    def default_setUp(self):

        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0024(self):
        """企业群/党群在消息列表内展示——最新消息时间（修改手机时间可以测试）"""

        # 进入企业群聊天会话页面
        Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        # 发送文本
        gcp.input_text_message("123")
        gcp.click_send_button()
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 1.1分钟内为“刚刚”，正常展示
        self.assertEquals(mp.get_first_message_send_time("刚刚"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0025(self):
        """企业群/党群在消息列表内展示——最新消息时间（修改手机时间可以测试）"""

        # 进入企业群聊天会话页面
        Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        # 发送文本
        gcp.input_text_message("123")
        gcp.click_send_button()
        # 等待
        time.sleep(59)
        current_mobile().launch_app()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 1.分钟加1后显示为“X时：X分”，正常展示
        self.assertEquals(mp.get_first_message_send_time(":"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0031(self):
        """企业群/党群在消息列表内展示——最新消息展示——文字及表情"""

        # 进入企业群聊天会话页面
        group_name = Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        # 发送长文本
        text1= "啊" * 20
        gcp.input_text_message(text1)
        gcp.click_send_button()
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 1.文字及表情消息展示具体内容:仅展示一行（超长后加“...”），正常展示(由于“...”无法抓取，采用间接验证)
        self.assertEquals(mp.is_first_message_content(text1), True)
        mp.click_accessibility_id_attribute_by_name(group_name)
        gcp.wait_for_page_load()
        # 发送长表情文本
        text2 = "[微笑1]" * 20
        gcp.input_text_message(text2)
        gcp.click_send_button()
        gcp.click_back_button()
        mp.wait_for_page_load()
        self.assertEquals(mp.is_first_message_content(text2), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0046(self):
        """企业群/党群在消息列表内展示——免打扰"""

        # 进入企业群聊天会话页面
        group_name = Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        # 发送文本，确保消息列表有记录
        gcp.input_text_message("123")
        gcp.click_send_button()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        # 滑动页面，刷新免打扰按钮
        gcs.page_up()
        # 确保群消息免打扰开关打开
        if gcs.get_switch_undisturb_value() == "0":
            gcs.click_switch_undisturb()
            time.sleep(3)
        gcs.click_back_button(2)
        mp = MessagePage()
        mp.wait_for_page_load()
        # 1.免打扰时右下角免打扰标识，正常展示
        self.assertEquals(mp.is_exists_no_disturb_icon_by_message_name(group_name), True)

    @staticmethod
    def tearDown_test_msg_huangmianhua_0046():
        """恢复环境"""

        try:
            fail_time = 0
            while fail_time < 5:
                try:
                    Preconditions.make_already_in_message_page()
                    # 进入企业群聊天会话页面
                    Preconditions.enter_enterprise_group_chat_page()
                    gcp = GroupChatPage()
                    gcp.click_setting()
                    gcs = GroupChatSetPage()
                    gcs.wait_for_page_load()
                    # 滑动页面，刷新免打扰按钮
                    gcs.page_up()
                    # 确保群消息免打扰开关关闭
                    if gcs.get_switch_undisturb_value() == "1":
                        gcs.click_switch_undisturb()
                        time.sleep(3)
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0048(self):
        """企业群/党群在消息列表内展示——长按/左划出功能选择弹窗——iOS（左划）"""

        # 进入企业群聊天会话页面
        group_name = Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        # 发送文本，确保消息列表有记录
        gcp.input_text_message("123")
        gcp.click_send_button()
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 1.滑动展示效果:样式是否正常,右划收回；置顶:已置顶则显示“取消置顶”；删除；全部正常
        mp.left_slide_message_record_by_number()
        self.assertEquals(mp.is_exists_accessibility_id_attribute_by_name("删除"), True)
        # 确保已置顶
        if not mp.is_exists_accessibility_id_attribute_by_name("取消置顶"):
            mp.click_element_by_name("置顶")
            mp.left_slide_message_record_by_number()
        self.assertEquals(mp.is_exists_accessibility_id_attribute_by_name("取消置顶"), True)
        mp.click_element_by_name("删除")
        self.assertEquals(mp.is_exists_accessibility_id_attribute_by_name(group_name), False)

    @staticmethod
    def tearDown_test_msg_huangmianhua_0048():
        """恢复环境"""

        try:
            fail_time = 0
            while fail_time < 5:
                try:
                    Preconditions.make_already_in_message_page()
                    # 进入企业群聊天会话页面
                    Preconditions.enter_enterprise_group_chat_page()
                    gcp = GroupChatPage()
                    gcp.click_setting()
                    gcs = GroupChatSetPage()
                    gcs.wait_for_page_load()
                    # 滑动页面，刷新置顶聊天按钮
                    gcs.page_up()
                    # 确保置顶聊天开关关闭
                    if gcs.get_switch_top_value() == "1":
                        gcs.click_switch_top()
                        time.sleep(3)
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0078(self):
        """消息列表——发起群聊——选择一个群——模糊搜索存在的企业群和党群"""

        mp = MessagePage()
        # 点击右上角的+号，发起群聊
        mp.click_add_icon()
        mp.click_group_chat()
        scg = SelectContactsPage()
        # 1.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击选择一个群
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 2.点击选择一个群，可以进入到群聊列表展示页面
        sog.wait_for_page_load()
        sog.click_search_box()
        # 中文模糊搜索企业群和党群
        sog.input_search_keyword("中文测试")
        # 3.中文模糊搜索企业群和党群，可以匹配展示搜索结果（有相应“企”或党徽标识）
        self.assertEquals(sog.page_should_contain_text2("中文测试企业群"), True)
        self.assertEquals(sog.is_exists_enterprise_group_icon(), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0079(self):
        """消息列表——发起群聊——选择一个群——模糊搜索不存在的企业群和党群"""

        mp = MessagePage()
        # 点击右上角的+号，发起群聊
        mp.click_add_icon()
        mp.click_group_chat()
        scg = SelectContactsPage()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击选择一个群
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待选择一个群页面加载
        sog.wait_for_page_load()
        sog.click_search_box()
        # 中文模糊搜索企业群和党群
        sog.input_search_keyword("不存在的群")
        # 1.中文模糊搜索企业群和党群，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(sog.page_should_contain_text2("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0080(self):
        """群聊列表展示页面——中文精确搜索存在的企业群和党群"""

        mp = MessagePage()
        # 点击右上角的+号，发起群聊
        mp.click_add_icon()
        mp.click_group_chat()
        scg = SelectContactsPage()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击选择一个群
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待选择一个群页面加载
        sog.wait_for_page_load()
        sog.click_search_box()
        # 中文精确搜索企业群和党群
        search_name = "中文测试企业群"
        sog.input_search_keyword(search_name)
        # 1.中文精确搜索企业群和党群，可以匹配展示搜索结果（有相应“企”或党徽标识）
        self.assertEquals(sog.page_should_contain_text2(search_name), True)
        self.assertEquals(sog.is_exists_enterprise_group_icon(), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0081(self):
        """群聊列表展示页面——中文精确搜索不存在的企业群和党群"""

        mp = MessagePage()
        # 点击右上角的+号，发起群聊
        mp.click_add_icon()
        mp.click_group_chat()
        scg = SelectContactsPage()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击选择一个群
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待选择一个群页面加载
        sog.wait_for_page_load()
        sog.click_search_box()
        # 中文精确搜索企业群和党群
        sog.input_search_keyword("不存在企业群")
        # 1.中文精确搜索企业群和党群，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(sog.page_should_contain_text2("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0082(self):
        """群聊列表展示页面——英文精确搜索存在的企业群和党群"""

        mp = MessagePage()
        # 点击右上角的+号，发起群聊
        mp.click_add_icon()
        mp.click_group_chat()
        scg = SelectContactsPage()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击选择一个群
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待选择一个群页面加载
        sog.wait_for_page_load()
        sog.click_search_box()
        # 英文精确搜索企业群和党群
        search_name = "test_enterprise_group"
        sog.input_search_keyword(search_name)
        # 1.英文精确搜索企业群和党群，可以匹配展示搜索结果（有相应“企”或党徽标识）
        self.assertEquals(sog.page_should_contain_text2(search_name), True)
        self.assertEquals(sog.is_exists_enterprise_group_icon(), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0083(self):
        """群聊列表展示页面——英文精确搜索不存在的企业群和党群"""

        mp = MessagePage()
        # 点击右上角的+号，发起群聊
        mp.click_add_icon()
        mp.click_group_chat()
        scg = SelectContactsPage()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击选择一个群
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待选择一个群页面加载
        sog.wait_for_page_load()
        sog.click_search_box()
        # 英文精确搜索企业群和党群
        search_name = "test_no_exists"
        sog.input_search_keyword(search_name)
        # 1.英文精确搜索企业群和党群，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(sog.page_should_contain_text2("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0084(self):
        """群聊列表展示页面——空格精确搜索存在的企业群和党群"""

        mp = MessagePage()
        # 点击右上角的+号，发起群聊
        mp.click_add_icon()
        mp.click_group_chat()
        scg = SelectContactsPage()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击选择一个群
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待选择一个群页面加载
        sog.wait_for_page_load()
        sog.click_search_box()
        # 空格精确搜索企业群和党群
        search_name = "好好 企业群"
        sog.input_search_keyword(search_name)
        # 1.空格精确搜索企业群和党群，可以匹配展示搜索结果（有相应“企”或党徽标识）
        self.assertEquals(sog.page_should_contain_text2(search_name), True)
        self.assertEquals(sog.is_exists_enterprise_group_icon(), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0085(self):
        """群聊列表展示页面——空格精确搜索不存在的企业群和党群"""

        mp = MessagePage()
        # 点击右上角的+号，发起群聊
        mp.click_add_icon()
        mp.click_group_chat()
        scg = SelectContactsPage()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击选择一个群
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待选择一个群页面加载
        sog.wait_for_page_load()
        sog.click_search_box()
        # 空格精确搜索企业群和党群
        search_name = "你好 啊啊"
        sog.input_search_keyword(search_name)
        # 1.空格精确搜索企业群和党群，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(sog.page_should_contain_text2("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0086(self):
        """群聊列表展示页面——数字精确搜索存在的企业群和党群"""

        mp = MessagePage()
        # 点击右上角的+号，发起群聊
        mp.click_add_icon()
        mp.click_group_chat()
        scg = SelectContactsPage()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击选择一个群
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待选择一个群页面加载
        sog.wait_for_page_load()
        sog.click_search_box()
        # 数字精确搜索企业群和党群
        search_name = "198891"
        sog.input_search_keyword(search_name)
        # 1.数字精确搜索企业群和党群，可以匹配展示搜索结果（有相应“企”或党徽标识）
        self.assertEquals(sog.page_should_contain_text2(search_name), True)
        self.assertEquals(sog.is_exists_enterprise_group_icon(), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0087(self):
        """群聊列表展示页面——数字精确搜索不存在的企业群和党群"""

        mp = MessagePage()
        # 点击右上角的+号，发起群聊
        mp.click_add_icon()
        mp.click_group_chat()
        scg = SelectContactsPage()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击选择一个群
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待选择一个群页面加载
        sog.wait_for_page_load()
        sog.click_search_box()
        # 数字精确搜索企业群和党群
        search_name = "168861768"
        sog.input_search_keyword(search_name)
        # 1.数字精确搜索企业群和党群，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(sog.page_should_contain_text2("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0088(self):
        """群聊列表展示页面——字符精确搜索存在的企业群和党群"""

        mp = MessagePage()
        # 点击右上角的+号，发起群聊
        mp.click_add_icon()
        mp.click_group_chat()
        scg = SelectContactsPage()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击选择一个群
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待选择一个群页面加载
        sog.wait_for_page_load()
        sog.click_search_box()
        # 字符精确搜索企业群和党群
        search_name = "*#@"
        sog.input_search_keyword(search_name)
        # 1.字符精确搜索企业群和党群，可以匹配展示搜索结果（有相应“企”或党徽标识）
        self.assertEquals(sog.page_should_contain_text2(search_name), True)
        self.assertEquals(sog.is_exists_enterprise_group_icon(), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0089(self):
        """群聊列表展示页面——字符精确搜索不存在的企业群和党群"""

        mp = MessagePage()
        # 点击右上角的+号，发起群聊
        mp.click_add_icon()
        mp.click_group_chat()
        scg = SelectContactsPage()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击选择一个群
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待选择一个群页面加载
        sog.wait_for_page_load()
        sog.click_search_box()
        # 字符精确搜索企业群和党群
        search_name = "$$$###"
        sog.input_search_keyword(search_name)
        # 1.字符精确搜索企业群和党群，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(sog.page_should_contain_text2("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0102(self):
        """在群聊设置页面，群成员头像上方文案展示"""

        # 进入企业群聊天会话页面
        Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        # 等待群聊设置页面加载
        gcs.wait_for_page_load()
        # 获取群成员头像数
        number = gcs.get_group_members_image_number()
        # 1.在群聊设置页面，群成员左上角展示了：群成员+括号+群聊天人数
        self.assertEquals(gcs.get_group_number_text(), "群成员 ({}）".format(number))
        # 2.页面左上角，展示了群聊设置，返回按钮
        self.assertEquals(gcs.is_exists_back_button(), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0103(self):
        """在群聊设置页面，群成员展示"""

        # 进入企业群聊天会话页面
        Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        # 等待群聊设置页面加载
        gcs.wait_for_page_load()
        # 1.在群聊设置页面，群头像默认展示为：头像+昵称
        self.assertEquals(gcs.is_exists_element_by_text("群成员头像"), True)
        self.assertEquals(gcs.is_exists_element_by_text("群成员名字"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0104(self):
        """在群聊设置页面，群成员展示列表，点击“>”"""

        # 进入企业群聊天会话页面
        Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        # 等待群聊设置页面加载
        gcs.wait_for_page_load()
        # 在群聊设置页面，点击群成员展示列表右上角的“>”按钮
        gcs.click_element_by_text("群成员文本")
        # 1.在群聊设置页面，点击群成员展示列表右上角的“>”按钮，可以跳转到群成员列表页
        self.assertEquals(gcs.is_exists_accessibility_id_attribute_by_name("群成员"), True)
        # 任意点击一个陌生的群成员头像
        gcs.click_accessibility_id_attribute_by_name("大佬1")
        cdp = ContactDetailsPage()
        # 2.任意点击一个陌生的群成员头像，会跳转到陌生人详情页中并展示交换名片按钮(间接验证)
        cdp.wait_for_page_load()
        self.assertEquals(cdp.is_exists_share_card_icon(), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0114(self):
        """在群聊设置页面中——群主头像展示"""

        # 进入企业群聊天会话页面
        Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        # 等待群聊设置页面加载
        gcs.wait_for_page_load()
        # 1.在群聊天设置页面，群主的头像上面，会戴上一个皇冠
        self.assertEquals(gcs.is_exists_element_by_text("群主头像皇冠"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0133(self):
        """在群聊天会话页面，长按消息体，点击收藏"""

        # 进入企业群聊天会话页面
        Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        # 确保有文本消息，由于企业群页面部分元素无法定位，发送两次
        gcp.input_text_message("123")
        gcp.click_send_button()
        gcp.input_text_message("测试文本消息0133")
        gcp.click_send_button()
        # 长按消息体
        gcp.press_last_text_message()
        # 1.长按消息体，会弹出功能列表
        self.assertEquals(gcp.page_should_contain_text2("收藏"), True)
        # 点击收藏
        gcp.click_accessibility_id_attribute_by_name("收藏")
        # 2.点击收藏，收藏成功，会提示：已收藏
        self.assertEquals(gcp.page_should_contain_text2("已收藏"), True)

    @staticmethod
    def tearDown_test_msg_huangmianhua_0133():
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
    def test_msg_huangmianhua_0134(self):
        """我——收藏——收藏内容展示"""

        mp = MessagePage()
        # 清空收藏列表，确保没有收藏影响验证
        Preconditions.enter_collection_page()
        mcp = MeCollectionPage()
        mcp.delete_all_collection()
        mcp.click_back_button()
        mp.open_message_page()
        # 进入企业群聊天会话页面
        group_name = Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        file_type = ".ppt"
        # 确保收藏列表存在收藏内容
        Preconditions.send_file_by_type(file_type)
        gcp.press_file_by_type(file_type)
        gcp.click_accessibility_id_attribute_by_name("收藏")
        gcp.click_back_button()
        # 1.我——收藏——收藏内容展示列表
        Preconditions.enter_collection_page()
        # 2.收藏内容展示：内容来源、收藏时间、收藏内容（部分或全部）
        self.assertEquals(mcp.page_should_contain_text2(group_name), True)
        self.assertEquals(mcp.page_should_contain_text2("今天"), True)
        self.assertEquals(mcp.is_exists_file_by_type(file_type), True)

    @staticmethod
    def tearDown_test_msg_huangmianhua_0134():
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
    def test_msg_huangmianhua_0135(self):
        """我——收藏——收藏内展示——点击收藏内容"""

        # 进入企业群聊天会话页面
        Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        file_type = ".ppt"
        # 确保收藏列表存在收藏内容
        Preconditions.send_file_by_type(file_type)
        gcp.press_file_by_type(file_type)
        gcp.click_accessibility_id_attribute_by_name("收藏")
        gcp.click_back_button()
        # 收藏内容展示列表，点击收藏内容
        Preconditions.enter_collection_page()
        mcp = MeCollectionPage()
        mcp.click_file_by_type(file_type)
        # 1.收藏内容展示列表，点击收藏内容，会跳转到收藏内容详情页面
        self.assertEquals(mcp.is_exists_more_icon(), True)
        # 点击左上角的返回按钮
        mcp.click_back_button()
        # 2.点击左上角的返回按钮，可以返回到收藏列表页
        mcp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_huangmianhua_0135():
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
    def test_msg_huangmianhua_0137(self):
        """我——收藏——收藏内展示——点击收藏内容——点击删除收藏内容"""

        mp = MessagePage()
        # 清空收藏列表，确保没有收藏影响验证
        Preconditions.enter_collection_page()
        mcp = MeCollectionPage()
        mcp.delete_all_collection()
        mcp.click_back_button()
        mp.open_message_page()
        # 进入企业群聊天会话页面
        Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        # 确保有文本消息，由于企业群页面部分元素无法定位，发送两次
        gcp.input_text_message("123")
        gcp.click_send_button()
        gcp.input_text_message("测试文本消息0137")
        gcp.click_send_button()
        # 确保存在收藏内容
        gcp.press_last_text_message()
        gcp.click_accessibility_id_attribute_by_name("收藏")
        gcp.click_back_button()
        # 收藏内容展示列表，左滑收藏文件
        Preconditions.enter_collection_page()
        mcp.left_slide_collection()
        # 1.收藏内容展示列表，左滑收藏文件，会展示删除功能
        self.assertEquals(mcp.is_exists_delete_button(), True)
        # 点击删除按钮
        mcp.click_element_delete_icon()
        # 2.点击删除按钮，会弹出确认弹窗(部分验证点变动)
        # 3.点击取消，关闭确认弹窗，停留在收藏列表(部分验证点变动)
        # 4.点击确定，成功移除收藏文件并弹出toast提示：已成功取消收藏(部分验证点变动)
        self.assertEquals(mcp.is_exists_collection(), False)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0152(self):
        """在群聊会话窗口，点击页面顶部的通话按钮"""

        # 进入企业群聊天会话页面
        Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        # 点击页面顶部的通话按钮
        gcp.click_mutilcall()
        # 1.点击页面顶部的通话按钮，会调起通话选择项弹窗
        self.assertEquals(gcp.is_exists_accessibility_id_attribute_by_name("飞信电话(免费)"), True)
        self.assertEquals(gcp.is_exists_accessibility_id_attribute_by_name("多方视频"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0153(self):
        """在群聊会话窗口，点击通话按钮——拨打多方电话"""

        # 进入企业群聊天会话页面
        Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        # 点击页面顶部的通话按钮
        gcp.click_mutilcall()
        # 点击多方电话按钮(部分步骤变动)
        gcp.click_accessibility_id_attribute_by_name("飞信电话(免费)")
        # 1.点击多方电话按钮，可以跳转到群成员联系人选择器页
        self.assertEquals(gcp.page_should_contain_text2("呼叫"), True)
        # 任意选中几个群成员，点击右上角的呼叫按钮
        gcp.click_accessibility_id_attribute_by_name("大佬1")
        gcp.click_accessibility_id_attribute_by_name("大佬2")
        gcp.click_name_attribute_by_name("呼叫")
        # 如果接到飞信电话，则挂断
        if gcp.page_should_contain_text2("拒绝"):
            gcp.click_name_attribute_by_name("拒绝")
        mcp = MultipartyCallPage()
        # 2.任意选中几个群成员，点击右上角的呼叫按钮，可以成功发起呼叫
        self.assertEquals(mcp.is_exists_element_by_text("红色挂断按钮"), True)
        mcp.click_element_by_text("红色挂断按钮")
        mcp.click_name_attribute_by_name("确定")

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0154(self):
        """在群聊会话窗口，点击通话按钮——拨打多方视频"""

        # 进入企业群聊天会话页面
        Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        # 点击页面顶部的通话按钮
        gcp.click_mutilcall()
        # 点击多方视频按钮
        gcp.click_accessibility_id_attribute_by_name("多方视频")
        # 1.点击多方视频按钮，可以跳转到群成员联系人选择器页
        self.assertEquals(gcp.page_should_contain_text2("呼叫"), True)
        # 任意选中几个群成员，点击右上角的呼叫按钮
        gcp.click_accessibility_id_attribute_by_name("大佬1")
        gcp.click_accessibility_id_attribute_by_name("大佬2")
        gcp.click_name_attribute_by_name("呼叫")
        mvp = MultiPartyVideoPage()
        # 2.任意选中几个群成员，点击右上角的呼叫按钮，可以成功发起呼叫
        self.assertEquals(mvp.page_should_contain_text2("多方视频呼叫中"), True)
        mvp.click_element_by_text("红色挂断按钮")
        mvp.click_name_attribute_by_name("确定")

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0155(self):
        """在群聊会话窗口，点击输入框上方的图片ICON，进入到图片展示列表"""

        # 进入企业群聊天会话页面
        Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        # 点击输入框上方的图片ICON
        gcp.click_picture()
        cpp = ChatPicPage()
        # 1.点击输入框上方的图片ICON，可以进入到相册列表页
        cpp.wait_for_page_load()
        # 任意选中一张照片，点击右下角的发送按钮
        cpp.select_picture()
        cpp.click_send()
        # 2.任意选中一张照片，点击右下角的发送按钮，可以发送成功(由于群聊的图片无法定位，间接验证)
        gcp.wait_for_page_load()
        self.assertEquals(gcp.is_exists_element_by_text("最后一条消息记录发送失败标识"), False)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0156(self):
        """在群聊会话窗口，点击输入框上方的相机ICON，进入到相机拍摄页"""

        # 进入企业群聊天会话页面
        Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        # 点击输入框上方的相机ICON
        gcp.click_take_picture()
        cpp = ChatPhotoPage()
        # 1.点击输入框上方的相机ICON,可以正常调起相机操作页
        cpp.wait_for_page_load()
        # 轻触拍摄按钮
        cpp.take_photo()
        # 2.轻触拍摄按钮，会拍摄成功一张照片
        cpp.wait_for_record_video_after_page_load()
        # 点击右下角的“√”按钮
        cpp.send_photo()
        # 3.点击右下角的“√”按钮，可以发送成功(由于群聊的图片无法定位，间接验证)
        gcp.wait_for_page_load()
        self.assertEquals(gcp.is_exists_element_by_text("最后一条消息记录发送失败标识"), False)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0157(self):
        """在群聊会话窗口，点击输入框上方的相机ICON，进入到相机拍摄页"""

        # 进入企业群聊天会话页面
        Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        # 点击输入框上方的相机ICON
        gcp.click_take_picture()
        cpp = ChatPhotoPage()
        # 1.点击输入框上方的相机ICON，调起相机操作页
        cpp.wait_for_page_load()
        # 长按拍摄按钮，录制时间超过1秒钟后，松手
        cpp.press_video(5)
        # 2.长按拍摄按钮，会进入到录像功能(间接验证)
        # self.assertEquals(cpp.is_exists_element_by_text("录像中"), True)
        self.assertEquals(cpp.is_exists_element_by_text("拍照"), False)
        # 3.录制时间超过1秒钟后，松手，会录制成功的视频
        cpp.wait_for_record_video_after_page_load()
        # 点击右下角的“√”按钮
        cpp.send_photo()
        # 4.点击右下角的“√”按钮，可以发送成功(间接验证)
        gcp.wait_for_page_load()
        self.assertEquals(gcp.is_exists_element_by_text("最后一条消息记录发送失败标识"), False)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0168(self):
        """消息草稿-聊天列表显示-不输入任何消息"""

        # 进入企业群聊天会话页面
        Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        # 确保当前群聊排在消息列表第一个
        text = "测试消息0168"
        gcp.input_text_message(text)
        # 确保输入框内容为空
        gcp.click_send_button()
        # 1.发送按钮不显示，无法发送
        self.assertEquals(gcp.is_exist_send_button(), False)
        # 返回聊天列表，查看显示
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 2.聊天页面显示群聊会话窗口页最新一条消息预览，无[草稿]标识
        self.assertEquals(mp.is_first_message_content(text), True)
        self.assertEquals(mp.is_first_message_draft(), False)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0169(self):
        """消息草稿-聊天列表显示-输入文本信息"""

        # 进入企业群聊天会话页面
        group_name = Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        # 确保当前群聊排在消息列表第一个
        gcp.input_text_message("123")
        gcp.click_send_button()
        # 文本编辑器中输入文本信息
        text = "测试文本消息0169"
        gcp.input_text_message(text)
        # 1.发送按钮高亮，可点击(间接验证)
        self.assertEquals(gcp._is_enabled_send_button(), True)
        # 返回聊天列表，查看显示
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()
        time.sleep(2)
        # 2.聊天页面显示输入文本信息预览，有[草稿]标识并标红(间接验证)
        self.assertEquals(mp.is_first_message_content("[草稿] " + text), True)
        # 清空输入框
        mp.click_accessibility_id_attribute_by_name(group_name)
        gcp.wait_for_page_load()
        gcp.input_text_message("")
        gcp.click_back_button()
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0170(self):
        """消息草稿-聊天列表显示-输入表情信息"""

        # 进入企业群聊天会话页面
        group_name = Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        # 确保当前群聊排在消息列表第一个
        gcp.input_text_message("123")
        gcp.click_send_button()
        # 点击输入框右侧表情图标
        gcp.click_expression_button()
        # 1.键盘转变为表情展示页
        self.assertEquals(gcp.is_exists_gif_button(), True)
        # 输入表情信息
        gcp.click_expression_wx()
        # 2.选择表情，发送按钮高亮，可点击(间接验证)
        self.assertEquals(gcp._is_enabled_send_button(), True)
        # 返回聊天列表，查看显示
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()
        time.sleep(2)
        # 3.聊天页面显示输入表情信息预览，有[草稿]标识并标红(间接验证)
        self.assertEquals(mp.is_first_message_content("[草稿] [微笑1]"), True)
        # 清空输入框
        mp.click_accessibility_id_attribute_by_name(group_name)
        gcp.wait_for_page_load()
        gcp.input_text_message("")
        gcp.click_back_button()
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0171(self):
        """消息草稿-聊天列表显示-输入特殊字符"""

        # 进入企业群聊天会话页面
        group_name = Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        # 确保当前群聊排在消息列表第一个
        gcp.input_text_message("123")
        gcp.click_send_button()
        # 文本编辑器中输入特殊字符信息
        text = "&*$"
        gcp.input_text_message(text)
        # 1.发送按钮高亮，可点击(间接验证)
        self.assertEquals(gcp._is_enabled_send_button(), True)
        # 返回聊天列表，查看显示
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()
        time.sleep(2)
        # 2.聊天页面显示输入特殊字符信息预览，有[草稿]标识并标红(间接验证)
        self.assertEquals(mp.is_first_message_content("[草稿] " + text), True)
        # 清空输入框
        mp.click_accessibility_id_attribute_by_name(group_name)
        gcp.wait_for_page_load()
        gcp.input_text_message("")
        gcp.click_back_button()
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0174(self):
        """消息草稿-聊天列表显示-草稿信息发送成功"""

        # 进入企业群聊天会话页面
        group_name = Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        # 确保当前群聊排在消息列表第一个
        gcp.input_text_message("123")
        gcp.click_send_button()
        # 输入文本信息，不发送
        text = "测试文本消息0174"
        gcp.input_text_message(text)
        # 1.保存为草稿信息
        self.assertEquals(gcp.is_exists_text_by_input_box(text), True)
        # 返回消息列表，查看预览
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()
        time.sleep(2)
        # 2.消息列表，显示[草稿]标红字样，消息预览显示草稿信息，信息过长时显示…(间接验证)
        self.assertEquals(mp.is_first_message_content("[草稿] " + text), True)
        # 返回群聊会话窗口页，点击发送
        mp.click_accessibility_id_attribute_by_name(group_name)
        gcp.wait_for_page_load()
        gcp.click_send_button()
        # 3.消息发送成功(间接验证)
        self.assertEquals(gcp.is_exists_element_by_text("最后一条消息记录发送失败标识"), False)
        # 返回消息列表，查看预览信息
        gcp.click_back_button()
        mp.wait_for_page_load()
        # 4.消息列表[草稿]标红字样消失，显示为正常消息预览
        self.assertEquals(mp.is_first_message_draft(), False)
        self.assertEquals(mp.is_first_message_content(text), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0175(self):
        """消息草稿-聊天列表显示-草稿信息删除"""

        # 进入企业群聊天会话页面
        group_name = Preconditions.enter_enterprise_group_chat_page()
        gcp = GroupChatPage()
        # 确保当前群聊排在消息列表第一个
        text = "测试文本消息0175"
        gcp.input_text_message(text)
        gcp.click_send_button()
        # 输入文本信息，不发送
        draft_text = "测试草稿消息0175"
        gcp.input_text_message(draft_text)
        # 1.保存为草稿信息
        self.assertEquals(gcp.is_exists_text_by_input_box(draft_text), True)
        # 返回消息列表，查看预览
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()
        time.sleep(2)
        # 2.消息列表，显示[草稿]标红字样，消息预览显示草稿信息，信息过长时显示…(间接验证)
        self.assertEquals(mp.is_first_message_content("[草稿] " + draft_text), True)
        # 返回群聊会话窗口页，删除草稿信息
        mp.click_accessibility_id_attribute_by_name(group_name)
        gcp.wait_for_page_load()
        gcp.input_text_message("")
        # 3.草稿信息删除成功
        self.assertEquals(gcp.is_clear_the_input_box(), True)
        # 返回消息列表，查看预览信息
        gcp.click_back_button()
        mp.wait_for_page_load()
        time.sleep(2)
        # 4.消息列表[草稿]标红字样消失，显示为最近一次消息预览
        self.assertEquals(mp.is_first_message_draft(), False)
        self.assertEquals(mp.is_first_message_content(text), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0187(self):
        """通讯录——群聊——搜索——选择一个群"""

        mp = MessagePage()
        # 点击右上角的+号，发起群聊
        mp.click_add_icon()
        mp.click_group_chat()
        scg = SelectContactsPage()
        # 1.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击选择一个群
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 2.点击选择一个群，可以进入到群聊列表展示页面
        sog.wait_for_page_load()
        sog.click_search_box()
        # 中文模糊搜索
        search_name = "中文测试"
        sog.input_search_keyword(search_name)
        # 3.中文模糊搜索，可以匹配展示搜索结果
        self.assertEquals(sog.page_should_contain_text2("中文测试企业群"), True)
        # 进入通讯录-群聊页面
        sog.click_back_button(3)
        mp.wait_for_page_load()
        mp.open_contacts_page()
        cp = ContactsPage()
        cp.wait_for_page_load()
        cp.open_group_chat_list()
        glp = GroupListPage()
        # 等待群聊列表页面加载
        glp.wait_for_page_load()
        glp.click_search_input()
        group_search = GroupListSearchPage()
        # 搜索群聊
        group_search.input_search_keyword(search_name)
        self.assertEquals(group_search.is_group_in_list("中文测试企业群"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0188(self):
        """通讯录-群聊-中文模糊搜索——搜索结果展示"""

        mp = MessagePage()
        mp.open_contacts_page()
        cp = ContactsPage()
        # 等待通讯录页面加载
        cp.wait_for_page_load()
        cp.open_group_chat_list()
        glp = GroupListPage()
        # 等待群聊列表页面加载
        glp.wait_for_page_load()
        glp.click_search_input()
        group_search = GroupListSearchPage()
        # 中文模糊搜索
        group_search.input_search_keyword("不存在的群")
        # 1.中文模糊搜索，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(group_search.page_should_contain_text2("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0189(self):
        """通讯录-群聊-中文精确搜索——搜索结果展示"""

        mp = MessagePage()
        mp.open_contacts_page()
        cp = ContactsPage()
        # 等待通讯录页面加载
        cp.wait_for_page_load()
        cp.open_group_chat_list()
        glp = GroupListPage()
        # 等待群聊列表页面加载
        glp.wait_for_page_load()
        glp.click_search_input()
        group_search = GroupListSearchPage()
        # 中文精确搜索
        search_name = "中文测试企业群"
        group_search.input_search_keyword(search_name)
        # 1.中文精确搜索，可以匹配展示搜索结果
        self.assertEquals(group_search.is_group_in_list(search_name), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0190(self):
        """通讯录-群聊-中文精确搜索——搜索结果展示"""

        mp = MessagePage()
        mp.open_contacts_page()
        cp = ContactsPage()
        # 等待通讯录页面加载
        cp.wait_for_page_load()
        cp.open_group_chat_list()
        glp = GroupListPage()
        # 等待群聊列表页面加载
        glp.wait_for_page_load()
        glp.click_search_input()
        group_search = GroupListSearchPage()
        # 中文精确搜索
        group_search.input_search_keyword("不存在企业群")
        # 1.中文精确搜索，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(group_search.page_should_contain_text2("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0191(self):
        """通讯录-群聊-英文精确搜索——搜索结果展示"""

        mp = MessagePage()
        mp.open_contacts_page()
        cp = ContactsPage()
        # 等待通讯录页面加载
        cp.wait_for_page_load()
        cp.open_group_chat_list()
        glp = GroupListPage()
        # 等待群聊列表页面加载
        glp.wait_for_page_load()
        glp.click_search_input()
        group_search = GroupListSearchPage()
        # 英文精确搜索
        search_name = "test_enterprise_group"
        group_search.input_search_keyword(search_name)
        # 1.英文精确搜索，可以匹配展示搜索结果
        self.assertEquals(group_search.is_group_in_list(search_name), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0192(self):
        """通讯录-群聊-英文精确搜索——搜索结果展示"""

        mp = MessagePage()
        mp.open_contacts_page()
        cp = ContactsPage()
        # 等待通讯录页面加载
        cp.wait_for_page_load()
        cp.open_group_chat_list()
        glp = GroupListPage()
        # 等待群聊列表页面加载
        glp.wait_for_page_load()
        glp.click_search_input()
        group_search = GroupListSearchPage()
        # 英文精确搜索
        group_search.input_search_keyword("test_no_exists")
        # 1.英文精确搜索，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(group_search.page_should_contain_text2("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0193(self):
        """通讯录-群聊-空格精确搜索——搜索结果展示"""

        mp = MessagePage()
        mp.open_contacts_page()
        cp = ContactsPage()
        # 等待通讯录页面加载
        cp.wait_for_page_load()
        cp.open_group_chat_list()
        glp = GroupListPage()
        # 等待群聊列表页面加载
        glp.wait_for_page_load()
        glp.click_search_input()
        group_search = GroupListSearchPage()
        # 空格精确搜索
        search_name = "好好 企业群"
        group_search.input_search_keyword(search_name)
        # 1.空格精确搜索，可以匹配展示搜索结果
        self.assertEquals(group_search.is_group_in_list(search_name), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0194(self):
        """通讯录-群聊-空格精确搜索——搜索结果展示"""

        mp = MessagePage()
        mp.open_contacts_page()
        cp = ContactsPage()
        # 等待通讯录页面加载
        cp.wait_for_page_load()
        cp.open_group_chat_list()
        glp = GroupListPage()
        # 等待群聊列表页面加载
        glp.wait_for_page_load()
        glp.click_search_input()
        group_search = GroupListSearchPage()
        # 空格精确搜索
        group_search.input_search_keyword("你好 啊啊")
        # 1.空格精确搜索，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(group_search.page_should_contain_text2("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0195(self):
        """通讯录-群聊-数字精确搜索——搜索结果展示"""

        mp = MessagePage()
        mp.open_contacts_page()
        cp = ContactsPage()
        # 等待通讯录页面加载
        cp.wait_for_page_load()
        cp.open_group_chat_list()
        glp = GroupListPage()
        # 等待群聊列表页面加载
        glp.wait_for_page_load()
        glp.click_search_input()
        group_search = GroupListSearchPage()
        # 数字精确搜索
        search_name = "198891"
        group_search.input_search_keyword(search_name)
        # 1.数字精确搜索，可以匹配展示搜索结果
        self.assertEquals(group_search.is_group_in_list(search_name), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0196(self):
        """通讯录-群聊-数字精确搜索——搜索结果展示"""

        mp = MessagePage()
        mp.open_contacts_page()
        cp = ContactsPage()
        # 等待通讯录页面加载
        cp.wait_for_page_load()
        cp.open_group_chat_list()
        glp = GroupListPage()
        # 等待群聊列表页面加载
        glp.wait_for_page_load()
        glp.click_search_input()
        group_search = GroupListSearchPage()
        # 数字精确搜索
        group_search.input_search_keyword("168861768")
        # 1.数字精确搜索，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(group_search.page_should_contain_text2("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0197(self):
        """通讯录-群聊-数字精确搜索——搜索结果展示"""

        mp = MessagePage()
        mp.open_contacts_page()
        cp = ContactsPage()
        # 等待通讯录页面加载
        cp.wait_for_page_load()
        cp.open_group_chat_list()
        glp = GroupListPage()
        # 等待群聊列表页面加载
        glp.wait_for_page_load()
        glp.click_search_input()
        group_search = GroupListSearchPage()
        # 数字精确搜索
        search_name = "198891"
        group_search.input_search_keyword(search_name)
        # 1.数字精确搜索，可以匹配展示搜索结果
        self.assertEquals(group_search.is_group_in_list(search_name), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0198(self):
        """群通讯录-群聊-数字精确搜索——搜索结果展示"""

        mp = MessagePage()
        mp.open_contacts_page()
        cp = ContactsPage()
        # 等待通讯录页面加载
        cp.wait_for_page_load()
        cp.open_group_chat_list()
        glp = GroupListPage()
        # 等待群聊列表页面加载
        glp.wait_for_page_load()
        glp.click_search_input()
        group_search = GroupListSearchPage()
        # 数字精确搜索
        group_search.input_search_keyword("168861768")
        # 1.数字精确搜索，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(group_search.page_should_contain_text2("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0199(self):
        """通讯录-群聊-字符精确搜索——搜索结果展示"""

        mp = MessagePage()
        mp.open_contacts_page()
        cp = ContactsPage()
        # 等待通讯录页面加载
        cp.wait_for_page_load()
        cp.open_group_chat_list()
        glp = GroupListPage()
        # 等待群聊列表页面加载
        glp.wait_for_page_load()
        glp.click_search_input()
        group_search = GroupListSearchPage()
        # 字符精确搜索
        search_name = "*#@"
        group_search.input_search_keyword(search_name)
        # 1.字符精确搜索，可以匹配展示搜索结果
        self.assertEquals(group_search.is_group_in_list(search_name), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0200(self):
        """通讯录-群聊-字符精确搜索——搜索结果展示"""

        mp = MessagePage()
        mp.open_contacts_page()
        cp = ContactsPage()
        # 等待通讯录页面加载
        cp.wait_for_page_load()
        cp.open_group_chat_list()
        glp = GroupListPage()
        # 等待群聊列表页面加载
        glp.wait_for_page_load()
        glp.click_search_input()
        group_search = GroupListSearchPage()
        # 字符精确搜索
        group_search.input_search_keyword("$$$###")
        # 1.字符精确搜索，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(group_search.page_should_contain_text2("无搜索结果"), True)
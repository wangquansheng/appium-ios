import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import ContactsPage
from pages import GroupChatPage
from pages import GroupChatSetPage
from pages import GroupListPage
from pages import MessagePage
from pages import SelectContactsPage
from pages import SelectOneGroupPage
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
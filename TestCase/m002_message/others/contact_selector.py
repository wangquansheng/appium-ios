import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import ContactsPage
from pages import GroupChatPage
from pages import GroupListPage
from pages import MeCollectionPage
from pages import MePage
from pages import MessagePage
from pages import SelectContactsPage
from pages import WorkbenchPage
from pages.workbench.group_messenger.GroupMessenger import GroupMessengerPage
from pages.workbench.group_messenger.HelpCenter import HelpCenterPage
from pages.workbench.group_messenger.NewMessage import NewMessagePage
from pages.workbench.group_messenger.SelectCompanyContacts import SelectCompanyContactsPage
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
    def enter_group_messenger_page():
        """进入群发信使首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_group_messenger()

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

class ContactSelectorTest(TestCase):
    """联系人选择器"""

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

        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0002_01(self):
        """新建消息—输入姓名/号码搜索"""
        # 1.点击搜索框
        # 2.姓名搜索：中文、英文、数字、特殊字符、各种混和等等
        # 号码搜索：有“+”，例“+86、+852”；一般号码；无手机联系人且为手机号
        # 3.查看搜索页面展示
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("新建消息")
        time.sleep(2)
        scg = SelectContactsPage()
        scg.search("飞信")
        if not scg.is_text_present_("飞信电话"):
            raise AssertionError("搜索结果有误")
        scg.click_back_button()
        scg.click_back_button()

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0002_02(self):
        """新建消息—输入姓名/号码搜索"""
        # 1.点击搜索框
        # 2.姓名搜索：中文、英文、数字、特殊字符、各种混和等等
        # 号码搜索：有“+”，例“+86、+852”；一般号码；无手机联系人且为手机号
        # 3.查看搜索页面展示
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("新建消息")
        time.sleep(2)
        scg = SelectContactsPage()
        scg.search("En")
        if not scg.is_text_present_("English"):
            raise AssertionError("搜索结果有误")
        scg.click_back_button()
        scg.click_back_button()

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0002_03(self):
        """新建消息—输入姓名/号码搜索"""
        # 1.点击搜索框
        # 2.姓名搜索：中文、英文、数字、特殊字符、各种混和等等
        # 号码搜索：有“+”，例“+86、+852”；一般号码；无手机联系人且为手机号
        # 3.查看搜索页面展示
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("新建消息")
        time.sleep(2)
        scg = SelectContactsPage()
        scg.search("1")
        if not scg.is_text_present_("测试1"):
            raise AssertionError("搜索结果有误")
        scg.click_back_button()
        scg.click_back_button()

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0002_04(self):
        """新建消息—输入姓名/号码搜索"""
        # 1.点击搜索框
        # 2.姓名搜索：中文、英文、数字、特殊字符、各种混和等等
        # 号码搜索：有“+”，例“+86、+852”；一般号码；无手机联系人且为手机号
        # 3.查看搜索页面展示
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("新建消息")
        time.sleep(2)
        scg = SelectContactsPage()
        scg.search("@$")
        if not scg.is_text_present_("特殊!@$"):
            raise AssertionError("搜索结果有误")
        scg.click_back_button()
        scg.click_back_button()

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0002_05(self):
        """新建消息—输入姓名/号码搜索"""
        # 1.点击搜索框
        # 2.姓名搜索：中文、英文、数字、特殊字符、各种混和等等
        # 号码搜索：有“+”，例“+86、+852”；一般号码；无手机联系人且为手机号
        # 3.查看搜索页面展示
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("新建消息")
        time.sleep(2)
        scg = SelectContactsPage()
        scg.search("i@1大")
        if not scg.is_text_present_("Li@1大佬"):
            raise AssertionError("搜索结果有误")
        scg.click_back_button()
        scg.click_back_button()

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0003_01(self):
        """新建消息—输入姓名/号码搜索—查看搜索结果"""
        # 1.点击搜索框
        # 2.姓名或手机号码搜索
        # 3.当本地有搜索结果时
        # 4.当本地无搜索结果时
        # 5.搜索关键字与我的电脑有关时，
        # 6.当无手机联系人且为手机号时，查看搜索结果展示
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("新建消息")
        time.sleep(2)
        scg = SelectContactsPage()
        scg.search("飞信")
        if not scg.is_text_present_("飞信电话"):
            raise AssertionError("搜索结果有误")
        scg.click_back_button()
        scg.click_back_button()

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0003_02(self):
        """新建消息—输入姓名/号码搜索—查看搜索结果"""
        # 1.点击搜索框
        # 2.姓名或手机号码搜索
        # 3.当本地有搜索结果时
        # 4.当本地无搜索结果时
        # 5.搜索关键字与我的电脑有关时，
        # 6.当无手机联系人且为手机号时，查看搜索结果展示
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("新建消息")
        time.sleep(2)
        scg = SelectContactsPage()
        # 输入无搜索结果的内容
        scg.search("说的是吧")
        if scg.is_text_present_("说的是吧"):
            raise AssertionError("搜索结果有误")
        scg.click_back_button()
        scg.click_back_button()

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0003_03(self):
        """新建消息—输入姓名/号码搜索—查看搜索结果"""
        # 1.点击搜索框
        # 2.姓名或手机号码搜索
        # 3.当本地有搜索结果时
        # 4.当本地无搜索结果时
        # 5.搜索关键字与我的电脑有关时，
        # 6.当无手机联系人且为手机号时，查看搜索结果展示
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("新建消息")
        time.sleep(2)
        scg = SelectContactsPage()
        # 输入有关我的电脑的内容
        scg.search("我")
        if not scg.is_text_present_("我的电脑"):
            raise AssertionError("搜索结果有误")
        scg.click_back_button()
        scg.click_back_button()

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0003_04(self):
        """新建消息—输入姓名/号码搜索—查看搜索结果"""
        # 1.点击搜索框
        # 2.姓名或手机号码搜索
        # 3.当本地有搜索结果时
        # 4.当本地无搜索结果时
        # 5.搜索关键字与我的电脑有关时，
        # 6.当无手机联系人且为手机号时，查看搜索结果展示
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("新建消息")
        time.sleep(2)
        scg = SelectContactsPage()
        # 输入有关我的电脑的内容
        scg.search("19864759568")
        if not scg.is_text_contain_present_("tel"):
            raise AssertionError("搜索结果有误")
        scg.click_back_button()
        scg.click_back_button()

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0004(self):
        """新建消息—输入姓名/号码搜索—查看本地搜索结果的展示"""
        # 1.点击搜索框
        # 2.姓名或手机号码搜索
        # 3.当本地有搜索结果时
        # 4.搜索结果规则显示
        # 5.当搜索结果 > 3条时，点击查看更多
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("新建消息")
        time.sleep(2)
        scg = SelectContactsPage()
        # 输入有关我的电脑的内容
        scg.search("大")
        if not scg.is_text_present_("大佬"):
            raise AssertionError("搜索结果有误")
        scg.click_back_button()
        scg.click_back_button()

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0005(self):
        """新建消息—搜索-搜索团队联系人"""
        # 1.点击搜索框
        # 2.姓名或手机号码搜索
        # 3.点击搜索团队联系人
        # 4.查看页面展示
        # 5.点击任意联系人
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("新建消息")
        time.sleep(2)
        scg = SelectContactsPage()
        # 输入有关我的电脑的内容
        scg.search("大")
        time.sleep(2)
        scg.click_text("搜索团队联系人")
        time.sleep(5)
        if not scg.is_text_contain_present_("大佬"):
            raise AssertionError("搜索结果有误")
        scg.click_text("大佬")
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0006(self):
        """新建消息—选择团队联系人"""
        # 1.点击选择团队联系人
        # 2.查看页面展示
        # 3.点击所在的企业和部门
        # 4.查看页面展示
        # 5.搜索框搜索
        # 6.查看搜索结果页面展示
        # 7.点击任意联系人
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("新建消息")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(5)
        scg.search("大")
        time.sleep(3)
        if not scg.is_text_contain_present_("大佬"):
            raise AssertionError("搜索结果有误")
        scg.click_text("大佬")
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0010(self):
        """新建消息—进入我的团队页面显示逻辑"""
        # 1.点击新建消息
        # 2.点击选择团队联系人
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("新建消息")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(5)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0011(self):
        """新新建消息—选择手机联系人"""
        # 1.查看手机联系人的页面展示规则
        # 2.点击任意联系人
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("新建消息")
        time.sleep(2)
        scg = SelectContactsPage()
        scg.click_one_contact("飞信电话")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0295(self):
        """新建消息-选择团队联系人-企业列表页面的文案展示"""
        # 1、点击选择团队联系人
        # 2、查看企业列表展示页面
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("新建消息")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(5)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0296(self):
        """新建消息-选择团队联系人-企业列表页面-点击搜索框"""
        # 1、点击选择团队联系人
        # 2、点击搜索框
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("新建消息")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(5)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
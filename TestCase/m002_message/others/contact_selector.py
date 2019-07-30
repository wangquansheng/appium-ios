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
from pages import SelectOneGroupPage
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

        # 导入团队联系人、企业部门
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
                                  ('陈丹丹', "13800137004"), ('alice', "13800137005"), ('郑海', "13802883296"),
                                  ('a+6.和', "13802883297"), ('e123', "13802883277"), ('短号', "666")]
                Preconditions.create_he_contacts2(contact_names2)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

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
        if scg.is_text_contain_present_("无搜索结果"):
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
        if not scg.is_text_contain_present_("大佬"):
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

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0297(self):
        """新建消息-选择团队联系人-企业列表页面-搜索框为空时或者有内容"""
        # 1、点击选择团队联系人
        # 2、点击搜索框
        # 3、输入框输入内容时，查看输入框展示
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
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("大")
        time.sleep(3)
        if not scg.is_text_contain_present_("大佬"):
            raise AssertionError("搜索结果有误")

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0298(self):
        """新建消息/免费短信（发送短信）—联系人选择器-企业列表页面-搜索联系人"""
        # 1、点击选择团队联系人
        # 2、点击搜索框
        # 3、输入框输入姓名或者号码进行搜索（如：13888888888），查看搜索结果展示
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
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("大")
        time.sleep(3)
        if not scg.is_text_contain_present_("大佬"):
            raise AssertionError("搜索结果有误")

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0299(self):
        """新建消息—联系人选择器-企业列表页面-搜索联系人"""
        # 1、点击选择团队联系人
        # 2、点击搜索框
        # 3、输入框输入姓名或者号码进行搜索（如：13888888888），查看搜索结果展示
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
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("你")
        time.sleep(3)
        if not scg.is_text_contain_present_("无搜索结果"):
            raise AssertionError("搜索结果有误")

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0300(self):
        """新建消息-选择团队联系人-企业列表页面-上滑联系人"""
        # 1、点击选择团队联系人
        # 2、搜索框搜索
        # 3、上滑查看更多联系人
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
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("大")
        time.sleep(3)
        if not scg.is_text_contain_present_("大佬"):
            raise AssertionError("搜索结果有误")
        scg.page_down()
        scg.page_up()
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0310(self):
        """新建消息-选择团队联系人-企业列表页面-输入一个大写/小写字母搜索联系人"""
        # 1、点击选择团队联系人
        # 2、搜索框输入一个大写 / 小写字母进行搜索
        # 3、跳转到企业列表展示页面，输入一个大写 / 小写字母搜索联系人
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
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("c")
        time.sleep(3)
        if not scg.is_text_contain_present_("c平5"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0311(self):
        """新建消息-选择团队联系人-企业列表页面-输入联系人的姓名拼音"""
        # 1、点击选择团队联系人
        # 2、搜索框输入联系人的姓名拼音进行搜索
        # 3、跳转到企业列表展示页面，输入联系人的姓名拼音，搜索联系人
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
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("chen")
        time.sleep(3)
        if not scg.is_text_contain_present_("陈丹丹"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0312(self):
        """新建消息-选择团队联系人-企业列表页面-输入任何一个汉字——搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入汉字进行搜索
        # 3、跳转到企业列表展示页面，输入任何一个汉字，搜索联系人
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
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("陈")
        time.sleep(3)
        if not scg.is_text_contain_present_("陈丹丹"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0313(self):
        """新建消息-选择团队联系人-企业列表页面-输入号码规则的3位数字——搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入“135”进行搜索
        # 3、跳转到企业列表展示页面，输入号码规则的3位数字——搜索
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
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("138")
        time.sleep(3)
        if not scg.is_text_contain_present_("13800"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0314(self):
        """新建消息-选择团队联系人-企业列表页面-输入号码规则的11位数字——搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入“13533110870”进行搜索
        # 3、企业列表展示页面
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
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("13800137004")
        time.sleep(3)
        if not scg.is_text_contain_present_("陈丹丹"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0315(self):
        """新建消息-选择团队联系人-企业列表页面-企业列表页面-输入号码规则的12位数字——搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入“135331108701”进行搜索
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
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("135331108701")
        time.sleep(3)
        if not scg.is_text_contain_present_("无搜索结果"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0316(self):
        """新建消息-选择团队联系人-企业列表页面-企业列表页面-输入随机1位数字——搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入随机1位数字进行搜索
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
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("9")
        time.sleep(3)
        if not scg.is_text_contain_present_("无搜索结果"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0317(self):
        """新建消息-选择团队联系人-企业列表页面-企业列表页面-输入随机1位数字——搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入随机1位数字进行搜索
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
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("5")
        time.sleep(3)
        if not scg.is_text_contain_present_("c平5"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0318(self):
        """新建消息-选择团队联系人-企业列表页面-输入特殊字符‘+’——搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入特殊字符‘+’进行搜索
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
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("+")
        time.sleep(3)
        if not scg.is_text_contain_present_("a+6.和"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0319(self):
        """新建消息-选择团队联系人-企业列表页面-输入特殊字符‘.’——搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入特殊字符‘.’进行搜索
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
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search(".")
        time.sleep(3)
        if not scg.is_text_contain_present_("a+6.和"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0320(self):
        """新建消息-选择团队联系人-企业列表页面-输入汉字和数字-组合搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入汉字和数字（如测123）进行搜索
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
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("平5")
        time.sleep(3)
        if not scg.is_text_contain_present_("c平5"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0321(self):
        """新建消息-选择团队联系人-企业列表页面-输入数字和特殊字符组合-组合搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入数字和特殊字符组合（如123 @￥ % ）进行搜索
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
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("6.")
        time.sleep(3)
        if not scg.is_text_contain_present_("a+6.和"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0322(self):
        """新建消息-选择团队联系人-企业列表页面-输入数字和字母组合-组合搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入数字和字母组合（如ce123）进行搜索
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
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("e1")
        time.sleep(3)
        if not scg.is_text_contain_present_("e123"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0323(self):
        """新建消息-选择团队联系人-企业列表页面-输入汉字和字母组合-组合搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入汉字和字母组合（如ce试）进行搜索
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
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("b测")
        time.sleep(3)
        if not scg.is_text_contain_present_("b测算"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0324(self):
        """新建消息-选择团队联系人-企业列表页面-输入字母和特殊字符组合-组合搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入字母和特殊字符组合（如ce @￥  # ）进行搜索
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
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("a+")
        time.sleep(3)
        if not scg.is_text_contain_present_("a+6.和"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0325(self):
        """新建消息-选择团队联系人-企业列表页面-输入短号666-搜索"""
        # 1、点击选择团队联系人
        # 2、跳转到企业列表展示页面，输入短号666，搜索联系人
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
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("666")
        time.sleep(3)
        if not scg.is_text_contain_present_("短号"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0326(self):
        """转发/批量转发-选择团队联系人-企业列表页面的文案展示"""
        # 1、点击选择团队联系人
        # 2、查看企业列表展示页面
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        if not scg.is_text_contain_present_("选择联系人"):
            raise AssertionError("左上角的标题文案不是选择联系人")
        if not scg.is_text_contain_present_("搜索或输入手机号"):
            raise AssertionError("搜索框中默认展示的文案不是搜索或输入手机号")

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0327(self):
        """转发/批量转发-选择团队联系人-企业列表页面-点击搜索框"""
        # 1、点击选择团队联系人
        # 2、点击搜索框
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.page_down()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0328(self):
        """转发/批量转发-选择团队联系人-企业列表页面-搜索框为空时或者有内容"""
        # 1、点击选择团队联系人
        # 2、点击搜索框
        # 3、输入框输入内容时，查看输入框展示
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("大")
        time.sleep(3)
        if not scg.is_text_contain_present_("大佬"):
            raise AssertionError("搜索结果有误")

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0329(self):
        """转发/批量转发—联系人选择器-企业列表页面-搜索联系人"""
        # 1、点击选择团队联系人
        # 2、点击搜索框
        # 3、输入框输入姓名或者号码进行搜索（如：13888888888），查看搜索结果展示
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("13800137004")
        time.sleep(3)
        if not scg.is_text_contain_present_("陈丹丹"):
            raise AssertionError("搜索结果有误")

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0330(self):
        """转发/批量转发—联系人选择器-企业列表页面-搜索联系人"""
        # 1、点击选择团队联系人
        # 2、点击搜索框
        # 3、输入框输入姓名或者号码进行搜索（如：13888888888），查看搜索结果展示
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("你")
        time.sleep(3)
        if not scg.is_text_contain_present_("无搜索结果"):
            raise AssertionError("搜索结果有误")
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0331(self):
        """转发/批量转发-选择团队联系人-企业列表页面-上滑联系人"""
        # 1、点击选择团队联系人
        # 2、搜索框搜索
        # 3、上滑查看更多联系人
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("大")
        time.sleep(3)
        if not scg.is_text_contain_present_("大佬"):
            raise AssertionError("搜索结果有误")
        scg.page_down()
        scg.page_up()
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0332(self):
        """转发/批量转发-选择团队联系人-企业列表页面-输入一个大写/小写字母搜索联系人"""
        # 1、点击选择团队联系人
        # 2、搜索框输入一个大写 / 小写字母进行搜索
        # 3、跳转到企业列表展示页面，输入一个大写 / 小写字母搜索联系人
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("c")
        time.sleep(3)
        if not scg.is_text_contain_present_("c平5"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0333(self):
        """转发/批量转发-选择团队联系人-企业列表页面-输入联系人的姓名拼音"""
        # 1、点击选择团队联系人
        # 2、搜索框输入联系人的姓名拼音进行搜索
        # 3、跳转到企业列表展示页面，输入联系人的姓名拼音，搜索联系人
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("chen")
        time.sleep(3)
        if not scg.is_text_contain_present_("陈丹丹"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0334(self):
        """转发/批量转发-选择团队联系人-企业列表页面-输入任何一个汉字——搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入汉字进行搜索
        # 3、跳转到企业列表展示页面，输入任何一个汉字，搜索联系人
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("陈")
        time.sleep(3)
        if not scg.is_text_contain_present_("陈丹丹"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0335(self):
        """转发/批量转发-选择团队联系人-企业列表页面-输入号码规则的3位数字——搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入“135”进行搜索
        # 3、跳转到企业列表展示页面，输入号码规则的3位数字——搜索
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("138")
        time.sleep(3)
        if not scg.is_text_contain_present_("13800"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0336(self):
        """转发/批量转发-选择团队联系人-企业列表页面-输入号码规则的11位数字——搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入“13533110870”进行搜索
        # 3、企业列表展示页面
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.search("13800137004")
        time.sleep(3)
        if not scg.is_text_contain_present_("陈丹丹"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0337(self):
        """转发/批量转发-选择团队联系人-企业列表页面-企业列表页面-输入号码规则的12位数字——搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入“135331108701”进行搜索
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.search("135331108701")
        time.sleep(3)
        if not scg.is_text_contain_present_("无搜索结果"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0338(self):
        """转发/批量转发-选择团队联系人-企业列表页面-企业列表页面-输入随机1位数字——搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入随机1位数字进行搜索
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.search("9")
        time.sleep(3)
        if not scg.is_text_contain_present_("无搜索结果"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0339(self):
        """转发/批量转发-选择团队联系人-企业列表页面-企业列表页面-输入随机1位数字——搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入随机1位数字进行搜索
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("5")
        time.sleep(3)
        if not scg.is_text_contain_present_("c平5"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0340(self):
        """转发/批量转发-选择团队联系人-企业列表页面-输入特殊字符‘+’——搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入特殊字符‘+’进行搜索
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("+")
        time.sleep(3)
        if not scg.is_text_contain_present_("a+6.和"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0341(self):
        """转发/批量转发-选择团队联系人-企业列表页面-输入特殊字符‘.’——搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入特殊字符‘.’进行搜索
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search(".")
        time.sleep(3)
        if not scg.is_text_contain_present_("a+6.和"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0342(self):
        """转发/批量转发-选择团队联系人-企业列表页面-输入汉字和数字-组合搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入汉字和数字（如测123）进行搜索
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("平5")
        time.sleep(3)
        if not scg.is_text_contain_present_("c平5"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0343(self):
        """转发/批量转发-选择团队联系人-企业列表页面-输入数字和特殊字符组合-组合搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入数字和特殊字符组合（如123 @￥ % ）进行搜索
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("6.")
        time.sleep(3)
        if not scg.is_text_contain_present_("a+6.和"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0344(self):
        """转发/批量转发-选择团队联系人-企业列表页面-输入数字和字母组合-组合搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入数字和字母组合（如ce123）进行搜索
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("e1")
        time.sleep(3)
        if not scg.is_text_contain_present_("e123"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0345(self):
        """转发/批量转发-选择团队联系人-企业列表页面-输入汉字和字母组合-组合搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入汉字和字母组合（如ce试）进行搜索
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("b测")
        time.sleep(3)
        if not scg.is_text_contain_present_("b测算"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0346(self):
        """转发/批量转发-选择团队联系人-企业列表页面-输入字母和特殊字符组合-组合搜索"""
        # 1、点击选择团队联系人
        # 2、搜索框输入字母和特殊字符组合（如ce @￥  # ）进行搜索
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("a+")
        time.sleep(3)
        if not scg.is_text_contain_present_("a+6.和"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_huangcaizui_A_0347(self):
        """转发/批量转发-选择团队联系人-企业列表页面-输入短号666-搜索"""
        # 1、点击选择团队联系人
        # 2、跳转到企业列表展示页面，输入短号666，搜索联系人
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("666")
        time.sleep(3)
        if not scg.is_text_contain_present_("短号"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_xiaoqiu_0637(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面的文案展示"""
        # 1、发起群聊 / 添加群成员 / 转发 - 选择团队联系人
        # 2、跳转到企业列表展示页面
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        if not scg.is_text_contain_present_("选择联系人"):
            raise AssertionError("页面展示有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_xiaoqiu_0638(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面搜索框中默认文案展示"""
        # 1、发起群聊 / 添加群成员 / 转发 - 选择团队联系人
        # 2、跳转到企业列表展示页面
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        if not scg.is_text_contain_present_("搜索或输入手机号"):
            raise AssertionError("搜索框中默认文案展示有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_xiaoqiu_0639(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-点击搜索框"""
        # 1、发起群聊 / 添加群成员 / 转发 - 选择团队联系人
        # 2、跳转到企业列表展示页面
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.page_down()
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_xiaoqiu_0640(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-搜索框为空时"""
        # 1、发起群聊 / 添加群成员 / 转发 - 选择团队联系人
        # 2、跳转到企业列表展示页面
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_xiaoqiu_0641(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入框存在内容时"""
        # 1、发起群聊 / 添加群成员 / 转发 - 选择团队联系人
        # 2、跳转到企业列表展示页面
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("666")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_xiaoqiu_0642(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-搜索联系人"""
        # 1、发起群聊 / 添加群成员 / 转发 - 选择团队联系人
        # 2、跳转到企业列表展示页面
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("666")
        time.sleep(3)
        if not scg.is_text_contain_present_("短号"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_xiaoqiu_0643(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-上滑联系人"""
        # 1、发起群聊 / 添加群成员 / 转发 - 选择团队联系人
        # 2、跳转到企业列表展示页面
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("大")
        time.sleep(3)
        if not scg.is_text_contain_present_("大佬"):
            raise AssertionError("搜索结果有误")
        scg.page_down()
        scg.page_up()
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_xiaoqiu_0644(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入一个大写字母搜索联系人"""
        # 1、发起群聊 / 添加群成员 / 转发 - 选择团队联系人
        # 2、跳转到企业列表展示页面，输入一个大写字母搜索联系人
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("C")
        time.sleep(3)
        if not scg.is_text_contain_present_("c平5"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_xiaoqiu_0645(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入一个大写字母搜索联系人"""
        # 1、发起群聊 / 添加群成员 / 转发 - 选择团队联系人
        # 2、跳转到企业列表展示页面，输入一个大写字母搜索联系人
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("Q")
        time.sleep(3)
        if not scg.is_text_contain_present_("无搜索结果"):
            raise AssertionError("搜索结果有误")
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_xiaoqiu_0646(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入2个大写字母搜索联系人"""
        # 1、发起群聊 / 添加群成员 / 转发 - 选择团队联系人
        # 2、跳转到企业列表展示页面，输入2个大写字母搜索联系人
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("AL")
        time.sleep(3)
        if not scg.is_text_contain_present_("alice"):
            raise AssertionError("搜索结果有误")
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_xiaoqiu_0647(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入2个大写字母搜索联系人"""
        # 1、发起群聊 / 添加群成员 / 转发 - 选择团队联系人
        # 2、跳转到企业列表展示页面，输入2个大写字母搜索联系人
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("QQ")
        time.sleep(3)
        if not scg.is_text_contain_present_("无搜索结果"):
            raise AssertionError("搜索结果有误")
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_xiaoqiu_0648(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入一个小写字母搜索联系人"""
        # 1、发起群聊 / 添加群成员 / 转发 - 选择团队联系人
        # 2、跳转到企业列表展示页面，输入一个小写字母搜索联系人
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("c")
        time.sleep(3)
        if not scg.is_text_contain_present_("c平5"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_xiaoqiu_0649(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入一个小写字母搜索联系人"""
        # 1、发起群聊 / 添加群成员 / 转发 - 选择团队联系人
        # 2、跳转到企业列表展示页面，输入一个小写字母搜索联系人
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("q")
        time.sleep(3)
        if not scg.is_text_contain_present_("无搜索结果"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)

    @tags('ALL', 'CMCC', 'YYX')
    def test_msg_xiaoqiu_0650(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入2个小写字母搜索联系人"""
        # 1、发起群聊 / 添加群成员 / 转发 - 选择团队联系人
        # 2、跳转到企业列表展示页面，输入2个小写字母搜索联系人
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击新建消息
        mp.click_element_("发起群聊")
        time.sleep(2)
        scg = SelectContactsPage()
        time.sleep(2)
        scg.click_element_("选择一个群")
        time.sleep(3)
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name("群聊1")
        time.sleep(3)
        chat = GroupChatPage()
        chat.make_sure_chatwindow_have_message()
        # 1、长按文本消息，选择转发功能，跳转到联系人选择器页面（群聊文本消息id无法获取,长按使用坐标长按）
        chat.press_last_text_message()
        time.sleep(2)
        chat.click_forward()
        time.sleep(2)
        scg.click_text("选择团队联系人")
        time.sleep(3)
        scg.click_element_("搜索或输入手机号")
        time.sleep(3)
        scg.search("al")
        time.sleep(3)
        if not scg.is_text_contain_present_("alice"):
            raise AssertionError("搜索结果有误")
        time.sleep(3)


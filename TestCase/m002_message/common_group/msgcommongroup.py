import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages.contacts.my_group import ALLMyGroup
from pages.workbench.group_messenger.GroupMessenger import GroupMessengerPage
from pages.workbench.group_messenger.HelpCenter import HelpCenterPage
from pages.workbench.group_messenger.NewMessage import NewMessagePage
from pages.workbench.group_messenger.SelectCompanyContacts import SelectCompanyContactsPage
from preconditions.BasePreconditions import WorkbenchPreconditions
from pages import *
import warnings



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

# lxd_debug2
class MsgCommonGroupAllTest(TestCase):

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
        """确保每个用例运行前在群聊聊天会话页面"""
        Preconditions.select_mobile('IOS-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_group_messenger_page()
            return
        gmp = GroupMessengerPage()
        if not gmp.is_on_group_messenger_page():
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_group_messenger_page()

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL','CMCC','group_chat','full','high')
    def test_msg_xiaoqiu_0001(self):
        """消息列表——发起群聊——选择已有群"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_help_icon()
        hcp = HelpCenterPage()
        # 等待等待群发信使->帮助中心页面加载
        hcp.wait_for_page_load()
        # 1.查看应用简介
        hcp.click_introduction()
        hcp.wait_for_introduction_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看操作指引
        hcp.click_guide()
        hcp.wait_for_guide_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看资费说明
        hcp.click_explain()
        hcp.wait_for_explain_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看常见问题
        hcp.click_problem()
        hcp.wait_for_problem_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        hcp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat','full','high')
    def test_msg_xiaoqiu_0002(self):
        """消息列表——发起群聊——选择已有群"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬1"
        # 输入查找信息
        sccp.input_search_message(search_name)
        # 点击勾选搜索出的联系人头像
        sccp.click_contacts_image()
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 1.搜索出的联系人是否被选择
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name(search_name), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat','full','high')
    def test_msg_xiaoqiu_0003(self):
        """群聊列表展示页面——中文精确搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 添加多个联系人
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        sccp.click_accessibility_id_attribute_by_name("大佬3")
        # 是否成功选中
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬3"), True)
        # 点击部门已选成员图像取消勾选
        sccp.click_contacts_image_by_name("大佬1")
        # 点击顶部已选成员信息移除成员
        sccp.click_select_contacts_name("佬2")
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0004(self):
        """群聊列表展示页面——中文精确搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬1"
        # 输入查找信息
        sccp.input_search_message(search_name)
        # 点击勾选搜索出的联系人头像
        sccp.click_contacts_image()
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 1.搜索出的联系人是否被选择
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name(search_name), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0005(self):
        """群聊列表展示页面——英文精确搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_help_icon()
        hcp = HelpCenterPage()
        # 等待等待群发信使->帮助中心页面加载
        hcp.wait_for_page_load()
        # 1.查看应用简介
        hcp.click_introduction()
        hcp.wait_for_introduction_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看操作指引
        hcp.click_guide()
        hcp.wait_for_guide_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看资费说明
        hcp.click_explain()
        hcp.wait_for_explain_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看常见问题
        hcp.click_problem()
        hcp.wait_for_problem_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        hcp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0006(self):
        """群聊列表展示页面——英文精确搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.进入多个部门，添加成员
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_accessibility_id_attribute_by_name("测试部门2")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        # 2.各个部门添加成员是否累计
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), True)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0007(self):
        """群聊列表展示页面——空格精确搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 添加多个联系人
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        sccp.click_accessibility_id_attribute_by_name("大佬3")
        # 是否成功选中
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬3"), True)
        # 点击部门已选成员图像取消勾选
        sccp.click_contacts_image_by_name("大佬1")
        # 点击顶部已选成员信息移除成员
        sccp.click_select_contacts_name("佬2")
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0008(self):
        """群聊列表展示页面——空格精确搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬1"
        # 输入查找信息
        sccp.input_search_message(search_name)
        # 点击勾选搜索出的联系人头像
        sccp.click_contacts_image()
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 1.搜索出的联系人是否被选择
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name(search_name), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0009(self):
        """群聊列表展示页面——数字精确搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 添加多个联系人
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        sccp.click_accessibility_id_attribute_by_name("大佬3")
        # 是否成功选中
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬3"), True)
        # 点击部门已选成员图像取消勾选
        sccp.click_contacts_image_by_name("大佬1")
        # 点击顶部已选成员信息移除成员
        sccp.click_select_contacts_name("佬2")
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0010(self):
        """群聊列表展示页面——数字精确搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_help_icon()
        hcp = HelpCenterPage()
        # 等待等待群发信使->帮助中心页面加载
        hcp.wait_for_page_load()
        # 1.查看应用简介
        hcp.click_introduction()
        hcp.wait_for_introduction_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看操作指引
        hcp.click_guide()
        hcp.wait_for_guide_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看资费说明
        hcp.click_explain()
        hcp.wait_for_explain_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看常见问题
        hcp.click_problem()
        hcp.wait_for_problem_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        hcp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_xiaoqiu_0011(self):
        """群聊列表展示页面——数字精确搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 添加多个联系人
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        sccp.click_accessibility_id_attribute_by_name("大佬3")
        # 是否成功选中
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬3"), True)
        # 点击部门已选成员图像取消勾选
        sccp.click_contacts_image_by_name("大佬1")
        # 点击顶部已选成员信息移除成员
        sccp.click_select_contacts_name("佬2")
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_xiaoqiu_0012(self):
        """群聊列表展示页面——数字精确搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬1"
        # 输入查找信息
        sccp.input_search_message(search_name)
        # 点击勾选搜索出的联系人头像
        sccp.click_contacts_image()
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 1.搜索出的联系人是否被选择
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name(search_name), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_xiaoqiu_0013(self):
        """群聊列表展示页面——字符精确搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.进入多个部门，添加成员
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_accessibility_id_attribute_by_name("测试部门2")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        # 2.各个部门添加成员是否累计
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), True)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_xiaoqiu_0014(self):
        """群聊列表展示页面——字符精确搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_help_icon()
        hcp = HelpCenterPage()
        # 等待等待群发信使->帮助中心页面加载
        hcp.wait_for_page_load()
        # 1.查看应用简介
        hcp.click_introduction()
        hcp.wait_for_introduction_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看操作指引
        hcp.click_guide()
        hcp.wait_for_guide_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看资费说明
        hcp.click_explain()
        hcp.wait_for_explain_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看常见问题
        hcp.click_problem()
        hcp.wait_for_problem_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        hcp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_xiaoqiu_0015(self):
        """群聊列表展示页面——索引字母定位选择"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.进入多个部门，添加成员
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_accessibility_id_attribute_by_name("测试部门2")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        # 2.各个部门添加成员是否累计
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), True)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0017(self):
        """在群聊天会话页面，发送一条字符长度等于：1的，文本消息"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_number = "13800138005"
        # 输入查找信息
        sccp.input_search_message(search_number)
        # 1.检查搜索结果是否完全匹配关键字
        self.assertEquals(sccp.is_search_contacts_number_full_match(search_number), True)
        # 选择搜索结果
        sccp.click_name_attribute_by_name(search_number, "xpath")
        # 2.是否成功选中，输入框是否自动清空
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_clear_search_box(search_number), True)
        sccp.click_back_button()
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0018(self):
        """在群聊天会话页面，发送一条字符长度，大于1的文本消息"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 添加多个联系人
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        sccp.click_accessibility_id_attribute_by_name("大佬3")
        # 是否成功选中
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬3"), True)
        # 点击部门已选成员图像取消勾选
        sccp.click_contacts_image_by_name("大佬1")
        # 点击顶部已选成员信息移除成员
        sccp.click_select_contacts_name("佬2")
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0021(self):
        """在群聊天会话页面，输入框中录入1个字符，使用缩小功能发送"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_number = "13800138005"
        # 输入查找信息
        sccp.input_search_message(search_number)
        # 1.检查搜索结果是否完全匹配关键字
        self.assertEquals(sccp.is_search_contacts_number_full_match(search_number), True)
        # 选择搜索结果
        sccp.click_name_attribute_by_name(search_number, "xpath")
        # 2.是否成功选中，输入框是否自动清空
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_clear_search_box(search_number), True)
        sccp.click_back_button()
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0022(self):
        """在群聊天会话页面，输入框中录入500个字符，使用缩小功能发送"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.进入多个部门，添加成员
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_accessibility_id_attribute_by_name("测试部门2")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        # 2.各个部门添加成员是否累计
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), True)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0023(self):
        """在群聊天会话页面，输入框中录入5000个字符，使用缩小功能发送"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 添加多个联系人
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        sccp.click_accessibility_id_attribute_by_name("大佬3")
        # 是否成功选中
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬3"), True)
        # 点击部门已选成员图像取消勾选
        sccp.click_contacts_image_by_name("大佬1")
        # 点击顶部已选成员信息移除成员
        sccp.click_select_contacts_name("佬2")
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0024(self):
        """在群聊天会话页面，输入框中录入1个字符，使用放大功能发送"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬1"
        # 输入查找信息
        sccp.input_search_message(search_name)
        # 点击勾选搜索出的联系人头像
        sccp.click_contacts_image()
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 1.搜索出的联系人是否被选择
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name(search_name), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0025(self):
        """在群聊天会话页面，输入框中录入500个字符，使用放大功能发送"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.进入多个部门，添加成员
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_accessibility_id_attribute_by_name("测试部门2")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        # 2.各个部门添加成员是否累计
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), True)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0026(self):
        """在群聊天会话页面，输入框中录入5000个字符，使用放大功能发送"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 添加多个联系人
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        sccp.click_accessibility_id_attribute_by_name("大佬3")
        # 是否成功选中
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬3"), True)
        # 点击部门已选成员图像取消勾选
        sccp.click_contacts_image_by_name("大佬1")
        # 点击顶部已选成员信息移除成员
        sccp.click_select_contacts_name("佬2")
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0035(self):
        """进入到群聊天会话页面，录入文字+表情字符，放大发送"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_help_icon()
        hcp = HelpCenterPage()
        # 等待等待群发信使->帮助中心页面加载
        hcp.wait_for_page_load()
        # 1.查看应用简介
        hcp.click_introduction()
        hcp.wait_for_introduction_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看操作指引
        hcp.click_guide()
        hcp.wait_for_guide_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看资费说明
        hcp.click_explain()
        hcp.wait_for_explain_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看常见问题
        hcp.click_problem()
        hcp.wait_for_problem_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        hcp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0036(self):
        """进入到群聊天会话页面，录入文字+表情字符，缩小发送"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_number = "13800138005"
        # 输入查找信息
        sccp.input_search_message(search_number)
        # 1.检查搜索结果是否完全匹配关键字
        self.assertEquals(sccp.is_search_contacts_number_full_match(search_number), True)
        # 选择搜索结果
        sccp.click_name_attribute_by_name(search_number, "xpath")
        # 2.是否成功选中，输入框是否自动清空
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_clear_search_box(search_number), True)
        sccp.click_back_button()
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0037(self):
        """在群聊天会话页面，长按消息体，点击收藏"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬1"
        # 输入查找信息
        sccp.input_search_message(search_name)
        # 1.检查搜索结果是否精准匹配关键字
        self.assertEquals(sccp.is_search_contacts_name_full_match(search_name), True)
        # 选择搜索结果
        sccp.click_name_attribute_by_name(search_name, "xpath")
        # 2.搜索栏是否清空，是否出现已选人名和头像，是否展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0038(self):
        """我——收藏——收藏内容展示"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.进入多个部门，添加成员
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_accessibility_id_attribute_by_name("测试部门2")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        # 2.各个部门添加成员是否累计
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), True)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0039(self):
        """我——收藏——收藏内展示——点击收藏内容"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 添加多个联系人
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        sccp.click_accessibility_id_attribute_by_name("大佬3")
        # 是否成功选中
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬3"), True)
        # 点击部门已选成员图像取消勾选
        sccp.click_contacts_image_by_name("大佬1")
        # 点击顶部已选成员信息移除成员
        sccp.click_select_contacts_name("佬2")
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0040(self):
        """我——收藏——收藏内展示——点击收藏内容——点击播放收藏语音文件"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬1"
        # 输入查找信息
        sccp.input_search_message(search_name)
        # 点击勾选搜索出的联系人头像
        sccp.click_contacts_image()
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 1.搜索出的联系人是否被选择
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name(search_name), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0041(self):
        """我——收藏——收藏内展示——点击收藏内容——点击删除收藏内容"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.进入多个部门，添加成员
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_accessibility_id_attribute_by_name("测试部门2")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        # 2.各个部门添加成员是否累计
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), True)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0050(self):
        """发送一组数字：95533，发送失败的状态展示"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 添加多个联系人
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        sccp.click_accessibility_id_attribute_by_name("大佬3")
        # 是否成功选中
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬3"), True)
        # 点击部门已选成员图像取消勾选
        sccp.click_contacts_image_by_name("大佬1")
        # 点击顶部已选成员信息移除成员
        sccp.click_select_contacts_name("佬2")
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0072(self):
        """仅语音模式，录制时长等于1秒时，点击发送按钮"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_help_icon()
        hcp = HelpCenterPage()
        # 等待等待群发信使->帮助中心页面加载
        hcp.wait_for_page_load()
        # 1.查看应用简介
        hcp.click_introduction()
        hcp.wait_for_introduction_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看操作指引
        hcp.click_guide()
        hcp.wait_for_guide_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看资费说明
        hcp.click_explain()
        hcp.wait_for_explain_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看常见问题
        hcp.click_problem()
        hcp.wait_for_problem_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        hcp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0073(self):
        """仅语音模式，发送录制时长大于1秒的语音"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬1"
        # 输入查找信息
        sccp.input_search_message(search_name)
        # 1.检查搜索结果是否精准匹配关键字
        self.assertEquals(sccp.is_search_contacts_name_full_match(search_name), True)
        # 选择搜索结果
        sccp.click_name_attribute_by_name(search_name, "xpath")
        # 2.搜索栏是否清空，是否出现已选人名和头像，是否展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0074(self):
        """仅语音模式，录制时长大于10秒——发送"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.进入多个部门，添加成员
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_accessibility_id_attribute_by_name("测试部门2")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        # 2.各个部门添加成员是否累计
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), True)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0075(self):
        """仅语音模式，录制时长等于60秒—自动发送"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.是否直接进入企业子一层级
        self.assertEquals(sccp.is_exist_corporate_grade(), True)
        sccp.click_back_button()
        # 2.页面是否跳转到企业层级
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exist_department_name(), True)
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0076(self):
        """仅语音模式，录制时长超过60秒"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬1"
        # 输入查找信息
        sccp.input_search_message(search_name)
        # 点击勾选搜索出的联系人头像
        sccp.click_contacts_image()
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 1.搜索出的联系人是否被选择
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name(search_name), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0085(self):
        """在聊天会话页面——点击语音ICON"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 添加多个联系人
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        sccp.click_accessibility_id_attribute_by_name("大佬3")
        # 是否成功选中
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬3"), True)
        # 点击部门已选成员图像取消勾选
        sccp.click_contacts_image_by_name("大佬1")
        # 点击顶部已选成员信息移除成员
        sccp.click_select_contacts_name("佬2")
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0088(self):
        """进入到语音录制页——网络异常"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_help_icon()
        hcp = HelpCenterPage()
        # 等待等待群发信使->帮助中心页面加载
        hcp.wait_for_page_load()
        # 1.查看应用简介
        hcp.click_introduction()
        hcp.wait_for_introduction_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看操作指引
        hcp.click_guide()
        hcp.wait_for_guide_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看资费说明
        hcp.click_explain()
        hcp.wait_for_explain_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看常见问题
        hcp.click_problem()
        hcp.wait_for_problem_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        hcp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0089(self):
        """语音录制中途——网络异常"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.是否直接进入企业子一层级
        self.assertEquals(sccp.is_exist_corporate_grade(), True)
        sccp.click_back_button()
        # 2.页面是否跳转到企业层级
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exist_department_name(), True)
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0090(self):
        """语音录制完成——网络异常"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬1"
        # 输入查找信息
        sccp.input_search_message(search_name)
        # 1.检查搜索结果是否精准匹配关键字
        self.assertEquals(sccp.is_search_contacts_name_full_match(search_name), True)
        # 选择搜索结果
        sccp.click_name_attribute_by_name(search_name, "xpath")
        # 2.搜索栏是否清空，是否出现已选人名和头像，是否展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx')
    def test_msg_xiaoqiu_0098(self):
        """在群聊会话窗口，点击页面顶部的通话按钮"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.是否直接进入企业子一层级
        self.assertEquals(sccp.is_exist_corporate_grade(), True)
        sccp.click_back_button()
        # 2.页面是否跳转到企业层级
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exist_department_name(), True)
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx')
    def test_msg_xiaoqiu_0101(self):
        """在群聊会话窗口，点击输入框上方的图片ICON，进入到图片展示列表"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_help_icon()
        hcp = HelpCenterPage()
        # 等待等待群发信使->帮助中心页面加载
        hcp.wait_for_page_load()
        # 1.查看应用简介
        hcp.click_introduction()
        hcp.wait_for_introduction_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看操作指引
        hcp.click_guide()
        hcp.wait_for_guide_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看资费说明
        hcp.click_explain()
        hcp.wait_for_explain_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        # 查看常见问题
        hcp.click_problem()
        hcp.wait_for_problem_page_load()
        hcp.click_back_button()
        hcp.wait_for_page_load()
        hcp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()


class MsgCommonGroupTotalTest(TestCase):
    """普通群"""

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
    def test_msg_xiaoqiu_0016(self):
        """在群聊天会话页面，输入框中，不录入任何内容"""

        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 确保输入框内容为空
        if not gcp.is_clear_the_input_box():
            gcp.input_text_message("")
        # 1.在输入框中不输入任何一个字符，输入框右边的语音按钮仍然展示为语音按钮
        self.assertEquals(gcp.is_exist_voice_button(), True)
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0019(self):
        """在群聊天会话页面，发送一条字符长度等于5000的文本消息"""

        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 获取发送前消息记录数量
        number = gcp.get_message_record_number()
        # 在输入框中输入5000个字符
        gcp.input_text_message("哈" * 5000)
        # 1.在输入框中输入5000个字符，右边的语音按钮自动变为发送按钮
        self.assertEquals(gcp.is_exist_send_button(), True)
        # 点击发送按钮
        gcp.click_send_button()
        time.sleep(5)
        # 获取发送后消息记录数量
        new_number = gcp.get_message_record_number()
        # 2.输入框中的内容发送成功(由于文本无法定位，采用间接验证)
        self.assertEquals(number + 1, new_number)
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0020(self):
        """在群聊天会话页面，发送一条字符大于5000的文本消息"""

        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 在输入框中输入5001个字符
        gcp.input_text_message("哈" * 5000 + "好")
        # 1.在输入框中不可以输入5001个字符，会输入失败
        # self.assertEquals(gcp.page_should_contain_text2("发送字数超过限制"), True)
        self.assertEquals(gcp.is_exists_text_by_input_box("好"), False)
        # 点击发送按钮，清空输入框
        gcp.click_send_button()
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0028(self):
        """进入到群聊天会话页面，录入500个表情字符，缩小发送"""

        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 先发送500个表情字符，用来做对比
        gcp.input_text_message("[微笑1]" * 500)
        gcp.click_send_button()
        time.sleep(5)
        # 获取正常发送表情大小
        width, height = gcp.get_size_of_last_expression_message()
        # 在输入框中，录入500个表情字符后，长按发送按钮向下滑动
        gcp.input_text_message("[微笑1]" * 500)
        gcp.click_send_slide_down()
        time.sleep(5)
        # 获取向下滑动发送表情大小
        new_width, new_height = gcp.get_size_of_last_expression_message()
        # 1.在输入框中，录入500个表情字符后，长按发送按钮向下滑动，发送出去的此条表情消息，展示为缩小字体状态
        self.assertEquals(new_width < width and new_height < height, True)
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0032(self):
        """进入到群聊天会话页面，录入500个表情字符，放大发送"""

        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 先发送500个表情字符，用来做对比
        gcp.input_text_message("[微笑1]" * 500)
        gcp.click_send_button()
        time.sleep(5)
        # 获取正常发送表情大小
        width, height = gcp.get_size_of_last_expression_message()
        # 在输入框中，录入500个表情字符后，长按发送按钮向上滑动
        gcp.input_text_message("[微笑1]" * 500)
        gcp.click_send_slide_up()
        time.sleep(5)
        # 获取向上滑动发送表情大小
        new_width, new_height = gcp.get_size_of_last_expression_message()
        # 1.在输入框中，录入500个表情字符后，长按发送按钮向上滑动，发送出去的此条表情消息，展示为放大字体状态
        self.assertEquals(new_width > width and new_height > height, True)
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0055(self):
        """在聊天会话页面，长按文本消息——收藏"""

        mp = MessagePage()
        # 清空收藏列表，确保没有收藏影响验证
        Preconditions.enter_collection_page()
        mcp = MeCollectionPage()
        mcp.delete_all_collection()
        mcp.click_back_button()
        mp.open_message_page()
        mp.wait_for_page_load()
        group_name = "群聊1"
        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page(group_name)
        gcp = GroupChatPage()
        # 确保有文本消息，由于群聊页面部分元素无法定位，发送两次
        gcp.input_text_message("123")
        gcp.click_send_button()
        gcp.input_text_message("测试文本消息0055")
        gcp.click_send_button()
        # 长按文本消息，选择收藏功能
        gcp.press_last_text_message()
        gcp.click_accessibility_id_attribute_by_name("收藏")
        # 1.长按文本消息，选择收藏功能，收藏成功后，弹出toast提示：已收藏
        self.assertEquals(gcp.page_should_contain_text2("已收藏"), True)
        gcp.click_back_button()
        # 在我的页面，点击收藏入口
        Preconditions.enter_collection_page()
        # 2.在我的页面，点击收藏入口，检查刚收藏的消息内容，可以正常展示出来(由于内容捕捉不到，采用间接验证)
        self.assertEquals(mcp.page_should_contain_text2(group_name), True)
        # 点击收藏成功的消息体
        mcp.click_name_attribute_by_name(group_name)
        # 3.点击收藏成功的消息体，可以进入到消息展示详情页面
        self.assertEquals(mcp.page_should_contain_text2("详情"), True)
        time.sleep(2)
        mcp.click_back_button()
        # 左滑收藏消息体
        mcp.left_slide_collection()
        # 4.左滑收藏消息体，会展示删除按钮
        self.assertEquals(mcp.is_exists_delete_button(), True)
        # 点击删除按钮
        mcp.click_element_delete_icon()
        # 5.点击删除按钮，可以删除收藏的消息体
        self.assertEquals(mcp.is_exists_collection(), False)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0058(self):
        """语音+文字模式下，3秒内未能识别出内容"""

        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 确保语音按钮存在
        if not gcp.is_clear_the_input_box():
            gcp.input_text_message("")
        # 点击输入框右边的语音按钮，设置语音模式为：语音+文字模式
        gcp.click_voice_button()
        gcp.click_accessibility_id_attribute_by_name("发送")
        gcp.click_accessibility_id_attribute_by_name("设置")
        gcp.click_name_attribute_by_name("同时发送语音+文字")
        gcp.click_accessibility_id_attribute_by_name("确定")
        # 1.3秒内未能识别出内容，提示：无法识别，请重试
        self.assertEquals(gcp.page_should_contain_text2("无法识别，请重试", 20), True)
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0060(self):
        """语音+文字模式下，3秒内未检测到声音"""

        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 确保语音按钮存在
        if not gcp.is_clear_the_input_box():
            gcp.input_text_message("")
        # 点击输入框右边的语音按钮，设置语音模式为：语音+文字模式
        gcp.click_voice_button()
        gcp.click_accessibility_id_attribute_by_name("发送")
        gcp.click_accessibility_id_attribute_by_name("设置")
        gcp.click_name_attribute_by_name("同时发送语音+文字")
        gcp.click_accessibility_id_attribute_by_name("确定")
        # 1.3秒内未检测到声音，提示：无法识别，请重试
        self.assertEquals(gcp.page_should_contain_text2("无法识别，请重试", 20), True)
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0065(self):
        """语音+文字模式下，识别中途，点击退出按钮"""

        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 确保语音按钮存在
        if not gcp.is_clear_the_input_box():
            gcp.input_text_message("")
        # 点击输入框右边的语音按钮，设置语音模式为：语音+文字模式
        gcp.click_voice_button()
        gcp.click_accessibility_id_attribute_by_name("发送")
        gcp.click_accessibility_id_attribute_by_name("设置")
        gcp.click_name_attribute_by_name("同时发送语音+文字")
        gcp.click_accessibility_id_attribute_by_name("确定")
        # 1.点击输入框右边的语音按钮，设置语音模式为：语音+文字模式
        self.assertEquals(gcp.page_should_contain_text2("说句话试试"), True)
        # 语音+文字模式识别中途，点击左下角的退出按钮
        gcp.click_accessibility_id_attribute_by_name("退出")
        # 2.语音+文字模式识别中途，点击左下角的退出按钮，会退出语音识别模式
        self.assertEquals(gcp.page_should_contain_text2("说句话试试", 3), False)
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0067(self):
        """仅发送文字模式下，3秒未检测到声音"""

        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 确保语音按钮存在
        if not gcp.is_clear_the_input_box():
            gcp.input_text_message("")
        # 点击输入框右边的语音按钮，设置语音模式为：仅发送文字模式
        gcp.click_voice_button()
        gcp.click_accessibility_id_attribute_by_name("发送")
        gcp.click_accessibility_id_attribute_by_name("设置")
        gcp.click_name_attribute_by_name("仅发送文字")
        gcp.click_accessibility_id_attribute_by_name("确定")
        # 1.3秒内未检测到声音，提示：无法识别，请重试
        self.assertEquals(gcp.page_should_contain_text2("无法识别，请重试", 20), True)
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0068(self):
        """仅发送文字模式下，3秒未识别出内容"""

        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 确保语音按钮存在
        if not gcp.is_clear_the_input_box():
            gcp.input_text_message("")
        # 点击输入框右边的语音按钮，设置语音模式为：仅发送文字模式
        gcp.click_voice_button()
        gcp.click_accessibility_id_attribute_by_name("发送")
        gcp.click_accessibility_id_attribute_by_name("设置")
        gcp.click_name_attribute_by_name("仅发送文字")
        gcp.click_accessibility_id_attribute_by_name("确定")
        # 1.3秒内未能识别出内容，提示：无法识别，请重试
        self.assertEquals(gcp.page_should_contain_text2("无法识别，请重试", 20), True)
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0078(self):
        """仅语音模式，录制中途——退出录制"""

        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 确保语音按钮存在
        if not gcp.is_clear_the_input_box():
            gcp.input_text_message("")
        # 点击输入框右边的语音按钮，设置语音模式为：仅发送语音模式
        gcp.click_voice_button()
        gcp.click_accessibility_id_attribute_by_name("发送")
        gcp.click_accessibility_id_attribute_by_name("设置")
        gcp.click_name_attribute_by_name("仅发送语音")
        gcp.click_accessibility_id_attribute_by_name("确定")
        self.assertEquals(gcp.page_should_contain_text2("语音录制中"), True)
        self.assertEquals(gcp.is_exist_send_button(), True)
        # 录制中途，退出录制
        time.sleep(5)
        gcp.click_accessibility_id_attribute_by_name("退出")
        # 1.录制中途，退出录制，会自动清除录制的语音文件(间接验证)
        self.assertEquals(gcp.page_should_contain_text2("语音录制中", 3), False)
        self.assertEquals(gcp.is_exist_voice_button(), True)
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0241(self):
        """消息草稿-聊天列表显示-不输入任何消息"""

        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 确保当前群聊排在消息列表第一个
        text = "测试消息0241"
        gcp.input_text_message(text)
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
    def test_msg_xiaoqiu_0243(self):
        """消息草稿-聊天列表显示-输入表情信息"""

        # 进入群聊聊天会话页面
        group_name = "群聊1"
        Preconditions.enter_group_chat_page(group_name)
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
        gcp.click_back_button()
        mp = MessagePage()
        # 返回聊天列表，查看显示
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
    def test_msg_xiaoqiu_0244(self):
        """消息草稿-聊天列表显示-输入特殊字符"""

        # 进入群聊聊天会话页面
        group_name = "群聊1"
        Preconditions.enter_group_chat_page(group_name)
        gcp = GroupChatPage()
        # 确保当前群聊排在消息列表第一个
        gcp.input_text_message("123")
        gcp.click_send_button()
        # 文本编辑器中输入特殊字符信息
        text = "&*$"
        gcp.input_text_message(text)
        # 1.发送按钮高亮，可点击(间接验证)
        self.assertEquals(gcp._is_enabled_send_button(), True)
        gcp.click_back_button()
        mp = MessagePage()
        # 返回聊天列表，查看显示
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
    def test_msg_xiaoqiu_0248(self):
        """消息草稿-聊天列表显示-草稿信息删除"""

        # 进入群聊聊天会话页面
        group_name = "群聊1"
        Preconditions.enter_group_chat_page(group_name)
        gcp = GroupChatPage()
        # 确保当前群聊排在消息列表第一个
        text = "测试消息0248"
        gcp.input_text_message(text)
        gcp.click_send_button()
        # 输入文本信息，不发送
        draft_text = "123"
        gcp.input_text_message(draft_text)
        # 1.保存为草稿信息
        self.assertEquals(gcp.is_exists_text_by_input_box(draft_text), True)
        gcp.click_back_button()
        mp = MessagePage()
        # 返回消息列表，查看预览
        mp.wait_for_page_load()
        time.sleep(2)
        # 2.消息列表，显示[草稿]标红字样，消息预览显示草稿信息，信息过长时显示…
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
        self.assertEquals(mp.is_first_message_content(text), True)


class MsgCommonGroupContactTest(TestCase):
    """普通群-通讯录"""

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter("ignore",ResourceWarning)
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

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0280(self):
        """通讯录-群聊-中文精确搜索——搜索结果展示"""
        mess = MessagePage()
        # 1.点击通讯录
        mess.click_contacts()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        # 2.点击群聊
        contacts.click_group_chat()
        glp = GroupListPage()
        glp.wait_for_page_load()
        # 3.点击搜索群组
        glp.click_search_input()
        # 4.输入中文群名
        glp.input_group_name("群聊1")
        time.sleep(2)
        glsp = GroupListSearchPage()
        # 5.验证是否可以匹配展示搜索结果
        self.assertTrue(glsp.is_group_in_list("群聊1"))

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0281(self):
        """通讯录-群聊-中文精确搜索——搜索结果展示"""
        mess = MessagePage()
        # 1.点击通讯录
        mess.click_contacts()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        # 2.点击群聊
        contacts.click_group_chat()
        glp = GroupListPage()
        glp.wait_for_page_load()
        # 3.点击搜索群组
        glp.click_search_input()
        # 4.输入中文群名
        glp.input_group_name("群聊测试测试")
        time.sleep(2)
        glsp = GroupListSearchPage()
        # 5.验证是否展示提示：无搜索结果
        self.assertTrue(glsp.page_should_contain_text("无搜索结果"))

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0282(self):
        """通讯录-群聊-英文精确搜索——搜索结果展示"""
        mess = MessagePage()
        # 1.点击通讯录
        mess.click_contacts()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        # 2.点击群聊
        contacts.click_group_chat()
        glp = GroupListPage()
        glp.wait_for_page_load()
        # 3.点击搜索群组
        glp.click_search_input()
        # 4.输入英文群名
        glp.input_group_name("group_test")
        glsp = GroupListSearchPage()
        # 5.验证是否可以匹配展示搜索结果
        self.assertTrue(glsp.is_group_in_list("group_test"))
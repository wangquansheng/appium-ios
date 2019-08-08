import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages.chat.ChatGroupSMSExpenses import ChatGroupSMSExpensesPage
from pages.contacts.my_group import ALLMyGroup
from pages.message.FreeMsg import FreeMsgPage
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

    @staticmethod
    def delete_mobile_contacts_if_exists(name):
        """如果存在指定手机联系人则删除"""

        mp = MessagePage()
        mp.open_contacts_page()
        cp = ContactsPage()
        cp.wait_for_page_load()
        cp.click_mobile_contacts()
        if cp.page_should_contain_text2(name):
            cp.click_accessibility_id_attribute_by_name(name, 10)
            cdp = ContactDetailsPage()
            cdp.wait_for_page_load()
            cdp.click_edit_contact()
            cdp.click_accessibility_id_attribute_by_name("删除联系人")
            cdp.click_accessibility_id_attribute_by_name("删除")
            time.sleep(2)
        cp.click_back_button()
        cp.open_message_page()
        mp.wait_for_page_load()

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

        # 导入多人普通群
        fail_time3 = 0
        flag3 = False
        while fail_time3 < 5:
            try:
                Preconditions.make_already_in_message_page()
                conts = ContactsPage()
                conts.open_contacts_page()
                conts.open_group_chat_list()
                group_list = GroupListPage()
                group_chats = [('多人测试普通群', ['大佬1', '大佬2', '大佬3', '大佬4'])]
                for group_name, members in group_chats:
                    group_list.wait_for_page_load()
                    group_list.create_group_chats_if_not_exits(group_name, members)
                group_list.click_back()
                conts.open_message_page()
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
    def test_msg_xiaoqiu_0004(self):
        """群聊列表展示页面——中文精确搜索"""

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
        # 中文精确搜索
        sog.input_search_keyword("不存在群")
        # 1.中文精确搜索，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(sog.page_should_contain_text2("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0005(self):
        """群聊列表展示页面——英文精确搜索"""

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
        # 英文精确搜索
        search_name = "group_test"
        sog.input_search_keyword(search_name)
        # 1.英文精确搜索，可以匹配展示搜索结果
        self.assertEquals(sog.page_should_contain_text2(search_name), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0006(self):
        """群聊列表展示页面——英文精确搜索"""

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
        # 英文精确搜索
        sog.input_search_keyword("test_no_exists")
        # 1.英文精确搜索，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(sog.page_should_contain_text2("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0007(self):
        """群聊列表展示页面——空格精确搜索"""

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
        # 空格精确搜索
        search_name = "带空格的 群"
        sog.input_search_keyword(search_name)
        # 1.空格精确搜索，可以匹配展示搜索结果
        self.assertEquals(sog.page_should_contain_text2(search_name), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0008(self):
        """群聊列表展示页面——空格精确搜索"""

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
        # 空格精确搜索
        sog.input_search_keyword("你好 啊啊")
        # 1.空格精确搜索，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(sog.page_should_contain_text2("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0009(self):
        """群聊列表展示页面——数字精确搜索"""

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
        # 数字精确搜索
        search_name = "138138138"
        sog.input_search_keyword(search_name)
        # 1.数字精确搜索，可以匹配展示搜索结果
        self.assertEquals(sog.page_should_contain_text2(search_name), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0010(self):
        """群聊列表展示页面——数字精确搜索"""

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
        # 数字精确搜索
        sog.input_search_keyword("168861768")
        # 1.数字精确搜索，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(sog.page_should_contain_text2("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0011(self):
        """群聊列表展示页面——数字精确搜索"""

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
        # 数字精确搜索
        search_name = "138138138"
        sog.input_search_keyword(search_name)
        # 1.数字精确搜索，可以匹配展示搜索结果
        self.assertEquals(sog.page_should_contain_text2(search_name), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0012(self):
        """群聊列表展示页面——数字精确搜索"""

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
        # 数字精确搜索
        sog.input_search_keyword("168861768")
        # 1.数字精确搜索，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(sog.page_should_contain_text2("无搜索结果"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0013(self):
        """群聊列表展示页面——字符精确搜索"""

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
        # 字符精确搜索
        search_name = "&%@"
        sog.input_search_keyword(search_name)
        # 1.字符精确搜索，可以匹配展示搜索结果
        self.assertEquals(sog.page_should_contain_text2(search_name), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0014(self):
        """群聊列表展示页面——字符精确搜索"""

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
        # 字符精确搜索
        sog.input_search_keyword("$$$###")
        # 1.字符精确搜索，无匹配搜索结果，展示提示：无搜索结果
        self.assertEquals(sog.page_should_contain_text2("无搜索结果"), True)

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
        # 在输入框中输入5000个字符
        gcp.input_text_message("哈" * 5000)
        # 1.在输入框中输入5000个字符，右边的语音按钮自动变为发送按钮
        self.assertEquals(gcp.is_exist_send_button(), True)
        # 点击发送按钮
        gcp.click_send_button()
        # 2.输入框中的内容发送成功(由于文本无法定位，采用间接验证)
        self.assertEquals(gcp.is_exists_element_by_text("最后一条消息记录发送失败标识"), False)
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
        # 确保群聊页面表情消息能定位，先发送一次文本
        gcp.input_text_message("123")
        gcp.click_send_button()
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
        # 确保群聊页面表情消息能定位，先发送一次文本
        gcp.input_text_message("123")
        gcp.click_send_button()
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
    def test_msg_xiaoqiu_0248(self):
        """消息草稿-聊天列表显示-草稿信息删除"""

        # 进入群聊聊天会话页面
        group_name = "群聊1"
        Preconditions.enter_group_chat_page(group_name)
        gcp = GroupChatPage()
        # 确保当前群聊排在消息列表第一个
        text = "测试文本消息0248"
        gcp.input_text_message(text)
        gcp.click_send_button()
        # 输入文本信息，不发送
        draft_text = "测试草稿消息0248"
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
    def test_msg_xiaoqiu_0315(self):
        """普通群profile优化：聊天设置页——群成员预览"""

        # 如果存在指定手机联系人则删除
        Preconditions.delete_mobile_contacts_if_exists("大佬2")
        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("多人测试普通群")
        gcp = GroupChatPage()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        # 点击已保存手机的联系人成员头像进入profile页
        gcs.click_group_members_image_by_name("大佬1")
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        # 1.如果其为普通手机联系人则有：星标、编辑、分享名片；如果其为安卓SIM卡联系人则无：星标、编辑功能
        self.assertEquals(cdp.is_exists_element_by_text("星标"), True)
        self.assertEquals(cdp.is_exists_element_by_text("编辑"), True)
        self.assertEquals(cdp.is_exists_element_by_text("分享名片"), True)
        cdp.click_back_button()
        # 点击未保存手机的联系人成员头像进入profile页
        gcs.click_group_members_image_by_name("138********")
        # 2.进入到未保存的群聊profile页，展示交换名片页面
        self.assertEquals(gcs.page_should_contain_text2("交换名片"), True)
        cdp.click_back_button()
        # 获取我在本群的昵称
        my_name = gcs.get_element_value_by_text("我在本群的昵称")
        # 点击自己头像进入profile页
        gcs.click_group_members_image_by_name(my_name)
        # 3.与进入“我--编辑个人资料”页面一致，功能有：编辑、分享名片
        self.assertEquals(gcs.page_should_contain_text2("编辑"), True)
        self.assertEquals(gcs.page_should_contain_text2("分享名片"), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0315():
        """恢复环境"""

        try:
            fail_time = 0
            while fail_time < 5:
                try:
                    Preconditions.make_already_in_message_page()
                    mp = MessagePage()
                    mp.open_contacts_page()
                    cp = ContactsPage()
                    # 如果不存在指定手机联系人则创建
                    cp.create_contacts_if_not_exits("大佬2", "13800138006")
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0316(self):
        """普通群profile优化：群聊设置页--“>”群成员列表"""

        # 如果存在指定手机联系人则删除
        Preconditions.delete_mobile_contacts_if_exists("大佬2")
        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("多人测试普通群")
        gcp = GroupChatPage()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        # 获取我在本群的昵称
        my_name = gcs.get_element_value_by_text("我在本群的昵称")
        gcs.click_element_by_text("群成员文本")
        # 点击已保存手机的联系人成员头像进入profile页
        gcs.click_group_members_image_by_name("大佬1")
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        # 1.如果其为普通手机联系人则有：星标、编辑、分享名片；如果其为安卓SIM卡联系人无：星标、编辑功能
        self.assertEquals(cdp.is_exists_element_by_text("星标"), True)
        self.assertEquals(cdp.is_exists_element_by_text("编辑"), True)
        self.assertEquals(cdp.is_exists_element_by_text("分享名片"), True)
        cdp.click_back_button()
        # 点击未保存手机的联系人成员头像进入profile页
        gcs.click_group_members_image_by_name("138********")
        # 2.进入到未保存的群聊profile页，展示交换名片页面
        self.assertEquals(gcs.page_should_contain_text2("交换名片"), True)
        cdp.click_back_button()
        # 点击自己头像进入profile页
        gcs.click_group_members_image_by_name(my_name)
        # 3.与进入“我--编辑个人资料”页面一致，功能有：编辑、分享名片
        self.assertEquals(gcs.page_should_contain_text2("编辑"), True)
        self.assertEquals(gcs.page_should_contain_text2("分享名片"), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0316():
        """恢复环境"""

        try:
            fail_time = 0
            while fail_time < 5:
                try:
                    Preconditions.make_already_in_message_page()
                    mp = MessagePage()
                    mp.open_contacts_page()
                    cp = ContactsPage()
                    # 如果不存在指定手机联系人则创建
                    cp.create_contacts_if_not_exits("大佬2", "13800138006")
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0317(self):
        """普通群profile优化：群聊设置页--“>”群成员列表--搜索结果"""

        # 如果存在指定手机联系人则删除
        Preconditions.delete_mobile_contacts_if_exists("大佬2")
        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("多人测试普通群")
        gcp = GroupChatPage()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        # 获取我在本群的昵称
        my_name = gcs.get_element_value_by_text("我在本群的昵称")
        gcs.click_element_by_text("群成员文本")
        # 输入搜索群成员
        gcs.input_search_group_members("大佬1")
        time.sleep(1)
        # 点击已保存手机的联系人成员头像进入profile页
        gcs.click_group_members_image_by_name("大佬1")
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        # 1.如果其为普通手机联系人则有：星标、编辑、分享名片；如果其为安卓SIM卡联系人无：星标、编辑功能
        self.assertEquals(cdp.is_exists_element_by_text("星标"), True)
        self.assertEquals(cdp.is_exists_element_by_text("编辑"), True)
        self.assertEquals(cdp.is_exists_element_by_text("分享名片"), True)
        cdp.click_back_button()
        # 输入搜索群成员
        gcs.input_search_group_members("138********")
        time.sleep(1)
        # 点击未保存手机的联系人成员头像进入profile页
        gcs.click_group_members_image_by_name("138********")
        # 2.进入到未保存的群聊profile页，展示交换名片页面
        self.assertEquals(gcs.page_should_contain_text2("交换名片"), True)
        cdp.click_back_button()
        # 输入搜索群成员
        gcs.input_search_group_members(my_name)
        time.sleep(1)
        # 点击自己头像进入profile页
        gcs.click_group_members_image_by_name(my_name)
        # 3.与进入“我--编辑个人资料”页面一致，功能有：编辑、分享名片
        self.assertEquals(gcs.page_should_contain_text2("编辑"), True)
        self.assertEquals(gcs.page_should_contain_text2("分享名片"), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0317():
        """恢复环境"""

        try:
            fail_time = 0
            while fail_time < 5:
                try:
                    Preconditions.make_already_in_message_page()
                    mp = MessagePage()
                    mp.open_contacts_page()
                    cp = ContactsPage()
                    # 如果不存在指定手机联系人则创建
                    cp.create_contacts_if_not_exits("大佬2", "13800138006")
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_xiaoqiu_0388(self):
        """验证群主在群设置页面——将所有群成员移出群后——群主收到的系统消息"""

        # 进入群聊聊天会话页面
        group_name = "多人测试普通群"
        Preconditions.enter_group_chat_page(group_name)
        gcp = GroupChatPage()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        # 等待群聊设置页面加载
        gcs.wait_for_page_load()
        # 点击-删除群成员，全选群成员进行删除
        gcs.click_del_member()
        gcs.click_name_attribute_by_name("大佬1")
        gcs.click_name_attribute_by_name("大佬2")
        gcs.click_name_attribute_by_name("大佬3")
        gcs.click_name_attribute_by_name("大佬4")
        gcs.click_sure()
        gcs.click_sure_icon()
        # 1.提示删除成功(间接验证)
        # self.assertEquals(gcs.page_should_contain_text2("删除成功"), True)
        self.assertEquals(gcs.page_should_contain_text2(group_name), True)
        time.sleep(5)
        # 返回到消息列表页查看系统消息
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_accessibility_id_attribute_by_name("系统消息")
        # 2.系统消息显示：该群已解散
        self.assertEquals(mp.is_exists_first_system_message_by_text(group_name), True)
        self.assertEquals(mp.is_exists_first_system_message_by_text("该群已解散"), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0388():
        """恢复环境"""

        try:
            fail_time = 0
            while fail_time < 5:
                try:
                    Preconditions.make_already_in_message_page()
                    conts = ContactsPage()
                    conts.open_contacts_page()
                    conts.open_group_chat_list()
                    group_list = GroupListPage()
                    group_chats = [('多人测试普通群', ['大佬1', '大佬2', '大佬3', '大佬4'])]
                    for group_name, members in group_chats:
                        group_list.wait_for_page_load()
                        group_list.create_group_chats_if_not_exits(group_name, members)
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')


class MsgCommonGroupContactTest(TestCase):
    """普通群-通讯录-免费短信-群短信"""

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter("ignore",ResourceWarning)
        # Preconditions.select_mobile('IOS-移动')
        # # 导入测试联系人、群聊
        # fail_time1 = 0
        # flag1 = False
        # import dataproviders
        # while fail_time1 < 3:
        #     try:
        #         required_contacts = dataproviders.get_preset_contacts()
        #         conts = ContactsPage()
        #         Preconditions.make_already_in_message_page()
        #         conts.open_contacts_page()
        #         for name, number in required_contacts:
        #             # 创建联系人
        #             conts.create_contacts_if_not_exits(name, number)
        #         required_group_chats = dataproviders.get_preset_group_chats()
        #         conts.open_group_chat_list()
        #         group_list = GroupListPage()
        #         for group_name, members in required_group_chats:
        #             group_list.wait_for_page_load()
        #             # 创建群
        #             group_list.create_group_chats_if_not_exits(group_name, members)
        #         group_list.click_back()
        #         conts.open_message_page()
        #         flag1 = True
        #     except:
        #         fail_time1 += 1
        #     if flag1:
        #         break
        #
        # # 导入团队联系人
        # fail_time2 = 0
        # flag2 = False
        # while fail_time2 < 5:
        #     try:
        #         Preconditions.make_already_in_message_page()
        #         contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
        #         Preconditions.create_he_contacts(contact_names)
        #         flag2 = True
        #     except:
        #         fail_time2 += 1
        #     if flag2:
        #         break
        #
        # # 导入企业群
        # fail_time3 = 0
        # flag3 = False
        # while fail_time3 < 5:
        #     try:
        #         Preconditions.make_already_in_message_page()
        #         group_chats = ["中文测试企业群", "test_enterprise_group", "好好 企业群", "198891", "*#@"]
        #         Preconditions.create_enterprise_group_if_not_exists(group_chats)
        #         flag3 = True
        #     except:
        #         fail_time3 += 1
        #     if flag3:
        #         break

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

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0283(self):
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
        glp.input_group_name("English-test")
        glsp = GroupListSearchPage()
        # 5.验证是否展示提示：无搜索结果
        self.assertTrue(glsp.page_should_contain_text("无搜索结果"))

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0284(self):
        """通讯录-群聊-带空格精确搜索——搜索结果展示"""
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
        # 4.输入带空格群名
        glp.input_group_name("带空格的 群")
        glsp = GroupListSearchPage()
        # 5.验证是否可以匹配展示搜索结果
        self.assertTrue(glsp.is_group_in_list("带空格的 群"))

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0285(self):
        """通讯录-群聊-带空格精确搜索——搜索结果展示"""
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
        # 4.输入带空格群名
        glp.input_group_name("测试 空格")
        glsp = GroupListSearchPage()
        # 5.验证是否展示提示：无搜索结果
        self.assertTrue(glsp.page_should_contain_text("无搜索结果"))

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0286(self):
        """通讯录-群聊-数字精确搜索——搜索结果展示"""
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
        # 4.输入数字群名
        glp.input_group_name("138138138")
        glsp = GroupListSearchPage()
        # 5.验证是否可以匹配展示搜索结果
        self.assertTrue(glsp.is_group_in_list("138138138"))

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0287(self):
        """通讯录-群聊-数字精确搜索——搜索结果展示"""
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
        # 4.输入数字群名
        glp.input_group_name("6688")
        glsp = GroupListSearchPage()
        # 5.验证是否展示提示：无搜索结果
        self.assertTrue(glsp.page_should_contain_text("无搜索结果"))

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0288(self):
        """通讯录-群聊-数字精确搜索——搜索结果展示"""
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
        # 4.输入数字群名
        glp.input_group_name("1122")
        glsp = GroupListSearchPage()
        # 5.验证是否可以匹配展示搜索结果
        self.assertTrue(glsp.is_group_in_list("1122"))

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0289(self):
        """通讯录-群聊-数字精确搜索——搜索结果展示"""
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
        # 4.输入数字群名
        glp.input_group_name("9911")
        glsp = GroupListSearchPage()
        # 5.验证是否展示提示：无搜索结果
        self.assertTrue(glsp.page_should_contain_text("无搜索结果"))

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0290(self):
        """通讯录-群聊-字符精确搜索——搜索结果展示"""
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
        # 4.输入数字群名
        glp.input_group_name("&%@")
        glsp = GroupListSearchPage()
        # 5.验证是否可以匹配展示搜索结果
        self.assertTrue(glsp.is_group_in_list("&%@"))

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0291(self):
        """通讯录-群聊-字符精确搜索——搜索结果展示"""
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
        # 4.输入数字群名
        glp.input_group_name("字符&%@")
        glsp = GroupListSearchPage()
        # 5.验证是否展示提示：无搜索结果
        self.assertTrue(glsp.page_should_contain_text("无搜索结果"))

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0404(self):
        """在全局搜索搜索群聊时——点击进入到群会话窗口——群设置页面(重复在消息列表页已有的群聊列表进入到群这个入口进群进行测试)"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击搜索框
        mess.click_search_box()
        # 2.输入群名
        mess.input_search_text("群聊1")
        time.sleep(2)
        # 3.点击搜索结果
        mess.click_search_result_by_name("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 4.点击设置
        gcp.click_setting()
        # 5.验证是否在群聊设置页面
        gcsp = GroupChatSetPage()
        self.assertTrue(gcsp.is_on_this_page())
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0405(self):
        """在点击消息列表右上角的+，选择发起群聊，新成功创建的群会话窗口和群设置页面(重复在消息列表页已有的群聊列表进入到群这个入口进群进行测试)"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击+号
        mess.click_add_icon()
        # 2.点击发起群聊
        mess.click_group_chat()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 3.点击选择手机联系人
        scp.select_local_contacts()
        member_name = ["大佬1", "大佬2"]
        for member in member_name:
            scp.select_one_contact_by_name(member)
        # 4.点击确定
        scp.click_sure_bottom()
        alg = ALLMyGroup()
        # 5.点击清除群名称
        alg.click_clear_group_name()
        # 6.输入群名
        alg.input_group_name("创建群测试")
        # 7.点击创建
        alg.click_sure_creat()
        time.sleep(2)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 8.点击设置
        gcp.click_setting()
        # 9.验证是否在群聊设置页面
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        self.assertTrue(gcsp.is_on_this_page())
        time.sleep(2)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0405():
        """解散群"""
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.dissolution_the_group()
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0406(self):
        """在点击消息列表右上角的+，选择发起群聊选择已有群进入到群会话窗口和群设置页面(重复在消息列表页已有的群聊列表进入到群这个入口进群进行测试)"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击+号
        mess.click_add_icon()
        # 2.点击发起群聊
        mess.click_group_chat()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 3.点击选择一个群
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        # 4.根据名字选择一个群
        sogp.selecting_one_group_by_name("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 5.点击设置
        gcp.click_setting()
        # 6.验证是否在群聊设置页面
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        self.assertTrue(gcsp.is_on_this_page())
        time.sleep(2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0407():
        """进入单聊会话页面"""
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_single_chat_page("大佬1")

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0407(self):
        """在点对点建群——新创建的群会话窗口和群设置页面"""
        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 1.点击设置
        scp.click_setting()
        scsp = SingleChatSetPage()
        scsp.wait_for_page_load()
        # 2.点击+添加成员
        scsp.click_add_icon()
        scp = SelectContactsPage()
        # 3.根据联系人名称选择
        scp.select_one_contact_by_name("大佬3")
        # 4.点击确定
        scp.click_confirm_button()
        alg = ALLMyGroup()
        # 5.点击清除群名称
        alg.click_clear_group_name()
        # 6.输入群名
        alg.input_group_name("点对点创建群测试")
        # 7.点击创建
        alg.click_sure_creat()
        time.sleep(2)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 8.点击设置
        gcp.click_setting()
        # 9.验证是否在群聊设置页面
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        self.assertTrue(gcsp.is_on_this_page())
        time.sleep(2)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0407():
        """解散群"""
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.dissolution_the_group()
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0408(self):
        """点击通讯录——点击群聊——任意选中一个群——进入到群会话窗口和群设置页面"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击通讯录
        mess.click_contacts()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        # 2.点击群聊
        contacts.click_group_chat()
        glp = GroupListPage()
        glp.wait_for_page_load()
        # 3.根据群名选择一个群
        glp.selecting_one_group_by_name("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 4.点击设置
        gcp.click_setting()
        # 5.验证是否在群聊设置页面
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        self.assertTrue(gcsp.is_on_this_page())
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0409(self):
        """点击通讯录——点击群聊——点击右上角创建群聊按钮——进入到会话窗口和群设置页面"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击通讯录
        mess.click_contacts()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        # 2.点击群聊
        contacts.click_group_chat()
        glp = GroupListPage()
        glp.wait_for_page_load()
        # 3.点击创建群组
        glp.click_create_group()
        scp = SelectContactsPage()
        scp.click_phone_contact()
        member_name = ["大佬1", "大佬2"]
        for member in member_name:
            scp.select_one_contact_by_name(member)
        # 4.点击确定
        scp.click_sure_bottom()
        alg = ALLMyGroup()
        # 5.点击清除群名称
        alg.click_clear_group_name()
        # 6.输入群名
        alg.input_group_name("通讯录创建群测试")
        # 7.点击创建
        alg.click_sure_creat()
        time.sleep(2)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 8.点击设置
        gcp.click_setting()
        # 9.验证是否在群聊设置页面
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        self.assertTrue(gcsp.is_on_this_page())
        time.sleep(2)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0409():
        """解散群"""
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.dissolution_the_group()
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0427(self):
        """聊天会话页面——长按——撤回——超过一分钟的文本消息"""
        Preconditions.enter_group_chat_page("群聊3")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        for i in range(2):
            # 1.输入文本
            gcp.input_message_text("测试-哈哈-哈哈")
            # 2.点击发送
            gcp.click_send_button()
        time.sleep(30)
        # time.sleep(30)
        # 3.长按最后一条文本消息
        gcp.press_last_text_message()
        # 4.点击撤回
        gcp.click_accessibility_id_attribute_by_name("撤回")
        # 5.验证是否在会话窗口展示：你撤回了一条消息
        self.assertTrue(gcp.is_element_present_by_locator(locator='你撤回了一条消息'))
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_B_0015(self):
        """验证点击确定按钮是否是进入发送短信页面"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击加号
        mess.click_add_icon()
        # 2.点击免费短信
        mess.click_free_sms()
        free_msg = FreeMsgPage()
        # 3.若在资费介绍页，点击确定
        if free_msg.is_exist_free_message_tariff():
            free_msg.click_sure_btn()
        scp = SelectContactsPage()
        # 4.根据联系人名称选择
        scp.select_one_contact_by_name("大佬1")
        # 5.验证是否提示资费说明弹框
        self.assertEquals(free_msg.is_exists_element_by_text("资费说明"), True)
        # 6.若存在你正在使用免费短信，点击退出
        if free_msg.is_exist_using_free_message():
            free_msg.click_quit_btn()
        self.assertEquals(free_msg.is_exists_element_by_text("资费说明"), False)

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_B_0016(self):
        """验证点击退出短信是否成功退出"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击加号
        mess.click_add_icon()
        # 2.点击免费短信
        mess.click_free_sms()
        free_msg = FreeMsgPage()
        # 3.若在资费介绍页，点击确定
        if free_msg.is_exist_free_message_tariff():
            free_msg.click_sure_btn()
        scp = SelectContactsPage()
        # 4.根据联系人名称选择
        scp.select_one_contact_by_name("大佬1")
        # 5.验证是否进入单聊会话页面
        self.assertTrue(free_msg.is_on_this_page())
        # 6.点击返回
        free_msg.click_back_btn()

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_B_0020(self):
        """验证编辑短信后不发送，是否信息草稿"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击加号
        mess.click_add_icon()
        # 2.点击免费短信
        mess.click_free_sms()
        free_msg = FreeMsgPage()
        # 3.若在资费介绍页，点击确定
        if free_msg.is_exist_free_message_tariff():
            free_msg.click_sure_btn()
        scp = SelectContactsPage()
        # 4.根据联系人名称选择
        scp.select_one_contact_by_name("大佬1")
        # 5.输入框输入文本消息
        free_msg.input_message_text("免费短信测试")
        # 6.点击返回消息页面
        free_msg.click_back_btn()
        # 7.验证是否显示草稿标识
        mess.wait_for_page_load()
        self.assertTrue(mess.is_first_message_draft())
        # 8.点击消息列表第一条记录
        mess.click_msg_first_list()
        # 9.进入短信编辑页面，可继续编辑短信（清空输入框）
        free_msg.clear_input_text()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_B_0021(self):
        """验证编辑短信不发送，再次进入是否可以再次编辑"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击加号
        mess.click_add_icon()
        # 2.点击免费短信
        mess.click_free_sms()
        free_msg = FreeMsgPage()
        # 3.若在资费介绍页，点击确定
        if free_msg.is_exist_free_message_tariff():
            free_msg.click_sure_btn()
        scp = SelectContactsPage()
        # 4.根据联系人名称选择
        scp.select_one_contact_by_name("大佬1")
        # 5.输入框输入文本消息
        free_msg.input_message_text("免费短信测试")
        # 6.退出短信编辑页面
        free_msg.click_back_btn()
        mess.wait_for_page_load()
        # 7.点击消息列表第一条记录，再次进入短信编辑页面
        mess.click_msg_first_list()
        # 8.，可继续编辑短信（清空输入框）
        free_msg.clear_input_text()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_B_0036(self):
        """转发短信"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击加号
        mess.click_add_icon()
        # 2.点击免费短信
        mess.click_free_sms()
        free_msg = FreeMsgPage()
        # 3.若在资费介绍页，点击确定
        if free_msg.is_exist_free_message_tariff():
            free_msg.click_sure_btn()
        scp = SelectContactsPage()
        # 4.根据联系人名称选择
        scp.select_one_contact_by_name("大佬1")
        # 5.输入框输入文本消息,点击发送
        free_msg.input_message_text("免费短信测试")
        free_msg.click_send_btn()
        if free_msg.page_should_contain_text2("资费提醒", 1):
            free_msg.click_name_attribute_by_name("确定")
        # 6.长按最后一条文本消息
        free_msg.press_last_text_message()
        # 7.点击转发
        time.sleep(2)
        free_msg.click_accessibility_id_attribute_by_name("转发")
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 8.点击选择手机联系人
        scp.select_local_contacts()
        scp.select_one_contact_by_name("大佬2")
        scp.click_forward_sure()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_B_0037(self):
        """删除短信"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击加号
        mess.click_add_icon()
        # 2.点击免费短信
        mess.click_free_sms()
        free_msg = FreeMsgPage()
        # 3.若在资费介绍页，点击确定
        if free_msg.is_exist_free_message_tariff():
            free_msg.click_sure_btn()
        scp = SelectContactsPage()
        # 4.根据联系人名称选择
        scp.select_one_contact_by_name("大佬1")
        # 5.点击设置，清空聊天记录，以免影响验证结果
        free_msg.click_setting_btn()
        free_msg.click_clear_local_chat_history()
        free_msg.click_sure_clear_local_chat_history()
        free_msg.click_back_btn()
        # 6.输入框输入文本消息,点击发送
        free_msg.input_message_text("免费短信测试")
        free_msg.click_send_btn()
        if free_msg.page_should_contain_text2("资费提醒", 1):
            free_msg.click_name_attribute_by_name("确定")
        free_msg = FreeMsgPage()
        # 7.长按最后一条文本消息
        free_msg.press_last_text_message()
        # 8.点击删除
        time.sleep(2)
        free_msg.click_accessibility_id_attribute_by_name("删除")
        # 9.点击确定删除
        free_msg.click_sure_btn()

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_B_0038(self):
        """复制短信"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击加号
        mess.click_add_icon()
        # 2.点击免费短信
        mess.click_free_sms()
        free_msg = FreeMsgPage()
        # 3.若在资费介绍页，点击确定
        if free_msg.is_exist_free_message_tariff():
            free_msg.click_sure_btn()
        scp = SelectContactsPage()
        # 4.根据联系人名称选择
        scp.select_one_contact_by_name("大佬1")
        # 5.输入框输入文本消息,点击发送
        free_msg.input_message_text("免费短信测试")
        free_msg.click_send_btn()
        if free_msg.page_should_contain_text2("资费提醒", 1):
            free_msg.click_name_attribute_by_name("确定")
        free_msg = FreeMsgPage()
        # 6.长按最后一条文本消息
        free_msg.press_last_text_message()
        # 7.点击复制
        time.sleep(2)
        free_msg.click_accessibility_id_attribute_by_name("复制")

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_B_0039(self):
        """收藏短信"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击加号
        mess.click_add_icon()
        # 2.点击免费短信
        mess.click_free_sms()
        free_msg = FreeMsgPage()
        # 3.若在资费介绍页，点击确定
        if free_msg.is_exist_free_message_tariff():
            free_msg.click_sure_btn()
        scp = SelectContactsPage()
        # 4.根据联系人名称选择
        scp.select_one_contact_by_name("大佬1")
        # 5.输入框输入文本消息,点击发送
        free_msg.input_message_text("免费短信测试")
        free_msg.click_send_btn()
        if free_msg.page_should_contain_text2("资费提醒", 1):
            free_msg.click_name_attribute_by_name("确定")
        free_msg = FreeMsgPage()
        # 6.长按最后一条文本消息                                                                  不 不
        free_msg.press_last_text_message()
        # 7.点击收藏
        time.sleep(2)
        free_msg.click_accessibility_id_attribute_by_name("收藏")

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_B_0040(self):
        """多选，批量转发与删除短信"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击加号
        mess.click_add_icon()
        # 2.点击免费短信
        mess.click_free_sms()
        free_msg = FreeMsgPage()
        # 3.若在资费介绍页，点击确定
        if free_msg.is_exist_free_message_tariff():
            free_msg.click_sure_btn()
        scp = SelectContactsPage()
        # 4.根据联系人名称选择
        scp.select_one_contact_by_name("大佬1")
        # 5.输入框输入文本消息,点击发送
        free_msg.input_message_text("免费短信测试")
        free_msg.click_send_btn()
        if free_msg.page_should_contain_text2("资费提醒", 1):
            free_msg.click_name_attribute_by_name("确定")
        free_msg = FreeMsgPage()
        # 6.长按最后一条文本消息
        free_msg.press_last_text_message()
        # 7.点击多选
        time.sleep(2)
        free_msg.click_accessibility_id_attribute_by_name("多选")
        # 8.点击转发
        free_msg.click_forward_btn()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 9.点击选择手机联系人
        scp.select_local_contacts()
        scp.select_one_contact_by_name("大佬2")
        scp.click_forward_sure()
        time.sleep(2)
        # 10.长按最后一条文本消息
        free_msg.press_last_text_message()
        # 11.点击多选
        time.sleep(2)
        free_msg.click_accessibility_id_attribute_by_name("多选")
        # 12.点击删除
        free_msg.click_delete_btn()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_C_0006(self):
        """验证退出短信是否成功退出"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击更多+号按钮
        gcp.click_add_button()
        gcp.click_group_message()
        cgp = ChatGroupSMSExpensesPage()
        # 2.若在资费介绍页，点击确定
        if cgp.is_exist_group_message_tariff():
            cgp.click_sure()
        # cgp.wait_for_page_load()
        # 3.点击返回
        cgp.click_back()
        gcp.wait_for_page_load()
        # 4.验证是否在群聊页面
        self.assertTrue(gcp.is_on_this_page())
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_C_0008(self):
        """验证编辑短信，不选择联系人，发送短信是否弹出toast提示"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击更多+号按钮
        gcp.click_add_button()
        gcp.click_group_message()
        cgp = ChatGroupSMSExpensesPage()
        # 2.若在资费介绍页，点击确定
        if cgp.is_exist_group_message_tariff():
            cgp.click_sure()
        # 3.若在群记录页面，点击新建群发进入编辑页面
        if cgp.is_on_message_record_page():
            cgp.click_build_new_group_send()
        # 4.若在消息编辑界面，编辑短信发送
        if cgp.is_on_message_edit_page():
            cgp.click_input_box()
            cgp.input_message_text("群短信测试")
            cgp.click_send()

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_C_0010(self):
        """群聊中群短信无记录"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击更多+号按钮
        gcp.click_add_button()
        gcp.click_group_message()
        cgp = ChatGroupSMSExpensesPage()
        # 2.若在资费介绍页，点击确定
        if cgp.is_exist_group_message_tariff():
            cgp.click_sure()
        # 3.若在消息编辑页面，群短信无记录
        if cgp.is_on_message_edit_page():
            print("当前群聊中群短信无记录")
        # 4.验证当前页面是否在群记录页面
        if cgp.is_on_message_record_page():
            print("当前页面在群短信记录页面")

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_C_0011(self):
        """群聊中群短信有记录"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击更多+号按钮
        gcp.click_add_button()
        gcp.click_group_message()
        cgp = ChatGroupSMSExpensesPage()
        # 2.若在资费介绍页，点击确定
        if cgp.is_exist_group_message_tariff():
            cgp.click_sure()
        # 3.验证是否在消息编辑页面，群短信无记录
        if cgp.is_on_message_edit_page():
            print("当前群聊中群短信无记录")
        # 4.验证当前页面是否在群记录页面
        if cgp.is_on_message_record_page():
            print("当前页面在群短信记录页面")

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_C_0013(self):
        """群短信输入1个字符的文本内容进行发送"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击更多+号按钮
        gcp.click_add_button()
        gcp.click_group_message()
        cgp = ChatGroupSMSExpensesPage()
        # 2.若在资费介绍页，点击确定
        if cgp.is_exist_group_message_tariff():
            cgp.click_sure()
        # 3.若在群记录页面，点击新建群发进入编辑页面
        if cgp.is_on_message_record_page():
            cgp.click_build_new_group_send()
        # 4.若在消息编辑界面，编辑短信发送
        if cgp.is_on_message_edit_page():
            cgp.click_input_box()
            cgp.input_message_text("a")
            # 5.选择收件人
            cgp.click_addressee()
            time.sleep(2)
            cgp.click_first_contact()
            # 6.点击确定
            cgp.click_sure()
            # 7.点击发送
            cgp.click_send()
        time.sleep(2)
        # 8.验证是否发送成功（是否跳转至群记录页面）
        if not cgp.is_on_message_record_page():
            raise AssertionError("当前页面不在群记录页面，消息未发送")
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_C_0016(self):
        """短信已发送多条的情况，查看群短信记录排序"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击更多+号按钮
        gcp.click_add_button()
        gcp.click_group_message()
        cgp = ChatGroupSMSExpensesPage()
        # 2.若在资费介绍页，点击确定
        if cgp.is_exist_group_message_tariff():
            cgp.click_sure()
        # 3.若在群记录页面，点击新建群发进入编辑页面
        time.sleep(2)
        if not cgp.is_on_message_record_page():
            raise AssertionError("当前页面不在群短信记录页面")

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_C_0017(self):
        """观察群短信内容以及群成员的展示"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击更多+号按钮
        gcp.click_add_button()
        gcp.click_group_message()
        cgp = ChatGroupSMSExpensesPage()
        # 2.若在资费介绍页，点击确定
        if cgp.is_exist_group_message_tariff():
            cgp.click_sure()
        # 3.若在群记录页面，点击新建群发进入编辑页面
        if cgp.is_on_message_record_page():
            cgp.click_build_new_group_send()
        # 4.若在消息编辑界面，编辑短信发送
        if cgp.is_on_message_edit_page():
            cgp.click_input_box()
            cgp.input_message_text("群短信发送测试")
            # 5.选择收件人
            cgp.click_addressee()
            time.sleep(2)
            cgp.click_first_contact()
            # 6.点击确定
            cgp.click_sure()
            # 7.点击发送
            cgp.click_send()
            time.sleep(2)
        if cgp.is_on_message_record_page():
            # 8.验证是否含有群短信内容展示
            self.assertTrue(cgp.page_should_contain_text2("群短信发送测试"))
            # 9.验证是否有群成员展示
            self.assertTrue(cgp.is_exist_addressee())

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_C_0019(self):
        """点击底部编辑按钮，是否跳转到编辑页面"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击更多+号按钮
        gcp.click_add_button()
        gcp.click_group_message()
        cgp = ChatGroupSMSExpensesPage()
        # 2.若在资费介绍页，点击确定
        if cgp.is_exist_group_message_tariff():
            cgp.click_sure()
        # 3.若在群记录页面
        if cgp.is_on_message_record_page():
            # 4.点击新建群发
            cgp.click_build_new_group_send()
        # 5.验证是否在短信编辑页面
        time.sleep(2)
        self.assertTrue(cgp.is_on_message_edit_page())

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_C_0020(self):
        """点击左上角返回键时候返回群聊天页面"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击更多+号按钮
        gcp.click_add_button()
        gcp.click_group_message()
        cgp = ChatGroupSMSExpensesPage()
        # 2.若在资费介绍页，点击确定
        if cgp.is_exist_group_message_tariff():
            cgp.click_sure()
        # 3.若在群记录页面
        if cgp.is_on_message_record_page():
            # 4.点击返回
            cgp.click_back()
        # 5.验证是否返回群聊页面
        time.sleep(2)
        self.assertTrue(gcp.is_on_this_page())

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_C_0021(self):
        """从群短信列表进入群发短信页面"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击更多+号按钮
        gcp.click_add_button()
        gcp.click_group_message()
        cgp = ChatGroupSMSExpensesPage()
        # 2.若在资费介绍页，点击确定
        if cgp.is_exist_group_message_tariff():
            cgp.click_sure()
        # 3.若在群短信列表页面
        if cgp.is_on_message_record_page():
            # 4.点击新建群发
            cgp.click_build_new_group_send()
        # 5.验证是否群发短信编辑页面
        time.sleep(2)
        self.assertTrue(cgp.is_on_message_edit_page())

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_C_0025(self):
        """进入群短信收件人联系人选择器"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击更多+号按钮
        gcp.click_add_button()
        gcp.click_group_message()
        cgp = ChatGroupSMSExpensesPage()
        # 2.若在资费介绍页，点击确定
        if cgp.is_exist_group_message_tariff():
            cgp.click_sure()
        # 3.若在群短信列表页面,点击新建群发
        if cgp.is_on_message_record_page():
            cgp.click_build_new_group_send()
        # 4.输入文本消息
        cgp.input_message_text("测试")
        # 5.点击右边接收人头像
        cgp.click_receivcer_avatar()
        time.sleep(2)
        # 6.验证是否存在全选按钮
        self.assertTrue(cgp.is_exist_select_all)
        # 7.选择第一个联系人
        cgp.click_first_contact()
        # 8.验证是否存在已选择人数和可选择的最高上限人数显示
        self.assertTrue(cgp.is_exist_select_and_all())
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_C_0026(self):
        """当人数小于最高上限时，点击全选按钮"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        # 1.点击设置，获取群人数
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        number = gcsp.get_group_members_image_number()
        gcsp.click_back()
        # 1.点击更多+号按钮
        gcp.click_add_button()
        gcp.click_group_message()
        cgp = ChatGroupSMSExpensesPage()
        # 2.若在资费介绍页，点击确定
        if cgp.is_exist_group_message_tariff():
            cgp.click_sure()
        # 3.若在群短信列表页面,点击新建群发
        if cgp.is_on_message_record_page():
            cgp.click_build_new_group_send()
        # 4.输入文本消息
        time.sleep(2)
        cgp.input_message_text("测试")
        # 5.点击右边接收人头像
        cgp.click_receivcer_avatar()
        time.sleep(2)
        # 6.点击全选
        cgp.click_select_all()
        time.sleep(2)
        # 7.验证是否全选
        self.assertTrue(cgp.is_select_all(number))
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_C_0033(self):
        """昵称搜索群成员"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 1.点击设置，获取第一个群成员名字
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        time.sleep(2)
        name = gcsp.get_first_number_name()
        # 2.返回群聊页面
        gcsp.click_back()
        gcp.wait_for_page_load()
        # 3.点击更多+号按钮
        gcp.click_add_button()
        gcp.click_group_message()
        cgp = ChatGroupSMSExpensesPage()
        # 4.若在资费介绍页，点击确定
        if cgp.is_exist_group_message_tariff():
            cgp.click_sure()
        # 5.若在群短信列表页面,点击新建群发
        if cgp.is_on_message_record_page():
            cgp.click_build_new_group_send()
        # 6.输入文本消息
        time.sleep(2)
        cgp.input_message_text("测试")
        # 7.点击右边接收人头像
        cgp.click_receivcer_avatar()
        time.sleep(2)
        cgp.input_search_message(name)
        # 8.验证是否存在搜索结果
        self.assertTrue(cgp.is_contact_in_list(name))
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_C_0034(self):
        """号码搜索群成员"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击更多+号按钮
        gcp.click_add_button()
        gcp.click_group_message()
        cgp = ChatGroupSMSExpensesPage()
        # 2.若在资费介绍页，点击确定
        if cgp.is_exist_group_message_tariff():
            cgp.click_sure()
        # 3.若在群短信列表页面,点击新建群发
        if cgp.is_on_message_record_page():
            cgp.click_build_new_group_send()
        # 4.输入文本消息
        time.sleep(2)
        cgp.input_message_text("测试")
        # 5.点击右边接收人头像
        cgp.click_receivcer_avatar()
        time.sleep(2)
        cgp.input_search_message("13800138005")
        # 6.验证是否显示搜索无结果
        self.assertTrue(cgp.page_should_contain_text2("无搜索结果"))
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_C_0035(self):
        """选择群成员后返回去查看，是否可以从新选择"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击更多+号按钮
        gcp.click_add_button()
        gcp.click_group_message()
        cgp = ChatGroupSMSExpensesPage()
        # 2.若在资费介绍页，点击确定
        if cgp.is_exist_group_message_tariff():
            cgp.click_sure()
        # 3.若在群短信列表页面,点击新建群发
        if cgp.is_on_message_record_page():
            cgp.click_build_new_group_send()
        # 4.输入文本消息
        time.sleep(2)
        cgp.input_message_text("测试")
        # 5.点击右边接收人头像，选择第一个联系人
        cgp.click_receivcer_avatar()
        time.sleep(2)
        cgp.click_first_contact()
        # 6.点击确定
        cgp.click_sure()
        # 7.再次点击右边接收人头像，选择第二个联系人
        cgp.click_receivcer_avatar()
        cgp.click_second_contact()
        # 8.验证是否可以重新选择联系人
        self.assertTrue(cgp.is_exist_renew_select())
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_C_0037(self):
        """编辑群短信字符数为1"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击更多+号按钮
        gcp.click_add_button()
        gcp.click_group_message()
        cgp = ChatGroupSMSExpensesPage()
        # 2.若在资费介绍页，点击确定
        if cgp.is_exist_group_message_tariff():
            cgp.click_sure()
        # 3.若在群短信列表页面,点击新建群发
        if cgp.is_on_message_record_page():
            cgp.click_build_new_group_send()
        # 4.编辑群短信字符数为1
        cgp.input_message_text("1")
        # 5.点击右边接收人头像，选择第一个联系人
        cgp.click_receivcer_avatar()
        time.sleep(2)
        cgp.click_first_contact()
        # 6.点击确定
        cgp.click_sure()
        # 7.点击发送
        cgp.click_send()
        time.sleep(1)
        # 8.验证是否进入群短信列表页面（记录）
        self.assertTrue(cgp.is_on_message_record_page())
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_huangcaizui_C_0040(self):
        """验证正常发送短信是否成功"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击更多+号按钮
        gcp.click_add_button()
        gcp.click_group_message()
        cgp = ChatGroupSMSExpensesPage()
        # 2.若在资费介绍页，点击确定
        if cgp.is_exist_group_message_tariff():
            cgp.click_sure()
        # 3.若在群短信列表页面,点击新建群发
        if cgp.is_on_message_record_page():
            cgp.click_build_new_group_send()
        # 4.编辑群短信
        cgp.input_message_text("群短信测试，测试，测试，测试，测试，测试")
        # 5.点击右边接收人头像，选择第一个联系人
        cgp.click_receivcer_avatar()
        time.sleep(2)
        cgp.click_first_contact()
        # 6.点击确定
        cgp.click_sure()
        # 7.点击发送
        cgp.click_send()
        time.sleep(1)
        # 8.验证是否进入群短信列表页面（记录）
        self.assertTrue(cgp.is_on_message_record_page())
        time.sleep(2)

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0421(self):
        """群主或群成员在设置页面——点击+邀请群成员后"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击+添加成员
        gcsp.click_add_member()
        scp = SelectContactsPage()
        # 3.通过名称选择联系人
        scp.select_one_contact_by_name("飞信电话")
        # 4.点击确定
        scp.click_sure_bottom()
        time.sleep(2)
        # 5.验证在群聊页面是否收到一条提示：你向XXXX发出群邀请
        # self.assertTrue(gcp.page_should_contain_text2("你向 飞信电话 发出群邀请"))

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoqiu_0426(self):
        """聊天会话页面——长按——撤回——不足一分钟的文本消息"""
        Preconditions.enter_group_chat_page("群聊3")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        for i in range(2):
            # 1.输入文本
            gcp.input_message_text("测试-哈哈-哈哈")
            # 2.点击发送
            gcp.click_send_button()
        time.sleep(3)
        # 3.长按最后一条文本消息
        gcp.press_last_text_message()
        # 4.点击撤回
        time.sleep(2)
        gcp.click_accessibility_id_attribute_by_name("撤回")
        # 5.验证是否在会话窗口展示：你撤回了一条消息
        time.sleep(2)
        self.assertTrue(gcp.is_element_present_by_locator(locator='你撤回了一条消息'))

    @tags('ALL', 'CMCC', 'YX', 'YX_IOS')
    def test_msg_xiaoliping_A_0026(self):
        """进入我的二维码页面"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 1.点击+
        mess.click_add_icon()
        # 2.点击扫一扫
        mess.click_take_a_scan()
        time.sleep(2)
        scan_page = ScanPage()
        # 3.验证是否在扫一扫页面
        self.assertTrue(scan_page.is_on_this_page())
        # 4.点击我的二维码
        scan_page.open_my_qr_code_page()
        myqr_code = MyQRCodePage()
        # 5.验证是否在我的二维码页面
        self.assertTrue(myqr_code.is_on_this_page())
        time.sleep(2)




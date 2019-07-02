import time

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import ContactsPage
from pages import GroupListPage
from pages import MessagePage
from pages.workbench.Workbench import WorkbenchPage
from pages.workbench.group_messenger.GroupMessenger import GroupMessengerPage
from pages.workbench.group_messenger.HelpCenter import HelpCenterPage
from pages.workbench.group_messenger.NewMessage import NewMessagePage
from pages.workbench.group_messenger.SelectCompanyContacts import SelectCompanyContactsPage
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage
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
    def add_phone_number_to_department(department_name):
        """添加本机号码到指定部门"""

        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        n = 1
        # 解决工作台不稳定问题
        while not osp.page_should_contain_text2("添加联系人"):
            osp.click_back_button()
            wbp.wait_for_page_load()
            wbp.click_organization()
            n += 1
            if n > 20:
                break
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        if not osp.is_exist_specify_element_by_name(department_name):
            osp.click_specify_element_by_name("添加子部门")
            osp.input_sub_department_name(department_name)
            osp.input_sub_department_sort("1")
            # 收起键盘
            osp.click_name_attribute_by_name("完成")
            time.sleep(1)
            osp.click_confirm()
            osp.wait_for_page_load()
        osp.click_specify_element_by_name(department_name)
        time.sleep(1)
        osp.click_specify_element_by_name("添加联系人")
        osp.click_specify_element_by_name("手动输入添加")
        time.sleep(2)
        osp.input_contacts_name("admin")
        osp.input_contacts_number(phone_number)
        # 收起键盘
        osp.click_name_attribute_by_name("完成")
        time.sleep(1)
        osp.click_confirm()
        time.sleep(2)
        osp.click_close()
        wbp.wait_for_page_load()

    @staticmethod
    def delete_department_by_name(department_name):
        """删除指定部门"""

        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        n = 1
        # 解决工作台不稳定问题
        while not osp.page_should_contain_text2("添加联系人"):
            osp.click_back_button()
            wbp.wait_for_page_load()
            wbp.click_organization()
            n += 1
            if n > 20:
                break
        if osp.is_exist_specify_element_by_name(department_name):
            osp.click_specify_element_by_name(department_name)
            osp.click_specify_element_by_name("更多")
            osp.click_specify_element_by_name("部门设置")
            osp.click_delete()
            osp.click_sure()
            time.sleep(2)
        osp.click_back_button()
        wbp.wait_for_page_load()

    @staticmethod
    def add_phone_number_to_he_contacts():
        """添加本机号码到和通讯录"""

        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        n = 1
        # 解决工作台不稳定问题
        while not osp.page_should_contain_text2("添加联系人"):
            osp.click_back_button()
            wbp.wait_for_page_load()
            wbp.click_organization()
            n += 1
            if n > 20:
                break
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        if not osp.is_exist_specify_element_by_name(phone_number):
            osp.click_specify_element_by_name("添加联系人")
            osp.click_specify_element_by_name("手动输入添加")
            time.sleep(2)
            osp.input_contacts_name("admin")
            osp.input_contacts_number(phone_number)
            # 收起键盘
            osp.click_name_attribute_by_name("完成")
            time.sleep(1)
            osp.click_confirm()
            time.sleep(2)
            osp.click_back_button()
            osp.wait_for_page_load()
        osp.click_back_button()
        wbp.wait_for_page_load()


class MassMessengerAllTest(TestCase):

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
        """
        1、成功登录和飞信
        2、当前页面在群发信使首页
        """

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

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0001(self):
        """可以正常查看帮助中心内容"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 点击右上角【？】
        gmp.click_help_icon()
        hcp = HelpCenterPage()
        # 等待等待群发信使->帮助中心页面加载
        hcp.wait_for_page_load()
        # 看见每个子页面
        hcp.click_introduction()
        # 1.可正常查看子页面内容详情
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

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0005(self):
        """添加搜索出的联系人"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 点击“新建短信”
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬1"
        # 在搜索框输入关键词
        sccp.input_search_message(search_name)
        # 点击勾选搜索出的联系人图像
        sccp.click_contacts_image()
        # 点击“确定”
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 1.可以正常选择搜索出的联系人
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name(search_name), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0006(self):
        """添加成员之后再移除成员"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 点击“新建短信”
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 在联系人选择器页面添加多个联系人
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
        # 点击“确定”
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.可正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0007(self):
        """多个部门累计添加成员"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 点击“新建短信”
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 在联系人选择器页面添加多个联系人
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        # 进入多个部门，勾选成员
        sccp.click_accessibility_id_attribute_by_name("测试部门2")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        # 1.可正常进入多个部门勾选成员
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        # 2.各个部门添加的成员可累计
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        # 点击“确定”
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), True)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0009(self):
        """用户不在任何部门下"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        # 点击“+”添加联系人
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.直接进入企业子一层级
        self.assertEquals(sccp.is_exist_corporate_grade(), True)
        # 点击返回
        sccp.click_back_button()
        # 2.页面跳转到企业层级
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exist_department_name(), True)
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0010(self):
        """用户在企业部门下"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 确保用户在企业部门下
        gmp.click_back_button()
        wbp = WorkbenchPage()
        # 添加本机号码到指定部门
        department_name = "admin_department"
        Preconditions.add_phone_number_to_department(department_name)
        workbench_name = wbp.get_workbench_name()
        wbp.click_group_messenger()
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        # 点击“+”添加联系人
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.跳转后直接进入企业层级：企业+部门名称
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exists_accessibility_id_attribute_by_name(workbench_name), True)
        self.assertEquals(sccp.is_exists_accessibility_id_attribute_by_name(department_name), True)
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @staticmethod
    def tearDown_test_QFXS_0010():
        """恢复环境"""

        try:
            fail_time = 0
            while fail_time < 5:
                try:
                    Preconditions.make_already_in_message_page()
                    mp = MessagePage()
                    mp.open_workbench_page()
                    wbp = WorkbenchPage()
                    Preconditions.delete_department_by_name("admin_department")
                    wbp.click_group_messenger()
                    gmp = GroupMessengerPage()
                    gmp.wait_for_page_load()
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0011(self):
        """用户在企业部门下又在企业子一层级中，直接进入企业层级"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 确保用户既在企业部门下又在企业子一层级
        gmp.click_back_button()
        wbp = WorkbenchPage()
        # 添加本机号码到指定部门
        department_name = "admin_department"
        Preconditions.add_phone_number_to_department(department_name)
        # 添加本机号码到和通讯录
        Preconditions.add_phone_number_to_he_contacts()
        workbench_name = wbp.get_workbench_name()
        wbp.click_group_messenger()
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        # 点击“+”添加联系人
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.跳转后直接进入企业层级：企业+部门名称
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exists_accessibility_id_attribute_by_name(workbench_name), True)
        self.assertEquals(sccp.is_exists_accessibility_id_attribute_by_name(department_name), True)
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @staticmethod
    def tearDown_test_QFXS_0011():
        """恢复环境"""

        try:
            fail_time = 0
            while fail_time < 5:
                try:
                    Preconditions.make_already_in_message_page()
                    mp = MessagePage()
                    mp.open_workbench_page()
                    wbp = WorkbenchPage()
                    Preconditions.delete_department_by_name("admin_department")
                    wbp.click_group_messenger()
                    gmp = GroupMessengerPage()
                    gmp.wait_for_page_load()
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0012(self):
        """用户同时在两个部门下"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 确保用户在企业部门下
        gmp.click_back_button()
        wbp = WorkbenchPage()
        # 添加本机号码到指定部门1
        department_name1 = "admin_department1"
        Preconditions.add_phone_number_to_department(department_name1)
        # 添加本机号码到指定部门2
        department_name2 = "admin_department2"
        Preconditions.add_phone_number_to_department(department_name2)
        workbench_name = wbp.get_workbench_name()
        wbp.click_group_messenger()
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        # 点击“+”添加联系人
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.跳转后显示企业层级：企业+部门名称（部门随机显示一个）
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exists_accessibility_id_attribute_by_name(workbench_name), True)
        self.assertEquals((sccp.is_exists_accessibility_id_attribute_by_name(department_name1) or sccp.is_exists_accessibility_id_attribute_by_name(department_name2)), True)
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @staticmethod
    def tearDown_test_QFXS_0012():
        """恢复环境"""

        try:
            fail_time = 0
            while fail_time < 5:
                try:
                    Preconditions.make_already_in_message_page()
                    mp = MessagePage()
                    mp.open_workbench_page()
                    wbp = WorkbenchPage()
                    Preconditions.delete_department_by_name("admin_department1")
                    Preconditions.delete_department_by_name("admin_department2")
                    wbp.click_group_messenger()
                    gmp = GroupMessengerPage()
                    gmp.wait_for_page_load()
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0016(self):
        """搜索“我的电脑”"""

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
        # 搜索“我的电脑”
        sccp.input_search_message("我的电脑")
        # 1.无搜索结果
        self.assertEquals(sccp.is_exist_text(), True)
        sccp.click_back_button(2)
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0017(self):
        """11位号码精准搜索"""

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
        # 在搜索框输入11位号码，查看匹配结果
        sccp.input_search_message(search_number)
        # 1.匹配出对应的联系人，关键词高亮，按第一个汉字的字顺序排序显示(间接验证)
        self.assertEquals(sccp.is_search_contacts_number_full_match(search_number), True)
        # 点击结果，查看是否可选择成功
        sccp.click_name_attribute_by_name(search_number, "xpath")
        # 2.可成功选中，输入框自动清空
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_clear_search_box(search_number), True)
        sccp.click_back_button(2)
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0018(self):
        """6-10位数字可支持模糊搜索匹配结果"""

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
        search_number = "138005"
        # 在搜索框输入6-10位数字,查看匹配结果
        sccp.input_search_message(search_number)
        # 1.匹配出名称号码中包含6-10的联系人，关键词高亮，按第一个汉字的字顺序排序显示(间接验证)
        self.assertEquals(sccp.is_search_contacts_number_match(search_number), True)
        # 点击结果，查看是否可选择成功
        sccp.click_name_attribute_by_name(search_number, "xpath")
        # 2.可成功选中，输入框自动清空
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_clear_search_box(search_number), True)
        sccp.click_back_button(2)
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0019(self):
        """联系人姓名（全名）精准搜索"""

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
        # 在搜索框输入联系人姓名（全名）,查看匹配结果
        sccp.input_search_message(search_name)
        # 1.匹配对应名称的联系人，关键词高亮，按第一个汉字的字顺序排序显示(间接验证)
        self.assertEquals(sccp.is_search_contacts_name_full_match(search_name), True)
        # 点击结果，查看是否可选择成功
        sccp.click_name_attribute_by_name(search_name, "xpath")
        # 2.搜索栏清空，搜索栏左侧出现已选人名和头像，右上角展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button(2)
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0020(self):
        """联系人姓名（非全名）模糊搜索"""

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
        search_name = "佬1"
        # 在搜索框输入联系人联系人姓名（非全名）,查看匹配结果
        sccp.input_search_message(search_name)
        # 1.匹配包含名字的联系人，关键词高亮，按第一个汉字的字顺序排序显示(间接验证)
        self.assertEquals(sccp.is_search_contacts_name_match(search_name), True)
        # 点击结果，查看是否可选择成功
        sccp.click_name_attribute_by_name(search_name, "xpath")
        # 2.搜索栏清空，搜索栏左侧出现已选人名和头像，右上角展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button(2)
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0025(self):
        """纯空格键不支持搜索匹配"""

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
        search_content = "    "
        # 在搜索框输入空格，查看显示
        sccp.input_search_message(search_content)
        # 1.纯空格键不支持搜索匹配(部分验证点变动)
        # self.assertEquals(sccp.is_exist_corporate_grade(), True)
        self.assertEquals(sccp.is_exist_text(), True)
        sccp.click_back_button(2)
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0026(self):
        """空格键+文本 可支持匹配"""

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
        search_name = " 马上"
        # 在搜索框输入 空格键+文本,查看匹配结果
        sccp.input_search_message(search_name)
        # 1.匹配出对应包含 空格键+文本的联系人，文本关键词高亮，按第一个汉字的字顺序排序显示(间接验证)
        self.assertEquals(sccp.is_search_contacts_name_match(search_name), True)
        # 点击结果，查看是否可选择成功
        sccp.click_name_attribute_by_name(search_name, "xpath")
        # 2.搜索栏清空，搜索栏左侧出现已选人名和头像，右上角展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("马上"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image("马上"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button(2)
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0030(self):
        """字母+汉字组合可精准搜索"""

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
        search_name = "b测算"
        # 在搜索框输入：字母+汉字,查看匹配结果
        sccp.input_search_message(search_name)
        # 1.查看匹配结果
        self.assertEquals(sccp.is_search_contacts_name_full_match(search_name), True)
        # 点击结果，查看是否可选择成功
        sccp.click_name_attribute_by_name(search_name, "xpath")
        # 2.搜索栏清空，搜索栏左侧出现已选人名和头像，右上角展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("测算"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image("测算"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button(2)
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0031(self):
        """字母+汉字+数字 组合可精准搜索"""

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
        search_name = "c平5"
        # 在搜索框输入：字母+汉字+数字,查看匹配结果
        sccp.input_search_message(search_name)
        # 1.查看匹配结果
        self.assertEquals(sccp.is_search_contacts_name_full_match(search_name), True)
        # 点击结果，查看是否可选择成功
        sccp.click_name_attribute_by_name(search_name, "xpath")
        # 2.搜索栏清空，搜索栏左侧出现已选人名和头像，右上角展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("平5"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image("平5"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button(2)
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0032(self):
        """搜索非企业联系人提示无结果"""

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
        # 搜索不存在在企业通讯录中的用户电话号码，大陆号码11位或8位香港号码
        sccp.input_search_message("13900009999")
        # 1.提示“无搜索结果”
        self.assertEquals(sccp.is_exist_text(), True)
        sccp.click_back_button(2)
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0033(self):
        """任意点击搜索结果联系人"""

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
        # 任意点击头像，选择人员
        sccp.click_contacts_image()
        # 1.选择人员那行勾选，搜索栏左侧出现已选人名和头像，右上角展示已选人数/上限人数(间接验证)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button(2)
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0035(self):
        """多选-任意选择多位联系人"""

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
        # 任意选择多位联系人
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        sccp.click_accessibility_id_attribute_by_name("大佬3")
        # 联系人是否为已选中状态
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬3"), True)
        # 是否展示已选人数/上限人数
        self.assertEquals(sccp.is_exist_select_and_all("3"), True)
        # 取消已选联系人
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        # 1.选择人员那行，勾选取消，搜索栏左侧被取消人员人名和头像被移除，展示已选人数/上限人数
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), False)
        self.assertEquals(sccp.is_exist_select_contacts_image("佬1"), False)
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        sccp.click_back_button(2)
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0036(self):
        """添加多部门联系人"""

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
        # 进入A部门勾选C用户后，返回一级页面在进入B部门勾选其它用户
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_accessibility_id_attribute_by_name("测试部门2")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        # 1.部门人数可以叠加，同一号码（不同姓名、不同部门）选择一个则其余都选上
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        sccp.click_back_button(3)
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0039(self):
        """直接添加接收人后再次点击'+'"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        # 点击“+”添加接收人
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 任意选择2位以上联系人后点击确定
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 再次点击”+“添加接收人
        nmp.click_add_icon()
        sccp.wait_for_page_load()
        # 1.跳转联系人选择器后，上次添加的联系人为已选中状态
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        # 任意选择联系人之后，点击确定
        sccp.click_accessibility_id_attribute_by_name("大佬3")
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 2.添加成功，已添加与新添加用户均展示正常
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), True)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), True)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0042(self):
        """点击返回键返回上一级页面"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        # 在任意页面点击顶部【<】
        nmp.click_back_button()
        # 1.返回到上一级页面
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0043(self):
        """点击顶部关闭按钮退出到工作台页面"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 确保有【x】控件可点击
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        # 点击顶部【x】
        nmp.click_close()
        wbp = WorkbenchPage()
        # 1.返回到工作台页面
        wbp.wait_for_page_load()
        wbp.click_group_messenger()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

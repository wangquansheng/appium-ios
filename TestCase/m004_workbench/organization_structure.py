import time

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile
from pages import ContactsPage
from pages import GroupListPage
from pages import MessagePage
from pages import SelectLocalContactsPage
from pages import WorkbenchPage
from pages.workbench.enterprise_contacts.EnterpriseContacts import EnterpriseContactsPage
from pages.workbench.group_messenger.SelectCompanyContacts import SelectCompanyContactsPage
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage
from pages.workbench.voice_notice.VoiceNotify import VoiceNotifyPage
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
    def enter_workbench_page():
        """进入工作台首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @staticmethod
    def enter_organization_structure_page():
        """进入组织架构首页"""

        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_organization()
        # osp = OrganizationStructurePage()
        # n = 1
        # # 解决工作台不稳定问题
        # while not osp.page_should_contain_text2("添加联系人"):
        #     osp.click_back_button()
        #     wbp.wait_for_page_load()
        #     wbp.click_organization()
        #     n += 1
        #     if n > 20:
        #         break

    @staticmethod
    def delete_contacts_if_exists(name):
        """组织架构如果存在某个联系人则删除"""

        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        if osp.page_should_contain_text2(name):
            osp.click_name_attribute_by_name(name)
            osp.click_accessibility_id_attribute_by_name("删除联系人")
            osp.click_accessibility_id_attribute_by_name("确定")
            osp.wait_for_page_load()

    @staticmethod
    def delete_department_if_exists(name):
        """组织架构如果存在某个部门则删除"""

        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        if osp.page_should_contain_text2(name):
            osp.click_name_attribute_by_name(name)
            osp.click_accessibility_id_attribute_by_name("更多")
            osp.click_accessibility_id_attribute_by_name("部门设置")
            osp.click_delete()
            osp.click_sure()
            osp.wait_for_page_load()


class OrganizationStructureAllTest(TestCase):

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
        2、当前页面在工作台首页
        """

        Preconditions.select_mobile('IOS-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_workbench_page()
            return
        wbp = WorkbenchPage()
        if not wbp.is_on_workbench_page():
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_workbench_page()

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZZJG_0001(self):
        """工作台管理员权限可看到组织架构入口"""

        # 进入组织架构首页
        Preconditions.enter_organization_structure_page()
        osp = OrganizationStructurePage()
        # 1.可正常跳转到组织架构页面
        osp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZZJG_0002(self):
        """从通讯录中进入组织架构"""

        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        workbench_name = wbp.get_workbench_name()
        wbp.open_contacts_page()
        cp = ContactsPage()
        # 进入通讯录-和通讯录(进入通讯录-全部团队)(部分步骤变动)
        cp.wait_for_page_load()
        cp.click_accessibility_id_attribute_by_name("全部团队")
        time.sleep(1)
        # 找到自己是管理员权限的企业通讯录
        cp.click_accessibility_id_attribute_by_name(workbench_name)
        ecp = EnterpriseContactsPage()
        ecp.wait_for_page_load()
        # 点击右上角【...】
        ecp.click_three_points_icon()
        # 点击【团队管理】
        ecp.click_accessibility_id_attribute_by_name("团队管理")
        osp = OrganizationStructurePage()
        # 1.可正常跳转到组织架构页面
        osp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZZJG_0003(self):
        """手动添加联系人"""

        # 点击“组织架构”应用
        Preconditions.enter_organization_structure_page()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        # 确保要添加的联系人能正常添加
        name = "测试号"
        Preconditions.delete_contacts_if_exists(name)
        # 点击“添加联系人”
        osp.click_name_attribute_by_name("添加联系人")
        # 点击“手动输入添加”
        osp.click_name_attribute_by_name("手动输入添加")
        time.sleep(2)
        # 输入姓名：测试号
        osp.input_contacts_name(name)
        number = "15220089861"
        # 输入主手机：15220089861
        osp.input_contacts_number(number)
        # 收起键盘
        osp.click_name_attribute_by_name("完成")
        time.sleep(1)
        # 点击“完成”
        osp.click_confirm()
        # 1.成功添加用户，新添加用户信息与填写信息一致
        self.assertEquals(osp.page_should_contain_text2("成功"), True)
        osp.click_back_button()
        osp.wait_for_page_load()
        self.assertEquals(osp.page_should_contain_text2(name), True)
        self.assertEquals(osp.page_should_contain_text2(number), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZZJG_0004(self):
        """手动添加联系人"""

        # 点击“组织架构”应用
        Preconditions.enter_organization_structure_page()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        # 确保要添加的联系人能正常添加
        name = "测试号0004"
        Preconditions.delete_contacts_if_exists(name)
        # 点击“添加联系人”
        osp.click_name_attribute_by_name("添加联系人")
        # 点击“手动输入添加”
        osp.click_name_attribute_by_name("手动输入添加")
        # 不输入姓名
        osp.click_confirm()
        # 1.添加失败，有对应toast提示
        self.assertEquals(osp.page_should_contain_text2("请输入姓名"), True)
        # 不输入主手机号码
        osp.input_contacts_name(name)
        # 收起键盘
        osp.click_name_attribute_by_name("完成")
        time.sleep(1)
        # 点击“完成”
        osp.click_confirm()
        # 2.提示“请输入姓名”或“请输入手机号”
        self.assertEquals(osp.page_should_contain_text2("请输入手机号"), True)
        osp.input_contacts_number("19877775555")
        # 收起键盘
        osp.click_name_attribute_by_name("完成")
        time.sleep(1)
        osp.click_confirm()
        time.sleep(2)
        osp.click_close()
        # 3.【企业通讯录】【语音通知】等应用调起联系人同步添加
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_enterprise_contacts()
        ecp = EnterpriseContactsPage()
        ecp.wait_for_page_load()
        self.assertEquals(osp.page_should_contain_text2(name), True)
        ecp.click_back_button(2)
        wbp.wait_for_page_load()
        wbp.click_add_voice_notice()
        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        time.sleep(2)
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        self.assertEquals(sccp.page_should_contain_text2(name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZZJG_0005(self):
        """从手机通讯录添加联系人"""

        # 点击“组织架构”应用
        Preconditions.enter_organization_structure_page()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        # 确保要添加的联系人能正常添加
        name = "给个红包1"
        Preconditions.delete_contacts_if_exists(name)
        # 点击“添加联系人”
        osp.click_name_attribute_by_name("添加联系人")
        # 点击“从手机通讯录添加”
        osp.click_name_attribute_by_name("从手机通讯录添加")
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 选择通讯录中的成员，点击【确定】
        slc.selecting_local_contacts_by_name(name)
        slc.click_sure()
        # 1.成功导入联系人，提示【操作成功】
        self.assertEquals(osp.page_should_contain_text2("全部导入成功"), True)
        # 2.页面返回上一级
        self.assertEquals(osp.page_should_contain_text2("添加成员加入团队"), True)
        osp.click_back_button()
        osp.wait_for_page_load()
        osp.click_back_button()
        # 3.【企业通讯录】【语音通知】等应用调起联系人同步添加
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_enterprise_contacts()
        ecp = EnterpriseContactsPage()
        ecp.wait_for_page_load()
        self.assertEquals(osp.page_should_contain_text2(name), True)
        ecp.click_back_button(2)
        wbp.wait_for_page_load()
        wbp.click_add_voice_notice()
        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        time.sleep(2)
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        self.assertEquals(sccp.page_should_contain_text2(name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZZJG_0006(self):
        """从手机通讯录添加搜索的联系人"""

        # 点击“组织架构”应用
        Preconditions.enter_organization_structure_page()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        # 确保要添加的联系人能正常添加
        name = "给个红包1"
        Preconditions.delete_contacts_if_exists(name)
        # 点击“添加联系人”
        osp.click_name_attribute_by_name("添加联系人")
        # 点击“从手机通讯录添加”
        osp.click_name_attribute_by_name("从手机通讯录添加")
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 在搜索框输入关键字
        slc.input_search_keyword(name)
        # 点击联系人
        slc.click_name_attribute_by_name(name)
        # 点击【确定】
        slc.click_sure()
        # 1.成功导入联系人，提示【操作成功】
        self.assertEquals(osp.page_should_contain_text2("全部导入成功"), True)
        # 2.页面返回上一级
        self.assertEquals(osp.page_should_contain_text2("添加成员加入团队"), True)
        osp.click_back_button()
        osp.wait_for_page_load()
        osp.click_back_button()
        # 3.【企业通讯录】【语音通知】等应用调起联系人同步添加
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_enterprise_contacts()
        ecp = EnterpriseContactsPage()
        ecp.wait_for_page_load()
        self.assertEquals(osp.page_should_contain_text2(name), True)
        ecp.click_back_button(2)
        wbp.wait_for_page_load()
        wbp.click_add_voice_notice()
        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        time.sleep(2)
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        self.assertEquals(sccp.page_should_contain_text2(name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZZJG_0007(self):
        """点击邀请小伙伴正常跳转到邀请成员页面"""

        # 点击“组织架构”应用
        Preconditions.enter_organization_structure_page()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        # 点击“添加联系人”
        osp.click_name_attribute_by_name("添加联系人")
        # 点击“邀请小伙伴”(点击“扫描二维码邀请”)(部分步骤变动)
        osp.click_name_attribute_by_name("扫描二维码邀请")
        # 1.成功跳转到邀请成员页面
        self.assertEquals(osp.page_should_contain_text2("申请加入"), True)
        # 操作页面的各个按钮
        osp.click_invite_share()
        # 2.邀请成员页面所有按钮都可以操作
        self.assertEquals(osp.is_exists_share_box(), True)
        osp.click_coordinate(50, 50)
        osp.click_invite_save()
        self.assertEquals(osp.page_should_contain_text2("保存图片成功"), True)
        osp.click_add_qr_code_button()
        self.assertEquals(osp.page_should_contain_text2("新增二维码"), True)
        # 点击返回
        osp.click_back_button(3)
        # 3.返回到组织架构页面
        osp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZZJG_0008(self):
        """点击取消，弹窗隐藏"""

        # 点击“组织架构”应用
        Preconditions.enter_organization_structure_page()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        # 点击“添加联系人”
        osp.click_name_attribute_by_name("添加联系人")
        self.assertEquals(osp.page_should_contain_text2("添加成员加入团队"), True)
        # 点击“取消”(点击返回)(部分步骤变动)
        osp.click_back_button()
        # 1.弹窗隐藏(部分验证点变动)
        self.assertEquals(osp.page_should_contain_text2("添加成员加入团队"), False)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZZJG_0009(self):
        """成功添加一个子部门"""

        # 点击“组织架构”应用
        Preconditions.enter_organization_structure_page()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        # 确保要添加的部门能正常添加
        name = "测试部门0009"
        Preconditions.delete_department_if_exists(name)
        # 点击“添加子部门”
        osp.click_name_attribute_by_name("添加子部门")
        # 输入部门名称：“测试部”
        osp.input_sub_department_name(name)
        # 收起键盘
        osp.click_name_attribute_by_name("完成")
        time.sleep(1)
        # 点击完成
        osp.click_confirm()
        osp.wait_for_page_load()
        # 1.创建成功
        self.assertEquals(osp.page_should_contain_text2(name), True)
        osp.click_back_button()
        # 2.【企业通讯录】【语音通知】等应用调起联系人也同步新增部门
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_enterprise_contacts()
        ecp = EnterpriseContactsPage()
        ecp.wait_for_page_load()
        self.assertEquals(osp.page_should_contain_text2(name), True)
        ecp.click_back_button(2)
        wbp.wait_for_page_load()
        wbp.click_add_voice_notice()
        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        time.sleep(2)
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        self.assertEquals(sccp.page_should_contain_text2(name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZZJG_0010(self):
        """从部门进入扫码审核"""

        Preconditions.enter_organization_structure_page()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        osp.click_name_attribute_by_name("测试部门1")
        # 点击“更多”
        osp.click_accessibility_id_attribute_by_name("更多")
        # 点击“扫码审核”
        osp.click_accessibility_id_attribute_by_name("扫码审核")
        # 1.正常跳转到扫码待审核页面
        self.assertEquals(osp.page_should_contain_text2("待审核"), True)
        osp.click_back_button(2)
        osp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZZJG_0011(self):
        """成功批量删除部门中成员信息"""

        Preconditions.enter_organization_structure_page()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        # 确保有部门成员可删除
        name = "测试部门0011"
        Preconditions.delete_department_if_exists(name)
        osp.click_name_attribute_by_name("添加子部门")
        osp.input_sub_department_name(name)
        osp.input_sub_department_sort("1")
        # 收起键盘
        osp.click_name_attribute_by_name("完成")
        time.sleep(1)
        osp.click_confirm()
        osp.wait_for_page_load()
        osp.click_name_attribute_by_name(name)
        time.sleep(1)
        osp.click_name_attribute_by_name("添加联系人")
        osp.click_name_attribute_by_name("从手机通讯录添加")
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        slc.selecting_local_contacts_by_name("大佬1")
        slc.selecting_local_contacts_by_name("大佬2")
        slc.selecting_local_contacts_by_name("大佬3")
        slc.selecting_local_contacts_by_name("大佬4")
        slc.click_sure()
        time.sleep(2)
        osp.click_back_button()
        # 点击“更多”
        osp.click_name_attribute_by_name("更多")
        # 点击“批量删除成员”
        osp.click_name_attribute_by_name("批量删除成员")
        # 勾选需要删除的成员
        osp.click_name_attribute_by_name("大佬1")
        osp.click_name_attribute_by_name("大佬2")
        osp.click_name_attribute_by_name("大佬3")
        # 点击“确定”
        osp.click_name_attribute_by_name("确定")
        # 1.删除成功
        self.assertEquals(osp.page_should_contain_text2("成功"), True)
        osp.click_close()
        # 2.【企业通讯录】【语音通知】等应用调起联系人也同步删除
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_enterprise_contacts()
        ecp = EnterpriseContactsPage()
        ecp.wait_for_page_load()
        ecp.click_accessibility_id_attribute_by_name(name)
        time.sleep(2)
        self.assertEquals(ecp.page_should_contain_text2("大佬1", 2), False)
        self.assertEquals(ecp.page_should_contain_text2("大佬2", 2), False)
        self.assertEquals(ecp.page_should_contain_text2("大佬3", 2), False)
        self.assertEquals(ecp.page_should_contain_text2("大佬4", 2), True)
        ecp.click_back_button(3)
        wbp.wait_for_page_load()
        wbp.click_add_voice_notice()
        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        time.sleep(2)
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        ecp.click_accessibility_id_attribute_by_name(name)
        time.sleep(2)
        self.assertEquals(ecp.page_should_contain_text2("大佬1", 2), False)
        self.assertEquals(ecp.page_should_contain_text2("大佬2", 2), False)
        self.assertEquals(ecp.page_should_contain_text2("大佬3", 2), False)
        self.assertEquals(ecp.page_should_contain_text2("大佬4", 2), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZZJG_0017(self):
        """当前页面无成员"""

        Preconditions.enter_organization_structure_page()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        # 确保当前页面无联系人
        osp.delete_all_contacts_if_exists()
        # 点击“更多”
        osp.click_name_attribute_by_name("更多")
        # 点击“批量删除成员”
        osp.click_name_attribute_by_name("批量删除成员")
        # 1.页面提示“暂无成员”(部分验证点变动)
        self.assertEquals(osp.page_should_contain_text2("请选择联系人"), True)
        osp.click_back_button()
        osp.wait_for_page_load()

    @staticmethod
    def tearDown_test_ZZJG_0017():
        """恢复环境"""

        try:
            fail_time = 0
            while fail_time < 5:
                try:
                    Preconditions.make_already_in_message_page()
                    contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                    Preconditions.create_he_contacts(contact_names)
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZZJG_0018(self):
        """搜索已经存在的成员姓名"""

        # 点击“组织架构”应用
        Preconditions.enter_organization_structure_page()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        name = "大佬1"
        # 搜索已存在成员姓名
        osp.input_search_box(name)
        # 收起键盘
        osp.click_name_attribute_by_name("完成")
        # 1.列举所有包含搜索词条的成员名单
        self.assertEquals(osp.page_should_contain_text2(name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZZJG_0019(self):
        """搜索已经存在的成员电话（最少输入电话号码前6位）"""

        # 点击“组织架构”应用
        Preconditions.enter_organization_structure_page()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        number = "13800138005"
        # 搜索已存在成员电话号码（最少输入电话号码前6位）
        osp.input_search_box(number)
        # 收起键盘
        osp.click_name_attribute_by_name("完成")
        # 1.列举所有符合搜索词条的成员名单
        self.assertEquals(osp.page_should_contain_text2(number), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZZJG_0020(self):
        """搜索不经存在的成员姓名"""

        # 点击“组织架构”应用
        Preconditions.enter_organization_structure_page()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        # 搜索不存在成员姓名
        osp.input_search_box("不存在")
        # 收起键盘
        osp.click_name_attribute_by_name("完成")
        # 1.没有搜索结果，提示“暂无成员”
        self.assertEquals(osp.page_should_contain_text2("暂无成员"), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZZJG_0021(self):
        """搜索不存在的成员电话（最少输入电话号码前6位）"""

        # 点击“组织架构”应用
        Preconditions.enter_organization_structure_page()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        # 搜索不存在成员电话号码（最少输入电话号码前6位）
        osp.input_search_box("123456")
        # 收起键盘
        osp.click_name_attribute_by_name("完成")
        # 1.没有搜索结果，提示“暂无成员”
        self.assertEquals(osp.page_should_contain_text2("暂无成员"), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZZJG_0022(self):
        """点击顶部返回键，返回到上一级页面"""

        # 点击“组织架构”应用
        Preconditions.enter_organization_structure_page()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        # 组织架构首页点击顶部返回键【 < 】
        osp.click_back_button()
        wbp = WorkbenchPage()
        # 1.返回到工作台页面
        wbp.wait_for_page_load()
        wbp.click_organization()
        osp.wait_for_page_load()
        osp.click_name_attribute_by_name("添加联系人")
        time.sleep(1)
        # 组织架构其他页面点击顶部返回键【 < 】
        osp.click_back_button()
        # 2.如果在应用其他页面，返回到上一级页面
        osp.wait_for_page_load()




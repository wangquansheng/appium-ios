import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import MessagePage
from pages.workbench.Workbench import WorkbenchPage
from pages.workbench.group_messenger.SelectCompanyContacts import SelectCompanyContactsPage
from pages.workbench.super_meeting.SuperConference import SuperConferencePage
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
    def enter_super_conference_page():
        """进入超级会议首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_super_meeting()


class SuperMeetingAllTest(TestCase):
    """超级会议"""

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在超级会议首页
        """

        Preconditions.select_mobile('IOS-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_super_conference_page()
            return
        smp = SuperConferencePage()
        if not smp.is_on_super_meeting_page():
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_super_conference_page()

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_CJHY_0001(self):
        """查看超级会议使用说明"""

        smp = SuperConferencePage()
        smp.wait_for_page_load()
        # 点击超级会议顶部下拉箭头
        smp.click_down_triangle()
        # 点击“使用指南”
        smp.click_help_icon()
        # 1.正常跳转到超级会议使用说明页面
        self.assertEquals(smp.page_should_contain_text2("超级会议使用说明"), True)
        # 上下滑动浏览页面
        smp.driver.execute_script('mobile: scroll', {'direction': 'down'})
        # 2.上下滑动可正常浏览页面，无异常，不报错
        self.assertEquals(smp.page_should_contain_text2("计费标准"), True)
        smp.driver.execute_script('mobile: scroll', {'direction': 'up'})
        self.assertEquals(smp.page_should_contain_text2("发起超级会议"), True)
        smp.click_back_button()
        smp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_CJHY_0022(self):
        """用户不在任何部门下"""

        smp = SuperConferencePage()
        smp.wait_for_page_load()
        smp.click_appointment_meeting()
        # 点击“+”添加联系人(点击企业通讯录)(部分步骤变动)
        smp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        # 等待选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.直接进入企业子一层级
        self.assertEquals(sccp.is_exist_corporate_grade(), True)
        # 点击返回或者企业通讯录
        sccp.click_back_button()
        # 2.页面跳转到企业层级
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exist_department_name(), True)
        smp.click_back_button(2)
        smp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_CJHY_0023(self):
        """用户在企业部门下"""

        smp = SuperConferencePage()
        smp.wait_for_page_load()
        # 确保用户在企业部门下
        smp.click_back_button()
        wbp = WorkbenchPage()
        # 添加本机号码到指定部门
        department_name = "admin_department"
        Preconditions.add_phone_number_to_department(department_name)
        workbench_name = wbp.get_workbench_name()
        wbp.click_super_meeting()
        smp.wait_for_page_load()
        smp.click_appointment_meeting()
        # 点击“+”添加联系人(点击企业通讯录)(部分步骤变动)
        smp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        # 等待选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.跳转后直接进入企业层级：企业+部门名称
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exists_accessibility_id_attribute_by_name(workbench_name), True)
        self.assertEquals(sccp.is_exists_accessibility_id_attribute_by_name(department_name), True)
        smp.click_back_button(2)
        smp.wait_for_page_load()

    @staticmethod
    def tearDown_test_CJHY_0023():
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
                    wbp.click_super_meeting()
                    smp = SuperConferencePage()
                    smp.wait_for_page_load()
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_CJHY_0024(self):
        """用户在企业部门下又在企业子一层级中，直接进入企业层级"""

        smp = SuperConferencePage()
        smp.wait_for_page_load()
        # 确保用户既在企业部门下又在企业子一层级
        smp.click_back_button()
        wbp = WorkbenchPage()
        # 添加本机号码到指定部门
        department_name = "admin_department"
        Preconditions.add_phone_number_to_department(department_name)
        # 添加本机号码到和通讯录
        Preconditions.add_phone_number_to_he_contacts()
        workbench_name = wbp.get_workbench_name()
        wbp.click_super_meeting()
        smp.wait_for_page_load()
        smp.click_appointment_meeting()
        # 点击“+”添加联系人(点击企业通讯录)(部分步骤变动)
        smp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        # 等待选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.跳转后直接进入企业层级：企业+部门名称
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exists_accessibility_id_attribute_by_name(workbench_name), True)
        self.assertEquals(sccp.is_exists_accessibility_id_attribute_by_name(department_name), True)
        smp.click_back_button(2)
        smp.wait_for_page_load()

    @staticmethod
    def tearDown_test_CJHY_0024():
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
                    wbp.click_super_meeting()
                    smp = SuperConferencePage()
                    smp.wait_for_page_load()
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_CJHY_0025(self):
        """用户同时在两个部门下"""

        smp = SuperConferencePage()
        smp.wait_for_page_load()
        # 确保用户在企业部门下
        smp.click_back_button()
        wbp = WorkbenchPage()
        # 添加本机号码到指定部门1
        department_name1 = "admin_department1"
        Preconditions.add_phone_number_to_department(department_name1)
        # 添加本机号码到指定部门2
        department_name2 = "admin_department2"
        Preconditions.add_phone_number_to_department(department_name2)
        workbench_name = wbp.get_workbench_name()
        wbp.click_super_meeting()
        smp.wait_for_page_load()
        smp.click_appointment_meeting()
        # 点击“+”添加联系人(点击企业通讯录)(部分步骤变动)
        smp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        # 等待选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.跳转后显示企业层级：企业+部门名称（部门随机显示一个）
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exists_accessibility_id_attribute_by_name(workbench_name), True)
        self.assertEquals((sccp.is_exists_accessibility_id_attribute_by_name(
            department_name1) or sccp.is_exists_accessibility_id_attribute_by_name(department_name2)), True)
        smp.click_back_button(2)
        smp.wait_for_page_load()

    @staticmethod
    def tearDown_test_CJHY_0025():
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
                    wbp.click_super_meeting()
                    smp = SuperConferencePage()
                    smp.wait_for_page_load()
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_CJHY_0058(self):
        """点击顶部返回键"""

        smp = SuperConferencePage()
        smp.wait_for_page_load()
        # 超级会议首页点击顶部【<】
        smp.click_back_button()
        wbp = WorkbenchPage()
        # 1.如果在首页，则返回到工作台
        wbp.wait_for_page_load()
        wbp.click_super_meeting()
        smp.wait_for_page_load()
        smp.click_help_icon()
        self.assertEquals(smp.page_should_contain_text2("超级会议使用说明"), True)
        # 超级会议其他页面点击顶部【<】
        smp.click_back_button()
        # 2.如果在其他页面，则返回到上一级页面
        smp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_CJHY_0059(self):
        """点击顶部关闭按钮"""

        smp = SuperConferencePage()
        smp.wait_for_page_load()
        smp.click_help_icon()
        self.assertEquals(smp.page_should_contain_text2("超级会议使用说明"), True)
        # 在其他有关闭按钮页面，点击顶部【x】
        smp.click_close()
        wbp = WorkbenchPage()
        # 1.关闭超级会议，返回到工作台页面
        wbp.wait_for_page_load()
        wbp.click_super_meeting()
        smp.wait_for_page_load()

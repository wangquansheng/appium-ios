import time

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile, switch_to_mobile, current_driver
from pages import AgreementDetailPage
from pages import CallPage
from pages import ChatWindowPage
from pages import ContactDetailsPage
from pages import ContactListSearchPage
from pages import ContactsPage
from pages import CreateContactPage
from pages import GroupChatPage
from pages import GuidePage
from pages import MessagePage
from pages import OneKeyLoginPage
from pages import PermissionListPage
from pages import SelectContactsPage
from pages import SelectOneGroupPage
from pages import SingleChatPage
from pages import WorkbenchPage
from pages.components import BaseChatPage
from pages.workbench.enterprise_contacts.EnterpriseContacts import EnterpriseContactsPage
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    # 'Android-移动': 'single_mobile',
    'IOS-移动': '',
    'Android-电信': 'single_telecom',
    'Android-联通': 'single_union',
    'Android-移动-联通': 'mobile_and_union',
    'Android-移动-电信': '',
    'Android-移动-移动': 'double_mobile',
    'Android-XX-XX': 'others_double',
}


class Preconditions(object):
    """前置条件"""

    @staticmethod
    def select_mobile(category, reset=False):
        """选择手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        if reset:
            current_mobile().reset_app()
        return client

    @staticmethod
    def make_already_in_one_key_login_page():
        """已经进入一键登录页"""
        # 如果当前页面已经是一键登录页，不做任何操作
        one_key = OneKeyLoginPage()
        if one_key.is_on_this_page():
            return

        # 如果当前页不是引导页第一页，重新启动app
        guide_page = GuidePage()
        if not guide_page.is_on_the_first_guide_page():
            # current_mobile().launch_app()
            current_mobile().reset_app()
            guide_page.wait_for_page_load(20)

        # 跳过引导页
        guide_page.wait_for_page_load(30)
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
        current_mobile().hide_keyboard_if_display()
        guide_page.click_start_the_experience()

        # 点击权限列表页面的确定按钮
        permission_list = PermissionListPage()
        permission_list.click_submit_button()
        one_key.wait_for_page_load(30)

    @staticmethod
    def login_by_one_key_login():
        """
        从一键登录页面登录
        :return:
        """
        # 等待号码加载完成后，点击一键登录
        one_key = OneKeyLoginPage()
        one_key.wait_for_page_load()
        # one_key.wait_for_tell_number_load(60)
        one_key.click_one_key_login()
        if one_key.have_read_agreement_detail():
            one_key.click_read_agreement_detail()
            # 同意协议
            agreement = AgreementDetailPage()
            agreement.click_agree_button()
        # 等待消息页
        message_page = MessagePage()
        message_page.wait_login_success(60)

    @staticmethod
    def make_already_in_message_page(reset_required=False):
        """确保应用在消息页面"""

        if not reset_required:
            message_page = MessagePage()
            if message_page.is_on_this_page():
                return
            else:
                try:
                    current_mobile().terminate_app('com.chinasofti.rcs', timeout=2000)
                except:
                    pass
                current_mobile().launch_app()
            try:
                message_page.wait_until(
                    condition=lambda d: message_page.is_on_this_page(),
                    timeout=3
                )
                return
            except TimeoutException:
                pass
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""

        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def enter_workbench_page():
        """进入工作台首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()

    @staticmethod
    def enter_enterprise_contacts_page():
        """进入企业通讯录首页"""

        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_add_enterprise_contacts()
        ecp = EnterpriseContactsPage()
        ecp.wait_for_page_load()

    @staticmethod
    def add_phone_number_to_department(department_name):
        """添加本机号码到指定部门"""

        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        time.sleep(5)
        n = 1
        # 解决工作台不稳定问题
        while osp.is_text_present("账号认证失败"):
            osp.click_back()
            wbp.wait_for_workbench_page_load()
            wbp.click_organization()
            time.sleep(5)
            n += 1
            if n > 10:
                break
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        time.sleep(3)
        if not osp.is_exist_specify_element_by_name(department_name):
            osp.click_specify_element_by_name("添加子部门")
            time.sleep(2)
            osp.input_sub_department_name(department_name)
            osp.input_sub_department_sort("1")
            osp.click_confirm()
            if osp.is_toast_exist("部门已存在", 2):
                osp.click_back()
            osp.wait_for_page_load()
        osp.click_specify_element_by_name(department_name)
        time.sleep(2)
        osp.click_specify_element_by_name("添加联系人")
        time.sleep(2)
        osp.click_specify_element_by_name("手动输入添加")
        osp.input_contacts_name("admin")
        osp.input_contacts_number(phone_number)
        osp.click_confirm()
        osp.click_close()
        wbp.wait_for_workbench_page_load()

    @staticmethod
    def delete_department_by_name(department_name):
        """删除指定部门"""

        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        time.sleep(5)
        n = 1
        # 解决工作台不稳定问题
        while osp.is_text_present("账号认证失败"):
            osp.click_back()
            wbp.wait_for_workbench_page_load()
            wbp.click_organization()
            time.sleep(5)
            n += 1
            if n > 10:
                break
        time.sleep(5)
        if osp.is_exist_specify_element_by_name(department_name):
            osp.click_specify_element_by_name(department_name)
            time.sleep(2)
            osp.click_specify_element_by_name("更多")
            time.sleep(2)
            osp.click_specify_element_by_name("部门设置")
            time.sleep(2)
            osp.click_delete()
            osp.click_sure()
        osp.click_back()
        wbp.wait_for_workbench_page_load()

    @staticmethod
    def add_phone_number_to_he_contacts():
        """添加本机号码到和通讯录"""

        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        time.sleep(5)
        n = 1
        # 解决工作台不稳定问题
        while osp.is_text_present("账号认证失败"):
            osp.click_back()
            wbp.wait_for_workbench_page_load()
            wbp.click_organization()
            time.sleep(5)
            n += 1
            if n > 10:
                break
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        time.sleep(3)
        if not osp.is_exist_specify_element_by_name(phone_number):
            osp.click_specify_element_by_name("添加联系人")
            time.sleep(2)
            osp.click_specify_element_by_name("手动输入添加")
            osp.input_contacts_name("admin")
            osp.input_contacts_number(phone_number)
            osp.click_confirm()
            osp.wait_for_page_load()
        osp.click_back()
        wbp.wait_for_workbench_page_load()

class EnterpriseContactsAllTest(TestCase):
    """
    模块：工作台->企业通讯录
    文件位置：20190313工作台全量用例整理.xlsx
    表格：工作台->企业通讯录
    Author：刘晓东
    """

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在工作台首页
        """

        Preconditions.select_mobile('Android-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_workbench_page()
            return
        wbp = WorkbenchPage()
        if wbp.is_on_workbench_page():
            current_mobile().hide_keyboard_if_display()
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_workbench_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYTXL_0001(self):
        """用户不在任何部门下直接进入企业子一层级"""

        # 进入企业通讯录首页
        Preconditions.enter_enterprise_contacts_page()
        ecp = EnterpriseContactsPage()
        # 1.是否直接进入企业子一层级
        self.assertEquals(ecp.is_exist_corporate_grade(), True)
        ecp.click_back()
        time.sleep(2)
        # 2.页面是否跳转到企业层级
        self.assertEquals(ecp.is_exist_corporate_grade(), False)
        self.assertEquals(ecp.is_exist_department_name(), True)
        ecp.click_back()
        # 等待工作台首页加载
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYTXL_0002(self):
        """用户在企业部门下直接进入企业层级"""

        wbp = WorkbenchPage()
        # 添加本机号码到指定部门
        department_name = "admin_department"
        Preconditions.add_phone_number_to_department(department_name)
        workbench_name = wbp.get_workbench_name()
        # 解决用户部门变更后不能及时刷新的问题
        wbp.click_company_contacts()
        ecp = EnterpriseContactsPage()
        ecp.wait_for_page_load()
        ecp.click_back()
        time.sleep(1)
        ecp.click_back()
        wbp.wait_for_workbench_page_load()
        wbp.click_company_contacts()
        ecp.wait_for_page_load()
        # 1.是否直接进入企业层级：企业+部门名称
        self.assertEquals(ecp.is_exist_corporate_grade(), False)
        self.assertEquals(ecp.is_exist_department_by_name(workbench_name), True)
        self.assertEquals(ecp.is_exist_department_by_name(department_name), True)
        ecp.click_back()
        wbp.wait_for_workbench_page_load()

    @staticmethod
    def tearDown_test_QYTXL_0002():
        """恢复环境"""

        fail_time = 0
        while fail_time < 5:
            try:
                Preconditions.make_already_in_message_page()
                mp = MessagePage()
                mp.open_workbench_page()
                wbp = WorkbenchPage()
                Preconditions.delete_department_by_name("admin_department")
                # 解决用户部门变更后不能及时刷新的问题
                wbp.click_company_contacts()
                ecp = EnterpriseContactsPage()
                ecp.wait_for_page_load()
                ecp.click_back()
                time.sleep(2)
                if ecp.is_exist_department_name():
                    ecp.click_back()
                wbp.wait_for_workbench_page_load()
                return
            except:
                fail_time += 1

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYTXL_0003(self):
        """用户在企业部门下又在企业子一层级中，直接进入企业层级"""

        wbp = WorkbenchPage()
        # 添加本机号码到指定部门
        department_name = "admin_department"
        Preconditions.add_phone_number_to_department(department_name)
        # 添加本机号码到和通讯录
        Preconditions.add_phone_number_to_he_contacts()
        workbench_name = wbp.get_workbench_name()
        # 解决用户部门变更后不能及时刷新的问题
        wbp.click_company_contacts()
        ecp = EnterpriseContactsPage()
        ecp.wait_for_page_load()
        ecp.click_back()
        time.sleep(1)
        ecp.click_back()
        wbp.wait_for_workbench_page_load()
        wbp.click_company_contacts()
        ecp.wait_for_page_load()
        # 1.是否直接进入企业层级：企业+部门名称
        self.assertEquals(ecp.is_exist_corporate_grade(), False)
        self.assertEquals(ecp.is_exist_department_by_name(workbench_name), True)
        self.assertEquals(ecp.is_exist_department_by_name(department_name), True)
        ecp.click_back()
        wbp.wait_for_workbench_page_load()

    @staticmethod
    def tearDown_test_QYTXL_0003():
        """恢复环境"""

        fail_time = 0
        while fail_time < 5:
            try:
                Preconditions.make_already_in_message_page()
                mp = MessagePage()
                mp.open_workbench_page()
                wbp = WorkbenchPage()
                Preconditions.delete_department_by_name("admin_department")
                # 解决用户部门变更后不能及时刷新的问题
                wbp.click_company_contacts()
                ecp = EnterpriseContactsPage()
                ecp.wait_for_page_load()
                ecp.click_back()
                time.sleep(2)
                if ecp.is_exist_department_name():
                    ecp.click_back()
                wbp.wait_for_workbench_page_load()
                return
            except:
                fail_time += 1

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYTXL_0004(self):
        """用户同时在两个部门下直接进入企业层级"""

        wbp = WorkbenchPage()
        # 添加本机号码到指定部门1
        department_name1 = "admin_department1"
        Preconditions.add_phone_number_to_department(department_name1)
        # 添加本机号码到指定部门2
        department_name2 = "admin_department2"
        Preconditions.add_phone_number_to_department(department_name2)
        workbench_name = wbp.get_workbench_name()
        # 解决用户部门变更后不能及时刷新的问题
        wbp.click_company_contacts()
        ecp = EnterpriseContactsPage()
        ecp.wait_for_page_load()
        ecp.click_back()
        time.sleep(1)
        ecp.click_back()
        wbp.wait_for_workbench_page_load()
        wbp.click_company_contacts()
        ecp.wait_for_page_load()
        # 1.跳转后是否显示企业层级：企业+部门名称（部门随机显示一个）
        self.assertEquals(ecp.is_exist_corporate_grade(), False)
        self.assertEquals(ecp.is_exist_department_by_name(workbench_name), True)
        self.assertEquals((ecp.is_exist_department_by_name(department_name1) or ecp.is_exist_department_by_name(department_name2)), True)
        ecp.click_back()
        wbp.wait_for_workbench_page_load()

    @staticmethod
    def tearDown_test_QYTXL_0004():
        """恢复环境"""

        fail_time = 0
        while fail_time < 5:
            try:
                Preconditions.make_already_in_message_page()
                mp = MessagePage()
                mp.open_workbench_page()
                wbp = WorkbenchPage()
                Preconditions.delete_department_by_name("admin_department1")
                Preconditions.delete_department_by_name("admin_department2")
                # 解决用户部门变更后不能及时刷新的问题
                wbp.click_company_contacts()
                ecp = EnterpriseContactsPage()
                ecp.wait_for_page_load()
                ecp.click_back()
                time.sleep(2)
                if ecp.is_exist_department_name():
                    ecp.click_back()
                wbp.wait_for_workbench_page_load()
                return
            except:
                fail_time += 1

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYTXL_0008(self):
        """验证点击返回按钮是否正确"""

        # 进入企业通讯录首页
        Preconditions.enter_enterprise_contacts_page()
        ecp = EnterpriseContactsPage()
        # 点击【<】返回
        ecp.click_back()
        time.sleep(1)
        ecp.click_back()
        # 1.等待工作台首页加载
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYTXL_0009(self):
        """精确搜索（数字、中文、英文）"""

        # 进入企业通讯录首页
        Preconditions.enter_enterprise_contacts_page()
        ecp = EnterpriseContactsPage()
        # 点击搜索框
        ecp.click_search_box()
        search_name = "陈丹丹"
        ecp.input_search_message(search_name)
        time.sleep(2)
        # 1.检查搜索结果是否完全匹配关键字
        self.assertEquals(ecp.is_search_contacts_name_full_match(search_name), True)
        search_name2 = "alice"
        ecp.input_search_message(search_name2)
        time.sleep(2)
        # 2.检查搜索结果是否完全匹配关键字
        self.assertEquals(ecp.is_search_contacts_name_full_match(search_name2), True)
        search_number = "13802883296"
        ecp.input_search_message(search_number)
        time.sleep(2)
        # 3.检查搜索结果是否完全匹配关键字
        self.assertEquals(ecp.is_search_contacts_number_full_match(search_number), True)
        ecp.click_return()
        time.sleep(1)
        ecp.click_back()
        time.sleep(1)
        ecp.click_back()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYTXL_0010(self):
        """模糊搜索（数字、中文、英文）"""

        # 进入企业通讯录首页
        Preconditions.enter_enterprise_contacts_page()
        ecp = EnterpriseContactsPage()
        # 点击搜索框
        ecp.click_search_box()
        search_name = "陈"
        ecp.input_search_message(search_name)
        time.sleep(2)
        # 1.检查搜索结果是否模糊匹配关键字
        self.assertEquals(ecp.is_search_contacts_name_match(search_name), True)
        search_name2 = "zhg"
        ecp.input_search_message(search_name2)
        time.sleep(2)
        # 2.检查搜索结果是否模糊匹配关键字
        self.assertEquals(ecp.is_search_contacts_name_match("郑海贵"), True)
        search_number = "138028"
        ecp.input_search_message(search_number)
        time.sleep(2)
        # 3.检查搜索结果是否模糊匹配关键字
        self.assertEquals(ecp.is_search_contacts_number_match(search_number), True)
        ecp.click_return()
        time.sleep(1)
        ecp.click_back()
        time.sleep(1)
        ecp.click_back()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYTXL_0011(self):
        """网络异常下搜索企业通讯录联系人"""

        # 进入企业通讯录首页
        Preconditions.enter_enterprise_contacts_page()
        ecp = EnterpriseContactsPage()
        # 设置手机网络断开
        ecp.set_network_status(0)
        # 点击搜索框
        ecp.click_search_box()
        search_name = "大佬1"
        ecp.input_search_message(search_name)
        # 1.页面是否出现网络异常提示
        self.assertEquals(ecp.is_toast_exist("网络连接异常"), True)
        self.assertEquals(ecp.is_text_present("网络出错，轻触屏幕重新加载"), True)
        ecp.click_return()
        time.sleep(1)
        ecp.click_back()
        time.sleep(1)
        ecp.click_back()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()

    @staticmethod
    def tearDown_test_QYTXL_0011():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYTXL_0012(self):
        """搜索企业通讯录联系人结果展示"""

        # 进入企业通讯录首页
        Preconditions.enter_enterprise_contacts_page()
        ecp = EnterpriseContactsPage()
        # 点击搜索框
        ecp.click_search_box()
        search_name = "陈丹丹"
        ecp.input_search_message(search_name)
        time.sleep(2)
        # 1.是否显示头像、姓名、号码、公司部门（没公司部门的不显示）
        self.assertEquals(ecp.is_exists_contacts_image(), True)
        self.assertEquals(ecp.is_exists_contacts_name(), True)
        self.assertEquals(ecp.is_exists_contacts_number(), True)
        self.assertEquals(ecp.is_exists_value_by_name(search_name), True)
        ecp.click_return()
        time.sleep(1)
        ecp.click_back()
        time.sleep(1)
        ecp.click_back()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYTXL_0013(self):
        """点击搜索结果已保存到本地的RCS用户进入联系人详情页"""

        # 进入企业通讯录首页
        Preconditions.enter_enterprise_contacts_page()
        ecp = EnterpriseContactsPage()
        # 点击搜索框
        ecp.click_search_box()
        search_name = "大佬1"
        ecp.input_search_message(search_name)
        time.sleep(2)
        ecp.click_contacts_by_name(search_name)
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        # 1.是否显示用户的详情信息（副号拨打没做验证，需要提供满足条件的测试号码）
        self.assertEquals(cdp.is_exists_contacts_name(), True)
        self.assertEquals(cdp.is_exists_contacts_number(), True)
        self.assertEquals(cdp.is_exists_contacts_image(), True)
        self.assertEquals(cdp.is_exists_value_by_name("公司"), True)
        self.assertEquals(cdp.is_exists_value_by_name("职位"), True)
        self.assertEquals(cdp.is_exists_value_by_name("邮箱"), True)
        self.assertEquals(cdp.is_exists_message_icon(), True)
        self.assertEquals(cdp.is_exists_call_icon(), True)
        self.assertEquals(cdp.is_exists_voice_call_icon(), True)
        self.assertEquals(cdp.is_exists_video_call_icon(), True)
        self.assertEquals(cdp.is_exists_dial_hefeixin_icon(), True)
        self.assertEquals(cdp.is_exists_share_card_icon(), True)
        # 返回工作台
        cdp.click_back_icon()
        time.sleep(1)
        ecp.click_return()
        time.sleep(1)
        ecp.click_back()
        time.sleep(1)
        ecp.click_back()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYTXL_0015(self):
        """点击搜索结果已保存到本地的本机用户进入联系人详情页"""

        # 进入企业通讯录首页
        Preconditions.enter_enterprise_contacts_page()
        ecp = EnterpriseContactsPage()
        # 点击搜索框
        ecp.click_search_box()
        search_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        ecp.input_search_message(search_number)
        time.sleep(2)
        ecp.click_contacts_by_number(search_number)
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        time.sleep(2)
        # 确保本机用户已保存到本地
        if cdp.is_exists_save_contacts_icon():
            cdp.click_save_contacts_icon()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            ccp.save_contact()
            cdp.wait_for_page_load()
            time.sleep(2)
        # 1.是否显示用户的详情信息（副号拨打没做验证，需要提供满足条件的测试号码）
        self.assertEquals(cdp.is_exists_contacts_name(), True)
        self.assertEquals(cdp.is_exists_contacts_number(), True)
        self.assertEquals(cdp.is_exists_contacts_image(), True)
        self.assertEquals(cdp.is_exists_value_by_name("公司"), True)
        self.assertEquals(cdp.is_exists_value_by_name("职位"), True)
        self.assertEquals(cdp.is_exists_value_by_name("邮箱"), True)
        self.assertEquals(cdp.is_exists_message_icon(), True)
        self.assertEquals(cdp.is_exists_call_icon(), True)
        self.assertEquals(cdp.is_exists_voice_call_icon(), True)
        self.assertEquals(cdp.is_exists_video_call_icon(), True)
        self.assertEquals(cdp.is_exists_dial_hefeixin_icon(), True)
        self.assertEquals(cdp.is_exists_share_card_icon(), True)
        # 点击分享名片
        cdp.click_share_card_icon()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        name = "群聊1"
        # 分享名片到一个普通群
        sog.selecting_one_group_by_name(name)
        time.sleep(2)
        sog.click_text("发送名片")
        # 2.是否提示已发送
        self.assertEquals(sog.is_toast_exist("已发送"), True)
        time.sleep(2)
        # 3.验证消息、电话、语音视频、视频电话、副号拨打（需要提供满足条件的测试号码）、和飞信电话是否置灰，不可点击
        self.assertEquals(cdp.message_icon_is_enabled(), False)
        self.assertEquals(cdp.call_icon_is_enabled(), False)
        self.assertEquals(cdp.voice_call_icon_is_enabled(), False)
        self.assertEquals(cdp.video_call_icon_is_enabled(), False)
        self.assertEquals(cdp.dial_hefeixin_icon_is_enabled(), False)
        # 返回消息页面验证是否发送成功
        cdp.click_back_icon()
        time.sleep(1)
        ecp.click_return()
        time.sleep(1)
        ecp.click_back()
        time.sleep(1)
        ecp.click_back()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        mp = MessagePage()
        mp.open_message_page()
        mp.wait_for_page_load()
        mp.choose_chat_by_name(name)
        time.sleep(2)
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        gcp = GroupChatPage()
        # 返回工作台
        gcp.click_back()
        mp.wait_for_page_load()
        mp.open_workbench_page()
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYTXL_0016(self):
        """点击搜索结果未保存到本地的RCS用户进入Profile页"""

        # 进入企业通讯录首页
        Preconditions.enter_enterprise_contacts_page()
        ecp = EnterpriseContactsPage()
        # 点击搜索框
        ecp.click_search_box()
        search_name = "陈丹丹"
        ecp.input_search_message(search_name)
        time.sleep(2)
        ecp.click_contacts_by_name(search_name)
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        # 1.是否显示用户的详情信息（副号拨打没做验证，需要提供满足条件的测试号码）
        self.assertEquals(cdp.is_exists_contacts_name(), True)
        self.assertEquals(cdp.is_exists_contacts_number(), True)
        self.assertEquals(cdp.is_exists_contacts_image(), True)
        self.assertEquals(cdp.is_exists_value_by_name("公司"), True)
        self.assertEquals(cdp.is_exists_value_by_name("职位"), True)
        self.assertEquals(cdp.is_exists_value_by_name("邮箱"), True)
        self.assertEquals(cdp.is_exists_message_icon(), True)
        self.assertEquals(cdp.is_exists_call_icon(), True)
        self.assertEquals(cdp.is_exists_voice_call_icon(), True)
        self.assertEquals(cdp.is_exists_video_call_icon(), True)
        self.assertEquals(cdp.is_exists_dial_hefeixin_icon(), True)
        self.assertEquals(cdp.is_exists_save_contacts_icon(), True)
        # 2.点击各个按钮验证（副号拨打没做验证，需要提供满足条件的测试号码）
        # 点击联系人头像
        cdp.click_contacts_image()
        time.sleep(5)
        # 验证是否显示大图
        self.assertEquals(cdp.is_exists_big_avatar(), True)
        # 返回
        cdp.click_big_avatar()
        time.sleep(2)
        # 点击消息图标
        cdp.click_message_icon()
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            bcp.click_i_have_read()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        scp.click_back()
        time.sleep(2)
        # 点击电话图标
        cdp.click_call_icon()
        time.sleep(4)
        # 验证是否在通话界面
        self.assertEquals(cdp.is_phone_in_calling_state(), True)
        cp = CallPage()
        # 挂断电话
        cp.hang_up_the_call()
        time.sleep(2)
        # 点击语音通话图标
        cdp.click_voice_call_icon()
        time.sleep(4)
        if cdp.is_text_present("继续拨打"):
            cdp.click_text("继续拨打")
            time.sleep(2)
        if cdp.is_text_present("暂不开启"):
            cdp.click_text("暂不开启")
            time.sleep(2)
        # 验证是否弹出语音会话弹窗
        self.assertEquals(cdp.is_text_present("正在呼叫"), True)
        # 挂断语音通话
        cp.hang_up_voice_call()
        time.sleep(2)
        # 点击视频通话图标
        cdp.click_video_call_icon()
        time.sleep(4)
        if cdp.is_text_present("继续拨打"):
            cdp.click_text("继续拨打")
            time.sleep(2)
        if cdp.is_text_present("暂不开启"):
            cdp.click_text("暂不开启")
            time.sleep(2)
        # 验证是否弹出视频会话弹窗
        self.assertEquals(cdp.is_text_present("视频通话呼叫中"), True)
        # 挂断视频通话
        cp.hang_up_video_call()
        # 点击和飞信电话
        cdp.click_hefeixin_call_menu()
        time.sleep(2)
        if cdp.is_text_present("我知道了"):
            cdp.click_text("我知道了")
            time.sleep(2)
        if cdp.is_text_present("始终允许"):
            cdp.click_text("始终允许")
            time.sleep(2)
        if cdp.is_text_present("和飞信电话"):
            cp.hang_up_the_call()
            time.sleep(2)
        if cdp.is_text_present("暂不开启"):
            cdp.click_text("暂不开启")
            time.sleep(2)
        # 验证是否拨打和飞信电话
        self.assertEquals(cdp.is_text_present("请先接听来电，随后将自动呼叫对方"), True)
        # 挂断和飞信电话
        cp.hang_up_hefeixin_call()
        time.sleep(2)
        # 3.点击保存到通讯录按钮，进入编辑联系人页面，验证每个字段都可以编辑并保存成功
        cdp.click_save_contacts_icon()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        ccp.create_contact("陈丹丹", "13800137004", "test_work", "员工", "13800137004@139.com")
        time.sleep(2)
        # 是否保存成功
        self.assertEquals(cdp.is_exists_share_card_icon(), True)
        self.assertEquals(cdp.is_exists_save_contacts_icon(), False)

    @staticmethod
    def tearDown_test_QYTXL_0016():
        """恢复环境"""

        Preconditions.make_already_in_message_page()
        mp = MessagePage()
        mp.open_contacts_page()
        cp = ContactsPage()
        cp.wait_for_page_load()
        # 删除指定联系人
        cp.click_search_box()
        name = "陈丹丹"
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword(name)
        if contact_search.is_contact_in_list(name):
            cp.select_contacts_by_name(name)
            cdp = ContactDetailsPage()
            cdp.wait_for_page_load()
            cdp.click_edit_contact()
            time.sleep(1)
            current_mobile().hide_keyboard_if_display()
            time.sleep(1)
            cdp.change_delete_number()
            cdp.click_sure_delete()
        contact_search.click_back()
        cp.wait_for_page_load()
        mp.open_workbench_page()
        wbp = WorkbenchPage()
        # 返回工作台
        wbp.wait_for_workbench_page_load()
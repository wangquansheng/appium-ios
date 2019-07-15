import time

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile
from pages import ContactDetailsPage
from pages import ContactsPage
from pages import CreateContactPage
from pages import GroupChatPage
from pages import GroupListPage
from pages import MessagePage
from pages import SelectContactsPage
from pages import SelectOneGroupPage
from pages import WorkbenchPage
from pages.workbench.enterprise_contacts.EnterpriseContacts import EnterpriseContactsPage
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
    def enter_enterprise_contacts_page():
        """进入企业通讯录首页"""

        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_enterprise_contacts()
        ecp = EnterpriseContactsPage()
        ecp.wait_for_page_load()


class EnterpriseContactsAllTest(TestCase):

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
    def test_QYTXL_0001(self):
        """用户不在任何部门下直接进入企业子一层级"""

        # 进入企业通讯录首页
        Preconditions.enter_enterprise_contacts_page()
        ecp = EnterpriseContactsPage()
        # 1.直接进入企业子一层级
        self.assertEquals(ecp.is_exists_three_points_icon(), True)
        ecp.click_back_button()
        # 2.页面跳转到企业层级
        self.assertEquals(ecp.is_exists_three_points_icon(), False)
        self.assertEquals(ecp.is_exist_department_icon(), True)
        ecp.click_back_button()
        # 等待工作台首页加载
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYTXL_0002(self):
        """用户在企业部门下直接进入企业层级"""

        wbp = WorkbenchPage()
        # 添加本机号码到指定部门
        department_name = "admin_department"
        Preconditions.add_phone_number_to_department(department_name)
        workbench_name = wbp.get_workbench_name()
        ecp = EnterpriseContactsPage()
        wbp.click_company_contacts()
        ecp.wait_for_page_load()
        # 1.跳转后直接进入企业层级：企业+部门名称
        self.assertEquals(ecp.is_exists_three_points_icon(), False)
        self.assertEquals(ecp.is_exists_accessibility_id_attribute_by_name(workbench_name), True)
        self.assertEquals(ecp.is_exists_accessibility_id_attribute_by_name(department_name), True)
        ecp.click_back_button()
        wbp.wait_for_page_load()

    @staticmethod
    def tearDown_test_QYTXL_0002():
        """恢复环境"""

        try:
            fail_time = 0
            while fail_time < 5:
                try:
                    Preconditions.make_already_in_message_page()
                    mp = MessagePage()
                    mp.open_workbench_page()
                    Preconditions.delete_department_by_name("admin_department")
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

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
        ecp = EnterpriseContactsPage()
        wbp.click_company_contacts()
        ecp.wait_for_page_load()
        # 1.跳转后直接进入企业层级：企业+部门名称
        self.assertEquals(ecp.is_exists_three_points_icon(), False)
        self.assertEquals(ecp.is_exists_accessibility_id_attribute_by_name(workbench_name), True)
        self.assertEquals(ecp.is_exists_accessibility_id_attribute_by_name(department_name), True)
        ecp.click_back_button()
        wbp.wait_for_page_load()

    @staticmethod
    def tearDown_test_QYTXL_0003():
        """恢复环境"""

        try:
            fail_time = 0
            while fail_time < 5:
                try:
                    Preconditions.make_already_in_message_page()
                    mp = MessagePage()
                    mp.open_workbench_page()
                    Preconditions.delete_department_by_name("admin_department")
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

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
        ecp = EnterpriseContactsPage()
        wbp.click_company_contacts()
        ecp.wait_for_page_load()
        # 1.跳转后显示企业层级：企业+部门名称（部门随机显示一个）
        self.assertEquals(ecp.is_exists_three_points_icon(), False)
        self.assertEquals(ecp.is_exists_accessibility_id_attribute_by_name(workbench_name), True)
        self.assertEquals((ecp.is_exists_accessibility_id_attribute_by_name(department_name1) or ecp.is_exists_accessibility_id_attribute_by_name(department_name2)), True)
        ecp.click_back_button()
        wbp.wait_for_page_load()

    @staticmethod
    def tearDown_test_QYTXL_0004():
        """恢复环境"""

        try:
            fail_time = 0
            while fail_time < 5:
                try:
                    Preconditions.make_already_in_message_page()
                    mp = MessagePage()
                    mp.open_workbench_page()
                    Preconditions.delete_department_by_name("admin_department1")
                    Preconditions.delete_department_by_name("admin_department2")
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYTXL_0008(self):
        """验证点击返回按钮是否正确"""

        # 进入企业通讯录首页
        Preconditions.enter_enterprise_contacts_page()
        ecp = EnterpriseContactsPage()
        # 点击【<】返回
        ecp.click_back_button(2)
        # 1.返回上一级页面（返回到工作台）
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYTXL_0009(self):
        """精确搜索（数字、中文、英文）"""

        # 进入企业通讯录首页
        Preconditions.enter_enterprise_contacts_page()
        ecp = EnterpriseContactsPage()
        # 点击搜索框
        ecp.click_search_box()
        search_name = "陈丹丹"
        # 点击搜索输入文字陈丹丹（已存）
        ecp.input_search_message(search_name)
        # 1.自动匹配陈丹丹搜索结果，且陈丹丹高亮(间接验证)
        self.assertEquals(ecp.is_search_contacts_name_full_match(search_name), True)
        ecp.click_back_button()
        ecp.click_search_box()
        search_name2 = "alice"
        # 点击搜索输入英文全称alice（已存）
        ecp.input_search_message(search_name2)
        # 2.自动匹配alice搜索结果，alice高亮显示(间接验证)
        self.assertEquals(ecp.is_search_contacts_name_full_match(search_name2), True)
        ecp.click_back_button()
        ecp.click_search_box()
        search_number = "13802883296"
        # 点击搜索输入13802883296（已存）
        ecp.input_search_message(search_number)
        # 3.自动匹配精准搜素结果，13802883296高亮显示(间接验证)
        self.assertEquals(ecp.is_search_contacts_number_full_match(search_number), True)
        ecp.click_back_button(3)
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYTXL_0010(self):
        """模糊搜索（数字、中文、英文）"""

        # 进入企业通讯录首页
        Preconditions.enter_enterprise_contacts_page()
        ecp = EnterpriseContactsPage()
        # 点击搜索框
        ecp.click_search_box()
        search_name = "陈"
        # 点击搜索输入文字陈（已存）
        ecp.input_search_message(search_name)
        # 1.自动匹配输入结果陈字标黄，排序结果企业通讯录排列结果一致(间接验证)
        self.assertEquals(ecp.is_search_contacts_name_match(search_name), True)
        ecp.click_back_button()
        ecp.click_search_box()
        search_name2 = "zh"
        # 点击搜索输入全昵称首字母zh（已存）
        ecp.input_search_message(search_name2)
        # 2.自动匹配输入结果，昵称标黄，排序结果企业通讯录排列结果一致(间接验证)
        self.assertEquals(ecp.is_search_contacts_name_match("郑海"), True)
        ecp.click_back_button()
        ecp.click_search_box()
        search_number = "138028"
        # 点击搜索输入138028（已存）
        ecp.input_search_message(search_number)
        # 3.自动匹配输入结果，手机号码标黄排序结果企业通讯录排列结果一致(间接验证)
        self.assertEquals(ecp.is_search_contacts_number_match(search_number), True)
        ecp.click_back_button(3)
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYTXL_0012(self):
        """搜索企业通讯录联系人结果展示"""

        # 进入企业通讯录首页
        Preconditions.enter_enterprise_contacts_page()
        ecp = EnterpriseContactsPage()
        # 点击搜索框
        ecp.click_search_box()
        search_name = "大佬1"
        # 搜索联系人xxx
        ecp.input_search_message(search_name)
        time.sleep(2)
        # 1.展示搜索结果，显示头像、姓名、号码、公司部门（没公司部门的不显示）
        self.assertEquals(ecp.is_exists_contacts_image(), True)
        self.assertEquals(ecp.is_exists_contacts_name(), True)
        self.assertEquals(ecp.is_exists_contacts_number(), True)
        self.assertEquals(ecp.is_exists_contacts_department(), True)
        ecp.click_back_button(3)
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYTXL_0013(self):
        """点击搜索结果已保存到本地的RCS用户进入联系人详情页"""

        # 进入企业通讯录首页
        Preconditions.enter_enterprise_contacts_page()
        ecp = EnterpriseContactsPage()
        # 点击搜索框
        ecp.click_search_box()
        search_name = "大佬1"
        # 点击搜索框输入关键字
        ecp.input_search_message(search_name)
        # 点击搜索结果已保存到本地的RCS用户
        ecp.click_name_attribute_by_name(search_name, "xpath")
        cdp = ContactDetailsPage()
        # 1.页面跳转到该用户的Profile页，显示用户的详情：姓名、号码、头像、公司、职位(有值时显示)、邮箱(有值时显示)，
        # 中部显示消息、电话、语音通话、视频通话、副号拨打(有副号且开机时显示)、和飞信电话，底部只提供分享名片按钮
        # (间接验证)(副号拨打无法验证，需要提供满足条件的测试号码）
        cdp.wait_for_page_load()
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
        cdp.click_back_button(4)
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYTXL_0015(self):
        """点击搜索结果已保存到本地的本机用户进入联系人详情页"""

        # 进入企业通讯录首页
        Preconditions.enter_enterprise_contacts_page()
        ecp = EnterpriseContactsPage()
        # 点击搜索框
        ecp.click_search_box()
        search_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # 点击搜索框输入关键字
        ecp.input_search_message(search_number)
        # 点击搜索结果已保存到本地的本机用户
        ecp.click_name_attribute_by_name(search_number, "xpath")
        cdp = ContactDetailsPage()
        # 1.页面跳转到该用户的Profile页，显示用户的详情：姓名、号码、头像、公司、职位(有值时显示)、邮箱(有值时显示)，
        # 中部显示消息、电话、语音通话、视频通话、副号拨打(有副号且开机时显示)、和飞信电话，底部提供分享名片按钮
        # (间接验证)(副号拨打无法验证，需要提供满足条件的测试号码)
        cdp.wait_for_page_load()
        # 确保本机用户已保存到本地
        if cdp.is_exists_save_contacts_icon():
            cdp.click_save_contacts_icon()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            ccp.save_contact()
            time.sleep(2)
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
        # 2.点击分享名片进入选择联系人页面，可以成功的分享给人/群
        cdp.click_share_card_icon()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        name = "群聊1"
        # 分享名片到一个普通群
        sog.selecting_one_group_by_name(name)
        sog.click_accessibility_id_attribute_by_name("发送名片")
        # self.assertEquals(sog.page_should_contain_text2("分享成功"), True)
        time.sleep(2)
        # 3.消息、电话、语音视频、视频电话、副号拨打(需要提供满足条件的测试号码)、和飞信电话置灰，不可点击(间接验证)
        self.assertEquals(cdp.message_icon_is_enabled(), False)
        self.assertEquals(cdp.call_icon_is_enabled(), False)
        self.assertEquals(cdp.voice_call_icon_is_enabled(), False)
        self.assertEquals(cdp.video_call_icon_is_enabled(), False)
        # self.assertEquals(cdp.dial_hefeixin_icon_is_enabled(), False)
        # 和飞信电话不可点击使用间接验证
        cdp.click_hefeixin_call_menu()
        time.sleep(2)
        cdp.wait_for_page_load()
        cdp.click_back_button(4)
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        # 返回消息页面验证名片是否分享成功
        wbp.open_message_page()
        mp = MessagePage()
        mp.wait_for_page_load()
        mp.choose_chat_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        self.assertEquals(gcp.page_should_contain_text2("个人名片"), True)
        gcp.click_back_button()
        mp.wait_for_page_load()
        mp.open_workbench_page()
        # 返回工作台
        wbp.wait_for_page_load()

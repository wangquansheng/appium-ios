import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import ContactsPage
from pages import GroupListPage
from pages import MessagePage
from pages import SelectLocalContactsPage
from pages.workbench.Workbench import WorkbenchPage
from pages.workbench.group_messenger.SelectCompanyContacts import SelectCompanyContactsPage
from pages.workbench.manager_console.EnterpriseInterests import EnterpriseInterestsPage
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
    def enter_voice_notice_page():
        """进入语音通知首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_voice_notice()


class VoiceNoticeAllTest(TestCase):

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
        2、当前页面在语音通知首页
        """

        Preconditions.select_mobile('IOS-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_voice_notice_page()
            return
        vnp = VoiceNotifyPage()
        if not vnp.is_on_voice_notify_page():
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_voice_notice_page()

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0001(self):
        """网络正常情况下正常跳转到应用首页"""

        vnp = VoiceNotifyPage()
        # 1.可正常跳转到语音通知首页
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0003(self):
        """剩余条数显示正确"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        # 查看本月剩余通知条数
        number = vnp.get_remaining_notice()
        # 发送一条语音通知，选择1个成员
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        vnp.input_notice_content("你好啊")
        # 收起键盘
        vnp.click_name_attribute_by_name("完成")
        # 点击通知接收人+号
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        sccp.click_contacts_by_name("大佬1")
        sccp.click_sure_button()
        vnp.wait_for_create_voice_notify_page_load()
        vnp.click_send()
        vnp.wait_for_page_load()
        # 查看本月剩余通知条数权益是否正常减去已发送的数量
        new_number = vnp.get_remaining_notice()
        # 剩余条数正常减1
        self.assertEquals(number - 1, new_number)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0004(self):
        """正常查看使用该指引"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        # 点击右上角【？】
        vnp.click_help_icon()
        # 1.可正常跳转到语音通知使用指引页面
        self.assertEquals(vnp.page_should_contain_text2("语音通知使用指引"), True)
        # 上下滑动浏览页面
        vnp.page_up()
        # 2.上下滑动可正常浏览页面
        self.assertEquals(vnp.page_should_contain_text2("创建语音通知"), True)
        vnp.page_down()
        self.assertEquals(vnp.page_should_contain_text2("发起语音通知"), True)
        vnp.click_back_button()
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0005(self):
        """正常展开收起权益"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        # 解决坐标定位错误问题
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        vnp.click_back_button()
        vnp.wait_for_page_load()
        # 点击本月剩余通知条数旁边的下三角
        vnp.click_down_triangle()
        # 1.可正常展开和收起权益展示
        self.assertEquals(vnp.page_should_contain_text2("企业认证"), True)
        # 点击展开页面的上三角
        vnp.click_up_triangle()
        self.assertEquals(vnp.page_should_contain_text2("企业认证", 3), False)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0006(self):
        """跳转企业认证"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        # 解决坐标定位错误问题
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        vnp.click_back_button()
        vnp.wait_for_page_load()
        # 点击本月剩余通知条数旁边的下三角
        vnp.click_down_triangle()
        # 点击“企业认证”
        vnp.click_accessibility_id_attribute_by_name("企业认证")
        # 1.可正常跳转到企业认证详情页
        self.assertEquals(vnp.page_should_contain_text2("马上去认证"), True)
        # 点击“马上去认证”
        vnp.click_accessibility_id_attribute_by_name("马上去认证")
        # 2.弹出“如何申请认证”引导页面
        self.assertEquals(vnp.page_should_contain_text2("如何申请认证"), True)
        # 点击复制地址
        vnp.click_accessibility_id_attribute_by_name("复制地址")
        # 3.可复制地址
        self.assertEquals(vnp.page_should_contain_text2("复制成功"), True)
        time.sleep(3)
        vnp.click_accessibility_id_attribute_by_name("马上去认证")
        # 点击【x】
        vnp.click_popup_close_icon()
        # 4.可关闭弹窗
        self.assertEquals(vnp.page_should_contain_text2("如何申请认证", 3), False)
        vnp.click_back_button()
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0007(self):
        """可正常跳转到充值页面"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        # 解决坐标定位错误问题
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        vnp.click_back_button()
        vnp.wait_for_page_load()
        # 点击本月剩余通知条数旁边的下三角
        vnp.click_down_triangle()
        # 点击“充值”
        vnp.click_recharge()
        eip = EnterpriseInterestsPage()
        # 1.可正常跳转到充值页面
        eip.wait_for_service_page_load()
        vnp.click_back_button()
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0008(self):
        """添加搜索出的成员"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击“+”
        vnp.click_add_icon()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        search_name = "大佬1"
        # 搜索关键词
        slcp.input_search_keyword(search_name)
        # 1.可正常选择搜索出的成员
        self.assertEquals(slcp.is_exists_local_contacts_by_name(search_name), True)
        # 点击搜索结果中的成员
        slcp.selecting_local_contacts_by_name(search_name)
        # 点击“确定”
        slcp.click_sure()
        vnp.wait_for_create_voice_notify_page_load()
        # 2.成员列表显示已勾选成员信息
        self.assertEquals(vnp.page_should_contain_text2(search_name), True)
        vnp.click_back_button()
        vnp.click_accessibility_id_attribute_by_name("否")
        vnp.wait_for_page_load()

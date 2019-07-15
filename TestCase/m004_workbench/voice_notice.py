import time

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
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

        # 导入团队联系人、vip用户、企业部门
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
                vip_names = [("测试vip用户", "13566668888")]
                Preconditions.create_vip_contacts(vip_names)
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
        # 解决坐标定位错误问题
        vnp.click_back_button()
        vnp.wait_for_page_load()
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
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 解决坐标定位错误问题
        vnp.click_back_button()
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

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0009(self):
        """多个部门成员累加"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # # 解决坐标定位错误问题
        # vnp.click_back_button()
        # vnp.wait_for_page_load()
        # vnp.click_create_voice_notify()
        # vnp.wait_for_create_voice_notify_page_load()
        # 点击“+”
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        # 进入多个部门勾选成员
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_accessibility_id_attribute_by_name("测试部门2")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        # 1.可正常在多个部门切换选择成员
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        # 2.多个部门已选择的成员可累加
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        # 点击“确定”
        sccp.click_sure_button()
        vnp.wait_for_create_voice_notify_page_load()
        self.assertEquals(sccp.is_exists_accessibility_id_attribute_by_name("大佬1"), True)
        self.assertEquals(sccp.is_exists_accessibility_id_attribute_by_name("大佬2"), True)
        vnp.click_back_button()
        vnp.click_accessibility_id_attribute_by_name("否")
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0010(self):
        """移除成员"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 解决坐标定位错误问题
        vnp.click_back_button()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击“+”
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        # 选择多个成员
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        sccp.click_accessibility_id_attribute_by_name("大佬3")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬3"), True)
        # 部门下已选择成员，再次点击图像取消勾选
        sccp.click_contacts_image_by_name("大佬1")
        # 在顶部栏已选择成员信息点击成员图像移除成员
        sccp.click_contacts_image_by_name("佬2")
        # 点击“确定”
        sccp.click_sure_button()
        vnp.wait_for_create_voice_notify_page_load()
        # 1.两种方式都可以成功删除成员
        self.assertEquals(vnp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(vnp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(vnp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        vnp.click_back_button()
        vnp.click_accessibility_id_attribute_by_name("否")
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0011(self):
        """移除成员再添加成员"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 解决坐标定位错误问题
        vnp.click_back_button()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击“+”
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        # 选择多个成员
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        sccp.click_accessibility_id_attribute_by_name("大佬3")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬3"), True)
        # 部门下已选择成员，再次点击图像取消勾选
        sccp.click_contacts_image_by_name("大佬1")
        # 在顶部栏已选择成员信息点击成员图像移除成员
        sccp.click_contacts_image_by_name("佬2")
        # 再添加其他成员
        sccp.click_accessibility_id_attribute_by_name("大佬4")
        # 点击“确定”
        sccp.click_sure_button()
        vnp.wait_for_create_voice_notify_page_load()
        # 1.移除成员之后还可继续添加其他成员
        self.assertEquals(vnp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(vnp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(vnp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        self.assertEquals(vnp.is_exists_accessibility_id_attribute_by_name("大佬4"), True)
        vnp.click_back_button()
        vnp.click_accessibility_id_attribute_by_name("否")
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0012(self):
        """无号码或自己等于100，成员等于20的时候成员不可勾选"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 解决坐标定位错误问题
        vnp.click_back_button()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击“+”
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        # 选择无号码或自己等级 = 100时，成员等级等于20的用户
        sccp.click_accessibility_id_attribute_by_name("测试vip用户")
        # 1.不可勾选，提示“该联系人不可选”(间接验证)
        # self.assertEquals(sccp.page_should_contain_text2("该联系人不可选择"), True)
        # 点击“确定”
        sccp.click_sure_button()
        time.sleep(1)
        sccp.wait_for_page_load()
        vnp.click_back_button(4)
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0014(self):
        """语音时长小于1s"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        # 点击“创建语音通知”
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击话筒icon录制语音
        vnp.click_microphone_icon()
        # 按住话筒录制小于1s语音就松手
        vnp.click_microphone_button()
        # 1.toast提示“录音时间太短，请重试”
        self.assertEquals(vnp.page_should_contain_text2("录音时间太短，请重试"), True)
        vnp.click_back_button(2)
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0015(self):
        """录制语音时长为59s"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        # 点击“创建语音通知”
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击话筒icon录制语音
        vnp.click_microphone_icon()
        # 按住话筒录制59s语音就松手(由于按住有延迟，需要多按压一秒)
        vnp.press_microphone_button(60)
        # 1.录制成功，内容栏中显示已录制的语音，并显示时长，旁边有删除按钮
        self.assertEquals(vnp.is_exists_element_by_text("录制语音"), True)
        self.assertEquals(vnp.get_voice_duration(), "59")
        self.assertEquals(vnp.is_exists_element_by_text("录制语音删除按钮"), True)
        vnp.click_back_button()
        vnp.click_accessibility_id_attribute_by_name("否")
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0016(self):
        """录制语音时长为60s"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        # 点击“创建语音通知”
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击话筒icon录制语音
        vnp.click_microphone_icon()
        # 按住话筒录制为60s语音就松手(由于按住有延迟，需要多按压一秒)
        vnp.press_microphone_button(61)
        # 1.录制成功，内容栏中显示已录制的语音，并显示时长，旁边有删除按钮
        self.assertEquals(vnp.is_exists_element_by_text("录制语音"), True)
        self.assertEquals(vnp.get_voice_duration(), "60")
        self.assertEquals(vnp.is_exists_element_by_text("录制语音删除按钮"), True)
        vnp.click_back_button()
        vnp.click_accessibility_id_attribute_by_name("否")
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0017(self):
        """录制语音时长大于60s"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        # 点击“创建语音通知”
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击话筒icon录制语音
        vnp.click_microphone_icon()
        # 按住话筒录制大于60s语音就松手
        vnp.press_microphone_button(65)
        # 1.录制成功，时长大于60s后自动停止录制，内容栏中显示已录制的语音，显示时长，旁边有删除按钮
        self.assertEquals(vnp.is_exists_element_by_text("话筒录制按钮"), False)
        self.assertEquals(vnp.is_exists_element_by_text("录制语音"), True)
        self.assertEquals(vnp.get_voice_duration(), "60")
        self.assertEquals(vnp.is_exists_element_by_text("录制语音删除按钮"), True)
        vnp.click_back_button()
        vnp.click_accessibility_id_attribute_by_name("否")
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0019(self):
        """录制时滑动到删除按钮删除语音"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        # 点击“创建语音通知”
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击话筒icon录制语音
        vnp.click_microphone_icon()
        time.sleep(2)
        # 按住话筒说话时往删除键方向滑动
        vnp.press_slide_microphone_button()
        # 1.录制内容被删除，页面停留在当前页面
        self.assertEquals(vnp.page_should_contain_text2("按住说话"), True)
        self.assertEquals(vnp.is_exists_element_by_text("话筒录制按钮"), True)
        vnp.click_back_button(2)
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0020(self):
        """录制后点击录音后边的删除按钮"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        # 点击“创建语音通知”
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击话筒icon录制语音
        vnp.click_microphone_icon()
        # 录制语音
        vnp.press_microphone_button(5)
        self.assertEquals(vnp.is_exists_element_by_text("录制语音时长"), True)
        # 录制成功之后，点击录音后边的删除按钮
        vnp.click_voice_delete_button()
        # 1.录制内容被删除，页面停留在当前页面
        self.assertEquals(vnp.is_exists_element_by_text("录制语音时长"), False)
        vnp.wait_for_create_voice_notify_page_load()
        vnp.click_back_button()
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0021(self):
        """录制后点击小键盘，切换到输入模式"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        # 点击“创建语音通知”
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击话筒icon录制语音
        vnp.click_microphone_icon()
        # 录制语音
        vnp.press_microphone_button(5)
        # 录制成功之后，点击录音右下角的小键盘icon
        vnp.click_keyboard_icon()
        # 1.切换到输入模式
        self.assertEquals(vnp.page_should_contain_text2("请输入通知内容"), True)
        vnp.click_back_button()
        vnp.click_accessibility_id_attribute_by_name("否")
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0025(self):
        """删除发送成功的语音通知"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        # 清空语音通知，确保不影响验证
        vnp.clear_voice_notice()
        # 发送一条语音通知
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 解决坐标定位错误问题
        vnp.click_back_button()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        vnp.click_microphone_icon()
        # 录制语音
        vnp.press_microphone_button(5)
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        sccp.click_contacts_by_name("大佬1")
        sccp.click_sure_button()
        vnp.wait_for_create_voice_notify_page_load()
        vnp.click_send()
        vnp.wait_for_page_load()
        # 点击一条发送成功的语音通知
        vnp.click_element_by_text("语音通知列表")
        # 点击“更多”-“删除”
        vnp.click_accessibility_id_attribute_by_name("更多")
        vnp.click_accessibility_id_attribute_by_name("删除")
        # 点击“确定”
        vnp.click_accessibility_id_attribute_by_name("确定")
        vnp.wait_for_page_load()
        # 1.删除成功，我创建的列表中被删除的通知信息被移除(由于没有可辨识元素，间接验证)
        self.assertEquals(vnp.page_should_contain_text2("发送成功", 3), False)
        self.assertEquals(vnp.page_should_contain_text2("审核中", 3), False)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0029(self):
        """用户不在任何部门下"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 解决坐标定位错误问题
        vnp.click_back_button()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击“+”添加联系人
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
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
        sccp.click_back_button(3)
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0030(self):
        """用户在企业部门下"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        # 确保用户在企业部门下
        vnp.click_back_button()
        wbp = WorkbenchPage()
        # 添加本机号码到指定部门
        department_name = "admin_department"
        Preconditions.add_phone_number_to_department(department_name)
        workbench_name = wbp.get_workbench_name()
        wbp.click_voice_notice()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 解决坐标定位错误问题
        vnp.click_back_button()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击“+”添加联系人
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        # 等待选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.跳转后直接进入企业层级：企业+部门名称
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exists_accessibility_id_attribute_by_name(workbench_name), True)
        self.assertEquals(sccp.is_exists_accessibility_id_attribute_by_name(department_name), True)
        sccp.click_back_button(3)
        vnp.wait_for_page_load()

    @staticmethod
    def tearDown_test_YYTZ_0030():
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
                    wbp.click_voice_notice()
                    vnp = VoiceNotifyPage()
                    vnp.wait_for_page_load()
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0031(self):
        """用户在企业部门下又在企业子一层级中，直接进入企业层级"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        # 确保用户既在企业部门下又在企业子一层级
        vnp.click_back_button()
        wbp = WorkbenchPage()
        # 添加本机号码到指定部门
        department_name = "admin_department"
        Preconditions.add_phone_number_to_department(department_name)
        # 添加本机号码到和通讯录
        Preconditions.add_phone_number_to_he_contacts()
        workbench_name = wbp.get_workbench_name()
        wbp.click_voice_notice()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 解决坐标定位错误问题
        vnp.click_back_button()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击“+”添加联系人
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        # 等待选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.跳转后直接进入企业层级：企业+部门名称
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exists_accessibility_id_attribute_by_name(workbench_name), True)
        self.assertEquals(sccp.is_exists_accessibility_id_attribute_by_name(department_name), True)
        sccp.click_back_button(3)
        vnp.wait_for_page_load()

    @staticmethod
    def tearDown_test_YYTZ_0031():
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
                    wbp.click_voice_notice()
                    vnp = VoiceNotifyPage()
                    vnp.wait_for_page_load()
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0032(self):
        """用户同时在两个部门下"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        # 确保用户在企业部门下
        vnp.click_back_button()
        wbp = WorkbenchPage()
        # 添加本机号码到指定部门1
        department_name1 = "admin_department1"
        Preconditions.add_phone_number_to_department(department_name1)
        # 添加本机号码到指定部门2
        department_name2 = "admin_department2"
        Preconditions.add_phone_number_to_department(department_name2)
        workbench_name = wbp.get_workbench_name()
        wbp.click_voice_notice()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 解决坐标定位错误问题
        vnp.click_back_button()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击“+”添加联系人
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        # 等待选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.跳转后显示企业层级：企业+部门名称（部门随机显示一个）
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exists_accessibility_id_attribute_by_name(workbench_name), True)
        self.assertEquals((sccp.is_exists_accessibility_id_attribute_by_name(
            department_name1) or sccp.is_exists_accessibility_id_attribute_by_name(department_name2)), True)
        sccp.click_back_button(3)
        vnp.wait_for_page_load()

    @staticmethod
    def tearDown_test_YYTZ_0032():
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
                    wbp.click_voice_notice()
                    vnp = VoiceNotifyPage()
                    vnp.wait_for_page_load()
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0033(self):
        """选择用户本人"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 解决坐标定位错误问题
        vnp.click_back_button()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击“+”
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        # 点击用户本人头像
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        sccp.click_contacts_image_by_name(phone_number)
        # 1.页面toast提示“该联系人不可选择
        self.assertEquals(sccp.page_should_contain_text2("该联系人不可选择"), True)
        vnp.click_back_button(4)
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0034(self):
        """选择无号码用户"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 解决坐标定位错误问题
        vnp.click_back_button()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击“+”
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        # 点击无号码的用户头像
        sccp.click_contacts_image_by_name("测试vip用户")
        # 1.页面toast提示“该联系人不可选择(间接验证)
        # self.assertEquals(sccp.page_should_contain_text2("该联系人不可选择"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), False)
        vnp.click_back_button(4)
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0035(self):
        """搜索不存在的用户昵称"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 解决坐标定位错误问题
        vnp.click_back_button()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击“+”
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        # 等待选择联系人页面加载
        sccp.wait_for_page_load()
        # 搜索不存在的用户名称
        sccp.input_search_message("不存在")
        sccp.page_down()
        # 1.提示“无搜索结果”
        self.assertEquals(sccp.page_should_contain_text2("无搜索结果"), True)
        vnp.click_back_button(4)
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0036(self):
        """搜索“我的电脑”"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 解决坐标定位错误问题
        vnp.click_back_button()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击“+”
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        # 等待选择联系人页面加载
        sccp.wait_for_page_load()
        # 搜索“我的电脑”
        sccp.input_search_message("我的电脑")
        sccp.page_down()
        # 1.无搜索结果
        self.assertEquals(sccp.page_should_contain_text2("无搜索结果"), True)
        vnp.click_back_button(4)
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0037(self):
        """11位号码精准搜索"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 解决坐标定位错误问题
        vnp.click_back_button()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击“+”
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        # 等待选择联系人页面加载
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
        vnp.click_back_button(4)
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0038(self):
        """6-10位数字可支持模糊搜索匹配结果"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 解决坐标定位错误问题
        vnp.click_back_button()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击“+”
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        # 等待选择联系人页面加载
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
        vnp.click_back_button(4)
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0039(self):
        """联系人姓名（全名）精准搜索"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 解决坐标定位错误问题
        vnp.click_back_button()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击“+”
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        # 等待选择联系人页面加载
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
        vnp.click_back_button(4)
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0040(self):
        """联系人姓名（非全名）模糊搜索"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 解决坐标定位错误问题
        vnp.click_back_button()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击“+”
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        # 等待选择联系人页面加载
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
        vnp.click_back_button(4)
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0046(self):
        """空格键+文本 可支持匹配"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 解决坐标定位错误问题
        vnp.click_back_button()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击“+”
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        # 等待选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = " 马上"
        # 在搜索框输入 空格键+文本,查看匹配结果
        sccp.input_search_message(search_name)
        # 1.匹配出对应包含 空格键+文本的的联系人，文本关键词高亮，按第一个汉字的字顺序排序显示(间接验证)
        self.assertEquals(sccp.is_search_contacts_name_match(search_name), True)
        # 点击结果，查看是否可选择成功
        sccp.click_name_attribute_by_name(search_name, "xpath")
        # 2.搜索栏清空，搜索栏左侧出现已选人名和头像，右上角展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("马上"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image("马上"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        vnp.click_back_button(4)
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0050(self):
        """字母+汉字组合可精准搜索"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 解决坐标定位错误问题
        vnp.click_back_button()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击“+”
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        # 等待选择联系人页面加载
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
        vnp.click_back_button(4)
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0051(self):
        """字母+汉字+数字 组合可精准搜索"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 解决坐标定位错误问题
        vnp.click_back_button()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        vnp.wait_for_create_voice_notify_page_load()
        # 点击“+”
        vnp.click_add_icon()
        vnp.click_accessibility_id_attribute_by_name("企业通讯录")
        sccp = SelectCompanyContactsPage()
        # 等待选择联系人页面加载
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
        vnp.click_back_button(4)
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0063(self):
        """点击顶部返回键"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 在任意页面点击顶部【<】
        vnp.click_back_button()
        # 1.返回到上一级页面
        vnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0064(self):
        """点击顶部关闭按钮"""

        vnp = VoiceNotifyPage()
        vnp.wait_for_page_load()
        vnp.click_create_voice_notify()
        # 等待创建语音通知页面加载
        vnp.wait_for_create_voice_notify_page_load()
        # 在其他有关闭按钮页面，点击顶部【x】
        vnp.click_close()
        wbp = WorkbenchPage()
        # 1.关闭语音通知，返回到工作台页面
        wbp.wait_for_page_load()
        wbp.click_voice_notice()
        vnp.wait_for_page_load()
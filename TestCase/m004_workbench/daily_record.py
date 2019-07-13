import time

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile
from pages import ContactsPage
from pages import GroupListPage
from pages import MessagePage
from pages import WorkbenchPage
from pages.workbench.daily_record.DailyRecord import DailyRecordPage
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
    def enter_daily_record_page():
        """进入日志首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_daily_record()

    @staticmethod
    def create_new_log():
        """创建新日志"""

        drp = DailyRecordPage()
        drp.click_journals()
        drp.click_daily_paper()
        drp.wait_log_editor_page_load()
        # 输入日志标题、今日工作总结、明日工作计划、需要协调与帮助、备注等信息
        drp.input_title("测试日志")
        # 收起键盘
        drp.click_name_attribute_by_name("完成")
        drp.input_work_summary("测试工作总结")
        drp.input_work_plan("测试工作计划")
        drp.input_coordinate_and_help("测试协调与帮助")
        drp.input_remarks("测试备注")
        # 收起键盘
        drp.click_name_attribute_by_name("完成")
        # 接收人：点击“+”按钮
        drp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        # 点击相关提交人
        sccp.click_contacts_by_name("大佬1")
        sccp.click_sure_button()
        # 点击【提交】
        drp.click_submit()
        drp.wait_log_overview_page_load()
        drp.click_back_button(2)
        # 等待日志首页加载
        drp.wait_for_page_load()

    @staticmethod
    def create_draft_log():
        """创建草稿日报"""

        drp = DailyRecordPage()
        drp.click_journals()
        drp.click_daily_paper()
        drp.wait_log_editor_page_load()
        # 输入日志标题、今日工作总结、明日工作计划、需要协调与帮助、备注等信息
        drp.input_title("测试草稿日志")
        # 收起键盘
        drp.click_name_attribute_by_name("完成")
        drp.input_work_summary("测试草稿工作总结")
        drp.input_work_plan("测试草稿工作计划")
        drp.input_coordinate_and_help("测试草稿协调与帮助")
        drp.input_remarks("测试草稿备注")
        # 收起键盘
        drp.click_name_attribute_by_name("完成")
        # 接收人：点击“+”按钮
        drp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        # 点击相关提交人
        sccp.click_contacts_by_name("大佬1")
        sccp.click_sure_button()
        # 点击【存草稿】
        drp.click_save_draft()
        # 等待日志首页加载
        drp.wait_for_page_load()


class DailyRecordAllTest(TestCase):

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

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在日志首页
        """

        Preconditions.select_mobile('IOS-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_daily_record_page()
            return
        drp = DailyRecordPage()
        if not drp.is_on_daily_record_page():
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_daily_record_page()

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_RZ_0001(self):
        """验证点击返回按钮是否正确"""

        drp = DailyRecordPage()
        drp.wait_for_page_load()
        # 点击【<】返回
        drp.click_back_button()
        wbp = WorkbenchPage()
        # 1.返回到工作台
        wbp.wait_for_page_load()
        wbp.click_journal()
        # 等待日志首页加载
        drp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_RZ_0002(self):
        """新建日志"""

        drp = DailyRecordPage()
        drp.wait_for_page_load()
        # 点击【写日志】
        drp.click_journals()
        # 1.进入日志类型选择界面
        self.assertEquals(drp.page_should_contain_text2("日志类型"), True)
        # 选择【日报】
        drp.click_daily_paper()
        # 2.进入日报编辑界面
        drp.wait_log_editor_page_load()
        # 输入日志标题、今日工作总结、明日工作计划、需要协调与帮助、备注等信息
        drp.input_title("测试日志0002")
        # 收起键盘
        drp.click_name_attribute_by_name("完成")
        drp.input_work_summary("测试工作总结0002")
        drp.input_work_plan("测试工作计划0002")
        drp.input_coordinate_and_help("测试协调与帮助0002")
        drp.input_remarks("测试备注0002")
        # 收起键盘
        drp.click_name_attribute_by_name("完成")
        # 接收人：点击“+”按钮
        drp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 3.弹出选择联系人界面
        sccp.wait_for_page_load()
        # 在搜索框输入提交人信息
        search_name = "大佬1"
        sccp.input_search_message(search_name)
        # 4.自动搜索出相关的联系人
        self.assertEquals(sccp.is_search_contacts_name_full_match(search_name), True)
        # 点击相关提交人
        sccp.click_name_attribute_by_name(search_name, "xpath")
        # 点击【确定】
        sccp.click_sure_button()
        time.sleep(1)
        # 5.界面显示添加的提交人
        self.assertEquals(drp.page_should_contain_text2(search_name), True)
        # 点击【提交】
        drp.click_submit()
        # 6.日志提交成功，显示当前日报提交概览界面
        self.assertEquals(drp.page_should_contain_text2("提交成功"), True)
        drp.wait_log_overview_page_load()
        drp.click_back_button(2)
        # 等待日志首页加载
        drp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_RZ_0003(self):
        """新建日志 -- 提交人使用上次提交人"""

        drp = DailyRecordPage()
        drp.wait_for_page_load()
        # 确保可以使用上次提交人按钮
        Preconditions.create_new_log()
        # 点击【写日志】
        drp.click_journals()
        # 1.进入日志类型选择界面
        self.assertEquals(drp.page_should_contain_text2("日志类型"), True)
        # 选择【日报】
        drp.click_daily_paper()
        # 2.进入日报编辑界面
        drp.wait_log_editor_page_load()
        # 输入日志标题、今日工作总结、明日工作计划、需要协调与帮助、备注等信息
        drp.input_title("测试日志0003")
        # 收起键盘
        drp.click_name_attribute_by_name("完成")
        drp.input_work_summary("测试工作总结0003")
        drp.input_work_plan("测试工作计划0003")
        drp.input_coordinate_and_help("测试协调与帮助0003")
        drp.input_remarks("测试备注0003")
        # 收起键盘
        drp.click_name_attribute_by_name("完成")
        # 接收人：点击右侧的添加上次联系人
        drp.click_add_last_contact()
        # 3.自动添加上次日报提交人信息
        self.assertEquals(drp.page_should_contain_text2("大佬1"), True)
        # 点击【提交】
        drp.click_submit()
        # 4.日志提交成功，显示当前日报提交概览界面
        self.assertEquals(drp.page_should_contain_text2("提交成功"), True)
        drp.wait_log_overview_page_load()
        drp.click_back_button(2)
        # 等待日志首页加载
        drp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_RZ_0004(self):
        """新建日志 -- 删除已选择的提交人"""

        drp = DailyRecordPage()
        drp.wait_for_page_load()
        # 点击【写日志】
        drp.click_journals()
        # 1.进入日志类型选择界面
        self.assertEquals(drp.page_should_contain_text2("日志类型"), True)
        # 选择【日报】
        drp.click_daily_paper()
        # 2.进入日报编辑界面
        drp.wait_log_editor_page_load()
        # 输入日志标题、今日工作总结、明日工作计划、需要协调与帮助、备注等信息
        drp.input_title("测试日志0004")
        # 收起键盘
        drp.click_name_attribute_by_name("完成")
        drp.input_work_summary("测试工作总结0004")
        drp.input_work_plan("测试工作计划0004")
        drp.input_coordinate_and_help("测试协调与帮助0004")
        drp.input_remarks("测试备注0004")
        # 收起键盘
        drp.click_name_attribute_by_name("完成")
        # 接收人：点击“+”按钮
        drp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 3.弹出选择联系人界面
        sccp.wait_for_page_load()
        search_name = "大佬1"
        # 在搜索框输入提交人信息
        sccp.input_search_message(search_name)
        # 4.自动搜索出相关的联系人
        self.assertEquals(sccp.is_search_contacts_name_full_match(search_name), True)
        # 点击相关提交人
        sccp.click_name_attribute_by_name(search_name, "xpath")
        # 点击【确定】
        sccp.click_sure_button()
        time.sleep(1)
        # 5.界面显示添加的提交人
        self.assertEquals(drp.page_should_contain_text2(search_name), True)
        # 点击联系人头像信息
        drp.click_accessibility_id_attribute_by_name(search_name)
        time.sleep(1)
        # 6.联系人删除
        self.assertEquals(drp.page_should_contain_text2(search_name, 3), False)
        # 重复步骤4 - 7，选择另一个联系人
        drp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        search_name2 = "大佬2"
        sccp.input_search_message(search_name2)
        sccp.click_name_attribute_by_name(search_name2, "xpath")
        sccp.click_sure_button()
        time.sleep(1)
        # 7.界面显示添加的提交人
        self.assertEquals(drp.page_should_contain_text2(search_name2), True)
        # 点击【提交】
        drp.click_submit()
        # 8.日志提交成功，显示当前日报提交概览界面
        self.assertEquals(drp.page_should_contain_text2("提交成功"), True)
        drp.wait_log_overview_page_load()
        drp.click_back_button(2)
        # 等待日志首页加载
        drp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_RZ_0005(self):
        """新建草稿日志"""

        drp = DailyRecordPage()
        drp.wait_for_page_load()
        # 确保可以使用上次提交人按钮
        Preconditions.create_new_log()
        # 点击【写日志】
        drp.click_journals()
        # 1.进入日志类型选择界面
        self.assertEquals(drp.page_should_contain_text2("日志类型"), True)
        # 选择【日报】
        drp.click_daily_paper()
        # 2.进入日报编辑界面
        drp.wait_log_editor_page_load()
        # 输入日志标题、今日工作总结、明日工作计划、需要协调与帮助、备注等信息
        drp.input_title("测试日志0005")
        # 收起键盘
        drp.click_name_attribute_by_name("完成")
        drp.input_work_summary("测试工作总结0005")
        drp.input_work_plan("测试工作计划0005")
        drp.input_coordinate_and_help("测试协调与帮助0005")
        drp.input_remarks("测试备注0005")
        # 收起键盘
        drp.click_name_attribute_by_name("完成")
        # 接收人：点击右侧的添加上次联系人
        drp.click_add_last_contact()
        # 3.自动添加上次日报提交人信息
        self.assertEquals(drp.page_should_contain_text2("大佬1"), True)
        # 点击【存草稿】
        drp.click_save_draft()
        # 4.日报存草稿成功，返回我发出的日志列表
        self.assertEquals(drp.page_should_contain_text2("草稿保存成功"), True)
        # 等待日志首页加载
        drp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_RZ_0006(self):
        """新建草稿日志 -- 修改并提交"""

        drp = DailyRecordPage()
        drp.wait_for_page_load()
        # 确保有草稿日报可修改
        Preconditions.create_draft_log()
        # 点击相关的草稿日报记录
        drp.click_accessibility_id_attribute_by_name("测试草稿日志")
        # 1.进入日报编辑界面
        drp.wait_log_editor_page_load()
        # 更改日志标题、今日工作总结、明日工作计划、需要协调与帮助、备注等相关信息
        drp.input_title("修改的测试日志0006")
        # 收起键盘
        drp.click_name_attribute_by_name("完成")
        drp.input_work_summary("修改的测试工作总结0006")
        drp.input_work_plan("修改的测试工作计划0006")
        drp.input_coordinate_and_help("修改的测试协调与帮助0006")
        drp.input_remarks("修改的测试备注0006")
        # 收起键盘
        drp.click_name_attribute_by_name("完成")
        # 接收人：点击右侧的添加上次联系人
        drp.click_add_last_contact()
        # 2.自动添加上次日报提交人信息
        self.assertEquals(drp.page_should_contain_text2("大佬1"), True)
        # 点击【提交】
        drp.click_submit()
        # 3.草稿日报提交成功，显示当前日报提交概览界面
        self.assertEquals(drp.page_should_contain_text2("提交成功"), True)
        drp.wait_log_overview_page_load()
        drp.click_back_button()
        # 等待日志首页加载
        drp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_RZ_0007(self):
        """新建草稿日志 -- 删除"""

        drp = DailyRecordPage()
        drp.wait_for_page_load()
        # 确保有草稿日报可删除
        drp.click_journals()
        drp.click_daily_paper()
        drp.wait_log_editor_page_load()
        title = "测试草稿日志0007"
        drp.input_title(title)
        # 收起键盘
        drp.click_name_attribute_by_name("完成")
        drp.input_work_summary("测试草稿工作总结0007")
        drp.input_work_plan("测试草稿工作计划0007")
        drp.input_coordinate_and_help("测试草稿协调与帮助0007")
        drp.input_remarks("测试草稿备注0007")
        # 收起键盘
        drp.click_name_attribute_by_name("完成")
        drp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        sccp.click_contacts_by_name("大佬1")
        sccp.click_sure_button()
        drp.click_save_draft()
        drp.wait_for_page_load()
        # 点击相关的草稿日报记录，右下角【删除】
        drp.click_delete()
        # 1.弹出删除草稿日报提示弹窗
        self.assertEquals(drp.page_should_contain_text2("确定"), True)
        # 点击【确定】
        drp.click_sure()
        # 2.草稿日报删除成功，已删除的草稿日报从日报列表消失
        self.assertEquals(drp.page_should_contain_text2("删除成功"), True)
        self.assertEquals(drp.page_should_contain_text2(title, 3), False)
        # 等待日志首页加载
        drp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_RZ_0008(self):
        """已提交日报点赞"""

        drp = DailyRecordPage()
        drp.wait_for_page_load()
        # 确保有已提交日报可供点赞
        Preconditions.create_new_log()
        # 点击任意一条已提交的日报
        drp.click_accessibility_id_attribute_by_name("测试日志")
        # 1.进入日报概览界面
        drp.wait_log_overview_page_load()
        # 获取日报编辑人名字
        name = drp.get_log_editor_name()
        # 点击日报界面的【❤】
        drp.click_love_icon()
        time.sleep(1)
        # 进入点赞人信息页面
        drp.click_accessibility_id_attribute_by_name("1")
        time.sleep(1)
        # 2.点赞成功，并显示点赞人信息和和点赞数量
        self.assertEquals(drp.page_should_contain_text2(name), True)
        self.assertEquals(drp.page_should_contain_text2("1人点赞"), True)
        drp.click_back_button(2)
        # 等待日志首页加载
        drp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_RZ_0009(self):
        """已提交日报取消点赞"""

        drp = DailyRecordPage()
        drp.wait_for_page_load()
        # 确保有可供取消点赞的日报
        Preconditions.create_new_log()
        drp.click_accessibility_id_attribute_by_name("测试日志")
        # 1.进入日报概览界面
        drp.wait_log_overview_page_load()
        # 点击点赞图标
        drp.click_love_icon()
        self.assertEquals(drp.is_exists_accessibility_id_attribute_by_name("1"), True)
        time.sleep(1)
        # 再次点击日报界面的【❤】
        drp.click_love_icon()
        # 2.取消点赞成功，当前点赞人信息和点赞数量减1(间接验证)
        self.assertEquals(drp.is_exists_accessibility_id_attribute_by_name("1"), False)
        drp.click_back_button()
        # 等待日志首页加载
        drp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_RZ_0010(self):
        """已提交日报发表评论"""

        drp = DailyRecordPage()
        drp.wait_for_page_load()
        # 确保有已提交日报可供评论
        Preconditions.create_new_log()
        # 点击任意一条已提交的日报
        drp.click_accessibility_id_attribute_by_name("测试日志")
        # 1.进入日报概览界面
        drp.wait_log_overview_page_load()
        time.sleep(2)
        # 点击日报右下角的【评论】按钮
        drp.click_comment_icon()
        # 2.弹窗评论输入弹窗
        self.assertEquals(drp.page_should_contain_text2("发布"), True)
        # 输入评论内容
        comment = "测试评论0010"
        drp.input_comment(comment)
        # 点击【发布】
        drp.click_release()
        time.sleep(1)
        # 3.评论发布成功，日报概览界面底部显示评论信息
        self.assertEquals(drp.page_should_contain_text2(comment), True)
        drp.click_back_button()
        # 等待日志首页加载
        drp.wait_for_page_load()
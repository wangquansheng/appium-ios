import time

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile
from pages import ContactsPage
from pages import GroupListPage
from pages import MessagePage
from pages import WorkbenchPage
from pages.workbench.group_messenger.SelectCompanyContacts import SelectCompanyContactsPage
from pages.workbench.important_matters.ImportantMatters import ImportantMattersPage
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
    def enter_important_matters_page():
        """进入重要事项首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_important_matters()

    @staticmethod
    def ensure_have_item():
        """确保已有事项"""

        imp = ImportantMattersPage()
        if not imp.is_exists_item():
            imp.click_new_item()
            # 等待创建事项页面加载
            imp.wait_for_create_item_page_load()
            # 输入创建事项标题
            title = "测试事项"
            imp.input_create_item_title(title)
            # 输入创建事项描述
            imp.input_create_item_describe("描述内容12345")
            # 收起键盘
            imp.click_name_attribute_by_name("完成")
            time.sleep(1)
            imp.click_add_icon()
            sccp = SelectCompanyContactsPage()
            sccp.wait_for_page_load()
            # 选择参与人
            sccp.click_contacts_by_name("大佬1")
            sccp.click_sure_button()
            imp.wait_for_create_item_page_load()
            imp.click_create_item()
            imp.wait_for_page_load()

    @staticmethod
    def create_new_item():
        """创建新事项"""

        imp = ImportantMattersPage()
        imp.click_new_item()
        # 等待创建事项页面加载
        imp.wait_for_create_item_page_load()
        # 输入创建事项标题
        title = "测试事项"
        imp.input_create_item_title(title)
        # 输入创建事项描述
        imp.input_create_item_describe("描述内容12345")
        # 收起键盘
        imp.click_name_attribute_by_name("完成")
        time.sleep(1)
        imp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        # 选择参与人
        sccp.click_contacts_by_name("大佬1")
        sccp.click_sure_button()
        imp.wait_for_create_item_page_load()
        imp.click_create_item()
        imp.wait_for_page_load()


class ImportantMattersAllTest(TestCase):

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
        2、当前页面在重要事项首页
        """

        Preconditions.select_mobile('IOS-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_important_matters_page()
            return
        imp = ImportantMattersPage()
        if not imp.is_on_important_matters_page():
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_important_matters_page()

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0001(self):
        """验证点击返回按钮是否正确"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 点击返回
        imp.click_back_button()
        wbp = WorkbenchPage()
        # 1.等待工作台页面加载
        wbp.wait_for_page_load()
        wbp.click_important_items()
        # 等待重要事项首页加载
        imp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0002(self):
        """新建事项"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 清空进行中的事项，确保不影响验证
        imp.clear_item()
        imp.click_new_item()
        # 1.等待创建事项页面加载
        imp.wait_for_create_item_page_load()
        # 输入创建事项标题
        title = "测试事项0002"
        imp.input_create_item_title(title)
        # 输入创建事项描述
        imp.input_create_item_describe("描述内容0002")
        # 收起键盘
        imp.click_name_attribute_by_name("完成")
        time.sleep(1)
        imp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        # 选择参与人
        sccp.click_contacts_by_name("大佬1")
        sccp.click_sure_button()
        imp.wait_for_create_item_page_load()
        imp.click_create_item()
        imp.wait_for_page_load()
        # 2.显示刚刚创建的事项
        self.assertEquals(imp.page_should_contain_text2(title), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0003(self):
        """修改事项标题"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 确保已有事项
        Preconditions.ensure_have_item()
        imp.click_first_item()
        # 1.等待查看事项页面加载
        imp.wait_for_check_item_page_load()
        # 2.点击查看事项页面标题
        imp.click_check_item_title()
        time.sleep(2)
        modify_title = "修改的测试事项标题0003"
        imp.input_modify_content(modify_title)
        # 收起键盘
        imp.click_name_attribute_by_name("完成")
        imp.click_save()
        # 3.等待查看事项页面加载，界面事项标题显示为修改后的标题
        imp.wait_for_check_item_page_load()
        self.assertEquals(imp.page_should_contain_text2(modify_title), True)
        imp.click_back_button()
        # 等待重要事项首页加载
        imp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0004(self):
        """修改事项描述"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 确保已有事项
        Preconditions.ensure_have_item()
        imp.click_first_item()
        # 1.等待查看事项页面加载
        imp.wait_for_check_item_page_load()
        # 2.点击查看事项页面描述
        imp.click_check_item_describe()
        time.sleep(2)
        modify_describe = "修改的测试事项描述0004"
        imp.input_modify_content(modify_describe)
        # 收起键盘
        imp.click_name_attribute_by_name("完成")
        imp.click_save()
        # 3.等待查看事项页面加载，界面事项描述显示为修改后的内容
        imp.wait_for_check_item_page_load()
        self.assertEquals(imp.page_should_contain_text2(modify_describe), True)
        imp.click_back_button()
        # 等待重要事项首页加载
        imp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0005(self):
        """修改增加事项参与人"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 确保已有事项
        Preconditions.ensure_have_item()
        imp.click_first_item()
        # 1.等待查看事项页面加载
        imp.wait_for_check_item_page_load()
        imp.click_personnel_status()
        # 2.等待人员状态页面加载
        imp.wait_for_personnel_status_page_load()
        imp.click_add_personnel()
        sccp = SelectCompanyContactsPage()
        # 3.等待选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬2"
        sccp.input_search_message(search_name)
        # 4.显示搜索结果
        self.assertEquals(sccp.is_search_contacts_name_full_match(search_name), True)
        sccp.click_name_attribute_by_name(search_name, "xpath")
        sccp.click_sure_button()
        # 5.添加成功，等待人员状态页面加载，界面显示刚刚添加的联系人信息
        self.assertEquals(imp.page_should_contain_text2("添加成功"), True)
        imp.wait_for_personnel_status_page_load()
        self.assertEquals(imp.page_should_contain_text2("佬2"), True)
        imp.click_back_button()
        imp.wait_for_check_item_page_load()
        imp.click_back_button()
        # 等待重要事项首页加载
        imp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0006(self):
        """修改删除事项参与人"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 确保已有事项
        Preconditions.ensure_have_item()
        imp.click_first_item()
        # 1.等待查看事项页面加载
        imp.wait_for_check_item_page_load()
        imp.click_personnel_status()
        # 2.等待人员状态页面加载
        imp.wait_for_personnel_status_page_load()
        # 确保有人员可移除
        imp.click_add_personnel()
        sccp = SelectCompanyContactsPage()
        # 等待选择联系人页面加载
        sccp.wait_for_page_load()
        add_name = "大佬3"
        sccp.click_contacts_by_name(add_name)
        sccp.click_sure_button()
        imp.wait_for_personnel_status_page_load()
        imp.click_delete_personnel()
        # 3.界面未读人员显示可删除按钮
        self.assertEquals(imp.is_exists_delete_icon_by_name("佬3"), True)
        imp.click_delete_icon_by_name("佬3")
        time.sleep(2)
        # 4.删除的联系人从界面消失
        self.assertEquals(imp.page_should_contain_text2("佬3"), False)
        # 5.退出删除状态
        imp.click_delete_personnel()
        imp.click_back_button()
        imp.wait_for_check_item_page_load()
        imp.click_back_button()
        # 等待重要事项首页加载
        imp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0007(self):
        """添加评论"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 创建新事项
        Preconditions.create_new_item()
        imp.click_first_item()
        # 1.等待查看事项页面加载
        imp.wait_for_check_item_page_load()
        # 2.打开评论编辑页
        imp.click_comment()
        time.sleep(2)
        comment = "测试评论0007"
        # 输入评论内容
        imp.input_modify_content(comment)
        # 收起键盘
        imp.click_name_attribute_by_name("完成")
        imp.click_submit_comments()
        # 3.等待查看事项页面加载，界面底部显示刚刚的评论内容
        imp.wait_for_check_item_page_load()
        self.assertEquals(imp.page_should_contain_text2(comment), True)
        imp.click_back_button()
        # 等待重要事项首页加载
        imp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0008(self):
        """删除评论"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 创建新事项
        Preconditions.create_new_item()
        imp.click_first_item()
        # 1.等待查看事项页面加载
        imp.wait_for_check_item_page_load()
        # 确保有评论可删除
        imp.click_comment()
        time.sleep(2)
        comment = "测试评论0008"
        imp.input_modify_content(comment)
        # 收起键盘
        imp.click_name_attribute_by_name("完成")
        imp.click_submit_comments()
        imp.wait_for_check_item_page_load()
        # 2.收起事项信息，显示事项动态栏信息
        imp.click_accessibility_id_attribute_by_name("收起详情")
        # 点击指定评论后的删除图标
        imp.click_delete_icon_by_comment(comment)
        # 3.弹出删除评论确认弹窗
        imp.click_sure()
        # 4.评论删除成功，评论从界面消失
        self.assertEquals(imp.page_should_contain_text2("删除成功"), True)
        imp.wait_for_check_item_page_load()
        time.sleep(1)
        self.assertEquals(imp.page_should_contain_text2(comment), False)
        imp.click_back_button()
        # 等待重要事项首页加载
        imp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0009(self):
        """添加子任务"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 创建新事项
        Preconditions.create_new_item()
        imp.click_first_item()
        # 1.等待查看事项页面加载
        imp.wait_for_check_item_page_load()
        imp.click_add_subtasks()
        # 2.等待添加子任务页面加载
        imp.wait_for_add_subtasks_page_load()
        # 输入子任务标题
        title = "子任务标题0009"
        imp.input_subtasks_title(title)
        # 输入子任务描述
        imp.input_subtasks_describe("子任务描述0009")
        # 收起键盘
        imp.click_name_attribute_by_name("完成")
        time.sleep(1)
        imp.click_subtasks_add_icon()
        sccp = SelectCompanyContactsPage()
        # 3.等待选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬1"
        sccp.input_search_message(search_name)
        sccp.click_name_attribute_by_name(search_name, "xpath")
        # sccp.click_sure_button()
        # 4.返回添加子任务编辑界面，界面底部显示添加的联系人
        imp.wait_for_add_subtasks_page_load()
        self.assertEquals(imp.page_should_contain_text2("佬1"), True)
        # 选择截止时间
        imp.click_modify()
        time.sleep(2)
        imp.swipe_time_by_hour()
        imp.click_sure()
        imp.click_save()
        imp.wait_for_check_item_page_load()
        # 5.中间子任务栏，显示刚刚添加的子任务
        self.assertEquals(imp.page_should_contain_text2(title), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0010(self):
        """添加子任务"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 创建新事项
        Preconditions.create_new_item()
        imp.click_first_item()
        # 1.等待查看事项页面加载
        imp.wait_for_check_item_page_load()
        imp.click_add_subtasks()
        # 2.等待添加子任务页面加载
        imp.wait_for_add_subtasks_page_load()
        # 输入子任务标题
        title = "子任务标题0010"
        imp.input_subtasks_title(title)
        # 输入子任务描述
        imp.input_subtasks_describe("子任务描述0010")
        # 收起键盘
        imp.click_name_attribute_by_name("完成")
        time.sleep(1)
        imp.click_subtasks_add_icon()
        sccp = SelectCompanyContactsPage()
        # 3.等待选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬1"
        sccp.input_search_message(search_name)
        sccp.click_name_attribute_by_name(search_name, "xpath")
        # sccp.click_sure_button()
        # 4.返回添加子任务编辑界面，界面底部显示添加的联系人
        imp.wait_for_add_subtasks_page_load()
        self.assertEquals(imp.page_should_contain_text2("佬1"), True)
        # 选择截止时间
        imp.click_modify()
        time.sleep(2)
        imp.swipe_time_by_hour()
        imp.click_sure()
        imp.click_save()
        imp.wait_for_check_item_page_load()
        # 5.中间子任务栏，显示刚刚添加的子任务
        self.assertEquals(imp.page_should_contain_text2(title), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0011(self):
        """修改子任务-修改任务标题"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 创建新事项
        Preconditions.create_new_item()
        imp.click_first_item()
        # 1.等待查看事项页面加载
        imp.wait_for_check_item_page_load()
        # 确保有子任务可修改
        imp.click_add_subtasks()
        imp.wait_for_add_subtasks_page_load()
        title = "子任务标题0011"
        imp.input_subtasks_title(title)
        imp.input_subtasks_describe("子任务描述0011")
        # 收起键盘
        imp.click_name_attribute_by_name("完成")
        time.sleep(1)
        imp.click_subtasks_add_icon()
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        sccp.click_contacts_by_name("大佬1")
        # sccp.click_sure_button()
        imp.wait_for_add_subtasks_page_load()
        imp.click_save()
        imp.wait_for_check_item_page_load()
        # 2.打开查看子任务界面
        imp.click_accessibility_id_attribute_by_name(title)
        time.sleep(2)
        # 3.打开子任务标题编辑界面
        imp.click_accessibility_id_attribute_by_name(title)
        time.sleep(2)
        modify_title = "修改的子任务标题0011"
        imp.input_modify_content(modify_title)
        # 收起键盘
        imp.click_name_attribute_by_name("完成")
        imp.click_save()
        # 4.修改成功，返回查看子任务详情界面，界面任务标题显示为刚刚修改的标题
        self.assertEquals(imp.page_should_contain_text2("修改成功"), True)
        imp.wait_for_check_subtasks_page_load()
        self.assertEquals(imp.page_should_contain_text2(modify_title), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0012(self):
        """修改子任务-修改任务描述"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 创建新事项
        Preconditions.create_new_item()
        imp.click_first_item()
        # 1.等待查看事项页面加载
        imp.wait_for_check_item_page_load()
        # 确保有子任务可修改
        imp.click_add_subtasks()
        imp.wait_for_add_subtasks_page_load()
        title = "子任务标题0012"
        imp.input_subtasks_title(title)
        content = "子任务描述0012"
        imp.input_subtasks_describe(content)
        # 收起键盘
        imp.click_name_attribute_by_name("完成")
        time.sleep(1)
        imp.click_subtasks_add_icon()
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        sccp.click_contacts_by_name("大佬1")
        # sccp.click_sure_button()
        imp.wait_for_add_subtasks_page_load()
        imp.click_save()
        imp.wait_for_check_item_page_load()
        # 2.打开查看子任务界面
        imp.click_accessibility_id_attribute_by_name(title)
        time.sleep(2)
        # 3.打开子任务内容编辑界面
        imp.click_accessibility_id_attribute_by_name(content)
        time.sleep(2)
        modify_content = "修改的子任务描述0012"
        imp.input_modify_content(modify_content)
        # 收起键盘
        imp.click_name_attribute_by_name("完成")
        imp.click_save()
        # 4.修改成功，返回查看子任务详情界面，界面任务描述显示为刚刚修改的信息
        self.assertEquals(imp.page_should_contain_text2("修改成功"), True)
        imp.wait_for_check_subtasks_page_load()
        self.assertEquals(imp.page_should_contain_text2(modify_content), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0013(self):
        """修改子任务-修改标题"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 创建新事项
        Preconditions.create_new_item()
        imp.click_first_item()
        # 1.等待查看事项页面加载
        imp.wait_for_check_item_page_load()
        # 确保有子任务可修改
        imp.click_add_subtasks()
        imp.wait_for_add_subtasks_page_load()
        title = "子任务标题0013"
        imp.input_subtasks_title(title)
        imp.input_subtasks_describe("子任务描述0013")
        # 收起键盘
        imp.click_name_attribute_by_name("完成")
        time.sleep(1)
        imp.click_subtasks_add_icon()
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        sccp.click_contacts_by_name("大佬1")
        # sccp.click_sure_button()
        imp.wait_for_add_subtasks_page_load()
        imp.click_save()
        imp.wait_for_check_item_page_load()
        # 2.打开查看子任务界面
        imp.click_accessibility_id_attribute_by_name(title)
        time.sleep(2)
        # 3.打开子任务标题编辑界面
        imp.click_accessibility_id_attribute_by_name(title)
        time.sleep(2)
        modify_title = "修改的子任务标题0013"
        imp.input_modify_content(modify_title)
        # 收起键盘
        imp.click_name_attribute_by_name("完成")
        imp.click_save()
        # 4.修改成功，返回查看子任务详情界面，界面任务标题显示为刚刚修改的标题
        self.assertEquals(imp.page_should_contain_text2("修改成功"), True)
        imp.wait_for_check_subtasks_page_load()
        self.assertEquals(imp.page_should_contain_text2(modify_title), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0014(self):
        """修改子任务-修改负责人"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 创建新事项
        Preconditions.create_new_item()
        imp.click_first_item()
        # 1.等待查看事项页面加载
        imp.wait_for_check_item_page_load()
        # 确保有子任务可修改
        imp.click_add_subtasks()
        imp.wait_for_add_subtasks_page_load()
        title = "子任务标题0014"
        imp.input_subtasks_title(title)
        imp.input_subtasks_describe("子任务描述0014")
        # 收起键盘
        imp.click_name_attribute_by_name("完成")
        time.sleep(1)
        imp.click_subtasks_add_icon()
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        sccp.click_contacts_by_name("大佬1")
        # sccp.click_sure_button()
        imp.wait_for_add_subtasks_page_load()
        imp.click_save()
        imp.wait_for_check_item_page_load()
        # 2.打开查看子任务界面
        imp.click_accessibility_id_attribute_by_name(title)
        time.sleep(2)
        imp.click_accessibility_id_attribute_by_name("佬1")
        # 3.等待选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬2"
        sccp.input_search_message(search_name)
        time.sleep(2)
        sccp.click_name_attribute_by_name(search_name, "xpath")
        # sccp.click_sure_button()
        # 4.修改成功，返回查看子任务详情界面，界面负责人显示为刚刚修改的联系人
        imp.wait_for_check_subtasks_page_load()
        self.assertEquals(imp.page_should_contain_text2("佬2"), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0015(self):
        """修改子任务-修改截止时间"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 创建新事项
        Preconditions.create_new_item()
        imp.click_first_item()
        # 1.等待查看事项页面加载
        imp.wait_for_check_item_page_load()
        # 确保有子任务可修改
        imp.click_add_subtasks()
        imp.wait_for_add_subtasks_page_load()
        title = "子任务标题0015"
        imp.input_subtasks_title(title)
        imp.input_subtasks_describe("子任务描述0015")
        # 收起键盘
        imp.click_name_attribute_by_name("完成")
        time.sleep(1)
        imp.click_subtasks_add_icon()
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        sccp.click_contacts_by_name("大佬1")
        # sccp.click_sure_button()
        imp.wait_for_add_subtasks_page_load()
        imp.click_save()
        imp.wait_for_check_item_page_load()
        # 2.打开查看子任务界面
        imp.click_accessibility_id_attribute_by_name(title)
        time.sleep(2)
        # 3.打开时间选择弹窗
        imp.click_modify()
        time.sleep(2)
        # 选择截止时间
        year = "2022"
        imp.click_year(year)
        hour = "23"
        imp.click_hour(hour)
        minute = "59"
        imp.click_minute(minute)
        imp.click_sure()
        # 4.修改成功，返回查看子任务详情界面，界面截止时间显示为刚刚修改的时间信息
        self.assertEquals(imp.page_should_contain_text2("修改成功"), True)
        imp.wait_for_check_subtasks_page_load()
        self.assertEquals(imp.page_should_contain_text2(hour + ":" + minute), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0016(self):
        """删除子任务"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 创建新事项
        Preconditions.create_new_item()
        imp.click_first_item()
        # 1.等待查看事项页面加载
        imp.wait_for_check_item_page_load()
        # 确保有子任务可修改
        imp.click_add_subtasks()
        imp.wait_for_add_subtasks_page_load()
        title = "子任务标题0016"
        imp.input_subtasks_title(title)
        imp.input_subtasks_describe("子任务描述0016")
        # 收起键盘
        imp.click_name_attribute_by_name("完成")
        time.sleep(1)
        imp.click_subtasks_add_icon()
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        sccp.click_contacts_by_name("大佬1")
        # sccp.click_sure_button()
        imp.wait_for_add_subtasks_page_load()
        imp.click_save()
        imp.wait_for_check_item_page_load()
        # 2.打开查看子任务界面
        imp.click_accessibility_id_attribute_by_name(title)
        time.sleep(2)
        # 3.弹窗删除子任务按钮
        imp.click_task_three_points_icon()
        # 4.弹窗删除确认弹窗
        imp.click_delete_subtasks()
        imp.click_sure()
        # 5.子任务删除，返回事项列表首页，再次打开该事项详情，相关的子任务已经从子任务列表消失（由于元素没有ID，间接验证）
        self.assertEquals(imp.page_should_contain_text2("删除成功"), True)
        imp.wait_for_page_load()
        imp.click_first_item()
        imp.wait_for_check_item_page_load()
        self.assertEquals(imp.page_should_contain_text2("没子任务"), True)
        imp.click_back_button()
        # 等待重要事项首页加载
        imp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0018(self):
        """事项归档"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 确保已有事项
        Preconditions.ensure_have_item()
        imp.click_first_item()
        # 1.等待查看事项页面加载
        imp.wait_for_check_item_page_load()
        # 2.弹出是否归档提示弹窗
        imp.click_file_matters()
        imp.click_sure()
        # 3.事项归档成功，显示已归档事项列表
        self.assertEquals(imp.page_should_contain_text2("归档成功", 20), True)
        imp.wait_for_filed_list_page_load()
        imp.click_check_having_item()
        # 等待重要事项首页加载
        imp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0019(self):
        """事项删除"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 清空进行中的事项，确保不影响验证
        imp.clear_item()
        # 确保有事项删除
        imp.click_new_item()
        imp.wait_for_create_item_page_load()
        title = "测试事项0019"
        imp.input_create_item_title(title)
        imp.input_create_item_describe("描述内容0019")
        # 收起键盘
        imp.click_name_attribute_by_name("完成")
        time.sleep(1)
        imp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        sccp.click_contacts_by_name("大佬1")
        sccp.click_sure_button()
        imp.wait_for_create_item_page_load()
        imp.click_create_item()
        imp.wait_for_page_load()
        imp.click_first_item()
        # 1.等待查看事项页面加载
        imp.wait_for_check_item_page_load()
        # 2.弹出删除事项弹窗
        imp.click_three_points_icon()
        # 3.弹出删除事项确认弹窗
        imp.click_delete_item()
        imp.click_sure()
        # 4.事项删除成功，事项从进行中事项列表清除
        self.assertEquals(imp.page_should_contain_text2("删除成功"), True)
        imp.wait_for_page_load()
        self.assertEquals(imp.page_should_contain_text2(title), False)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0020(self):
        """进行中事项列表和归档事项列表切换"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        imp.click_filed_item()
        # 1.切换到已归档事项列表
        imp.wait_for_filed_list_page_load()
        imp.click_check_having_item()
        # 2.切换到进行中的事项列表
        imp.wait_for_page_load()

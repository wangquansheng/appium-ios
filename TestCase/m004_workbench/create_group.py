import time

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile
from pages import ContactsPage
from pages import GroupChatPage
from pages import GroupListPage
from pages import MessagePage
from pages import WorkbenchPage
from pages.workbench.create_group.CreateGroup import CreateGroupPage
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
    def enter_workbench_page():
        """进入工作台首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @staticmethod
    def enter_create_group_page():
        """进入创建群首页"""

        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_create_group()


class CreateGroupAllTest(TestCase):

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
    def test_CJQ_0001(self):
        """建一个企业群，并发起群聊"""

        Preconditions.enter_create_group_page()
        cgp = CreateGroupPage()
        cgp.wait_for_page_load()
        # 点击界面底部【马上创建群】
        cgp.click_create_group()
        sccp = SelectCompanyContactsPage()
        # 1.打开企业联系人选择界面
        sccp.wait_for_page_load()
        # 搜索要加入群的联系人
        search_name1 = "大佬1"
        sccp.input_search_message(search_name1)
        # 2.点击搜索结果里面的联系人
        sccp.click_name_attribute_by_name(search_name1, "xpath")
        # 重复步骤2，全部联系人添加完成后，点击【确定】
        search_name2 = "大佬2"
        sccp.input_search_message(search_name2)
        sccp.click_name_attribute_by_name(search_name2, "xpath")
        sccp.click_sure_button()
        # 3.打开创建群命名界面
        self.assertEquals(cgp.page_should_contain_text2("马上创建群"), True)
        # 输入群名，点击【马上创建群】
        cgp.input_group_name("测试企业群0001")
        # 收起键盘
        cgp.click_name_attribute_by_name("完成")
        cgp.click_create_group()
        # 4.成功创建群，打开发起群聊界面
        self.assertEquals(cgp.page_should_contain_text2("创建群成功"), True)
        # 点击【马上发起群聊】
        cgp.click_name_attribute_by_name("发起群聊")
        gcp = GroupChatPage()
        # 5.打开群聊界面
        gcp.wait_for_page_load()
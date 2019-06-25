import time
import unittest

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import ChatMorePage
from pages import ChatSelectFilePage
from pages import ChatSelectLocalFilePage
from pages import CreateGroupNamePage
from pages import GroupChatPage
from pages import MessagePage
from pages import SelectContactsPage
from pages import SelectLocalContactsPage
from pages import SelectOneGroupPage
from pages import GroupChatSetPage
from pages import WorkbenchPage
from pages.workbench.group_messenger.GroupMessenger import GroupMessengerPage
from pages.workbench.group_messenger.HelpCenter import HelpCenterPage
from pages.workbench.group_messenger.NewMessage import NewMessagePage
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
    def enter_group_chat_page(reset=False):
        """进入群聊聊天会话页面"""
        # 确保已有群
        Preconditions.make_already_have_my_group(reset)
        # 如果有群，会在选择一个群页面，没有创建群后会在群聊页面
        scp = GroupChatPage()
        sogp = SelectOneGroupPage()
        if sogp.is_on_this_page():
            group_name = Preconditions.get_group_chat_name()
            # 点击群名，进入群聊页面
            sogp.select_one_group_by_name(group_name)
            scp.wait_for_page_load()
        if scp.is_on_this_page():
            return
        else:
            raise AssertionError("Failure to enter group chat session page.")

    @staticmethod
    def make_already_have_my_group(reset=False):
        """确保有群，没有群则创建群名为mygroup+电话号码后4位的群"""
        # 消息页面
        Preconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            flag = sc.wait_for_page_load()
            if not flag:
                sc.click_back()
                time.sleep(2)
                mess.click_add_icon()
                mess.click_group_chat()
                sc = SelectContactsPage()
            else:
                break
            n = n + 1
        time.sleep(3)
        sc.click_select_one_group()
        # 群名
        group_name = Preconditions.get_group_chat_name()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        group_names = sog.get_group_name()
        # 有群返回，无群创建
        if group_name in group_names:
            return
        sog.click_back()
        time.sleep(2)
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 从本地联系人中选择成员创建群
        sc.click_local_contacts()
        time.sleep(2)
        slc = SelectLocalContactsPage()
        a=0
        names={}
        while a<3:
            names = slc.get_contacts_name()
            num=len(names)
            if not names:
                raise AssertionError("No contacts, please add contacts in address book.")
            if num==1:
                sog.page_up()
                a+=1
                if a==3:
                    raise AssertionError("联系人只有一个，请再添加多个不同名字联系人组成群聊")
            else:
                break
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        slc.click_sure()
        # 创建群
        cgnp = CreateGroupNamePage()
        cgnp.input_group_name(group_name)
        cgnp.click_sure()
        # 等待群聊页面加载
        GroupChatPage().wait_for_page_load()

    @staticmethod
    def get_group_chat_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "ag" + phone_number[-4:]
        return group_name

    @staticmethod
    def public_send_file(file_type):
        """选择指定类型文件发送"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = GroupChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击本地文件
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 没有预置文件，则上传
        flag = local_file.push_preset_file()
        if flag:
            local_file.click_back()
            csf.click_local_file()
        # 进入预置文件目录，选择文件发送
        local_file.click_preset_file_dir()
        file = local_file.select_file(file_type)
        if file:
            local_file.click_send()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @staticmethod
    def delete_record_group_chat():
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # if not gcsp.is_toast_exist("聊天记录清除成功"):
            #     raise AssertionError("没有聊天记录清除成功弹窗")
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            if not scp.is_on_this_page():
                raise AssertionError("没有返回到群聊页面")
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @staticmethod
    def build_one_new_group(group_name):
        """新建一个指定名称的群，如果已存在，不建群"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            flag = sc.wait_for_page_load()
            if not flag:
                sc.click_back()
                time.sleep(2)
                mess.click_add_icon()
                mess.click_group_chat()
                sc = SelectContactsPage()
            else:
                break
            n = n + 1
        time.sleep(2)
        sc.click_select_one_group()
        # 群名
        # group_name = Preconditions.get_group_chat_name()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        a=0
        while a<10:
            group_names = sog.get_group_name()
            # 有群返回，无群创建
            if group_name in group_names:
                sog.click_back()
                return
            a+=1
            sog.page_up()

        sog.click_back()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 从本地联系人中选择成员创建群
        sc.click_local_contacts()
        time.sleep(2)
        slc = SelectLocalContactsPage()
        a = 0
        names = {}
        while a < 3:
            names = slc.get_contacts_name()
            num = len(names)
            if not names:
                raise AssertionError("No contacts, please add contacts in address book.")
            if num == 1:
                sog.page_up()
                a += 1
                if a == 3:
                    raise AssertionError("联系人只有一个，请再添加多个不同名字联系人组成群聊")
            else:
                break
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        slc.click_sure()
        # 创建群
        cgnp = CreateGroupNamePage()
        cgnp.input_group_name(group_name)
        cgnp.click_sure()
        # 等待群聊页面加载
        GroupChatPage().wait_for_page_load()
        GroupChatPage().click_back()

    @staticmethod
    def enter_group_messenger_page():
        """进入群发信使首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_group_messenger()


class MsgCommonGroupAllTest(TestCase):

    def default_setUp(self):
        """确保每个用例运行前在群聊聊天会话页面"""
        Preconditions.select_mobile('IOS-移动')
        # mess = MessagePage()
        # if mess.is_on_this_page():
        #     Preconditions.enter_group_chat_page()
        #     return
        # scp = GroupChatPage()
        # if scp.is_on_this_page():
        #     current_mobile().hide_keyboard_if_display()
        #     return
        # else:
        #     current_mobile().launch_app()
        #     # current_mobile().reset_app()
        #     Preconditions.enter_group_chat_page()
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

    @tags('ALL','CMCC','group_chat','full','high')
    def test_msg_xiaoqiu_0001(self):
        """消息列表——发起群聊——选择已有群"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_help_icon()
        hcp = HelpCenterPage()
        # 等待等待群发信使->帮助中心页面加载
        hcp.wait_for_page_load()
        # 1.查看应用简介
        hcp.click_introduction()
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

    @tags('ALL', 'CMCC', 'group_chat','full','high')
    def test_msg_xiaoqiu_0002(self):
        """消息列表——发起群聊——选择已有群"""

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
        # 输入查找信息
        sccp.input_search_message(search_name)
        # 点击勾选搜索出的联系人头像
        sccp.click_contacts_image()
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 1.搜索出的联系人是否被选择
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name(search_name), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat','full','high')
    def test_msg_xiaoqiu_0003(self):
        """群聊列表展示页面——中文精确搜索"""

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
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 添加多个联系人
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
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0004(self):
        """群聊列表展示页面——中文精确搜索"""

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
        # 输入查找信息
        sccp.input_search_message(search_name)
        # 点击勾选搜索出的联系人头像
        sccp.click_contacts_image()
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 1.搜索出的联系人是否被选择
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name(search_name), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0005(self):
        """群聊列表展示页面——英文精确搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_help_icon()
        hcp = HelpCenterPage()
        # 等待等待群发信使->帮助中心页面加载
        hcp.wait_for_page_load()
        # 1.查看应用简介
        hcp.click_introduction()
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

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0006(self):
        """群聊列表展示页面——英文精确搜索"""

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
        # 1.进入多个部门，添加成员
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_accessibility_id_attribute_by_name("测试部门2")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        # 2.各个部门添加成员是否累计
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), True)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0007(self):
        """群聊列表展示页面——空格精确搜索"""

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
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 添加多个联系人
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
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0008(self):
        """群聊列表展示页面——空格精确搜索"""

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
        # 输入查找信息
        sccp.input_search_message(search_name)
        # 点击勾选搜索出的联系人头像
        sccp.click_contacts_image()
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 1.搜索出的联系人是否被选择
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name(search_name), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0009(self):
        """群聊列表展示页面——数字精确搜索"""

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
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 添加多个联系人
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
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0010(self):
        """群聊列表展示页面——数字精确搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_help_icon()
        hcp = HelpCenterPage()
        # 等待等待群发信使->帮助中心页面加载
        hcp.wait_for_page_load()
        # 1.查看应用简介
        hcp.click_introduction()
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

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_xiaoqiu_0011(self):
        """群聊列表展示页面——数字精确搜索"""

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
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 添加多个联系人
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
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_xiaoqiu_0012(self):
        """群聊列表展示页面——数字精确搜索"""

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
        # 输入查找信息
        sccp.input_search_message(search_name)
        # 点击勾选搜索出的联系人头像
        sccp.click_contacts_image()
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 1.搜索出的联系人是否被选择
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name(search_name), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_xiaoqiu_0013(self):
        """群聊列表展示页面——字符精确搜索"""

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
        # 1.进入多个部门，添加成员
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_accessibility_id_attribute_by_name("测试部门2")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        # 2.各个部门添加成员是否累计
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), True)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_xiaoqiu_0014(self):
        """群聊列表展示页面——字符精确搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_help_icon()
        hcp = HelpCenterPage()
        # 等待等待群发信使->帮助中心页面加载
        hcp.wait_for_page_load()
        # 1.查看应用简介
        hcp.click_introduction()
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

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_xiaoqiu_0015(self):
        """群聊列表展示页面——索引字母定位选择"""

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
        # 1.进入多个部门，添加成员
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_accessibility_id_attribute_by_name("测试部门2")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        # 2.各个部门添加成员是否累计
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), True)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0017(self):
        """在群聊天会话页面，发送一条字符长度等于：1的，文本消息"""

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
        # 1.检查搜索结果是否完全匹配关键字
        self.assertEquals(sccp.is_search_contacts_number_full_match(search_number), True)
        # 选择搜索结果
        sccp.click_name_attribute_by_name(search_number, "xpath")
        # 2.是否成功选中，输入框是否自动清空
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_clear_search_box(search_number), True)
        sccp.click_back_button()
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0018(self):
        """在群聊天会话页面，发送一条字符长度，大于1的文本消息"""

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
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 添加多个联系人
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
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0021(self):
        """在群聊天会话页面，输入框中录入1个字符，使用缩小功能发送"""

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
        # 1.检查搜索结果是否完全匹配关键字
        self.assertEquals(sccp.is_search_contacts_number_full_match(search_number), True)
        # 选择搜索结果
        sccp.click_name_attribute_by_name(search_number, "xpath")
        # 2.是否成功选中，输入框是否自动清空
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_clear_search_box(search_number), True)
        sccp.click_back_button()
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0022(self):
        """在群聊天会话页面，输入框中录入500个字符，使用缩小功能发送"""

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
        # 1.进入多个部门，添加成员
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_accessibility_id_attribute_by_name("测试部门2")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        # 2.各个部门添加成员是否累计
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), True)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0023(self):
        """在群聊天会话页面，输入框中录入5000个字符，使用缩小功能发送"""

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
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 添加多个联系人
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
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0024(self):
        """在群聊天会话页面，输入框中录入1个字符，使用放大功能发送"""

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
        # 输入查找信息
        sccp.input_search_message(search_name)
        # 点击勾选搜索出的联系人头像
        sccp.click_contacts_image()
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 1.搜索出的联系人是否被选择
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name(search_name), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0025(self):
        """在群聊天会话页面，输入框中录入500个字符，使用放大功能发送"""

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
        # 1.进入多个部门，添加成员
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_accessibility_id_attribute_by_name("测试部门2")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        # 2.各个部门添加成员是否累计
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), True)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0026(self):
        """在群聊天会话页面，输入框中录入5000个字符，使用放大功能发送"""

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
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 添加多个联系人
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
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0035(self):
        """进入到群聊天会话页面，录入文字+表情字符，放大发送"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_help_icon()
        hcp = HelpCenterPage()
        # 等待等待群发信使->帮助中心页面加载
        hcp.wait_for_page_load()
        # 1.查看应用简介
        hcp.click_introduction()
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

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0036(self):
        """进入到群聊天会话页面，录入文字+表情字符，缩小发送"""

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
        # 1.检查搜索结果是否完全匹配关键字
        self.assertEquals(sccp.is_search_contacts_number_full_match(search_number), True)
        # 选择搜索结果
        sccp.click_name_attribute_by_name(search_number, "xpath")
        # 2.是否成功选中，输入框是否自动清空
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_clear_search_box(search_number), True)
        sccp.click_back_button()
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0037(self):
        """在群聊天会话页面，长按消息体，点击收藏"""

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
        # 输入查找信息
        sccp.input_search_message(search_name)
        # 1.检查搜索结果是否精准匹配关键字
        self.assertEquals(sccp.is_search_contacts_name_full_match(search_name), True)
        # 选择搜索结果
        sccp.click_name_attribute_by_name(search_name, "xpath")
        # 2.搜索栏是否清空，是否出现已选人名和头像，是否展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0038(self):
        """我——收藏——收藏内容展示"""

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
        # 1.进入多个部门，添加成员
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_accessibility_id_attribute_by_name("测试部门2")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        # 2.各个部门添加成员是否累计
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), True)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0039(self):
        """我——收藏——收藏内展示——点击收藏内容"""

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
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 添加多个联系人
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
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0040(self):
        """我——收藏——收藏内展示——点击收藏内容——点击播放收藏语音文件"""

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
        # 输入查找信息
        sccp.input_search_message(search_name)
        # 点击勾选搜索出的联系人头像
        sccp.click_contacts_image()
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 1.搜索出的联系人是否被选择
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name(search_name), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0041(self):
        """我——收藏——收藏内展示——点击收藏内容——点击删除收藏内容"""

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
        # 1.进入多个部门，添加成员
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_accessibility_id_attribute_by_name("测试部门2")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        # 2.各个部门添加成员是否累计
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), True)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0050(self):
        """发送一组数字：95533，发送失败的状态展示"""

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
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 添加多个联系人
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
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0072(self):
        """仅语音模式，录制时长等于1秒时，点击发送按钮"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_help_icon()
        hcp = HelpCenterPage()
        # 等待等待群发信使->帮助中心页面加载
        hcp.wait_for_page_load()
        # 1.查看应用简介
        hcp.click_introduction()
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

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0073(self):
        """仅语音模式，发送录制时长大于1秒的语音"""

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
        # 输入查找信息
        sccp.input_search_message(search_name)
        # 1.检查搜索结果是否精准匹配关键字
        self.assertEquals(sccp.is_search_contacts_name_full_match(search_name), True)
        # 选择搜索结果
        sccp.click_name_attribute_by_name(search_name, "xpath")
        # 2.搜索栏是否清空，是否出现已选人名和头像，是否展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0074(self):
        """仅语音模式，录制时长大于10秒——发送"""

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
        # 1.进入多个部门，添加成员
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        sccp.click_accessibility_id_attribute_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_accessibility_id_attribute_by_name("测试部门2")
        sccp.click_accessibility_id_attribute_by_name("大佬2")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        # 2.各个部门添加成员是否累计
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), True)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0075(self):
        """仅语音模式，录制时长等于60秒—自动发送"""

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
        # 1.是否直接进入企业子一层级
        self.assertEquals(sccp.is_exist_corporate_grade(), True)
        sccp.click_back_button()
        # 2.页面是否跳转到企业层级
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exist_department_name(), True)
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0076(self):
        """仅语音模式，录制时长超过60秒"""

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
        # 输入查找信息
        sccp.input_search_message(search_name)
        # 点击勾选搜索出的联系人头像
        sccp.click_contacts_image()
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 1.搜索出的联系人是否被选择
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name(search_name), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0085(self):
        """在聊天会话页面——点击语音ICON"""

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
        sccp.click_accessibility_id_attribute_by_name("测试部门1")
        # 添加多个联系人
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
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        time.sleep(2)
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬1"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬2"), False)
        self.assertEquals(nmp.is_exists_accessibility_id_attribute_by_name("大佬3"), True)
        nmp.click_back_button()
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0088(self):
        """进入到语音录制页——网络异常"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_help_icon()
        hcp = HelpCenterPage()
        # 等待等待群发信使->帮助中心页面加载
        hcp.wait_for_page_load()
        # 1.查看应用简介
        hcp.click_introduction()
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

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0089(self):
        """语音录制中途——网络异常"""

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
        # 1.是否直接进入企业子一层级
        self.assertEquals(sccp.is_exist_corporate_grade(), True)
        sccp.click_back_button()
        # 2.页面是否跳转到企业层级
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exist_department_name(), True)
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0090(self):
        """语音录制完成——网络异常"""

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
        # 输入查找信息
        sccp.input_search_message(search_name)
        # 1.检查搜索结果是否精准匹配关键字
        self.assertEquals(sccp.is_search_contacts_name_full_match(search_name), True)
        # 选择搜索结果
        sccp.click_name_attribute_by_name(search_name, "xpath")
        # 2.搜索栏是否清空，是否出现已选人名和头像，是否展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back_button()
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx')
    def test_msg_xiaoqiu_0098(self):
        """在群聊会话窗口，点击页面顶部的通话按钮"""

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
        # 1.是否直接进入企业子一层级
        self.assertEquals(sccp.is_exist_corporate_grade(), True)
        sccp.click_back_button()
        # 2.页面是否跳转到企业层级
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exist_department_name(), True)
        sccp.click_back_button()
        nmp.wait_for_page_load()
        nmp.click_back_button()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx')
    def test_msg_xiaoqiu_0101(self):
        """在群聊会话窗口，点击输入框上方的图片ICON，进入到图片展示列表"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_help_icon()
        hcp = HelpCenterPage()
        # 等待等待群发信使->帮助中心页面加载
        hcp.wait_for_page_load()
        # 1.查看应用简介
        hcp.click_introduction()
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

import time
import unittest

from selenium.common.exceptions import TimeoutException
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import AgreementDetailPage
from pages import ChatAudioPage
from pages import ChatMorePage
from pages import ChatSelectFilePage
from pages import ChatSelectLocalFilePage
from pages import ChatWindowPage
from pages import CreateGroupNamePage
from pages import GroupChatPage
from pages import GuidePage
from pages import MeCollectionPage
from pages import MePage
from pages import MessagePage
from pages import OneKeyLoginPage
from pages import PermissionListPage
from pages import SelectContactsPage
from pages import SelectLocalContactsPage
from pages import SelectOneGroupPage
from pages import GroupChatSetPage
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


class MsgCommonGroupAllTest(TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     pass

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

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    # @staticmethod
    # def setUp_test_msg_xiaoqiu_0001():
    #
    #     Preconditions.select_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     current_mobile().launch_app()
    #     # current_mobile().reset_app()
    #     # current_mobile().connect_mobile()
    #     Preconditions.make_already_in_message_page()

    @tags('ALL','CMCC','group_chat','full','high')
    def test_msg_xiaoqiu_0001(self):
        """消息列表——发起群聊——选择已有群"""
        # 1、点击右上角的+号，发起群聊
        # 2、点击选择一个群，是否可以进入到群聊列表展示页面
        # 3、中文模糊搜索，是否可以匹配展示搜索结果
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("啊测测试试")
        #先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("啊")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "啊测测试试":
            raise AssertionError("无法中文模糊搜索")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    # @staticmethod
    # def setUp_test_msg_xiaoqiu_0002():
    #
    #     Preconditions.select_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     mess = MessagePage()
    #     if mess.is_on_this_page():
    #         return
    #     current_mobile().launch_app()
    #     # current_mobile().reset_app()
    #     # current_mobile().connect_mobile()
    #     Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full','high')
    def test_msg_xiaoqiu_0002(self):
        """消息列表——发起群聊——选择已有群"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("啊测测试试")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("啊啊测")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    # @staticmethod
    # def setUp_test_msg_xiaoqiu_0003():
    #
    #     Preconditions.select_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     mess = MessagePage()
    #     if mess.is_on_this_page():
    #         return
    #     current_mobile().launch_app()
    #     # current_mobile().reset_app()
    #     # current_mobile().connect_mobile()
    #     Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full','high')
    def test_msg_xiaoqiu_0003(self):
        """群聊列表展示页面——中文精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("啊测测试试")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("啊测测试试")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "啊测测试试":
            raise AssertionError("无法中文精确搜索")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    # @staticmethod
    # def setUp_test_msg_xiaoqiu_0004():
    #
    #     Preconditions.select_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     mess = MessagePage()
    #     if mess.is_on_this_page():
    #         return
    #     current_mobile().launch_app()
    #     # current_mobile().reset_app()
    #     # current_mobile().connect_mobile()
    #     Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0004(self):
        """群聊列表展示页面——中文精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("啊测测试试")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("啊测测试试啊")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    # @staticmethod
    # def setUp_test_msg_xiaoqiu_0005():
    #
    #     Preconditions.select_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     mess = MessagePage()
    #     if mess.is_on_this_page():
    #         return
    #     current_mobile().launch_app()
    #     # current_mobile().reset_app()
    #     # current_mobile().connect_mobile()
    #     Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0005(self):
        """群聊列表展示页面——英文精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("atteesstt")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("atteesstt")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "atteesstt":
            raise AssertionError("无法英文精确搜索")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    # @staticmethod
    # def setUp_test_msg_xiaoqiu_0006():
    #
    #     Preconditions.select_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     mess = MessagePage()
    #     if mess.is_on_this_page():
    #         return
    #     current_mobile().launch_app()
    #     # current_mobile().reset_app()
    #     # current_mobile().connect_mobile()
    #     Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0006(self):
        """群聊列表展示页面——英文精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("atteesstt")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("aatteesstt")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    # @staticmethod
    # def setUp_test_msg_xiaoqiu_0007():
    #
    #     Preconditions.select_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     mess = MessagePage()
    #     if mess.is_on_this_page():
    #         return
    #     current_mobile().launch_app()
    #     # current_mobile().reset_app()
    #     # current_mobile().connect_mobile()
    #     Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0007(self):
        """群聊列表展示页面——空格精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("a a")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword(" ")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "a a":
            raise AssertionError("无法空格精确搜索")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    # @staticmethod
    # def setUp_test_msg_xiaoqiu_0008():
    #
    #     Preconditions.select_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     mess = MessagePage()
    #     if mess.is_on_this_page():
    #         return
    #     current_mobile().launch_app()
    #     # current_mobile().reset_app()
    #     # current_mobile().connect_mobile()
    #     Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0008(self):
        """群聊列表展示页面——空格精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("a a")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("  ")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    # @staticmethod
    # def setUp_test_msg_xiaoqiu_0009():
    #
    #     Preconditions.select_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     mess = MessagePage()
    #     if mess.is_on_this_page():
    #         return
    #     current_mobile().launch_app()
    #     # current_mobile().reset_app()
    #     # current_mobile().connect_mobile()
    #     Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0009(self):
        """群聊列表展示页面——数字精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("112233445566")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("112233445566")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "112233445566":
            raise AssertionError("无法数字精确搜索")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    # @staticmethod
    # def setUp_test_msg_xiaoqiu_0010():
    #
    #     Preconditions.select_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     mess = MessagePage()
    #     if mess.is_on_this_page():
    #         return
    #     current_mobile().launch_app()
    #     # current_mobile().reset_app()
    #     # current_mobile().connect_mobile()
    #     Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_xiaoqiu_0010(self):
        """群聊列表展示页面——数字精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("112233445566")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("1112233445566")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    # @staticmethod
    # def setUp_test_msg_xiaoqiu_0011():
    #
    #     Preconditions.select_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     mess = MessagePage()
    #     if mess.is_on_this_page():
    #         return
    #     current_mobile().launch_app()
    #     # current_mobile().reset_app()
    #     # current_mobile().connect_mobile()
    #     Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_xiaoqiu_0011(self):
        """群聊列表展示页面——数字精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("112233445566")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("112233445566")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "112233445566":
            raise AssertionError("无法数字精确搜索")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    # @staticmethod
    # def setUp_test_msg_xiaoqiu_0012():
    #
    #     Preconditions.select_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     mess = MessagePage()
    #     if mess.is_on_this_page():
    #         return
    #     current_mobile().launch_app()
    #     # current_mobile().reset_app()
    #     # current_mobile().connect_mobile()
    #     Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_xiaoqiu_0012(self):
        """群聊列表展示页面——数字精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("112233445566")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("1112233445566")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    # @staticmethod
    # def setUp_test_msg_xiaoqiu_0013():
    #
    #     Preconditions.select_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     mess = MessagePage()
    #     if mess.is_on_this_page():
    #         return
    #     current_mobile().launch_app()
    #     # current_mobile().reset_app()
    #     # current_mobile().connect_mobile()
    #     Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_xiaoqiu_0013(self):
        """群聊列表展示页面——字符精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("$$")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("$$")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "$$":
            raise AssertionError("无法字符精确搜索")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    # @staticmethod
    # def setUp_test_msg_xiaoqiu_0014():
    #
    #     Preconditions.select_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     mess = MessagePage()
    #     if mess.is_on_this_page():
    #         return
    #     current_mobile().launch_app()
    #     # current_mobile().reset_app()
    #     # current_mobile().connect_mobile()
    #     Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_xiaoqiu_0014(self):
        """群聊列表展示页面——字符精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("$$")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("$$$")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        sog.click_back_icon()
        sog.click_back()
        # sc.click_back()

    # @staticmethod
    # def setUp_test_msg_xiaoqiu_0015():
    #
    #     Preconditions.select_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     mess = MessagePage()
    #     if mess.is_on_this_page():
    #         return
    #     current_mobile().launch_app()
    #     # current_mobile().reset_app()
    #     # current_mobile().connect_mobile()
    #     Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_xiaoqiu_0015(self):
        """群聊列表展示页面——索引字母定位选择"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("iiiiii")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_text("I")
        time.sleep(2)
        if not sog.is_text_present("iiiiii"):
            raise AssertionError("索引字母不能进行定位")
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            gcp.click_back()
        sog.click_back()
        # sc.click_back()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0017(self):
        """在群聊天会话页面，发送一条字符长度等于：1的，文本消息"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("哈")
        if gcp.is_audio_btn_exit():
            raise AssertionError("右边的语音按钮不会自动变为发送按钮")
        gcp.page_should_contain_send_btn()
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0018(self):
        """在群聊天会话页面，发送一条字符长度，大于1的文本消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        mess="哈"*10
        gcp.input_message(mess)
        if gcp.is_audio_btn_exit():
            raise AssertionError("右边的语音按钮不会自动变为发送按钮")
        gcp.page_should_contain_send_btn()
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0021(self):
        """在群聊天会话页面，输入框中录入1个字符，使用缩小功能发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取文本信息正常的宽度
        info = "哈"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width = gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        info = "哈"
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为width
        # if not gcp.get_width_of_msg_of_text() <= width:
        #     raise AssertionError("文本消息没有缩小展示")

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0022(self):
        """在群聊天会话页面，输入框中录入500个字符，使用缩小功能发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取文本信息正常的高度
        info = "哈"*500
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        height= gcp.get_height_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        info = "哈"*500
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,文本框信息正常高度为height
        if not gcp.get_height_of_msg_of_text() < height:
            raise AssertionError("文本消息没有缩小展示")

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0023(self):
        """在群聊天会话页面，输入框中录入5000个字符，使用缩小功能发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取文本信息正常的高度
        info = "哈" * 5000
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        height = gcp.get_height_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        info = "哈" * 5000
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,文本框信息正常高度为height
        # if not gcp.get_height_of_msg_of_text() <= height:
        #     raise AssertionError("文本消息没有缩小展示")

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0024(self):
        """在群聊天会话页面，输入框中录入1个字符，使用放大功能发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取文本信息正常的宽度
        info = "哈"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width = gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        info = "哈"
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为width
        if not gcp.get_width_of_msg_of_text() > width:
            raise AssertionError("文本消息没有放大展示")

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0025(self):
        """在群聊天会话页面，输入框中录入500个字符，使用放大功能发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取文本信息正常的宽度
        info = "哈"*500
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width = gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        info = "哈"*500
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为width
        # if not gcp.get_width_of_msg_of_text() > width:
        #     raise AssertionError("文本消息没有放大展示")

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0026(self):
        """在群聊天会话页面，输入框中录入5000个字符，使用放大功能发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取文本信息正常的宽度
        info = "哈" * 5000
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width = gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        info = "哈" * 5000
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为width
            # if not gcp.get_width_of_msg_of_text() > width:
            #     raise AssertionError("文本消息没有放大展示")

    # @tags('ALL', 'CMCC', 'group_chat', 'full')
    @unittest.skip("过")
    def test_msg_xiaoqiu_0028(self):
        """进入到群聊天会话页面，录入500个表情字符，缩小发送"""
        gcp=GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 点击表情按钮
        gcp.click_expression_button()
        time.sleep(2)
        # 任意点击一个表情
        els = gcp.get_expressions()
        i=0
        while i<500:
            els[0].click()
            i+=1
        # inputText = gcp.get_input_box().get_attribute("text")
        # if not inputText == els[0].get_attribute("text")*500:
        #     raise AssertionError("被选中的表情不可以存放输入框展示")

        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()

    # @tags('ALL', 'CMCC', 'group_chat', 'full')
    @unittest.skip("过")
    def test_msg_xiaoqiu_0032(self):
        """进入到群聊天会话页面，录入500个表情字符，放大发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 点击表情按钮
        gcp.click_expression_button()
        time.sleep(2)
        # 任意点击一个表情
        els = gcp.get_expressions()
        i = 0
        while i < 500:
            els[0].click()
            i += 1
        # inputText = gcp.get_input_box().get_attribute("text")
        # if not inputText == els[0].get_attribute("text") * 500:
        #     raise AssertionError("被选中的表情不可以存放输入框展示")

        # 长按发送按钮并滑动
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0035(self):
        """进入到群聊天会话页面，录入文字+表情字符，放大发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取信息正常的宽度
        info = "哈"
        gcp.input_message(info)
        # 点击表情按钮
        gcp.click_expression_button()
        time.sleep(2)
        # 任意点击一个表情
        els = gcp.get_expressions()
        els[0].click()
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width = gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        gcp.input_message(info)
        # 任意点击一个表情
        els = gcp.get_expressions()
        els[0].click()
        # 长按发送按钮并滑动
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为width
        if not gcp.get_width_of_msg_of_text() > width:
            raise AssertionError("文本消息没有放大展示")
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()

    @tags('ALL', 'CMCC', 'group_chat', 'full','high')
    def test_msg_xiaoqiu_0036(self):
        """进入到群聊天会话页面，录入文字+表情字符，缩小发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取信息正常的宽度
        info = "哈"
        gcp.input_message(info)
        # 点击表情按钮
        gcp.click_expression_button()
        time.sleep(2)
        # 任意点击一个表情
        els = gcp.get_expressions()
        els[0].click()
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width = gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        gcp.input_message(info)
        # 任意点击一个表情
        els = gcp.get_expressions()
        els[0].click()
        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为width
        if not gcp.get_width_of_msg_of_text() < width:
            raise AssertionError("文本消息没有放大展示")
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0037(self):
        """在群聊天会话页面，长按消息体，点击收藏"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        #输入信息
        info = "哈哈"
        gcp.input_message(info)
        gcp.send_message()
        # 长按信息并点击收藏
        time.sleep(2)
        gcp.press_file_to_do("哈哈", "收藏")
        flag = gcp.is_toast_exist("已收藏")
        self.assertTrue(flag)

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0038(self):
        """我——收藏——收藏内容展示"""
        gcp = GroupChatPage()
        time.sleep(2)
        gcp.click_back()
        time.sleep(2)
        sogp = SelectOneGroupPage()
        if sogp.is_on_this_page():
            sogp.click_back()
            sc = SelectContactsPage()
            sc.click_back()
        # 进入我页面
        mess = MessagePage()
        time.sleep(2)
        mess.open_me_page()
        me = MePage()
        me.click_collection()
        time.sleep(1)
        if not me.is_text_present("哈哈"):
            raise AssertionError("收藏的消息内容不能正常展示出来")
        mcp = MeCollectionPage()
        mcp.page_contain_element("收藏时间")
        mcp.page_contain_element("内容来源")
        mcp.click_back()
        me.open_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0039(self):
        """我——收藏——收藏内展示——点击收藏内容"""
        gcp = GroupChatPage()
        time.sleep(2)
        if gcp.is_on_this_page():
            gcp.click_back()
        # sogp = SelectOneGroupPage()
        # sogp.click_back()
        # sc = SelectContactsPage()
        # sc.click_back()
        # 进入我页面
        mess = MessagePage()
        mess.open_me_page()
        me = MePage()
        me.click_collection()
        time.sleep(1)
        if not me.is_text_present("哈哈"):
            raise AssertionError("收藏的消息内容不能正常展示出来")
        mcp = MeCollectionPage()
        mcp.click_text("哈哈")
        time.sleep(1)
        if not mcp.is_text_present("详情"):
            raise AssertionError("不能进入到消息展示详情页面")
        mcp.click_back()
        time.sleep(2)
        #验证可以返回到收藏列表页
        if not mcp.is_text_present("收藏"):
            raise AssertionError("不能返回到收藏列表页")
        mcp.click_back()
        me.open_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0040(self):
        """我——收藏——收藏内展示——点击收藏内容——点击播放收藏语音文件"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        time.sleep(1)
        gcp.press_voice_message_to_do("收藏")
        if not gcp.is_toast_exist("已收藏"):
            raise AssertionError("收藏失败")
        gcp.click_back()
        # sogp = SelectOneGroupPage()
        # sogp.click_back()
        # sc = SelectContactsPage()
        # sc.click_back()
        # 进入我页面
        mess = MessagePage()
        mess.open_me_page()
        me = MePage()
        me.click_collection()
        time.sleep(1)
        if not me.is_text_present("秒"):
            raise AssertionError("收藏的消息内容不能正常展示出来")
        mcp = MeCollectionPage()
        mcp.click_text("秒")
        time.sleep(1)
        if not mcp.is_text_present("详情"):
            raise AssertionError("不能进入到消息展示详情页面")
        # 播放语音消息
        mcp.click_collection_voice_msg()
        time.sleep(2)
        # 暂停语音消息
        mcp.click_collection_voice_msg()
        mcp.click_back()
        time.sleep(2)
        mcp.click_back()
        me.open_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0041(self):
        """我——收藏——收藏内展示——点击收藏内容——点击删除收藏内容"""
        gcp = GroupChatPage()
        time.sleep(2)
        gcp.click_back()
        # sogp = SelectOneGroupPage()
        # sogp.click_back()
        # sc = SelectContactsPage()
        # sc.click_back()
        # 进入我页面
        mess = MessagePage()
        mess.open_me_page()
        me = MePage()
        me.click_collection()
        time.sleep(2)
        # 左滑收藏消息体
        mcp = MeCollectionPage()
        mcp.press_and_move_left()
        # 判断是否有删除按钮
        if mcp.is_delete_element_present():
            mcp.click_delete_collection()
            time.sleep(2)
            #判断是否会弹出确认弹窗
            if not mcp.is_text_present("确定"):
                raise AssertionError("没有弹出确认窗口")
            #点击取消
            mcp.click_cancel_forward()
            flag=mcp.is_delete_element_present()
            self.assertTrue(flag)
            time.sleep(1)
            mcp.click_delete_collection()
            mcp.click_sure_forward()
            time.sleep(2)
            if not mcp.is_toast_exist("取消收藏成功"):
                raise AssertionError("不可以删除收藏的消息体")
        else:
            raise AssertionError("没有删除按钮")
        mcp.click_back()
        me.open_message_page()


    @tags('ALL', 'CMCC', 'group_chat', 'full','a','high')
    def test_msg_xiaoqiu_0050(self):
        """发送一组数字：95533，发送失败的状态展示"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.set_network_status(0)
        # 输入信息
        info = "95533"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送失败'.format(10))
        # 判断是否会展示重新发送按钮
        if not gcp.is_exist_msg_send_failed_button():
            try:
                raise AssertionError("没有重发按钮")
            except AssertionError as e:
                raise e
        time.sleep(2)
        gcp.click_back()
        # sogp = SelectOneGroupPage()
        # sogp.click_back()
        # sc = SelectContactsPage()
        # sc.click_back()
        # time.sleep(1)
        mess = MessagePage()
        if mess.is_on_this_page():
            # 判断是否有“！”
            if not mess.is_iv_fail_status_present():
                try:
                    raise AssertionError("没有消息发送失败“！”标致")
                except AssertionError as e:
                    raise e
            # 进入新消息窗口判断消息是否发送失败
            mess.click_text("95533")
            gcp.wait_for_page_load()
            gcp.set_network_status(6)
            time.sleep(2)
            # 点击重发按钮
            gcp.click_msg_send_failed_button()
            # 点击确定重发
            gcp.click_resend_confirm()
            # 判断信息发送状态
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息未在 {}s 内发送成功'.format(10))

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0072(self):
        """仅语音模式，录制时长等于1秒时，点击发送按钮"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
            if gcp.is_text_present("允许"):
                audio.click_allow()
            time.sleep(1)
            audio.click_send_bottom()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            audio.click_exit()
            gcp.hide_keyboard()
        else:
            audio.click_send_bottom()
            audio.click_setting_bottom()
            if audio.wait_for_audio_type_select_page_load():
                # 点击只发送语言模式
                audio.click_only_voice()
                audio.click_sure()
                audio.click_send_bottom()
                # 验证是否发送成功
                cwp = ChatWindowPage()
                try:
                    cwp.wait_for_msg_send_status_become_to('发送成功', 10)
                except TimeoutException:
                    raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
                audio.click_exit()
                gcp.hide_keyboard()
            else:
                raise AssertionError("语音模式选择页面加载失败")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0073(self):
        """仅语音模式，发送录制时长大于1秒的语音"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.hide_keyboard()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
            if gcp.is_text_present("允许"):
                audio.click_allow()
            time.sleep(2)
            audio.click_send_bottom()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            audio.click_exit()
            gcp.hide_keyboard()
        else:
            audio.click_send_bottom()
            audio.click_setting_bottom()
            if audio.wait_for_audio_type_select_page_load():
                # 点击只发送语言模式
                audio.click_only_voice()
                audio.click_sure()
                time.sleep(2)
                audio.click_send_bottom()
                # 验证是否发送成功
                cwp = ChatWindowPage()
                try:
                    cwp.wait_for_msg_send_status_become_to('发送成功', 10)
                except TimeoutException:
                    raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
                audio.click_exit()
                gcp.hide_keyboard()
            else:
                raise AssertionError("语音模式选择页面加载失败")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0074(self):
        """仅语音模式，录制时长大于10秒——发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.hide_keyboard()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
            if gcp.is_text_present("允许"):
                audio.click_allow()
            time.sleep(11)
            audio.click_exit()
            time.sleep(1)
            if gcp.is_text_present("语音录制中"):
                raise AssertionError("退出语音录制模式失败")
            gcp.hide_keyboard()
        else:
            audio.click_send_bottom()
            audio.click_setting_bottom()
            if audio.wait_for_audio_type_select_page_load():
                # 点击只发送语言模式
                audio.click_only_voice()
                audio.click_sure()
                time.sleep(11)
                audio.click_exit()
                time.sleep(1)
                if gcp.is_text_present("语音录制中"):
                    raise AssertionError("退出语音录制模式失败")
                gcp.hide_keyboard()
            else:
                raise AssertionError("语音模式选择页面加载失败")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0075(self):
        """仅语音模式，录制时长等于60秒—自动发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.hide_keyboard()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
            if gcp.is_text_present("允许"):
                audio.click_allow()
            time.sleep(60)
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            audio.click_exit()
            gcp.hide_keyboard()
        else:
            audio.click_send_bottom()
            audio.click_setting_bottom()
            if audio.wait_for_audio_type_select_page_load():
                # 点击只发送语言模式
                audio.click_only_voice()
                audio.click_sure()
                time.sleep(1)
                audio.click_exit()
                Preconditions.delete_record_group_chat()
                gcp.click_audio_btn()
                time.sleep(60)
                # 验证是否发送成功
                cwp = ChatWindowPage()
                try:
                    cwp.wait_for_msg_send_status_become_to('发送成功', 10)
                except TimeoutException:
                    raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
                audio.click_exit()
                gcp.hide_keyboard()
            else:
                raise AssertionError("语音模式选择页面加载失败")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0076(self):
        """仅语音模式，录制时长超过60秒"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.hide_keyboard()
        audio = ChatAudioPage()
        if gcp.is_text_present("退出"):
            audio.click_exit()
            time.sleep(2)
        gcp.click_audio_btn()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
            if gcp.is_text_present("允许"):
                audio.click_allow()
            time.sleep(65)
            if gcp.is_text_present("语音录制中"):
                raise AssertionError("录制时长可以超过60秒")
            audio.click_exit()
            gcp.hide_keyboard()
        else:
            audio.click_send_bottom()
            audio.click_setting_bottom()
            if audio.wait_for_audio_type_select_page_load():
                # 点击只发送语言模式
                audio.click_only_voice()
                audio.click_sure()
                time.sleep(65)
                if gcp.is_text_present("语音录制中"):
                    raise AssertionError("录制时长可以超过60秒")
                audio.click_exit()
                gcp.hide_keyboard()
            else:
                raise AssertionError("语音模式选择页面加载失败")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0085(self):
        """在聊天会话页面——点击语音ICON"""
        gcp = GroupChatPage()
        #断网
        gcp.set_network_status(0)
        time.sleep(8)
        Preconditions.delete_record_group_chat()
        gcp.hide_keyboard()
        audio = ChatAudioPage()
        if gcp.is_text_present("退出"):
            audio.click_exit()
            time.sleep(2)
        gcp.click_audio_btn()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
            time.sleep(2)
            if gcp.is_text_present("允许"):
                audio.click_allow()
            time.sleep(3)
            if not gcp.is_text_present("网络不可用，请检查网络设置"):
                raise AssertionError("没有出现网络不可用提示")
            audio.click_exit()
            gcp.hide_keyboard()
        else:
            time.sleep(3)
            if not gcp.is_text_present("网络不可用，请检查网络设置"):
                raise AssertionError("没有出现网络不可用提示")
            audio.click_exit()
            gcp.hide_keyboard()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0088(self):
        """进入到语音录制页——网络异常"""
        gcp = GroupChatPage()
        # 断网
        gcp.set_network_status(0)
        time.sleep(2)
        Preconditions.delete_record_group_chat()
        gcp.hide_keyboard()
        audio = ChatAudioPage()
        if gcp.is_text_present("退出"):
            audio.click_exit()
            time.sleep(2)
        gcp.click_audio_btn()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
            if gcp.is_text_present("允许"):
                audio.click_allow()
            time.sleep(3)
            if not gcp.is_text_present("网络不可用，请检查网络设置"):
                raise AssertionError("没有出现网络不可用提示")
            audio.click_exit()
            gcp.hide_keyboard()
        else:
            time.sleep(3)
            if not gcp.is_text_present("网络不可用，请检查网络设置"):
                raise AssertionError("没有出现网络不可用提示")
            audio.click_exit()
            gcp.hide_keyboard()

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0089(self):
        """语音录制中途——网络异常"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.hide_keyboard()
        audio = ChatAudioPage()
        if gcp.is_text_present("退出"):
            audio.click_exit()
            time.sleep(2)
        gcp.click_audio_btn()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
            if gcp.is_text_present("允许"):
                audio.click_allow()
            time.sleep(5)
            # 断网
            gcp.set_network_status(0)
            time.sleep(3)
            if not gcp.is_text_present("语音录制中"):
                raise AssertionError("录制会被中断")
            audio.click_exit()
            gcp.hide_keyboard()
        else:
            audio.click_send_bottom()
            audio.click_setting_bottom()
            if audio.wait_for_audio_type_select_page_load():
                # 点击只发送语言模式
                audio.click_only_voice()
                audio.click_sure()
                time.sleep(5)
                # 断网
                gcp.set_network_status(0)
                time.sleep(3)
                if not gcp.is_text_present("语音录制中"):
                    raise AssertionError("录制会被中断")
                audio.click_exit()
                # gcp.hide_keyboard()
                current_mobile().hide_keyboard_if_display()
                time.sleep(3)
            else:
                raise AssertionError("语音模式选择页面加载失败")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx','high')
    def test_msg_xiaoqiu_0090(self):
        """语音录制完成——网络异常"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.hide_keyboard()
        audio = ChatAudioPage()
        if gcp.is_text_present("退出"):
            audio.click_exit()
            time.sleep(2)
        gcp.click_audio_btn()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
            if gcp.is_text_present("允许"):
                audio.click_allow()
            time.sleep(5)
            # 断网
            gcp.set_network_status(0)
            time.sleep(3)
            audio.click_send_bottom()
            # 验证是否发送失败
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送失败', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送失败'.format(10))
            audio.click_exit()
            gcp.hide_keyboard()
        else:
            audio.click_send_bottom()
            audio.click_setting_bottom()
            if audio.wait_for_audio_type_select_page_load():
                # 点击只发送语言模式
                audio.click_only_voice()
                audio.click_sure()
                time.sleep(5)
                # 断网
                gcp.set_network_status(0)
                time.sleep(3)
                audio.click_send_bottom()
                # 验证是否发送失败
                cwp = ChatWindowPage()
                try:
                    cwp.wait_for_msg_send_status_become_to('发送失败', 10)
                except TimeoutException:
                    raise AssertionError('消息在 {}s 内没有发送失败'.format(10))
                audio.click_exit()
                gcp.hide_keyboard()
            else:
                raise AssertionError("语音模式选择页面加载失败")

    # @staticmethod
    # def setUp_test_msg_xiaoqiu_0095():
    #     Preconditions.select_mobile('Android-移动')
    #     # current_mobile().launch_app()
    #     current_mobile().reset_app()
    #     Preconditions.enter_group_chat_page()

    # @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx')
    @unittest.skip("跳过")
    def test_msg_xiaoqiu_0095(self):
        """当前版本，消息语音icon上红点展示后，清除数据重新登录"""
        gcp = GroupChatPage()
        gcp.click_more()
        time.sleep(2)
        gcp.click_more()
        time.sleep(2)
        if not gcp.is_exist_red_dot():
            raise AssertionError("清除数据重新登陆,语音icon不存在红点提示")
        time.sleep(2)
        current_mobile().reset_app()
        Preconditions.enter_group_chat_page()
        gcp.click_more()
        time.sleep(2)
        gcp.click_more()
        time.sleep(2)
        if not gcp.is_exist_red_dot():
            raise AssertionError("清除数据重新登陆,语音icon不存在红点提示")

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx')
    def test_msg_xiaoqiu_0098(self):
        """在群聊会话窗口，点击页面顶部的通话按钮"""
        # 1、点击页面顶部的通话按钮，是否会调起通话选择项弹窗
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_mutilcall()
        time.sleep(2)
        if not gcp.is_text_present("多方视频"):
            raise AssertionError("不会调起通话选择项弹窗")
        gcp.tap_coordinate([(100, 20), (100, 60), (100,100)])

    @tags('ALL', 'CMCC', 'group_chat', 'full', 'full-yyx')
    def test_msg_xiaoqiu_0101(self):
        """在群聊会话窗口，点击输入框上方的图片ICON，进入到图片展示列表"""
        # 1、点击输入框上方的图片ICON，是否可以进入到相册列表页
        # 2、任意选中一张照片，点击右下角的发送按钮，是否可以发送成功
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        Preconditions.delete_record_group_chat()
        if gcp.is_text_present("退出"):
            audio = ChatAudioPage()
            audio.click_exit()
            time.sleep(2)
        gcp.click_picture()
        time.sleep(2)
        if not gcp.is_text_present("原图"):
            raise AssertionError("不可以进入到相册列表页")
        gcp.select_picture()
        time.sleep(2)
        gcp.click_text("发送")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))


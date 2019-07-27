import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.workbench.corporate_news.CorporateNews import CorporateNewsPage
from pages.workbench.corporate_news.CorporateNewsDetails import CorporateNewsDetailsPage
from pages.workbench.corporate_news.CorporateNewsImageText import CorporateNewsImageTextPage
from pages.workbench.corporate_news.CorporateNewsLink import CorporateNewsLinkPage
from pages.workbench.corporate_news.CorporateNewsNoNews import CorporateNewsNoNewsPage
from preconditions.BasePreconditions import WorkbenchPreconditions
import warnings
from pages import *
from pages.contacts.my_group import ALLMyGroup

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
    def make_already_have_my_picture():
        """确保当前群聊页面已有图片"""
        # 1.点击输入框左上方的相册图标
        gcp = GroupChatPage()
        cpg = ChatPicPage()
        gcp.is_on_this_page()
        if gcp.is_exist_msg_image():
            return
        else:
            # 2.进入相片页面,选择一张片相发送
            time.sleep(2)
            gcp.click_picture()
            cpg.wait_for_page_load()
            cpg.select_pic_fk(1)
            cpg.click_send()
            time.sleep(5)

    @staticmethod
    def make_already_have_my_videos():
        """确保当前群聊页面已有视频"""
        # 1.点击输入框左上方的相册图标
        gcp = GroupChatPage()
        cpg = ChatPicPage()
        gcp.wait_for_page_load()
        if gcp.is_exist_msg_videos():
            return
        else:
            # 2.进入相片页面,选择一张片相发送
            gcp.click_picture()
            cpg.wait_for_page_load()
            cpg.select_video_fk(1)
            cpg.click_send()
            time.sleep(5)

    @staticmethod
    def get_into_group_chat_page(name):
        """进入群聊聊天会话页面"""
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击发起群聊
        mp.click_group_chat()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @staticmethod
    def make_no_message_send_failed_status():
        """确保当前消息列表没有消息发送失败的标识影响验证结果"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        if mp.is_iv_fail_status_present():
            mp.clear_fail_in_send_message()

class CommonGroupSetPage(TestCase):
    """群聊设置页面"""

    def default_setUp(self):
        """确保每个用例开始前在群聊页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        name = '群聊2'
        Preconditions.get_into_group_chat_page(name)

    def default_tearDown(self):
        Preconditions.disconnect_mobile('IOS-移动')

    def setUp_test_msg_xiaoqiu_0228(self):
        """确保进入群聊页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg = MessagePage()
        msg.delete_all_message_list()
        name = '群聊2'
        Preconditions.get_into_group_chat_page(name)
        # 确保群聊人数是3个
        GroupChatPage().click_setting()
        # 设置页面 确保群成员人数为3
        set = GroupChatSetPage()
        set.add_member_by_name('大佬1')
        set.add_member_by_name('大佬2')

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0228(self):
        """聊天设置页面——删除并退出群聊——群主(群人数等于3)"""
        set = GroupChatSetPage()
        # 2、点击页面底部的“删除并退出”按钮，会弹出群主转让确认弹窗
        set.click_delete_and_exit()
        self.assertTrue(set.is_exit_element(locator='取消'))
        self.assertTrue(set.is_exit_element(locator='转让'))
        # 3、点击取消或者弹窗空白处，可以关闭弹窗
        set.click_cancel()
        self.assertFalse(set.is_exit_element(locator='转让'))
        # 4、点击“确定”按钮，会跳转到群主转让选择群成员列表页面
        set.click_delete_and_exit()
        set.click_transfer_of_group()
        self.assertTrue(set.is_text_present('选择成员'))
        # 5、任意选中一个成员，弹出群主转让确认弹窗（不会弹出确认弹框，直接退出当前群）
        set.click_menber_list_first_member()
        time.sleep(2)
        # 7.回到消息列表，收到一条系统消息：你已退出群
        MessagePage().wait_for_page_load()
        MessagePage().page_should_contain_text('你已退出群')

    def tearDown_test_msg_xiaoqiu_0228(self):
        """解散群之后添加群"""
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        my_group.creat_group_if_not_exit('群聊2', member_name=['给个红包3', '给个红包2'])
        Preconditions.disconnect_mobile('IOS-移动')

    def setUp_test_msg_xiaoqiu_0229(self):
        """确保进入群聊页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg = MessagePage()
        msg.delete_all_message_list()
        name = '群聊2'
        Preconditions.get_into_group_chat_page(name)
        # 确保群聊人数是3个
        GroupChatPage().click_setting()
        # 设置页面 确保群成员人数为3
        set = GroupChatSetPage()
        set.add_member_by_name('大佬1')

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0229(self):
        """聊天设置页面——删除并退出群聊——群主（群人数小于3）"""
        set = GroupChatSetPage()
        # 2、点击页面底部的“删除并退出”按钮，会弹出提示：解散群后，所有成员将被移除此群
        set.click_delete_and_exit()
        set.page_should_contain_text('群主退群将导致该群解散，确定退出？')
        # 3、点击确定，返回到消息列表并收到一条系统消息，该群已解散
        set.click_sure_exit_group()
        time.sleep(2)
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_contain_text('该群已解散')

    def tearDown_test_msg_xiaoqiu_0229(self):
        """解散群之后添加群"""
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        my_group.creat_group_if_not_exit('群聊2', member_name=['给个红包3', '给个红包2'])
        Preconditions.disconnect_mobile('IOS-移动')

    def setUp_test_msg_xiaoqiu_0231(self):
        """确保进入群聊页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg = MessagePage()
        msg.delete_all_message_list()
        name = '群聊2'
        Preconditions.get_into_group_chat_page(name)
        # 确保群聊人数是3个
        GroupChatPage().click_setting()
        # 设置页面 确保群成员人数大于3
        set = GroupChatSetPage()
        set.add_member_by_name('大佬1')
        set.add_member_by_name('大佬2')
        set.add_member_by_name('大佬3')
        set.click_back()

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0231(self):
        """群聊天会话页面——输入框输入@字符——@联系人"""
        chat = GroupChatPage()
        # 1、在群聊天会话窗口
        self.assertTrue(chat.is_on_this_page())
        # 2、在输入框中，输入@字符，会调起联系人选择器页面
        chat.click_input_box()
        chat.input_message_text('@')
        time.sleep(2)
        chat.page_should_contain_text('选择群成员')
        # 3、选择一个联系人后，会自动返回到聊天会话页面并且在输入框中展示选中联系人的信息
        name = '大佬1'
        chat.select_members_by_name(name)
        message = chat.get_input_message()
        text = '@' + name + ' '
        self.assertEqual(message, text)
        # 4、点击右边的发送按钮，发送出去后，被@的联系人会在消息列表收到@提示
        chat.click_send_button()
        self.assertFalse(chat.is_element_present_resend())

    def tearDown_test_msg_xiaoqiu_0231(self):
        """解散群之后添加群"""
        # 解散群
        if GroupChatPage().is_on_this_page():
            GroupChatPage().wait_for_page_load()
        else:
            Preconditions.make_already_in_message_page()
            Preconditions.enter_group_chat_page('群聊2')
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        set.dissolution_the_group()
        # 新增群
        Preconditions.make_already_in_message_page()
        MessagePage().open_contacts_page()
        ContactsPage().open_group_chat_list()
        my_group = ALLMyGroup()
        my_group.creat_group_if_not_exit('群聊2', member_name=['给个红包3', '给个红包2'])
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0250(self):
        """群消息列表——群聊天会话窗口——发送的消息类型展示"""
        chat = GroupChatPage()
        # 发送文件
        chat.send_file()
        # 1、群聊会话页面中，发送新消息时，会在消息列表的会话窗口展示：发送消息的类型或者类型+内容展示
        Preconditions.make_already_in_message_page()
        MessagePage().page_should_contain_text('文件')

    def setUp_test_msg_xiaoqiu_0267(self):
        """确保进入单聊会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg = MessagePage()
        msg.delete_all_message_list()
        name = '大佬1'
        msg.open_contacts_page()
        ContactsPage().click_phone_contact()
        ContactsPage().select_contacts_by_name(name)
        ContactDetailsPage().click_message_icon()
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        chat.click_setting()
        time.sleep(3)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0267(self):
        """一对一聊天——点对点建群——网络正常"""
        # 1、在单聊设置页面，点击+号，可以跳转到联系人选择器页面
        set = SingleChatSetPage()
        set.click_add_icon()
        select = SelectContactsPage()
        select.page_should_contain_text('选择团队联系人')
        # 2、选择手机联系人后，页面顶部搜索框的左边会展示已选择的联系人信息
        select.select_one_contact_by_name('大佬2')
        time.sleep(2)
        self.assertTrue(select.is_element_present(locator='已选择的联系人'))
        # 3、点击一下，已选择的联系人，会取消已选择的联系人的选中状态
        select.click_contact_which_is_selecd()
        self.assertFalse(select.is_element_present(locator='已选择的联系人'))
        # 4、点击右上角的确定按钮，会跳转到群名称设置页面
        select.select_one_contact_by_name('大佬2')
        select.click_sure_bottom()
        creat_group = CreateGroupNamePage()
        creat_group.page_should_contain_text('群聊名称')
        # 5、群名称设置页面中的群名称，默认展示为：群聊 （不是默认为群聊）
        # 6、设置完群名称，再次点击右上角的确定按钮，建群成功
        creat_group.click_clear_group_name()
        creat_group.input_group_name('新建群聊')
        creat_group.click_sure_creat()
        time.sleep(3)
        self.assertTrue(GroupChatPage().is_on_this_page())

    def tearDown_test_msg_xiaoqiu_0267(self):
        """解散群"""
        # 解散群
        if GroupChatPage().is_on_this_page():
            GroupChatPage().wait_for_page_load()
        else:
            Preconditions.make_already_in_message_page()
            Preconditions.enter_group_chat_page('新建群聊')
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        set.dissolution_the_group()
        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0270(self):
        """群聊设置——群成员列表——未进群提示展示"""
        # 点击进入群成员列表页面
        chat = GroupChatPage()
        chat.click_setting()
        set = GroupChatSetPage()
        set.click_enter_contact_list()
        time.sleep(2)
        # 1、在群成员展示列表页面，点击：还有人未进群，再次邀请提示，会跳转到未进群联系人详情页
        set.click_invite_to_use_again_someone_notuse()
        time.sleep(2)
        set.page_should_contain_text('邀请人员')
        # 2、在未进群联系人详情页面，点击再次邀请按钮，弹出toast提示：群邀请已发送并且返回到群聊天会话页面
        set.click_invite_to_use_again()
        time.sleep(2)
        chat.wait_for_page_load()
        self.assertTrue(chat.is_on_this_page())


    def setUp_test_msg_xiaoqiu_0534(self):
        """确保进入群聊列表页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.open_contacts_page()
        ContactsPage().open_group_chat_list()
        time.sleep(3)

    @tags('ALL', 'CMCC', '')
    def test_msg_xiaoqiu_0534(self):
        """创建一个普通群"""
        # 1、可以正常创建一个普通群
        group = ALLMyGroup()
        group.creat_group_if_not_exit('新建群聊1')
        self.assertTrue(GroupChatPage().is_on_this_page())

    def tearDown_test_msg_xiaoqiu_0534(self):
        # 解散群
        if GroupChatPage().is_on_this_page():
            GroupChatPage().wait_for_page_load()
        else:
            Preconditions.make_already_in_message_page()
            Preconditions.enter_group_chat_page('新建群聊1')
        GroupChatPage().click_setting()
        set = GroupChatSetPage()
        set.dissolution_the_group()






import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import ContactsPage
from pages import GroupChatPage
from pages import GroupListPage
from pages import MessagePage
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


class EnterpriseGroupTotalTest(TestCase):
    """企业群"""

    # @classmethod
    # def setUpClass(cls):
    #
    #     Preconditions.select_mobile('IOS-移动')
    #     # 导入测试联系人、群聊
    #     fail_time1 = 0
    #     flag1 = False
    #     import dataproviders
    #     while fail_time1 < 3:
    #         try:
    #             required_contacts = dataproviders.get_preset_contacts()
    #             conts = ContactsPage()
    #             Preconditions.make_already_in_message_page()
    #             conts.open_contacts_page()
    #             for name, number in required_contacts:
    #                 # 创建联系人
    #                 conts.create_contacts_if_not_exits(name, number)
    #             required_group_chats = dataproviders.get_preset_group_chats()
    #             conts.open_group_chat_list()
    #             group_list = GroupListPage()
    #             for group_name, members in required_group_chats:
    #                 group_list.wait_for_page_load()
    #                 # 创建群
    #                 group_list.create_group_chats_if_not_exits(group_name, members)
    #             group_list.click_back()
    #             conts.open_message_page()
    #             flag1 = True
    #         except:
    #             fail_time1 += 1
    #         if flag1:
    #             break

    def default_setUp(self):

        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0024(self):
        """企业群/党群在消息列表内展示——最新消息时间（修改手机时间可以测试）"""

        # 进入企业群聊天会话页面
        Preconditions.enter_group_chat_page("测试企业群")
        gcp = GroupChatPage()
        # 发送文本
        gcp.input_text_message("123")
        gcp.click_send_button()
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 1分钟内为“刚刚”
        # 1.正常展示
        self.assertEquals(mp.get_first_message_send_time("刚刚"), True)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangmianhua_0025(self):
        """企业群/党群在消息列表内展示——最新消息时间（修改手机时间可以测试）"""

        # 进入企业群聊天会话页面
        Preconditions.enter_group_chat_page("测试企业群")
        gcp = GroupChatPage()
        # 发送文本
        gcp.input_text_message("123")
        gcp.click_send_button()
        # 超过一分钟后返回
        time.sleep(70)
        gcp.click_back_button()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 分钟加1后显示为“X时：X分”
        # 1.正常展示
        self.assertEquals(mp.get_first_message_send_time(":"), True)

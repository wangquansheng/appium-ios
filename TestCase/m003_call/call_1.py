import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from preconditions.BasePreconditions import WorkbenchPreconditions
import warnings
from pages import *


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


class MsgGroupChatTest(TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     """删除消息列表的消息记录"""
    #     warnings.simplefilter('ignore', ResourceWarning)
    #     Preconditions.select_mobile('IOS-移动')
    #     #创建团队ateam7272
    #     Preconditions.make_already_in_message_page()
    #     MessagePage().delete_all_message_list()
    #     Preconditions.create_team_if_not_exist_and_set_as_defalut_team()
    #     # 导入团队联系人、企业部门
    #     fail_time2 = 0
    #     flag2 = False
    #     while fail_time2 < 5:
    #         try:
    #             Preconditions.make_already_in_message_page()
    #             contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
    #             Preconditions.create_he_contacts(contact_names)
    #             contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
    #                               ('陈丹丹', "13800137004"), ('alice', "13800137005"), ('郑海', "13802883296")]
    #             Preconditions.create_he_contacts2(contact_names2)
    #             department_names = ["测试部门1", "测试部门2"]
    #             Preconditions.create_department_and_add_member(department_names)
    #             flag2 = True
    #         except:
    #             fail_time2 += 1
    #         if flag2:
    #             break

    def default_setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zhenyishan_0053(self):
        """从群聊发起多方视频，在多方视频管理界面点击“+”进入联系人选择页"""
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击多方通话
        group_chat_page.click_mutilcall()
        group_chat_page.click_name_attribute_by_name('多方视频')
        time.sleep(2)
        # self.assertEqual(group_chat_page.page_should_contain_text2('大佬2'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zhenyishan_0155(self):
        """分组群发/标签分组/群发消息：发起多方视频，在管理页面点击“+”进入标签分组联系人选择页"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_contacts_only()
        # 联系界面
        contacts_page = ContactsPage()
        contacts_page.wait_for_page_load()
        contacts_page.click_mobile_contacts()
        contacts_page.click_label_grouping()
        contacts_page.click_name_attribute_by_name('新建分组')
        contacts_page.click_name_attribute_by_name('为你的分组创建一个名称')
        lable_group_detail_page = LableGroupDetailPage()
        lable_group_detail_page.input_group_new_name('测试标签分组')
        lable_group_detail_page.click_sure()
        lable_group_detail_page.click_name_attribute_by_name('测试1')
        lable_group_detail_page.click_name_attribute_by_name('测试2')
        lable_group_detail_page.click_name_attribute_by_name('确定(2/200)')
        lable_group_detail_page.click_label_group_icon()
        # 进入标签分组
        lable_group_detail_page.wait_for_page_load()
        lable_group_detail_page.click_send_group_info()
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_mutilcall()
        group_chat_page.click_name_attribute_by_name('多方视频')
        self.assertEqual(group_chat_page.page_should_contain_text2('测试1'), True)
        self.assertEqual(group_chat_page.page_should_contain_text2('测试2'), True)

    @staticmethod
    def tearDown_test_call_zhenyishan_0155():
        """恢复环境，将用例创建的标签删除"""
        try:
            Preconditions.make_already_in_message_page()
            message_page = MessagePage()
            message_page.wait_for_page_load()
            message_page.click_contacts_only()
            # 联系界面
            contacts_page = ContactsPage()
            contacts_page.wait_for_page_load()
            contacts_page.click_mobile_contacts()
            contacts_page.click_label_grouping()
            lable_group_detail_page = LableGroupDetailPage()
            lable_group_detail_page.click_label_group_icon()
            lable_group_detail_page.open_setting_menu()
            lable_group_detail_page.delete_lable_group()
            lable_group_detail_page.click_sure_delete()
            time.sleep(2)
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zhenyishan_0087(self):
        """通话模块：团队联系人选择页搜索栏--搜索本机号码"""
        # 消息界面进入到多方视频选择联系人界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_call_button()
        call_page = CallPage()
        call_page.wait_for_page_load()
        call_page.click_multi_party_video()
        # 搜索框输入本机号码
        call_page.input_video_search_text('15946309425')
        self.assertEqual(call_page.is_exist_number_grey(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_shenlisi_0390(self):
        """检查单聊会话窗口右上角电话按钮-普通电话拨打"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_add_icon()
        message_page.click_new_message()
        message_page.click_name_attribute_by_name('测试1')
        # 等待界面加载
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        single_chat_page.click_action_call()
        single_chat_page.click_name_attribute_by_name('普通电话')
        self.assertEqual(single_chat_page.page_should_contain_text2('呼叫'), True)
        single_chat_page.click_cancel()

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zhenyishan_0096(self):
        """通话模块：检查企业入口"""
        # 消息界面进入到多方视频选择联系人界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_call_button()
        call_page = CallPage()
        call_page.wait_for_page_load()
        call_page.click_multi_party_video()
        # 点击团队联系人进入我的团队
        call_page.click_name_attribute_by_name('团队联系人')
        call_page.click_name_attribute_by_name('ateam7272')
        self.assertEqual(call_page.is_exist_group_contact_search(), True)
        self.assertEqual(call_page.page_should_contain_text2('ateam7272'), True)
        self.assertEqual(call_page.page_should_contain_text2('大佬1'), True)
        # 点击团队看是否跳转到选择团队联系人界面
        call_page.click_name_attribute_by_name('ateam7272')
        self.assertEqual(call_page.page_should_contain_text2('选择联系人'), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zhenyishan_0112(self):
        """通话模块：当前勾选人数已有8人，继续勾选团队联系人，检查提示"""
        # 消息界面进入到多方视频选择联系人界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_call_button()
        call_page = CallPage()
        call_page.wait_for_page_load()
        call_page.click_multi_party_video()
        # 点击团队联系人进入我的团队
        call_page.click_name_attribute_by_name('团队联系人')
        call_page.click_name_attribute_by_name('ateam7272')
        call_page.click_name_attribute_by_name('alice')
        call_page.click_name_attribute_by_name('b测算')
        call_page.click_name_attribute_by_name('陈丹丹')
        call_page.click_name_attribute_by_name('c平5')
        call_page.click_name_attribute_by_name('大佬1')
        call_page.click_name_attribute_by_name('大佬2')
        call_page.click_name_attribute_by_name('大佬3')
        call_page.click_name_attribute_by_name('大佬4')
        call_page.click_name_attribute_by_name('郑海')
        # 判断是否出现人数已达上线8人
        self.assertEqual(call_page.page_should_contain_text2('人数已达上限8人'), True)
        call_page.click_name_attribute_by_name('确定')
        self.assertEqual(call_page.page_should_contain_text2('人数已达上限8人'), False)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zhenyishan_0158(self):
        """多方视频管理页面，检查免提按钮"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_mutilcall()
        group_chat_page.click_name_attribute_by_name('多方视频')
        multi_party_video_page = MultiPartyVideoPage()
        time.sleep(2)
        multi_party_video_page.click_name_attribute_by_name('大佬1')
        multi_party_video_page.click_call()
        time.sleep(5)
        multi_party_video_page.click_name_attribute_by_name('取消')
        multi_party_video_page.click_hands_free()

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zhenyishan_0159(self):
        """多方视频管理页面，静音按钮"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_mutilcall()
        group_chat_page.click_name_attribute_by_name('多方视频')
        multi_party_video_page = MultiPartyVideoPage()
        time.sleep(2)
        multi_party_video_page.click_name_attribute_by_name('大佬1')
        multi_party_video_page.click_call()
        time.sleep(5)
        multi_party_video_page.click_name_attribute_by_name('取消')
        multi_party_video_page.click_mute()

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zhenyishan_0183(self):
        """主叫多方视频管理界面，检查挂断按钮"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_mutilcall()
        group_chat_page.click_name_attribute_by_name('多方视频')
        multi_party_video_page = MultiPartyVideoPage()
        time.sleep(2)
        multi_party_video_page.click_name_attribute_by_name('大佬1')
        multi_party_video_page.click_call()
        time.sleep(5)
        multi_party_video_page.click_name_attribute_by_name('取消')
        # 点击红色挂断按钮
        multi_party_video_page.click_red_drop()
        multi_party_video_page.click_name_attribute_by_name('取消')
        multi_party_video_page.click_red_drop()
        multi_party_video_page.click_name_attribute_by_name('确定')
        time.sleep(3)
        group_chat_page.wait_for_page_load()

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zhenyishan_0186(self):
        """多方视频管理界面，检查添加联系人按钮"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_mutilcall()
        group_chat_page.click_name_attribute_by_name('多方视频')
        multi_party_video_page = MultiPartyVideoPage()
        time.sleep(2)
        multi_party_video_page.click_name_attribute_by_name('大佬1')
        multi_party_video_page.click_call()
        time.sleep(5)
        multi_party_video_page.click_name_attribute_by_name('取消')
        # 点击添加成员按钮
        multi_party_video_page.click_add_members()
        self.assertEqual(multi_party_video_page._is_enabled_call_button(), True)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_wangqiong_0059(self):
        """网络正常，通话页-多方电话悬浮，发起正常，发起正常"""
        # 消息界面进入到多方电话选择联系人界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_call_button()
        call_page = CallPage()
        call_page.wait_for_page_load()
        call_page.click_feixin_call()
        call_page.click_name_attribute_by_name('测试1')
        call_page.click_name_attribute_by_name('测试2')
        call_page.click_many_people_call()
        self.assertEqual(call_page.is_exist_stop_call_button(), True)
        time.sleep(2)
        # 挂断和飞信电话
        call_page.hang_up_hefeixin_call()

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_wangqiong_0057(self):
        """网络正常，拨号盘多方电话按钮，发起正常"""
        # 消息界面进入到多方电话选择联系人界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_call_button()
        call_page = CallPage()
        call_page.wait_for_page_load()
        call_page.click_dial_button()
        call_page.is_on_the_dial_pad()
        call_page.click_keyboard_feixin_call()
        call_page.click_name_attribute_by_name('测试1')
        call_page.click_name_attribute_by_name('测试2')
        call_page.click_many_people_call()
        self.assertEqual(call_page.is_exist_stop_call_button(), True)
        # 挂断飞信电话
        call_page.hang_up_hefeixin_call()


    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_wangqiong_0063(self):
        """网络正常，多方电话通话详情页可再次呼叫成功"""
        # 消息界面进入到多方电话选择联系人界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_call_button()
        call_page = CallPage()
        call_page.wait_for_page_load()
        call_page.click_dial_button()
        call_page.is_on_the_dial_pad()
        call_page.click_keyboard_feixin_call()
        call_page.click_name_attribute_by_name('测试1')
        call_page.click_name_attribute_by_name('测试2')
        call_page.click_many_people_call()
        call_page.hang_up_hefeixin_call()
        time.sleep(3)
        call_page.click_name_attribute_by_name('[飞信电话]')
        self.assertEqual(call_page.is_exist_stop_call_button(), True)
        # 挂断飞信电话
        call_page.hang_up_hefeixin_call()


    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_wangqiong_0073(self):
        """网络正常，消息+：分组群发-多方电话 ，拨打正常"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_contacts_only()
        # 联系界面
        contacts_page = ContactsPage()
        contacts_page.wait_for_page_load()
        contacts_page.click_mobile_contacts()
        contacts_page.click_label_grouping()
        LabelGroupingPage().delete_all_label()
        contacts_page.click_name_attribute_by_name('新建分组')
        contacts_page.click_name_attribute_by_name('为你的分组创建一个名称')
        lable_group_detail_page = LableGroupDetailPage()
        lable_group_detail_page.input_group_new_name('测试标签分组')
        lable_group_detail_page.click_sure()
        lable_group_detail_page.click_name_attribute_by_name('测试1')
        lable_group_detail_page.click_name_attribute_by_name('测试2')
        lable_group_detail_page.click_name_attribute_by_name('确定(2/200)')
        lable_group_detail_page.click_label_group_icon()
        # 进入标签分组
        lable_group_detail_page.wait_for_page_load()
        lable_group_detail_page.click_send_group_info()
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_mutilcall()
        group_chat_page.click_name_attribute_by_name('飞信电话(免费)')
        call_page = CallPage()
        call_page.click_name_attribute_by_name('测试1')
        call_page.click_name_attribute_by_name('测试2')
        call_page.click_many_people_call()
        self.assertEqual(call_page.is_exist_stop_call_button(), True)
        # 挂断飞信电话
        call_page.hang_up_hefeixin_call()


    @staticmethod
    def tearDown_test_call_wangqiong_0073():
        """恢复环境，将用例创建的标签删除"""
        try:
            Preconditions.make_already_in_message_page()
            message_page = MessagePage()
            message_page.wait_for_page_load()
            message_page.click_contacts_only()
            # 联系界面
            contacts_page = ContactsPage()
            contacts_page.wait_for_page_load()
            contacts_page.click_mobile_contacts()
            contacts_page.click_label_grouping()
            lable_group_detail_page = LableGroupDetailPage()
            lable_group_detail_page.click_label_group_icon()
            lable_group_detail_page.open_setting_menu()
            lable_group_detail_page.delete_lable_group()
            lable_group_detail_page.click_sure_delete()
            time.sleep(2)
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_wangqiong_0071(self):
        """网络正常，消息+：分组群发-多方电话 ，拨打正常"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_contacts_only()
        # 联系界面
        contacts_page = ContactsPage()
        contacts_page.wait_for_page_load()
        contacts_page.click_mobile_contacts()
        contacts_page.click_label_grouping()
        LabelGroupingPage().delete_all_label()
        contacts_page.click_name_attribute_by_name('新建分组')
        contacts_page.click_name_attribute_by_name('为你的分组创建一个名称')
        lable_group_detail_page = LableGroupDetailPage()
        lable_group_detail_page.input_group_new_name('测试标签分组')
        lable_group_detail_page.click_sure()
        lable_group_detail_page.click_name_attribute_by_name('测试1')
        lable_group_detail_page.click_name_attribute_by_name('测试2')
        lable_group_detail_page.click_name_attribute_by_name('确定(2/200)')
        lable_group_detail_page.click_label_group_icon()
        # 进入标签分组
        lable_group_detail_page.wait_for_page_load()
        lable_group_detail_page.click_multi_tel()
        call_page = CallPage()
        call_page.click_name_attribute_by_name('测试1')
        call_page.click_name_attribute_by_name('测试2')
        call_page.click_many_people_call()
        self.assertEqual(call_page.is_exist_stop_call_button(), True)
        # 挂断飞信电话
        call_page.hang_up_hefeixin_call()


    @staticmethod
    def tearDown_test_call_wangqiong_0071():
        """恢复环境，将用例创建的标签删除"""
        try:
            Preconditions.make_already_in_message_page()
            message_page = MessagePage()
            message_page.wait_for_page_load()
            message_page.click_contacts_only()
            # 联系界面
            contacts_page = ContactsPage()
            contacts_page.wait_for_page_load()
            contacts_page.click_mobile_contacts()
            contacts_page.click_label_grouping()
            lable_group_detail_page = LableGroupDetailPage()
            lable_group_detail_page.click_label_group_icon()
            lable_group_detail_page.open_setting_menu()
            lable_group_detail_page.delete_lable_group()
            lable_group_detail_page.click_sure_delete()
            time.sleep(2)
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zengxi_0028(self):
        """在拨号盘输入有效号码（手机号码、固号），可拨打普通电话成功"""
        # 消息界面进入到多方电话选择联系人界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_call_button()
        call_page = CallPage()
        call_page.wait_for_page_load()
        call_page.click_dial_button()
        call_page.dial_number('13333333333')
        call_page.click_call_phone()
        call_page.click_name_attribute_by_name('普通电话')
        self.assertEqual(call_page.page_should_contain_text2('呼叫'), True)
        call_page.click_name_attribute_by_name('取消')
        time.sleep(2)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zengxi_0034(self):
        """单聊会话-拨号，可发起呼叫普通电话"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_add_icon()
        message_page.click_new_message()
        message_page.click_name_attribute_by_name('测试1')
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        single_chat_page.click_action_call()
        single_chat_page.click_name_attribute_by_name('普通电话')
        self.assertEqual(single_chat_page.page_should_contain_text2('呼叫'), True)
        single_chat_page.click_name_attribute_by_name('取消')
        time.sleep(2)

    @tags('ALL', 'CMCC', 'ZHM')
    def test_call_zengxi_0035(self):
        """1V1的通话详情页入口，可发起呼叫普通电话"""
        # 消息界面进入到多方电话选择联系人界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_add_icon()
        message_page.click_new_message()
        message_page.click_name_attribute_by_name('测试1')
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        single_chat_page.click_add_button()
        single_chat_page.click_name_attribute_by_name('音视频通话')
        single_chat_page.click_name_attribute_by_name('视频通话')
        time.sleep(15)
        single_chat_page.click_back()
        message_page.wait_for_page_load()
        message_page.click_call_button()
        call_page = CallPage()
        call_page.click_name_attribute_by_name('刚刚')
        call_page.click_infor_call()
        self.assertEqual(call_page.page_should_contain_text2('呼叫'), True)
        call_page.click_name_attribute_by_name('取消')
        time.sleep(1)
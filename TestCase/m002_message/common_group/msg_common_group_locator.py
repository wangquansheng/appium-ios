import unittest
import time
import warnings
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from preconditions.BasePreconditions import LoginPreconditions,WorkbenchPreconditions
from library.core.utils.testcasefilter import tags
from pages.chat.chatfileProview import ChatfileProviewPage


from pages import *
from selenium.common.exceptions import TimeoutException

import re
import random
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from pages.contacts.AllMyTeam import AllMyTeamPage
from pages.contacts.my_group import ALLMyGroup


REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    # 'Android-移动': 'single_mobile',
    'IOS-移动': 'iphone',
    'IOS-移动-移动': 'M960BDQN229CHiphone8',
}


class Preconditions(WorkbenchPreconditions):
    """
    分解前置条件
    """
    @staticmethod
    def disconnect_mobile(category):
        """断开手机"""
        client = switch_to_mobile(category)
        client.disconnect_mobile()
        return client

    @staticmethod
    def make_sure_chatwindow_exist_locator_list():
        """确保我的电脑页面有位置记录"""
        chat=ChatWindowPage()
        time.sleep(2)
        if chat.is_element_present_locator_list():
            chat.wait_for_page_load()
        else:
            chat = ChatWindowPage()
            time.sleep(2)
            chat.click_more()
            chat.click_locator()
            time.sleep(2)
            # 选择位置界面
            locator = ChatLocationPage()
            locator.wait_for_page_load()
            locator.click_send()
            time.sleep(2)

    @staticmethod
    def send_locator():
        """聊天界面-发送位置"""
        chat = ChatWindowPage()
        chat.clear_all_chat_record()
        time.sleep(2)
        chat.click_more()
        chat.click_locator()
        time.sleep(2)
        # 选择位置界面
        locator = ChatLocationPage()
        locator.wait_for_page_load()
        locator.click_send()
        time.sleep(2)



class GroupChatLocator(TestCase):
    """群聊-位置"""

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

    @classmethod
    def default_setUp(self):
        """确保每个用例执行前在群聊聊天界面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg=MessagePage()
        name = '群聊1'
        if msg.is_text_present(name):
            msg.click_text(name)
        else:
            msg.open_contacts_page()
            ContactsPage().open_group_chat_list()
            my_group = ALLMyGroup()
            my_group.select_group_by_name(name)
            time.sleep(2)

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_qun_0312(self):
        """群聊（企业群/普通群）发送位置成功"""
        # 勾选位置
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_more()
        chat.click_locator()
        # 选择位置界面
        locator = ChatLocationPage()
        locator.wait_for_page_load()
        self.assertEqual(locator.is_on_this_page(), True)
        locator.click_send()
        # 3.发送成功
        time.sleep(2)
        self.assertEqual(chat.is_element_present_resend(), False)
        # 返回聊天列表查看
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        msg.wait_for_page_load()
        msg.page_should_contain_text('位置')

    @tags('ALL', 'msg', 'CMCC','common_group')
    def test_msg_weifenglian_qun_0336(self):
        """将自己发送的位置转发到手机联系人"""
        # 确保当前页面有地址记录
        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_locator_list()
        time.sleep(3)
        # 长按转发
        chat.press_and_move_right_locator()
        # 调起菜单判断
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        # 点击转发
        chat.click_forward()
        time.sleep(2)
        # 判断在选择联系人界面
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(),True)
        # 选择一个手机联系人
        select.select_local_contacts()
        local_contact=SelectLocalContactsPage()
        self.assertEqual(local_contact.is_on_this_page(),True)
        local_contact.swipe_select_one_member_by_name('大佬2')
        # 选择群后，弹起弹框
        time.sleep(2)
        local_contact.page_should_contain_text('取消')
        local_contact.page_should_contain_text('确定')
        local_contact.click_sure()
        time.sleep(2)
        # 返回到聊天界面
        self.assertEqual(chat.is_on_this_page(),True)


    @tags('ALL', 'msg', 'CMCC','common_group')
    def test_msg_weifenglian_qun_0349(self):
        """将自己发送的位置转发到团队未置灰的联系人"""
        # 确保当前页面有地址记录
        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_locator_list()
        time.sleep(3)
        # 长按转发
        chat.press_and_move_right_locator()
        # 调起菜单判断
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        # 点击转发
        chat.click_forward()
        time.sleep(2)
        # 判断在选择联系人界面
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(),True)
        # 选择一个团队未置灰的联系人
        select.click_he_contacts()
        group_contact=SelectHeContactsPage()
        group_contact.select_one_team_by_name('ateam7272')
        group_detail=SelectHeContactsDetailPage()
        group_detail.select_one_he_contact_by_name('alice')
        # 选择群后，弹起弹框
        time.sleep(2)
        group_detail.page_should_contain_text('取消')
        group_detail.page_should_contain_text('确定')
        group_detail.click_sure()
        time.sleep(2)
        # 返回到聊天界面
        self.assertEqual(chat.is_on_this_page(),True)

    @tags('ALL', 'msg', 'CMCC','common_group')
    def test_msg_weifenglian_qun_0369(self):
        """将自己发送的位置转发到我的电脑"""
        #确保当前页面有地址记录
        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_locator_list()
        time.sleep(3)
        # 长按转发
        chat.press_and_move_right_locator()
        #调起菜单判断
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        #点击转发
        chat.click_forward()
        time.sleep(2)
        #判断在选择联系人界面
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(),True)
        #选择一个搜索我的电脑
        select.click_search_contact()
        select.input_search_keyword('我的电脑')
        select.click_element_by_id(text='搜索结果列表1')
        #选择群后，弹起弹框
        time.sleep(2)
        select.page_should_contain_text('取消')
        select.page_should_contain_text('确定')
        select.click_sure_forward()
        time.sleep(2)
        #返回到聊天界面
        self.assertEqual(chat.is_on_this_page(),True)

    @tags('ALL', 'msg', 'CMCC','common_group')
    def test_msg_weifenglian_qun_0370(self):
        """将自己发送的位置转发到最近聊天联系人"""
        #确保当前页面有地址记录
        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_locator_list()
        time.sleep(3)
        # 长按转发
        chat.press_and_move_right_locator()
        #调起菜单判断
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        #点击转发
        chat.click_forward()
        time.sleep(2)
        #判断在选择联系人界面
        select=SelectContactsPage()
        self.assertEqual(select.is_on_this_page(),True)
        #选择最近聊天联系人
        select.click_recent_chat_contact()
        #选择群后，弹起弹框
        time.sleep(2)
        select.page_should_contain_text('取消')
        select.page_should_contain_text('确定')
        select.click_sure_forward()
        time.sleep(2)
        #返回到聊天界面
        self.assertEqual(chat.is_on_this_page(),True)

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_qun_0373(self):
        """对接收到的位置消息进行删除"""
        #确保当前页面有地址记录
        chat = ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_locator_list()
        time.sleep(3)
        # 长按转发
        chat.press_and_move_right_locator()
        #调起菜单判断
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        #点击删除
        chat.click_delete()
        time.sleep(2)
        chat.page_should_contain_text('取消')
        chat.page_should_contain_text('删除')
        chat.click_sure_delete()
        time.sleep(2)

    def setUp_test_msg_weifenglian_qun_0374(self):
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        msg = MessagePage()
        msg.delete_all_message_list()
        name = '群聊1'
        msg.click_search_box()
        time.sleep(1)
        msg.input_search_text(name)
        time.sleep(2)
        msg.click_element_first_list()
        time.sleep(2)

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_qun_0374(self):
        """对自己发送出去的位置消息进行十秒内撤回"""
        # 确保当前页面有地址记录
        chat = ChatWindowPage()
        Preconditions.send_locator()
        time.sleep(3)
        # 长按转发
        chat.press_and_move_right_locator()
        # 调起菜单判断
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='撤回')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        # 点击撤回
        chat.click_revoke()
        time.sleep(2)
        chat.click_i_know()
        time.sleep(2)
        chat.page_down()
        self.assertTrue(chat.is_element_present_by_locator(locator='你撤回了一条消息'))

    def tearDown_test_msg_weifenglian_qun_0374(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_qun_0375(self):
        """对自己发送出去的位置消息进行收藏"""
        # 确保当前页面有地址记录
        chat = ChatWindowPage()
        chat.send_locator()
        time.sleep(3)
        # 长按转发
        chat.press_and_move_right_locator()
        # 调起菜单判断
        time.sleep(2)
        chat.page_contain_element(locator='转发')
        chat.page_contain_element(locator='删除')
        chat.page_contain_element(locator='收藏')
        chat.page_contain_element(locator='多选')
        # 点击收藏
        chat.click_collection()
        time.sleep(2)
        # 返回收藏列表查看
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        me = MePage()
        me.click_collection()
        collection = MeCollectionPage()
        time.sleep(3)
        collection.page_should_contain_text('位置')
        collection.page_should_contain_text('广东省')

    @tags('ALL', 'msg', 'CMCC')
    def test_msg_weifenglian_qun_0312(self):
        """群聊（企业群/普通群）发送位置成功"""
        #勾选位置
        chat = ChatWindowPage()
        time.sleep(2)
        chat.click_more()
        chat.click_locator()
        #选择位置界面
        locator = ChatLocationPage()
        self.assertEqual(locator.is_on_this_page(),True)
        locator.click_send()
        #3.发送成功
        time.sleep(2)
        self.assertEqual(chat.is_element_present_resend(), False)
        # 返回聊天列表查看
        Preconditions.make_already_in_message_page()
        msg = MessagePage()
        msg.wait_for_page_load()
        msg.page_should_contain_text('位置')



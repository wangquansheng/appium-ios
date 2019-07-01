import time

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile
from pages import MessagePage
from pages import WorkbenchPage
from pages.workbench.attendance_card.AttendanceCard import AttendanceCardPage
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
    def enter_attendance_card_page():
        """进入考勤打卡首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_attendance_card()
        acp = AttendanceCardPage()
        # 确保已经加入考勤组
        if not acp.is_on_attendance_card_page():
            acp.click_accessibility_id_attribute_by_name("新建考勤组")
            # if acp.is_text_present("始终允许"):
            #     acp.click_text("始终允许")
            acp.click_name_attribute_by_name("请选择")
            acp.click_accessibility_id_attribute_by_name("全选")
            acp.click_name_attribute_by_name("确认")
            acp.click_create_attendance_group_button()
            time.sleep(2)
            acp.click_back()
            acp.wait_for_page_load()
            time.sleep(1)


class AttendanceCardAllTest(TestCase):

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在考勤打卡首页
        """

        Preconditions.select_mobile('IOS-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_attendance_card_page()
            return
        acp = AttendanceCardPage()
        if not acp.is_on_attendance_card_page():
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_attendance_card_page()

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_KQDK_0001(self):
        """帮助文档展示正常"""

        acp = AttendanceCardPage()
        acp.wait_for_page_load()
        # 点击“？”
        acp.click_help_icon()
        # 点击各个页面
        acp.click_accessibility_id_attribute_by_name("获取地址失败")
        # 1.每个帮助点击可正常跳转到对应页面，页面正常展示
        acp.wait_for_help_page_load("获取地址失败")
        acp.click_back2()
        acp.click_accessibility_id_attribute_by_name("定位不准确")
        acp.wait_for_help_page_load("定位不准确")
        acp.click_back2()
        acp.click_accessibility_id_attribute_by_name("提示不在考勤组")
        acp.wait_for_help_page_load("提示不在考勤组")
        acp.click_back2()
        time.sleep(1)
        acp.click_back2()
        # 等待考勤打卡首页加载
        acp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_KQDK_0006(self):
        """点击顶部返回键，返回到上一级页面"""

        acp = AttendanceCardPage()
        acp.wait_for_page_load()
        # 在任意页面点击顶部返回键【 < 】
        acp.click_back()
        wbp = WorkbenchPage()
        # 1.在首页返回到工作台页面
        wbp.wait_for_page_load()
        wbp.click_attendance_card()
        acp.wait_for_page_load()
        acp.click_help_icon()
        time.sleep(2)
        acp.click_back2()
        # 2.如果在应用其他页面，返回到上一级页面
        acp.wait_for_page_load()




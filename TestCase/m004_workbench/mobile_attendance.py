import time

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile
from pages import MessagePage
from pages import WorkbenchPage
from pages.workbench.mobile_attendance.MobileAttendance import MobileAttendancePage
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
    def enter_mobile_attendance_page():
        """进入移动出勤首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_mobile_attendance()


class MobileAttendanceAllTest(TestCase):

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在移动出勤首页
        """

        Preconditions.select_mobile('IOS-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_mobile_attendance_page()
            return
        map = MobileAttendancePage()
        if not map.is_on_mobile_attendance_page():
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_mobile_attendance_page()

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YDCQ_0001(self):
        """可正常进入应用"""

        map = MobileAttendancePage()
        # 1.等待移动出勤首页加载
        map.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YDCQ_0009(self):
        """点击顶部返回键"""

        map = MobileAttendancePage()
        # 等待移动出勤首页加载
        map.wait_for_page_load()
        # 移动出勤首页点击顶部【<】
        map.click_back_button()
        wbp = WorkbenchPage()
        # 1.等待工作台首页加载
        wbp.wait_for_page_load()
        wbp.click_mobile_attendance()
        map.wait_for_page_load()
        map.click_field_attendance()
        time.sleep(1)
        # 其他页面点击顶部【<】
        map.click_back_button()
        # 2.等待移动出勤首页加载
        map.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YDCQ_0010(self):
        """点击顶部关闭按钮"""

        map = MobileAttendancePage()
        # 等待移动出勤首页加载
        map.wait_for_page_load()
        map.click_field_attendance()
        # 点击顶部【x】
        map.click_close()
        wbp = WorkbenchPage()
        # 1.等待工作台首页加载
        wbp.wait_for_page_load()
        wbp.click_mobile_attendance()
        map.wait_for_page_load()
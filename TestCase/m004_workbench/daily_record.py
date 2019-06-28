import time

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile
from pages import MessagePage
from pages import WorkbenchPage
from pages.workbench.daily_record.DailyRecord import DailyRecordPage
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
    def enter_daily_record_page():
        """进入日志首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_daily_record()


class DailyRecordAllTest(TestCase):

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在日志首页
        """

        Preconditions.select_mobile('IOS-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_daily_record_page()
            return
        drp = DailyRecordPage()
        if not drp.is_on_daily_record_page():
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_daily_record_page()

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_RZ_0001(self):
        """验证点击返回按钮是否正确"""

        drp = DailyRecordPage()
        drp.wait_for_page_load()
        # 点击【<】返回
        drp.click_back_button()
        wbp = WorkbenchPage()
        # 1.返回到工作台
        wbp.wait_for_page_load()
        wbp.click_journal()
        # 等待日志首页加载
        drp.wait_for_page_load()

    # @tags('ALL', 'CMCC', 'workbench', 'LXD')
    # def test_RZ_0002(self):
    #     """新建日志"""
    #
    #     drp = DailyRecordPage()
    #     drp.wait_for_page_load()
    #     drp.click_journals()


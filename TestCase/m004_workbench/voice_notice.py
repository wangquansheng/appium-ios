import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import MessagePage
from pages.workbench.Workbench import WorkbenchPage
from pages.workbench.voice_notice.VoiceNotify import VoiceNotifyPage
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
    def enter_voice_notice_page():
        """进入语音通知首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_voice_notice()


class VoiceNoticeAllTest(TestCase):

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在语音通知首页
        """

        Preconditions.select_mobile('IOS-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_voice_notice_page()
            return
        vnp = VoiceNotifyPage()
        if not vnp.is_on_voice_notify_page():
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_voice_notice_page()

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYTZ_0001(self):
        """网络正常情况下正常跳转到应用首页"""

        vnp = VoiceNotifyPage()
        # 1.可正常跳转到语音通知首页
        vnp.wait_for_page_load()

from appium.webdriver.common.mobileby import MobileBy
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages import *


class GroupLogDetailPage(BasePage):
    """日志详情页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.EditGroupPageActivity'

    __locators = {
        '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
        '关闭': (MobileBy.ACCESSIBILITY_ID, 'cc h5 ic close'),
        #
        '输入标题': (MobileBy.XPATH, 'back'),
        '输入今日工作总结': (MobileBy.XPATH, 'back'),
        '输入明日工作计划': (MobileBy.XPATH, 'back'),
        '输入需要协调与帮助': (MobileBy.XPATH, 'back'),
        '输入备注': (MobileBy.XPATH, 'back'),
        '添加接收人': (MobileBy.XPATH, 'back'),
        '日志转聊天': (MobileBy.XPATH, 'back'),
        '分享至当前群': (MobileBy.XPATH, 'back'),
        '存草稿': (MobileBy.ACCESSIBILITY_ID, '存草稿'),
        '提交': (MobileBy.ACCESSIBILITY_ID, '提交'),


    }

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在审批"""

        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self.is_text_present('今日工作总结')
            )
            return True
        except:
            return False

    @TestLogger.log()
    def wait_for_page_load(self, timeout=15, auto_accept_alerts=True):
        """等待审批详情页面加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["输入标题"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log('判断页面存在元素')
    def is_exist_element(self, locator='关闭'):
        return self._is_element_present(self.__locators[locator])

    @TestLogger.log()
    def click_back(self, element='返回'):
        """点击返回"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_close_h5(self, element='关闭'):
        """点击关闭h5页面按钮"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_summary_of_work_today(self, element='输入今日工作总结'):
        """点击今日工作总结输入框"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def input_summary_of_work_today(self, text):
        """输入今日工作总结内容"""
        self.input_text(self.__class__.__locators['输入今日工作总结'], text)

    @TestLogger.log()
    def click_add_recipient(self, element='添加接收人'):
        """点击添加接收人"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def add_approver(self, name='大佬1'):
        """添加接收人"""
        self.click_add_recipient()
        time.sleep(2)
        SelectHeContactsDetailPage().select_one_he_contact_by_name(name)
        SelectHeContactsDetailPage().click_sure_icon()
        time.sleep(4)

    @TestLogger.log()
    def click_approval_change_to_chat(self):
        """点击审批转聊天"""
        self.click_element((MobileBy.IOS_PREDICATE, 'name CONTAINS "日志转聊天"'))
        time.sleep(3)

    @TestLogger.log()
    def click_share_to_group(self):
        """点击分享至当前群"""
        self.click_element((MobileBy.IOS_PREDICATE, 'name CONTAINS "分享至当前群"'))
        time.sleep(3)

    @TestLogger.log()
    def click_submit(self, element='提交'):
        """点击提交"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_save_as_draft(self, element='存草稿'):
        """点击存草稿"""
        self.click_element(self.__class__.__locators[element])


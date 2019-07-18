from appium.webdriver.common.mobileby import MobileBy
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages import *


class GroupChatApprovalDetail(BasePage):
    """群聊--审批-审批内容页面 """
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.EditGroupPageActivity'

    __locators = {
        '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
        '关闭': (MobileBy.ACCESSIBILITY_ID, 'cc h5 ic close'),
        '请输入申请内容': (MobileBy.IOS_PREDICATE, 'value == "请输入申请内容"'),
        '添加审批人': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="审批"]/XCUIElementTypeOther[4]/XCUIElementTypeOther[3]/XCUIElementTypeOther'),
        '添加抄送人': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="审批"]/XCUIElementTypeOther[7]/XCUIElementTypeOther/XCUIElementTypeOther'),
        '审批转聊天': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="审批"]/XCUIElementTypeOther[9]'),
        '分享至当前群': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="审批"]/XCUIElementTypeOther[10]'),
        '提交': (MobileBy.ACCESSIBILITY_ID, '提交'),

    }

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在审批"""

        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self.is_text_present('我的通用审批')
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
                condition=lambda d: self._is_element_present(self.__class__.__locators["请输入申请内容"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log('判断页面存在元素')
    def is_exist_element(self, locator='关闭'):
        if self._is_element_present(self.__locators[locator]):
            return True
        else:
            return False

    @TestLogger.log()
    def click_back(self, element='返回'):
        """点击返回"""
        self.click_element(self.__class__.__locators[element])


    @TestLogger.log()
    def click_close_h5(self, element='关闭'):
        """点击关闭h5页面按钮"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_input_application_detail(self, element='请输入申请内容'):
        """点击请输入申请内容"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def input_application_detail(self, text):
        """输入申请内容"""
        self.input_text(self.__class__.__locators['请输入申请内容'], text)

    @TestLogger.log()
    def click_add_approver(self, element='添加审批人'):
        """点击添加审批人"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def add_approver(self, name='大佬1'):
        """添加审批人"""
        self.click_add_approver()
        time.sleep(2)
        SelectHeContactsDetailPage().select_one_he_contact_by_name(name)
        SelectHeContactsDetailPage().click_sure_icon()
        time.sleep(2)

    @TestLogger.log()
    def click_approval_change_to_chat(self):
        """点击审批转聊天"""
        self.click_element((MobileBy.IOS_PREDICATE, 'name CONTAINS "审批转聊天"'))
        # self.click_element(self.__class__.__locators[element])
        time.sleep(3)

    @TestLogger.log()
    def click_share_to_group(self):
        """点击分享至当前群"""
        self.click_element((MobileBy.IOS_PREDICATE, 'name CONTAINS "分享至当前群"'))
        # self.click_element(self.__class__.__locators[element])
        time.sleep(3)

    @TestLogger.log()
    def click_submit(self, element='提交'):
        """点击提交"""
        self.click_element(self.__class__.__locators[element])

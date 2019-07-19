from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupChatApproval(BasePage):
    """群聊--审批 """
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.EditGroupPageActivity'

    __locators = {
        '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
        '问号': (MobileBy.ACCESSIBILITY_ID, 'cc call groupcall profile ic q'),
        '我审批的': (MobileBy.ACCESSIBILITY_ID, '我审批的'),
        '我审批的头像': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="审批"]/XCUIElementTypeOther[1]/XCUIElementTypeImage'),
        '我发起的': (MobileBy.ACCESSIBILITY_ID, '我发起的'),
        '我发起的头像': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="审批"]/XCUIElementTypeOther[3]/XCUIElementTypeImage'),
        '抄送我的': (MobileBy.ACCESSIBILITY_ID, '抄送我的'),
        '抄送我的头像': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="审批"]/XCUIElementTypeOther[5]/XCUIElementTypeImage'),
        '请假': (MobileBy.ACCESSIBILITY_ID, '请假'),
        '请假头像': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="审批"]/XCUIElementTypeOther[7]/XCUIElementTypeImage'),
        '加班': (MobileBy.ACCESSIBILITY_ID, '加班'),
        '加班头像': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="审批"]/XCUIElementTypeOther[9]/XCUIElementTypeImage'),
        '外出': (MobileBy.ACCESSIBILITY_ID, '外出'),
        '外出头像': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="审批"]/XCUIElementTypeOther[11]/XCUIElementTypeImage'),
        '出差': (MobileBy.ACCESSIBILITY_ID, '出差'),
        '出差头像': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="审批"]/XCUIElementTypeOther[13]/XCUIElementTypeImage'),
        '报销': (MobileBy.ACCESSIBILITY_ID, '报销'),
        '报销头像': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="审批"]/XCUIElementTypeOther[15]/XCUIElementTypeImage'),
        '备用金': (MobileBy.ACCESSIBILITY_ID, '备用金'),
        '备用金头像': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="审批"]/XCUIElementTypeOther[17]/XCUIElementTypeImage'),
        '用车': (MobileBy.ACCESSIBILITY_ID, '用车'),
        '用车头像': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="审批"]/XCUIElementTypeOther[19]/XCUIElementTypeImage'),
        '物品领用': (MobileBy.ACCESSIBILITY_ID, '物品领用'),
        '物品领用头像': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="审批"]/XCUIElementTypeOther[21]/XCUIElementTypeImage'),
        '采购': (MobileBy.ACCESSIBILITY_ID, '采购'),
        '采购头像': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="审批"]/XCUIElementTypeOther[23]/XCUIElementTypeImage'),
        '用章': (MobileBy.ACCESSIBILITY_ID, '用章'),
        '用章头像': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="审批"]/XCUIElementTypeOther[25]/XCUIElementTypeImage'),
        '通用审批': (MobileBy.ACCESSIBILITY_ID, '通用审批'),
        '通用审批头像': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="审批"]/XCUIElementTypeOther[27]/XCUIElementTypeImage'),
        # 审批问题与解答页面
        '关闭': (MobileBy.ACCESSIBILITY_ID, 'cc h5 ic close'),
        '': (MobileBy.ACCESSIBILITY_ID, ''),

    }


    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在审批"""

        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self.is_text_present('审批')
            )
            return True
        except:
            return False

    @TestLogger.log()
    def wait_for_page_load(self, timeout=15, auto_accept_alerts=True):
        """等待审批页面加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["请假"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log('判断页面存在元素')
    def is_exist_element(self, locator='问号'):
        if self._is_element_present(self.__locators[locator]):
            return True
        else:
            return False

    @TestLogger.log()
    def click_back(self, element='返回'):
        """点击返回"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_question_mark(self, element='问号'):
        """点击问号图标"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_close_h5(self, element='关闭'):
        """点击关闭h5页面按钮"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_ask_for_level(self, element='请假'):
        """点击请假"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_general_approval(self, element='通用审批'):
        """点击通用审批"""
        self.click_element(self.__class__.__locators[element])

    @TestLogger.log()
    def click_i_initiated_approval(self, element='我发起的'):
        """点击通用审批"""
        self.click_element(self.__class__.__locators[element])

import time

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from selenium.common.exceptions import TimeoutException


class MeCallMultiPage(BasePage):
    """我-》多方通话"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.MultiCallRechargeManageActivity'

    __locators = {'返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
                  '飞信电话管理': (MobileBy.ACCESSIBILITY_ID, '飞信电话管理'),
                  'Q&A': (MobileBy.ACCESSIBILITY_ID, 'cc_call_groupcall_profile_ic_question'),
                  '飞信电话可用时长': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]'),
                  '充值中心': (MobileBy.ACCESSIBILITY_ID, '充值中心'),
                  '使用攻略': (MobileBy.ACCESSIBILITY_ID, '使用攻略'),
                  '资费攻略': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="资费攻略"])[1]'),
                  #常见问题详情页面
                  '常见问题': (MobileBy.XPATH, '//XCUIElementTypeStaticText[@name="飞信电话-常见问题"]'),
                  '剩余时长': (MobileBy.ACCESSIBILITY_ID, '//XCUIElementTypeOther[@name="飞信电话-常见问题"]/XCUIElementTypeOther[1]'),
                  #时长详情页面
                  '时长详情': (MobileBy.ACCESSIBILITY_ID, '时长详情'),
                  '套餐详情': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]'),
                  '充值': (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="充值"])[1]'),
                  #充值中心
                  '查看充值记录': (MobileBy.ACCESSIBILITY_ID, '查看充值记录'),
                  '充值记录账单': (MobileBy.ACCESSIBILITY_ID, '充值记录账单'),
                  #使用攻略
                  '飞信电话使用攻略': (MobileBy.XPATH, '//XCUIElementTypeStaticText[@name="飞信电话使用攻略"]'),
                  '抢先体验飞信电话': (MobileBy.ACCESSIBILITY_ID, '抢先体验飞信电话'),
                  #资费攻略
                  '资费说明': (MobileBy.ACCESSIBILITY_ID, '资费说明'),
                  '资费说明详情': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="资费说明"]/XCUIElementTypeOther[1]'),


                  }


    @TestLogger.log("点击返回")
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators['返回'])


    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待卡片页面弹框加载 """
        try:
            time.sleep(5)
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["飞信电话可用时长"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log("检查该页面包含多个文本")
    def page_contain_text(self, menu):
        for text in menu:
            self.is_text_present(text)
        return True

    @TestLogger.log()
    def click_el_text(self, locator):
        """点击字段选项 """
        self.click_element(self.__locators[locator])

    @TestLogger.log()
    def page_contain_ele(self, locator):
        """该页面是否包含字段 """
        self.page_should_contain_element(self.__locators[locator])

    @TestLogger.log()
    def wait_for_page_load_call_questions(self, timeout=20, auto_accept_alerts=True):
        """等待多方电话FQA页面弹框加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators["常见问题"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_page_load_call_details(self, timeout=20, auto_accept_alerts=True):
        """等待多方电话时长详情页面弹框加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["套餐详情"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    # @TestLogger.log()
    # def wait_for_page_load_call_details_charge(self, text, timeout=20, auto_accept_alerts=True,):
    #     """等待多方电话时长详情页面弹框加载 """
    #     try:
    #         self.wait_until(
    #             timeout=timeout,
    #             auto_accept_permission_alert=auto_accept_alerts,
    #             condition=lambda d: self.is_text_present(text)
    #         )
    #     except:
    #         message = "页面在{}s内，没有加载成功".format(timeout)
    #         raise AssertionError(
    #             message
    #         )
    #     return self
    #
    # @TestLogger.log()
    # def wait_for_page_load_charge_center(self, timeout=8, auto_accept_alerts=True):
    #     """等待多方电话时长详情页面弹框加载 """
    #     try:
    #         self.wait_until(
    #             timeout=timeout,
    #             auto_accept_permission_alert=auto_accept_alerts,
    #             condition=lambda d: self.is_text_present("充值套餐")
    #         )
    #     except:
    #         message = "页面在{}s内，没有加载成功".format(timeout)
    #         raise AssertionError(
    #             message
    #         )
    #     return self

    @TestLogger.log()
    def ele_is_click(self, locator):
        """点击字段选项 """
        self.element_should_be_enabled(self.__locators[locator])


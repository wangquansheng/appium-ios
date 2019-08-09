from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MePayPage(BasePage):
    """和包支付页面"""

    __locators = {
        "和包支付授权": (MobileBy.XPATH, '(//XCUIElementTypeNavigationBar[@name="和包支付授权"])'),
        "确认授权": (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="确认授权"])'),
        "暂不授权": (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="暂不授权"])'),
        "和包余额": (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="和包余额"])'),
        "银行卡": (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="银行卡"])'),
        "现金红包": (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="现金红包"])'),
        "更多": (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="rb cash main more"])'),
        "和包支付": (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="和包支付"])'),
        "充值": (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="充值"])'),
        "提现": (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="提现"])'),
        "金额0": (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="￥0.00"])'),
        '帮助中心-返回': (MobileBy.ACCESSIBILITY_ID, 'red nav icon return normal'),
        "交易记录": (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="交易记录"])'),
        "支付管理": (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="支付管理"])'),
        "管理中心": (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="管理中心"])'),
        "帮助中心": (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="帮助中心"])'),
        "帮助中心页面": (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="帮助中心"])'),
        "取消": (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="取消"])'),
        "已收红包": (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="已收红包"])'),
        "已发红包": (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="已发红包"])'),
        "原和飞信零钱已合并至和包余额": (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="原和飞信零钱已合并至和包余额"])'),
        "绑定新银行卡": (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="绑定新银行卡"])'),
        '银行卡号': (MobileBy.IOS_PREDICATE, 'value == "银行卡号"'),
        "下一步": (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="下一步"])'),
        "您的银行卡号有误，请核对后重试": (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="您的银行卡号有误，请核对后重试"])'),
        "确定": (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="确定"])'),
        '持卡人姓名': (MobileBy.IOS_PREDICATE, 'value == "持卡人姓名"'),
        '银行预留身份证号': (MobileBy.IOS_PREDICATE, 'value == "银行预留身份证号"'),
        '银行预留手机号': (MobileBy.IOS_PREDICATE, 'value == "银行预留手机号"'),
        "勾选": (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="checkbox selected "])'),
        "快捷支付协议": (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="《快捷支付协议》"])'),
        "填写银行预留信息": (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="填写银行预留信息"])'),
        "填写银行卡号": (MobileBy.XPATH, '((//XCUIElementTypeStaticText[@name="填写银行卡号"])[1])'),
        "填写银行预留信息-返回": (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="pop l but 100"])'),
        "什么是实名认证": (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="1、什么是实名认证？"])'),
        "热点问题": (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="热点问题"])'),
        "协议内容": (MobileBy.XPATH, '(//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTextView)'),

    }

    @TestLogger.log()
    def is_on_payment_authorization_page(self):
        """判断是否在和包支付授权页面"""
        return self._is_element_present(self.__locators['和包支付授权'])

    @TestLogger.log()
    def click_sure_authorization(self):
        """点击确定授权"""
        self.click_element(self.__class__.__locators['确认授权'])

    @TestLogger.log()
    def click_cancel_authorization(self):
        """点击暂不授权"""
        self.click_element(self.__class__.__locators['暂不授权'])

    @TestLogger.log()
    def is_on_paymentn_page(self):
        """判断是否在和包支付页面"""
        return self._is_element_present(self.__locators['和包支付'])

    @TestLogger.log()
    def check_bank_card(self):
        """验证是否存在银行卡"""
        return self._is_element_present(self.__locators['银行卡'])

    @TestLogger.log()
    def check_cash_bonus(self):
        """判断是否列表开头"""
        return self._is_element_present(self.__locators['现金红包'])

    @TestLogger.log()
    def bank_card_btn_is_enabled(self):
        """银行卡按钮是否可点击"""
        return self._is_enabled(self.__class__.__locators["银行卡"])

    @TestLogger.log()
    def cash_bonus_btn_is_enabled(self):
        """现金红包按钮是否可点击"""
        return self._is_enabled(self.__class__.__locators["现金红包"])

    @TestLogger.log()
    def click_balance(self):
        """点击和包余额"""
        self.click_element(self.__class__.__locators['和包余额'])

    @TestLogger.log()
    def check_if_element_exist(self):
        """检查元素是否存在原和飞信零钱已合并至和包余额"""
        return self._is_element_present(self.__locators['原和飞信零钱已合并至和包余额'])

    @TestLogger.log()
    def check_if_balance_element_exist(self):
        """检查元素是否和包余额"""
        return self._is_element_present(self.__locators['原和飞信零钱已合并至和包余额'])

    @TestLogger.log()
    def click_cash_withdrawal(self):
        """点击提现"""
        self.click_element(self.__class__.__locators['提现'])

    @TestLogger.log()
    def click_bank_card(self):
        """点击银行卡"""
        self.click_element(self.__class__.__locators['银行卡'])

    @TestLogger.log()
    def is_exist_binding_new_bank_cards(self):
        """检查元素是否存在绑定新银行卡"""
        return self._is_element_present(self.__locators['绑定新银行卡'])

    @TestLogger.log()
    def click_binding_new_bank_cards(self):
        """点击绑定新银行"""
        self.click_element(self.__class__.__locators['绑定新银行卡'])

    @TestLogger.log()
    def click_input_box(self):
        """'点击输入框'"""
        self.click_element(self.__locators['银行卡号'])

    @TestLogger.log()
    def input_bank_card_number(self, number):
        """输入银行卡号"""
        self.input_text(self.__locators['银行卡号'], number)

    @TestLogger.log()
    def is_on_input_bank_card_page(self):
        """判断是否输入卡号页面"""
        return self._is_element_present(self.__locators['填写银行卡号'])

    @TestLogger.log()
    def next_step_btn_is_enabled(self):
        """下一步是否可点击"""
        return self._is_enabled(self.__class__.__locators["下一步"])

    @TestLogger.log()
    def click_next_step(self):
        """'点击下一步'"""
        self.click_element(self.__locators['下一步'])

    @TestLogger.log()
    def is_exist_error(self):
        """检查元素是否存在您的银行卡号有误，请核对后重试"""
        return self._is_element_present(self.__locators['您的银行卡号有误，请核对后重试'])

    @TestLogger.log()
    def input_name(self, name):
        """输入名字"""
        self.input_text(self.__locators['持卡人姓名'], name)

    @TestLogger.log()
    def input_ID_card(self, number):
        """输入身份证号"""
        self.input_text(self.__locators['银行预留身份证号'], number)

    @TestLogger.log()
    def input_phone_number(self, number):
        """输入银行预留手机号"""
        self.input_text(self.__locators['银行预留手机号'], number)

    @TestLogger.log()
    def click_checklist(self):
        """'点击取消勾选'"""
        self.click_element(self.__locators['勾选'])

    @TestLogger.log()
    def click_fast_payment_protocol(self):
        """'点击快捷支付协议'"""
        self.click_element(self.__locators['快捷支付协议'])

    @TestLogger.log()
    def is_exist_agreement_common(self):
        """是否存在协议内容"""
        return self._is_element_present(self.__locators['协议内容'])

    @TestLogger.log()
    def click_sure(self):
        """'点击确定'"""
        self.click_element(self.__locators['确定'])

    @TestLogger.log()
    def is_on_bank_reservation_page(self):
        """判断是否在银行预留信息页面"""
        return self._is_element_present(self.__locators['填写银行预留信息'])

    @TestLogger.log()
    def wait_for_pay_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待和包支付页面"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["银行卡"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_new_cards_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待绑定新银行卡"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["绑定新银行卡"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_bank_back(self):
        """'点击返回'"""
        self.click_element(self.__locators['填写银行预留信息-返回'])

    @TestLogger.log()
    def click_help(self):
        """'点击帮助中心'"""
        self.click_element(self.__locators['帮助中心'])

    @TestLogger.log()
    def click_more(self):
        """'点击更多'"""
        self.click_element(self.__locators['更多'])

    @TestLogger.log()
    def is_on_hotspot_issues_page(self):
        """判断是否在帮助中心热点问题页面"""
        return self._is_element_present(self.__locators['热点问题'])

    @TestLogger.log()
    def click_real_name_authentication(self):
        """'点击什么是实名认证'"""
        self.click_element(self.__locators['什么是实名认证'])

    @TestLogger.log()
    def click_help_back(self):
        """'点击帮助中心返回'"""
        self.click_element(self.__locators['帮助中心-返回'])
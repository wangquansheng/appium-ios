import time
from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class EnterpriseContactsPage(BasePage):
    """企业通讯录首页"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '企业通讯录标题': (MobileBy.XPATH, "//*[@name='back']/../following-sibling::*[1]/XCUIElementTypeOther/XCUIElementTypeStaticText"),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '返回上一级': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back'),
        '企业层级': (MobileBy.ID, "android:id/title"),
        '部门名称': (MobileBy.ID, "com.chinasofti.rcs:id/tv_title_department"),
        '部门图标': (MobileBy.IOS_PREDICATE, "name=='cc_contacts_organization_classA'"),
        '联系人名': (MobileBy.XPATH, '//*[@name="搜索"]/../following-sibling::*[2]/XCUIElementTypeCell/XCUIElementTypeStaticText[1]'),
        '联系人号码': (MobileBy.XPATH, '//*[@name="搜索"]/../following-sibling::*[2]/XCUIElementTypeCell/XCUIElementTypeStaticText[1]'),
        '联系人头像': (MobileBy.XPATH, '//*[@name="搜索"]/../following-sibling::*[2]/XCUIElementTypeCell/XCUIElementTypeImage[@name="cc_chat_personal_default"]'),
        '联系人所在部门': (MobileBy.XPATH, '//*[@name="搜索"]/../following-sibling::*[2]/XCUIElementTypeCell/XCUIElementTypeStaticText[1]/following-sibling::XCUIElementTypeStaticText[@name]'),
        '搜索框': (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeSearchField"'),
        '搜索输入框': (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeSearchField"'),
        '右上角三点': (MobileBy.ACCESSIBILITY_ID, 'cc chat more normal'),
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待企业通讯录首页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["企业通讯录标题"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def is_on_enterprise_contacts_page(self, timeout=20, auto_accept_alerts=True):
        """当前页面是否在企业通讯录首页"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["企业通讯录标题"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_return(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回上一级"])

    @TestLogger.log()
    def is_exist_corporate_grade(self):
        """是否存在企业层级"""
        return self._is_element_present(self.__class__.__locators['企业层级'])

    @TestLogger.log()
    def is_exists_three_points_icon(self):
        """是否存在右上角三点"""
        return self._is_element_present2(self.__class__.__locators["右上角三点"])

    @TestLogger.log()
    def click_three_points_icon(self):
        """点击右上角三点"""
        self.click_element(self.__class__.__locators["右上角三点"])

    @TestLogger.log()
    def is_exist_department_name(self):
        """是否存在部门/企业名称"""
        return self._is_element_present(self.__class__.__locators['部门名称'])

    @TestLogger.log()
    def is_exist_department_icon(self):
        """是否存在部门/企业图标"""
        return self._is_element_present(self.__class__.__locators['部门图标'])

    @TestLogger.log()
    def is_exist_department_by_name(self, name):
        """是否存在指定部门/企业名称"""
        locator = (
        MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_title_department" and @text="%s"]' % name)
        return self._is_element_present(locator)

    @TestLogger.log()
    def is_search_contacts_number_full_match(self, number):
        """搜索联系人号码是否精准匹配"""
        if self._is_element_present2(self.__class__.__locators["联系人号码"]):
            text = self.get_element(self.__class__.__locators["联系人号码"]).text
            if number == text[(text.rindex(" ") + 1):]:
                return True
            raise AssertionError('搜索结果"{}"没有找到与关键字"{}"完全匹配的号码'.format(text, number))
        else:
            raise AssertionError('找不到元素 {}'.format(number))

    @TestLogger.log()
    def is_search_contacts_number_match(self, number):
        """搜索联系人号码是否模糊匹配"""
        if self._is_element_present2(self.__class__.__locators["联系人号码"]):
            text = self.get_element(self.__class__.__locators["联系人号码"]).text
            if number in text[(text.rindex(" ") + 1):]:
                return True
            raise AssertionError('搜索结果"{}"没有找到包含关键字"{}"的号码'.format(text, number))
        else:
            raise AssertionError('找不到元素 {}'.format(number))

    @TestLogger.log()
    def is_search_contacts_name_full_match(self, name):
        """搜索联系人名是否精准匹配"""
        if self._is_element_present2(self.__class__.__locators["联系人名"]):
            text = self.get_element(self.__class__.__locators["联系人名"]).text
            if name == text[:text.rindex(" ")]:
                return True
            raise AssertionError('搜索结果"{}"没有找到与关键字"{}"完全匹配的文本'.format(text, name))
        else:
            raise AssertionError('找不到元素 {}'.format(name))

    @TestLogger.log()
    def is_search_contacts_name_match(self, name):
        """搜索联系人名是否模糊匹配"""
        if self._is_element_present2(self.__class__.__locators["联系人名"]):
            text = self.get_element(self.__class__.__locators["联系人名"]).text
            if name in text[:text.rindex(" ")]:
                return True
            raise AssertionError('搜索结果"{}"没有找到包含关键字"{}"的文本'.format(text, name))
        else:
            raise AssertionError('找不到元素 {}'.format(name))

    @TestLogger.log()
    def input_search_message(self, message):
        """输入查找信息"""
        self.input_text(self.__class__.__locators["搜索输入框"], message)

    @TestLogger.log()
    def click_search_box(self):
        """点击搜索框"""
        self.click_element(self.__class__.__locators["搜索框"])

    @TestLogger.log()
    def is_exists_contacts_image(self):
        """是否存在联系人头像"""
        return self._is_element_present2(self.__class__.__locators["联系人头像"])

    @TestLogger.log()
    def is_exists_contacts_name(self):
        """是否存在联系人名"""
        return self._is_element_present2(self.__class__.__locators["联系人名"])

    @TestLogger.log()
    def is_exists_contacts_number(self):
        """是否存在联系人号码"""
        return self._is_element_present2(self.__class__.__locators["联系人号码"])

    @TestLogger.log()
    def is_exists_contacts_department(self):
        """是否存在联系人部门"""
        return self._is_element_present2(self.__class__.__locators["联系人所在部门"])

    @TestLogger.log()
    def click_contacts_by_name(self, name):
        """选择指定联系人名"""
        self.click_accessibility_id_attribute_by_name(name)

    @TestLogger.log()
    def click_contacts_by_number(self, number):
        """选择指定联系人号码"""
        locator = (
            MobileBy.XPATH,
            '//*[@resource-id="com.chinasofti.rcs:id/tv_number_personal_contactlist" and contains(@text,"%s")]' % number)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)
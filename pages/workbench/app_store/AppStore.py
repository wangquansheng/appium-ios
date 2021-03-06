import time
from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class AppStorePage(BasePage):
    """应用商城首页"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '关闭': (MobileBy.ACCESSIBILITY_ID, 'cc h5 ic close'),
        '搜索应用': (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeTextField"'),
        '搜索框': (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeTextField"'),
        '搜索': (MobileBy.IOS_PREDICATE, 'name=="搜索"'),
        '添加': (MobileBy.IOS_PREDICATE, 'name=="添加"'),
        '打开': (MobileBy.IOS_PREDICATE, 'name=="打开"'),
        '确定': (MobileBy.IOS_PREDICATE, 'name=="确定"'),
        '热门推荐': (MobileBy.ACCESSIBILITY_ID, "热门推荐"),
        '个人专区': (MobileBy.IOS_PREDICATE, 'name=="个人专区"'),
        '添加应用': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="添加应用"])[2]'),
        '应用介绍': (MobileBy.IOS_PREDICATE, 'name=="应用介绍"'),
        'brenner图1': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="应用商城"]/XCUIElementTypeLink[5]/XCUIElementTypeImage'),
        'brenner图2': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="应用商城"]/XCUIElementTypeLink[6]/XCUIElementTypeImage'),
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待应用商城首页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["热门推荐"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def is_on_app_store_page(self, timeout=20, auto_accept_alerts=True):
        """当前页面是否在应用商城首页"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["热门推荐"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_close(self):
        """点击关闭"""
        self.click_element(self.__class__.__locators["关闭"])

    @TestLogger.log()
    def click_search_app(self):
        """点击搜索应用"""
        self.click_element(self.__class__.__locators["搜索应用"])

    @TestLogger.log()
    def input_store_name(self, name):
        """输入商店应用名称"""
        self.input_text(self.__class__.__locators["搜索框"], name)

    @TestLogger.log()
    def click_search(self):
        """点击搜索"""
        self.click_element(self.__class__.__locators["搜索"])

    @TestLogger.log()
    def is_exist_join(self):
        """是否存在添加"""
        return self._is_element_present(self.__class__.__locators["添加"])

    @TestLogger.log()
    def click_join(self):
        """点击添加"""
        self.click_element(self.__class__.__locators["添加"])

    @TestLogger.log()
    def click_open(self):
        """点击打开"""
        self.click_element(self.__class__.__locators["打开"])

    @TestLogger.log()
    def click_add_app(self):
        """点击添加应用"""
        self.click_element(self.__class__.__locators["添加应用"])

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log()
    def get_search_box_text(self):
        """获取搜索栏文本"""
        if self._is_element_present2(self.__class__.__locators["搜索框"]):
            el = self.get_element(self.__class__.__locators["搜索框"])
            return el.text

    @TestLogger.log()
    def is_search_result_match(self, name):
        """搜索结果是否匹配"""
        locator = (MobileBy.XPATH, '//XCUIElementTypeLink[@name="添加"]/following-sibling::*[1]')
        if self._is_element_present2(locator):
            text = self.get_element(locator).text
            if name in text:
                return True
            raise AssertionError('搜索结果"{}"没有找到包含关键字"{}"的文本'.format(text, name))

    @TestLogger.log()
    def click_search_result(self):
        """点击搜索结果"""
        locator = (MobileBy.XPATH, '//XCUIElementTypeLink[@name="添加"]/following-sibling::*[1]')
        self.click_element(locator)

    @TestLogger.log()
    def wait_for_search_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待搜索页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["搜索"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def wait_for_app_details_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待应用介绍详情页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["应用介绍"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def wait_for_app_group_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待应用分组页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["添加应用"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def wait_for_personal_area_page_load(self, timeout=30, auto_accept_alerts=True):
        """等待个人专区页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("政企优惠")
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def wait_for_classification_page_load(self, timeout=30, auto_accept_alerts=True):
        """等待分类页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("移动办公套件")
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_personal_area(self):
        """点击个人专区"""
        self.click_element(self.__class__.__locators["个人专区"])

    @TestLogger.log()
    def add_app_by_name(self, name, max_try=10):
        """添加指定应用"""
        locator = (MobileBy.XPATH, '//XCUIElementTypeLink[contains(@name,"%s")]/preceding-sibling::*[1]/XCUIElementTypeStaticText[@name="添加"]' % name)
        while max_try:
            if self._is_element_present2(locator):
                self.click_element(locator)
                return
            else:
                self.page_up()
                max_try -= 1

    @TestLogger.log()
    def get_app_button_text_by_name(self, name, max_try=10):
        """获取指定应用后的按钮文本"""
        locator = (MobileBy.XPATH,
                   '//XCUIElementTypeLink[contains(@name,"%s")]/preceding-sibling::*[1]/XCUIElementTypeStaticText' % name)
        while max_try:
            if self._is_element_present2(locator):
                return self.get_element(locator).text
            else:
                self.page_up()
                max_try -= 1

    @TestLogger.log()
    def click_app(self, name):
        """点击应用"""
        locator = (MobileBy.XPATH, "//XCUIElementTypeLink[contains(@name,'%s')]" % name)
        self.click_element(locator)

    @TestLogger.log()
    def swipe_by_brenner1(self):
        """滑动brenner图1"""
        self.swipe_by_direction(self.__class__.__locators["brenner图1"], "left")

    @TestLogger.log()
    def swipe_by_brenner2(self):
        """滑动brenner图2"""
        self.swipe_by_direction(self.__class__.__locators["brenner图2"], "right")

    @TestLogger.log()
    def click_brenner(self):
        """点击brenner图"""
        self.click_element(self.__class__.__locators["brenner图1"])

    @TestLogger.log()
    def click_text_by_name(self, name, max_try=3):
        """点击指定文本"""
        while max_try:
            if self._is_element_present2((MobileBy.IOS_PREDICATE, "name CONTAINS '%s'" % name)):
                self.click_name_attribute_by_name(name)
                return
            else:
                self.page_up()
                max_try -= 1
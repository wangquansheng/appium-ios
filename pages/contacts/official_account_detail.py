from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from .components.menu_more import MenuMore


class OfficialAccountDetailPage(MenuMore, BasePage):
    """公众号详情"""
    ACTIVITY = 'com.rcs.rcspublicaccount.PublicAccountDetailActivity'

    __locators = {
        '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
        '更多菜单': (MobileBy.ACCESSIBILITY_ID, 'cc chat more normal'),
        '公众号标题-和飞信新闻': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="和飞信新闻"])[1]'),
        '公众号名称-和飞信新闻': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="和飞信新闻"])[2]'),
        '公共账号：4011020490': (MobileBy.IOS_PREDICATE, 'name CONTAINS "公共账号:"'),
        '功能介绍': (MobileBy.ACCESSIBILITY_ID, '功能介绍'),
        '认证主体': (MobileBy.ACCESSIBILITY_ID, '认证主体'),
        '公众号头像': (MobileBy.IOS_PREDICATE, 'name CONTAINS "/var/mobile/Containers/Data/Application"'),
        '置顶公众号-关闭': (MobileBy.XPATH, '//XCUIElementTypeSwitch[@name="置顶公众号"]'),
        'com.chinasofti.rcs:id/ll_history_message': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_history_message'),
        '查看历史资讯': (MobileBy.ACCESSIBILITY_ID, '查看历史资讯'),
        '进入公众号': (MobileBy.ACCESSIBILITY_ID, '进入公众号'),
        '历史资讯': (MobileBy.XPATH, '//XCUIElementTypeCell/XCUIElementTypeStaticText'),
        '时间显示': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[4]/XCUIElementTypeImage'),
    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('点击打开更多菜单')
    def click_menu_more(self):
        self.click_element(self.__locators['更多菜单'])

    @TestLogger.log()
    def page_contain_public_name(self,):
        """页面应该包含的元素-公众号名称"""
        return self.page_should_contain_element(self.__locators['公众号名称-和飞信新闻'])

    @TestLogger.log()
    def page_contain_public_title_name(self,):
        """页面应该包含的元素-公众号名称"""
        return self.page_should_contain_element(self.__locators['公众号标题-和飞信新闻'])

    @TestLogger.log()
    def page_contain_public_header(self):
        """页面应该包含的元素-公众号头像"""
        return self.page_should_contain_element(self.__locators['公众号头像'])

    @TestLogger.log()
    def page_contain_public_number(self):
        """页面应该包含的元素-公共账号"""
        return self.page_should_contain_element(self.__locators['公共账号：4011020490'])

    @TestLogger.log()
    def page_contain_features(self):
        """页面应该包含的元素-功能介绍"""
        return self.page_should_contain_element(self.__locators['功能介绍'])

    @TestLogger.log()
    def page_contain_certification(self):
        """页面应该包含的元素-认证主体"""
        return self.page_should_contain_element(self.__locators['认证主体'])

    @TestLogger.log()
    def page_contain_read_more(self):
        """页面应该包含的元素-更多"""
        return self.page_should_contain_element(self.__locators['更多菜单'])

    @TestLogger.log('点击置顶公众号')
    def click_to_be_top(self):
        self.click_element(self.__locators['置顶公众号-关闭'])

    @TestLogger.log('点击查看历史资讯')
    def click_read_old_message(self):
        self.click_element(self.__locators['查看历史资讯'])

    def swipe_page_up(self):
        """向上滑动"""
        self.swipe_by_percent_on_screen(50, 70, 50, 50, 800)


    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待历史资讯页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["时间显示"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)
        return self

    @TestLogger.log()
    def page_contain_time(self):
        """页面应该包含的元素-时间"""
        try:
            pct=self.page_should_contain_element(self.__locators['时间显示'])
        except:
            self.swipe_page_up()
            pct=self.page_should_contain_element(self.__locators['时间显示'])
        return pct

    @TestLogger.log('点击进入公众号')
    def click_into_public(self):
        self.click_element(self.__locators['进入公众号'])

    @TestLogger.log('页面是否有历史资讯')
    def is_contain_old_mes(self):
        return self._is_element_present(self.__locators['历史资讯'])

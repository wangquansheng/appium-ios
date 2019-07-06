import time
from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class AnnouncementInformationPage(BasePage):
    """公告信息首页"""

    __locators = {
        '发布公告': (MobileBy.ACCESSIBILITY_ID, "发布公告"),
        '未发公告': (MobileBy.ACCESSIBILITY_ID, "未发公告"),
        '公告信息名称': (MobileBy.XPATH,
                 '//XCUIElementTypeOther/XCUIElementTypeLink[@name]/XCUIElementTypeLink/XCUIElementTypeStaticText'),
        '公告详情': (MobileBy.IOS_PREDICATE, 'name=="公告详情"'),
        '删除': (MobileBy.ACCESSIBILITY_ID, "删除"),
        '发布': (MobileBy.ACCESSIBILITY_ID, "发布"),
        '下线': (MobileBy.ACCESSIBILITY_ID, "下线"),
        '确定': (MobileBy.IOS_PREDICATE, 'name=="确定"'),
        '取消': (MobileBy.ACCESSIBILITY_ID, "取消"),
        '保存': (MobileBy.ACCESSIBILITY_ID, "保存"),
        '关闭': (MobileBy.ACCESSIBILITY_ID, 'cc h5 ic close'),
        '右上角搜索图标': (MobileBy.ACCESSIBILITY_ID, 'search'),
        '搜索框': (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeTextField"'),
        '搜索结果公告标题': (MobileBy.XPATH,
                 '//XCUIElementTypeTextField/following-sibling::*[2]/XCUIElementTypeLink/XCUIElementTypeStaticText'),
        '搜索结果创建公告人': (MobileBy.XPATH,
                     '//XCUIElementTypeTextField/following-sibling::*[3]/XCUIElementTypeStaticText[1]'),
        '搜索结果创建时间': (MobileBy.XPATH,
                      '//XCUIElementTypeTextField/following-sibling::*[3]/XCUIElementTypeStaticText[2]'),
        '搜索结果浏览人数': (MobileBy.XPATH,
                     '//XCUIElementTypeTextField/following-sibling::*[4]/XCUIElementTypeStaticText'),
        '浏览量': (MobileBy.XPATH,
                '//XCUIElementTypeLink/following-sibling::XCUIElementTypeOther[2]/XCUIElementTypeStaticText'),
        '图文发布标题输入框': (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeTextField"'),
        '图文发布内容输入框': (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeTextView"'),
        '链接发布': (MobileBy.IOS_PREDICATE, 'name=="链接发布"'),
        '链接发布标题输入框': (MobileBy.XPATH, '(//XCUIElementTypeTextField)[1]'),
        '链接发布网址输入框': (MobileBy.XPATH, '(//XCUIElementTypeTextField)[2]'),
        '公告详情页浏览量': (
            MobileBy.XPATH, '//XCUIElementTypeOther[@name="公告详情"]/XCUIElementTypeOther[3]/XCUIElementTypeStaticText'),
    }

    @TestLogger.log()
    def is_on_announcement_information_page(self, timeout=20, auto_accept_alerts=True):
        """当前页面是否在公告信息首页"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["发布公告"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待公告信息首页加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["发布公告"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def wait_for_detail_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待公告信息详情页加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["公告详情"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def clear_announcement_information(self):
        """清空公告信息"""
        current = 0
        while self._is_element_present2(self.__class__.__locators["公告信息名称"]):
            current += 1
            if current > 20:
                return
            el = self.get_element(self.__class__.__locators["公告信息名称"])
            el.click()
            self.wait_for_detail_page_load()
            self.click_offline()
            self.click_sure()
            self.wait_for_page_load()

    @TestLogger.log()
    def click_offline(self):
        """点击下线"""
        self.click_element(self.__class__.__locators["下线"])

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log()
    def click_cancel(self):
        """点击取消"""
        self.click_element(self.__class__.__locators["取消"])

    @TestLogger.log()
    def click_release(self):
        """点击发布"""
        self.click_element(self.__class__.__locators["发布"])

    @TestLogger.log()
    def click_delete(self):
        """点击删除"""
        self.click_element(self.__class__.__locators["删除"])

    @TestLogger.log()
    def click_save(self):
        """点击保存"""
        self.click_element(self.__class__.__locators["保存"])

    @TestLogger.log()
    def click_close(self):
        """点击关闭"""
        self.click_element(self.__class__.__locators["关闭"])

    @TestLogger.log()
    def click_release_announcement(self):
        """点击发布公告"""
        self.click_element(self.__class__.__locators["发布公告"])

    @TestLogger.log()
    def click_no_announcement(self):
        """点击未发公告"""
        self.click_element(self.__class__.__locators["未发公告"])

    @TestLogger.log()
    def is_exist_release_announcement_button(self):
        """是否存在发布公告按钮"""
        return self._is_element_present2(self.__class__.__locators["发布公告"])

    @TestLogger.log()
    def is_exist_no_announcement_button(self):
        """是否存在未发公告按钮"""
        return self._is_element_present2(self.__class__.__locators["未发公告"])

    @TestLogger.log()
    def click_search_icon(self):
        """点击右上角搜索图标"""
        self.click_element(self.__class__.__locators["右上角搜索图标"])

    @TestLogger.log()
    def click_search_box(self):
        """点击搜索框"""
        self.click_element(self.__class__.__locators["搜索框"])

    @TestLogger.log()
    def input_search_message(self, text):
        """输入搜索内容"""
        self.input_text(self.__class__.__locators["搜索框"], text)

    @TestLogger.log()
    def is_search_message_full_match(self, name):
        """搜索公告信息是否精准匹配"""
        if self._is_element_present2(self.__class__.__locators["搜索结果公告标题"]):
            text = self.get_element(self.__class__.__locators["搜索结果公告标题"]).text
            if name == text:
                return True
            raise AssertionError('搜索结果"{}"没有找到与关键字"{}"完全匹配的文本'.format(text, name))
        else:
            raise AssertionError('找不到元素 {}'.format(name))

    @TestLogger.log()
    def is_exist_close_button(self):
        """是否存在关闭按钮"""
        return self._is_element_present2(self.__class__.__locators["关闭"])

    @TestLogger.log()
    def wait_for_image_release_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待发布公告-图文发布页加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["图文发布内容输入框"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def wait_for_link_release_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待发布公告-链接发布页加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["链接发布网址输入框"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def input_search_message(self, text):
        """输入搜索内容"""
        self.input_text(self.__class__.__locators["搜索框"], text)

    @TestLogger.log()
    def input_announcement_image_title(self, title):
        """输入图文公告标题"""
        self.input_text(self.__class__.__locators["图文发布标题输入框"], title)

    @TestLogger.log()
    def input_announcement_image_content(self, content):
        """输入图文公告内容"""
        self.input_text(self.__class__.__locators["图文发布内容输入框"], content)

    @TestLogger.log()
    def input_announcement_link_title(self, title):
        """输入链接公告标题"""
        self.input_text(self.__class__.__locators["链接发布标题输入框"], title)

    @TestLogger.log()
    def input_announcement_link_url(self, url):
        """输入链接公告网址"""
        self.input_text(self.__class__.__locators["链接发布网址输入框"], url)

    @TestLogger.log()
    def get_announcement_information_titles(self):
        """获取公告信息标题"""
        if self._is_element_present2(self.__class__.__locators["公告信息名称"]):
            els = self.get_elements(self.__class__.__locators["公告信息名称"])
            titles = []
            for el in els:
                title = el.text
                titles.insert(0, title)
            return titles

    @TestLogger.log()
    def is_exists_announcement_title(self):
        """搜索结果是否存在公告标题"""
        return self._is_element_present2(self.__class__.__locators["搜索结果公告标题"])

    @TestLogger.log()
    def is_exists_create_announcer(self):
        """搜索结果是否存在创建公告人"""
        return self._is_element_present2(self.__class__.__locators["搜索结果创建公告人"])

    @TestLogger.log()
    def is_exists_create_time(self):
        """搜索结果是否存在创建时间"""
        return self._is_element_present2(self.__class__.__locators["搜索结果创建时间"])

    @TestLogger.log()
    def is_exists_visitors(self):
        """搜索结果是否存在浏览人数"""
        return self._is_element_present2(self.__class__.__locators["搜索结果浏览人数"])

    @TestLogger.log()
    def click_link_publishing(self):
        """点击链接发布"""
        self.click_element(self.__class__.__locators["链接发布"])

    @TestLogger.log()
    def is_exist_announcement_information(self):
        """是否存在公告信息"""
        return self._is_element_present2(self.__class__.__locators["公告信息名称"])

    @TestLogger.log()
    def click_announcement_by_number(self, number):
        """点击某一条公告"""
        if self._is_element_present2(self.__class__.__locators["浏览量"]):
            els = self.get_elements(self.__class__.__locators["浏览量"])
            els[number].click()

    @TestLogger.log()
    def get_announcement_view_by_number(self, number):
        """返回某一条公告浏览量"""
        if self._is_element_present2(self.__class__.__locators["浏览量"]):
            els = self.get_elements(self.__class__.__locators["浏览量"])
            amount = els[number].text
            return int(amount)

    @TestLogger.log()
    def get_announcement_detail_view(self):
        """返回某一条公告详情页浏览量"""
        if self._is_element_present2(self.__class__.__locators["公告详情页浏览量"]):
            el = self.get_element(self.__class__.__locators["公告详情页浏览量"])
            amount = el.text
            return int(amount)
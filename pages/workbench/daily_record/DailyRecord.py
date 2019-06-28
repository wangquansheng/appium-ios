from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class DailyRecordPage(BasePage):
    """日志首页"""

    __locators = {
        '写日志': (MobileBy.ACCESSIBILITY_ID, '写日志'),
        '日报': (MobileBy.ACCESSIBILITY_ID, '日报'),
        '提交': (MobileBy.ACCESSIBILITY_ID, '提交'),
        '标题输入框': (MobileBy.XPATH, '//*[@name="标题"]/../following-sibling::*[1]'),
        '今日工作总结输入框': (MobileBy.XPATH, '//*[@name="今日工作总结"]/../following-sibling::*[1]'),
        '明日工作计划输入框': (MobileBy.XPATH, '//*[@name="明日工作计划"]/../following-sibling::*[1]'),
        '需要协调与帮助输入框': (MobileBy.XPATH, '//*[@name="需要协调与帮助"]/../following-sibling::*[1]'),
        '备注输入框': (MobileBy.XPATH, '//*[@name="备注"]/../following-sibling::*[1]'),
        '+号': (MobileBy.ACCESSIBILITY_ID, '+'),
        '添加上次联系人': (MobileBy.IOS_PREDICATE, 'name=="添加上次联系人"'),
        '存草稿': (MobileBy.ACCESSIBILITY_ID, '存草稿'),
        '确定': (MobileBy.ACCESSIBILITY_ID, '确定'),
        '删除': (MobileBy.ACCESSIBILITY_ID, '删除'),
        '更多': (MobileBy.ACCESSIBILITY_ID, 'cc chat more normal'),
        '点赞图标': (MobileBy.XPATH, '(//XCUIElementTypeImage)[last()]'),
        '评论图标': (MobileBy.XPATH, '(//XCUIElementTypeImage)[last()]/../following-sibling::*[1]'),
        '发布': (MobileBy.ACCESSIBILITY_ID, '发布'),
        '评论输入框': (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeTextView"'),
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待日志首页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["写日志"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def is_on_daily_record_page(self, timeout=20, auto_accept_alerts=True):
        """当前页面是否在日志首页"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["写日志"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_journals(self):
        """点击写日志"""
        self.click_element(self.__class__.__locators["写日志"])

    @TestLogger.log()
    def click_daily_paper(self):
        """点击日报"""
        self.click_element(self.__class__.__locators["日报"])

    @TestLogger.log()
    def click_submit(self):
        """点击提交"""
        self.click_element(self.__class__.__locators["提交"])

    @TestLogger.log()
    def wait_log_editor_page_load(self, timeout=30, auto_accept_alerts=True):
        """等待日志编辑页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["提交"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def wait_log_overview_page_load(self, timeout=30, auto_accept_alerts=True):
        """等待日志概览页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["更多"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def input_title(self, text):
        """输入标题"""
        self.input_text(self.__class__.__locators["标题输入框"], text)

    @TestLogger.log()
    def input_work_summary(self, text):
        """输入工作总结"""
        self.input_text(self.__class__.__locators["今日工作总结输入框"], text)

    @TestLogger.log()
    def input_work_plan(self, text):
        """输入工作计划"""
        self.input_text(self.__class__.__locators["明日工作计划输入框"], text)

    @TestLogger.log()
    def input_coordinate_and_help(self, text):
        """输入协调与帮助"""
        self.input_text(self.__class__.__locators["需要协调与帮助输入框"], text)

    @TestLogger.log()
    def input_remarks(self, text):
        """输入备注"""
        self.input_text(self.__class__.__locators["备注输入框"], text)

    @TestLogger.log()
    def click_add_icon(self):
        """点击+号图标"""
        self.click_element(self.__class__.__locators["+号"])

    @TestLogger.log()
    def click_add_last_contact(self):
        """点击添加上次联系人"""
        self.click_element(self.__class__.__locators["添加上次联系人"])

    @TestLogger.log()
    def click_save_draft(self):
        """点击存草稿"""
        self.click_element(self.__class__.__locators["存草稿"])

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log()
    def click_delete(self):
        """点击删除"""
        self.click_element(self.__class__.__locators["删除"])

    @TestLogger.log()
    def click_love_icon(self):
        """点击点赞图标"""
        self.click_element(self.__class__.__locators["点赞图标"])

    @TestLogger.log()
    def click_comment_icon(self):
        """点击评论图标"""
        self.click_element(self.__class__.__locators["评论图标"])

    @TestLogger.log()
    def click_release(self):
        """点击发布"""
        self.click_element(self.__class__.__locators["发布"])

    @TestLogger.log()
    def input_comment(self, text):
        """输入评论"""
        self.input_text(self.__class__.__locators["评论输入框"], text)

    @TestLogger.log()
    def get_log_editor_name(self):
        """获取日报编辑人名字"""
        locator = (MobileBy.XPATH, "//*[@name='日志']/XCUIElementTypeOther[2]/XCUIElementTypeStaticText")
        if self._is_element_present2(locator):
            el = self.get_element(locator)
            return el.text
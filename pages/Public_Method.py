from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class PublicMethodBase(BasePage):

    @TestLogger.log("ios-通过ios-—predicate属性点击元素")
    def public_click_element_by_PREDICATE(self, attribute, operator, string):
        self.click_element((MobileBy.IOS_PREDICATE, "{} {} '{}'".format(attribute, operator, string)))

    @TestLogger.log("ios-通过ios-—predicate属性寻找元素")
    def public_find_element_by_PREDICATE(self, attribute, operator, string):
        return self.wait_until(
                condition=lambda x: self.get_element(
                    (MobileBy.IOS_PREDICATE, "{} {} '{}'".format(attribute, operator, string))),
                auto_accept_permission_alert=False
            )

    @TestLogger.log("ios-通过ios-—predicate属性寻找多个元素")
    def public_find_elements_by_PREDICATE(self, attribute, operator, string, index=None):
        elements = self.wait_until(
                condition=lambda x: self.get_elements(
                    (MobileBy.IOS_PREDICATE, "{} {} '{}'".format(attribute, operator, string))),
                auto_accept_permission_alert=False
            )
        if index is None:
            return elements
        else:
            return elements[index]


class PublicMethod(PublicMethodBase):

    @TestLogger.log("ios-点击发送")
    def public_click_send(self):
        self.public_click_attribute_by_name('发送')

    @TestLogger.log("ios-点击取消")
    def public_click_cancel(self):
        self.public_click_attribute_by_name('取消')

    @TestLogger.log("ios-点击返回")
    def public_click_back(self):
        self.public_click_attribute_by_name('back')

    @TestLogger.log("ios-点击确定")
    def public_click_sure(self):
        self.public_click_attribute_by_name('确定')

    @TestLogger.log("ios-点击确定(页面有多个确定)")
    def public_click_sure_icon(self, n=2):
        self.click_element((MobileBy.XPATH, '(//XCUIElementTypeButton[@name="确定"])[%s]' % n))

    @TestLogger.log("ios-点击name属性")
    def public_click_attribute_by_name(self, string):
        self.public_click_attribute_equal_text('name', string)

    @TestLogger.log("ios-点击label属性")
    def public_click_attribute_by_label(self, string):
        self.public_click_attribute_equal_text('lable', string)

    @TestLogger.log("ios-点击value属性")
    def public_click_attribute_by_value(self, string):
        self.public_click_attribute_equal_text('value', string)

    @TestLogger.log("ios-点击type属性")
    def public_click_attribute_by_type(self, string):
        self.public_click_attribute_equal_text('type', string)

    @TestLogger.log("ios-点击包含text的元素,默认name元素")
    def public_click_attribute_equal_text(self, attribute, text):
        self.public_click_element_by_PREDICATE(attribute, '==', text)

    @TestLogger.log("ios-点击包含text的元素,默认name元素")
    def public_click_attribute_contains_text(self, attribute, text):
        self.public_click_element_by_PREDICATE(attribute, 'CONTAINS', text)

    @TestLogger.log("ios-点击结尾为text的元素,默认name元素")
    def public_click_attribute_endswith_text(self, attribute, text):
        self.public_click_element_by_PREDICATE(attribute, 'ENDSWITH', text)

    @TestLogger.log("寻找元素以name属性结尾")
    def public_find_element_by_attribute_endswith(self, text):
        try:
            self.public_find_element_by_PREDICATE('name', 'ENDSWITH', text)
            return True
        except:
            return False

    @TestLogger.log("寻找元素与name相同属性元素，可做判断页面")
    def public_is_on_this_page_by_element_attribute(self, text):
        try:
            self.public_find_elements_by_PREDICATE('name', '==', text)
            return True
        except:
            return False
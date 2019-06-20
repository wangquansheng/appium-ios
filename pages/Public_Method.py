from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class PublicMethod(BasePage):

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

    @TestLogger.log("ios-点击name属性")
    def public_click_attribute_by_name(self, name):
        self.click_element((MobileBy.IOS_PREDICATE, "name == '{}'".format(name)))

    @TestLogger.log("ios-点击label属性")
    def public_click_attribute_by_label(self, label):
        self.click_element((MobileBy.IOS_PREDICATE, "label == '{}'".format(label)))

    @TestLogger.log("ios-点击value属性")
    def public_click_attribute_by_value(self, value):
        self.click_element((MobileBy.IOS_PREDICATE, "value == '{}'".format(value)))

    @TestLogger.log("ios-点击包含text的元素,默认name元素")
    def public_click_attribute_contains_text(self, text, attribute='name'):
        self.click_element((MobileBy.IOS_PREDICATE, "{} CONTAINS '{}'".format(attribute, text)))

    @TestLogger.log("ios-点击结尾为text的元素,默认name元素")
    def public_click_attribute_endswith_text(self, text, attribute='name'):
        self.click_element((MobileBy.IOS_PREDICATE, "{} ENDSWITH '{}'".format(attribute, text)))
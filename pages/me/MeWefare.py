from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MeSetWefarePage(BasePage):
    """我-》福利"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.MultiLanguageSettingActivity'

    __locators = {
                  '': (MobileBy.ID, ''),
                  '福利': (MobileBy.XPATH, '//XCUIElementTypeStaticText[@name="福利"]'),
                  '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
                  '福利详情第一个banaer': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="福利"]/XCUIElementTypeOther[1]'),
                  # 打开福利活动也
                  '关闭h5页面': (MobileBy.ACCESSIBILITY_ID, 'cc h5 ic close'),
                  '更多': (MobileBy.ACCESSIBILITY_ID, 'cc chat more normal'),
                  '转发给朋友': (MobileBy.ACCESSIBILITY_ID, "hfx_share_transmit_friend"),
                  '转发给微信好友': (MobileBy.ACCESSIBILITY_ID, "hfx_share_wechat"),
                  '转发到朋友圈': (MobileBy.ACCESSIBILITY_ID, "hfx_share_circle"),
                  '转发到qq好友': (MobileBy.ACCESSIBILITY_ID, "hfx_share_qq"),
                  '在Safari中打开': (MobileBy.ACCESSIBILITY_ID, "hfx_share_safari"),
                  '复制链接': (MobileBy.ACCESSIBILITY_ID, "hfx_share_copylink"),
                  '刷新': (MobileBy.ACCESSIBILITY_ID, "hfx_share_refresh"),
                  '取消': (MobileBy.ACCESSIBILITY_ID, "取消"),
                  # '刷新': (MobileBy.ACCESSIBILITY_ID, "hfx_share_refresh"),

                  }

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__locators["返回"])

    @TestLogger.log()
    def page_contain_element(self,text='返回'):
        """页面应该包含的元素"""
        self.page_should_contain_element(self.__locators[text])

    @TestLogger.log()
    def click_first_banaer(self):
        """点击第一个banaer"""
        self.click_element(self.__locators["福利详情第一个banaer"])


    @TestLogger.log()
    def click_close_welfare_activities(self):
        """点击关闭福利活动"""
        self.click_element(self.__locators["关闭h5页面"])

    @TestLogger.log()
    def click_more(self):
        """点击更多操作"""
        self.click_element(self.__locators["更多"])

    @TestLogger.log()
    def click_share_friend(self):
        """点击转发给朋友"""
        self.click_element(self.__locators["转发给朋友"])

    @TestLogger.log()
    def click_open_browser(self):
        """点击在浏览器中打开"""
        self.click_element(self.__locators["在系统浏览器中打开"])

    @TestLogger.log()
    def click_copy_link(self):
        """点击在浏览器中打开"""
        self.click_element(self.__locators["复制链接"])

    @TestLogger.log()
    def click_refurbish(self):
        """点击在浏览器中打开"""
        self.click_element(self.__locators["刷新"])

    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待福利详情页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators['福利详情第一个banaer'])
            )
        except:
            message = "我的福利：{}s内没有加载完毕，或者没有包含文本：设置语言".format(timeout)
            raise AssertionError(
                message
            )
        return self

    def wait_for_page_load_banaer_detail(self, timeout=20, auto_accept_alerts=True):
        """等待banaer详情页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators['更多'])
            )
        except:
            message = "我的福利：{}s内没有加载完毕，或者没有包含文本：设置语言".format(timeout)
            raise AssertionError(
                message
            )
        return self


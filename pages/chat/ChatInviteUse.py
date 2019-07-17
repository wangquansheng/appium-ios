from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatInvitationUse(BasePage):
    """聊天页面--邀请使用页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.EditGroupPageActivity'

    __locators = {
        '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
        '未使用成员': (MobileBy.ACCESSIBILITY_ID, '未使用成员'),
        '一键邀请': (MobileBy.ACCESSIBILITY_ID, '一键邀请'),
        '成员头像': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeImage'),
        '': (MobileBy.ACCESSIBILITY_ID, ''),

        '': (MobileBy.ACCESSIBILITY_ID, ''),

        # 再次邀请页面
        '再次邀请': (MobileBy.ACCESSIBILITY_ID, '再次邀请'),

    }

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在通讯录"""

        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["未使用成员"])
            )
            return True
        except:
            return False

    @TestLogger.log("点击返回")
    def click_back(self, text='返回'):
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log('判断页面存在元素')
    def is_exist_element(self, locator='未使用成员'):
        if self._is_element_present(self.__locators[locator]):
            return True
        else:
            return False

    @TestLogger.log("点击一键邀请")
    def click_one_key_use(self, text='一键邀请'):
        self.click_element(self.__class__.__locators[text])

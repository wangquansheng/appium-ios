from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class CreateGroupNamePage(BasePage):
    """创建群聊名称页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.EditGroupPageActivity'

    __locators = {
        #创建群聊
        '清除文本': (MobileBy.ACCESSIBILITY_ID, '清除文本'),
        '请输入群聊名称': (MobileBy.IOS_PREDICATE, 'value CONTAINS "请输入群聊名称"'),
        '创建': (MobileBy.ACCESSIBILITY_ID, '创建'),

    }

    @TestLogger.log()
    def input_group_name(self, group_name):
        """输入群聊名称"""
        self.input_text(self.__locators['请输入群聊名称'], group_name)

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log('点击清除群组名称')
    def click_clear_group_name(self):
        self.click_element(self.__locators['清除文本'])

    @TestLogger.log('点击创建')
    def click_sure_creat(self):
        self.click_element(self.__locators['创建'])

    @TestLogger.log('通过名称判断群聊是否存在')
    def is_exist_group_by_name(self, name='群聊1'):
        locator = (MobileBy.ACCESSIBILITY_ID, '%s' % name)
        return self._is_element_present(locator)



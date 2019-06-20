from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time

class SelectHeContactsPage(BasePage):
    """选择和通讯录页面"""
    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterPriseContactSelectActivity'

    __locators = {
        '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
        '选择联系人': (MobileBy.ACCESSIBILITY_ID, '选择联系人'),
        '搜索或输入手机号': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeTextField'),
        '团队列表': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell'),
        '团队列表-第一个': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]'),
        '团队头像-第一个': (MobileBy.XPATH, '(//XCUIElementTypeImage[@name="cc_contacts_organization_classA"])[1]'),
        '团队联系人列表第一个': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]'),
        '团队联系人列表第二个': (MobileBy.XPATH,
                       '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]'),
        #搜索结果
        '搜索结果列表头像1': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeImage'),
        '搜索结果列表1': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeTable/XCUIElementTypeCell[1]'),
        '': (MobileBy.ACCESSIBILITY_ID, ''),
        '': (MobileBy.ACCESSIBILITY_ID, ''),




                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/actionbar_enterprise_contactselect_activity': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/actionbar_enterprise_contactselect_activity'),
                  'com.chinasofti.rcs:id/layout_search_enterprise_contactSelect_activity': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/layout_search_enterprise_contactSelect_activity'),
                  'com.chinasofti.rcs:id/layout_nomal_enterprise_contactSelect_activity': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/layout_nomal_enterprise_contactSelect_activity'),
                  'com.chinasofti.rcs:id/enterprise_fragment_contactSelect_activity': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/enterprise_fragment_contactSelect_activity'),
                  'com.chinasofti.rcs:id/lv_data_enterprise_fragment': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/lv_data_enterprise_fragment'),
                  'com.chinasofti.rcs:id/img_icon_department': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/img_icon_department'),
                  'myteam': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_department'),
                  'com.chinasofti.rcs:id/img_right_department': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/img_right_department'),
                  'Superman': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_department'),
                  'myteam02': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_department'),
                  '团队名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_department'),
                  }


    @TestLogger.log()
    def select_one_team_by_name(self, name):
        """选择一个团队"""
        self.click_element((MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="%s"])' % name))


    @TestLogger.log()
    def click_search_box(self):
        """点击搜索框"""
        self.click_element(self.__class__.__locators['搜索或输入手机号'])

    @TestLogger.log()
    def input_search_text(self, text):
        """输入搜索内容"""
        self.input_text(self.__class__.__locators['搜索或输入手机号'],text)


    @TestLogger.log()
    def click_element_by_id(self, text='搜索结果列表1'):
        """输入搜索内容"""
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def page_contain_element(self, text='搜索结果列表1'):
        """输入搜索内容"""
        return self.page_should_contain_element(self.__class__.__locators[text])


    @TestLogger.log()
    def wait_for_page_load(self, timeout=30, auto_accept_alerts=True):
        """等待选择团队页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators['团队头像-第一个'])
            )
        except:
            message = "页面在{}s内，没有加载成功，或者在和通讯录没有团队".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def get_team_names(self,name):
        """获取团队名字"""
        locater=(MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="%s"])' % name)
        els = self.get_elements(self.__class__.__locators[locater])
        team_names = []
        if els:
            for el in els:
                team_names.append(el.text)
        return team_names


    @TestLogger.log()
    def click_back(self):
        """点击 返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log("获取所有团队名称")
    def get_all_group_name(self):
        """获取所有团队名"""
        max_try = 5
        current = 0
        while current < max_try:
            if self._is_element_present(self.__class__.__locators["团队名称"]):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        els = self.get_elements(self.__class__.__locators["团队名称"])
        group_name = []
        if els:
            for el in els:
                group_name.append(el.text)
        else:
            raise AssertionError("No m005_group, please add m005_group in address book.")
        return group_name


    @TestLogger.log("点击分享名片")
    def click_share_business_card(self):
        """点击分享名片"""
        time.sleep(2)
        self.click_element(self.__locators['分享名片'])

from appium.webdriver.common.mobileby import MobileBy
import re
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from selenium.common.exceptions import NoSuchElementException

class SelectLocalContactsPage(BasePage):
    """选择联系人->本地联系人 页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ContactsSelectActivity'

    __locators = {'': (MobileBy.ID, ''),
                  '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
                  '选择联系人': (MobileBy.ACCESSIBILITY_ID, '选择联系人'),
                  '确定': (MobileBy.IOS_PREDICATE, "name CONTAINS '确定'"),
                  '确定按钮': (MobileBy.ACCESSIBILITY_ID, '确定'),
                  '+号': (MobileBy.ID, "cc contacts add normal"),
                  '取消': (MobileBy.ACCESSIBILITY_ID, '取消'),
                  '发送': (MobileBy.ACCESSIBILITY_ID, '发送'),
                  '发送名片': (MobileBy.ACCESSIBILITY_ID, '发送名片'),
                  '搜索或输入手机号': (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeTextField"'),
                  '选择和通讯录联系人': (MobileBy.ACCESSIBILITY_ID, '选择和通讯录联系人'),
                  '选择和通讯录联系人右侧箭头': (
                      MobileBy.ACCESSIBILITY_ID, '/var/containers/Bundle/Application/8A752131-104A-4280-AF2E-2CC6995F5BFE/AndFetion.app/cc_me_next@3x.png'),
                  '联系人列表': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[2]'),
                  '电话号码': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="12560"])[1]'),
                  '联系人头像': (
                  MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[2]/XCUIElementTypeImage'),
                  #搜索结果
                  '搜索结果列表': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell'),
                  '搜索结果-联系人头像': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeImage'),
                  'com.chinasofti.rcs:id/contact_index_bar_container': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_container'),
                  '右侧字母索引': (MobileBy.XPATH,
                             '//*[@resource-id="com.chinasofti.rcs:id/contact_index_bar_container"]/android.widget.TextView'),
                  '左侧字母索引': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_index"]'),
                  # 删除成员
                  '确定删除': (MobileBy.XPATH, '//*[@text="确定"]'),
                  # 分享群二维码时选择联系人后的弹窗页面
                  '确定分享': (MobileBy.XPATH, '//*[@text="确定"]'),
                  '取消分享': (MobileBy.XPATH, '//*[@text="取消"]'),
                  '发送给:xxx': (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message'),
                  # 群主转让
                  '确定转让': (MobileBy.XPATH, '//*[@text="确定"]'),
                  '取消转让': (MobileBy.XPATH, '//*[@text="取消"]'),
                  # 选择一个本地联系人转发消息时的弹框
                  '发送给': (MobileBy.XPATH, "//*[contains(@text, '发送给')]"),
                  '取消转发': (MobileBy.XPATH, "//*[contains(@text, '取消')]"),
                  '确定转发': (MobileBy.XPATH, "//*[contains(@text, '确定')]"),
                  '被选中的联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/avator'),
                  '搜索结果展示': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell'),
                  '已选联系人名': (MobileBy.ID, 'com.chinasofti.rcs:id/image_text'),
                  }

    @TestLogger.log()
    def swipe_select_one_member_by_name(self, name):
        """通过人名选择一个联系人"""
        time.sleep(2)
        locator = (MobileBy.ACCESSIBILITY_ID, '%s' % name)
        self.click_element(locator)

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_sure(self):
        """点击确定(选择联系人后确定按钮)"""
        els = self.get_elements(self.__class__.__locators["确定"])
        return els[-1].click()
        # self.click_element(self.__class__.__locators["确定"])
        # self.click_element((MobileBy.XPATH, '(//XCUIElementTypeButton[@name="确定"])[2]'))

    @TestLogger.log()
    def click_sure_icon(self):
        """点击确定"""
        self.click_element(self.__class__.__locators["确定按钮"])

    @TestLogger.log()
    def click_share_card(self):
        """点击分享名片"""
        self.click_element(self.__class__.__locators['发送名片'])

    @TestLogger.log()
    def click_search_box(self):
        """点击搜索框"""
        self.click_element(self.__class__.__locators['搜索或输入手机号'])

    @TestLogger.log()
    def input_search_keyword(self, keyword):
        """输入搜索内容"""
        self.input_text(self.__locators['搜索或输入手机号'], keyword)

    @TestLogger.log()
    def click_search_result(self):
        """点击搜索结果"""
        self.click_element(self.__class__.__locators['搜索结果列表'])

    @TestLogger.log()
    def click_element_by_id(self, text='搜索结果列表1'):
        """点击元素"""
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def click_send(self):
        """点击发送"""
        self.click_element(self.__class__.__locators['发送'])

    @TestLogger.log()
    def click_sure_forward(self):
        """点击确定转发"""
        self.click_element(self.__class__.__locators['确定按钮'])

    @TestLogger.log()
    def click_cancel_forward(self):
        """点击取消转发"""
        self.click_element(self.__class__.__locators['取消'])

    @TestLogger.log("根据导航栏的第一个字母定位")
    def choose_index_bar_click_element(self):
        self.click_element(
            ('xpath','//*[@resource-id="com.chinasofti.rcs:id/contact_index_bar_container"]/android.widget.TextView[1]'))
        elements = self.get_elements(self.__class__.__locators["联系人名"])
        elements[0].click()

    @TestLogger.log()
    def click_sure_share(self):
        """点击确定分享"""
        self.click_element(self.__class__.__locators["确定分享"], auto_accept_permission_alert=False)

    @TestLogger.log()
    def click_sure_transfer(self):
        """点击确定群主转让"""
        self.click_element(self.__class__.__locators["确定转让"], auto_accept_permission_alert=False)

    @TestLogger.log()
    def click_cancel_transfer(self):
        """点击取消转让群主"""
        self.click_element(self.__class__.__locators["取消转让"], auto_accept_permission_alert=False)

    @TestLogger.log()
    def get_contacts_name(self):
        """获取联系人名"""
        els = self.get_elements(self.__class__.__locators["联系人名"])
        contacts_name = []
        if els:
            for el in els:
                contacts_name.append(el.text)
        b = set(contacts_name)
        return b

    @TestLogger.log()
    def click_sure_del(self):
        """点击确定删除成员"""
        self.click_element(self.__class__.__locators["确定删除"])

    @TestLogger.log()
    def get_phone_numbers(self):
        """获取电话号码"""
        els = self.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'))
        phones = []
        if els:
            for el in els:
                phones.append(el.text)
        return phones

    @TestLogger.log()
    def search(self, text):
        """搜索联系人"""
        self.input_text(self.__class__.__locators["搜索或输入手机号"], text)
        try:
            self.driver.hide_keyboard()
        except:
            pass

    @TestLogger.log()
    def select_one_member_by_name(self, name):
        """通过人名选择一个联系人"""
        self.click_element((MobileBy.XPATH, '//*[@text ="%s"]' % name))

    @TestLogger.log()
    def search_and_select_one_member_by_name(self, name):
        """搜索选择联系人"""
        self.input_text(self.__class__.__locators["搜索或输入手机号"], name)
        # self.click_element(self.__class__.__locators["联系人名"])
        self.click_element(self.__class__.__locators["联系人列表"])

    @TestLogger.log()
    def sure_btn_is_enabled(self):
        """确定按钮是否可点击"""
        return self._is_enabled(self.__class__.__locators["确定"])

    @TestLogger.log()
    def get_sure_btn_text(self):
        """获取确定点击按钮文本"""
        return self.get_element(self.__class__.__locators["确定"]).text

    @TestLogger.log()
    def contacts_is_selected(self, name):
        """获取联系人的选择状态"""
        selected_els = self.get_elements((MobileBy.XPATH,
                                          '//*[@text ="%s"]/../android.widget.ImageView[@resource-id="com.chinasofti.rcs:id/contact_icon"]' % name))
        if selected_els:
            return True
        else:
            return False

    @TestLogger.log()
    def is_exist_select_contacts_name(self):
        """是否存在已选联系人名"""
        return self._is_element_present(self.__class__.__locators["已选联系人名"])

    @TestLogger.log()
    def is_element_exit(self, text='确定'):
        """判断元素是否存在"""
        return self._is_element_present(self.__class__.__locators[text])

    def swipe_to_top(self, times=20):
        """滑动到顶部"""
        while times > 0:
            self.swipe_by_direction(self.__class__.__locators['容器列表'], 'down')
            flag = self.is_text_present("选择团队联系人")
            if flag:
                break
            times = times - 1

    @TestLogger.log()
    def get_all_contacts_name(self):
        """获取所有联系人名"""
        els = self.get_elements(self.__class__.__locators["联系人名"])
        contacts_name = []
        if els:
            for el in els:
                contacts_name.append(el.text)
        else:
            raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
        flag = True
        current = 0
        while flag:
            current += 1
            if current > 20:
                return
            self.page_up()
            els = self.get_elements(self.__class__.__locators["联系人名"])
            for el in els:
                if el.text not in contacts_name:
                    contacts_name.append(el.text)
                    flag = True
                else:
                    flag = False
        return contacts_name

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待选择联系人页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators['选择联系人'])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def get_selected_and_threshold_nums(self):
        """获取确定按钮上的选择人数与可选的总人数"""
        # sure_info = "确定(3/499)"
        sure_info = self.get_element(self.__class__.__locators['确定']).text
        nums = re.findall(r'\d+', sure_info)
        if len(nums) == 2:
            return int(nums[0]), int(nums[1])
        else:
            if not sure_info == '确定':
                raise AssertionError("确定按钮显示异常，不是‘确定’或者 ‘确定(3/499)’格式")

    @TestLogger.log()
    def selecting_local_contacts_by_name(self, name):
        """根据名字选择一个手机联系人"""
        locator = (MobileBy.IOS_PREDICATE, 'name=="%s"' % name)
        self.click_element(locator)

    @TestLogger.log()
    def is_exists_local_contacts_by_name(self, name):
        """是否存在指定手机联系人"""
        locator = (MobileBy.IOS_PREDICATE, 'name=="%s"' % name)
        return self._is_element_present2(locator)

    @TestLogger.log()
    def is_search_result(self, msg):
        """搜索结果判断"""
        els = self.get_elements((MobileBy.XPATH, '//*[contains(@text, "%s")]' % msg))
        return len(els) > 1

    @TestLogger.log()
    def select_local_contacts(self, n):
        """选择n个本地联系人"""

        els = self.get_elements(self.__class__.__locators["联系人名"])
        current = 0
        while current < n:
            els[current].click()
            current += 1

    @TestLogger.log()
    def get_contacts_name_list(self):
        """获取联系人名"""
        els = self.get_elements(self.__class__.__locators["联系人名"])
        contacts_name = []
        if els:
            for el in els:
                contacts_name.append(el.text)
        return contacts_name

    @TestLogger.log("点击第一个联系人")
    def click_first_phone_contacts(self):
        self.wait_until(
            condition=lambda x: self.get_elements(self.__locators['电话号码'])[0],
            auto_accept_permission_alert=False
        ).click()

    @TestLogger.log("当前页面是否在选择联系人页")
    def is_on_this_page(self):
        el = self.get_elements(self.__locators['选择联系人'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log("点击搜索第一个联系人")
    def click_search_phone_contacts(self):
        self.wait_until(
            condition=lambda x: self.get_elements(('id', 'com.chinasofti.rcs:id/contact_list_item'))[0],
            auto_accept_permission_alert=False
        ).click()

    @TestLogger.log()
    def click_add_icon(self):
        """点击加号图标"""
        self.click_element(self.__locators['+号'])

    def is_element_present_result(self):
        return self._is_element_present(self.__locators['搜索结果展示'])


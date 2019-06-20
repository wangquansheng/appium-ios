from appium.webdriver.common.mobileby import MobileBy

from library.core.TestLogger import TestLogger
from pages.components import FooterPage
import time


class ContactsPage(FooterPage):
    """通讯录页面"""
    # ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        #通讯录页面
        '通讯录标题': (MobileBy.XPATH, '//XCUIElementTypeStaticText[@name="通讯录"]'),
        '搜索': (MobileBy.XPATH, '(//XCUIElementTypeSearchField[@name="搜索"])[1]'),
        '群聊': (MobileBy.ACCESSIBILITY_ID, '群聊'),
        '公众号': (MobileBy.ACCESSIBILITY_ID, '公众号'),
        '创建团队': (MobileBy.ACCESSIBILITY_ID, '创建团队'),
        '全部团队': (MobileBy.ACCESSIBILITY_ID, '全部团队'),
        '默认团队': (MobileBy.ACCESSIBILITY_ID, '默认团队'),
        '设置': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="默认团队"]/XCUIElementTypeButton'),

        '团队头像': (MobileBy.ACCESSIBILITY_ID, 'cc_contacts_organization_classA'),
        '团队名称': (MobileBy.XPATH,''),
        #搜索结果
        '输入关键字快速搜索': (MobileBy.XPATH, '(//XCUIElementTypeSearchField[@name="输入关键字快速搜索"])[1]'),
        '搜索结果列表1': (MobileBy.XPATH,
                    '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell'),
        '搜索结果-团队联系人头像': (MobileBy.XPATH, '(//XCUIElementTypeImage[@name="cc_chat_personal_default"])'),
        '手机联系人': (MobileBy.ACCESSIBILITY_ID, '手机联系人'),
        '手机联系人头像':(MobileBy.XPATH,'//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeImage'),
        '群聊联系人头像': (MobileBy.XPATH,'(//XCUIElementTypeImage[@name="cc_chat_group_default"])[1]'),
        '和飞信新闻公众号头像': (MobileBy.XPATH,'//XCUIElementTypeImage[@name="/var/mobile/Containers/Data/Application/3FF94A5C-59E9-4E2B-AA59-79FEC854AC76/Library/RCSData/headimage/4cc45369622d4a44066beafd18633c55_(null)"]'),
        '查看更多1': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="查看更多"])[1]'),
        '查看更多2': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="查看更多"])[2]'),

        #底部标签栏
        '消息': (MobileBy.ACCESSIBILITY_ID, 'cc_chat_normal'),
        '通话': (MobileBy.ACCESSIBILITY_ID, 'cc_call_unselected'),
        '工作台': (MobileBy.ACCESSIBILITY_ID, 'cc_workbench_normal'),
        '通讯录': (MobileBy.ACCESSIBILITY_ID, 'cc_contacts_selected'),
        '我': (MobileBy.ACCESSIBILITY_ID, 'cc_me_unselected'),
        #手机联系人界面
        '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
        '搜索手机联系人': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeTextField'),
        '+号': (MobileBy.ACCESSIBILITY_ID, 'cc contacts add normal'),
        '标签分组': (MobileBy.ACCESSIBILITY_ID, '标签分组'),
        '索引字母容器': (MobileBy.XPATH,
                   '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]'),
        '列表项': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeTable/XCUIElementTypeCell'),
        '联系人头像': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeImage'),
        '本地联系人搜索结果': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeTable/XCUIElementTypeCell'),

    }

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在通讯录"""

        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["手机联系人"])
            )
            return True
        except:
            return False


    @TestLogger.log("点击手机联系人")
    def click_phone_contact(self):
        """点击手机联系人"""
        self.click_element(self.__class__.__locators['手机联系人'])

    @TestLogger.log("点击返回")
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators['返回'])


    @TestLogger.log('点击+号')
    def click_add(self):
        """点击+号"""
        self.click_element(self.__class__.__locators['+号'])

    @TestLogger.log('点击消息')
    def click_message_icon(self):
        """点击消息按钮"""
        self.click_element(self.__class__.__locators['消息'])

    @TestLogger.log('点击我页面')
    def click_me_icon(self):
        """点击进入我页面"""
        self.click_element(self.__class__.__locators['我'])

    @TestLogger.log('点击搜索框')
    def click_search_box(self):
        """点击搜索框"""
        self.click_element(self.__class__.__locators['搜索'])

    TestLogger.log("输入搜索内容")
    def input_search_text(self,text):
        time.sleep(1)
        self.input_text(self.__locators['输入关键字快速搜索'],text)

    TestLogger.log("查看控件是否存在")
    def page_contain_element(self,text='联系人头像'):
        time.sleep(1)
        return self.page_should_contain_element(self.__locators[text])

    TestLogger.log("查看控件是否存在")
    def page_not_contain_element(self,text='联系人头像'):
        time.sleep(1)
        return self.page_should_not_contain_element(self.__locators[text])



    @TestLogger.log('点击搜索框')
    def click_search_phone_contact(self):
        """点击搜索手机联系人"""
        self.click_element(self.__class__.__locators['搜索手机联系人'])

    @TestLogger.log('输入搜索手机联系人搜索内容')
    def input_search_keyword(self, keyword):
        self.input_text(self.__locators['搜索手机联系人'], keyword)


    @TestLogger.log('打开群聊列表')
    def open_group_chat_list(self):
        self.click_element(self.__class__.__locators['群聊'])

    @TestLogger.log()
    def select_contacts_by_name(self, name):
        """根据名字选择一个联系人"""
        locator = (MobileBy.ACCESSIBILITY_ID, '%s' % name)
        self.click_element(locator,max_try=10)



    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待通讯录页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["+号"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def is_contacts_exist_by_name(self, name):
        """通过联系人名判断联系人是否存在"""
        max_try = 10
        current = 0
        while current < max_try:
            if self.is_text_present(name):
                return True
            current += 1
            self.page_up()
        return False


    @TestLogger.log('获取页面所有联系人')
    def get_page_elements(self,text='搜索结果-联系人头像'):
        return self.get_elements(self.__class__.__locators[text])


    @TestLogger.log('点击搜索出的联系人')
    def click_element_contact(self,text='联系人头像'):
        self.click_element(self.__class__.__locators[text])


    @TestLogger.log('判断列表是否存在XXX联系人')
    def is_contact_in_list(self, name='本地联系人搜索结果'):
        if self.is_element_present_by_id(self.__class__.__locators[name]):
            return True
        else:
            return False
        # self.scroll_to_top()
        # groups = self.mobile.list_iterator(self.__locators['搜索结果列表'], self.__locators['列表项'])
        # for group in groups:
        #     if group.find_elements(MobileBy.XPATH,
        #                            '(//XCUIElementTypeStaticText[@name="%s"])[2]'.format(name)):
        #         return True
        # return False


    def page_up(self):
        """向上滑动一页"""
        self.driver.execute_script('mobile: swipe', {'direction': 'up'})

    @TestLogger.log("上一页")
    def page_down(self):
        """向下滑动"""
        self.driver.execute_script('mobile: swipe', {'direction': 'down'})

    @TestLogger.log()
    def click_label_grouping(self):
        """点击标签分组"""
        self.click_element(self.__class__.__locators['标签分组'])

    @TestLogger.log('判断元素是否存在')
    def is_element_present_by_id(self, locator,times=10):
        if self._is_element_present(self.__class__.__locators[locator]):
            return True
        else:
            c = 0
            while c < times:
                self.page_up()
                if self._is_element_present(self.__class__.__locators[locator]):
                    return True
                c += 1
            return False





















    @TestLogger.log("获取所有联系人名")
    def get_contacts_name(self):
        """获取所有联系人名"""
        max_try = 5
        current = 0
        while current < max_try:
            if self._is_element_present(self.__class__.__locators["联系人名"]):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        els = self.get_elements(self.__class__.__locators["联系人名"])
        contacts_name = []
        if els:
            for el in els:
                contacts_name.append(el.text)
        else:
            raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
        if "和通讯录" in contacts_name:
            contacts_name.remove("和通讯录")
        if "和飞信电话" in contacts_name:
            contacts_name.remove("和飞信电话")
        if "本机" in contacts_name:
            contacts_name.remove("本机")
        return contacts_name

    @TestLogger.log()
    def find_element_by_swipe(self, locator, times=15):
        """找不到元素就滑动"""
        if self._is_element_present(self.__class__.__locators[locator]):
            return self.get_element(self.__class__.__locators[locator])
        else:
            c = 0
            while c < times:
                self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
                if self._is_element_present(self.__class__.__locators[locator]):
                    return self.get_element(self.__class__.__locators[locator])
                c += 1
            return None



    @TestLogger.log("滚动列表到顶部")
    def scroll_to_top(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['通讯录列表'])
        )
        if self._is_element_present(self.__locators['群聊']):
            return True
        current = 0
        while True:
            current += 1
            if current > 20:
                return
            self.swipe_by_direction(self.__locators['通讯录列表'], 'up')
            if self._is_element_present(self.__locators['群聊']):
                break
        return True


    # @TestLogger.log("获取电话号码")
    # def get_phone_number(self):
    #     """获取电话号码"""
    #     els = self.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/contact_phone'))
    #     phones = []
    #     if els:
    #         for el in els:
    #             phones.append(el.text)
    #     else:
    #         raise AssertionError("m005_contacts is empty!")
    #     return phones


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
    def click_and_address(self):
        """点击和通讯录"""
        self.click_element(self.__class__.__locators['和通讯录'])


    @TestLogger.log('点击公众号图标')
    def click_official_account_icon(self):
        self.click_element(self.__locators['公众号'])

    @TestLogger.log('创建通讯录联系人')
    def create_contacts_if_not_exits(self, name, number):
        """
        导入联系人数据
        :param name:
        :param number:
        :return:
        """
        from pages import ContactDetailsPage
        detail_page = ContactDetailsPage()

        self.wait_for_page_load()
        # 创建联系人
        self.click_search_box()
        from pages import ContactListSearchPage
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword(name)
        if contact_search.is_contact_in_list(name):
            contact_search.click_back()
        else:
            contact_search.click_back()
            self.click_add()
            from pages import CreateContactPage
            create_page = CreateContactPage()
            create_page.wait_for_page_load()
            create_page.hide_keyboard_if_display()
            create_page.create_contact(name, number)
            detail_page.wait_for_page_load()
            detail_page.click_back_icon()

    @TestLogger.log()
    def click_and_address(self):
        """点击和通讯录"""
        self.click_element(self.__class__.__locators['和通讯录'])

    @TestLogger.log()
    def click_always_allowed(self):
        """获取通讯录权限点击始终允许"""
        if self.get_elements(self.__class__.__locators['弹出框点击允许']):
            self.click_element(self.__class__.__locators['弹出框点击允许'])

    @TestLogger.log()
    def click_forbidden(self):
        """点击禁止"""
        if self.get_elements(self.__class__.__locators['弹出框点击禁止']):
            self.click_element(self.__class__.__locators['弹出框点击禁止'])

    @TestLogger.log()
    def is_exist_allow_button(self):
        """是否存在始终允许"""
        return self._is_element_present(self.__class__.__locators["弹出框点击允许"])


    @TestLogger.log()
    def click_allow(self):
        """点击始终允许"""
        self.click_element(self.__class__.__locators['始终允许'])

    @TestLogger.log()
    def click_one_he_contacts(self):
        """获取和通讯录联系人"""
        els=self.get_elements(self.__class__.__locators['和通讯录联系人'])
        if els:
            els[0].click()
        else:
            raise AssertionError("和通迅录没有联系人，请添加")

    @TestLogger.log()
    def click_he_more(self):
        """点击和通讯录联系人更多"""
        self.click_element(self.__class__.__locators['和通讯录更多'])

    @TestLogger.log("处理SIM联系人弹框")
    def click_sim_contact(self):
        """点击和通讯录联系人更多"""
        time.sleep(2)
        if self.get_elements(self.__class__.__locators['不显示']):
            self.click_element(self.__class__.__locators['不显示'])

    @TestLogger.log()
    def is_exist_enterprise_group(self):
        """是否存在企业群"""
        max_try = 10
        current = 0
        while current < max_try:
            if self._is_element_present(self.__class__.__locators["企业群标识"]):
                return True
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        return False

    @TestLogger.log()
    def click_return(self):
        """点击返回"""
        self.click_element(self.__class__.__locators['群聊列表返回'])

    @TestLogger.log()
    def click_one_firm(self):
        """点击一个团队"""
        self.click_element(self.__class__.__locators['团队名称'])

    @TestLogger.log()
    def wait_for_contacts_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待通讯录页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["+号"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self


    @TestLogger.log()
    def page_contain_element_add(self):
        """页面包含元素+号"""
        self.page_should_contain_element(self.__class__.__locators['+号'])


    @TestLogger.log('判断元素是否存在')
    def is_page_contain_element(self, locator,times=10):
        # el=self.find_element_by_swipe(self.__class__.__locators[locator])
        if self._is_element_present(self.__class__.__locators[locator]):
             self.page_should_contain_element(self.__class__.__locators[locator])
        else:
            c = 0
            while c < times:
                self.page_up()
                if self._is_element_present(self.__class__.__locators[locator]):
                    return self.page_should_contain_element(self.__class__.__locators[locator])
                c += 1
            return self.page_should_contain_element(self.__class__.__locators[locator])



    @TestLogger.log("根据导航栏的第一个字母定位")
    def choose_index_bar_click_element(self):
        self.click_element(
            ('xpath','//*[@resource-id="com.chinasofti.rcs:id/contact_index_bar_container"]/android.widget.TextView[1]'))
        elements = self.get_elements(self.__class__.__locators["群聊名"])
        elements[0].click()

    @TestLogger.log('点击新建SIM联系人界面-确定')
    def click_sure_SIM(self):
        """点击确定"""
        self.click_element(self.__class__.__locators['新建手机联系人-确定'])


    @TestLogger.log('点击新建SIM联系人界面-确定')
    def input_contact_text(self,text):
        self.input_text(self.__class__.__locators["新建手机联系人-姓名"],text)

    @TestLogger.log('点击新建SIM联系人界面-确定')
    def click_creat_contacts(self):
        """点击新建联系人"""
        self.click_element(self.__class__.__locators['新建手机联系人'])


    #
    # @TestLogger.log()
    # def select_contacts_by_number(self, number):
    #     """根据号码选择一个联系人"""
    #     locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_number" and @text ="%s"]' % number)
    #     max_try = 20
    #     current = 0
    #     while current < max_try:
    #
    #         if self._is_element_present(locator):
    #             break
    #         self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
    #         current += 1
    #     self.click_element(locator)

    @TestLogger.log()
    def is_exit_element_by_text_swipe(self, number):
        """通过电话号码,滑动判断特定元素是否存在"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_number" and @text ="%s"]' % number)
        max_try = 20
        current = 0
        while current < max_try:
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
            if self._is_element_present(locator):
                return self.page_should_contain_element(locator)
            else:
                # break
                current += 1





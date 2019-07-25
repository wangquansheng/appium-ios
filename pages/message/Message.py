from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec

from library.core.TestLogger import TestLogger
from pages.components.Footer import FooterPage
import time
from pages.contacts.Contacts import ContactsPage


class MessagePage(FooterPage):
    """主页 - 消息页"""

    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        "+号": (MobileBy.ACCESSIBILITY_ID, 'cc contacts add normal'),
        "搜索": (MobileBy.ACCESSIBILITY_ID, '搜索'),
        "消息列表1": (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell'),
        "消息列表-对话消息头像": (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeImage'),
        "对话消息头像1": (MobileBy.XPATH,
                        '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeImage[1]'),
        '大佬1':(MobileBy.ACCESSIBILITY_ID, '大佬1'),
        '所有未读消息':(MobileBy.XPATH,'(//XCUIElementTypeStaticText[@name="1"])[2]'),
        '新消息通知':(MobileBy.XPATH,'(//XCUIElementTypeStaticText[@name="1"])[1]'),
        '消息免打扰图标':(MobileBy.ACCESSIBILITY_ID,'cc_chat_remind.png'),
        '企业群标识': (MobileBy.ACCESSIBILITY_ID, 'cc_chat_company'),
        '消息红点':(MobileBy.XPATH,'//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeOther[3]/XCUIElementTypeOther/XCUIElementTypeStaticText'),
        #搜索页面
        "输入关键字快速搜索": (MobileBy.XPATH, '(//XCUIElementTypeSearchField[@name="输入关键字快速搜索"])[1]'),
        "团队联系人列表": (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]'),
        "手机联系人头像": (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[2]/XCUIElementTypeImage'),
        "团队联系人头像": (MobileBy.ACCESSIBILITY_ID, 'cc_chat_personal_default'),
        "搜索结果列表1": (MobileBy.XPATH,
                    '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]'),
        "返回": (MobileBy.ACCESSIBILITY_ID, 'back'),
        #左滑
        "置顶": (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="置顶"])[1]'),
        "左滑删除": (MobileBy.XPATH, '//XCUIElementTypeButton[@name="删除"][1]'),
        # "删除": (MobileBy.ACCESSIBILITY_ID, '删除'),
        # 底部标签栏
        '通话': (MobileBy.ACCESSIBILITY_ID, 'cc_call_unselected'),
        '工作台': (MobileBy.ACCESSIBILITY_ID, 'cc_workbench_normal'),
        '通讯录': (MobileBy.ACCESSIBILITY_ID, 'cc_contects_unselected'),
        '我': (MobileBy.IOS_PREDICATE, 'name == "我"'),
        '新建消息': (MobileBy.ACCESSIBILITY_ID, '新建消息'),
        '免费短信': (MobileBy.ACCESSIBILITY_ID, '免费短信'),
        '发起群聊': (MobileBy.ACCESSIBILITY_ID, '发起群聊'),
        #系统消息页面
        '同意':(MobileBy.XPATH,'(//XCUIElementTypeButton[@name="同意"])[1]'),
        '分组群发': (
            MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/pop_navi_text" and @text ="分组群发"]'),
        '扫一扫': (
            MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/pop_navi_text" and @text ="扫一扫"]'),
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/activity_main': (MobileBy.ID, 'com.chinasofti.rcs:id/activity_main'),
        'com.chinasofti.rcs:id/home_tag_view_pager': (MobileBy.ID, 'com.chinasofti.rcs:id/home_tag_view_pager'),
        'com.chinasofti.rcs:id/constraintLayout_home_tab': (
            MobileBy.ID, 'com.chinasofti.rcs:id/constraintLayout_home_tab'),
        'com.chinasofti.rcs:id/viewPager': (MobileBy.ID, 'com.chinasofti.rcs:id/viewPager'),
        'com.chinasofti.rcs:id/toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/toolbar'),
        '页头-消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMessage'),
        '消息列表': (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeCell"'),
        # '搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/search_edit'),
        '消息项': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_conv_list_item'),
        '消息头像': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
        '消息名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_conv_name'),
        '消息时间': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_date'),
        # '消息免打扰': (MobileBy.XPATH,
        #           '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text="%s"]/../../*[@resource-id="com.chinasofti.rcs:id/ll_unread"]'),
        '消息发送失败感叹号': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_fail_status'),
        '删除': (MobileBy.XPATH, "//*[contains(@label, '删除')]"),
        '收藏': (MobileBy.XPATH, "//*[contains(@text, '收藏')]"),
        '删除聊天': (MobileBy.XPATH, "//*[contains(@text, '删除聊天')]"),
        # 消息页中点击已发送文件
        '文件': (MobileBy.XPATH, "//*[contains(@text, '文件')]"),
        '位置': (MobileBy.XPATH, "//*[contains(@text, '位置')]"),
        '发送名片': (MobileBy.XPATH, "//*[contains(@text, '发送名片')]"),
        '名片': (MobileBy.XPATH, "//*[contains(@text, '名片')]"),
        "未读消息气泡": (MobileBy.ID, "com.chinasofti.rcs:id/rnMessageBadge"),
        '页面文案': (MobileBy.XPATH, "//*[contains(@text, '图文消息，一触即发')]"),
        '置顶聊天': (MobileBy.XPATH, '//*[@text="置顶聊天"]'),
        '取消置顶': (MobileBy.XPATH, '//*[@text="取消置顶"]'),
        # "消息免打扰图标": (MobileBy.ID, "com.chinasofti.rcs:id/iv_conv_slient"),
        # "消息红点": (MobileBy.ID, "com.chinasofti.rcs:id/red_dot_silent"),
        "版本更新": (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_title'),
        "以后再说": (MobileBy.ID, "com.chinasofti.rcs:id/btn_cancel"),
        '立即更新': (MobileBy.ID, "com.chinasofti.rcs:id/btn_ok"),
        '创建群聊':(MobileBy.ID,"com.chinasofti.rcs:id/creategroup"),
        "选择手机联系人":(MobileBy.XPATH,"//*[contains(@text,'选择手机联系人')]"),
        "确定2":(MobileBy.ID,"com.chinasofti.rcs:id/tv_sure"),
        "群聊名":(MobileBy.ID,"com.chinasofti.rcs:id/et_group_name"),
        "第一条聊天记录":(MobileBy.XPATH,"//XCUIElementTypeCell[1]/XCUIElementTypeStaticText[2]"),
        "第一条聊天记录发送时间":(MobileBy.XPATH,"//XCUIElementTypeCell[1]/XCUIElementTypeStaticText[3]"),
    }

    @TestLogger.log()
    def press_and_move_left(self, element='大佬1'):
        """按住并向左滑动"""
        # b=self.get_element_attribute(self.__class__.__locators[element],"bounds")
        self.swipe_by_direction(self.__class__.__locators[element],'left')

    @TestLogger.log()
    def click_system_message_allow(self):
        """点击系统消息页面第一个同意"""
        self.click_element(self.__locators['同意'])

    @TestLogger.log()
    def click_add_icon(self):
        """点击加号图标"""
        self.click_element(self.__locators['+号'])

    @TestLogger.log()
    def click_search_box(self):
        """点击搜索框"""
        self.click_element(self.__class__.__locators['搜索'])

    @TestLogger.log()
    def input_search_text(self,text):
        """输入搜索文本"""
        self.input_text(self.__locators['输入关键字快速搜索'],text)

    @TestLogger.log()
    def click_search_local_contact(self):
        """点击搜索结果-本地联系人"""
        self.click_element(self.__locators['手机联系人头像'])

    @TestLogger.log()
    def click_element_first_list(self):
        """点击搜索结果排列第一的项"""
        # self.swipe_by_percent_on_screen()
        self.click_element(self.__locators['团队联系人列表'])

    @TestLogger.log()
    def is_element_present(self,text='消息列表1'):
        """是否存在消息头像"""
        return self._is_element_present(self.__class__.__locators[text])

    @TestLogger.log()
    def is_element_present_local_contact(self,text='手机联系人头像'):
        """是否存在手机联系人头像"""
        if self._is_element_present(self.__class__.__locators[text]):
            return True
        else:
            return False

    @TestLogger.log("点击消息列表第一条1v1记录")
    def click_msg_first_list(self):
        self.click_element(self.__class__.__locators["消息列表1"])
        time.sleep(1)

    @TestLogger.log("点击置顶")
    def click_list_to_be_top(self):
        self.click_element(self.__class__.__locators["置顶"])
        time.sleep(1)

    @TestLogger.log("点击删除")
    def click_delete_list(self):
        time.sleep(1)
        self.click_element(self.__class__.__locators["左滑删除"])

    @TestLogger.log("回到列表顶部")
    def scroll_to_top(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['搜索'])
        )
        # 如果找到“短信设置”菜单，则当作已经滑到底部
        if self._is_on_the_start_of_list_view():
            return True
        max_try = 50
        current = 0
        while current < max_try:
            current += 1
            self.page_up()
            if self._is_on_the_start_of_list_view():
                break
        return True

    @TestLogger.log("检查列表第一项消息标题")
    def assert_first_message_title_in_list_is(self):
        locator=(MobileBy.XPATH,'//XCUIElementTypeCell/XCUIElementTypeStaticText[1]')
        return self.get_element(locator).text

    @TestLogger.log("删除所有的消息列表")
    def delete_all_message_list(self):
        current = 0
        max_try = 10
        while self._is_element_present2(self.__class__.__locators["消息列表"]):
            if current < max_try:
                self.swipe_by_direction(self.__class__.__locators["消息列表"], "left")
                self.click_element_by_name("删除")
                current += 1
        # time.sleep(1)
        # current = 0
        # max_try = 10
        # while self.is_element_present(text='消息列表1'):
        #     if current < max_try:
        #         self.swipe_by_percent_on_screen(70,20,30,20)
        #         time.sleep(1)
        #         # self.click_delete_list()
        #         self.click_element_by_name("删除")
        #         current += 1

    @TestLogger.log()
    def wait_for_page_load(self, timeout=30, auto_accept_alerts=True):
        """等待消息页面加载（自动允许权限）"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["+号"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_page_load_new_message_coming(self, timeout=30, auto_accept_alerts=True):
        """等待消息页面新消息加载成功（自动允许权限）[默认只发送或接受到一条消息]"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["新消息通知"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def is_element_present_all_unread_message_number(self, number='1'):
        """是否存在所有未读消息"""
        locator=(MobileBy.XPATH,'(//XCUIElementTypeStaticText[@name="%s"])[2]' % number)
        return self._is_element_present(locator)


    @TestLogger.log()
    def is_exist_no_disturb_icon(self):
        """是否存在消息免打扰图标"""
        return self._is_element_present(self.__class__.__locators["消息免打扰图标"])

    @TestLogger.log()
    def is_exist_news_red_dot(self):
        """是否存在消息红点"""
        return self._is_element_present(self.__class__.__locators["消息红点"])

    @TestLogger.log()
    def is_exist_unread_make_and_number(self, number='1'):
        """是否存在新消息通知"""
        locator=(MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="%s"])[1]' % number)
        return self._is_element_present(locator)

    @TestLogger.log()
    def press_unread_make_and_move_down(self, number='1'):
        """拖动取消新消息通知"""
        locator = (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="%s"])[1]' % number)
        element = self.get_element(locator)
        rect = element.rect
        left, right = int(rect['x']) + 1, int(rect['x'] + rect['width']) - 1
        top, bottom = int(rect['y']) + 1, int(rect['y'] + rect['height']) - 1
        x_start = (left + right) // 2
        x_end = (left + right) // 2
        y_start = top
        y_end = bottom+200
        self.driver.execute_script("mobile:dragFromToForDuration",
                                   {"duration": 0.5, "element": None, "fromX": x_start,
                                    "fromY": y_start,
                                    "toX": x_end, "toY": y_end})

    @TestLogger.log()
    def press_new_message_red_icon(self):
        """拖动取消红点"""
        element = self.get_element(self.__class__.__locators["消息红点"])
        rect = element.rect
        left, right = int(rect['x']) + 1, int(rect['x'] + rect['width']) - 1
        top, bottom = int(rect['y']) + 1, int(rect['y'] + rect['height']) - 1
        x_start = (left + right) // 2
        x_end = (left + right) // 2
        y_start = top
        y_end = bottom+200
        self.driver.execute_script("mobile:dragFromToForDuration",
                                   {"duration": 0.5, "element": None, "fromX": x_start,
                                    "fromY": y_start,
                                    "toX": x_end, "toY": y_end})

    @TestLogger.log('点击发起群聊')
    def click_group_chat(self):
        """点击发起群聊"""
        self.click_element(self.__locators['发起群聊'])

    @TestLogger.log()
    def is_message_content_match_message_name(self, message):
        """查看刚刚发送消息的窗口消息内容是否显示 我 + <消息文本>"""
        locaor = (MobileBy.ACCESSIBILITY_ID, '我: %s' % message)
        return self._is_element_present(locaor)

    @TestLogger.log("点击创建群聊")
    def click_create_group(self):
        self.click_element(self.__locators["创建群聊"])
        time.sleep(1)

    @TestLogger.log("点击选择手机联系人")
    def click_contact_group(self):
        self.click_element(self.__locators["选择手机联系人"])
        time.sleep(1)

    @TestLogger.log("点击群聊名")
    def click_group_name(self):
        self.click_element(self.__locators["群聊名"])
        time.sleep(1)

    @TestLogger.log("检查群聊名是否存在")
    def check_group_name_exist(self):
        return self.page_should_not_contain_element(self.__locators["群聊名"])

    @TestLogger.log("设置群聊名")
    def set_group_name(self,text='aaa'):
        self.input_text(self.__locators["群聊名"],text)
        time.sleep(1)

    @TestLogger.log("点击确定")
    def click_sure_button(self):
        self.click_element(self.__locators["确定2"])
        time.sleep(1)

    @TestLogger.log('检查顶部搜索框是否显示')
    def assert_search_box_is_display(self, max_wait_time=5):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators['搜索']),
                timeout=max_wait_time
            )
        except TimeoutException:
            raise AssertionError('搜索框没有显示：{}'.format(self.__locators['搜索']))

    @TestLogger.log('检查顶部搜索框是否显示')
    def assert_search_box_text_is(self, text):
        self.mobile.assert_element_text_should_be(self.__locators['搜索'], text, '搜索框文本与"{}"不匹配'.format(text))

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在消息页"""

        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["+号"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_new_message(self):
        """点击新建消息"""
        self.click_element(self.__locators['新建消息'])

    @TestLogger.log()
    def assert_new_message_text_equal_to(self, expect):
        """检查新建消息菜单文本"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['新建消息'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def click_free_sms(self):
        """点击免费短信"""
        self.click_element(self.__locators['免费短信'])

    @TestLogger.log()
    def assert_free_sms_text_equal_to(self, expect):
        """检查免费短信菜单文本"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['免费短信'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def click_contacts(self):
        """点击通讯录"""
        self.click_element(self.__locators['通讯录'])
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        time.sleep(1)
        if ContactsPage().is_text_present('发现SIM卡联系人'):
            ContactsPage().click_text('显示')
        time.sleep(2)

    @TestLogger.log()
    def click_contacts_only(self):
        """只点击通讯录"""
        self.click_element(self.__locators['通讯录'])

    @TestLogger.log()
    def assert_group_chat_text_equal_to(self, expect):
        """检查发起群聊菜单文本"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['发起群聊'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def click_group_mass(self):
        """点击分组群发"""
        self.click_element(self.__locators['分组群发'])

    @TestLogger.log()
    def assert_group_mass_text_equal_to(self, expect):
        """检查分组群发菜单文本"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['分组群发'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def click_take_a_scan(self):
        """点击扫一扫"""
        self.click_element(self.__locators['扫一扫'])

    @TestLogger.log()
    def assert_take_a_scan_text_equal_to(self, expect):
        """检查扫一扫菜单文本"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['扫一扫'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def click_search(self):
        """搜索"""
        self.click_element(self.__class__.__locators['搜索'])

    @TestLogger.log()
    def input_search_message(self, message):
        """输入查询内容"""
        self.input_text(self.__class__.__locators['搜索'], message)

    @TestLogger.log()
    def wait_login_success(self, timeout=8, auto_accept_alerts=True):
        """等待消息页面加载（自动允许权限）"""
        # time.sleep(15)
        # locator = (MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/btn_cancel" and @text ="以后再说"]')
        # if self._is_element_present(locator):
        #     self.click_element(locator)
        self.__unexpected_info = None

        def unexpected():
            result = self.get_text(
                [MobileBy.XPATH,
                 '//*[@text="当前网络不可用(102101)，请检查网络设置" or' +
                 ' @text="服务器繁忙或加载超时,请耐心等待" or' +
                 ' contains(@text,"一键登录暂时无法使用") or' +
                 ' contains(@text,"登录失败") or' +
                 ' @text="网络连接超时(102102)，请使用短信验证码登录" or' +
                 ' @text="立即更新" or' +
                 ']'])
            self.__unexpected_info = result
            return result

        # mark = 10
        # while mark > 0:
        #     time.sleep(1)
        #     if (self._is_element_present(self.__class__.__locators["版本更新"])):
        #         self.click_element(self.__class__.__locators["以后再说"])
        #         break
        #     mark -= 1

        try:
            self.wait_condition_and_listen_unexpected(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators["+号"]),
                unexpected=unexpected
            )
        except TimeoutException:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        except AssertionError:
            raise AssertionError("检查到页面报错：{}".format(self.__unexpected_info))
        return self

    @TestLogger.log('检查是否收到某个号码的短信')
    def assert_get_sms_of(self, phone_number, content, max_wait_time=30):
        try:
            self.click_message(phone_number, max_wait_time)
        except NoSuchElementException:
            raise AssertionError('没有收到{}的消息'.format(phone_number))

    @TestLogger.log('检查页面有没有出现139邮箱消息')
    def assert_139_message_not_appear(self, max_wait_time=30):
        self.scroll_to_top()
        try:
            self.wait_until(
                condition=lambda d: self.is_text_present('139邮箱助手'),
                timeout=max_wait_time
            )
        except TimeoutException:
            return
        raise AssertionError('消息列表中不应该显示139邮箱消息，但实际上有显示')

    @TestLogger.log('点击消息')
    def click_message(self, title, max_wait_time=5):
        locator = [MobileBy.XPATH,
                   '//*[@resource-id="com.chinasofti.rcs:id/rl_conv_list_item" and ' +
                   './/*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text="{}"]]'.format(title)]
        self.find_message(title, max_wait_time)
        self.click_element(locator)

    @TestLogger.log('置顶消息')
    def set_top_for_message(self, title, max_wait_time=5):
        locator = [MobileBy.XPATH,
                   '//*[@resource-id="com.chinasofti.rcs:id/rl_conv_list_item" and ' +
                   './/*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text="{}"]]'.format(title)]
        self.find_message(title, max_wait_time)
        message = self.get_element(locator)
        position_x, position_y = message.location.get('x'), message.location.get('y')
        self.mobile.tap([(position_x, position_y)], 1000)
        if self.is_text_present('取消置顶'):
            el = self.get_element([MobileBy.XPATH, '//*[@text="取消置顶"]'])
            position_y, position_y = el.location.get('x'), el.location.get('y') - 100
            self.mobile.tap([(position_x, position_y)])
            return
        if self.is_text_present('置顶聊天'):
            self.click_text('置顶聊天')
        else:
            raise NoSuchElementException('没找到“置顶消息”菜单')

    @TestLogger.log("检查最新的一条消息的Title")
    def assert_the_first_message_is(self, title, max_wait_time=5):
        self.scroll_to_top()
        try:
            self.wait_until(
                condition=lambda d: self.get_text(self.__locators['消息名称']) == title,
                timeout=max_wait_time
            )
        except TimeoutException:
            raise AssertionError('{}秒内没有找到"{}"的最新消息'.format(max_wait_time, title))

    @TestLogger.log("寻找定位消息")
    def find_message(self, title, max_wait_time=5):
        locator = [MobileBy.XPATH,
                   '//*[@resource-id="com.chinasofti.rcs:id/rl_conv_list_item" and ' +
                   './/*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text="{}"]]'.format(title)]
        if not self._is_element_present(locator):
            # 找不到就翻页找到菜单再点击，
            self.scroll_to_top()
            if self._is_element_present(locator):
                return
            if not self.get_elements(self.__locators['消息项']):
                try:
                    self.wait_until(
                        condition=lambda d: self.get_element(locator),
                        timeout=max_wait_time,
                        auto_accept_permission_alert=False
                    )
                    return
                except TimeoutException:
                    raise NoSuchElementException('页面找不到元素：{}'.format(locator))
            max_try = 20
            current = 0
            while current < max_try:
                first_item = self.get_element(self.__locators['消息项'])
                current += 1
                self.page_down()
                if self._is_element_present(locator):
                    return
                if not ec.staleness_of(first_item)(True):
                    break
            self.scroll_to_top()
            try:
                self.wait_until(
                    condition=lambda d: self.get_element(locator),
                    timeout=max_wait_time,
                    auto_accept_permission_alert=False
                )
                return
            except TimeoutException:
                raise NoSuchElementException('页面找不到元素：{}'.format(locator))

    @TestLogger.log("下一页")
    def page_up(self):
        """向上滑动"""
        self.swipe_by_percent_on_screen(50, 70, 50, 30)

    @TestLogger.log("上一页")
    def page_down(self):
        """向下滑动"""
        self.swipe_by_percent_on_screen(50, 30, 50, 70)

    def _is_on_the_start_of_list_view(self):
        """判断是否列表开头"""
        return self._is_element_present(self.__locators['搜索'])

    @TestLogger.log()
    def is_exist_undisturb(self, group_name):
        """某群是否存在消息免打扰标志"""
        path = self.__class__.__locators["消息免打扰"][1]
        self.__class__.__locators["xpath"] = (self.__class__.__locators["消息免打扰"][0], path % group_name)
        return self._is_element_present(self.__class__.__locators["xpath"])

    @TestLogger.log()
    def get_top_news_name(self):
        """获取置顶群的名字"""
        return self.get_element(self.__class__.__locators['置顶群']).text

    @TestLogger.log()
    def click_element_by_text(self,text):
        """点击指定元素"""
        self.click_element((MobileBy.XPATH, '//*[@text="%s"]' % text))

    @TestLogger.log()
    def is_iv_fail_status_present(self):
        """判断消息发送失败“！”标致是否存在"""
        return self._is_element_present(self.__locators['消息发送失败感叹号'])

    @TestLogger.log()
    def is_message_fail_status_present(self,name):
        """判断某条消息,消息发送失败“！”标致是否存在"""
        return self._is_element_present(self.__locators['消息发送失败感叹号'],name)

    @TestLogger.log()
    def press_file_to_do(self, file, text):
        """长按指定文件进行操作"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def look_detail_news_by_name(self, name):
        """查看详细消息"""
        self.click_element((MobileBy.XPATH, "//*[@text='%s']" % name))

    @TestLogger.log()
    def click_msg_by_content(self, text):
        """点击消息"""
        self.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_content" and @text="%s"]' % text))

    @TestLogger.log('判断该页面是否有元素')
    def page_contain_element(self, locator):
        return self.page_should_contain_element(self.__locators[locator])

    @TestLogger.log("判断消息列表的消息是否包含省略号")
    def msg_is_contain_ellipsis(self):
        contents = []
        els = self.get_elements(self.__locators['消息简要内容'])
        for el in els:
            contents.append(el.text)
        for msg in contents:
            if "…" in msg:
                return True
        raise AssertionError("消息列表的消息无省略号")

    @TestLogger.log()
    def click_set_message(self, locator):
        """点击已发文件类型"""
        self.click_element(self.__locators[locator])

    @TestLogger.log()
    def choose_chat_by_name(self, name, max_try=5):
        """通过名字选择一个聊天"""
        locator = (MobileBy.IOS_PREDICATE, "name == '%s'" % name)
        self.click_element(locator, max_try)

    @TestLogger.log()
    def click_workbench(self):
        """点击工作台"""
        self.click_element(self.__class__.__locators["工作台"])

    @TestLogger.log()
    def search_box_is_enabled(self):
        """页面搜索框是否可点击"""
        return self._is_enabled(self.__class__.__locators["搜索"])

    @TestLogger.log()
    def add_icon_is_enabled(self):
        """+号图标是否可点击"""
        return self._is_enabled(self.__class__.__locators["+号"])

    @TestLogger.log()
    def is_exist_network_anomaly(self):
        """是否存在网络异常"""
        return self.is_text_present("当前网络不可用，请检查网络设置")

    @TestLogger.log()
    def is_exist_unread_messages(self):
        """是否存在未读消息"""
        els = self.get_elements(self.__class__.__locators["未读消息气泡"])
        return len(els) > 0

    @TestLogger.log()
    def clear_up_unread_messages(self):
        """清空未读消息"""
        els = self.get_elements(self.__class__.__locators["未读消息气泡"])
        rect = els[-1].rect
        x = int(rect["x"]) + int(rect["width"]) / 2
        y = -(int(rect["y"]) - 20)
        TouchAction(self.driver).long_press(els[-1], duration=3000).move_to(els[-1], x,
                                                                            y).wait(3).release().perform()
    @TestLogger.log()
    def wait_for_message_list_load(self, timeout=60, auto_accept_alerts=True):
        """等待消息列表加载"""
        # locator = (MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/btn_cancel" and @text ="以后再说"]')
        # if self._is_element_present(locator):
        #     self.click_element(locator)
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["消息名称"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def clear_fail_in_send_message(self):
        """清除发送失败消息记录"""
        current = 0
        while self._is_element_present(self.__class__.__locators["消息发送失败感叹号"]):
            current += 1
            if current > 5:
                return
            els = self.get_elements(self.__class__.__locators["消息发送失败感叹号"])
            for el in els:
                time.sleep(1)
                self.press(el)
                time.sleep(1)
                self.click_element(self.__class__.__locators["删除聊天"])

    @TestLogger.log()
    def is_exist_search_box(self):
        """是否存在消息搜索框"""
        return self._is_element_present(self.__class__.__locators["搜索"])

    @TestLogger.log()
    def is_exist_add_icon(self):
        """是否存在+号图标"""
        return self._is_element_present(self.__class__.__locators["+号"])

    @TestLogger.log()
    def is_exist_words(self):
        """是否存在页面文案"""
        return self._is_element_present(self.__class__.__locators["页面文案"])

    @TestLogger.log()
    def slide_to_the_top(self):
        """滑到消息记录顶端"""
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(self.__class__.__locators["搜索"]):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 30, 50, 70, 800)

    @TestLogger.log()
    def top_message_recording_by_number(self, number):
        """置顶某一条消息记录"""
        els = self.get_elements(self.__class__.__locators["消息名称"])
        name = els[number].text
        self.press(els[number])
        if self._is_element_present(self.__class__.__locators["置顶聊天"]):
            self.click_element(self.__class__.__locators["置顶聊天"])
        else:
            self.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        return name

    @TestLogger.log()
    def cancel_stick_message_recording_by_number(self, number):
        """取消置顶某一条消息记录"""
        els = self.get_elements(self.__class__.__locators["消息名称"])
        name = els[number].text
        self.press(els[number])
        if self._is_element_present(self.__class__.__locators["取消置顶"]):
            self.click_element(self.__class__.__locators["取消置顶"])
        else:
            self.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        return name

    @TestLogger.log()
    def get_message_name_by_number(self, number):
        """获取消息名称"""
        els = self.get_elements(self.__class__.__locators["消息名称"])
        name = els[number].text
        return name

    @TestLogger.log()
    def is_exist_message_name(self):
        """是否存在消息名称"""
        return self._is_element_present(self.__class__.__locators["消息名称"])

    @TestLogger.log()
    def is_exist_message_record(self):
        """是否存在消息记录"""
        return self._is_element_present(self.__class__.__locators["消息项"])

    @TestLogger.log()
    def is_exist_message_img(self):
        """是否存在消息头像"""
        return self._is_element_present(self.__class__.__locators["消息头像"])

    @TestLogger.log()
    def is_exist_message_time(self):
        """是否存在消息时间"""
        return self._is_element_present(self.__class__.__locators["消息时间"])

    @TestLogger.log()
    def is_exist_message_content(self):
        """是否存在消息内容"""
        return self._is_element_present(self.__class__.__locators["消息简要内容"])

    @TestLogger.log()
    def cancel_message_record_stick(self):
        """取消当前页消息记录所有已置顶"""
        els = self.get_elements(self.__class__.__locators["消息名称"])
        for el in els:
            self.press(el)
            if self._is_element_present(self.__class__.__locators["取消置顶"]):
                self.click_element(self.__class__.__locators["取消置顶"])
            else:
                self.tap_coordinate([(100, 20), (100, 60), (100, 100)])

    @TestLogger.log()
    def clear_message_record(self):
        """清空消息列表聊天记录"""
        current = 0
        while self._is_element_present(self.__class__.__locators["消息名称"]):
            current += 1
            if current > 5:
                return
            els = self.get_elements(self.__class__.__locators["消息名称"])
            for el in els:
                self.press(el)
                if self._is_element_present(self.__class__.__locators["删除聊天"]):
                    self.click_element(self.__class__.__locators["删除聊天"])
                else:
                    self.tap_coordinate([(100, 20), (100, 60), (100, 100)])

    @TestLogger.log()
    def is_slide_message_list(self):
        """验证消息列表是否可滑动"""
        self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        return self._is_element_present(self.__class__.__locators["搜索"])

    @TestLogger.log()
    def message_list_is_exist_name(self, name):
        """消息列表是否存在指定人名称"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % name)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                return True
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        return False

    @TestLogger.log()
    def delete_message_record_by_name(self, name):
        """删除指定消息记录"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % name)
        el = self.get_element(locator)
        self.press(el)
        self.click_element(self.__class__.__locators['删除聊天'])

    @TestLogger.log()
    def current_message_list_is_exist_name(self, name):
        """当前消息列表是否存在指定人名称"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % name)
        return self._is_element_present(locator)

    @TestLogger.log()
    def is_clear_no_disturb_icon(self):
        """拖拽后免打扰图标是否消除"""
        self.swipe_by_direction(self.__class__.__locators["消息免打扰图标"], "up", 800)
        if self._is_element_present(self.__class__.__locators["消息免打扰图标"]):
            return False
        return True

    @TestLogger.log()
    def is_clear_news_red_dot(self):
        """拖拽后消息红点是否消除"""
        self.swipe_by_direction(self.__class__.__locators["消息红点"], "up", 800)
        if self._is_element_present(self.__class__.__locators["消息红点"]):
            return False
        return True

    @TestLogger.log()
    def is_message_content_match_file_name(self, file_name):
        """查看刚刚发送消息的窗口消息内容是否显示文件+文件名"""
        els = self.get_elements(self.__class__.__locators["消息简要内容"])
        text = els[0].text
        if "[文件]%s" % file_name in text:
            return True
        return False

    @TestLogger.log()
    def is_message_content_match_picture(self):
        """查看刚刚发送消息的窗口消息内容是否显示图片"""
        els = self.get_elements(self.__class__.__locators["消息简要内容"])
        text = els[0].text
        if "[图片]" in text:
            return True
        return False

    @TestLogger.log()
    def is_message_content_match_video(self):
        """查看刚刚发送消息的窗口消息内容是否显示视频"""

        els = self.get_elements(self.__class__.__locators["消息简要内容"])
        text = els[0].text
        if "[视频]" in text:
            return True
        return False

    @TestLogger.log()
    def click_msg_delete(self):
        """点击删除"""
        self.click_element(self.__class__.__locators["删除"])

    @TestLogger.log()
    def delete_the_first_msg(self):
        """当前在消息界面，左滑删除第一个消息聊天"""
        for i in range(3):
            try:
                self.swipe_by_percent_on_screen(80, 20, 40, 20)
                self.click_msg_delete()
                break
            except:
                print("删除失败，重试")

    def click_message_session(self, index):
        """通过下标点击消息会话"""
        elements = self.get_elements(self.__class__.__locators["消息列表1"])
        try:
            if len(elements) > 0:
                return elements[index].click()
        except:
            raise IndexError("元素超出索引")

    @TestLogger.log()
    def is_first_message_image(self):
        """获取第一条聊天记录文本是否是图片"""
        el = self.get_element(self.__class__.__locators["第一条聊天记录"])
        if "[图片]" in el.text:
            return True
        else:
            return False

    @TestLogger.log()
    def is_first_message_expression(self):
        """获取第一条聊天记录文本是否是表情"""
        el = self.get_element(self.__class__.__locators["第一条聊天记录"])
        if "[表情]" in el.text:
            return True
        else:
            return False

    @TestLogger.log()
    def is_first_message_video(self):
        """获取第一条聊天记录文本是否是视频"""
        el = self.get_element(self.__class__.__locators["第一条聊天记录"])
        if "[视频]" in el.text:
            return True
        else:
            return False

    @TestLogger.log()
    def is_first_message_draft(self):
        """获取第一条聊天记录文本是否是草稿"""
        el = self.get_element(self.__class__.__locators["第一条聊天记录"])
        if "[草稿]" in el.text:
            return True
        else:
            return False

    @TestLogger.log()
    def is_first_message_content(self, text):
        """获取第一条聊天记录文本中是否包含输入的内容"""
        el = self.get_element(self.__class__.__locators["第一条聊天记录"])
        if text in el.text:
            return True
        else:
            return False

    @TestLogger.log()
    def get_first_message_send_time(self, text):
        """获取第一条聊天记录发送时间"""
        if self._is_element_present2(self.__class__.__locators["第一条聊天记录发送时间"]):
            el = self.get_element(self.__class__.__locators["第一条聊天记录发送时间"])
            if text in el.text:
                return True
            else:
                return False

    @TestLogger.log()
    def click_me_button(self):
        """点击底部信息栏'我'"""
        self.click_element(self.__class__.__locators["我"])

    @TestLogger.log()
    def click_element_(self,text):
        """点击指定元素"""
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def is_element_exit_(self, text):
        """指定元素是否存在"""
        return self._is_element_present(self.__class__.__locators[text])

    @TestLogger.log()
    def is_text_present_(self, text):
        """指定文本是否存在（精确匹配）"""
        return self._is_element_present((MobileBy.IOS_PREDICATE, 'name == "%s"' %text))

    @TestLogger.log()
    def is_exists_no_disturb_icon_by_message_name(self, name):
        """指定消息记录是否存在免打扰图标"""
        locator = (MobileBy.XPATH, '//*[@name="%s"]/../XCUIElementTypeImage[@name="cc_chat_remind.png"]' % name)
        return self._is_element_present2(locator)

    @TestLogger.log()
    def left_slide_message_record_by_number(self, index=0):
        """左滑某一条消息记录，默认选择第一条"""
        if self._is_element_present2(self.__class__.__locators["消息列表"]):
            self.swipe_by_direction2(self.__class__.__locators["消息列表"], "left", index)

    @TestLogger.log()
    def click_element_by_name(self, text):
        """点击指定元素"""
        locator = (MobileBy.ACCESSIBILITY_ID, "%s" % text)
        if self._is_element_present2(locator):
            rect = self.get_element(locator).rect
            x = rect['x']
            y = rect['y']
            width = rect['width']
            window_width = self.driver.get_window_size()["width"]
            # 如果元素宽大于手机屏幕宽，重新赋值
            if width > window_width:
                width = 74
            height = rect['height']
            x += width / 2
            y += height / 2
            self.driver.execute_script("mobile: tap", {"y": y, "x": x, "duration": 50})

    @TestLogger.log()
    def click_search_result_by_name(self,text):
        """点击搜索结果"""
        locator = (MobileBy.XPATH, '//XCUIElementTypeCell/XCUIElementTypeStaticText[contains(@name,"%s")]' % text)
        self.click_element(locator)

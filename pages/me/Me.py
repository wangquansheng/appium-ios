from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException

from library.core.TestLogger import TestLogger
from pages.components.Footer import FooterPage


class MePage(FooterPage):
    """ 我 页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        '页头-我':(MobileBy.XPATH, '//XCUIElementTypeStaticText[@name="我"]'),
        '二维码入口': (MobileBy.ACCESSIBILITY_ID, 'cc me qrcode normal'),
        '我的名称': (MobileBy.ACCESSIBILITY_ID, 'Label'),
        '查看并编辑个人资料': (MobileBy.ACCESSIBILITY_ID, '查看并编辑个人资料'),
        '个人头像': (MobileBy.ACCESSIBILITY_ID, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeImage'),
        '和飞信电话可用时长': (MobileBy.ACCESSIBILITY_ID, 'banner_bg_card.png'),
        '每天领积分': (MobileBy.ACCESSIBILITY_ID, 'banner_bg_card2.png'),
        '福利': (MobileBy.ACCESSIBILITY_ID, '福利'),
        '热点资讯': (MobileBy.ACCESSIBILITY_ID, '热点资讯'),
        '移动营业厅': (MobileBy.ACCESSIBILITY_ID, '移动营业厅'),
        '和包支付': (MobileBy.ACCESSIBILITY_ID, '和包支付'),
        '收藏': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="收藏"])[1]'),
        '设置': (MobileBy.XPATH, '//XCUIElementTypeStaticText[@name="设置"]'),
        #底部标签栏
        '消息': (MobileBy.IOS_PREDICATE, "name == '消息'"),
        '通话': (MobileBy.ACCESSIBILITY_ID, '通话'),
        '工作台': (MobileBy.ACCESSIBILITY_ID, '工作台'),
        '通讯录': (MobileBy.ACCESSIBILITY_ID, '联系'),
        '我': (MobileBy.XPATH, '//XCUIElementTypeButton[@name="我"]'),
        # 编辑资料页面
        '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
        '编辑': (MobileBy.ACCESSIBILITY_ID, '编辑'),
        '分享名片': (MobileBy.ACCESSIBILITY_ID, '//XCUIElementTypeStaticText[@name="分享名片"]'),
        '保存': (MobileBy.ACCESSIBILITY_ID, '保存'),
        '拍照': (MobileBy.ACCESSIBILITY_ID, 'cc me photography normal'),
        '编辑姓名': (MobileBy.XPATH, '(//XCUIElementTypeTextView[@name="2b610f78-8d44-11e9-95e5-309c23f30f2e"])[1]'),
        '电话': (MobileBy.ACCESSIBILITY_ID, '19849476421'),




        '页脚-我': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvMe" and @selected="true"]'),
        'com.chinasofti.rcs:id/rl_person': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_person'),
        'com.chinasofti.rcs:id/fl_name': (MobileBy.ID, 'com.chinasofti.rcs:id/fl_name'),
        '请完善名片': (MobileBy.ID, 'com.chinasofti.rcs:id/card_name_hint'),
        '电话号码': (MobileBy.ID, 'com.chinasofti.rcs:id/card_photo_num'),
        '多方电话': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_call_name_text'),
        '300': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_call_number_text'),
        '分钟': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_call_unit'),
        'com.chinasofti.rcs:id/user_money': (MobileBy.ID, 'com.chinasofti.rcs:id/user_money'),
        '账户余额': (MobileBy.ID, 'com.chinasofti.rcs:id/money_name_text'),
        '12.20': (MobileBy.ID, 'com.chinasofti.rcs:id/money_number_text'),
        '元': (MobileBy.ID, 'com.chinasofti.rcs:id/money_unit'),
        'com.chinasofti.rcs:id/layout_flow': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_flow'),
        '可用流量': (MobileBy.ID, 'com.chinasofti.rcs:id/liuliang_name_text'),
        '40.98': (MobileBy.ID, 'com.chinasofti.rcs:id/liuliang_number_text'),
        'G': (MobileBy.ID, 'com.chinasofti.rcs:id/liuliang_unit'),
        'com.chinasofti.rcs:id/redpager': (MobileBy.ID, 'com.chinasofti.rcs:id/redpager'),
        '钱包': (MobileBy.ID, 'com.chinasofti.rcs:id/repager_text'),
        'com.chinasofti.rcs:id/welfare': (MobileBy.ID, 'com.chinasofti.rcs:id/welfare'),

        '多重好礼等你来领': (MobileBy.ID, 'com.chinasofti.rcs:id/wfCopywriting'),
        '关于和飞信': (MobileBy.ID, 'com.chinasofti.rcs:id/about_app_text'),
        '推荐好友，赚现金红包': (MobileBy.ID, 'com.chinasofti.rcs:id/wfCopywriting'),
        '分享客户端': (MobileBy.ID, 'com.chinasofti.rcs:id/share_app_text'),
        'com.chinasofti.rcs:id/feedback': (MobileBy.ID, 'com.chinasofti.rcs:id/feedback'),
        '帮助与反馈': (MobileBy.ID, 'com.chinasofti.rcs:id/feedback_text'),
        'com.chinasofti.rcs:id/setting': (MobileBy.ID, 'com.chinasofti.rcs:id/setting'),
        '姓名': (MobileBy.ID, 'com.chinasofti.rcs:id/card_name'),
        "联系人管理":("com.chinasofti.rcs:id/manage_contact_text")
    }

    @TestLogger.log()
    def click_message_button(self):
        """点击消息"""
        self.click_element(self.__class__.__locators["消息"])

    @TestLogger.log('点击二维码图标')
    def click_qr_code_icon(self):
        self.click_element(self.__locators['二维码入口'])

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在我的页面"""
        el = self.get_elements(self.__locators['查看并编辑个人资料'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def click_view_edit(self):
        """点击查看并编辑资料按钮"""
        self.click_element(self.__locators['查看并编辑个人资料'])

    @TestLogger.log()
    def click_call_multiparty(self, timeout=60):
        """点击多方电话"""
        self.wait_until(
            timeout=timeout,
            condition=lambda d: self.get_element(self.__locators['和飞信电话可用时长'])
        ).click()

    @TestLogger.log()
    def click_welfare(self):
        """点击福利按钮"""
        self.click_element(self.__class__.__locators['福利'])

    @TestLogger.log()
    def click_collection(self):
        """点击收藏按钮"""
        self.click_element(self.__locators['收藏'])













    @TestLogger.log('点击个人名片头像')
    def click_head(self):
        self.click_element(self.__locators['个人头像'])

    @TestLogger.log()
    def wait_for_head_load(self, timeout=60, auto_accept_alerts=True):
        """等待个人名片头像加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["个人头像"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self



    @TestLogger.log('点击移动营业厅')
    def click_mobile_hall_butten(self):
        self.click_element(self.__locators['移动营业厅'])

    @TestLogger.log("点击菜单项")
    def click_menu(self, menu):
        locator = [MobileBy.XPATH, '//*[@text="{}"]'.format(menu)]
        self._find_menu(locator)
        self.click_element(locator)

    @TestLogger.log("回到列表顶部")
    def scroll_to_top(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['菜单区域'])
        )
        # 如果找到“短信设置”菜单，则当作已经滑到底部
        if self._is_on_the_start_of_menu_view():
            return True
        max_try = 5
        current = 0
        while current < max_try:
            current += 1
            self.page_up()
            if self._is_on_the_start_of_menu_view():
                break
        return True

    @TestLogger.log("滑到菜单底部")
    def scroll_to_bottom(self):
        """滑到菜单底部"""
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['页头-我'])
        )

        # 如果找到“设置”菜单，则当作已经滑到底部
        if self._is_on_the_end_of_menu_view():
            return True
        max_try = 5
        current = 0
        while current < max_try:
            current += 1
            self.page_down()
            if self._is_on_the_end_of_menu_view():
                break
        return True

    @TestLogger.log("点击设置菜单")
    def click_setting_menu(self):
        """点击设置菜单"""
        self.scroll_to_bottom()
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['设置'])
        ).click()

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """判断页面是否包含选中状态的“我”页脚标签"""
        try:
            self.wait_until(
                condition=lambda d: self.get_element(self.__locators['我']),
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    # @TestLogger.log("下一页")
    # def page_down(self):
    #     self.wait_until(
    #         condition=lambda d: self.get_element(self.__locators['菜单区域'])
    #     )
    #     self.swipe_by_direction(self.__locators['菜单区域'], 'up')
    #
    # @TestLogger.log("下一页")
    # def page_up(self):
    #     self.wait_until(
    #         condition=lambda d: self.get_element(self.__locators['菜单区域'])
    #     )
    #     self.swipe_by_direction(self.__locators['菜单区域'], 'down')

    @TestLogger.log()
    def _find_menu(self, locator):
        if not self._is_element_present(locator):
            # 找不到就翻页找到菜单再点击，
            self.scroll_to_top()
            if self._is_element_present(locator):
                return
            max_try = 5
            current = 0
            while current < max_try:
                current += 1
                self.page_down()
                if self._is_element_present(locator):
                    return
                if self._is_on_the_end_of_menu_view():
                    raise NoSuchElementException('页面找不到元素：{}'.format(locator))

    def _is_on_the_start_of_menu_view(self):
        """判断是否在菜单开头"""
        return self._is_element_present(self.__locators['电话号码'])

    def _is_on_the_end_of_menu_view(self):
        """判断是否在菜单开头"""
        return self._is_element_present(self.__locators['设置'])

    @TestLogger.log()
    def click_help_menu(self, timeout=60):
        """点击帮助与反馈菜单"""
        self.scroll_to_bottom()
        self.wait_until(
            timeout=timeout,
            condition=lambda d: self.get_element(self.__locators['帮助与反馈'])
        ).click()


    @TestLogger.log()
    def is_element_exist(self, text):
        """当前页面是否包含此元素"""
        return self._is_element_present(self.__locators[text])

    @TestLogger.log()
    def is_text_exist(self, text):
        """当前页面是否包含此元素"""
        return self.is_text_present(text)


    @TestLogger.log()
    def wait_for_me_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待我页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["二维码入口"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self



    @TestLogger.log()
    def _find_text_menu(self, locator):
        import time
        if not self.is_text_present(locator):
            # 找不到就翻页找到菜单再点击，
            self.scroll_to_top()
            time.sleep(1.5)
            if self.is_text_present(locator):
                return True
            max_try = 5
            current = 0
            while current < max_try:
                current += 1
                self.page_down()
                time.sleep(1.5)
                if self.is_text_present(locator):
                    return True
                if self._is_on_the_end_of_menu_view():
                    return False

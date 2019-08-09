import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class OfficialAccountPage(BasePage):
    """公众号"""
    # ACTIVITY = 'com.rcs.rcspublicaccount.PublicAccountsListActivity'

    __locators = {
        '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
        '公众号': (MobileBy.ACCESSIBILITY_ID, '公众号'),
        '加号': (MobileBy.ACCESSIBILITY_ID, 'cc contacts add normal'),
        '订阅/服务号': (MobileBy.ACCESSIBILITY_ID, '订阅/服务号'),
        '企业号': (MobileBy.ACCESSIBILITY_ID, '企业号'),
        '公众号列表项': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeOther[1]'),
        '公众号头像': (MobileBy.ACCESSIBILITY_ID, '/var/mobile/Containers/Data/Application/3FF94A5C-59E9-4E2B-AA59-79FEC854AC76/Library/RCSData/headimage/4cc45369622d4a44066beafd18633c55_(null)'),
        '公众号名称': (MobileBy.XPATH, ''),
        '未关注任何企业号': (MobileBy.ACCESSIBILITY_ID, '未关注任何企业号'),
        '和飞信': (MobileBy.ACCESSIBILITY_ID, '和飞信'),
        '和飞信团队': (MobileBy.ACCESSIBILITY_ID, '和飞信团队'),
        '和飞信新闻': (MobileBy.ACCESSIBILITY_ID, '和飞信新闻'),
        '中国移动10086': (MobileBy.ACCESSIBILITY_ID, '中国移动10086'),
        #进入公众号
        'input_box': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeTextView/XCUIElementTypeTextView'),
        'send_button': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc chat send normal"'),
        'setting': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc chat message site normal"'),
        '发送失败': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc chat again send normal"'),
        '信息': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypeImage[1]'),
        '键盘': (MobileBy.ACCESSIBILITY_ID, 'cc chat public keyboardclose'),
        '键盘开启': (MobileBy.ACCESSIBILITY_ID, 'cc chat public keyboardopen'),
        '和飞信-底部菜单1': (MobileBy.IOS_PREDICATE, 'name CONTAINS "服务案例"'),
        '和飞信团队-底部菜单1': (MobileBy.XPATH, '//XCUIElementTypeOther[2]/XCUIElementTypeOther[4]'),
        '和飞信团队-底部菜单2': (MobileBy.XPATH, '//XCUIElementTypeOther[2]/XCUIElementTypeOther[5]'),
        '已发送消息列表': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeImage[1]'),
        '菜单1的菜单详情列表1': (MobileBy.ID, 'com.chinasofti.rcs:id/public_item_menu_name1'),
        '页面详情点击返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '表情详情': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iv_expression_image"]'),
        'message': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_message"]'),
        '取消': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
        '百度一下': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_title'),
        '百度连接':(MobileBy.XPATH, '//*[@text="www.baidu.com"]'),
        '进入公众号': (MobileBy.ACCESSIBILITY_ID, '进入公众号'),
        '查看历史资讯': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="查看历史资讯"])[1]'),
        '始终允许': (MobileBy.XPATH, "//*[contains(@text, '始终允许')]"),
        '认证主体': (MobileBy.ACCESSIBILITY_ID, '认证主体'),
        '功能介绍': (MobileBy.ACCESSIBILITY_ID, '功能介绍'),
        '更多': (MobileBy.ACCESSIBILITY_ID, 'cc chat more normal'),
        '接收消息推送': (MobileBy.XPATH, '(//XCUIElementTypeSwitch[@name="接收消息推送"])'),
        '置顶公众号': (MobileBy.XPATH, '(//XCUIElementTypeSwitch[@name="置顶公众号"])'),
        '搜索公众号': (MobileBy.IOS_PREDICATE, 'value == "搜索公众号"'),
        '键盘搜索': (MobileBy.XPATH, '//XCUIElementTypeButton[@name="Search"]'),
        '和飞信-头像': (MobileBy.XPATH, '//XCUIElementTypeImage[@name="/var/mobile/Containers/Data/Application/4C944BB2-9748-4EED-A53E-55FEB000419B/Library/RCSData/headimage/f084dac67d41685d1c22e99cc50d7c26_(null)"]'),
        '和飞信-名字': (MobileBy.XPATH, '//XCUIElementTypeStaticText[@name="和飞信"]'),
        '和飞信-功能': (MobileBy.XPATH, '//XCUIElementTypeStaticText[@name="和飞信负一屏直击企业痛点 专注为企业提供移动化办公解决方案 为企业、团队、群体提供个性化ict门户 为企业提高管理和运作效率。]'),
        '关注': (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="关注"])[1]'),
        '已关注': (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="已关注"])'),

    }

    @TestLogger.log('点击添加')
    def click_add(self):
        self.click_element(self.__locators['加号'])


    @TestLogger.log('点击企业号')
    def click_enterprise(self):
        self.click_element(self.__locators['企业号'])

    @TestLogger.log('检查企业号列表是否为空')
    def assert_enterprise_account_list_is_empty(self):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators['未关注任何企业号'])
            )
            self.element_text_should_be(
                self.__locators['未关注任何企业号'],
                '未关注任何企业号', '检查点：列表为空时显示默认文案：未关注任何企业号'
            )
        except TimeoutException:
            raise AssertionError("检查点：企业号列表为空")

    @TestLogger.log("setting")
    def page_contain_setting(self):
        """检查该页面是否包含某元素"""
        return self.page_should_contain_element(self.__locators['setting'])

    @TestLogger.log("检查对应元素是否存在")
    def page_contain_element(self, text='setting'):
        """检查该页面是否包含某元素"""
        return self.page_should_contain_element(self.__locators[text])

    @TestLogger.log("input_box")
    def page_contain_input_box(self):
        """检查该页面是否包含某元素"""
        return self.page_should_contain_element(self.__locators['input_box'])

    @TestLogger.log("send_button")
    def page_contain_send_button(self):
        """检查该页面是否包含某元素"""
        return self.page_should_contain_element(self.__locators['send_button'])

    # @TestLogger.log("expression")
    # def page_contain_expresssion(self):
    #     """检查该页面是否包含某元素"""
    #     return self.page_should_contain_element(self.__locators['expression'])

    @TestLogger.log("和飞信新闻")
    def page_contain_news(self):
        """检查该页面是否包含某元素"""
        return self.page_should_contain_element(self.__locators['和飞信新闻'])

    @TestLogger.log('检查发送失败按钮')
    def page_should_not_contain_sendfail_element(self):
        return self.page_should_not_contain_element(self.__locators['发送失败'])

    @TestLogger.log('存在发送失败按钮')
    def page_should_contain_sendfail_element(self):
        return self.page_should_contain_element(self.__locators['发送失败'])

    @TestLogger.log('点击发送失败按妞')
    def click_repeat_button(self):
        self.click_element(self.__locators['发送失败'])

    @TestLogger.log('使用坐标点击')
    def click_coordinate(self, x=1300, y=2450):
        # width = self.driver.get_window_size()["width"]
        # height = self.driver.get_window_size()["height"]

        # x_start = float(x) / 100 * width
        # y_end = float(y) / 100 * width
        x_start = x
        y_end = y
        self.tap_coordinate([(x_start, y_end)])

    @TestLogger.log('和飞信新闻')
    def click_officel_account(self):
        self.click_element(self.__locators['和飞信新闻'], 30)

    @TestLogger.log('点击和飞信公众号')
    def click_officel_account_hefeixin(self):
        self.click_element(self.__locators['和飞信'], 30)

    @TestLogger.log('点击输入框')
    def click_input_box(self):
        self.click_element(self.__locators['input_box'])

    @TestLogger.log('点击发送')
    def click_send_button(self):
        self.click_element(self.__locators['send_button'])

    @TestLogger.log('输入框信息')
    def input_message(self, text='good news'):
        self.input_text(self.__locators['input_box'], text)

    # @TestLogger.log('点击表情按钮')
    # def click_expression(self, text='expression'):
    #     self.click_element(self.__locators[text])

    @TestLogger.log('删除信息')
    def remove_message(self):
        if self.page_should_contain_element(self.__locators['信息']):
            self.click_element(self.__locators['信息'])
            el = self.get_element(self.__locators['信息'])
            self.driver.long_press(el, 1, 1, 2000)

    @TestLogger.log()
    def send_btn_is_clickable(self):
        """发送按钮是否可点击"""
        return self._is_clickable(self.__class__.__locators["send_button"])

    @TestLogger.log()
    def page_contain_keyboard(self):
        """页面应该包含键盘"""
        return self.page_should_contain_element(self.__class__.__locators['键盘'])

    @TestLogger.log()
    def page_should_contain_element_menu(self):
        """页面应该包含底部菜单栏"""
        return self.page_should_contain_element(self.__locators["和飞信-底部菜单1"])

    @TestLogger.log()
    def is_exist_element(self, locator='键盘'):
        return self._is_element_present(self.__class__.__locators[locator])

    @TestLogger.log('底部菜单栏1')
    def click_menu_name1(self):
        self.click_element(self.__locators['底部菜单1'])

    @TestLogger.log('菜单1的菜单详情列表1')
    def click_menu_detail_name1(self):
        self.click_element(self.__locators['菜单1的菜单详情列表1'])

    @TestLogger.log('页面详情点击返回')
    def click_menu_detail_back(self):
        self.click_element(self.__locators['页面详情点击返回'])

    @TestLogger.log('点击键盘')
    def click_keyboard(self):
        self.click_element(self.__locators['键盘'])

    @TestLogger.log()
    def click_expression_detail(self):
        """点击表情详情"""
        self.click_element(self.__locators['表情详情'])

    @TestLogger.log()
    def click_send_detail(self, text):
        """点击发送的内容"""
        self.click_text(text)

    @TestLogger.log()
    def page_should_contain_element_unsent(self):
        """页面应该包含未发送成功图标"""
        return self.page_should_contain_element(self.__locators["发送失败"])

    @TestLogger.log()
    def click_element_unsent(self):
        """点击未发送成功图标"""
        self.click_element(self.__locators['发送失败'])

    @TestLogger.log()
    def click_sure_resent(self):
        """点击确定重发"""
        self.click_element(self.__locators['确定'])

    @TestLogger.log()
    def click_not_resent(self):
        """点击取消重发"""
        self.click_element(self.__locators['取消'])

    @TestLogger.log()
    def page_not_contain_element_unsent(self):
        """页面不存在未发送成功图标"""
        self.page_should_not_contain_element(self.__locators['发送失败'])

    @TestLogger.log()
    def click_setting(self):
        """点击设置"""
        self.click_element(self.__locators['setting'])

    @TestLogger.log()
    def page_contain_element_message(self):
        """页面应该包含信息"""
        return self.page_should_contain_element(self.__locators["message"])

    @TestLogger.log()
    def page_not_contain_element_message(self):
        """页面不应该包含信息"""
        return self.page_should_not_contain_element(self.__locators["message"])

    @TestLogger.log('查看是否显示公众号')
    def is_public_in_list(self, name):
        time.sleep(1)
        groups = self.mobile.list_iterator(self.__locators['公众号列表'], self.__locators['公众号列表项'])
        for group in groups:
            if group.find_elements(MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/textview_user_name" and ' +
                                                   '@text="{}"]'.format(name)):
                return True
        return False

    @TestLogger.log()
    def is_element_present_message(self):
        return self._is_element_present(self.__locators["message"])

    @TestLogger.log('点击百度连接')
    def click_already_send_message(self):
        locator = (MobileBy.XPATH, '//XCUIElementTypeCell[last()-1]/XCUIElementTypeOther/XCUIElementTypeImage/XCUIElementTypeOther')
        self.click_element(locator)

    @TestLogger.log('点击确定')
    def click_sure_button(self):
        self.click_element(self.__locators['确定'])

    @TestLogger.log('点击设置')
    def click_setting_button(self):
        self.click_element(self.__locators['setting'])

    @TestLogger.log()
    def get_first_account(self):
        """获取第一个公众号的名称"""
        return self.get_elements(self.__class__.__locators['公众号名称'])[0].text
        # el = el[0]
        # return el.text

    @TestLogger.log()
    def get_account_title(self):
        """获取公众号标题名称"""
        return self.get_element(self.__locators['公众号标题-和飞信新闻']).text

    @TestLogger.log()
    def click_always_allowed(self):
        """获取通讯录权限点击始终允许"""
        if self.get_elements(self.__class__.__locators['弹出框点击允许']):
            self.click_element(self.__class__.__locators['弹出框点击允许'])

    @TestLogger.log('点击和飞信')
    def click_hefeixin(self):
        self.click_element(self.__locators['和飞信'])

    @TestLogger.log()
    def is_exist_receive_messages_open(self):
        """接收消息推送开启"""
        locator = (MobileBy.XPATH, '//XCUIElementTypeSwitch[@name="接收消息推送"][@value="1"]')
        return self._is_element_present(locator)

    @TestLogger.log('点击接收消息推送')
    def click_receive_messages(self):
        self.click_element(self.__locators['接收消息推送'])

    @TestLogger.log()
    def is_exist_top_official_account(self):
        """置顶公众号开启"""
        locator = (MobileBy.XPATH, '//XCUIElementTypeSwitch[@name="置顶公众号"][@value="1"]')
        return self._is_element_present(locator)

    @TestLogger.log('点击置顶公众号')
    def click_top_official_account(self):
        self.click_element(self.__locators['置顶公众号'])

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('输入公众号名字')
    def input_message_text(self, content):
        self.input_text(self.__locators['搜索公众号'], content)

    @TestLogger.log('点击键盘搜索')
    def click_key_search(self):
        self.click_element(self.__locators['键盘搜索'])

    @TestLogger.log()
    def page_contain_search_result(self):
        """公众号搜索结果"""
        return self.page_should_contain_element(self.__locators['和飞信-头像'])
        # return self.page_should_contain_element(self.__locators['和飞信-名字'])
        # return self.page_should_contain_element(self.__locators['和飞信-结果'])

    @TestLogger.log('点击关注')
    def click_follow(self):
        self.click_element(self.__locators['关注'])

    def get_follow_by_number(self):
        """当前页面有多少个已关注"""
        el = self.get_elements(self.__locators['已关注'])
        return len(el)

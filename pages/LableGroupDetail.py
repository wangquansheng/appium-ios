from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from .components import LabelSettingMenu
import time

class LableGroupDetailPage(LabelSettingMenu, BasePage):
    """标签分组详细页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.LabelContactListActivity'

    __locators = {
        #无成员-弹出框
        '取消': (MobileBy.ACCESSIBILITY_ID, '取消'),
        '添加成员': (MobileBy.XPATH, '(//XCUIElementTypeButton[@name="添加成员"])[2]'),
        #有成员
        '新增成员': (MobileBy.ACCESSIBILITY_ID, '添加成员'),
        '群发消息': (MobileBy.ACCESSIBILITY_ID, '群发消息'),
        '飞信电话': (MobileBy.ACCESSIBILITY_ID, '飞信电话'),
        '多发视频': (MobileBy.ACCESSIBILITY_ID, '多方视频'),
        '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
        '呼叫':(MobileBy.IOS_PREDICATE,'name CONTAINS "呼叫"'),
        '我知道了': (MobileBy.ACCESSIBILITY_ID, '我知道了'),
        '标题': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]'),
        '设置': (MobileBy.ACCESSIBILITY_ID, 'cc chat message site normal'),
        '成员头像1': (MobileBy.ACCESSIBILITY_ID, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeImage'),
        #标签分组-设置界面
        '标签名称': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="标签名称"])[1]'),
        '移除成员': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="移除成员"])[1]'),
        '删除标签': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="删除标签"])[1]'),
        # 删除标签分组页面-弹框
        # '取消': (MobileBy.ACCESSIBILITY_ID, '取消'),
        '删除': (MobileBy.ACCESSIBILITY_ID, '删除'),
        #修改标签名称页面
        '输入框': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeTextField'),
        '确定': (MobileBy.ACCESSIBILITY_ID, '确定'),
        '清除文本': (MobileBy.ACCESSIBILITY_ID, '清除文本'),
        #移除成员页面
        '搜索或输入手机号': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeTextField'),
        '清空搜索内容': (MobileBy.ACCESSIBILITY_ID, 'cc contacts delete pressed'),


        '群发信息': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_second_colum'),
        'com.chinasofti.rcs:id/layout_third_item': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_third_item'),
        'com.chinasofti.rcs:id/image_third_colum': (MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'),
        '多方电话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_third_colum'),
        'com.chinasofti.rcs:id/layout_fourth_item': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_fourth_item'),
        'com.chinasofti.rcs:id/image_fourth_colum': (MobileBy.ID, 'com.chinasofti.rcs:id/image_fourth_colum'),
        '多方视频': (MobileBy.ID, '多方视频'),

        '大佬1': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '大佬2': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '大佬3': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '标签分组成员名称': (MobileBy.XPATH, '//*[contains(@value, ", 1"]'),
        'com.chinasofti.rcs:id/contact_index_bar_view': (
            MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_view'),
        'com.chinasofti.rcs:id/contact_index_bar_container': (
            MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_container'),
        'F': (MobileBy.ID, ''),
    }

    @TestLogger.log('获取分组名字')
    def get_group_name(self):
        name = self.get_text(self.__locators['标题'])
        return name

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('点击返回')
    def is_exit_element(self,text='群发消息'):
        return self._is_element_present(self.__locators[text])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待通讯录页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["群发消息"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self



    @TestLogger.log('弹框点击取消')
    def click_cancel(self):
        if self.is_text_present('取消'):
            self.click_element(self.__locators['取消'])

    @TestLogger.log('弹框点击添加成员')
    def click_add_contact(self):
        self.click_element(self.__locators['添加成员'])

    @TestLogger.log('打开标签组设置菜单')
    def open_setting_menu(self):
        self.click_element(self.__class__.__locators['设置'])

    @TestLogger.log('点击群发信息')
    def click_send_group_info(self):
        """点击群发消息"""
        self.click_element(self.__locators['群发消息'])

    @TestLogger.log('点击添加成员')
    def click_add_members(self):
        """点击添加成员"""
        self.click_element(self.__locators['添加成员'])

    @TestLogger.log('点击飞信电话')
    def click_multi_tel(self):
        """点击飞信电话"""
        self.click_element(self.__locators['飞信电话'])

    @TestLogger.log("点击呼叫")
    def click_to_call(self):
        self.click_element(self.__class__.__locators['呼叫'])

    @TestLogger.log("呼叫弹框处理")
    def call_box_processing(self):
        if self.is_text_present('我知道了'):
            self.click_element(self.__class__.__locators['我知道了'])

    @TestLogger.log('点击多方视频')
    def click_multiparty_videos(self):
        """点击多方视频"""
        self.click_element(self.__locators['多方视频'])

    @TestLogger.log("呼叫弹框处理")
    def video_call_box_processing(self):
        if self.is_text_present('不允许'):
            self.click_element(MobileBy.ACCESSIBILITY_ID,'好')

#修改标签名称
    @TestLogger.log('点击确定')
    def click_chang_lable_group_name(self):
        """点击进入修改标签名称页面"""
        self.click_element(self.__locators['标签名称'])


    @TestLogger.log('点击确定')
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__locators['确定'])

    @TestLogger.log('点击确定')
    def click_input_box(self):
        """点击输入框"""
        self.click_element(self.__locators['输入框'])

    @TestLogger.log('点击确定')
    def input_group_new_name(self, name='bbb'):
        """点击输入框"""
        self.input_text(self.__locators['输入框'],name)

    @TestLogger.log('点击确定')
    def clear_group_name(self):
        """清除标签分组输入框内容"""
        self.click_element(self.__locators['清除文本'])


    @TestLogger.log('点击确定')
    def change_lable_group_name(self,name='bbb'):
        """修改标签分组名称"""
        self.click_element(self.__locators['标签名称'])
        time.sleep(2)
        self.click_element(self.__class__.__locators['输入框'])
        self.input_text(self.__class__.__locators['输入框'],name)
        time.sleep(2)
        self.click_element(self.__locators['确定'])
        self.click_back()

#移除成员页面

    @TestLogger.log("移除按钮")
    def click_move_label_contact(self):
        time.sleep(1)
        self.click_element(self.__locators['移除成员'])
        time.sleep(1)

    @TestLogger.log("通过名称选择要移除的联系人")
    def move_label_contact_by_name(self,name):
        time.sleep(1)
        self.click_element((MobileBy.ACCESSIBILITY_ID,'%s' % name))



    @TestLogger.log("点击搜索框")
    def click_search_box_move_label_contact(self):
        time.sleep(1)
        self.click_element(self.__locators['搜索或输入手机号'])


    @TestLogger.log()
    def input_search_text_move_lable(self, name='bbb'):
        """点击输入框"""
        self.input_text(self.__locators['搜索或输入手机号'],name)


    @TestLogger.log()
    def clear_search_text(self):
        """清空搜索内容"""
        self.click_element(self.__locators['清空搜索内容'])


#删除标签

    @TestLogger.log("点击删除标签分组")
    def delete_lable_group(self):
        time.sleep(1)
        self.click_element(self.__locators['删除标签'])

    @TestLogger.log()
    def click_cancel_delete(self):
        """点击取消删除"""
        self.click_element(self.__locators['取消'])

    @TestLogger.log()
    def click_sure_delete(self):
        """点击确定删除"""
        self.click_element(self.__locators['删除'])




    @TestLogger.log('检查点：当前页面为标签详情页')
    def assert_this_page_is_opened(self):
        try:
            self.wait_until(
                condition=lambda d: self.get_elements(self.__locators['添加成员'])
            )
        except TimeoutException:
            raise AssertionError('当前页面不是标签组详情页')

    @TestLogger.log("获取标签分组成员人名")
    def get_members_names(self):
        """获取标签分组成员人名"""
        els = self.get_elements(self.__class__.__locators['成员名字'])
        names = []
        if els:
            for el in els:
                names.append(el.text)
        return names

    @TestLogger.log()
    def is_exists_lable_group_setting(self):
        """是否存在标签分组设置按钮"""
        flag = False
        el = self.get_elements(self.__class__.__locators['设置'])
        if len(el) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def click_label_grouping_contacts(self, index=0):
        """通过下标点击标签分组成员名称"""
        el = self.get_elements(self.__class__.__locators['标签分组成员名称'])
        print(len(el))
        try:
            if len(el) > 0:
                el[index].click()
        except:
            raise IndexError("元素超出索引")

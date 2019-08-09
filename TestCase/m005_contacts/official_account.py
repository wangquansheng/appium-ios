import unittest

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.contacts import OfficialAccountPage, SearchOfficialAccountPage
from pages.contacts import OfficialAccountDetailPage
from preconditions.BasePreconditions import LoginPreconditions
import time
# import preconditions
import warnings


REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    # 'Android-移动': 'single_mobile',
    'IOS-移动': 'iphone',
    'IOS-移动-移动': 'M960BDQN229CHiphone8',
}


class Preconditions(LoginPreconditions):
    """
    分解前置条件
    """
    @staticmethod
    def connect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

    @staticmethod
    def disconnect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(category)
        client.disconnect_mobile()
        return client


    @staticmethod
    def take_logout_operation_if_already_login():
        """已登录状态，执行登出操作"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()

        me = MePage()
        me.scroll_to_bottom()
        me.scroll_to_bottom()
        me.scroll_to_bottom()
        me.click_setting_menu()

        setting = SettingPage()
        setting.scroll_to_bottom()
        setting.click_logout()
        setting.click_ok_of_alert()

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""
        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def terminate_app():
        """
        强制关闭app,退出后台
        :return:
        """
        app_id = current_driver().desired_capability['appPackage']
        current_mobile().termiate_app(app_id)

    @staticmethod
    def background_app():
        """后台运行"""
        current_mobile().press_home_key()

    @staticmethod
    def activate_app(app_id=None):
        """激活APP"""
        if not app_id:
            app_id = current_mobile().driver.desired_capabilities['appPackage']
        current_mobile().driver.activate_app(app_id)

    @staticmethod
    def make_sure_in_official_page():
        """确保在公众号页面"""
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        conts_page = ContactsPage()
        MessagePage().click_contacts()
        # conts_page.open_contacts_page()
        conts_page.click_official_account_icon()



class OfficialAccountTest(TestCase):
    """通讯录 - 公众号模块"""

    def default_setUp(self):
        """确保每个用例运行前在公众号页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.make_sure_in_official_page()

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0322(self):
        """订阅号/服务号列表显示"""
        conts_page = ContactsPage()
        time.sleep(2)
        conts_page.is_text_present('和飞信')
        conts_page.is_text_present('和飞信团队')
        conts_page.is_text_present('和飞信新闻')
        conts_page.is_text_present('中国移动10086')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0323(self):
        """企业号列表显示为空"""
        official_account = OfficialAccountPage()
        # 1.点击企业号
        official_account.click_enterprise()
        time.sleep(1)
        # 2.验证是否显示未关注任何企业号
        official_account.page_should_contain_text('未关注任何企业号')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0324(self):
        """公众号会话页面(未配置底部菜单栏)"""
        official = OfficialAccountPage()
        official.click_officel_account()
        time.sleep(2)
        official.page_contain_news()
        official.page_contain_setting()
        official.page_contain_input_box()
        official.page_contain_send_button()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0325(self):
        """公众号会话页面(配置底部菜单栏)"""
        official = OfficialAccountPage()
        official.click_officel_account_hefeixin()
        time.sleep(2)
        official.page_should_contain_text('和飞信')
        time.sleep(3)
        official.page_contain_setting()
        # self.assertTrue(official.is_exist_element(locator='键盘'))
        self.assertTrue(official.is_exist_element(locator='和飞信-底部菜单1'))
        # official.page_should_contain_element_menu()
        # 点击键盘
        official.click_keyboard()
        time.sleep(2)
        official.page_contain_input_box()
        official.page_contain_send_button()
        # 再次点击键盘图标
        official.click_keyboard()
        time.sleep(2)
        official.page_should_contain_element_menu()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0326(self):
        """公众号会话页面发送文本消息"""
        official = OfficialAccountPage()
        official.click_officel_account()
        time.sleep(2)
        official.click_input_box()
        official.input_message('good news')
        official.click_send_button()
        official.page_should_not_contain_sendfail_element()
        official.page_contain_element(text='已发送消息列表')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0332(self):
        """公众号会话页面右上角设置按钮"""
        official = OfficialAccountPage()
        # 1.点击和飞信新闻
        official.click_officel_account()
        # 2.点击设置
        official.click_setting_button()
        time.sleep(2)
        official_account_detail = OfficialAccountDetailPage()
        # 3.进入公众号详情页，验证是否显示标识
        official_account_detail.page_contain_public_title_name()
        official_account_detail.page_contain_public_name()
        official_account_detail.page_contain_public_header()
        official_account_detail.page_contain_public_number()
        official_account_detail.page_contain_features()
        official_account_detail.page_contain_certification()
        official_account_detail.page_should_contain_text('置顶公众号')
        official_account_detail.page_should_contain_text('查看历史资讯')
        official_account_detail.page_should_contain_text('进入公众号')
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0329(self):
        """公众号会话页面，发送长信息"""
        official = OfficialAccountPage()
        official.click_officel_account()
        time.sleep(2)
        official.click_input_box()
        mesaage = 'good news'*10
        official.input_message(mesaage)
        official.click_send_button()
        official.page_should_not_contain_sendfail_element()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0330(self):
        """公众号会话页面发送链接消息"""
        official = OfficialAccountPage()
        official.click_officel_account()
        time.sleep(2)
        official.click_input_box()
        mesaage = 'www.baidu.com'
        official.input_message(mesaage)
        official.click_send_button()
        official.page_should_not_contain_sendfail_element()
        time.sleep(2)
        official.click_already_send_message()
        ChatWindowPage().wait_for_page_load_web_message()
        if official.is_text_present('权限'):
            official.click_always_allowed()
        official.page_should_contain_text("百度一下")


    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_quxinli_0333(self):
        """公众号详情-接收消息推送"""
        official = OfficialAccountPage()
        # 1.点击和飞信
        official.click_hefeixin()
        # 2.点击设置
        official.click_setting_button()
        # 3.若接收消息推送关闭，则开启
        if not official.is_exist_receive_messages_open():
            official.click_receive_messages()
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_quxinli_0334(self):
        """公众号详情-置顶公众号"""
        official = OfficialAccountPage()
        # 1.点击和飞信
        official.click_hefeixin()
        # 2.点击设置
        official.click_setting_button()
        # 3.若置顶公众号关闭，则开启
        if not official.is_exist_top_official_account():
            official.click_top_official_account()
        # 4.返回消息页面
        official.click_back()
        official.click_back()
        official.click_back()
        conts_page = ContactsPage()
        conts_page.click_message_icon()
        mess = MessagePage()
        # 5.获取消息列表第一条的标题
        name = mess.assert_first_message_title_in_list_is()
        # 6.验证是否置顶
        if not name == "和飞信":
            raise AssertionError("公众号置顶未开启")
        Preconditions.make_sure_in_official_page()
        official.click_hefeixin()
        # 7.点击设置
        official.click_setting_button()
        # 8.置顶公众号关闭
        official.click_top_official_account()
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_quxinli_0335(self):
        """公众号详情-查看历史资讯"""
        official = OfficialAccountPage()
        # 1.点击和飞信新闻
        official.click_officel_account()
        # 2.点击设置
        official.click_setting_button()
        # 3.点击查看历史资讯
        oadp = OfficialAccountDetailPage()
        oadp.click_read_old_message()
        # 4.验证是否有历史资讯
        if oadp.is_contain_old_mes():
            print("有历史资讯")
        else:
            print("没有历史资讯")

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_quxinli_0341(self):
        """输入公众号包含关键字进行搜索"""
        official = OfficialAccountPage()
        # 1.点击+
        official.click_add()
        # 2.输入公众号名字
        official.input_message_text("和飞信")
        time.sleep(1)
        # 3.点击搜索
        official.click_key_search()
        # 4.验证是否存在搜索结果
        self.assertTrue(official.page_contain_search_result())

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_quxinli_0342(self):
        """公众号搜索结果关注公众号"""
        official = OfficialAccountPage()
        # 1.点击+
        official.click_add()
        # 2.输入公众号名字
        official.input_message_text("和飞信")
        time.sleep(1)
        # 3.点击搜索
        official.click_key_search()
        # 4.获取点击关注前，已关注个数
        number = official.get_follow_by_number()
        # 5.点击关注
        time.sleep(2)
        official.click_follow()
        time.sleep(2)
        # 6.获取点击关注后，已关注个数
        number1 = official.get_follow_by_number()
        # 7.验证是否关注成功（提示已关注）
        if not number1 == number+1:
            raise AssertionError("未关注成功")
        time.sleep(2)




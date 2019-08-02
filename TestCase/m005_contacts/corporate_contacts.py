import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.contacts import OfficialAccountPage
from pages.contacts.AllMyTeam import AllMyTeamPage
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage
from preconditions.BasePreconditions import LoginPreconditions, WorkbenchPreconditions
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
        """确保在企业联系人页面"""
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        conts_page = ContactsPage()
        MessagePage().click_contacts()
        conts_page.click_all_my_team()


class CorporateContactsTest(TestCase):
    """通讯录 - 企业联系人选择器"""

    def default_setUp(self):
        """确保每个用例运行前在企业联系人页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.make_sure_in_official_page()

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_chenjixiang_0724(self):
        """测试搜索输入框的X按钮是否可以清空内容"""
        team = AllMyTeamPage()
        # 1.点击搜索
        team.click_search()
        # 2.输入框输入内容
        team.input_message("大佬1")
        time.sleep(2)
        # 3.点击X清除
        team.click_clear()
        # 4.验证是否清除
        self.assertTrue(team.is_element_present_default_prompt())
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_chenjixiang_0732(self):
        """顶部标题为：选择联系人"""
        # 顶部标题为全部团队
        team = AllMyTeamPage()
        self.assertTrue(team.is_element_present_title())

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_chenjixiang_0769(self):
        """搜索框默认提示语修改为：搜索或输入手机号"""
        # 搜索框默认提示语修改为：输入关键字快速搜索
        team = AllMyTeamPage()
        # 1.点击搜索
        team.click_search()
        # 2.验证搜索框默认提示语修改为：输入关键字快速搜索
        self.assertTrue(team.is_element_present_default_prompt())

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_chenjixiang_0770(self):
        """点击搜索框，光标在搜索框时自动弹出键盘，点击其他区域后，键盘自动收起"""
        team = AllMyTeamPage()
        # 1.点击搜索
        team.click_search()
        # 2.验证是否弹出键盘
        self.assertTrue(team.is_element_present_key())
        # 3.点击其它区域
        team.click_coordinate()
        # 4.验证键盘是否收起
        self.assertFalse(team.is_element_present_key())

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_chenjixiang_0771(self):
        """进入搜索状态，搜索框默认提示语“搜索”"""
        # 进入搜索状态，搜索框默认提示语：输入关键字快速搜索
        team = AllMyTeamPage()
        # 1.点击搜索
        team.click_search()
        # 2.验证搜索框默认提示语修改为：输入关键字快速搜索
        self.assertTrue(team.is_element_present_default_prompt())

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_chenjixiang_0772(self):
        """输入框为空时，右侧不显示 一键消除 X 按钮"""
        team = AllMyTeamPage()
        # 1.点击搜索
        team.click_search()
        # 2.验证右侧不显示 一键消除 X 按钮
        self.assertFalse(team.is_element_present_clear())

    @tags('ALL', 'CONTACTS', 'CMCC', 'YX', 'YX_IOS')
    def test_contacts_chenjixiang_0773(self):
        """输入框有内容时，右侧显示 一键消除 X 按钮，点击X可清空内容"""
        team = AllMyTeamPage()
        # 1.点击搜索
        team.click_search()
        # 2.输入框输入内容
        team.input_message("大佬1")
        time.sleep(2)
        # 3.点击X清除
        team.click_clear()
        # 4.验证是否清除
        self.assertTrue(team.is_element_present_default_prompt())
        time.sleep(2)
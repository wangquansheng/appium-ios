import time

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile
from pages import MessagePage
from pages import WorkbenchPage
from pages.workbench.app_manage.AppManage import AppManagePage
from pages.workbench.app_store.AppStore import AppStorePage
from pages.workbench.enterprise_contacts.EnterpriseContacts import EnterpriseContactsPage
from pages.workbench.manager_console.WorkbenchManage import WorkbenchManagePage
from pages.workbench.super_meeting.SuperMeeting import SuperMeetingPage
from preconditions.BasePreconditions import WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""

    @staticmethod
    def make_already_in_message_page(reset=False):
        """确保应用在消息页面"""
        # 如果在消息页，不做任何操作
        mp = MessagePage()
        if mp.is_on_this_page():
            return
        else:
            try:
                current_mobile().launch_app()
                mp.wait_for_page_load()
            except:
                # 进入一键登录页
                Preconditions.make_already_in_one_key_login_page()
                #  从一键登录页面登录
                Preconditions.login_by_one_key_login()

    @staticmethod
    def enter_workbench_page():
        """进入工作台首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @staticmethod
    def enter_app_store_page():
        """进入应用商城首页"""

        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_app_store()
        asp = AppStorePage()
        asp.wait_for_page_load()

    @staticmethod
    def ensure_not_exists_personal_app_by_name(name):
        """确保不存在指定个人应用"""

        wbp = WorkbenchPage()
        if wbp.is_exists_app_by_name(name):
            wbp.click_app_manage()
            amp = AppManagePage()
            amp.wait_for_page_load()
            amp.click_remove_icon_by_name(name)
            amp.click_sure()
            time.sleep(2)
            amp.click_back_button()
            wbp.wait_for_page_load()

    @staticmethod
    def ensure_not_exists_app_by_name(name):
        """确保不存在指定应用"""

        wbp = WorkbenchPage()
        if wbp.is_exists_app_by_name(name):
            wbp.click_workbench_manage()
            wmp = WorkbenchManagePage()
            wmp.wait_for_page_load()
            wmp.click_remove_icon_by_app_name(name)
            time.sleep(5)
            wmp.click_back_button()
            wbp.wait_for_page_load()


class AppStoreAllTest(TestCase):

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在工作台首页
        """

        Preconditions.select_mobile('IOS-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_workbench_page()
            return
        wbp = WorkbenchPage()
        if not wbp.is_on_workbench_page():
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_workbench_page()

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0001(self):
        """检查工作台进入应用商城入口是否正确"""

        # 进入应用商城首页
        Preconditions.enter_app_store_page()
        asp = AppStorePage()
        # 1.等待应用商城首页加载
        asp.wait_for_page_load()
        asp.click_back_button()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0002(self):
        """检查【>】返回按钮控件是否正确"""

        # 进入应用商城首页
        Preconditions.enter_app_store_page()
        asp = AppStorePage()
        asp.wait_for_page_load()
        asp.click_back_button()
        wbp = WorkbenchPage()
        # 1.等待工作台页面加载
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0003(self):
        """搜索未添加个人应用添加"""

        # 确保不存在指定个人应用
        app_name = "咪咕影院"
        Preconditions.ensure_not_exists_personal_app_by_name(app_name)
        # 添加工作台里的应用
        wbp = WorkbenchPage()
        wbp.click_app_store()
        asp = AppStorePage()
        asp.wait_for_page_load()
        # 点击搜索应用
        asp.click_search_app()
        # 1.等待搜索页加载
        asp.wait_for_search_page_load()
        asp.input_store_name(app_name)
        # 2.搜索栏是否显示指定文本
        self.assertEquals(asp.get_search_box_text(), app_name)
        asp.click_search()
        time.sleep(5)
        # 3.搜索关键词是否展示在搜索结果列表中
        self.assertEquals(asp.is_search_result_match(app_name), True)
        # 4.点击添加
        asp.click_join()
        asp.click_sure()
        # 5.添加成功，返回搜索页，搜索栏是否清空(部分验证点变动)
        asp.wait_for_search_page_load()
        time.sleep(5)
        self.assertEquals(asp.get_search_box_text(), "搜索应用")
        asp.click_close()
        wbp.wait_for_page_load()
        # 6.工作台新增个人应用分组，是否存在指定应用图标(部分验证点变动)
        # self.assertEquals(wbp.is_exists_app_by_name("个人应用"), True)
        self.assertEquals(wbp.is_exists_app_by_name(app_name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0004(self):
        """搜索未添加个人应用进入应用介绍页添加"""

        # 确保不存在指定个人应用
        app_name = "网易考拉"
        Preconditions.ensure_not_exists_personal_app_by_name(app_name)
        # 添加工作台里的应用
        wbp = WorkbenchPage()
        wbp.click_app_store()
        asp = AppStorePage()
        asp.wait_for_page_load()
        # 点击搜索应用
        asp.click_search_app()
        # 1.等待搜索页加载
        asp.wait_for_search_page_load()
        asp.input_store_name(app_name)
        # 2.搜索栏是否显示指定文本
        self.assertEquals(asp.get_search_box_text(), app_name)
        asp.click_search()
        time.sleep(5)
        # 3.搜索关键词是否展示在搜索结果列表中
        self.assertEquals(asp.is_search_result_match(app_name), True)
        # 点击搜索结果，进入应用介绍页
        asp.click_search_result()
        # 4.等待应用介绍详情页加载
        asp.wait_for_app_details_page_load()
        # 5.点击添加
        asp.click_join()
        asp.click_sure()
        time.sleep(2)
        asp.click_back_button()
        # 6.添加成功，返回搜索页，搜索栏内容保存
        asp.wait_for_search_page_load()
        self.assertEquals(asp.get_search_box_text(), app_name)
        asp.click_close()
        wbp.wait_for_page_load()
        # 7.工作台新增个人应用分组，是否存在指定应用图标(部分验证点变动)
        # self.assertEquals(wbp.is_exists_app_by_name("个人应用"), True)
        self.assertEquals(wbp.is_exists_app_by_name(app_name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0007(self):
        """个人专区添加应用"""

        # 确保不存在指定应用
        app_name = "帮助中心"
        Preconditions.ensure_not_exists_personal_app_by_name(app_name)
        # Preconditions.ensure_not_exists_app_by_name(app_name)
        # 添加工作台里的应用
        wbp = WorkbenchPage()
        wbp.click_app_store()
        asp = AppStorePage()
        asp.wait_for_page_load()
        # 1.点击个人专区
        asp.click_personal_area()
        asp.wait_for_personal_area_page_load()
        # 2.添加指定应用
        asp.add_app_by_name(app_name)
        asp.click_sure()
        # asp.click_add_app()
        # 3.添加成功，添加按钮是否变化为打开按钮(部分验证点变动)
        # self.assertEquals(asp.page_should_contain_text2("添加应用成功"), True)
        asp.wait_for_personal_area_page_load()
        self.assertEquals(asp.get_app_button_text_by_name(app_name), "打开")
        asp.click_back_button()
        wbp.wait_for_page_load()
        # 4.工作台新增个人应用分组，是否存在指定应用图标(部分验证点变动)
        # self.assertEquals(wbp.is_exists_app_by_name("个人应用"), True)
        self.assertEquals(wbp.is_exists_app_by_name(app_name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0008(self):
        """个人专区进入应用介绍页添加应用"""

        # 确保不存在指定个人应用
        app_name = "政企优惠"
        Preconditions.ensure_not_exists_personal_app_by_name(app_name)
        # 添加工作台里的应用
        wbp = WorkbenchPage()
        wbp.click_app_store()
        asp = AppStorePage()
        asp.wait_for_page_load()
        # 1.点击个人专区
        asp.click_personal_area()
        asp.wait_for_personal_area_page_load()
        # 进入应用介绍页
        asp.click_app(app_name)
        # 2.等待应用介绍详情页加载
        asp.wait_for_app_details_page_load()
        # 3.点击添加
        asp.click_join()
        asp.click_sure()
        time.sleep(2)
        asp.click_back_button()
        asp.wait_for_personal_area_page_load()
        # 4.添加成功，添加按钮是否变化为打开按钮(部分验证点变动)
        # self.assertEquals(asp.get_app_button_text_by_name(app_name), "打开")
        asp.click_back_button()
        wbp.wait_for_page_load()
        # 5.工作台新增个人应用分组，是否存在指定应用图标(部分验证点变动)
        # self.assertEquals(wbp.is_exists_app_by_name("个人应用"), True)
        self.assertEquals(wbp.is_exists_app_by_name(app_name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0011(self):
        """管理员搜索未添加企业应用时添加"""

        # 确保不存在指定应用
        app_name = "人事管理"
        Preconditions.ensure_not_exists_app_by_name(app_name)
        # 添加工作台里的应用
        wbp = WorkbenchPage()
        wbp.click_app_store()
        asp = AppStorePage()
        asp.wait_for_page_load()
        # 点击搜索应用
        asp.click_search_app()
        # 1.等待搜索页加载
        asp.wait_for_search_page_load()
        asp.input_store_name(app_name)
        # 2.搜索栏是否显示指定文本
        self.assertEquals(asp.get_search_box_text(), app_name)
        asp.click_search()
        time.sleep(5)
        # 3.搜索关键词是否展示在搜索结果列表中
        self.assertEquals(asp.is_search_result_match(app_name), True)
        asp.click_join()
        # 4.等待应用分组页加载
        asp.wait_for_app_group_page_load()
        # 5.选择应用分组（勾选状态没有可辨识标识，无法验证）
        asp.click_accessibility_id_attribute_by_name("特色通讯")
        asp.click_add_app()
        # 6.添加成功，返回进入移动办公套件应用列表，添加按钮是否变化为打开按钮
        self.assertEquals(asp.page_should_contain_text2("添加应用成功"), True)
        asp.wait_for_search_page_load()
        # 进入移动办公套件应用列表
        asp.click_back_button()
        asp.wait_for_page_load()
        asp.click_name_attribute_by_name("分类")
        asp.wait_for_classification_page_load()
        asp.click_accessibility_id_attribute_by_name("移动办公套件")
        self.assertEquals(asp.get_app_button_text_by_name(app_name), "打开")
        asp.click_close()
        wbp.wait_for_page_load()
        # 解决工作台没有及时刷新问题
        current_mobile().launch_app()
        Preconditions.enter_workbench_page()
        # 7.工作台是否存在指定应用图标
        self.assertEquals(wbp.is_exists_app_by_name(app_name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0012(self):
        """管理员搜索未添加企业应用进入应用介绍页时添加"""

        # 确保不存在指定应用
        app_name = "移动报销"
        Preconditions.ensure_not_exists_app_by_name(app_name)
        # 添加工作台里的应用
        wbp = WorkbenchPage()
        wbp.click_app_store()
        asp = AppStorePage()
        asp.wait_for_page_load()
        # 点击搜索应用
        asp.click_search_app()
        # 1.等待搜索页加载
        asp.wait_for_search_page_load()
        asp.input_store_name(app_name)
        # 2.搜索栏是否显示指定文本
        self.assertEquals(asp.get_search_box_text(), app_name)
        asp.click_search()
        time.sleep(5)
        # 3.搜索关键词是否展示在搜索结果列表中
        self.assertEquals(asp.is_search_result_match(app_name), True)
        # 点击搜索结果，进入应用介绍页
        asp.click_search_result()
        # 4.等待应用介绍详情页加载
        asp.wait_for_app_details_page_load()
        asp.click_join()
        # 5.等待应用分组页加载
        asp.wait_for_app_group_page_load()
        # 6.选择应用分组（勾选状态没有可辨识标识，无法验证）
        asp.click_accessibility_id_attribute_by_name("特色通讯")
        asp.click_add_app()
        # 7.添加成功，返回进入移动办公套件应用列表，添加按钮是否变化为打开按钮
        self.assertEquals(asp.page_should_contain_text2("添加应用成功"), True)
        # 进入移动办公套件应用列表
        time.sleep(2)
        asp.click_back_button()
        asp.wait_for_search_page_load()
        asp.click_back_button()
        asp.wait_for_page_load()
        asp.click_name_attribute_by_name("分类")
        asp.wait_for_classification_page_load()
        asp.click_accessibility_id_attribute_by_name("移动办公套件")
        self.assertEquals(asp.get_app_button_text_by_name(app_name), "打开")
        asp.click_close()
        wbp.wait_for_page_load()
        # 解决工作台没有及时刷新问题
        current_mobile().launch_app()
        Preconditions.enter_workbench_page()
        # 8.工作台是否存在指定应用图标
        self.assertEquals(wbp.is_exists_app_by_name(app_name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0013(self):
        """分类-管理员添加应用"""

        # 确保不存在指定应用
        app_name = "考试评测"
        Preconditions.ensure_not_exists_app_by_name(app_name)
        # 添加工作台里的应用
        wbp = WorkbenchPage()
        wbp.click_app_store()
        asp = AppStorePage()
        asp.wait_for_page_load()
        # 1.点击分类
        asp.click_name_attribute_by_name("分类")
        asp.wait_for_classification_page_load()
        # 2.点击移动办公套件
        asp.click_accessibility_id_attribute_by_name("移动办公套件")
        asp.add_app_by_name(app_name)
        # 3.等待应用分组页加载
        asp.wait_for_app_group_page_load()
        # 4.选择应用分组（勾选状态没有可辨识标识，无法验证）
        asp.click_accessibility_id_attribute_by_name("特色通讯")
        asp.click_add_app()
        # 5.添加成功，返回进入移动办公套件应用列表，添加按钮是否变化为打开按钮(部分验证点变动)
        self.assertEquals(asp.page_should_contain_text2("添加应用成功"), True)
        # self.assertEquals(asp.get_app_button_text_by_name(app_name), "打开")
        time.sleep(2)
        asp.click_close()
        wbp.wait_for_page_load()
        # 解决工作台没有及时刷新问题
        current_mobile().launch_app()
        Preconditions.enter_workbench_page()
        # 6.工作台是否存在指定应用图标
        self.assertEquals(wbp.is_exists_app_by_name(app_name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0014(self):
        """分类-管理员应用介绍页添加应用"""

        # 确保不存在指定应用
        app_name = "企业云盘"
        Preconditions.ensure_not_exists_app_by_name(app_name)
        # 添加工作台里的应用
        wbp = WorkbenchPage()
        wbp.click_app_store()
        asp = AppStorePage()
        asp.wait_for_page_load()
        # 1.点击分类
        asp.click_name_attribute_by_name("分类")
        asp.wait_for_classification_page_load()
        # 2.点击移动办公套件
        asp.click_accessibility_id_attribute_by_name("移动办公套件")
        # 进入应用介绍页
        asp.click_text_by_name(app_name)
        # 3.等待应用介绍详情页加载
        asp.wait_for_app_details_page_load()
        asp.click_join()
        # 4.等待应用分组页加载
        asp.wait_for_app_group_page_load()
        # 5.选择应用分组（勾选状态没有可辨识标识，无法验证）
        asp.click_accessibility_id_attribute_by_name("特色通讯")
        asp.click_add_app()
        # 6.添加成功，返回进入移动办公套件应用列表，添加按钮是否变化为打开按钮(部分验证点变动)
        self.assertEquals(asp.page_should_contain_text2("添加应用成功"), True)
        time.sleep(2)
        asp.click_back_button()
        # self.assertEquals(asp.get_app_button_text_by_name(app_name), "打开")
        asp.click_close()
        wbp.wait_for_page_load()
        # 解决工作台没有及时刷新问题
        current_mobile().launch_app()
        Preconditions.enter_workbench_page()
        # 7.工作台是否存在指定应用图标
        self.assertEquals(wbp.is_exists_app_by_name(app_name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0015(self):
        """验证brenner图>1时是否正常切换"""

        # 进入应用商城首页
        Preconditions.enter_app_store_page()
        asp = AppStorePage()
        asp.wait_for_page_load()
        # 1.滑动brenner图
        asp.swipe_by_brenner1()
        time.sleep(1)
        asp.swipe_by_brenner2()
        asp.click_back_button()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0016(self):
        """验证点击brenner图是否跳转正确"""

        # 进入应用商城首页
        Preconditions.enter_app_store_page()
        asp = AppStorePage()
        asp.wait_for_page_load()
        # 点击brenner图
        asp.click_brenner()
        # 1.等待应用介绍详情页加载
        asp.wait_for_app_details_page_load()
        asp.click_back_button()
        asp.wait_for_page_load()
        asp.click_back_button()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0018(self):
        """检查【X】返回按钮控件是否正确"""

        # 进入应用商城首页
        Preconditions.enter_app_store_page()
        asp = AppStorePage()
        asp.wait_for_page_load()
        # 进入应用商城二三级页面
        asp.click_name_attribute_by_name("超级会议")
        asp.wait_for_app_details_page_load()
        asp.click_close()
        wbp = WorkbenchPage()
        # 1.等待工作台页面加载
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YYSC_0019(self):
        """验证点击打开按钮是否跳转正确"""

        # 进入应用商城首页
        Preconditions.enter_app_store_page()
        asp = AppStorePage()
        wbp = WorkbenchPage()
        asp.wait_for_page_load()
        # 搜索应用
        asp.click_search_app()
        search_name = "企业通讯录"
        asp.wait_for_search_page_load()
        asp.input_store_name(search_name)
        asp.click_search()
        time.sleep(5)
        # 打开应用
        asp.click_open()
        # 1.等待应用首页加载
        ecp = EnterpriseContactsPage()
        ecp.wait_for_page_load()
        ecp.click_back_button(2)
        asp.wait_for_search_page_load()
        asp.click_back_button()
        asp.wait_for_page_load()
        # 进入应用介绍页
        asp.click_name_attribute_by_name("超级会议")
        asp.wait_for_app_details_page_load()
        # 打开应用
        asp.click_open()
        smp = SuperMeetingPage()
        # 2.等待应用首页加载
        smp.wait_for_page_loads()
        smp.click_close()
        wbp.wait_for_page_load()
import time

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile
from pages import MessagePage
from pages import WorkbenchPage
from pages.workbench.app_store.AppStore import AppStorePage
from pages.workbench.manager_console.WorkbenchManage import WorkbenchManagePage
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

    @staticmethod
    def ensure_exists_app_by_name(name):
        """确保存在指定应用"""

        wbp = WorkbenchPage()
        if not wbp.is_exists_app_by_name(name):
            wbp.click_app_store()
            asp = AppStorePage()
            asp.wait_for_page_load()
            asp.click_search_app()
            asp.input_store_name(name)
            asp.click_search()
            time.sleep(5)
            asp.click_join()
            asp.wait_for_app_group_page_load()
            asp.click_add_app()
            asp.click_close()
            time.sleep(5)
            wbp.wait_for_page_load()


class WorkbenchManageAllTest(TestCase):

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
    def test_GZTGL_0001(self):
        """搜索出应用再添加到分组"""

        # 确保应用未添加
        app_name = "人事管理"
        Preconditions.ensure_not_exists_app_by_name(app_name)
        wbp = WorkbenchPage()
        # 点击“工作台管理”
        wbp.click_workbench_manage()
        wmp = WorkbenchManagePage()
        wmp.wait_for_page_load()
        # 点击页面“常用应用”下的“+”号
        wmp.click_add_icon()
        asp = AppStorePage()
        asp.wait_for_page_load()
        asp.click_search_app()
        asp.wait_for_search_page_load()
        # 搜索未添加到工作台应用名称，且这个应用在应用商城中存在
        asp.input_store_name(app_name)
        asp.click_search()
        time.sleep(5)
        # 点击搜索出应用的添加按钮
        asp.click_join()
        asp.wait_for_app_group_page_load()
        # 选择分组，点击“添加应用”
        asp.click_accessibility_id_attribute_by_name("特色通讯")
        asp.click_add_app()
        # 1.成功添加应用
        self.assertEquals(asp.page_should_contain_text2("添加应用成功"), True)
        asp.wait_for_search_page_load()
        asp.click_close()
        wbp.wait_for_page_load()
        # 2.返回工作台页面可以在添加的分组中找到这个应用
        self.assertEquals(wbp.is_exists_app_by_name(app_name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GZTGL_0002(self):
        """搜索出应用，在应用介绍页面添加应用"""

        # 确保应用未添加
        app_name = "移动报销"
        Preconditions.ensure_not_exists_app_by_name(app_name)
        wbp = WorkbenchPage()
        # 点击“工作台管理”
        wbp.click_workbench_manage()
        wmp = WorkbenchManagePage()
        wmp.wait_for_page_load()
        # 点击页面“常用应用”下的“+”号
        wmp.click_add_icon()
        asp = AppStorePage()
        asp.wait_for_page_load()
        asp.click_search_app()
        asp.wait_for_search_page_load()
        # 搜索未添加到工作台应用名称，且这个应用在应用商城中存在
        asp.input_store_name(app_name)
        asp.click_search()
        time.sleep(5)
        # 点击搜索结果应用，进入应用介绍页
        asp.click_search_result()
        asp.wait_for_app_details_page_load()
        # 点击添加按钮
        asp.click_join()
        asp.wait_for_app_group_page_load()
        # 选择分组，点击“添加应用”
        asp.click_accessibility_id_attribute_by_name("特色通讯")
        asp.click_add_app()
        # 1.成功添加应用
        self.assertEquals(asp.page_should_contain_text2("添加应用成功"), True)
        asp.click_close()
        wbp.wait_for_page_load()
        # 2.返回工作台页面可以在添加的分组中找到这个应用
        self.assertEquals(wbp.is_exists_app_by_name(app_name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GZTGL_0003(self):
        """搜索不存在的应用名称"""

        wbp = WorkbenchPage()
        # 点击“工作台管理”
        wbp.click_workbench_manage()
        wmp = WorkbenchManagePage()
        wmp.wait_for_page_load()
        # 点击页面“常用应用”下的“+”号
        wmp.click_add_icon()
        asp = AppStorePage()
        asp.wait_for_page_load()
        asp.click_search_app()
        asp.wait_for_search_page_load()
        # 搜索应用商城不存在的应用名称
        asp.input_store_name("哈哈")
        asp.click_search()
        # 1.无搜索结果，页面提示“暂无相关应用”
        self.assertEquals(asp.page_should_contain_text2("暂无相关的应用"), True)
        asp.click_close()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GZTGL_0004(self):
        """在分类列表中添加应用到分组中"""

        # 确保应用未添加
        app_name = "考试评测"
        Preconditions.ensure_not_exists_app_by_name(app_name)
        wbp = WorkbenchPage()
        # 点击“工作台管理”
        wbp.click_workbench_manage()
        wmp = WorkbenchManagePage()
        wmp.wait_for_page_load()
        # 点击页面“常用应用”下的“+”号
        wmp.click_add_icon()
        asp = AppStorePage()
        # 进入应用分类，打开分类
        asp.wait_for_page_load()
        asp.click_name_attribute_by_name("分类")
        asp.wait_for_classification_page_load()
        asp.click_accessibility_id_attribute_by_name("移动办公套件")
        self.assertEquals(asp.page_should_contain_text2("官方"), True)
        # 选择未添加的应用，点击“添加”
        asp.add_app_by_name(app_name)
        asp.wait_for_app_group_page_load()
        # 选择分组，点击“添加应用”
        asp.click_accessibility_id_attribute_by_name("特色通讯")
        asp.click_add_app()
        # 1.成功添加应用
        self.assertEquals(asp.page_should_contain_text2("添加应用成功"), True)
        self.assertEquals(asp.page_should_contain_text2("官方"), True)
        # 返回到工作台管理页面，再返回到工作台页
        asp.click_back_button(2)
        wmp.wait_for_page_load()
        wmp.click_back_button()
        wbp.wait_for_page_load()
        # 2.返回工作台页面可以在添加的分组中找到这个应用
        self.assertEquals(wbp.is_exists_app_by_name(app_name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GZTGL_0005(self):
        """在应用介绍页面成功添加应用到分组中"""

        # 确保应用未添加
        app_name = "企业云盘"
        Preconditions.ensure_not_exists_app_by_name(app_name)
        wbp = WorkbenchPage()
        # 点击“工作台管理”
        wbp.click_workbench_manage()
        wmp = WorkbenchManagePage()
        wmp.wait_for_page_load()
        # 点击页面“常用应用”下的“+”号
        wmp.click_add_icon()
        asp = AppStorePage()
        # 进入应用分类，打开分类
        asp.wait_for_page_load()
        asp.click_name_attribute_by_name("分类")
        asp.wait_for_classification_page_load()
        asp.click_accessibility_id_attribute_by_name("移动办公套件")
        self.assertEquals(asp.page_should_contain_text2("官方"), True)
        # 选择未添加的应用，点击应用进入详情页面
        asp.click_text_by_name(app_name)
        asp.wait_for_app_details_page_load()
        # 点击“添加”
        asp.click_join()
        asp.wait_for_app_group_page_load()
        # 选择分组
        asp.click_accessibility_id_attribute_by_name("特色通讯")
        # 点击“添加应用”
        asp.click_add_app()
        # 1.提示“添加成功”
        self.assertEquals(asp.page_should_contain_text2("添加应用成功"), True)
        asp.wait_for_app_details_page_load()
        # 返回到工作台管理页面，再返回到工作台页面
        asp.click_back_button(3)
        wmp.wait_for_page_load()
        wmp.click_back_button()
        wbp.wait_for_page_load()
        # 2.返回首页可以看到添加的应用出现在指定的分组当中
        self.assertEquals(wbp.is_exists_app_by_name(app_name), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GZTGL_0006(self):
        """删除应用"""

        # 确保存在指定应用
        app_name = "人事管理"
        Preconditions.ensure_exists_app_by_name(app_name)
        wbp = WorkbenchPage()
        # 点击“工作台管理”，进入工作台管理页
        wbp.click_workbench_manage()
        wmp = WorkbenchManagePage()
        wmp.wait_for_page_load()
        # 点击要删除应用右上角的“x”符号
        wmp.click_remove_icon_by_app_name(app_name)
        # 1.弹窗显示移除应用成功，自动刷新工作台管理页面，发现刚刚删除的应用已不存在
        self.assertEquals(wmp.page_should_contain_text2("移除成功"), True)
        time.sleep(5)
        wmp.wait_for_page_load()
        self.assertEquals(wmp.page_should_contain_text2(app_name, 3), False)
        wmp.click_back_button()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GZTGL_0007(self):
        """点击顶部返回键，返回到上一级页面"""

        wbp = WorkbenchPage()
        # 点击“工作台管理”应用
        wbp.click_workbench_manage()
        wmp = WorkbenchManagePage()
        wmp.wait_for_page_load()
        # 工作台管理首页点击顶部返回键【 < 】
        wmp.click_back_button()
        # 1.返回到工作台页面
        wbp.wait_for_page_load()
        wbp.click_workbench_manage()
        wmp.click_add_icon()
        asp = AppStorePage()
        asp.wait_for_page_load()
        # 工作台管理其他页面点击顶部返回键【 < 】
        asp.click_back_button()
        # 2.如果在应用其他页面，返回到上一级页面
        wmp.wait_for_page_load()
        wmp.click_back_button()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GZTGL_0008(self):
        """点击顶部关闭按钮返回工作台页面"""

        wbp = WorkbenchPage()
        # 点击“工作台管理”应用
        wbp.click_workbench_manage()
        wmp = WorkbenchManagePage()
        wmp.wait_for_page_load()
        # 点击分组后边的“+”
        wmp.click_add_icon()
        asp = AppStorePage()
        # 进入应用商城
        asp.wait_for_page_load()
        # 点击顶部【X】
        asp.click_close()
        # 1.返回到工作台页面
        wbp.wait_for_page_load()
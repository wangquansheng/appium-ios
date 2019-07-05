import random
import re
import time
import unittest

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, switch_to_mobile, current_driver
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components import BaseChatPage
from pages.groupset.GroupChatSetPicVideo import GroupChatSetPicVideoPage
from pages.workbench.corporate_news.CorporateNews import CorporateNewsPage
from pages.workbench.corporate_news.CorporateNewsDetails import CorporateNewsDetailsPage
from pages.workbench.corporate_news.CorporateNewsImageText import CorporateNewsImageTextPage
from pages.workbench.corporate_news.CorporateNewsLink import CorporateNewsLinkPage
from pages.workbench.corporate_news.CorporateNewsNoNews import CorporateNewsNoNewsPage

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
    def make_already_have_my_picture():
        """确保当前群聊页面已有图片"""
        # 1.点击输入框左上方的相册图标
        gcp = GroupChatPage()
        cpg = ChatPicPage()
        gcp.is_on_this_page()
        if gcp.is_exist_msg_image():
            return
        else:
            # 2.进入相片页面,选择一张片相发送
            time.sleep(2)
            gcp.click_picture()
            cpg.wait_for_page_load()
            cpg.select_pic_fk(1)
            cpg.click_send()
            time.sleep(5)

    @staticmethod
    def make_already_have_my_videos():
        """确保当前群聊页面已有视频"""
        # 1.点击输入框左上方的相册图标
        gcp = GroupChatPage()
        cpg = ChatPicPage()
        gcp.wait_for_page_load()
        if gcp.is_exist_msg_videos():
            return
        else:
            # 2.进入相片页面,选择一张片相发送
            gcp.click_picture()
            cpg.wait_for_page_load()
            cpg.select_video_fk(1)
            cpg.click_send()
            time.sleep(5)

    @staticmethod
    def get_into_group_chat_page(name):
        """进入群聊聊天会话页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击发起群聊
        mp.click_group_chat()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @staticmethod
    def make_no_message_send_failed_status():
        """确保当前消息列表没有消息发送失败的标识影响验证结果"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        if mp.is_iv_fail_status_present():
            mp.clear_fail_in_send_message()

    @staticmethod
    def if_exists_multiple_enterprises_enter_group_chat(types):
        """选择团队联系人时存在多个团队时返回获取当前团队名，再进入群聊转发图片/视频"""

        shc = SelectHeContactsDetailPage()
        # 测试号码是否存在多个团队
        if not shc.is_exist_corporate_grade():
            mp = MessagePage()
            scg = SelectContactsPage()
            gcp = GroupChatPage()
            shc.click_back()
            scg.wait_for_page_load()
            scg.click_back()
            gcp.wait_for_page_load()
            gcp.click_back()
            mp.wait_for_page_load()
            mp.open_workbench_page()
            wbp = WorkbenchPage()
            wbp.wait_for_page_load()
            time.sleep(2)
            # 获取当前团队名
            workbench_name = wbp.get_workbench_name()
            mp.open_message_page()
            mp.wait_for_page_load()
            group_name = "群聊1"
            Preconditions.get_into_group_chat_page(group_name)
            # 转发图片/视频
            if types == "pic":
                gcp.forward_pic()
            elif types == "video":
                gcp.forward_video()
            scg.wait_for_page_load()
            scg.click_he_contacts()
            shc.wait_for_he_contacts_page_load()
            # 选择当前团队
            shc.click_department_name(workbench_name)

    @staticmethod
    def enter_corporate_news_page():
        """进入企业新闻首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_corporate_news()

    @staticmethod
    def create_unpublished_image_news(news):
        """创建未发新闻(图文新闻)"""

        cnp = CorporateNewsPage()
        cnp.wait_for_page_load()
        for title, content in news:
            # 点击发布新闻
            cnp.click_release_news()
            cnitp = CorporateNewsImageTextPage()
            cnitp.wait_for_page_load()
            # 输入图文新闻标题
            cnitp.input_news_title(title)
            # 输入图文新闻内容
            cnitp.input_news_content(content)
            cnitp.click_name_attribute_by_name("完成")
            # 点击保存
            cnitp.click_save()
            # 点击确定
            cnitp.click_sure()
            cnp.wait_for_page_load()
            time.sleep(2)

    @staticmethod
    def release_corporate_image_news(titles):
        """发布企业新闻(图文新闻)"""

        cnp = CorporateNewsPage()
        cnp.wait_for_page_load()
        for title in titles:
            # 点击发布新闻
            cnp.click_release_news()
            cnitp = CorporateNewsImageTextPage()
            cnitp.wait_for_page_load()
            # 输入图文新闻标题
            cnitp.input_news_title(title)
            # 输入图文新闻内容
            cnitp.input_news_content("123")
            cnitp.click_name_attribute_by_name("完成")
            # 点击发布
            cnitp.click_release()
            # 点击确定
            cnitp.click_sure()
            cnp.wait_for_page_load()
            time.sleep(2)


class MsgGroupChatVideoPicAllTest(TestCase):

    # @classmethod
    # def setUpClass(cls):
    #
    #     Preconditions.select_mobile('IOS-移动')
    #     # 导入测试联系人、群聊
    #     fail_time1 = 0
    #     flag1 = False
    #     import dataproviders
    #     while fail_time1 < 3:
    #         try:
    #             required_contacts = dataproviders.get_preset_contacts()
    #             conts = ContactsPage()
    #             current_mobile().hide_keyboard_if_display()
    #             Preconditions.make_already_in_message_page()
    #             conts.open_contacts_page()
    #             try:
    #                 if conts.is_text_present("发现SIM卡联系人"):
    #                     conts.click_text("显示")
    #             except:
    #                 pass
    #             for name, number in required_contacts:
    #                 # 创建联系人
    #                 conts.create_contacts_if_not_exits(name, number)
    #             required_group_chats = dataproviders.get_preset_group_chats()
    #             conts.open_group_chat_list()
    #             group_list = GroupListPage()
    #             for group_name, members in required_group_chats:
    #                 group_list.wait_for_page_load()
    #                 # 创建群
    #                 group_list.create_group_chats_if_not_exits(group_name, members)
    #             group_list.click_back()
    #             conts.open_message_page()
    #             flag1 = True
    #         except:
    #             fail_time1 += 1
    #         if flag1:
    #             break
    #
    #     # 导入团队联系人
    #     fail_time2 = 0
    #     flag2 = False
    #     while fail_time2 < 5:
    #         try:
    #             Preconditions.make_already_in_message_page()
    #             contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
    #             Preconditions.create_he_contacts(contact_names)
    #             flag2 = True
    #         except:
    #             fail_time2 += 1
    #         if flag2:
    #             break
    #
    #     # 确保有企业群
    #     fail_time3 = 0
    #     flag3 = False
    #     while fail_time3 < 5:
    #         try:
    #             Preconditions.make_already_in_message_page()
    #             Preconditions.ensure_have_enterprise_group()
    #             flag3 = True
    #         except:
    #             fail_time3 += 1
    #         if flag3:
    #             break

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、确保当前页面在群聊聊天会话页面
        """

        Preconditions.select_mobile('IOS-移动')
        # mp = MessagePage()
        # name = "群聊1"
        # if mp.is_on_this_page():
        #     Preconditions.get_into_group_chat_page(name)
        #     return
        # gcp = GroupChatPage()
        # if not gcp.is_on_this_page():
        #     current_mobile().launch_app()
        #     Preconditions.make_already_in_message_page()
        #     Preconditions.get_into_group_chat_page(name)
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_corporate_news_page()
            return
        cnp = CorporateNewsPage()
        if not cnp.is_on_corporate_news_page():
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_corporate_news_page()

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0021(self):
        """群聊会话页面，打开拍照，立刻返回会话窗口"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保企业新闻首页不存在新闻
        cnp.clear_corporate_news()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0041(self):
        """群聊会话页面,转发自己发送的图片到当前会话窗口"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        wbp = WorkbenchPage()
        if cnp.is_exist_close_button():
            cnp.click_close()
            wbp.wait_for_page_load()
            wbp.click_company_news()
            cnp.wait_for_page_load()
        # 点击【<】
        cnp.click_back_button()
        # 3.等待工作台页面加载
        wbp.wait_for_page_load()
        wbp.click_company_news()
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0042(self):
        """群聊会话页面，转发自己发送的图片到当前会话窗口时失败"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保有控件【X】
        cnp.click_no_news()
        cnnp = CorporateNewsNoNewsPage()
        cnnp.wait_for_page_load()
        # 点击【X】
        cnnp.click_close()
        # 3.等待工作台页面加载
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_company_news()
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0043(self):
        """群聊会话页面，转发自己发送的图片到当前会话窗口时点击取消转发"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保企业新闻首页不存在新闻
        cnp.clear_corporate_news()
        # 3.是否存在提示语,“发布新闻”、“未发新闻”按钮
        self.assertEquals(cnp.page_should_contain_text2("向团队所有成员发出第一条新闻"), True)
        self.assertEquals(cnp.is_exist_release_news_button(), True)
        self.assertEquals(cnp.is_exist_no_news_button(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0044(self):
        """群聊会话页面，转发自己发送的图片给手机联系人"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        cnp.clear_corporate_news()
        # 确保存在多条已发布的企业新闻
        titles = ["测试新闻00051", "测试新闻00052", "测试新闻00053", "测试新闻00054"]
        Preconditions.release_corporate_image_news(titles)
        # 3.企业新闻列表是否按发布时间倒序排序
        self.assertEquals(cnp.get_corporate_news_titles(), titles)

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0045(self):
        """群聊会话页面，转发自己发送的图片到手机联系人时失败"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保存在已发布的企业新闻
        if not cnp.is_exist_corporate_news():
            titles = ["测试新闻0006"]
            Preconditions.release_corporate_image_news(titles)
        # 3.选择一条企业新闻
        cnp.click_corporate_news_by_number(0)
        cndp = CorporateNewsDetailsPage()
        # 等待企业新闻详情页加载
        cndp.wait_for_page_load()
        # 4.点击下线
        cndp.click_offline()
        # 5.点击确定，是否提示下线成功(部分验证点变动)
        cndp.click_sure()
        # self.assertEquals(cndp.is_exist_offline_successfully(), True)
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0046(self):
        """群聊会话页面，转发自己发送的图片到手机联系人时点击取消转发"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击发布新闻
        cnp.click_release_news()
        cnitp = CorporateNewsImageTextPage()
        # 3.等待发布新闻-图文发布页加载
        cnitp.wait_for_page_load()
        # 4.点击链接发布
        cnitp.click_link_publishing()
        cnlp = CorporateNewsLinkPage()
        cnlp.wait_for_page_load()
        # 5.输入链接新闻标题、内容
        cnlp.input_news_title("测试新闻0017")
        cnlp.input_link_url("https://10086.com")
        cnlp.click_name_attribute_by_name("完成")
        # 6.点击发布
        cnlp.click_release()
        # 点击确定
        cnlp.click_sure()
        # 7.是否提示发布成功(部分验证点变动)
        # self.assertEquals(cnlp.is_exist_release_successfully(), True)
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0047(self):
        """群聊会话页面，转发自己发送的图片给团队联系人"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击发布新闻
        cnp.click_release_news()
        cnitp = CorporateNewsImageTextPage()
        # 3.等待发布新闻-图文发布页加载
        cnitp.wait_for_page_load()
        # 4.点击链接发布
        cnitp.click_link_publishing()
        cnlp = CorporateNewsLinkPage()
        cnlp.wait_for_page_load()
        # 5.输入链接新闻标题、内容
        cnlp.input_news_title("测试新闻0018")
        cnlp.input_link_url("https://10086.com")
        cnlp.click_name_attribute_by_name("完成")
        # 6.点击发布
        cnlp.click_release()
        # 7.取消发布新闻
        cnlp.click_cancel()
        cnlp.click_back_button()
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0048(self):
        """群聊会话页面，转发自己发送的图片到团队联系人时失败"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击未发新闻
        cnp.click_no_news()
        cnnp = CorporateNewsNoNewsPage()
        # 3.等待未发新闻页加载
        cnnp.wait_for_page_load()
        cnnp.clear_no_news()
        # 确保未发新闻列表存在数据
        news = [("测试新闻0019", "测试内容0019")]
        cnnp.click_close()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_company_news()
        Preconditions.create_unpublished_image_news(news)
        cnp.click_no_news()
        cnnp.wait_for_page_load()
        # 点击未发新闻
        title = cnnp.click_no_news_by_number(0)
        cndp = CorporateNewsDetailsPage()
        # 4.等待未发布新闻详情页加载
        cndp.wait_for_page_load()
        # 点击删除
        cndp.click_delete()
        # 5.点击确定
        cndp.click_sure()
        # 6.是否提示删除成功，未发新闻列表不存在该记录信息(部分验证点变动)
        # self.assertEquals(cndp.is_exist_delete_successfully(), True)
        cnnp.wait_for_page_load()
        self.assertEquals(cnnp.is_exist_no_news_by_name(title), False)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0049(self):
        """群聊会话页面，转发自己发送的图片到团队联系人时点击取消转发"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击未发新闻
        cnp.click_no_news()
        cnnp = CorporateNewsNoNewsPage()
        # 3.等待未发新闻页加载
        cnnp.wait_for_page_load()
        # 确保存在未发布的企业新闻
        if not cnnp.is_exist_no_news():
            cnnp.click_back_button()
            cnp.wait_for_page_load()
            news = [("测试新闻0020", "测试内容0020")]
            Preconditions.create_unpublished_image_news(news)
            cnp.click_no_news()
            cnnp.wait_for_page_load()
        # 点击一条未发新闻
        cnnp.click_no_news_by_number(0)
        cndp = CorporateNewsDetailsPage()
        # 4.等待企业新闻详情页加载
        cndp.wait_for_page_load()
        # 5.点击发布
        cndp.click_release()
        # 6.点击确定，是否提示发布成功(部分验证点变动)
        cndp.click_sure()
        # self.assertEquals(cndp.is_exist_release_successfully(), True)
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0050(self):
        """群聊会话页面，转发自己发送的图片给陌生人"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保存在多条已发布的企业新闻
        titles = ["测试新闻00301", "测试新闻00302"]
        Preconditions.release_corporate_image_news(titles)
        number = 0
        # 访问前的浏览量
        amount = cnp.get_corporate_news_page_view_by_number(number)
        # 3.进入新闻详情页
        cnp.click_corporate_news_by_number(number)
        cndp = CorporateNewsDetailsPage()
        cndp.wait_for_page_load()
        cndp.click_back_button()
        cnp.wait_for_page_load()
        # 访问后的浏览量
        news_amount = cnp.get_corporate_news_page_view_by_number(number)
        # 4.验证每次用户查看新闻详情再返回到列表之后，浏览数量是否+1
        self.assertEquals(amount + 1, news_amount)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0051(self):
        """群聊会话页面，转发自己发送的图片到陌生人时失败"""

        cnp = CorporateNewsPage()
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击发布新闻
        cnp.click_release_news()
        cnitp = CorporateNewsImageTextPage()
        cnitp.wait_for_page_load()
        # 点击链接发布
        cnitp.click_link_publishing()
        cnlp = CorporateNewsLinkPage()
        cnlp.wait_for_page_load()
        # 输入链接新闻标题
        cnlp.input_news_title("测试新闻0034")
        # 输入链接新闻网址
        cnlp.input_link_url("https://10086.com")
        cnlp.click_name_attribute_by_name("完成")
        # 点击保存
        cnlp.click_save()
        # 点击确定
        cnlp.click_sure()
        # 1.是否提示保存成功,等待企业新闻首页加载(部分验证点变动)
        # self.assertEquals(cnlp.is_exist_save_successfully(), True)
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0052(self):
        """群聊会话页面，转发自己发送的图片到陌生人时点击取消转发"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保企业新闻首页不存在新闻
        cnp.clear_corporate_news()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0053(self):
        """群聊会话页面，转发自己发送的图片到普通群"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        wbp = WorkbenchPage()
        if cnp.is_exist_close_button():
            cnp.click_close()
            wbp.wait_for_page_load()
            wbp.click_company_news()
            cnp.wait_for_page_load()
        # 点击【<】
        cnp.click_back_button()
        # 3.等待工作台页面加载
        wbp.wait_for_page_load()
        wbp.click_company_news()
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0054(self):
        """群聊会话页面，转发自己发送的图片到普通群时失败"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保有控件【X】
        cnp.click_no_news()
        cnnp = CorporateNewsNoNewsPage()
        cnnp.wait_for_page_load()
        # 点击【X】
        cnnp.click_close()
        # 3.等待工作台页面加载
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_company_news()
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0055(self):
        """群聊会话页面，转发自己发送的图片到普通群时点击取消转发"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保企业新闻首页不存在新闻
        cnp.clear_corporate_news()
        # 3.是否存在提示语,“发布新闻”、“未发新闻”按钮
        self.assertEquals(cnp.page_should_contain_text2("向团队所有成员发出第一条新闻"), True)
        self.assertEquals(cnp.is_exist_release_news_button(), True)
        self.assertEquals(cnp.is_exist_no_news_button(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0056(self):
        """群聊会话页面，转发自己发送的图片到企业群"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        cnp.clear_corporate_news()
        # 确保存在多条已发布的企业新闻
        titles = ["测试新闻00051", "测试新闻00052", "测试新闻00053", "测试新闻00054"]
        Preconditions.release_corporate_image_news(titles)
        # 3.企业新闻列表是否按发布时间倒序排序
        self.assertEquals(cnp.get_corporate_news_titles(), titles)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0057(self):
        """群聊会话页面，转发自己发送的图片到企业群时失败"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保存在已发布的企业新闻
        if not cnp.is_exist_corporate_news():
            titles = ["测试新闻0006"]
            Preconditions.release_corporate_image_news(titles)
        # 3.选择一条企业新闻
        cnp.click_corporate_news_by_number(0)
        cndp = CorporateNewsDetailsPage()
        # 等待企业新闻详情页加载
        cndp.wait_for_page_load()
        # 4.点击下线
        cndp.click_offline()
        # 5.点击确定，是否提示下线成功(部分验证点变动)
        cndp.click_sure()
        # self.assertEquals(cndp.is_exist_offline_successfully(), True)
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0058(self):
        """群聊会话页面，转发自己发送的图片到企业群时点击取消转发"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击发布新闻
        cnp.click_release_news()
        cnitp = CorporateNewsImageTextPage()
        # 3.等待发布新闻-图文发布页加载
        cnitp.wait_for_page_load()
        # 4.点击链接发布
        cnitp.click_link_publishing()
        cnlp = CorporateNewsLinkPage()
        cnlp.wait_for_page_load()
        # 5.输入链接新闻标题、内容
        cnlp.input_news_title("测试新闻0017")
        cnlp.input_link_url("https://10086.com")
        cnlp.click_name_attribute_by_name("完成")
        # 6.点击发布
        cnlp.click_release()
        # 点击确定
        cnlp.click_sure()
        # 7.是否提示发布成功(部分验证点变动)
        # self.assertEquals(cnlp.is_exist_release_successfully(), True)
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0069(self):
        """群聊会话页面，转发自己发送的视频给手机联系人"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击发布新闻
        cnp.click_release_news()
        cnitp = CorporateNewsImageTextPage()
        # 3.等待发布新闻-图文发布页加载
        cnitp.wait_for_page_load()
        # 4.点击链接发布
        cnitp.click_link_publishing()
        cnlp = CorporateNewsLinkPage()
        cnlp.wait_for_page_load()
        # 5.输入链接新闻标题、内容
        cnlp.input_news_title("测试新闻0018")
        cnlp.input_link_url("https://10086.com")
        cnlp.click_name_attribute_by_name("完成")
        # 6.点击发布
        cnlp.click_release()
        # 7.取消发布新闻
        cnlp.click_cancel()
        cnlp.click_back_button()
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0070(self):
        """群聊会话页面，转发自己发送的视频给手机联系人时失败"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击未发新闻
        cnp.click_no_news()
        cnnp = CorporateNewsNoNewsPage()
        # 3.等待未发新闻页加载
        cnnp.wait_for_page_load()
        cnnp.clear_no_news()
        # 确保未发新闻列表存在数据
        news = [("测试新闻0019", "测试内容0019")]
        cnnp.click_close()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_company_news()
        Preconditions.create_unpublished_image_news(news)
        cnp.click_no_news()
        cnnp.wait_for_page_load()
        # 点击未发新闻
        title = cnnp.click_no_news_by_number(0)
        cndp = CorporateNewsDetailsPage()
        # 4.等待未发布新闻详情页加载
        cndp.wait_for_page_load()
        # 点击删除
        cndp.click_delete()
        # 5.点击确定
        cndp.click_sure()
        # 6.是否提示删除成功，未发新闻列表不存在该记录信息(部分验证点变动)
        # self.assertEquals(cndp.is_exist_delete_successfully(), True)
        cnnp.wait_for_page_load()
        self.assertEquals(cnnp.is_exist_no_news_by_name(title), False)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0071(self):
        """群聊会话页面，转发自己发送的视频给手机联系人时点击取消转发"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击未发新闻
        cnp.click_no_news()
        cnnp = CorporateNewsNoNewsPage()
        # 3.等待未发新闻页加载
        cnnp.wait_for_page_load()
        # 确保存在未发布的企业新闻
        if not cnnp.is_exist_no_news():
            cnnp.click_back_button()
            cnp.wait_for_page_load()
            news = [("测试新闻0020", "测试内容0020")]
            Preconditions.create_unpublished_image_news(news)
            cnp.click_no_news()
            cnnp.wait_for_page_load()
        # 点击一条未发新闻
        cnnp.click_no_news_by_number(0)
        cndp = CorporateNewsDetailsPage()
        # 4.等待企业新闻详情页加载
        cndp.wait_for_page_load()
        # 5.点击发布
        cndp.click_release()
        # 6.点击确定，是否提示发布成功(部分验证点变动)
        cndp.click_sure()
        # self.assertEquals(cndp.is_exist_release_successfully(), True)
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0072(self):
        """群聊会话页面，转发自己发送的视频给团队联系人"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保存在多条已发布的企业新闻
        titles = ["测试新闻00301", "测试新闻00302"]
        Preconditions.release_corporate_image_news(titles)
        number = 0
        # 访问前的浏览量
        amount = cnp.get_corporate_news_page_view_by_number(number)
        # 3.进入新闻详情页
        cnp.click_corporate_news_by_number(number)
        cndp = CorporateNewsDetailsPage()
        cndp.wait_for_page_load()
        cndp.click_back_button()
        cnp.wait_for_page_load()
        # 访问后的浏览量
        news_amount = cnp.get_corporate_news_page_view_by_number(number)
        # 4.验证每次用户查看新闻详情再返回到列表之后，浏览数量是否+1
        self.assertEquals(amount + 1, news_amount)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0073(self):
        """群聊会话页面，转发自己发送的视频给团队联系人时失败"""

        cnp = CorporateNewsPage()
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击发布新闻
        cnp.click_release_news()
        cnitp = CorporateNewsImageTextPage()
        cnitp.wait_for_page_load()
        # 点击链接发布
        cnitp.click_link_publishing()
        cnlp = CorporateNewsLinkPage()
        cnlp.wait_for_page_load()
        # 输入链接新闻标题
        cnlp.input_news_title("测试新闻0034")
        # 输入链接新闻网址
        cnlp.input_link_url("https://10086.com")
        cnlp.click_name_attribute_by_name("完成")
        # 点击保存
        cnlp.click_save()
        # 点击确定
        cnlp.click_sure()
        # 1.是否提示保存成功,等待企业新闻首页加载(部分验证点变动)
        # self.assertEquals(cnlp.is_exist_save_successfully(), True)
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0074(self):
        """群聊会话页面，转发自己发送的视频给团队联系人时点击取消转发"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保有控件【X】
        cnp.click_no_news()
        cnnp = CorporateNewsNoNewsPage()
        cnnp.wait_for_page_load()
        # 点击【X】
        cnnp.click_close()
        # 3.等待工作台页面加载
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_company_news()
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0075(self):
        """群聊会话页面，转发自己发送的视频给陌生人"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保企业新闻首页不存在新闻
        cnp.clear_corporate_news()
        # 3.是否存在提示语,“发布新闻”、“未发新闻”按钮
        self.assertEquals(cnp.page_should_contain_text2("向团队所有成员发出第一条新闻"), True)
        self.assertEquals(cnp.is_exist_release_news_button(), True)
        self.assertEquals(cnp.is_exist_no_news_button(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0076(self):
        """群聊会话页面，转发自己发送的视频给陌生人时失败"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        cnp.clear_corporate_news()
        # 确保存在多条已发布的企业新闻
        titles = ["测试新闻00051", "测试新闻00052", "测试新闻00053", "测试新闻00054"]
        Preconditions.release_corporate_image_news(titles)
        # 3.企业新闻列表是否按发布时间倒序排序
        self.assertEquals(cnp.get_corporate_news_titles(), titles)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0077(self):
        """群聊会话页面，转发自己发送的视频给陌生人时点击取消转发"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保存在已发布的企业新闻
        if not cnp.is_exist_corporate_news():
            titles = ["测试新闻0006"]
            Preconditions.release_corporate_image_news(titles)
        # 3.选择一条企业新闻
        cnp.click_corporate_news_by_number(0)
        cndp = CorporateNewsDetailsPage()
        # 等待企业新闻详情页加载
        cndp.wait_for_page_load()
        # 4.点击下线
        cndp.click_offline()
        # 5.点击确定，是否提示下线成功(部分验证点变动)
        cndp.click_sure()
        # self.assertEquals(cndp.is_exist_offline_successfully(), True)
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()


class MsgGroupChatTest(TestCase):

    @classmethod
    def setUpClass(cls):

        Preconditions.select_mobile('IOS-移动')
        # 导入测试联系人、群聊
        fail_time1 = 0
        flag1 = False
        import dataproviders
        while fail_time1 < 3:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                Preconditions.make_already_in_message_page()
                conts.open_contacts_page()
                for name, number in required_contacts:
                    # 创建联系人
                    conts.create_contacts_if_not_exits(name, number)
                required_group_chats = dataproviders.get_preset_group_chats()
                conts.open_group_chat_list()
                group_list = GroupListPage()
                for group_name, members in required_group_chats:
                    group_list.wait_for_page_load()
                    # 创建群
                    group_list.create_group_chats_if_not_exits(group_name, members)
                group_list.click_back()
                conts.open_message_page()
                flag1 = True
            except:
                fail_time1 += 1
            if flag1:
                break


    def default_setUp(self):

        Preconditions.select_mobile('IOS-移动')

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0001(self):
        """群聊会话页面，不勾选相册内图片点击发送按钮"""

        mp = MessagePage()
        mp.wait_for_page_load()
        #在消息页面等待页面加载
        mp.click_add_icon()
        #点击加号
        mp.click_group_chat()
        #点击发起群聊
        sccp = SelectContactsPage()
        #选择联系人页面
        sccp.wait_for_page_load()
        #等待选择联系人页面加载
        sccp.click_select_one_group()
        #点击选择一个群按钮
        sog = SelectOneGroupPage()
        #选择一个群界面
        sog.selecting_one_group_by_name("群聊1")
        #通过名称找到群聊1
        gcp = GroupChatPage()
        #群聊1界面
        gcp.wait_for_page_load()
        #等待页面加载
        gcp.click_picture()
        #点击图片按钮
        cpp = ChatPicPage()
        #选择图片页面
        cpp.wait_for_page_load()
        #等待页面加载
        self.assertEquals(cpp.send_btn_is_enabled(), False)
        #判断发送按钮enabled是否为false

    def test_msg_xiaoliping_D_0002(self):
        '''群聊会话页面，勾选相册内一张图片发送'''
        mp = MessagePage()
        #等待页面加载
        mp.wait_for_page_load()
        #点击加号
        mp.click_add_icon()
        #点击发起群聊按钮
        mp.click_group_chat()
        #选择联系人界面
        scp = SelectContactsPage()
        #等待页面加载
        scp.wait_for_page_load()
        #点击选择一个群按钮
        scp.click_select_one_group()
        #选择一个群界面
        sog = SelectOneGroupPage()
        #等待页面加载
        sog.wait_for_page_load()
        #通过名称找到群聊'啊测测试试'
        sog.selecting_one_group_by_name('啊测测试试')
        #群聊页面
        gcp = GroupChatPage()
        #等待页面加载
        gcp.wait_for_page_load()
        #点击图片按钮
        gcp.click_picture()
        #选择图片界面
        cpp = ChatPicPage()
        #等待页面加载
        cpp.wait_for_page_load()
        #选择第一张照片
        cpp.select_picture()
        #点击发送 按钮中有发送就可以点击
        cpp.click_name_attribute_by_name("发送")
        #等待页面加载
        gcp.wait_for_page_load()
        #点击返回按钮
        gcp.click_back_button()
        #等待页面加载
        mp.wait_for_page_load()
        #验证第一条消息是否为图片
        self.assertEquals(mp.is_first_message_image(), True)

    def test_msg_xiaoliping_D_0003(self):
        '''群聊会话页面，预览相册内图片'''
        #消息界面
        mp = MessagePage()
        #等待界面加载
        mp.wait_for_page_load()
        #点击加号
        mp.click_add_icon()
        #点击发起群聊按钮
        mp.click_group_chat()
        #选择联系人界面
        scp = SelectContactsPage()
        #等待页面加载
        scp.wait_for_page_load()
        #点击选择一个群
        scp.click_select_one_group()
        #选择一个群界面
        sogp = SelectOneGroupPage()
        #等待页面加载
        sogp.wait_for_page_load()
        #通过名称选择'群聊1'群聊
        sogp.selecting_one_group_by_name('群聊1')
        #群聊界面
        gcp = GroupChatPage()
        #等待页面加载
        gcp.wait_for_page_load()
        #点击图片按钮
        gcp.click_picture()
        #选择图片界面
        cpp = ChatPicPage()
        #等待界面加载
        cpp.wait_for_page_load()
        #选择第一张图片
        cpp.select_picture()
        #点击预览按钮
        cpp.click_preview()
        #预览界面
        cpg = ChatPicPreviewPage()
        #等待界面加载
        cpg.wait_for_page_load()

    def test_msg_xiaoliping_D_0004(self):
        '''群聊会话页面，预览相册内图片，不勾选原图发送'''
        #消息界面
        message_page = MessagePage()
        #等待页面加载
        message_page.wait_for_page_load()
        #点击加号
        message_page.click_add_icon()
        #点击发起群聊按钮
        message_page.click_group_chat()
        #选择联系人界面
        select_contacts_page = SelectContactsPage()
        #等待界面加载
        select_contacts_page.wait_for_page_load()
        #选择一个群按钮
        select_contacts_page.click_select_one_group()
        #选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        #通过名称找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        #群聊界面
        group_chat_page = GroupChatPage()
        #等待界面加载
        group_chat_page.wait_for_page_load()
        #点击选择图片按钮
        group_chat_page.click_picture()
        #选择图片界面
        chat_pic_page = ChatPicPage()
        #等待界面加载
        chat_pic_page.wait_for_page_load()
        #选择第一张图片
        chat_pic_page.select_picture()
        #点击预览
        chat_pic_page.click_preview()
        #预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        #等待页面加载
        chat_pic_preview_page.wait_for_page_load()
        #点击发送
        chat_pic_preview_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（图片无法选中间接验证）
        self.assertEquals(message_page.is_first_message_image(), True)

    def test_msg_xiaoliping_D_0005(self):
        '''群聊会话页面，预览相册数量与发送按钮数量一致'''
        #消息界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        #点击加号
        message_page.click_add_icon()
        #点击发起群聊
        message_page.click_group_chat()
        #选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        #选择一个群
        select_contacts_page.click_select_one_group()
        #选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        #通过名称找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        #群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        #点击选择照片
        group_chat_page.click_picture()
        #选择图片页面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        #选择多张照片
        chat_pic_page.select_pictures(3)
        #点击预览
        chat_pic_page.click_preview()
        #预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        #获取预览数文本
        text1 = chat_pic_preview_page.get_preview_text()
        #获取发送按钮文本
        text2 = chat_pic_preview_page.get_send_text()
        #判断预览数与发送数是否相等
        self.assertEquals(text1, text2)

    def test_msg_xiaoliping_D_0006(self):
        """群聊会话页面，编辑图片发送"""
        #消息界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        #点击加号
        message_page.click_add_icon()
        #点击发起群聊
        message_page.click_group_chat()
        #选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        #点击选择一个群
        select_contacts_page.click_select_one_group()
        #选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        #通过群名找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        #群聊1界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        #点击图片按钮
        group_chat_page.click_picture()
        #选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        #选择一张图片
        chat_pic_page.select_pictures(1)
        #点击预览
        chat_pic_page.click_preview()
        #图片预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        #点击编辑
        chat_pic_preview_page.click_edit()
        #图片编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        #点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        #滑动进行涂鸦
        chat_pic_edit_page.do_doodle()
        #点击马赛克按钮
        chat_pic_edit_page.click_mosaic()
        #滑动进行马赛克操作
        chat_pic_edit_page.do_mosaic()
        #点击文本编辑按钮
        chat_pic_edit_page.click_text_edit_btn()
        #文本编辑
        chat_pic_edit_page.input_pic_text()
        #点击完成
        chat_pic_edit_page.click_done()
        #点击发送
        chat_pic_edit_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    def test_msg_xiaoliping_D_0007(self):
        """群聊会话页面，编辑图片不保存发送"""
        #消息界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        #点击加号
        message_page.click_add_icon()
        #点击发起群聊
        message_page.click_group_chat()
        #选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        #点击选择一个群
        select_contacts_page.click_select_one_group()
        #选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        #按名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        #群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        #点击图片按钮
        group_chat_page.click_picture()
        #选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        #选择一张图片
        chat_pic_page.select_pictures(1)
        #点击预览按钮
        chat_pic_page.click_preview()
        #图片预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        #点击编辑按钮
        chat_pic_preview_page.click_edit()
        #图片编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        #点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        #进行涂鸦操作
        chat_pic_edit_page.do_doodle()
        #点击马赛克按钮
        chat_pic_edit_page.click_mosaic()
        #进行马赛克操作
        chat_pic_edit_page.do_mosaic()
        #点击文本编辑按钮
        chat_pic_edit_page.click_text_edit_btn()
        #进行文本编辑
        chat_pic_edit_page.input_pic_text()
        #点击完成
        chat_pic_edit_page.click_done()
        #点击保存
        chat_pic_edit_page.click_save()
        chat_pic_edit_page.wait_for_page_load()
        #点击发送
        chat_pic_edit_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    def test_msg_xiaoliping_D_0008(self):
        """群聊会话页面，编辑图片中途直接发送"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures(1)
        # 点击预览
        chat_pic_page.click_preview()
        # 预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        # 点击编辑
        chat_pic_preview_page.click_edit()
        # 编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        # 进行涂鸦操作
        chat_pic_edit_page.do_doodle()
        # 点击马赛克按钮
        chat_pic_edit_page.click_mosaic()
        # 进行马赛克操作
        chat_pic_edit_page.do_mosaic()
        # 点击文本编辑按钮
        chat_pic_edit_page.click_text_edit_btn()
        # 进行文本编辑
        chat_pic_edit_page.input_pic_text()
        # 点击完成
        chat_pic_edit_page.click_done()
        # 点击发送
        chat_pic_edit_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    def test_msg_xiaoliping_D_0009(self):
        """群聊会话页面，编辑图片保存"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures(1)
        # 点击预览
        chat_pic_page.click_preview()
        # 预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        # 点击编辑
        chat_pic_preview_page.click_edit()
        # 编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        # 进行涂鸦操作
        chat_pic_edit_page.do_doodle()
        # 点击马赛克按钮
        chat_pic_edit_page.click_mosaic()
        # 进行马赛克操作
        chat_pic_edit_page.do_mosaic()
        # 点击文本编辑按钮
        chat_pic_edit_page.click_text_edit_btn()
        # 进行文本编辑
        chat_pic_edit_page.input_pic_text()
        # 点击完成
        chat_pic_edit_page.click_done()
        # 点击保存
        chat_pic_edit_page.click_save()
        # 判断保存之后是否有文字提示已保存至系统相册
        self.assertEquals(chat_pic_edit_page.page_should_contain_text2("已保存至系统相册", 20), True)

    def test_msg_xiaoliping_D_0014(self):
        """群聊会话页面，勾选9张相册内图片发送"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择九张图片
        chat_pic_page.select_pictures(9)
        # 点击发送
        chat_pic_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（发送图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    def test_msg_xiaoliping_D_0015(self):
        """群聊会话页面，勾选超9张相册内图片发送"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择九张图片
        chat_pic_page.select_pictures(9)
        # 判断第十个图片的点击按钮是否不可点击
        self.assertEquals(chat_pic_page.picture_btn_is_enabled(10), False)

    def test_msg_xiaoliping_D_0016(self):
        """群聊会话页面，同时发送相册中的图片和视频"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures(1)
        # 获取发送按钮文本1
        text1 = chat_pic_page.get_send_text()
        # 选择一个视频
        chat_pic_page.select_one_video()
        # 获取点击视频后发送按钮文本2
        text2 = chat_pic_page.get_send_text()
        # 比较文本1和2是否相同（发送按钮没有变化说明无法同时选取照片和视频）
        self.assertEquals(text1, text2)
        # # 判断点击图片之后是否有文字提示不能同时选择照片和视频（有时会抓不到文本信息 不稳定）
        # self.assertEquals(chat_pic_page.page_should_contain_text2("不能同时选择照片和视频", 20), True)

    def test_msg_xiaoliping_D_0017(self):
        """群聊会话页面，使用拍照功能并发送照片"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击拍照
        chat_photo_page.take_photo()
        # 点击发送
        chat_photo_page.send_photo()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（发送图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    def test_msg_xiaoliping_D_0110(self):
        """在群聊会话窗，验证点击趣图搜搜入口"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击表情按钮
        group_chat_page.click_expression_button()
        group_chat_page.wait_for_page_load()
        # 点击gif按钮
        group_chat_page.click_gif_button()
        group_chat_page.wait_for_page_load()
        # 判断当前页面时候有关闭gif按钮
        group_chat_page.is_exist_closegif_page()

    def test_msg_xiaoliping_D_0111(self):
        """在群聊会话窗，网络正常发送表情搜搜"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击表情按钮
        group_chat_page.click_expression_button()
        group_chat_page.wait_for_page_load()
        # 点击gif按钮
        group_chat_page.click_gif_button()
        group_chat_page.wait_for_page_load()
        # 点击发送GIF图片
        group_chat_page.click_send_gif()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 判断第一条消息是否为表情
        self.assertEquals(message_page.is_first_message_expression(), True)



































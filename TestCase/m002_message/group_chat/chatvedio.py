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

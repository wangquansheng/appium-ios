from appium.webdriver.common.mobileby import MobileBy
import time
import re
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatPicPage(BasePage):
    """选择照片页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GalleryActivity'

    __locators = {'返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
                  '相机胶卷': (MobileBy.XPATH,'//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]'),
                  '选择抖音': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[2]'),
                  #照片列表
                  '第一张照片': (MobileBy.XPATH,
                            '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypeImage'),
                  '第二张照片': (MobileBy.XPATH,
                            '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell[2]/XCUIElementTypeOther/XCUIElementTypeImage'),
                  '第三张照片': (MobileBy.XPATH,
                            '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell[3]/XCUIElementTypeOther/XCUIElementTypeImage'),
                  #选择照片
                  '发送': (MobileBy.IOS_PREDICATE, 'name CONTAINS "发送"'),
                  '取消': (MobileBy.ACCESSIBILITY_ID, '取消'),
                  '返回到群聊页面': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
                  '所有照片': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text'),
                  'com.chinasofti.rcs:id/select_rl': (MobileBy.ID, 'com.chinasofti.rcs:id/select_rl'),
                  '切换按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/drop_down_image'),
                  '照片分类选项': (MobileBy.ID, 'com.chinasofti.rcs:id/albumTitle'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  '列表容器': (MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView_gallery'),
                  'com.chinasofti.rcs:id/rl_img': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_img'),
                  '预览播放视频按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_video_icon'),
                  '播放视频按钮预览': (MobileBy.ID, 'com.chinasofti.rcs:id/pv_item'),
                  'com.chinasofti.rcs:id/imageview_video_start_background': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/imageview_video_start_background'),
                  'com.chinasofti.rcs:id/imageview_video_start': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/imageview_video_start'),
                  '00:02': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_video_time'),
                  'com.chinasofti.rcs:id/iv_gallery': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_gallery'),
                  'com.chinasofti.rcs:id/rliv_select': (MobileBy.ID, 'com.chinasofti.rcs:id/rliv_select'),
                  'com.chinasofti.rcs:id/iv_select': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_select'),
                  '00:03': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_video_time'),
                  '视频时长': (MobileBy.XPATH, '//*[contains(@name, "chatFile_video")]/following-sibling::*[1]'),
                  'com.chinasofti.rcs:id/rl_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_panel'),
                  '所有视频': (MobileBy.XPATH,
                           "//*[@resource-id='com.chinasofti.rcs:id/iv_video_icon']/../android.widget.RelativeLayout[@resource-id='com.chinasofti.rcs:id/rliv_select']"),
                  '所有图片': (MobileBy.XPATH,
                           "//android.widget.RelativeLayout[@resource-id='com.chinasofti.rcs:id/rl_img']/android.widget.RelativeLayout[1][not(contains(@resource-id,'com.chinasofti.rcs:id/iv_video_icon'))]"),
                  '预览': (MobileBy.ID, '预览'),
                  '原图': (MobileBy.ID, '原图'),
                  # '发送': (MobileBy.XPATH, '//*[contains(@name, "发送")]'),
                  '选择图片': (MobileBy.ACCESSIBILITY_ID, '选择图片'),
                  '直接点击图片': (MobileBy.XPATH,
                           "//XCUIElementTypeCell/XCUIElementTypeOther[count(XCUIElementTypeOther)=0]/XCUIElementTypeImage"),
                  '图片': (MobileBy.XPATH,
                         '//XCUIElementTypeCell/XCUIElementTypeOther[count(XCUIElementTypeOther)=0]/XCUIElementTypeButton[contains(@name,"cc chat picture unselected")]'),
                  '视频': (MobileBy.XPATH,
                         '//*[contains(@name, "chatFile_video")]/../preceding-sibling::XCUIElementTypeButton[1]'),
                  }

    @TestLogger.log('选择相机胶卷')
    def click_camara_picture(self):
        self.click_element(self.__locators["相机胶卷"])

    @TestLogger.log('选择第一张照片')
    def select_first_picture(self):
        self.click_element(self.__locators["第一张照片"])

    @TestLogger.log()
    def click_send(self, times=3):
        """点击发送"""
        self.click_element(self.__class__.__locators["发送"])
        time.sleep(times)

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在选择照片页面"""

        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self.is_text_present('本地照片')
            )
            return True
        except:
            return False

    @TestLogger.log("校验提示最多只能选择一个视频")
    def is_toast_exist_more_video(self):
        """校验提示最多只能选择一个视频"""
        return self.is_toast_exist("最多只能选择一个视频", 3)

    @TestLogger.log("校验提示照片和视频不能同时发送")
    def is_toast_exist_pv(self):
        """校验提示照片和视频不能同时发送"""
        return self.is_toast_exist("不能同时选择照片和视频", 3)

    @TestLogger.log()
    def get_pic_send_nums(self):
        """获取图片发送数量"""
        el = self.get_element(self.__class__.__locators["发送"])
        info = el.text
        num = info[-2]
        return num

    @TestLogger.log("判断是否有提示：最多只能勾选9张照片")
    def is_toast_exist_maxp(self):
        """提示最多只能勾选9张照片"""
        return self.is_toast_exist("最多只能选择9张照片", 3)

    @TestLogger.log()
    def wait_for_page_load(self, timeout=10, auto_accept_alerts=True):
        """等待选择照片页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["选择图片"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log("下一页")
    def page_up(self):
        """向上滑动一页"""
        self.swipe_by_direction(self.__locators['列表容器'], 'up')

    @TestLogger.log()
    def select_video(self, n=0):
        """选择视频
         :Args: - n  - 第n个视频
        """
        # 切换 视频 选项
        self.click_element(self.__class__.__locators['切换按钮'])
        self.click_element((MobileBy.XPATH, "//*[contains(@text, '视频')]"))
        time.sleep(1)
        videos = self.get_elements(self.__class__.__locators["所有视频"])
        if videos:
            try:
                videos[n].click()
            except:
                raise AssertionError("在所有照片首页没有 %s 个视频，请上传视频." % (n + 1))
        else:
            raise AssertionError("在所有照片首页没有视频")

    @TestLogger.log()
    def get_video_times(self):
        """获取视频时长"""
        # 切换 视频 选项
        self.click_element(self.__class__.__locators['切换按钮'])
        self.click_element((MobileBy.XPATH, "//*[contains(@text, '视频')]"))
        time.sleep(1)
        videos = self.get_elements(self.__class__.__locators["视频时长"])
        times = []
        if videos:
            for el in videos:
                times.append(el.text)
            return times
        else:
            raise AssertionError("在所有照片首页没有视频")

    @TestLogger.log()
    def select_pic(self, n=1):
        """选择n个图片"""
        # 切换 选项
        self.click_element(self.__class__.__locators['切换按钮'])
        time.sleep(1.8)
        items = self.get_elements(self.__class__.__locators['照片分类选项'])
        items_names = []
        if items:
            for item in items:
                items_names.append(item.text)
        tmp_list = []
        for tmp in items_names:
            if "视频" in tmp:
                tmp_list.append(tmp)
            if "所有照片" in tmp:
                tmp_list.append(tmp)
        items_names = [i for i in items_names if i not in tmp_list]
        # 选择一个选项发送图片
        send_items = "pic"
        for item in items_names:
            num = re.match(r'.*\((\d+)\)$', item).group(1)
            num = int(num)
            if num > 9:
                send_items = item
                break
        self.click_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % send_items))
        time.sleep(1.8)
        pics = self.get_elements(self.__class__.__locators["所有图片"])
        if n > len(pics):
            raise AssertionError("在所有照片首页没有 %s 张图片，请上传图片." % n)
        for i in range(n):
            pics[i].click()

    @TestLogger.log()
    def select_pic_fk(self, n=1):
        """选择n个图片"""
        # 切换到有图片选项
        self.click_element(self.__class__.__locators['切换按钮'])
        time.sleep(2)
        self.click_element((MobileBy.XPATH, "//*[contains(@text, 'pic')]"))
        pics = self.get_elements(self.__class__.__locators['所有图片'])
        if n > len(pics):
            raise AssertionError("在所有照片首页没有 %s 张图片，请上传图片." % n)
        for i in range(n):
            pics[i].click()
            time.sleep(0.5)

    @TestLogger.log()
    def select_video_fk(self, n=1):
        """选择n个视频"""
        # 切换 选项
        self.click_element(self.__class__.__locators['切换按钮'])
        time.sleep(1.8)
        items = self.get_elements(self.__class__.__locators['照片分类选项'])
        items[1].click()
        videos = self.get_elements(self.__class__.__locators['所有视频'])
        if n > len(videos):
            raise AssertionError("在所有照片首页没有 %s 张视频，请上传视频." % n)
        for i in range(n):
            videos[i].click()

    @TestLogger.log()
    def click_pic_preview(self):
        """点击图片阅览"""
        pics = self.get_elements(self.__class__.__locators["所有图片"])
        if not pics:
            raise AssertionError("There is no pic.")
        pics[0].click()
        pics[0].parent.find_element(MobileBy.ID, 'com.chinasofti.rcs:id/iv_gallery').click()

    @TestLogger.log()
    def click_preview(self):
        """点击预览"""
        self.click_element(self.__class__.__locators["预览"])

    @TestLogger.log()
    def send_btn_is_enabled(self):
        """获取发送按钮状态是否可点击"""
        return self._is_enabled(self.__class__.__locators["发送"])

    @TestLogger.log()
    def send_preview_is_enabled(self):
        """获取预览按钮状态是否可点击"""
        return self._is_enabled(self.__class__.__locators["预览"])

    @TestLogger.log()
    def get_pic_send_num(self):
        """获取图片发送数量"""
        el = self.get_element(self.__class__.__locators["发送"])
        info = el.text
        num = info[-2]
        return num

    @TestLogger.log()
    def pre_video_btn_is_enabled(self):
        """获取预览播放视频按钮按钮状态是否可点击"""
        return self._is_enabled(self.__class__.__locators["播放视频按钮预览"])

    @TestLogger.log()
    def click_back_back(self):
        """点击返回到群聊页面"""
        self.click_element(self.__class__.__locators["返回到群聊页面"])

    @TestLogger.log()
    def select_picture(self, index=0):
        """选择图片"""
        if self._is_element_present2(self.__class__.__locators["图片"]):
            els = self.get_elements(self.__class__.__locators["图片"])
            els[index].click()

    @TestLogger.log()
    def select_pictures(self, nums=1):
        """选择多个图片"""
        els = self.get_elements(self.__class__.__locators["图片"])
        for i in range(nums):
            els[i].click()

    @TestLogger.log()
    def select_one_video(self, index=0):
        """选择某个视频"""
        if self._is_element_present2(self.__class__.__locators["视频"]):
            els = self.get_elements(self.__class__.__locators["视频"])
            els[index].click()

    @TestLogger.log()
    def picture_btn_is_enabled(self, nums=1):
        """获取某一张图片按钮状态是否可点击"""
        els= self.get_elements(self.__class__.__locators["图片"])
        return els[nums-1].is_enabled()

    @TestLogger.log()
    def get_send_text(self):
        """获取发送按钮文本"""
        text = self.get_element(self.__class__.__locators["发送"]).text
        return text[3]

    @TestLogger.log()
    def get_send_video_text(self):
        """获取发送视频按钮文本"""
        text = self.get_element(self.__class__.__locators["发送"]).text
        return text

    @TestLogger.log()
    def click_picture_just(self):
        """直接点击图片"""
        self.click_element(self.__class__.__locators["直接点击图片"])

    @TestLogger.log()
    def get_video_text(self):
        """判断视频时长文本是否包含'：'"""
        text = self.get_element(self.__class__.__locators["视频时长"]).text
        print(text)
        if ":" in text:
            return True
        else:
            return False

    @TestLogger.log()
    def get_pic_numbers(self):
        """获取当前页面图片数量"""
        if self._is_element_present2(self.__class__.__locators["图片"]):
            els = self.get_elements(self.__class__.__locators["图片"])
            return len(els)

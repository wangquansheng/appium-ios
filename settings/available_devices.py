# 可用手机以及启动配置
from library.core.common.simcardtype import CardType
from library.core.common.supportedmodel import SupportedModel

# 测试APP信息
TARGET_APP = dict(
    # DOWNLOAD_URL="https://www.pgyer.com/apiv2/app/install?_api_key=298b363e3288c07f2683b96ca9bc5ab6&appKey=andfetiondev&buildPassword=qwer!234",
    DOWNLOAD_URL="http://dlrcs.fetion-portal.com/mobile/RCS_V6.2.9.0313_20190313.apk",
    APP_PACKAGE="com.chinasofti.rcs",
    APP_ACTIVITY="com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
    INSTALL_BEFORE_RUN=False
)

# ======================= 移动CI环境手机配置 =======================
AVAILABLE_DEVICES = {
    'M960BDQN229CH': {
        "MODEL": SupportedModel.HUAWEI_P20,
        "SERVER_URL": 'http://221.176.34.113:5000/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "8DF6R17526001515",
            "udid": "8DF6R17526001515",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            #  6.2.8
            # "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
            #  6.2.9
            "appActivity": "com.cmic.module_main.ui.activity.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '18875905984'
            },
        ]
    },
}

# ======================= 本地CI环境手机配置 =======================
AVAILABLE_DEVICES_DEV = {
    'M960BDQN229CH': {
        "MODEL": SupportedModel.MEIZU_PRO_6_PLUS,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0.1",
            "deviceName": "M960BDQN229DK",
            "udid": "M960BDQN229DK",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmic.module_main.ui.activity.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '13410559632'
            },
        ]
    },

    'M960BDQN229CK_20': {
        "MODEL": SupportedModel.HUAWEI_P20,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "9.0",
            "deviceName": "DWT7N18614014715",
            "udid": "DWT7N18614014715",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '18875905984'
            },
            None
        ]
    },
    'M960BDQN229CH-bak': {
        "MODEL": SupportedModel.MEIZU_PRO_6_PLUS,
        "SERVER_URL": 'http://192.168.200.112:4724/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "M960BDQN229CH",
            "udid": "M960BDQN229CH",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '19876283465'
            },
        ]
    },
    'M960BDQN229CH_me': {
        "MODEL": SupportedModel.RED_MI_NOTE_4X,
        "SERVER_URL": 'http://192.168.1.103:4724/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "VCO7IFTKKZZ5FI9T",
            "udid": "VCO7IFTKKZZ5FI9T",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '14775290489'
            },
        ]
    },
    'single_mobile': {
        "MODEL": SupportedModel.RED_MI_NOTE_4X,
        "SERVER_URL": 'http://192.168.1.104:4724/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "VCO7IFTKKZZ5FI9T",
            "udid": "VCO7IFTKKZZ5FI9T",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '14775290489'
            },
        ]
    },
    'single_telecom': {
        "MODEL": SupportedModel.RED_MI_NOTE_4X,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "VCO7IFTKKZZ5FI9T",
            "udid": "VCO7IFTKKZZ5FI9T",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_TELECOM,
                'CARD_NUMBER': '15338821645'
            },
        ]
    },
    'single_union': {
        "MODEL": SupportedModel.RED_MI_NOTE_4X,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "VCO7IFTKKZZ5FI9T",
            "udid": "VCO7IFTKKZZ5FI9T",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_UNION,
                'CARD_NUMBER': '18681151872'
            },
        ]
    },
    'double_mobile': {
        "MODEL": SupportedModel.RED_MI_NOTE_4X,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "VCO7IFTKKZZ5FI9T",
            "udid": "VCO7IFTKKZZ5FI9T",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '14775290489'
            },
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '19876283465'
            }
        ]
    },
    'mobile_and_union': {
        "MODEL": SupportedModel.RED_MI_NOTE_4X,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "VCO7IFTKKZZ5FI9T",
            "udid": "VCO7IFTKKZZ5FI9T",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '14775290489'
            },
            {
                'TYPE': CardType.CHINA_UNION,
                'CARD_NUMBER': '18681151872'
            }
        ]
    },
    'others_double': {
        "MODEL": SupportedModel.RED_MI_NOTE_4X,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "VCO7IFTKKZZ5FI9T",
            "udid": "VCO7IFTKKZZ5FI9T",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_TELECOM,
                'CARD_NUMBER': '15338821645'
            },
            {
                'TYPE': CardType.CHINA_UNION,
                'CARD_NUMBER': '18681151872'
            }
        ]
    }
}

# ======================= 个人本机执行环境手机配置 =======================
DEVICES_CONFIG_XIN = {
    'M960BDQN229CH': {
        "MODEL": SupportedModel.HUAWEI_P20,
        "SERVER_URL": 'http://apple.appium:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "8.0.0",
            "deviceName": "LKX0218814000312",
            "udid": "LKX0218814000312",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
            # "appPackage": "com.meizu.flyme.launcher",
            # "appActivity": ".Launcher",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '19876283465'
            },
        ]
    },
    # 'M960BDQN229CH': {
    #     "MODEL": SupportedModel.HUAWEI_P20,
    #     "SERVER_URL": 'http://221.176.34.113:5000/wd/hub',
    #     "DEFAULT_CAPABILITY": {
    #         "platformName": "Android",
    #         "platformVersion": "6.0",
    #         "deviceName": "8DF6R17526001515",
    #         "udid": "8DF6R17526001515",
    #         "automationName": "UiAutomator2",
    #         "newCommandTimeout": 600,
    #         "appPackage": "com.chinasofti.rcs",
    #         # "appPackage": "com.huawei.android.launcher",
    #         "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
    #         # "appActivity": ".unihome.UniHomeLauncher",
    #     },
    #     'CARDS': [
    #         {
    #             'TYPE': CardType.CHINA_MOBILE,
    #             'CARD_NUMBER': '14775970982'
    #         },
    #     ]
    # },
    # '红米Note4X': {
    #     "MODEL": SupportedModel.RED_MI_NOTE_4X,
    #     "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
    #     "DEFAULT_CAPABILITY": {
    #         "platformName": "Android",
    #         "platformVersion": "6.0",
    #         "deviceName": "VCO7IFTKKZZ5FI9T",
    #         "udid": "VCO7IFTKKZZ5FI9T",
    #         "automationName": "UiAutomator2",
    #         "newCommandTimeout": 600,
    #
    #         "appPackage": "com.chinasofti.rcs",
    #         "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
    #     },
    #     'CARDS': [
    #         {
    #             'TYPE': CardType.CHINA_MOBILE,
    #             'CARD_NUMBER': '14775290489'
    #         },
    #     ]
    # }
}

# DEVICES_CONFIG_YYX = {
#     'M960BDQN229CH': {
#         "MODEL": SupportedModel.HUAWEI_P20,
#         "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
#         "DEFAULT_CAPABILITY": {
#             "platformName": "Android",
#             "platformVersion": "8.1.0",
#             "deviceName": "JUBNU18816112025",
#             "udid": "JUBNU18816112025",
#             "automationName": "UiAutomator2",
#             "newCommandTimeout": 600,
#             "appPackage": "com.chinasofti.rcs",
#             "appActivity": "com.cmic.module_main.ui.activity.WelcomeActivity",
#         },
#         'CARDS': [
#             {
#                 'TYPE': CardType.CHINA_MOBILE,
#                 'CARD_NUMBER': '19864759568'
#             },
#         ]
#     },
# }

DEVICES_P20 = {
    'M960BDQN229CH': {
        "MODEL": SupportedModel.HUAWEI_P20,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "8.1.0",
            "deviceName": "CLB7N18904002073",
            "udid": "CLB7N18904002073",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmic.module_main.ui.activity.WelcomeActivity",
        },

        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '15918730974'
            },
        ]
    },
}

DEVICES_CONFIG_Nova = {
    'M960BDQN229CH': {
        "MODEL": SupportedModel.HUAWEI_P20,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "8.0.0",
            "deviceName": "8GP4C18720026139",
            "udid": "8GP4C18720026139",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '13537795364'
            },
        ]
    },
}

DEVICES_CONFIG_LXD = {
    # 'iphone': {
    #     "MODEL": SupportedModel.iPhone_XR,
    #     "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
    #     "DEFAULT_CAPABILITY": {
    #         "platformName": "ios",
    #         "platformVersion": "11.4.1",
    #         "deviceName": "iPhone8plus",
    #         "udid": "c72a846c88da4ff39aefe9451bcdde6f072b3f19",
    #         "automationName": "XCUITest",
    #         # "app": "cn.10086.rcs.beta",
    #         "app": "com.cmcc.enterprise-classID",
    #         "newCommandTimeout": 60,
    #         "xcodeOrgId": "A9TUX82M4W",
    #         "xcodeSigningId": "iPhone Developer"
    #     },
    #     'CARDS': [
    #         {
    #             'TYPE': CardType.CHINA_MOBILE,
    #             'CARD_NUMBER': '19874361585'
    #         },
    #     ]
    # },

    'iphone': {
        "MODEL": SupportedModel.iPhone_XR,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "ios",
            "platformVersion": "12.0.1",
            "deviceName": "iPhoneX",
            "udid": "6caf201048fe1199619e61da9b856014f5590d01",
            "automationName": "XCUITest",
            # "app": "cn.10086.rcs.beta",
            "app": "com.cmcc.enterprise-classID",
            "newCommandTimeout": 60,
            "xcodeOrgId": "A9TUX82M4W",
            "xcodeSigningId": "iPhone Developer"
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '14775451723'
            },
        ]
    },

    'M960BDQN229CHiphone8': {
        "MODEL": SupportedModel.iPhone8plus,
        "SERVER_URL": 'http://127.0.0.1:4724/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "ios",
            "platformVersion": "12.1.2",
            "deviceName": "iPhone7plus",
            "udid": "a0b733da2fbe5a9203910b008866fdedf574126c",
            "automationName": "XCUITest",
            # "app": "cn.10086.rcs.beta",
            "app": "com.cmcc.enterprise-classID",
            "xcodeOrgId": "A9TUX82M4W",
            "xcodeSigningId": "iPhone Developer"
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '15875537272'
            },
        ]
    },
}

DEVICES_CONFIG_YX = {
    'M960BDQN229CH': {
        "MODEL": SupportedModel.HUAWEI_P20,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "8.1.0",
            "deviceName": "DWT7N18614014715",
            "udid": "DWT7N18614014715",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '19849476421'
            },
        ]
    },
}

DEVICES_CONFIG_MATES = {
    'M960BDQN229CH': {
        # "MODEL": SupportedModel.HUAWEI_P20,
        "SERVER_URL": 'http://localhost:8100/status',
        "DEFAULT_CAPABILITY": {
            "platformName": "ios",
            "platformVersion": "12.1",
            "deviceName": "iPhone XR",
            "udid": "00008020-00011C1E2108002E",
            "automationName": "XCUITest",
            "app": "com.cmcc.enterprise-classID",
            "xcodeOrgId": "42J4UB47JC",
            "xcodeSigningId": "iPhone Developer"
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '19876283465'
            },
        ]
    },
}

DEVICES_CONFIG_nova3 = {
    'M960BDQN229CH': {
        "MODEL": SupportedModel.HUAWEI_P20,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "8.1.0",
            "deviceName": "DRB5T18721004015",
            "udid": "DRB5T18721004015",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmic.module_main.ui.activity.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '19876463625'
            },
        ]
    },
}

DEVICES_CONFIG_YMS2 = {
    'M960BDQN229CH': {
        "MODEL": SupportedModel.HUAWEI_P20,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "8.0.0",
            "deviceName": "RKKDU18321000975",
            "udid": "RKKDU18321000975",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmic.module_main.ui.activity.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '15875537272'
            },
        ]
    },
}

DEVICES_CONFIG_IOS = {
    'iphone': {
        "MODEL": SupportedModel.iPhone_XR,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "ios",
            "platformVersion": "12.1",
            "deviceName": "iPhone8plus酸梅",
            "udid": "7b5fcad5014e08f959214654bcc38077e557e7e0",
            "automationName": "XCUITest",
            "app": "com.cmcc.enterprise-classID",
            "xcodeOrgId": "42J4UB47JC",
            "newCommandTimeout": 60,
            "xcodeSigningId": "iPhone Developer"
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '18727021785'
            },
        ]
    },
    'M960BDQN229CHiphone8': {
        "MODEL": SupportedModel.iPhone8plus,
        "SERVER_URL": 'http://127.0.0.1:4724/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "ios",
            "platformVersion": "12.0.1",
            "deviceName": "iPhone8plus酸梅",
            "udid": "7b5fcad5014e08f959214654bcc38077e557e7e0",
            "automationName": "XCUITest",
            "app": "com.cmcc.enterprise-classID",
            "xcodeOrgId": "42J4UB47JC",
            "xcodeSigningId": "iPhone Developer"
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '18822825240'
            },
        ]
    },
}

DEVICES_CONFIG_IOS_YX = {
    # 'iphone': {
    #     "MODEL": SupportedModel.iPhone8plus,
    #     "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
    #     "DEFAULT_CAPABILITY": {
    #         "platformName": "ios",
    #         "platformVersion": "12.0.1",
    #         "deviceName": "iPhone6s",
    #         "udid": "6f861cac57078f8f7d18429dafbbd9a6db09a5ec",
    #         "automationName": "XCUITest",
    #         # "app": "cn.10086.rcs.beta",
    #         "app": "com.cmcc.enterprise-classID",
    #         "xcodeOrgId": "42J4UB47JC",
    #         "xcodeSigningId": "iPhone Developer"
    #     },
    #     'CARDS': [
    #         {
    #             'TYPE': CardType.CHINA_MOBILE,
    #             'CARD_NUMBER': '18822825240'
    #         },
    #     ]
    # },
    'iphone': {
        "MODEL": SupportedModel.iPhone_XR,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "ios",
            "platformVersion": "12.1",
            "deviceName": "iPhone XR",
            "udid": "00008020-00011C1E2108002E",
            "automationName": "XCUITest",
            "app": "com.cmcc.enterprise-classID",
            "xcodeOrgId": "42J4UB47JC",
            "newCommandTimeout": 60,
            "xcodeSigningId": "iPhone Developer"
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '19849476421'
            },
        ]
    },
    'M960BDQN229CHiphone8': {
        "MODEL": SupportedModel.iPhone8plus,
        "SERVER_URL": 'http://127.0.0.1:4724/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "ios",
            "platformVersion": "12.0.1",
            "deviceName": "iPhone8plus酸梅",
            "udid": "7b5fcad5014e08f959214654bcc38077e557e7e0",
            "automationName": "XCUITest",
            "app": "cn.10086.rcs.beta",
            "xcodeOrgId": "42J4UB47JC",
            "xcodeSigningId": "iPhone Developer"
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '18727021785'
            },
        ]
    },
}

DEVICES_CONFIG_IPHONEX = {
    'iphone': {
        "MODEL": SupportedModel.iPhone_XR,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "ios",
            "platformVersion": "11.4.1",
            "deviceName": "iPhone X",
            "udid": "c72a846c88da4ff39aefe9451bcdde6f072b3f19",
            "automationName": "XCUITest",
            # "app": "cn.10086.rcs.beta",
            "app": "com.cmcc.enterprise-classID",
            "xcodeOrgId": "S3LCRQ36CK",
            "newCommandTimeout": 60,
            "xcodeSigningId": "iPhone Developer"
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '19874361585'
            },
        ]
    },
}

DEVICES_CONFIG_YYX = {
    'iphone': {
        "MODEL": SupportedModel.iPhone_XR,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "ios",
            "platformVersion": "12.1.2",
            "deviceName": "iPhone7plus",
            "udid": "a0b733da2fbe5a9203910b008866fdedf574126c",
            "automationName": "XCUITest",
            "app": "cn.10086.rcs.beta",
            # "app": "com.cmcc.enterprise-classID",
            "newCommandTimeout": 60,
            "xcodeOrgId": "A9TUX82M4W",
            "xcodeSigningId": "iPhone Developer"
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '19875537272'
            },
        ]
    },
}

DEVICES_CONFIG_WJH = {
    'iphone': {
        "MODEL": SupportedModel.iPhone_XR,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "ios",
            "platformVersion": "11.0.1",
            "deviceName": "iPhone 8",
            "udid": "d20ea7886c5fcea7f6494de6b878f94bb1cf3727",
            "automationName": "XCUITest",
            "app": "cn.10086.rcs.beta",
            "xcodeOrgId": "TCBU5AR586",
            "newCommandTimeout": 60,
            "xcodeSigningId": "iPhone Developer"
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '14775970982'
            },
        ]
    },
    'M960BDQN229CHiphone8': {
        "MODEL": SupportedModel.iPhone_XR,
        "SERVER_URL": 'http://127.0.0.1:4725/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "ios",
            "platformVersion": "12.0.1",
            "deviceName": "iPhone7st",
            "udid": "13ca1b2deeeac7446f3a0cec3fec65dc6875714a",
            "automationName": "XCUITest",
            "app": "cn.10086.rcs.beta",
            "xcodeOrgId": "92GST8LVB9",
            "newCommandTimeout": 60,
            "xcodeSigningId": "iPhone Developer"
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '14775451723'
            },
        ]
    },
}

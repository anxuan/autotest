INIT_FID_COUNT = 3000           # 只返回最近两千条
APP_TASK_SEND_INTERVAL = 0.2    # app任务多久检查一次，发现合适的client就发送任务
WEB_TASK_SEND_INTERVAL = 0.2    # web任务多久检查一次，发现合适的client就发送任务

DB_CONFIG = {
    'NAME': 'hive',
    'USER': 'root',
    'HOST': '39.107.69.11',
    'PORT': '3306',
    'PASSWORD': 'Hive11223344abcdez!',
}

ACTION_LIST = (
    # worker
    ('new', '有新fid房源'),
    ('beat', '客户端心跳'),
    ('init_fid', '给worker初始化fid'),
    ('task', '向客户端发送任务的标识'),  # app请求
    ('task_web', '向客户端发送请求网页链接任务的标识'),

    # consumer
    ('call', '手机上开始打电话'),
    ('update_phone', '手机端获取到phone后提交socket后台更新'),
    ('get_phone_string', '手机端获取最近几千条手机号'),
    ('set_phone_string', '设置相应的值')
)

HEADERS_APP = {
    'apkbus': '',
    'User-Agent': 'okhttp/3.4.2',
    'official': 'true',
    'Accept-Encoding': 'zip,deflate',
    'ua': 'EVA-AL00',
    'uuid': 'b945be62-3efc-4af6-b4fa-48e6de08c399',
    'dirname': 'jn',
    'jumpinfo': '',
    'productorid': '1',
    'osv': '7.0',
    'brand': 'HUAWEI',
    'apn': 'WIFI',
    'lat': '',
    'X-Tingyun-Lib-Type-N-ST': '3;1548427304314',
    'rnsoerror': '0',
    'x-forwarded-for': '182.81.169.20',
    'version': '8.0.2',
    'ltext': '',
    'currentcid': '',
    'nettype': 'wifi',
    'bangbangid': '',
    'androidid': '47p5cb3clds756q0',
    'cid': '265',
    '58mac': '00',
    'lon': '',
    'rimei': '341548427304313',  # -
    'nop': '',
    'platform': 'android',
    'id58': '99188488906875',
    'uid': '',
    'PPU': '',
    'osarch': 'arm64-v8a',
    'bundle': 'com.wuba',
    'uniqueid': '06g41cbwq37151sz3rs98f3ym6vjok16',  # -
    'totalsize': '25.1',
    'owner': 'baidu',
    'product': '58app',
    'os': 'android',
    'Connection': 'Keep-Alive',
    'Host': 'apphouse.58.com',
    'm': '00',
    'deviceid': '47p5cb3clds756q0',
    'r': '1794_1080',
    'xxzl_deviceid': 'M3AwNjNyOGQ4cW80M3N3bTF5ZTkwMWkycGsyMWdtNDExMTdqZmxmMG1vdmwzeWIw',
    'xxzl_smartid': '',
    '58ua': '58app',
    'maptype': '2',
    'imei': '341548427304313',
    'tn': '',
    'location': '',
    'channelid': '671',
    'locationstate': ''
}



# coding: utf-8
#! python3
"""
客户端运行appium测试任务，需要首先运行此脚本，以接收服务端的任务

"""
import os
import sys
import json
import socket
import subprocess
from datetime import datetime as dt
import websocket

try:
    import thread
except ImportError:
    import _thread as thread
import time


client_name = socket.gethostname()  # 'HPCL201810018deMacBook-Pro'
HEART_BEAT_RATE = 5                 # 每几秒与server通信一次
# SERVER_HOST = 'localhost:8000'
SERVER_HOST = 'localhost:8000'
WEBSOCK_URL = "ws://%s/ws/test_task/" % SERVER_HOST
TMP_DIR = './tmp'                   # 脚本等文件存放于当前的tmp目录
if not os.path.exists('./tmp'):
    os.makedirs(TMP_DIR)
    print('created new tmp dir: %s' % TMP_DIR)

if not os.path.exists('./client_config.json'):
    raise Exception('task_client.py所在目录不存在配置文件client_config.json，请先找开发人员获取!')
with open('./client_config.json') as f:
    try:
        config = json.loads(f.read())
        print('config:', config)
    except Exception as e:
        print('配置文件client_config.json格式不对，解析失败!')
        raise e


def process_message(ws, message):
    res = json.loads(message)
    if res['message'] == 'run':
        def run(*args):
            task_id = res['task_id']
            content = res['script_file_content']
            task_name = res['task_name']
            tm_str = dt.now().strftime('%Y%m%d%H%M%S')
            print('run task...')

            if not os.path.exists(TMP_DIR):
                os.mkdir(TMP_DIR)
            script_file = '%s/appium_tid%s_%s.py' % (TMP_DIR, task_id, tm_str)
            # with open('/Users/wangxudong1129/projects/hupu/test/auto_test/ws_client/runtest_tmpl1.py') as f:
            #     tmpl = f.read()
            with open(script_file, 'w') as f:
                f.write(content)
                print('write file succ:', script_file)

            cmd = "%s %s" % (config['python_executable'], script_file)

            sub = subprocess.Popen(cmd,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   )  # close_fds=True
            out = sub.stdout.read()
            err = sub.stderr.read()

            print('out:', out)
            print('err:', err)

            res_dic = {
                'client_name': client_name,
                'action': 'update_task',
                'message': 'run end',
                'status': 'end',
                'task_id': task_id,

                'cmd': cmd,
                'out': str(out, encoding='utf-8'),
                'err': str(err, encoding='utf-8')
            }
            ws.send(json.dumps(res_dic))
            print('task run end...')

        thread.start_new_thread(run, ())
    print('received:', message, dt.now().strftime('%Y-%m-%d %H:%M:%S'))


def on_message(ws, message):
    try:
        process_message(ws, message)
    except Exception as e:
        print('on_message error:', e)


def on_error(ws, error):
    print('on_error:', error)
    if 'Connection refused' in str(error):
        time.sleep(3)


def on_close(ws):
    print("### closed ###")
    time.sleep(2)


def on_open(ws):
    print('服务端 %s 连接成功..' % WEBSOCK_URL)

    def run(*args):
        while True:
            dic = {
                'action': 'beat',
                'client_name': client_name,
                'os_type': sys.platform,
                'message': 'ok',
                'dt': str(dt.now()),
                "hubPort": '4444',
                "hubHost": "127.0.0.1",
            }
            ws.send(json.dumps(dic))
            time.sleep(HEART_BEAT_RATE)

    thread.start_new_thread(run, ())


class TaskClient(object):

    def run(self):
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(WEBSOCK_URL,
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close
                                    )
        # TRY TO RECONNECT
        while True:
            try:
                ws.run_forever(ping_interval=5)
            except:
                pass


if __name__ == '__main__':
    TaskClient().run()


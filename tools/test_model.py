import sys, os, json
from os.path import abspath, join, pardir, dirname
from dateutil.parser import parse as dt_parse

import django

sys.path.append(abspath(join(dirname(__file__), pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auto_test.settings")
django.setup()

from django.contrib.auth.models import User
from app_test.models import ScriptTmpl


with open('/Users/wangxudong1129/projects/hupu/test/auto_test/ws_client/runtest_tmpl.py') as f:
    tmpl = f.read()
    # print(type(tmpl))
    # print(tmpl)

st = ScriptTmpl.objects.get(id=1)
print(st.content)
print(type(st.content))
print(tmpl == st.content)
with open('/Users/wangxudong1129/projects/hupu/test/auto_test/ws_client/runtest_tmpl1.py', 'w') as f:
    f.write(st.content)


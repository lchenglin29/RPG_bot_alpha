import json,datetime,pytz

def load_json(name):
  with open(f'data/{name}.json', mode='r', encoding="utf8") as jFile:
      jdata = json.load(jFile)
#  print(f'[{name}.json] 讀取！')
  jFile.close()
  return jdata

def write_js(name,data):
  jsdata = json.dumps(data,ensure_ascii=False)
  with open(f'data/{name}.json', mode='w', encoding="utf8") as jFile:
    jFile.write(jsdata)
    jFile.close()
#    print(f'[{name}.json] 寫入！')

def now_time():
    current_time = datetime.datetime.now()
    timezone = pytz.timezone('Asia/Taipei')
    localized_time = current_time.astimezone(timezone)
    return localized_time.strftime("%Y-%m-%d %H:%M")
from mydef.mydef import load_json,write_js

def check_back(data):
  data["back"] = {key: value for key, value in data["back"].items() if value["amount"] > 0}
  return data

class users:
  def __init__(self,id):
    try:
      data = load_json(id)
    except FileNotFoundError:
      data = {
        "id":id,
        "global_plot_point":[],
        "badge":[],
        "save":[],
        "saves":{
        }
      }
      write_js(id,data)
      data = load_json(id)
    for key in data:
      setattr(self,key,data[key])
  def create_save(self,name,player_name,avatar):
    data = {
        'avatar':avatar,
        'name': player_name,
        'hp':100,
        'max_hp':100,
        'atk':10,
        'def':10,
        'handle':[],
        'armor':[],
        'reputation':50,
        'location':'ch1',
        'plot_point':[],
        'condition':[],
        'back':{
          '石劍':{
            'amount':1,
            'tags':['weapon','handleable']
          },
          'T-shirt':{
            'amount':1,
            'tags':['armor','wearable']
          }
        }
    }
    print('屬性沒抓到')
    self.saves[name] = data
    print('屬性有抓到')
    self.save_file()
    print("鍋在儲存")
  def save_file(self):
    try:
      data = self.__dict__
      write_js(self.id,data)
    except Exception as e:
      print(e)
    

class players:
  def __init__(self,id:str):
    self.id = id
    try:
      data = check_back(load_json(id)["saves"][load_json(id)["save"][0]])
    except:
      return
    for key in data:
      setattr(self,key,data[key])
  
  def save_file(self):
    try:
      all_data = load_json(self.id)
      all_data["saves"][all_data["save"][0]] = self.__dict__
      write_js(self.id,all_data)
    except Exception as e:
      print(e)
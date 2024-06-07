import json
import os

class SpiderCfg:
    def __init__(self, json_file_path=None) -> None:
        self.json_file_path = json_file_path
        if self.json_file_path==None:
            self.cfg = {
                    "driver_settings":{
                    "browser_executable_path":"/opt/chrome/chrome-linux64/chrome",
                    "driver_executable_path":"/opt/chrome/chromedriver-linux64/chromedriver"
                },
                "plans": [
                    {
                        "name": "plan0",
                        "init_url":"https://jiaotong.baidu.com/congestion/country/city/",
                        "variable_names": ["req_url"],
                        "setup_js_code":r'''document.datas=[];document.stop_flag=true;''',
                        "interval_js_code":r'''document.stop_flag=false;document.datas.push($.get("${req_url}"));document.stop_flag=true;''',
                        "break_flag_js_code":r"return document.stop_flag;",
                        "query_condition_js_code":r"return document.datas.length",
                        "final_js_code":r"return document.datas;",
                        "variables_value_in_interval_py_code":r"[{'req_url':f'https://jiaotong.baidu.com/trafficindex/overview/hishighwayroadrank?cityCode={cityCode}&startDay={startDay}&endDay={endDay}'} for cityCode,startDay,endDay in var_values]",
                        "pre_run_py_code":r'''import time;import os;import json;var_values=[(248,20240315,20240316)]''',
                        "final_run_py_code":r'''f=open(f"./out.json","w");json.dump(final_query,f);f.close();''',
                        "except_run_py_code":r'''exec(input(">>>"));print("error")''',
                        "interval_py_code":"1",
                        "waiting_interval_py_code":r'''print(f"running, step:{query_result}          \r",end="")''',
                    }
                ]
            }
        else:
            with open(self.json_file_path,"r",encoding="utf-8") as f:
                self.cfg=json.load(f)
    def set_item(self, plan_ind, key, value):
        if plan_ind>=len(self.cfg['plans']):
            self.cfg['plans'].append({
                        "name": "plan0",
                        "init_url":"https://jiaotong.baidu.com/congestion/country/city/",
                        "variable_names": ["req_url"],
                        "setup_js_code":r'''document.datas=[];document.stop_flag=true;''',
                        "interval_js_code":r'''document.stop_flag=false;document.datas.push($.get("${req_url}"));document.stop_flag=true;''',
                        "break_flag_js_code":r"return document.stop_flag;",
                        "query_condition_js_code":r"return document.datas.length",
                        "final_js_code":r"return document.datas;",
                        "variables_value_in_interval_py_code":r"[{'req_url':f'https://jiaotong.baidu.com/trafficindex/overview/hishighwayroadrank?cityCode={cityCode}&startDay={startDay}&endDay={endDay}'} for cityCode,startDay,endDay in var_values]",
                        "pre_run_py_code":r'''import time;import os;import json;var_values=[(248,20240315,20240316)]''',
                        "final_run_py_code":r'''f=open(f"./out.json","w");json.dump(final_query,f);f.close();''',
                        "except_run_py_code":r'''exec(input(">>>"));print("error")''',
                        "interval_py_code":"1",
                        "waiting_interval_py_code":r'''print(f"running, step:{query_result}          \r",end="")''',
                    })
            self.cfg['plans'][plan_ind]['name']=f"plan{plan_ind}"
        self.cfg['plans'][plan_ind][key]=value
    def save_json(self, path):
        with open(path,"w",encoding="utf-8") as f:
            json.dump(self.cfg,f)
    def copy_item(self, ind):
        self.cfg['plans'].append(self.cfg['plans'][ind].copy())
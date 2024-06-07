#!/home/naq/anaconda3/envs/spider/bin/python
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
import time
import pickle
import tqdm
import os
from selenium_stealth import stealth
from fake_useragent import UserAgent
from spider_setting import SpiderCfg
import sys

def main(cfg_file=None, plan_ind:list=[]):
    if cfg_file==None:
        if len(sys.argv)<2:
            cfg=SpiderCfg()
        else:
            cfg=SpiderCfg(json_file_path=sys.argv[-1])
    else:
        if type(cfg_file)==str:
            cfg=SpiderCfg(json_file_path=cfg_file)
        else:
            cfg=cfg_file
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-insecure-localhost')
    chrome_options.add_argument('--ignore-urlfetcher-cert-requests')
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--proxy-server=socks://172.29.0.1:10808')
    chrome_options.add_argument('--disable-gpu')
    driver = Chrome(options=chrome_options,
            **cfg.cfg['driver_settings']
            )
    # size
    rrr=[]
    driver.set_window_size(100, 100)
    if len(plan_ind)==0:
        pass
    else:
        for i in plan_ind:
            rrr.append(cfg.cfg['plans'][i])
        cfg.cfg['plans']=rrr

    for plan in cfg.cfg['plans']:
        print(f"Starting plan: {plan['name']}")
        exec(plan['pre_run_py_code'])

        driver.get(plan['init_url'])

        iters=eval(plan['variables_value_in_interval_py_code'])
        js_code_to_run=plan['setup_js_code']
        driver.execute_script(js_code_to_run)

        for itr in iters:
            js_code_to_run=plan['interval_js_code']
            for var in itr:
                js_code_to_run=js_code_to_run.replace(f"${'{'+var+'}'}",itr[var])
            try:
                driver.execute_script(js_code_to_run)
            except:
                exec(plan['except_run_py_code'])
            while not driver.execute_script(plan['break_flag_js_code']):
                time.sleep(float(eval(plan['interval_py_code'])))
                query_result=driver.execute_script(plan['query_condition_js_code'])
                exec(plan['waiting_interval_py_code'])
            final_query=driver.execute_script(plan['final_js_code'])
            exec(plan['final_run_py_code'])
        print(f"Plan {plan['name']} done.")

if __name__=="__main__":
    main()


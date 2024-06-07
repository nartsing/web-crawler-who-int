#!/root/anaconda3/envs/spider/bin/python
from spider_setting import SpiderCfg
from framework import main
import json
import sys
import pickle


if __name__=="__main__":
    if True:
        parms=pickle.load(open("./urls.pkl","rb"))
        cfg=SpiderCfg("./spider_cfg.json")
        dep=len(parms)//100
        for i in range(99):
            cfg.copy_item(0)
        for i in range(0, 100):
            cfg.set_item(
                i,"name",f"plan{i}"
            )
            cfg.set_item(
                i,"init_url","https://platform.who.int/mortality/themes/theme-details/mdb/injuries"
            )
            if i==99:
                cfg.set_item(
                    i,"setup_js_code",f'''
                    document.datas=[];document.pause_flag=false;document.parms={str(parms[i*(dep):])};document.max_num=document.parms.length;
                '''
                )
            else:
                cfg.set_item(
                    i,"setup_js_code",f'''
                    document.datas=[];document.pause_flag=false;document.parms={str(parms[i*(dep):(i+1)*(dep)])};document.max_num=document.parms.length;
                '''
                )
            cfg.set_item(
                i,"interval_js_code",r'''
                    document.interval_ids=setInterval(()=>{
                        // 定时发送get请求，并且将结果push进datas
                        if(document.pause_flag){
                            return;
                        }
                        if(document.datas.length==document.max_num){
                            document.pause_flag=true;
                            clearInterval(document.interval_ids);
                        }
                        if(document.parms.length==0){
                            return;
                        }
                        parm=document.parms.pop();
                        url_target=`https://apps.who.int/data/mortality/api/EN/facts/query?queryJson=${parm['parm']}`;
                        $.ajax({
                            url: url_target,
                            method: 'GET',
                            timeout: 60000, // 设置请求超时时间（毫秒）
                            success: function(data) {
                                document.datas.push({"url":this.url,"data":data})
                            },
                            error: function(jqXHR, textStatus, errorThrown) {
                                document.datas.push({"url":this.url,"status":jqXHR.status, "msg":textStatus})
                            }
                        });},100);
            '''
            )
        #cfg.save_json("./spider_cfg.json")
    main(cfg, [i for i in range(90,100)])






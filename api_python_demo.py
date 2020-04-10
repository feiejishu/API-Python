#coding:utf-8

import time
import hashlib
import requests

#说明：
URL = "http://api.feieyun.cn/Api/Open/"#不需要修改
USER = "xxxxxxxxxxxx"#*必填*：登录管理后台的账号名
UKEY = "xxxxxxxxxxxx"#*必填*: 注册账号后生成的UKEY
SN = "xxxxxxxxx"#*必填*：打印机编号，必须要在管理后台里手动添加打印机或者通过API添加之后，才能调用API
        

#签名
def signature(STIME):
    return hashlib.sha1(USER+UKEY+STIME).hexdigest();


def addprinter(snlist):
    STIME = str(int(time.time()))#不需要修改
    params = {
        'user':USER,
        'sig':signature(STIME),
        'stime':STIME,
        'apiname':'Open_printerAddlist',#固定值,不需要修改
        'printerContent':snlist
    }
    response = requests.post(URL,data=params,timeout=30)
    code = response.status_code #响应状态码
    if code==200:
        print response.content
    else:
        print "error"


def printOrder(sn):
    #标签说明：
    #单标签: 
    #"<BR>"为换行,"<CUT>"为切刀指令(主动切纸,仅限切刀打印机使用才有效果)
    #"<LOGO>"为打印LOGO指令(前提是预先在机器内置LOGO图片),"<PLUGIN>"为钱箱或者外置音响指令
    #成对标签：
    #"<CB></CB>"为居中放大一倍,"<B></B>"为放大一倍,"<C></C>"为居中,<L></L>字体变高一倍
    #<W></W>字体变宽一倍,"<QR></QR>"为二维码,"<BOLD></BOLD>"为字体加粗,"<RIGHT></RIGHT>"为右对齐
    #拼凑订单内容时可参考如下格式
    #根据打印纸张的宽度，自行调整内容的格式，可参考下面的样例格式
    
    content = "<CB>测试打印</CB><BR>"
    content += "名称　　　　　 单价  数量 金额<BR>"
    content += "--------------------------------<BR>"
    content += "饭　　　　　　 1.0    1   1.0<BR>"
    content += "炒饭　　　　　 10.0   10  10.0<BR>"
    content += "蛋炒饭　　　　 10.0   10  100.0<BR>"
    content += "鸡蛋炒饭　　　 100.0  1   100.0<BR>"
    content += "番茄蛋炒饭　　 1000.0 1   100.0<BR>"
    content += "西红柿蛋炒饭　 1000.0 1   100.0<BR>"
    content += "西红柿鸡蛋炒饭 100.0  10  100.0<BR>"
    content += "备注：加辣<BR>";
    content += "--------------------------------<BR>";
    content += "合计：xx.0元<BR>";
    content += "送货地点：广州市南沙区xx路xx号<BR>";
    content += "联系电话：13888888888888<BR>";
    content += "订餐时间：2016-08-08 08:08:08<BR>";
    content += "<QR>http://www.dzist.com</QR>"
    STIME = str(int(time.time()))#不需要修改
    params = {
        'user':USER,
        'sig':signature(STIME),
        'stime':STIME,
        'apiname':'Open_printMsg',#固定值,不需要修改
        'sn':sn,
        'content':content,
        'times':'1'#打印联数
    }
    response = requests.post(URL,data=params,timeout=30)
    code = response.status_code #响应状态码
    if code==200:
        print response.content#服务器返回的JSON字符串,建议要当做日志记录起来
    else:
        print "error"    
        

def queryOrderState(orderid):
    STIME = str(int(time.time()))#不需要修改
    params = {
        'user':USER,
        'sig':signature(STIME),
        'stime':STIME,
        'apiname':'Open_queryOrderState',#固定值,不需要修改
        'orderid':orderid
    }
    response = requests.post(URL,data=params,timeout=30)
    code = response.status_code #响应状态码
    if code==200:
        print response.content#返回的JSON字符串
    else:
        print "error"  



def queryOrderInfoByDate(sn,strdata):
    STIME = str(int(time.time()))#不需要修改
    params = {
        'user':USER,
        'sig':signature(STIME),
        'stime':STIME,
        'apiname':'Open_queryOrderInfoByDate',#固定值,不需要修改
        'sn':sn,
        'date':strdata,
    }
    response = requests.post(URL,data=params,timeout=30)
    code = response.status_code #响应状态码
    if code==200:
        print response.content#返回的JSON字符串
    else:
        print "error"  


def queryPrinterStatus(sn):
    STIME = str(int(time.time()))#不需要修改
    params = {
        'user':USER,
        'sig':signature(STIME),
        'stime':STIME,
        'apiname':'Open_queryPrinterStatus',#固定值,不需要修改
        'sn':sn,
    }
    response = requests.post(URL,data=params,timeout=30)
    code = response.status_code #响应状态码
    if code==200:
        print response.content#返回的JSON字符串
    else:
        print "error"  
        
        
        

#**********测试时，打开下面注释掉方法的即可,更多接口文档信息,请访问官网开放平台查看**********
if __name__ == '__main__':
    
    
    #==================添加打印机接口（支持批量）==================
    #***返回值JSON字符串***
    #成功：{"msg":"ok","ret":0,"data":"xxxxxxx_xxxxxxxx_xxxxxxxx","serverExecutedTime":5}
    #失败：{"msg":"错误描述","ret":非0,"data":"null","serverExecutedTime":5}
    
    #提示：打印机编号(必填) # 打印机识别码(必填) # 备注名称(选填) # 流量卡号码(选填)，多台打印机请换行（\n）添加新打印机信息，每次最多100行(台)。
    #snlist = "sn1#key1#remark1#carnum1\nsn2#key2#remark2#carnum2"
    #addprinter(snlist)
    
    
    
    #==================方法1.打印订单==================
    #***返回值JSON字符串***
    #成功：{"msg":"ok","ret":0,"data":"xxxxxxx_xxxxxxxx_xxxxxxxx","serverExecutedTime":5}
    #失败：{"msg":"错误描述","ret":非0,"data":"null","serverExecutedTime":5}
    #printOrder(SN)


    #===========方法2.查询某订单是否打印成功=============
    #***返回值JSON字符串***
    #成功：{"msg":"ok","ret":0,"data":true,"serverExecutedTime":2}//data:true为已打印,false为未打印
    #失败：{"msg":"错误描述","ret":非0, "data":null,"serverExecutedTime":7}
    #queryOrderState("xxxxxxxx_xxxxxxxx_xxxxxxxx");#订单ID，从方法1返回值data获取



    #===========方法3.查询指定打印机某天的订单详情============
    #***返回值JSON字符串***
    #成功：{"msg":"ok","ret":0,"data":{"print":6,"waiting":1},"serverExecutedTime":9}//print已打印，waiting为打印
    #失败：{"msg":"错误描述","ret":非0,"data":"null","serverExecutedTime":5}
    #queryOrderInfoByDate(SN,"2017-04-02")#注意时间格式为"yyyy-MM-dd"


    #===========方法4.查询打印机的状态==========================
    #***返回的状态有如下几种***
    #成功：{"msg":"ok","ret":0,"data":"状态","serverExecutedTime":4}
    #失败：{"msg":"错误描述","ret":非0,"data":"null","serverExecutedTime":5}
    #queryPrinterStatus(SN);

    pass









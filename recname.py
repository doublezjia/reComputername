#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : zealous (doublezjia@163.com)
# @Date    : 2019/6/25 16:56
# @Link    : https://github.com/doublezjia
# @Desc:

import os,shutil,sys
from datetime import datetime

base = "WIN-"
sn = os.popen("wmic bios get serialnumber").read()
Cname = base + sn.split()[1]

# 静默激活路径
kms = r"C:\IT工具\KMSpico\scripts\Silent.cmd"
# 注册表改名命令列表
reglist = [
r'reg add "HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\ComputerName\ActiveComputerName" /v ComputerName /t reg_sz /d {cname} /f'.format(cname=Cname),
r'reg add "HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\ComputerName\ComputerName" /v ComputerName /t reg_sz /d {cname} /f'.format(cname=Cname),
r'reg add "HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\Tcpip\Parameters" /v "NV Hostname" /t reg_sz /d {cname} /f'.format(cname=Cname),
r'reg add "HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\Tcpip\Parameters" /v Hostname /t reg_sz /d {cname} /f'.format(cname=Cname),
]

ping = 'ping 192.168.1.1 -n 1 >> ./temp/message.log'

sys64 = r'C:\Windows\SysWOW64'
netdomEXE = sys64 + r'\netdom.exe'
sys64enUS = r'C:\Windows\SysWOW64\en-US'
netdomEXEmui = sys64enUS + r'\netdom.exe.mui'
netdom = r'{netdom} join %computername% /Domain:localhost.domain.com /UserD:username /PasswordD:"{xiongdei}" /Reboot:10'

# xiongdei
def xiongDei():
    with open('./xiongdei.txt','r') as f:
        xiongdei = f.read()
    return xiongdei

# 检查netdom是否存在，不存在就复制过去
def netdomFile():
    if not os.path.isfile(netdomEXE):
        shutil.copy("./netdom/netdom.exe",netdomEXE)
    if not os.path.isfile(netdomEXEmui):
        shutil.copy("./netdom/netdom.exe.mui",netdomEXEmui)
    return 1

# 激活系统
def Kms():
    print('正在运行激活工具激活系统')
    if os.system(kms) == 0:
        print('系统激活成功')
    else:
        print('激活失败')
        print (r'请检查 C:\ITtool\KMSpico\scripts\Silent.cmd 这个文件是否存在.')
        print(r'稍后请手动激活.....')


 
# 计算机改名和加域
def reName_Joindomain():
    print('执行计算机名改名和加域操作。')
    # 新建目录
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    while True:
        print("正在检查域服务器网络连接是否正常，准备更改计算机名和加域")
        if os.system(ping) == 0:
            print ('域服务器正常PING通，进行改名加域操作')
            # 执行计算机名改名
            for reg in reglist:
                if os.system(reg+'>>./temp/message.log') == 0:
                    print('修改计算机名注册表成功。')
                else:
                    print('修改计算机名注册表失败，请检查是否管理员运行')
                    input('按回车键退出.....')
                    sys.exit()
            print('修改计算机名成功，进行加域操作.')

            # 获取xiongdei
            xiongdei = xiongDei()
            # 检查netdom是否存在，不存在就复制过去
            netdomFile()
            # 加域
            if os.system(netdom.format(netdom=netdomEXE,xiongdei=xiongdei)) == 0:
                print('加域成功，退出程序,10秒后重启电脑.')
                break  
            else:
                print('加域失败，退出程序，xiongdei检查一下是否有错。')
                input('按回车键退出.....')
                sys.exit()
        else:
            print('PING不通域服务器，请检查网络是否连接正常，然后任意键继续执行改名加域操作。')
            print('本机计算机名为%s' % Cname)
            os.system('pause')


# 删除目录
def delDir():
    print("删除程序缓存目录和封装目录。")
    if os.path.isdir(r'./temp'):
        shutil.rmtree(r'./temp',ignore_errors=True)
        print ('删除temp成功。')
    if os.path.isdir(r'C:\Intel'):
        shutil.rmtree(r'C:\Intel',ignore_errors=True)
        print(r'删除 C:\Intel 成功')
    if os.path.isdir(r'C:\test'):
        shutil.rmtree(r'C:\test',ignore_errors=True)
        print(r'删除 C:\test 成功')
    if os.path.isdir(r'C:\Sysprep'):
        shutil.rmtree(r'C:\Sysprep',ignore_errors=True)
        print(r'删除 C:\Sysprep 成功')

def main():
    # 第一步：激活系统
    print('第一步：激活系统')
    Kms()
    print('\n\n')

    # 第二步：改名加域
    print ('第二步：改名加域')
    reName_Joindomain()
    print('\n\n')

    # 第三步：删除多余文件夹
    print('第三步：删除多余文件夹')
    delDir()
    print('\n\n')


if __name__ == '__main__':
    main()
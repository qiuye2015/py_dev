#-*- coding: utf-8 -*-

import sys, win32api
import wx
import wx.lib.buttons as wxbtn
import winsound

"""给漂亮的计算器加上声音"""

APP_TITLE = '计算器' # 桌面程序的标题
APP_ICON = 'calculator.ico' # 桌面程序图标

class mainFrame(wx.Frame):
    """桌面程序主窗口类，继承自wx.Frame类"""
    
    def __init__(self):
        """构造函数"""
        
        style = wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.SIMPLE_BORDER
        wx.Frame.__init__(self, parent=None, id=-1, title=APP_TITLE, style=style)
        
        self.SetBackgroundColour((217, 228, 241)) # 设置窗口背景色
        self.SetSize((287, 283)) # 设置窗口大小
        self.Center() # 设置窗口屏幕居中
        
        if hasattr(sys, "frozen") and getattr(sys, "frozen") == "windows_exe": # 如果打包成exe文件，运行时执行此处代码
            exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None)) # 此处用到win32api模块
            icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO) # 读图标文件
        else : # 若以源码方式运行，则执行此处代码
            icon = wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO) # 读图标文件
        self.SetIcon(icon) # 设置图标
        
        # 用输入框控件作为计算器屏幕，设置为只读（wx.TE_READONLY）和右齐（wx.ALIGN_RIGHT）
        self.screen = wx.TextCtrl(self, -1, '', pos=(10,10), size=(252,45), style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        self.screen.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, '微软雅黑')) # 设置字体字号
        self.screen.SetBackgroundColour((0, 0, 0)) # 设置屏幕背景色
        self.screen.SetForegroundColour((0, 255, 0)) # 设置屏幕前景色
        
        # 按键布局参数
        btn_size = (60, 30)             # 定义按键的尺寸，便于统一修改
        x0, y0 = (10, 65)               # 定义按键区域的相对位置
        dx, dy = (64, 34)               # 定义水平步长和垂直步长
        
        # 定义按键排列顺序和名称
        allKeys = [
            ['(', ')', 'Back', 'Clear'],
            ['7',  '8',  '9',  '/'], 
            ['4',  '5',  '6',  '*'], 
            ['1',  '2',  '3',  '-'], 
            ['0',  '.',  '=',  '+']
        ]
        
        # 指定每个按键声音的频率，523赫兹就是C调中音
        self.keySound = {
            '(':392, ')': 440, '0':494, '1':523, '2':587, '3':659, '4':698, '5':784, '6':880, '7':988, '8':1047, 
            '9':1175, '.':1318, '+':523, '-':587, '*':659, '/':698, 'Clear':784, 'Back':880, '=':2000
        }
        
        # 生成所有按键
        for i in range(len(allKeys)):
            for j in range(len(allKeys[i])):
                # 添加按钮。请注意属性name的用法
                #btn_ = wx.Button(self, -1, allKeys[i][j], pos=(x0+j*dx, y0+i*dy), size=btn_size, name=allKeys[i][j])
                
                key = allKeys[i][j]
                btn = wxbtn.GenButton(self, -1, key, pos=(x0+j*dx, y0+i*dy), size=btn_size, name=key)
                if key in ['0','1','2','3','4','5','6','7','8','9','.']:
                    btn.SetBezelWidth(1)                                # 设置3D效果
                    btn.SetBackgroundColour(wx.Colour(217, 228, 241))   # 定义按键的背景色
                elif key in ['(',')','Back','Clear']:
                    btn.SetBezelWidth(2)
                    btn.SetBackgroundColour(wx.Colour(217, 220, 235))
                    btn.SetForegroundColour(wx.Colour(224, 60, 60))
                elif key in ['+','-','*','/']:
                    btn.SetBezelWidth(2)
                    btn.SetBackgroundColour(wx.Colour(246, 225, 208))
                    btn.SetForegroundColour(wx.Colour(60, 60, 224))
                else:
                    btn.SetBezelWidth(2)
                    btn.SetBackgroundColour(wx.Colour(245, 227, 129))
                    btn.SetForegroundColour(wx.Colour(60, 60, 224))
                    btn.SetToolTip(u"显示计算结果")
        
        # 绑定按钮事件（请注意：既非弹起，也不是按下，是按钮被点击）
        self.Bind(wx.EVT_BUTTON, self.onButton) # 将按钮事件绑定在所有按钮上
        
    def onButton(self, evt):
        """响应鼠标左键按下"""
        
        obj = evt.GetEventObject() # 获取事件对象（哪个按钮被按）
        key = obj.GetName() # 获取事件对象的名字
        
        self.PlayKeySound(key) # 播放按键对应频率的声音
        
        if key == 'Clear': # 按下了清除键，清空屏幕
            self.screen.SetValue('')
        elif key == 'Back': # 按下了回退键，去掉最后一个输入字符
            content = self.screen.GetValue()
            if content:
                self.screen.SetValue(content[:-1])
        elif key == '=': # 按下了等号键，则计算
            try:
                result = str(eval(self.screen.GetValue()))
            except:
                result = '算式错误，请Clear'
            self.screen.SetValue(result)
        else: # 按下了其他键，追加到显示屏上
            self.screen.AppendText(key)
    
    def PlayKeySound(self, key, Dur=100):
        """播放按键声音"""
        
        winsound.Beep(self.keySound[key], Dur)


class mainApp(wx.App): # 通常，mainApp类无需任何修改，看不明白的话，照抄即可
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = mainFrame()
        self.Frame.Show()
        return True

#----------------------------------------------------------------------
if __name__ == "__main__":
    app = mainApp() # 创建应用程序
    app.MainLoop() # 事件循环。wx是基于事件驱动的，每个事件都绑定了事件函数。一旦有事件发生，则触发对应的事件函数执行。
    
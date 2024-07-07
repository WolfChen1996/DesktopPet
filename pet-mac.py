'''
刀刀的猫猫
Made by Wolf
http://www.wolfchen.top
https://github.com/WolfChen1996/DesktopPet
'''
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from PIL import Image
import random
import sys
import os
import configparser
from setting import Ui_MainWindow

#初始化配置，并定义全局变量
#fp_dir=os.getcwd()
fp_dir=os.path.dirname(os.path.abspath(__file__))
print(fp_dir+'/config.ini')
config = configparser.ConfigParser()
configpath=fp_dir+'/config.ini'
config.read(configpath, encoding="utf-8-sig")
petidraw=config.get("config", "petids")
petids=petidraw.split(',')
petid=config.get("config", "petid")
traypath=config.get("config", "traypath")

#print(fp_dir+"/"+petid+"/petconfig.ini")
petconfig = configparser.ConfigParser()
petconfigpath=fp_dir+"/data/"+petid+"/petconfig.ini"
petconfig.read(petconfigpath, encoding="utf-8-sig")
petname=petconfig.get("config", "petname")
petscale=petconfig.getfloat("config", "petscale")
bottomfix=petconfig.getfloat("config", "bottomfix")
gamespeed=petconfig.getfloat("config", "gamespeed")
petspeed=petconfig.getfloat("config", "petspeed")
throwout=petconfig.get("config", "throwout")
intotray=petconfig.get("config", "intotray")
mirror=petconfig.get("config", "intotray")
dropspeed=petconfig.getfloat("config", "dropspeed")
gravity=petconfig.getfloat("config", "gravity")
dragingfixx=petconfig.getfloat("config", "dragingfixx")
dragingfixy=petconfig.getfloat("config", "dragingfixy")
fixdragspeedx=petconfig.getfloat("config", "dragspeedx")
fixdragspeedy=petconfig.getfloat("config", "dragspeedy")

petactionsraw=petconfig.get("config", "petaction")
petactionnumraw=petconfig.get("config", "petactionnum")
petactionrateraw=petconfig.get("config", "petactionrate")
standactionraw=petconfig.get("config", "standaction")
standactionnumraw=petconfig.get("config", "standactionnum")
standactionrateraw=petconfig.get("config", "standactionrate")

petactions=petactionsraw.split(',')
petactionnum=petactionnumraw.split(',')
petactionrate=petactionrateraw.split(',')
standaction=standactionraw.split(',')
standactionnum=standactionnumraw.split(',')
standactionrate=standactionrateraw.split(',')

image_url = fp_dir+'/data/'+ petid +'/'
image = image_url + 'main.png'
im = Image.open(image)
petwidth=int(im.size[0]*petscale)
petheight=int(im.size[1]*petscale)
bottomfix=bottomfix*petscale
screenwidth,screenheight=0,0
deskwidth,deskheight=0,0
deskbottom=0
onfloor=1
drop=1
dropa=0
draging=0
playid=1
playtime=0
playnum=1
playstand=-1
petaction,petaction2=0,0
mouseposx1,mouseposx2,mouseposx3,mouseposx4,mouseposx5=0,0,0,0,0
mouseposy1,mouseposy2,mouseposy3,mouseposy4,mouseposy5=0,0,0,0,0
dragspeedx,dragspeedy=0,0
petleft,pettop=0,0
gameleft,gamebottom=0,0
imgpath='main.png'

class App(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(App, self).__init__(parent)
        # initialize
        self.is_follow_mouse = False
        
        ### MAC用户看这里！！！For mac user!!!###
        # Mac用户可以把下面那行的#挪到windows那行，就可以看到猫了
        # Mac user can move the # from bottom line to the second line and you will see your pet.
        
        # Windows
        #self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow)
        # Mac
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        #self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        
        self.repaint()
        
        screen = QDesktopWidget().screenGeometry()
        desktop = QDesktopWidget().availableGeometry()
        self.tray()
        
        #修正开始菜单在左侧时拖动的定位
        global screenwidth,screenheight,deskwidth,deskheight,petleft,pettop
        screenwidth=screen.width()
        screenheight=screen.height()
        deskwidth=desktop.width()
        deskheight=desktop.height()
        gameleft=screenwidth-deskwidth
        gamebottom=deskheight-screenheight
        #self.setGeometry(0, 0, screen.width(), screen.height())
        #print("初始化宠物")
        #print('屏幕尺寸' ,screenwidth , '-' , screenheight)
        #print('桌面尺寸' ,deskwidth, '-' , deskheight)
        #print('宠物尺寸' ,petwidth , '-' , petheight)
        if intotray!="True":
            petleft = deskwidth-petwidth
            pettop = deskheight-petheight+bottomfix
        else:
            gameleft=0
            gamebottom=0
            petleft = screenwidth-petwidth
            pettop = screenheight-petheight+bottomfix

        # initial image
        petimage = image_url + 'start.png'
        #print(petimage)
        pix = QPixmap(petimage)
        pix = pix.scaled(petwidth, petheight, aspectRatioMode=Qt.KeepAspectRatio)
        self.lb1 = QLabel(self)
        self.lb1.setPixmap(pix)
        self.lb1.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lb1.customContextMenuRequested.connect(self.rightMenu)

        # display
        #print("BeginDisplay",pettop)
        petleft = int(petleft)
        pettop = int(pettop)
        self.move(int(petleft), int(pettop))
        self.resize(petwidth, petheight)
        self.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.game)
        self.timer.start(int(gamespeed))
    
    def game(self):
        #循环执行主函数
        global petwidth,playid,playtime,petaction,petaction2,playstand,playnum,petleft,pettop,imgpath
        ##print("loop:"+str(petaction))
        #print("Loop")
        right=0
        if drop==1 and onfloor==0:
            if draging==1:
                #print("Draging")
                playnum=int(petactionnum[3])
                if playid<int(petactionnum[3]):
                        imgpath=petactions[3]+str(playid)+'.png'
                        playid=playid+1
                else:
                    imgpath=petactions[3]+str(playid)+'.png'
                    playid=1
                
            elif draging==0:
                ##print("Falling")
                playnum=int(petactionnum[4])
                if playid<int(petactionnum[4]):
                        imgpath=petactions[4]+str(playid)+'.png'
                        playid=playid+1
                else:
                    imgpath=petactions[4]+str(playid)+'.png'
                    playid=1
                
            self.drop()

        if drop==0 or onfloor==1:
            
            if playtime==0:
                petaction=random.random()
                playstand=-1
                playid=1
            #print(petaction)
            #print(float(petactionrate[0])+float(petactionrate[1]))
            if petaction>=(float(petactionrate[0])+float(petactionrate[1])) and (petleft+petwidth+gameleft+petspeed)<deskwidth:
                ##print("Walking right")
                right=1
                playnum=int(petactionnum[2])
                if playid<int(petactionnum[2]):
                    imgpath=petactions[2]+str(playid)+'.png'
                    playid=playid+1
                    
                else:
                    imgpath=petactions[2]+str(playid)+'.png'
                    playid=1
                
                
                petleft=petleft+petspeed
                
                self.move(int(petleft), int(pettop))

                if playtime==0:
                    playtimemin=3
                    playtimemax=int((((deskwidth-(petleft+petwidth+gameleft)))/petspeed)/playnum)
                    if playtimemax<=3:
                        playtimemax=3
                playtime=int(playtime)-1
                #print("Right:"+str(petaction)+"."+str(playid)+"."+str(playtime))

            elif petaction<(float(petactionrate[0])+float(petactionrate[1])) and petaction>=float(petactionrate[0]) and (petleft-gameleft)>petspeed:
                playnum=int(petactionnum[1])
                if playid<int(petactionnum[1]):
                    imgpath=petactions[1]+str(playid)+'.png'
                    playid=playid+1
                    
                else:
                    imgpath=petactions[1]+str(playid)+'.png'
                    playid=1

                petleft=petleft-petspeed
                self.move(int(petleft), int(pettop))
                
                if playtime==0:
                    playtimemin=3
                    playtimemax=int((petleft-gameleft)/petspeed/playnum)
                    if playtimemax<=1:
                        playtimemax=1
                playtime=int(playtime)-1
                #print("Left:"+str(petaction)+"."+str(playid)+"."+str(playtime)+"playtimemax:"+str(petspeed))
                
            elif petaction<float(petactionrate[0]):
                #print("站立循环")

                if playstand==-1:
                    temp=random.random()
                    temp2=0
                    #print(temp)
                    for i in range(len(standactionrate)):
                        
                        if float(standactionrate[i])==0:
                            continue
                        temp2=temp2+float(standactionrate[i])
                        ##print("内循环："+str(i)+"累计概率："+str(temp2))
                        if temp<temp2:
                            petaction2=i
                            playnum=int(standactionnum[i])
                            playstand=1
                            ##print("GET!")
                            ##print(str(i)+":"+str(temp2))
                            break
                            
                            #playstand=random.randint(0,len(standaction))
                    if playstand==-1:
                        playnum=int(standactionnum[0])
                        playstand=1
                
                ##print("Playstand:"+str(playstand)+"Num:"+standactionnum[petaction2])
                if playstand<int(standactionnum[petaction2]):
                    #imgpath=standaction[i]+str(playid)+'.png'
                    imgpath=standaction[petaction2]+str(playstand)+'.png'
                    playstand=playstand+1
                else:
                    imgpath=standaction[petaction2]+str(playstand)+'.png'
                    playstand=1
                    playid=1
                
                if playtime==0:
                    playtimemin=1
                    playtimemax=1
                    
                playtime=int(playtime)-1
                ##print("Stand:"+str(petaction)+".Playid:"+str(playid)+"."+str(petaction2)+".Playstand:"+str(playstand)+".Playtime:"+str(playtime)+"Playnum:"+str(playnum))
                
                
                
            else:
                petaction=random.random()
                playstand=-1
            
            if playtime==-1:
                playtime=random.randint(1,playtimemax)*playnum
                
                
        petimage = image_url + imgpath
        print(petimage)
        #petimage=petimage.mirrored(True, False)
        pix = QPixmap(petimage)
        if right==1:
            tempimg = pix.toImage()
            tempimg = tempimg.mirrored(True, False)
            pix=QPixmap.fromImage(tempimg)
            
        pix=pix.scaled(petwidth, petheight, aspectRatioMode=Qt.KeepAspectRatio)
        self.lb1.setPixmap(pix)
        pass
    
    def rightMenu(self):
        menu = QMenu(self)
        menu.addAction(QAction(QIcon('./data/icon/deviceon.png'), '开启掉落', self, triggered=self.dropon))
        menu.addAction(QAction(QIcon('./data/icon/deviceoff.png'), '禁用掉落', self, triggered=self.dropoff))
        menu.addAction(QAction(QIcon('./data/icon/increase.png'), '放大', self, triggered=self.increase))
        menu.addAction(QAction(QIcon('./data/icon/decrease.png'), '缩小', self, triggered=self.decrease))
        menu.addAction(QAction(QIcon('./data/icon/eye_protection.png'), '隐藏', self, triggered=self.hide))
        menu.addAction(QAction(QIcon('./data/icon/settings.png'), '设置', self, triggered=self.setting))
        menu.addAction(QAction(QIcon('./data/icon/restore.png'), '重启', self, triggered=self.restart_program))
        menu.addAction(QAction(QIcon('./data/icon/close.png'), '退出', self, triggered=self.quit))
        menu.exec_(QCursor.pos())
        
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.is_follow_mouse = True
            global onfloor,draging,playid
            onfloor=0
            draging=1
            playid=1
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        global mouseposx1,mouseposx2,mouseposx3,mouseposx4,mouseposx5
        global mouseposy1,mouseposy2,mouseposy3,mouseposy4,mouseposy5
        global petleft,pettop
        if Qt.LeftButton and self.is_follow_mouse:
            petleft = QCursor.pos().x()-petwidth/2+dragingfixx*petscale
            pettop = QCursor.pos().y()-petheight/2+dragingfixy*petscale
            #mouseposx5=mouseposx4
            mouseposx4=mouseposx3
            mouseposx3=mouseposx2
            mouseposx2=mouseposx1
            mouseposx1=QCursor.pos().x()
            #mouseposy5=mouseposy4
            mouseposy4=mouseposy3
            mouseposy3=mouseposy2
            mouseposy2=mouseposy1
            mouseposy1=QCursor.pos().y()
            ##print("Moving")
            #print(petleft)
            #print(QCursor.pos().x() , '-' , petwidth/2 , '=' , petleft,'*')
            #print(QCursor.pos().y() , '-' , petheight/2, '=' , pettop)

            self.move(int(petleft), int(pettop))
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button()==Qt.LeftButton:
            global onfloor,dropa,draging,playid
            global dragspeedx,dragspeedy,mouseposx1,mouseposx3,mouseposy1,mouseposy3
            playid=1
            onfloor=0
            draging=0
            self.is_follow_mouse = False
            self.setCursor(QCursor(Qt.ArrowCursor))
            dropa=1
            dragspeedx=(mouseposx1-mouseposx3)/2*fixdragspeedx
            dragspeedy=(mouseposy1-mouseposy3)/2*fixdragspeedy
            mouseposx1=mouseposx3=0
            mouseposy1=mouseposy3=0
            ##print("mouseReleaseEvent")

    def tray(self):
        tray = QSystemTrayIcon(self)
        tray.setIcon(QIcon(traypath))
        menu = QMenu(self)

        menu.addAction(QAction(petname, self))
        menu.addAction(QAction(QIcon('./data/icon/eye_protection.png'),'显示', self, triggered=self.show))
        menu.addAction(QAction(QIcon('./data/icon/visible.png'), '隐藏', self, triggered=self.hide))
        menu.addAction(QAction(QIcon('./data/icon/deviceon.png'), '开启掉落', self, triggered=self.dropon))
        menu.addAction(QAction(QIcon('./data/icon/deviceoff.png'), '禁用掉落', self, triggered=self.dropoff))
        menu.addAction(QAction("打 * 功能有bug", self))
        menupick=QMenu(menu)
        menupick.setTitle("*选择宠物")
        
        menu.addMenu(menupick)
        #newpetid='cat1'
        #menupick.addAction(QAction(QIcon('./data/icon/collection.png'), '0', self, triggered=lambda:self.pick('0')))

        for temp in petids:
            if temp==petid:
                #menupick.addAction(QAction(QIcon('./data/icon/collection.png'),temp, self, triggered=lambda:self.pick(temp)))
                menupick.addAction(QAction(QIcon('./data/icon/collection.png'),temp, self, triggered=self.wrapped_pick(temp)))
            else:
                menupick.addAction(QAction(temp, self, triggered=self.wrapped_pick(temp)))

        menu.addSeparator()
        
        #menu.addAction(QAction(QIcon('./data/icon/increase.png'), '放大', self, triggered=self.increase))
        #menu.addAction(QAction(QIcon('./data/icon/decrease.png'), '缩小', self, triggered=self.decrease))
        menu.addAction(QAction(QIcon('./data/icon/settings.png'), '设置', self, triggered=self.setting))
        menu.addAction(QAction(QIcon('./data/icon/restore.png'), '重启', self, triggered=self.restart_program))
        menu.addAction(QAction(QIcon('./data/icon/close.png'), '退出', self, triggered=self.quit))
        
        tray.setContextMenu(menu)
        tray.show()
    '''
    def nextimg(self):
        image_url = './data/'+ petid +'/'
        petimage = image_url + 'stand1.png'
        self.img = QImage()
        self.img.load(petimage)
        print(petimage)
        self.image.setPixmap(QPixmap.fromImage(self.img))
    '''
    
    def wrapped_pick(self, id):
        def _(_):
            self.pick(id)
        return _
        
    def setting(self):
        #print("Setting")
        setting.show()
        
    def drop(self):
        #掉落
        #print("Dropping")
        global petleft,pettop
        global onfloor,dropa,dragspeedy
        if onfloor==0 and draging==0:
            ##print(dragspeedx)
            ##print(dragspeedy)
            #dropnext=pettop+info.gravity*dropa-info.gravity/2
            dropnext=pettop+dragspeedy+dropspeed
            movenext=petleft+dragspeedx
            if throwout!="True":
                if movenext<=gameleft:
                    movenext=gameleft
                elif movenext>screenwidth-petwidth:
                    movenext=(screenwidth-petwidth)
            
            dragspeedy=dragspeedy+gravity

            if dropnext>=(deskheight-petheight+gamebottom):
                pettop=deskheight-petheight+gamebottom
                petleft=movenext
                self.move(int(petleft), int(pettop))
                onfloor=1
                dropa=0
               
            elif dropnext<(deskheight-petheight+gamebottom):
                pettop=dropnext
                petleft=movenext
                self.move(int(petleft), int(pettop))
                

    def increase(self):
        global petscale,petwidth,petheight,bottomfix
        petscale=petscale*1.1
        petwidth=int(im.size[0]*petscale)
        petheight=int(im.size[1]*petscale)
        print(petwidth)
        bottomfix=bottomfix*petscale
        self.resize(petwidth, petheight)
        self.lb1.setGeometry(0,0,petwidth, petheight)
        #restart_program(self)
        
    def decrease(self):
        global petscale,petwidth,petheight,bottomfix
        petscale=petscale*0.9
        petwidth=int(im.size[0]*petscale)
        petheight=int(im.size[1]*petscale)
        bottomfix=bottomfix*petscale
        self.resize(petwidth, petheight)
        self.lb1.setGeometry(0,0,petwidth, petheight)
        #restart_program(self)

    
    def pick(self,newpetid):
        global petid
        petid=newpetid
        setting.loadpetconfig()
        
    def switchdrop(self):
        global drop
        sender = self.sender()
        if sender.text()=="禁用掉落":
            sender.setText("开启掉落")
            drop=0
        else:
            sender.setText("禁用掉落")
            drop=1     
            
    def dropon(self):
        global drop
        drop=1
        
    def dropoff(self):
        global drop
        drop=0
        
    def quit(self):
        self.close()
        sys.exit()

    def hide(self):
        self.setVisible(False)

    def show(self):
        self.setVisible(True)
        
    def restart_program(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)
        
    def quit(self):
        self.close()
        sys.exit()
    
class setting(QMainWindow, Ui_MainWindow):
    _startPos = None
    _endPos = None
    _isTracking = False
    def __init__(self, parent=None):
        super(setting, self).__init__(parent)
        
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        #self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        
        self.setupUi(self)
        
    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None
            
    
    def readcfg(self, MainWindow):
        self.settingpetid.setText(petid)
        self.settingpetlist.setPlainText(petidraw)
        self.settingtray.setText(traypath)

        self.settingpetname.setText(petname)
        self.settingscale.setText(str(petscale))
        self.settingbottomfix.setText(str(bottomfix))
        self.settingdragingfixx.setText(str(dragingfixx))
        self.settingdragingfixy.setText(str(dragingfixy))
        self.settingpetspeed.setText(str(petspeed))
        self.settinggamespeed.setText(str(gamespeed))
        self.settingspeedx.setText(str(fixdragspeedx))
        self.settingspeedy.setText(str(fixdragspeedy))
        self.settinggravity.setText(str(gravity))
        self.settingdropspeed.setText(str(dropspeed))
        self.settingpetaction.setText(petactionsraw)
        self.settingpetactionnum.setText(petactionnumraw)
        self.settingpetactionrate.setText(petactionrateraw)
        self.settingstandaction.setText(standactionraw)
        self.settingstandactionnum.setText(standactionnumraw)
        self.settingstandactionrate.setText(standactionrateraw)

        if throwout=="True":
            self.settingthrowout.setChecked(True)
        else:
            self.settingthrowout.setChecked(False)
        
        
        if intotray=="True":
            self.settingintotray.setChecked(True)
        else:
            self.settingintotray.setChecked(False)
        
        if intotray=="True":
            self.settingmirror.setChecked(True)
        else:
            self.settingmirror.setChecked(False)
        
    def savecfg1(self):
        config.set("config", "petid", self.settingpetid.text())  
        config.set("config", "petids", self.settingpetlist.toPlainText())  
        config.set("config", "traypath", self.settingtray.text())  
        config.write(open(configpath, "w", encoding="utf-8-sig"))
        
        self.loadconfig()
        self.readcfg(self)
        
    def savecfg2(self):
        petconfig.set("config", "petname", self.settingpetname.text())  
        petconfig.set("config", "petscale", self.settingscale.text())  
        petconfig.set("config", "bottomfix", self.settingbottomfix.text()) 
        petconfig.set("config", "dragingfixx", self.settingdragingfixx.text()) 
        petconfig.set("config", "dragingfixy", self.settingdragingfixy.text()) 
        petconfig.set("config", "petspeed", self.settingpetspeed.text()) 
        petconfig.set("config", "gamespeed", self.settinggamespeed.text()) 
        petconfig.set("config", "dragspeedx", self.settingspeedx.text()) 
        petconfig.set("config", "dragspeedy", self.settingspeedy.text()) 
        petconfig.set("config", "gravity", self.settinggravity.text()) 
        petconfig.set("config", "dropspeed", self.settingdropspeed.text()) 

        
        petconfig.set("config", "petaction", self.settingpetaction.text()) 
        petconfig.set("config", "petactionnum", self.settingpetactionnum.text()) 
        petconfig.set("config", "petactionrate", self.settingpetactionrate.text()) 
        petconfig.set("config", "standaction", self.settingstandaction.text()) 
        petconfig.set("config", "standactionnum", self.settingstandactionnum.text()) 
        petconfig.set("config", "standactionrate", self.settingstandactionrate.text()) 
        
        petconfig.set("config", "throwout", str(self.settingthrowout.isChecked()))
        petconfig.set("config", "intotray", str(self.settingintotray.isChecked()))
        petconfig.set("config", "mirror", str(self.settingmirror.isChecked()))
        petconfig.write(open(petconfigpath, "w", encoding="utf-8-sig"))
        
        self.loadpetconfig()
        self.readcfg(self)
    '''
        self.readcfg(MainWindow)
        self.save1.clicked.connect(MainWindow.savecfg1)
        self.save2.clicked.connect(MainWindow.savecfg2)
    '''
    def loadconfig(self):
        global configpath,petidraw,petids,petid,traypath
        #print(fp_dir+'/config.ini')
        config = configparser.ConfigParser()
        configpath=fp_dir+'/config.ini'
        config.read(configpath, encoding="utf-8-sig")
        petidraw=config.get("config", "petids")
        petids=petidraw.split(',')
        petid=config.get("config", "petid")
        traypath=config.get("config", "traypath")
    
    def loadpetconfig(self):
        print("LoadPetconfig")
        global petconfig,petname,petscale,bottomfix,gamespeed,petspeed,gravity,dragingfixx,dragingfixy,fixdragspeedx,fixdragspeedy,petactionnum,petactionrate,standaction,standactionnum,standactionrate,image_url,image,im,petwidth,petheight,petactionsraw,petactionnumraw,petactionrateraw,standactionraw,standactionnumraw,standactionrateraw,throwout,intotray,mirror,dropspeed
        
        fp_dir=os.getcwd()
        petconfig = configparser.ConfigParser()
        petconfig.read(fp_dir+"/data/"+petid+"/petconfig.ini", encoding="utf-8-sig")

        #print(fp_dir+"/"+petid+"/petconfig.ini")
        petconfig = configparser.ConfigParser()
        petconfig.read(fp_dir+"/data/"+petid+"/petconfig.ini", encoding="utf-8-sig")
        petname=petconfig.get("config", "petname")
        petscale=petconfig.getfloat("config", "petscale")
        bottomfix=petconfig.getfloat("config", "bottomfix")
        gamespeed=petconfig.getfloat("config", "gamespeed")
        petspeed=petconfig.getfloat("config", "petspeed")
        throwout=petconfig.get("config", "throwout")
        intotray=petconfig.get("config", "intotray")
        mirror=petconfig.get("config", "intotray")
        gravity=petconfig.getfloat("config", "gravity")
        dropspeed=petconfig.getfloat("config", "dropspeed")
        dragingfixx=petconfig.getfloat("config", "dragingfixx")
        dragingfixy=petconfig.getfloat("config", "dragingfixy")
        fixdragspeedx=petconfig.getfloat("config", "dragspeedx")
        fixdragspeedy=petconfig.getfloat("config", "dragspeedy")
        petactionsraw=petconfig.get("config", "petaction")
        petactionnumraw=petconfig.get("config", "petactionnum")
        petactionrateraw=petconfig.get("config", "petactionrate")
        standactionraw=petconfig.get("config", "standaction")
        standactionnumraw=petconfig.get("config", "standactionnum")
        standactionrateraw=petconfig.get("config", "standactionrate")
        
        petactions=petactionsraw.split(',')
        petactionnum=petactionnumraw.split(',')
        petactionrate=petactionrateraw.split(',')
        standaction=standactionraw.split(',')
        standactionnum=standactionnumraw.split(',')
        standactionrate=standactionrateraw.split(',')
        bottomfix=bottomfix*petscale
        image_url = './data/'+ petid +'/'
        image = image_url + 'main.png'
        im = Image.open(image)
        petwidth=int(im.size[0]*petscale)
        petheight=int(im.size[1]*petscale)
        bottomfix=bottomfix*petscale
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = App()
    setting = setting()
    sys.exit(app.exec_())

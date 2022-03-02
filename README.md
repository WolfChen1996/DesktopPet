# DesktopPet
《刀刀的猫猫》
作者：狗头人 www.wolfchen.top
qq群：980897840

修改宠物：
可直接进入对应文件夹修改图片；如需增减图片，需要修改文件夹中petconfig.ini文件（双击用文本文档打开即可），配置文件内有注释，对着修改每个状态对应的文件名即可。


添加宠物：
需要在config.ini文件中（右键》编辑，用文本文档打开即可），添加一个宠物的id，并前往data文件夹中添加一个和id对应的文件夹，并添加参数文件（从其他宠物的文件夹复制一个petconfig.ini过来）和图片。

【config.ini参数说明】
#这是配置文件，如果添加宠物，需要修改下面的petids数组；
#可以通过修改petid更改默认宠物。
#可以通过修改traypath修改托盘图标
[config]
#宠物id，可以是字母或者汉字，用英文逗号隔开
petids=1,2,cat1

#默认宠物的id
petid=cat1

#托盘图标路径
traypath=./data/tray.png



本项目由想养猫又养不了的大菜刀独家逼迫狗头人完成
早期参考了以下两个项目的框架
https://github.com/Laylar-sleep/DesktopPet
https://github.com/SpeedPromise/DesktopPet

特别感谢
xixi提供了切换宠物的代码思路
Maggie的鼓励
以及大菜刀的逼迫！
还有各位小伙伴的支持！

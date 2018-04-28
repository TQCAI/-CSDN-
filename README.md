# 解决CSDN不能直接插入图片的缺憾
CSDN是一个比较优秀的博客平台，但是美中不足的是不能直接插入剪切板图片。此项目用python3解决CSDN不能插入剪切板图片的缺憾

[toc]

下载地址
===
https://github.com/TQCAI/-CSDN-

---

效果演示
===
演示视频
---
![使用方法](https://img-blog.csdn.net/20180428232353862?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RRQ0FJNjY2/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
使用方法
---
1. 本项目用python3编写，确保本项目依赖的包全部安装上
2. 点击`启用服务.cmd`后，服务在后台启动。（注意修改脚本中的绝对路径）
3. 确保剪切板中复制有图片的情况下，按下`Ctrl+G`插入图片（和CSDN博客编辑界面插入图片的快捷键相同）
4. 在后台运行有剪切板服务时，按下`Ctrl+0` 关闭服务（`0` 是`backspace` 左侧的键）

---
源码讲解
===
将剪切板中的图片保存为文件
---
+ getImgFromClipboard.py
```python
from PIL import  Image
from PIL import ImageGrab
import numpy as np
import os
import sys
import pylab as plt
import win32con
import win32clipboard as w

def setText(aString):
    """设置剪贴板文本"""
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()

Path="剪切板图片"
PosFile=Path+"/pos.txt"

if __name__ == '__main__':
    im = ImageGrab.grabclipboard()
    if isinstance(im, Image.Image):
        img=np.array(im,dtype=np.uint8)
        if not os.path.exists(Path):
            os.makedirs(Path)
        if not os.path.exists(PosFile):
            fo = open(PosFile, "w")
            fo.write('1')
            fo.close()
        fo = open(PosFile, "r")
        try:
            pos=int(fo.read())
        except BaseException:
            pos=1
        fo.close()
        fo = open(PosFile, "w")
        fo.write(str(pos+1))
        fo.close()
        ImgFile=Path+'/'+str(pos)+'.jpg'
        plt.imsave(ImgFile,img)
        appDir=os.getcwd()  #os.path.split(sys.argv[0])[0]
        ansPath=appDir+'/'+ImgFile
        setText(ansPath.replace('/','\\'))
    else:
        print('您没有复制图片到剪切板')
```
用PIL的轮子，把剪切板的图片保存下来。有一大段代码是用来处理文件等操作的，本人小白，大佬轻虐
在后台监听键盘事件
---
CSDN插入图片的快捷键是`Ctrl+G`，为了方便操作，最好在**插入图片**事件发生的那一刻，运行对剪切板图片的操作
在这里我参考了GitHub的一个项目：
>https://github.com/ethanhs/pyhooked

+ watchKeyboard.py
```python
from pyhooked import Hook, KeyboardEvent
import os,sys

def handle_events(args):
    if isinstance(args, KeyboardEvent):
        print(args.key_code)
        if args.current_key == 'G' and args.event_type == 'key down' and 'Lcontrol' in args.pressed_key:
            os.system("python getImgFromClipboard.py")
        if args.current_key == '0' and args.event_type == 'key down' and 'Lcontrol' in args.pressed_key:
            print('exit')
            hk.stop()
            sys.exit(0)

if __name__ == '__main__':
    hk = Hook()  # make a new instance of PyHooked
    hk.handler = handle_events  # add a new shortcut ctrl+a, or triggered on mouseover of (300,400)
    hk.hook()  # hook into the events, and listen to the presses
```




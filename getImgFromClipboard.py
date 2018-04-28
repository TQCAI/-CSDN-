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
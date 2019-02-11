import os,sys
import re

rootDir='../../html'

htmlHeader='<!DOCTYPE html>\n\
<html lang="en">\n\
<head>\n\
	<meta charset="UTF-8">\n\
    <title>Title</title>\n\
	<meta name="viewport" content="initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no">\n\
	<link rel="stylesheet" href="/app.css">\n\
	<link rel="stylesheet" href="MYCSS">\n\
</head>'

def walkDir(path):
    try:
        os.chdir(path) #切换工作目录
    except:
        return
    list=os.listdir(os.curdir)
    for f in list:
        # print(fileName)
        if os.path.isdir(f):
            walkDir(f) 
            os.chdir(os.pardir) #将工作目录切换回当前目录
        else:            
            judgeFile(os.getcwd(),f)

def judgeFile(path,fileName):
    if(fileName.endswith("wxss")):
        #print("wxss",fileName)
        translateWxss(path,fileName)
    elif(fileName.endswith("wxml")):
        #print("wxml",fileName)
        translateWxml(path,fileName)

#翻译wxml
def translateWxml(path,fileName):
    oldFile=open(path+os.sep+fileName,"r")
    newFilePath=path+os.sep+fileName.replace('wxml','html')
    try:
        os.remove(newFilePath)
    except:
        print(newFilePath,"删除失败")
    
    newFile=open(newFilePath,'a')

    newFile.write(htmlHeader.replace('MYCSS',fileName.replace('wxml','css')))

    content=oldFile.readline()
    while content:
        #print("content===",content)
        content= content.replace('<view','<div').replace('</view>','</div>').replace('<image','<img')\
            .replace('</image>','').replace('<text','<span').replace('<text>','<span>')\
                .replace('</text>','</span>').replace('../../','')
        #print("修改后====",content)
        if content.find('style')>0 and content.find('rpx')>0:
            style=re.search('style\s*=\s*(\'[^\']*\'|"[^"]*")',content).group()
            newStyle=''
            itemList=style.split(';')
            for item in itemList:
                newStyle=newStyle+rpx2px(item)+';'
            newStyle=newStyle.replace(';";',';"')
            content=content.replace(style,newStyle)
            # print("newStyle=====",newStyle)
            # print("content===",content)
        newFile.write(content)  #新的文件中写入修改过的每行内容
        content=oldFile.readline()  #取出下一行内容

def translateWxss(path,fileName):
    oldFile=open(path+os.sep+fileName,"r")
    newFilePath=path+os.sep+fileName.replace('wxss','css')
    try:
        os.remove(newFilePath) #移除已经存在的css文件
    except :
        print(newFilePath,"删除失败")
    
    newFile=open(newFilePath,'a') #追加写入css文件
    content=oldFile.readline()  #读取第一行内容
    while content:
        
        # print("find====",content.find('rpx'))
        content=rpx2px(content)
        content= content.replace('page','body').replace('image','img').replace('view','div').replace('text','span')
        newFile.write(content)  #新的文件中写入修改过的每行内容
        content=oldFile.readline()  #取出下一行内容
      #  file.next()
    oldFile.close()
    newFile.close()

def rpx2px(content):
    if content.find('rpx')>0:
            value=content.split(':') #分割key value
            if len(value)>1:
                strList=value[1].split(' ') #分割每一项
                newValue=''
                for item in strList: # 取出每个
                    itemContentList=item.split('rpx') 
                    if len(itemContentList)>1: #如果包含rpx和其他数据
                        num=int(itemContentList[0]) #取出对应的rpx数据
                        # print("num===",num)
                        # print("num/2===",num/2)
                        itemContentList[0]=str(int(num/2))+'px' #将数据大小除以2，并添加单位，替换原来的数据
                    newItem=''
                    for itemConent in itemContentList:  #拼装空格分割的每项内容
                        newItem=newItem+itemConent 
                    
                    # print('oldItem',item)
                    # print('newItem',newItem)
                    newValue=newValue+' '+newItem # 拼装key value中的key
                # print(strList)
                # print(newValue)
                content=value[0]+':'+newValue #拼装key value
            # print("content====",content)
    return content




print("运行环境为",sys.version)
walkDir(rootDir)


# BilibiliDownLoad
![](./resources/timg.jpeg)

[TOC]

## 简介：

数据结构课程作品。一个能够下载B站视频的软件，还在开发当中。目前实现的功能有：
* 下载B站视频和弹幕
* 将弹幕生成词云图并保存
* 解析视频链接，得到清晰度等信息
* 可以选择清晰度进行下载
* 可以选择保存路径

## 效果展示
### 主体界面
![30%](./resources/ImageMainPage.png)
![30%](./resources/Downloading.png)
![30%](./resources/ImageDownLoad.png)
![30%](./resources/formatTransform.png)
### 下载结果
![30%](./resources/result.png)
![30%](./resources/wordcloud.png)
> 感谢蔡徐坤先生对开发过程中提供的素材支持 :smile:
## 依赖
* PyQt5
* moviepy
* wordcloud
* python3

## 依赖安装
```cmd
pip install pyqt5
pip install moviepy
pip install wordcloud
```

## 运行
windows 下双击main.py文件或通过VSCode之类的IDE运行main.py

## 注意
* 有些链接的视频不能下载，包括播放列表有多个视频的链接，视频格式不为dash的链接等，但大部分链接是可以的。如果链接的视频不能下载会有提示不能下载的原因。
* 使用链接为https://bilibili.com/av...的链接，其中省略号为视频的id，比如https://www.bilibili.com/video/av34337039 链接后面可能会有其他的字符比如https://www.bilibili.com/video/av50379490/?spm_id_from=333.334.b_63686965665f7265636f6d6d656e64.16 我们只取前面的https://www.bilibili.com/video/av50379490/
* 很多视频名称很长，**解析出来视频名称后可以在输入框中修改视频的名称**
* 词云字体用的是C:/WINDOWS/Fonts/SIMHEI.TTF，如果你的电脑对应路径没有这个字体就换一个中文字体，在DownLoad.py文件中对
```python
wordcloud = WordCloud(font_path="C:/WINDOWS/Fonts/SIMHEI.TTF",background_color="white",width=1000, height=860, margin=2).generate(text)
```
这一行进行修改
* 建议下载视频长度为几分钟的视频，清晰度选低一点的，这样下载快一点。而且由于下载完之后还要进行音频和视频的融合，会比较满，**视频如果太大会很久**
* 请别忘了设置保存路径

## 技术手段
### 界面
![20%](./resources/ImageDesigner.png)
使用pyqt5库进行开发，用Qt设计师软件对界面进行设计，然后通过pyuic5生成界面的python代码，利用qt的信号与槽机制来实现按钮等控件的后台行为。
### 视频和弹幕的获取
纯手工爬虫。解析视频链接，取出对应清晰度的视频链接和音频链接并下载（两者是分开的，如果只是下载视频视频没有声音）。用到requests,urllib、re、json库
### 视频的处理
下载完视频后将视频和音频进行合成，导出成MP4格式，用的是movepy库。

## 开发过程中的困难
1. 下载视频的时候窗口会阻塞，这是因为下载视频的函数没有办法马上就执行完，必须等到下载视频的函数结束了之后窗口才能被激活。否则视频没下载完窗口就会被阻塞而变成灰色，看起来就像卡了一样。解决方法是将下载视频的任务分配一个线程去运行，不要阻塞主线程
2. 进度条的功能是一大难点。要实现进度条的功能，就要分段下载视频，每段大概256B,还要知道下载视频的总大小，这样目前的进度就可以用目前下载的大小除以总大小获得。同时下载完每256字节就更新进度条的数值。这里又是一个困难，另外一个线程的任务没有办法影响进度条所在的窗口。解决方法是自定义一个qt信号量，要更新进度条的时候就发送这个信号，信号是可以跨线程的，绑定这个信号的槽函数接收到这个信号就更新进度条数值
3. 获取视频链接和音频链接的视频和音频。如果直接请求这两个链接的东西会失败，返回403Forbidden，解决方法是请求的时候加上一个header，模拟浏览器的行为，header里面还必须有refer字段
4. qt designer的使用上，设计时候的窗口大小跟实际运行的窗口大小不一样，实际的窗口大小变大。
5. 编码解码上的问题。爬下来的弹幕中文是乱码，词云图默认设置没有办法解析中文字符。

## 下一步的工作
1. 完成批量下载功能
2. 实现对除av链接的视频下载外，还有bangumi等链接的视频下载
3. 实现对除dash格式的视频下载
4. 用pyinstaller等工具打包成exe可执行文件
5. 程序图标和开启动画的制作

---

# 6月1日

截止到6月1号完成的工作如下

- 批量下载功能的实现
- 实现对/bangumi/ep类型的链接的视频的下载
- 除了dash格式外，对durl格式的视频也能下载
- 程序图标和开启动画

未完成：可执行文件的打包，复杂且意义不大，不做了

## 新成果展示：

### 对含有多个视频的链接进行解析，并选择性进行批量下载
![30%](./resources/批量下载页面.jpg)
![30%](./resources/链接解析.jpg)
![30%](./resources/设置.jpg)

### 开启动画
![30%](./resources/logo.png)



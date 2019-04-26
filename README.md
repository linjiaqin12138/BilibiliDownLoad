# BilibiliDownLoad

## 简介：

数据结构课程作品。一个能够下载B站视频的软件，还在开发当中。目前实现的功能有：
* 下载B站视频和弹幕
* 将弹幕生成词云图并保存
* 解析视频链接，得到清晰度等信息
* 可以选择清晰度进行下载
* 可以选择保存路径

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
使用pyqt5库进行开发，用Qt设计师软件对界面进行设计，然后通过pyuic5生成界面的python代码，利用qt的信号与槽机制来实现按钮等控件的后台行为
### 视频和弹幕的获取
纯手工爬虫。解析视频链接，取出对应清晰度的视频链接和音频链接并下载（两者是分开的，如果只是下载视频视频没有声音）
### 视频的处理
下载完视频后将视频和音频进行合成，导出成MP4格式

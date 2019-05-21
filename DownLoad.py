import logging
# 用到的库（有些可能没用到）
import requests
import re
import json
from urllib import request,error
import socket
import os
from moviepy.editor import *
from PyQt5.QtCore import QObject,pyqtSignal

# 自定义信号量
class ProcessSignal(QObject):
    trigger = pyqtSignal(float)
    merge_trigger = pyqtSignal()
    close_trigger = pyqtSignal()
    total_size = pyqtSignal(int)
    def update(self,value):
        self.trigger.emit(value)
    def merge(self):
        self.merge_trigger.emit()
    def close_message(self):
        self.close_trigger.emit()
    def TotalSize(self,value):
        self.total_size.emit(value)
    
def match1(text, *patterns):
    """Scans through a string for substrings matched some patterns (first-subgroups only).

    Args:
        text: A string to be scanned.
        patterns: Arbitrary number of regex patterns.

    Returns:
        When only one pattern is given, returns a string (None if no match found).
        When more than one pattern are given, returns a list of strings ([] if no match found).
    """

    if len(patterns) == 1:
        pattern = patterns[0]
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return None
    else:
        ret = []
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                ret.append(match.group(1))
        return ret

class MultiplePageError(Exception):
    def __init__(self,message):
        self.message = message
    def errorMessage(self):
        return self.message

class VideoFormatError(MultiplePageError):
    def __init__(self,message):
        super(VideoFormatError,self).__init__(message)


def urlopen_with_retry(*args, **kwargs):
    retry_time = 3
    for i in range(retry_time):
        try:
            return request.urlopen(*args, **kwargs)
        except socket.timeout as e:
            logging.debug('request attempt %s timeout' % str(i + 1))
            if i + 1 == retry_time:
                raise e
        # try to tackle youku CDN fails
        except error.HTTPError as http_error:
            logging.debug('HTTP Error with code{}'.format(http_error.code))
            if i + 1 == retry_time:
                raise http_error

def url_size(url, faker=False, headers={}):
    if faker:
        response = urlopen_with_retry(
            request.Request(url, headers=fake_headers)
        )
    elif headers:
        response = urlopen_with_retry(request.Request(url, headers=headers))
    else:
        response = urlopen_with_retry(url)

    size = response.headers['content-length']
    return int(size) if size is not None else float('inf')

class DownLoader(object):
    processsignal = ProcessSignal()
    # 提前了解到的关于哔哩哔哩的一些视频信息
    stream_types = [
        {'id': 'flv_p60', 'quality': 116, 'audio_quality': 30280,
         'container': 'FLV', 'video_resolution': '1080p', 'desc': '高清 1080P60'},
        # 'id': 'hdflv2', 'quality': 112?
        {'id': 'flv', 'quality': 80, 'audio_quality': 30280,
         'container': 'FLV', 'video_resolution': '1080p', 'desc': '高清 1080P'},
        {'id': 'flv720_p60', 'quality': 74, 'audio_quality': 30280,
         'container': 'FLV', 'video_resolution': '720p', 'desc': '高清 720P60'},
        {'id': 'flv720', 'quality': 64, 'audio_quality': 30280,
         'container': 'FLV', 'video_resolution': '720p', 'desc': '高清 720P'},
        {'id': 'hdmp4', 'quality': 48, 'audio_quality': 30280,
         'container': 'MP4', 'video_resolution': '720p', 'desc': '高清 720P (MP4)'},
        {'id': 'flv480', 'quality': 32, 'audio_quality': 30280,
         'container': 'FLV', 'video_resolution': '480p', 'desc': '清晰 480P'},
        {'id': 'flv360', 'quality': 16, 'audio_quality': 30216,
         'container': 'FLV', 'video_resolution': '360p', 'desc': '流畅 360P'},
        # 'quality': 15?
        {'id': 'mp4', 'quality': 0},
    ]
    def __init__(self,url):
        # 构造函数
        self.url = url

    @staticmethod
    def bilibili_headers(referer=None, cookie=None):
        # 请求消息的头部，模拟浏览器的行为访问Bilibili网站，否则访问会被拒绝
        ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        headers = {'User-Agent': ua}
        if referer is not None:
            headers.update({'Referer': referer})
        if cookie is not None:
            headers.update({'Cookie': cookie})
        return headers
    @staticmethod
    def get_content(url, headers={}, decoded=True):
        # 获取链接的html文件
        logging.debug('get_content: %s' % url)
        data = None
        session = requests.Session()
        try:
            response = session.get(url, headers=headers,verify=False)
        except:
            raise
        else:
            data = response.text

        return data

    def prepare(self):
        # 解析视频链接信息的函数
        self.stream_qualities = {s['quality']: s for s in self.stream_types}
        #获得html源代码
        html_content = self.get_content(self.url, headers=self.bilibili_headers())
        #视频信息获取，视频信息就藏在html的<script>标签内的一个json对象里面
        initial_state_text = match1(html_content,r'__INITIAL_STATE__=(.*?);\(function\(\)')  
        self.initial_state = json.loads(initial_state_text)
        playinfo_text = match1(html_content, r'__playinfo__=(.*?)</script><script>')  
        self.playinfo = json.loads(playinfo_text) if playinfo_text else None
        #视频数目，必须为1否则不能下载，要改用批量下载功能去下载
        # TODO 设置界面的提醒视频数目
        pn = self.initial_state['videoData']['videos']
        #视频题目
        self.title = self.initial_state['videoData']['title']
        #当前视频质量编号 整数
        self.currentQuality = self.playinfo['data']['quality']
        #可选视频质量列表
        qualityIDs = []
        for i in self.playinfo['data']['accept_quality']:
            if i in (116,80,74,64,48,32,16):#我们只对stream_types里面有的视频质量进行下载
                qualityIDs.append(i)
        #可选的视频质量列表
        self.acceptQualitys = [self.stream_qualities[id]['desc'] for id in qualityIDs]

        if pn > 1:
            raise MultiplePageError("链接中包含多个视频，请使用只有一个视频的链接或在批量下载页面进行下载")
        #cid用来获取弹幕文件
        p = int(match1(self.url, r'[\?&]p=(\d+)') or match1(self.url, r'/index_(\d+)') or '1')
        cid = self.initial_state['videoData']['pages'][p - 1]['cid']
        # 请求弹幕文件并解码
        response = requests.get('http://comment.bilibili.com/%s.xml' % cid,headers=self.bilibili_headers())
        self.danmaku = response.content.decode()
        
    def startToDownLoad(self,stream_id,output_dir,title):
        #开始下载
        self.title = title
        #这里解析当前传入的清晰度选项
        qualityIDs = []
        for i in self.playinfo['data']['accept_quality']:
            if i in (116,80,74,64,48,32,16):#我们只对stream_types里面有的视频质量进行下载
                qualityIDs.append(i)
        for id in qualityIDs:
            if stream_id == self.stream_qualities[id]['desc']:
                self.currentQuality = id
        # 只能下载dash格式的视频
        if 'dash' in self.playinfo['data']:
            self.dash_streams = {}
            for video in self.playinfo['data']['dash']['video']:
                # 筛选出用户选择的清晰度
                if video['id'] != self.currentQuality:
                    continue
                #这是用户选择的清晰度相应的视频信息
                s = self.stream_qualities[video['id']] 
                self.format_id = 'dash-' + s['id']  # 清晰度
                self.container = 'mp4'  # 视频格式定位MP4
                self.desc = s['desc'] # 
                self.audio_quality = s['audio_quality'] # 音频质量
                self.baseurl = video['baseUrl'] # 视频下载的一次性链接
                # 获得视频的大小
                self.video_size = url_size(self.baseurl, headers=self.bilibili_headers(referer=self.url))

                # 获取对应音频质量的音频链接
                self.audio_baseurl = self.playinfo['data']['dash']['audio'][0]['baseUrl']
                for audio in self.playinfo['data']['dash']['audio']:
                    if int(audio['id']) == self.audio_quality:
                        self.audio_baseurl = audio['baseUrl']
                        break
                #　音频的大小
                self.audio_size = url_size(self.audio_baseurl, headers=self.bilibili_headers(referer=self.url))
                # 音视频总大小
                self.total_size = int(self.video_size)+int(self.audio_size)
                #我们需要下载的视频清晰度、格式、视频链接和音频链接和总大小都在这里
                self.dash_streams[self.format_id] = {'container': self.container, 'quality': self.desc,
                                                'src': [[self.baseurl], [self.audio_baseurl]], 'size': self.total_size}
                urls = self.dash_streams[self.format_id]['src']
                ext = self.dash_streams[self.format_id]['container']
                total_size = self.dash_streams[self.format_id]['size']
                self.received = 0
                # 以二进制形式将音视频写到文件中
                open_mode = "wb"
                
                #用来请求视频和音频的header
                temp_header = self.bilibili_headers(referer = self.url)
                parts = []
                self.processsignal.TotalSize(total_size)
                
                # 下载音频和视频，一次循环下载视频，一次循环下载音频
                for i,url in enumerate(urls):
                    filename = '%s[%02d].%s' % (self.title, i, ext)
                    filepath = os.path.join(output_dir, filename)
                    parts.append(filepath)
                    url = url[0]
                    received_chunk = 0
                    #分段请求视频或音频
                    temp_header['Range'] = 'bytes=' + str(received_chunk) + '-'
                    temp_filepath = filename+".download" 
                    response = urlopen_with_retry(
                        request.Request(url, headers=temp_header)
                    )
                    content_length = response.headers['content-length']
                    range_length = int(content_length) if content_length is not None \
                        else float('inf')
                    with open(temp_filepath,open_mode) as output:
                        while True:
                            buffer = None
                            try:
                                # 每次请求255字节数据
                                buffer = response.read(1024 * 256)
                            except socket.timeout:
                                pass
                            if not buffer:
                                if received_chunk == range_length:
                                    break
                                elif self.received == total_size:  # Download finished
                                    break
                            #　写入文件
                            output.write(buffer)
                            received_chunk += len(buffer)
                            self.received += len(buffer)
                            self.percent = round(self.received * 100 / self.total_size  ,1)
                            # 更新进度条
                            self.processsignal.update(self.percent)
                    os.rename(temp_filepath, filepath)
                #　完成下载，开始合成
                self.processsignal.merge()
                output_filepath = os.path.join(output_dir, self.title+".mp4")
                audioclip = AudioFileClip(parts[1])
                videoclip = VideoFileClip(parts[0])
                videoclip = videoclip.set_audio(audioclip)
                videoclip.write_videofile(output_filepath)
                self.processsignal.close_message()
                #　弹幕提取，制作词云图
                pattern = r'\"\>(.*?)\<\/d\>'
                match = re.findall(pattern, self.danmaku)
                text = ""
                for string in match:
                    text += (string+" ")
                from wordcloud import WordCloud
                if len(text) > 0:
                    wordcloud = WordCloud(background_color="white",width=1000, height=860, margin=2).generate(text)
                wordcloud.to_file(os.path.join(output_dir, self.title+".png"))
                #　删掉原来下载的音视频文件，因为我们已将他们合成导出了
                os.remove(parts[0])
                os.remove(parts[1])
                break
        else:
            # TODO 其他类型格式视频的下载
            raise VideoFormatError("无法下载链接的视频，格式暂时不支持")
           

if __name__=='__main__':
    test = DownLoader("https://www.bilibili.com/video/av48201613")
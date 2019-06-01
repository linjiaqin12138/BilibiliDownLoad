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
    title = pyqtSignal(str)
    def updatetitle(self,title):
        self.title.emit(title)
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
    if headers:
        response = urlopen_with_retry(request.Request(url, headers=headers))
    else:
        response = urlopen_with_retry(url)

    size = response.headers['content-length']
    return int(size) if size is not None else float('inf')

class DownLoader(object):
    pn = 0
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
        self.url = url.rstrip(' ').rstrip('/')
    @staticmethod
    def height_to_quality(height):
        if height <= 360:
            return 16
        elif height <= 480:
            return 32
        elif height <= 720:
            return 64
        else:
            return 80
    @staticmethod
    def bilibili_bangumi_api(avid, cid, ep_id, qn=0):
        return 'https://api.bilibili.com/pgc/player/web/playurl?avid=%s&cid=%s&qn=%s&type=&otype=json&ep_id=%s&fnver=0&fnval=16' % (avid, cid, qn, ep_id)
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
    # 解析链接，获得视频数量、视频标题、视频清晰度、弹幕文件链接，page是软件页面
    def prepare(self,page):
        # 解析视频链接信息的函数
        self.stream_qualities = {s['quality']: s for s in self.stream_types}
        #获得html源代码
        html_content = self.get_content(self.url, headers=self.bilibili_headers())
        #视频信息获取，视频信息就藏在html的<script>标签内的一个json对象里面
        if re.match(r'https?://(www\.)?bilibili\.com/bangumi/play/ep(\d+)', self.url):
            self.sort = 'bangumi'
        elif re.match(r'https?://(www\.)?bilibili\.com/video/av(\d+)', self.url):
            self.sort = 'video'
        if self.sort == 'video':
            initial_state_text = match1(html_content,r'__INITIAL_STATE__=(.*?);\(function\(\)')  
            self.initial_state = json.loads(initial_state_text)
            playinfo_text = match1(html_content, r'__playinfo__=(.*?)</script><script>')  
            self.playinfo = json.loads(playinfo_text) if playinfo_text else None
            #视频数目，必须为1否则不能下载，要改用批量下载功能去下载
            self.pn = self.initial_state['videoData']['videos']
            # TODO 设置界面的提醒视频数目
            self.title =  self.initial_state['videoData']['title']
            #当前视频质量编号 整数
            self.currentQuality = self.playinfo['data']['quality']
            #可选视频质量列表
            self.qualityIDs = []
            for i in self.playinfo['data']['accept_quality']:
                if i in (116,80,74,64,48,32,16):#我们只对stream_types里面有的视频质量进行下载
                    self.qualityIDs.append(i)
            #可选的视频质量列表
            self.acceptQualitys = [self.stream_qualities[id]['desc'] for id in self.qualityIDs]
            # p是第p个视频
            p = int(match1(self.url, r'[\?&]p=(\d+)') or match1(self.url, r'/index_(\d+)') or '1')
            cid = self.initial_state['videoData']['pages'][p - 1]['cid']
        elif self.sort=='bangumi':
            initial_state_text = match1(html_content,r'__INITIAL_STATE__=(.*?);\(function\(\)')  
            self.initial_state = json.loads(initial_state_text)
            self.pn = len(self.initial_state['epList'])
            self.title = self.initial_state['h1Title']

            ep_id = self.initial_state['epInfo']['id']
            avid = self.initial_state['epInfo']['aid']
            # cid用来获取弹幕文件
            cid = self.initial_state['epInfo']['cid']
            self.playinfos = []
            api_url = self.bilibili_bangumi_api(avid,cid,ep_id)
            api_content = self.get_content(api_url, headers=self.bilibili_headers())
            api_playinfo = json.loads(api_content)
            if api_playinfo['code'] == 0:  # success
                self.playinfos.append(api_playinfo)
            else:
                raise MultiplePageError("解析失败")
            #api_playinfo['result']['accept_description']
            self.currentQuality = api_playinfo['result']['quality']
            #self.acceptQualitys = api_playinfo['result']['accept_quality']
            self.qualityIDs = []
            for i in api_playinfo['result']['accept_quality']:
                if i in (116,80,74,64,48,32,16):#我们只对stream_types里面有的视频质量进行下载
                    self.qualityIDs.append(i)
            #可选的视频质量列表
            self.acceptQualitys = [self.stream_qualities[id]['desc'] for id in self.qualityIDs]
            for qn in [80, 64, 32, 16]:
                # automatic format for durl: qn=0
                # for dash, qn does not matter
                if qn != self.currentQuality:
                    api_url = self.bilibili_bangumi_api(avid, cid, ep_id, qn=qn)
                    api_content = self.get_content(api_url, headers=self.bilibili_headers())
                    api_playinfo = json.loads(api_content)
                    if api_playinfo['code'] == 0:  # success
                        self.playinfos.append(api_playinfo)

        if self.pn > 1:
            if page==1 and not(match1(self.url, r'[\?&]p=(\d+)') or match1(self.url, r'/index_(\d+)')):
                raise MultiplePageError("链接中包含多个视频，请使用只有一个视频的链接或在批量下载页面进行下载")
            else:
                pass
        elif self.pn == 1:
            if page == 2:
                raise MultiplePageError("使用下载单个视频下载")
            else:
                pass    
        # 请求弹幕文件并解码
        response = requests.get('http://comment.bilibili.com/%s.xml' % cid,headers=self.bilibili_headers())
        self.danmaku=response.content.decode()
    def get_pageN(self):
        return self.pn
    # 批量下载的视频名称
    def get_titles(self):
        if self.pn<=1:
            raise Exception("请用批量下载")
        titles = []
        if self.sort == 'video':
            for i in range(self.pn):
                titles.append(self.initial_state['videoData']['pages'][i]['part'])
        else:
            for i in range(self.pn):
                titles.append(self.initial_state['epList'][i]['titleFormat']+" "+self.initial_state['epList'][i]['longTitle'])
        return titles
    def DownLoaddanmaku(self,output_dir,title = ""):
        #　弹幕提取，制作词云图
        pattern = r'\"\>(.*?)\<\/d\>'
        match = re.findall(pattern, self.danmaku)
        text = ""
        for string in match:
            text += (string+" ")
        from wordcloud import WordCloud
        if len(text) > 0:
            wordcloud = WordCloud(background_color="white",width=1000, height=860, margin=2).generate(text)
            wordcloud.to_file(os.path.join(output_dir, title+".png"))
    def DataRetrive(self,streamsDict,format_id,output_dir,title,isDash = False):
        urls = streamsDict[format_id]['src']
        ext = streamsDict[format_id]['container']
        total_size = streamsDict[format_id]['size']
        self.received = 0
        # 以二进制形式将音视频写到文件中
        open_mode = "wb"
        temp_header = self.bilibili_headers(referer = self.url)
        # 下载的片段名称
        parts = []
        for i,url in enumerate(urls):
            filename = '%s[%02d].%s' % (title, i, ext)
            filepath = os.path.join(output_dir, filename)
            parts.append(filepath)
            if isDash:
                url = url[0]
            received_chunk = 0
            #分段请求视频或音频
            temp_header['Range'] = 'bytes=' + str(received_chunk) + '-'
            temp_filepath = output_dir+filename+".download" 
            response = urlopen_with_retry(
                request.Request(url, headers=temp_header)
            )
            content_length = response.headers['content-length']
            range_length = int(content_length) if content_length is not None \
                else float('inf')
            # durl 用来合并的列表
            video_parts = []
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
                        else:
                            temp_header['Range'] = 'bytes='+str(received_chunk)+'-'
                            response = urlopen_with_retry(
                                request.Request(url, headers=temp_header)
                            )
                            continue
                    #　写入文件
                    output.write(buffer)
                    received_chunk += len(buffer)
                    self.received += len(buffer)
                    self.percent = round(self.received * 100 / total_size ,1)
                    # 更新进度条
                    self.processsignal.update(self.percent)
            os.rename(temp_filepath, filepath)
            if not isDash:
                videoclip = VideoFileClip(parts[i])
                video_parts.append(videoclip)
        self.processsignal.merge()
        if isDash:
            output_filepath = os.path.join(output_dir, title+".mp4")
            audioclip = AudioFileClip(parts[1])
            videoclip = VideoFileClip(parts[0])
            videoclip = videoclip.set_audio(audioclip)
            videoclip.write_videofile(output_filepath)
            audioclip.close()
            videoclip.close()
            self.processsignal.close_message()
            self.DownLoaddanmaku(output_dir,title)
            #　删掉原来下载的音视频文件，因为我们已将他们合成导出了
            os.remove(parts[0])
            os.remove(parts[1])
        else:
            final_clip = concatenate_videoclips(video_parts)
            final_clip.to_videofile(os.path.join(output_dir,title+".mp4"))
            for eachvideo in video_parts:
                eachvideo.close()
            final_clip.close()
            self.processsignal.close_message()
            self.DownLoaddanmaku(output_dir,title)
            #　删掉原来下载的音视频文件，因为我们已将他们合成导出了
            for i in range(len(parts)):
                os.remove(parts[i])
            

    def RetriveDashData(self,output_dir,title):
        self.dash_streams = {}
        # 循环找出清晰度
        for video in self.playinfo['data']['dash']['video']:
            # 筛选出用户选择的清晰度
            if video['id'] != self.currentQuality:
                continue
            else:
                break
        s = self.stream_qualities[video['id']] 
        format_id = 'dash-' + s['id']  # 清晰度
        container = 'mp4'  # 视频格式定位MP4
        desc = s['desc'] # 
        audio_quality = s['audio_quality'] # 音频质量
        baseurl = video['baseUrl'] # 视频下载的一次性链接
        # 获得视频的大小
        video_size = url_size(baseurl, headers=self.bilibili_headers(referer=self.url))
        # 获取对应音频质量的音频链接
        audio_baseurl = self.playinfo['data']['dash']['audio'][0]['baseUrl']
        for audio in self.playinfo['data']['dash']['audio']:
            if int(audio['id']) == audio_quality:
                audio_baseurl = audio['baseUrl']
                break
        #　音频的大小
        audio_size = url_size(audio_baseurl, headers=self.bilibili_headers(referer=self.url))
        # 音视频总大小
        total_size = int(video_size)+int(audio_size)
        #我们需要下载的视频清晰度、格式、视频链接和音频链接和总大小都在这里
        self.dash_streams[format_id] = {'container': container, 'quality': desc,
                                        'src': [[baseurl], [audio_baseurl]], 'size': total_size}
        self.DataRetrive(self.dash_streams,format_id,output_dir,title,True)
        
    def RetriveDurlData(self,output_dir,title):
        self.streams = {}
        src,total_size = [],0
        format_id = self.stream_qualities[self.currentQuality]['id']
        container = self.stream_qualities[self.currentQuality]['container'].lower()
        desc = self.stream_qualities[self.currentQuality]['desc']
        for durl in self.playinfo['data']['durl']:
            src.append(durl['url'])
            total_size += durl['size']
        self.streams[format_id] = {'container':container,'quality':desc,'size':total_size,'src':src}
        self.DataRetrive(self.streams,format_id,output_dir,title,False)
        
    
    def StartToDOwnLoadMore(self,stream_id,output_dir,videoIndexAndtitleList,optionHigh=False):
        # 一条条视频链接进行解析，先清空前面保留的弹幕
        #self.danmaku.clear()
        #https://www.bilibili.com/video/av19397094/?p=2
        if self.sort == 'video':
            aid = self.initial_state['videoData']['aid']
            for idx,title in videoIndexAndtitleList:
                purl = 'https://www.bilibili.com/video/av%s?p=%s' % (aid, idx+1)
                self.url = purl
                self.prepare(2)
                self.processsignal.updatetitle(title)
                self.startToDownLoadOne(stream_id,output_dir,title,optionHigh)
        else:
            for idx,title in videoIndexAndtitleList:
                ep_id = self.initial_state['epList'][idx]['id']
                epurl = 'https://www.bilibili.com/bangumi/play/ep%s/' % ep_id
                self.url = epurl
                self.prepare(2)
                self.processsignal.updatetitle(title)
                self.startToDownLoadOneBangumi(stream_id,output_dir,title,optionHigh)
                
    def startToDownLoadOne(self,stream_id,output_dir,title,optionHigh = False):
        if self.sort == 'video':
            self.startToDownLoadOneVideo(stream_id,output_dir,title,optionHigh = False)
        elif self.sort == 'bangumi':
            self.startToDownLoadOneBangumi(stream_id,output_dir,title,optionHigh = False)
    def startToDownLoadOneBangumi(self,stream_id,output_dir,title,optionHigh = False):
        #这里解析当前传入的清晰度选项
        stream_id_exist = False
        for id in self.qualityIDs:
            if stream_id == self.stream_qualities[id]['desc']:
                stream_id_exist = True
                self.currentQuality = id
        if not stream_id_exist:
            if not optionHigh:
                minid = 116
                for id in qualityIDs:
                    if id<minid:
                        minid = id
                self.currentQuality = minid
            else:
                maxid = 0
                for id in qualityIDs:
                    if id>maxid:
                        maxid = id
                self.currentQuality = maxid
        self.streams = {}
        self.dash_streams = {}
        for playinfo in self.playinfos:
            if 'durl' in playinfo['result']:
                quality = playinfo['result']['quality']
                format_id = self.stream_qualities[quality]['id']
                container = self.stream_qualities[quality]['container'].lower()
                desc = self.stream_qualities[quality]['desc']
                src,size = [],0
                for durl in playinfo['result']['durl']:
                    src.append(durl['durl'])
                    size+=durl['size']
                self.streams[format_id] = {'container':container,'quality':desc,'size':size,'src':src}
            if 'dash' in playinfo['result']:
                for video in playinfo['result']['dash']['video']:
                    quality =  self.height_to_quality(video['height'])
                    s = self.stream_qualities[quality]
                    format_id = 'dash-' + s['id'] 
                    container = 'mp4'
                    desc = s['desc']
                    audio_quality = s['audio_quality']
                    baseurl = video['baseUrl']
                    size = url_size(baseurl,headers=self.bilibili_headers(referer = self.url))

                    audio_baseurl = playinfo['result']['dash']['audio'][0]['baseUrl']
                    for audio in playinfo['result']['dash']['audio']:
                        if int(audio['id'])==audio_quality:
                            audio_baseurl = audio['baseUrl']
                    size += url_size(audio_baseurl,headers=self.bilibili_headers(referer=self.url))
                    self.dash_streams[format_id] = {'container':container,'quality':desc,'src':[[baseurl],[audio_baseurl]],'size':size}
        if self.streams:
            format_id = self.stream_qualities[self.currentQuality]['id']
            self.DataRetrive(self.streams,format_id,output_dir,title,False)
        else:
            format_id = 'dash-'+self.stream_qualities[self.currentQuality]['id']
            self.DataRetrive(self.dash_streams,format_id,output_dir,title,True)

            
    def startToDownLoadOneVideo(self,stream_id,output_dir,title,optionHigh = False):
        #这里解析当前传入的清晰度选项
        stream_id_exist = False
        for id in self.qualityIDs:
            if stream_id == self.stream_qualities[id]['desc']:
                stream_id_exist = True
                self.currentQuality = id
        if not stream_id_exist:
            if not optionHigh:
                minid = 116
                for id in qualityIDs:
                    if id<minid:
                        minid = id
                self.currentQuality = minid
            else:
                maxid = 0
                for id in qualityIDs:
                    if id>maxid:
                        maxid = id
                self.currentQuality = maxid
        if 'durl' in self.playinfo['data']:
            self.RetriveDurlData(output_dir,title)
        if 'dash' in self.playinfo['data']:
            self.RetriveDashData(output_dir,title)
            

           

if __name__=='__main__':
    test = DownLoader("https://www.bilibili.com/video/av48201613")
    test = DownLoader("")

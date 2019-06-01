import requests
import json
import logging
import re
from moviepy.editor import *
from urllib import request,error

def bilibili_headers(referer=None, cookie=None):
    # 请求消息的头部，模拟浏览器的行为访问Bilibili网站，否则访问会被拒绝
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    headers = {'User-Agent': ua}
    if referer is not None:
        headers.update({'Referer': referer})
    if cookie is not None:
        headers.update({'Cookie': cookie})
    return headers

def height_to_quality(height):
    if height <= 360:
        return 16
    elif height <= 480:
        return 32
    elif height <= 720:
        return 64
    else:
        return 80
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
def bilibili_bangumi_api(avid, cid, ep_id, qn=0):
    return 'https://api.bilibili.com/pgc/player/web/playurl?avid=%s&cid=%s&qn=%s&type=&otype=json&ep_id=%s&fnver=0&fnval=16' % (avid, cid, qn, ep_id)
def url_size(url, faker=False, headers={}):
    if headers:
        response = urlopen_with_retry(request.Request(url, headers=headers))
    else:
        response = urlopen_with_retry(url)

    size = response.headers['content-length']
    return int(size) if size is not None else float('inf')

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
stream_qualities = {s['quality']: s for s in stream_types}
url = "https://www.bilibili.com/bangumi/play/ep250634"
html_content = get_content(url, headers=bilibili_headers())
initial_state_text = match1(html_content,r'__INITIAL_STATE__=(.*?);\(function\(\)')  
initial_state = json.loads(initial_state_text)
epn = len(initial_state['epList'])
title = initial_state['h1Title']
ep_id = initial_state['epInfo']['id']
avid = initial_state['epInfo']['aid']
cid = initial_state['epInfo']['cid']
playinfos = []
api_url = bilibili_bangumi_api(avid,cid,ep_id)
api_content = get_content(api_url, headers=bilibili_headers())
api_playinfo = json.loads(api_content)
if api_playinfo['code'] == 0:  # success
    playinfos.append(api_playinfo)
#api_playinfo['result']['accept_description']
current_quality = api_playinfo['result']['quality']
for qn in [80, 64, 32, 16]:
    # automatic format for durl: qn=0
    # for dash, qn does not matter
    if qn != current_quality:
        api_url = bilibili_bangumi_api(avid, cid, ep_id, qn=qn)
        api_content = get_content(api_url, headers=bilibili_headers())
        api_playinfo = json.loads(api_content)
        if api_playinfo['code'] == 0:  # success
            playinfos.append(api_playinfo)
streams = {}
dash_streams = {}
for playinfo in playinfos:
    if 'durl' in playinfo['result']:
        quality = playinfo['result']['quality']
        format_id = stream_qualities[quality]['id']
        container = stream_qualities[quality]['container'].lower()
        desc = stream_qualities[quality]['desc']

        src,size = [],0
        for durl in playinfo['result']['durl']:
            src.append(durl['durl'])
            size+=durl['size']
        streams[format_id] = {'container':container,'quality':desc,'size':size,'src':src}
    if 'dash' in playinfo['result']:
        for video in playinfo['result']['dash']['video']:
            quality =  height_to_quality(video['height'])
            s = stream_qualities[quality]
            format_id = 'dash-' + s['id'] 
            container = 'mp4'
            desc = s['desc']
            audio_quality = s['audio_quality']
            baseurl = video['baseUrl']
            size = url_size(baseurl,headers=bilibili_headers(referer = url))

            audio_baseurl = playinfo['result']['dash']['audio'][0]['baseUrl']
            for audio in playinfo['result']['dash']['audio']:
                if int(audio['id'])==audio_quality:
                    audio_baseurl = audio['baseUrl']
            size += url_size(audio_baseurl,headers=bilibili_headers(referer=url))
            dash_streams[format_id] = {'container':container,'quality':desc,'src':[[baseurl],[audio_baseurl]],'size':size}
dammaku = get_content('http://comment.bilibili.com/%s.xml' % cid)
dash_streams
    

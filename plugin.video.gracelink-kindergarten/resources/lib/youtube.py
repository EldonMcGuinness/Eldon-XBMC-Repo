import urllib2, json

class playlistBuilder:
    API_URL = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={PLAYLIST_ID}&key={API_KEY}'
    API_KEY = 'AIzaSyCFkn14sfQE6HWDWvIhPe5WsOks-flwX08'
    url = API_URL
    items = []

    def __init__(self, playlistId):
        # PLkFyfqehc4MqiOLhHl-TBY2Insri9KsrX
        self.url = self.url.replace('{PLAYLIST_ID}',playlistId).replace('{API_KEY}',self.API_KEY)
        self.populateItems()

    def populateItems(self):
        #print('Fetching URL [{0}]'.format(self.url))
        playlist = json.loads(urllib2.urlopen(self.url).read().decode('utf8'))
        for item in playlist['items']:
            self.items.append({
                'title':item['snippet']['title'],
                'description':item['snippet']['description'],
                'img':item['snippet']['thumbnails']['default']['url'],
                'videoId':item['snippet']['resourceId']['videoId']
            })

class videoFinder:
    baseUrl = 'http://www.youtube.com/get_video_info?video_id='
    videoId = None
    videos = []
    parameters = None

    def __init__(self, videoId):
        self.videos = []
        self.parameters = None
        self.videoId = videoId
        self.getPage(videoId)

    def getPage(self, videoId):
        #print 'Getting Page: {0}'.format(videoId)
        #print 'URL: {0}'.format(self.baseUrl+videoId)
        request = urllib2.Request(self.baseUrl+videoId)
        request.add_header('Prama','no-cache')
        request.add_header('User-Agent', 'Mozilla/5.0')
        result = urllib2.build_opener().open(request)
        raw = result.read()
        self.parameters = self.videoInfoDecode(raw)
        img = 'http://i.ytimg.com/vi/{0}/mqdefault.jpg'.format(videoId)
        for video in self.parameters['url_encoded_fmt_stream_map']:
            self.videos.append({'quality':video['quality'],'url':video['url'],'img':img})

    def __urlDecode(self, p):
        return urllib2.unquote(p).decode('utf8')

    def __querystringDecode(self, p):
        parsedData = None
        videoObject = {}

        parsedData = p.split('&')

        for data in parsedData:
            key = data.split('=')[0]
            val = self.__urlDecode(data.split('=')[1])
            videoObject[key] = val        

        return videoObject

    def videoInfoDecode(self, raw):
        parsedData = None
        videoObject = self.__querystringDecode(raw)
        validVideos = []

        videoObject['url_encoded_fmt_stream_map'] = videoObject['url_encoded_fmt_stream_map'].split(',')
        videoObject['url_encoded_fmt_stream_map'] = map(self.__querystringDecode,videoObject['url_encoded_fmt_stream_map'])
        
        #Get rid of non-mp4 videos
        for video in videoObject['url_encoded_fmt_stream_map']:
            if 'mp4' in video['type']:
                validVideos.append(video)

        videoObject['url_encoded_fmt_stream_map'] = validVideos

        return videoObject

    def getBestQuality(self):
        rank = {'hd720':2, 'medium':1, 'small':0 } 
        currentBest = None
        for video in self.videos:
            if currentBest is None:
                currentBest = video
            else:
                if rank[currentBest['quality']] < rank[video['quality']]:
                    currentBest = video 

        return currentBest


#if (__name__ == "__main__"):
    '''
    print('Addon Started')
    loader = videoFinder('JOPmoY9Ec18');
    best = loader.getBestQuality()
    print 'Best Quality Found: {0} {1}'.format(best['quality'],best['url']);
    '''
    '''
    playlist = playlistBuilder('PLkFyfqehc4MqiOLhHl-TBY2Insri9KsrX');
    print str(playlist.items)
    '''

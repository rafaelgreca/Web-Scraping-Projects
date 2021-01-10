import requests
import json

class Streams:
    url_auth = 'https://id.twitch.tv/oauth2/token'
    
    def __init__(self, client_secret, client_id):
        self.client_secret = client_secret
        self.client_id = client_id
        self.grant_type = 'client_credentials'
        self.access_token = ''
        self.headers = ''

    def getCredentials(self):

        credentials = {
            'client_secret': self.client_secret,
            'client_id': self.client_id,
            'grant_type': self.grant_type
        }

        auth = requests.post(self.url_auth, data=credentials)
        self.access_token = auth.json()['access_token']
        self.headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'client-id': self.client_id,
            'Accept': 'application/vnd.twitchtv.v5+json'
        }

    def getLiveStreams(self, game=None, language=None, offset=None, limit=None, stream_type=None):
        
        if self.access_token == '':
            self.getCredentials()

        params = {
            #'channel': ['108268890'],
            'game': '' or game,
            'language': '' or language,
            'stream_type': 'live' or stream_type,
            'limit': 25 or limit,
            'offset': 0 or offset
        }

        url = 'https://api.twitch.tv/kraken/streams/'

        request = requests.get(url, headers=self.headers, params=params)

        if request.status_code == 200:        
            self.saveJson('LiveStreams.json', request.json())
        else:
            print(request.json())
        
    def getStreamsSummary(self, game=None):
        
        if self.access_token == '':
            self.getCredentials()

        url = 'https://api.twitch.tv/kraken/streams/summary'

        params = {
            'game': '' or game
        }

        request = requests.get(url, headers=self.headers, params=params)

        if request.status_code == 200:
            self.saveJson('StreamsSummary.json', request.json())
        else:
            print(request.json())

    def getFeaturedStreams(self, limit=None, offset=None):
        
        if self.access_token == '':
            self.getCredentials()

        url = 'https://api.twitch.tv/kraken/streams/featured'

        params = {
            'limit': 25 or limit,
            'offset': 0 or offset
        }

        request = requests.get(url, headers=self.headers, params=params)

        if request.status_code == 200:
            self.saveJson('FeaturedStreams.json', request.json())
        else:
            print(request.json())

    def getStreamByUserID(self, user, stream_type=None):

        if self.access_token == '':
            self.getCredentials()

        url = 'https://api.twitch.tv/kraken/streams/' + str(user)

        params = {
            'stream_type': 'live' or stream_type
        }

        request = requests.get(url, headers=self.headers, params=params)

        if request.status_code == 200:
            self.saveJson('StreamByUserID.json', request.json())
        else:
            print(request.json())

    def saveJson(self, name, json_file):

        with open(name, 'w', encoding='utf-8') as f:
            json.dump(json_file, f, ensure_ascii=True, indent=4)

if __name__ == "__main__":

    streams = Streams(client_secret='', client_id='')

    #streams.getLiveStreams(game='Dota 2', language='en')
    #streams.getStreamsSummary()
    #streams.getFeaturedStreams()
    #streams.getStreamByUserID(user='23220337')
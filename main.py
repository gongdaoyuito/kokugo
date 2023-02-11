from PIL import Image,ImageFont,ImageDraw
import textwrap
import random

image_path = "素材.jpeg" # 文字を重ねる画像
out_path = 'output.jpg' # 出力先

font_path = "Aiharahudemojikaisho_free305.ttf"
font_size = 60
font_color = (51,54,49) #文字の色
num = random.randint(0, 243)
text = ' 徒然草 第{}段原文'.format(str(num).zfill(3))
text = textwrap.fill(text=text, width=5)

font = ImageFont.truetype(font_path, font_size)

image = Image.open(image_path)
draw = ImageDraw.Draw(image)

width, height = image.size
draw.multiline_text((width / 2, height / 2), text, font=font, fill=font_color, anchor="mm", align="center")
image.save(out_path)

out_path2 = 'output2.jpg' # 出力先

text = ' 徒然草 第{}段口語訳'.format(str(num).zfill(3))
text = textwrap.fill(text=text, width=5)

font = ImageFont.truetype(font_path, font_size)

image = Image.open(image_path)
draw = ImageDraw.Draw(image)

width, height = image.size
draw.multiline_text((width / 2, height / 2), text, font=font, fill=font_color, anchor="mm", align="center")
image.save(out_path2)

import requests
import json
import datetime
from pprint import pprint

def basic_info():
    # 初期
    config = dict()
    # 【要修正】アクセストークン
    config["access_token"]         = 'EAARUVzKkZCGkBANLW2X8YVhMDj9rNVQAq7uZCGd3r0OviJd9Hli2bVjqQ6QfIUVV1l58zZCR7uPla0QZC81ZCK7u4rZCqekSDJWOhZA6dlfHLSBH2jyqHFZBv2tdYJ8dtKHHSf6HZC71LSOrimNFgZAJmgzszHFPiVn1DfDYin4Pb57ZCy8dLgnIVvI'
    # 【要修正】アプリID
    config["app_id"]               = '1218633395403881'
    # 【要修正】アプリシークレット
    config["app_secret"]           = '9939a04d8a4d726c4e4246b65a2b2'
    # 【要修正】インスタグラムビジネスアカウントID
    config['instagram_account_id'] = "17841457779061851"
    # 【要修正】グラフバージョン
    config["version"]              = 'v16.0'
    # 【修正不要】graphドメイン
    config["graph_domain"]         = 'https://graph.facebook.com/'
    # 【修正不要】エンドポイント
    config["endpoint_base"]        = config["graph_domain"]+config["version"] + '/'
    # 出力
    return config

import requests
import json
import datetime
from pprint import pprint

# APIリクエスト用の関数
def InstaApiCall(url, params, request_type):
    
    # リクエスト
    if request_type == 'POST' :
        # POST
        req = requests.post(url,params)
    else :
        # GET
        req = requests.get(url,params)
    
    # レスポンス
    res = dict()
    res["url"] = url
    res["endpoint_params"]        = params
    res["endpoint_params_pretty"] = json.dumps(params, indent=4)
    res["json_data"]              = json.loads(req.content)
    res["json_data_pretty"]       = json.dumps(res["json_data"], indent=4)
    
    # 出力
    return res

def debugAT(params):
    # エンドポイントに送付するパラメータ
    Params = dict()
    Params["input_token"]  = params["access_token"]
    Params["access_token"] = params["access_token"]
    # エンドポイントURL
    url = params["graph_domain"] + "/debug_token"
    # 戻り値
    return InstaApiCall(url, Params, 'GET')


# リクエスト
params   = basic_info()       # リクエストパラメータ
response = debugAT(params)    # レスポンス

# レスポンス
pprint(response)

import time

# メディア作成
def createMedia(params) :
    """
    ******************************************************************************************************
    【画像・動画コンテンツ作成】
    https://graph.facebook.com/v5.0/{ig-user-id}/media?image_url={image-url}&caption={caption}&access_token={access-token}
    https://graph.facebook.com/v5.0/{ig-user-id}/media?video_url={video-url}&caption={caption}&access_token={access-token}
    ******************************************************************************************************
    """
    # エンドポイントURL
    url = params['endpoint_base'] + params['instagram_account_id'] + '/media'
    # エンドポイント用パラメータ
    Params = dict() 
    Params['caption'] = params['caption']           # 投稿文
    Params['access_token'] = params['access_token'] # アクセストークン
    # メディアの区分け
    if 'IMAGE' == params['media_type'] :
        # 画像：メディアURLを画像URLに指定
        Params['image_url'] = params['media_url']    # 画像URL
    else :
        # 動画：メディアURLを動画URLに指定
        Params['media_type'] = params['media_type']  # メディアタイプ
        Params['video_url']  = params['media_url']   # ビデオURL
    # 出力
    return InstaApiCall(url, Params, 'POST')


# メディアID別ステータス管理
def getMediaStatus(mediaObjectId, params) :
    """
    ******************************************************************************************************
    【APIエンドポイント】
    https://graph.facebook.com/v5.0/{ig-container-id}?fields=status_code
    ******************************************************************************************************
    """
    # エンドポイントURL
    url = params['endpoint_base'] + '/' + mediaObjectId
    # パラメータ
    Params = dict()
    Params['fields']       = 'status_code'          # フィールド
    Params['access_token'] = params['access_token'] # アクセストークン
    # 出力
    return InstaApiCall(url, Params, 'GET')

# メディア投稿
def publishMedia(mediaObjectId, params):
    """
    ******************************************************************************************************
    【APIエンドポイント】
    https://graph.facebook.com/v5.0/{ig-user-id}/media_publish?creation_id={creation-id}&access_token={access-token}
    ******************************************************************************************************
    """
    # エンドポイントURL
    url = params['endpoint_base'] + params['instagram_account_id'] + '/media_publish'
    # エンドポイント送付用パラメータ
    Params = dict()
    Params['creation_id'] = mediaObjectId           # メディアID
    Params['access_token'] = params['access_token'] # アクセストークン
    # 出力
    return InstaApiCall(url, Params, 'POST')

# ユーザの公開レート制限・使用率を取得
def getContentPublishingLimit( params ) :
    """ 
    ******************************************************************************************************
    https://graph.facebook.com/v5.0/{ig-user-id}/content_publishing_limit?fields=config,quota_usage
    ******************************************************************************************************
    """
    # エンドポイントURL
    url = params['endpoint_base'] + params['instagram_account_id'] + '/content_publishing_limit' # endpoint url
    # エンドポイント送付用のパラメータ
    Params = dict() 
    Params['fields'] = 'config,quota_usage'         # フィールド
    Params['access_token'] = params['access_token'] # アクセストークン

    return InstaApiCall(url, Params, 'GET')

# 画像投稿
def instagram_upload_image(media_url, media_caption):
    # パラメータ
    params = basic_info()
    params['media_type'] = 'IMAGE'         # メディアType
    params['media_url']  =  media_url      # メディアURL
    params['caption']    = media_caption
    
    
    # APIでメディア作成＆ID発行
    imageMediaId = createMedia(params)['json_data']['id']
    
    # メディアアップロード
    StatusCode = 'IN_PROGRESS';
    while StatusCode != 'FINISHED':
        # メディアステータス取得
        StatusCode = getMediaStatus(imageMediaId,params)['json_data']['status_code']
        # 待ち時間
        time.sleep(5)

    # Instagramにメディア公開 
    publishImageResponse = publishMedia(imageMediaId,params)
    # 出力
    print("Instagram投稿完了")
    return publishImageResponse['json_data_pretty']

# coding=utf-8
import dropbox

dbx = dropbox.Dropbox('sl.BYl__dQ4VAFMkL7YY8MSPsLaQtC0Bjs3N5k1T4yPBgYAEAXh98nWXPyVuwSxZfYkGCJG_bIc03TKgu0hBdixk817xqxjuCV62NQA22awoZBcL6dq2h1wRxN7NwKKB8ua2qRznRhaWpaT')

local_path = 'output.jpg'
local_path2 = 'output2.jpg'
path = '/image/' + local_path  #dropbox直下に「images」フォルダを作成
path2 = '/image/' + local_path2  #dropbox直下に「images」フォルダを作成

try:
    dbx.files_delete(path)
    dbx.files_delete(path2)
except:
    pass

# ファイルをDropboxにアップロード
f = open(local_path, 'rb')
dbx.files_upload(f.read(),path )
f.close()
f = open(local_path2, 'rb')
dbx.files_upload(f.read(),path2 )
f.close()


setting = dropbox.sharing.SharedLinkSettings(requested_visibility=dropbox.sharing.RequestedVisibility.public)
link = dbx.sharing_create_shared_link_with_settings(path=path, settings=setting)

# 共有リンク取得
links = dbx.sharing_list_shared_links(path=path, direct_only=True).links
if links is not None:
    for link in links:
        url = link.url 
        url = url.replace('www.dropbox','dl.dropboxusercontent').replace('?dl=0','')
        print(url)

link = dbx.sharing_create_shared_link_with_settings(path=path2, settings=setting)

# 共有リンク取得
links2 = dbx.sharing_list_shared_links(path=path2, direct_only=True).links
if links2 is not None:
    for link2 in links2:
        url2 = link2.url 
        url2 = url2.replace('www.dropbox','dl.dropboxusercontent').replace('?dl=0','')
        print(url2)


filename = "k_tsurezure{}.txt".format(str(num).zfill(3))
with open(filename, encoding="utf-8") as f:
    media_caption = f.read()

print(media_caption)

#関数実行
instagram_upload_image(url, media_caption)

filename = "g_tsurezure{}.txt".format(str(num).zfill(3))
with open(filename, encoding="utf-8") as f:
    media_caption = f.read()

print(media_caption)

#関数実行
instagram_upload_image(url2, media_caption)
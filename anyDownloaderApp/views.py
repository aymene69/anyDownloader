from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import searchURL
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from pytube import YouTube
import ffmpeg
import os
import twitter_video_dl as tvdl
import instaloader
import re
def getPlatform(link):
    parsed_url = urlparse(link)
    domain = parsed_url.netloc

    if 'tiktok' in domain:
        return 'TikTok'
    elif 'twitter' in domain:
        return 'Twitter'
    elif 'x.com' in domain:
        return 'Twitter'
    elif 'instagram' in domain:
        return 'Instagram'
    elif 'youtube' in domain:
        return 'YouTube'
    elif 'youtu.be' in domain:
        return 'YouTube'
    else:
        return 'Error'

def index(request):
    if request.method == "GET":
        form = searchURL()
        return render(request, "index.html", {'form': form})
    else:
        form = searchURL(request.POST)
        if form.is_valid():
            link = form.cleaned_data['search']
            platform = getPlatform(link)
            if platform == 'TikTok':
                headers = {
                    'authority': 'ssstik.io',
                    'accept': '*/*',
                    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,nl;q=0.6',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'hx-current-url': 'https://ssstik.io/en',
                    'hx-request': 'true',
                    'hx-target': 'target',
                    'hx-trigger': '_gcaptcha_pt',
                    'origin': 'https://ssstik.io',
                    'referer': 'https://ssstik.io/en',
                    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"macOS"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                }

                params = {
                    'url': 'dl',
                }

                data = {
                    'id': link,
                    'locale': 'en',
                    'tt': 'WG05S0w0',
                    # NOTE: This value gets changed, please use the value that you get when you copy the curl command from the network console
                }

                response = requests.post('https://ssstik.io/abc', params=params, headers=headers,
                                         data=data)
                downloadSoup = BeautifulSoup(response.text, "html.parser")
                downloadLink = downloadSoup.a["href"]
                return redirect(downloadLink)
            elif platform == 'Twitter':
                tvdl.download_video_for_sc(link, "video")
                response = HttpResponse(open("medias/video.mp4", 'rb'), content_type='video/mp4')
                response['Content-Disposition'] = 'attachment; filename="video.mp4"'
                return response
            elif platform == 'Instagram':
                pattern = r'/reel/([A-Za-z0-9_-]+)/'
                corresp = re.search(pattern, link)
                code = corresp.group(1)
                L = instaloader.Instaloader()
                post = instaloader.Post.from_shortcode(L.context, code)
                video_url = post.video_url
                filename = L.format_filename(post, target=post.owner_username)
                L.download_pic(filename="medias/" + filename, url=video_url, mtime=post.date_utc)
                response = HttpResponse(open("medias/" + filename + ".mp4", 'rb'), content_type='video/mp4')
                response['Content-Disposition'] = 'attachment; filename="' + filename + '.mp4"'
                return response
            elif platform == 'YouTube':
                yt = YouTube(link)
                title = yt.title
                id = yt.video_id
                return render(request, "youtube.html", {'title': title, 'id': id})
            else:
                return HttpResponse("Error")
        else:
            return HttpResponse("Error")

def youtube_mp3(request, id):
    if request.method == "GET":
        yt = YouTube("https://www.youtube.com/watch?v=" + id)
        title = yt.title
        yt.streams.filter(only_audio=True).first().download(filename="medias/"+id + ".mp4")
        print("téléchargé")
        ffmpeg.input("medias/" + id + ".mp4").output("medias/" + title + ".mp3").run(overwrite_output=True)
        print("ffmpegé")
        os.remove("medias/" +id + ".mp4")
        return redirect('/medias/' + title + '.mp3')
    else:
        return HttpResponse("Error")

def youtube_mp4(request, id):
    if request.method == "GET":
        yt = YouTube("https://www.youtube.com/watch?v=" + id)
        title = yt.title
        yt.streams.filter(progressive=True).last().download(filename="medias/"+title + ".mp4")
        response = redirect('/medias/' + title + '.mp4')
        return response
    else:
        return HttpResponse("Error")
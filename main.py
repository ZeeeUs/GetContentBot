import requests
import random

HOST = 'https://www.instagram.com/'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
}


def build_valid_url(url):
    query_string = "__a=1"
    url = url[:url.find("?") + 1] + query_string
    return url


def get_json(url):
    r = requests.get(url, headers=HEADERS)
    new_json = r.json()
    return new_json


def get_all_url(doc):
    all_url = {}
    try:
        # Добираемся до контента
        path_to_items = doc["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]
        # path_to_items = doc["graphql"]["shortcode_media"]["displays_resources"]
        items_count = len(path_to_items)
        for i in range(items_count):
            # Проверка, явлется ли объект видео
            if path_to_items[i]["node"]["is_video"]:
                all_url[i] = {"mp4": path_to_items[i]["node"]["video_url"]}
            else:
                all_url[i] = {"jpg": path_to_items[i]["node"]["display_resources"][2]["src"]}
    except KeyError:
        path_to_items = doc["graphql"]["shortcode_media"]
        if path_to_items["is_video"]:
            all_url = {"mp4": path_to_items["video_url"]}
        else:
            all_url = {"jpg": path_to_items["display_resources"][2]["src"]}
    return all_url


def download(link):
    if "mp4" in link:
        ext = "mp4"
    elif "jpg" in link:
        ext = "jpg"
    name = f'dwnld{random.randint(1, 1000)}.{ext}'
    r = requests.get(link[ext])
    with open("./media/" + name, 'wb') as f:
        f.write(r.content)
    return name, ext


def start(user_url):
    valid_url = build_valid_url(user_url)
    doc = get_json(valid_url)
    all_url = get_all_url(doc)
    return all_url

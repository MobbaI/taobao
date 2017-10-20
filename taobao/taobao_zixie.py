import urllib.request
import urllib.error
import urllib.parse
import re
import json
import os
import time


class TAOBAOMMSpider:

    def __init__(self):
        self._http = "https:"
        self.code_type = "gbk"
        self.save_path = r'E:\PycharmProjects\taobao\img_zixie'
        # 相册id=的json
        self.js_pic_url = "https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id=1062991248&album_id="
        # 该MM的相册
        self.url = "https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id%20=1062991248"
        # 相册id正则表达式
        self.one_pattern = re.compile('<h4>.*?&album_id=(.*?)&', re.S)
        # 相册总页数正则表达式
        self.all_pattern = re.compile('<input name="totalPage" id="J_Totalpage" value="(.*?)"', re.S)

    # 相册有几页
    def get_album_page(self):
        request = urllib.request.Request(self.url)
        response = urllib.request.urlopen(request)
        result = response.read().decode(self.code_type)
        page_num = re.search(self.all_pattern, result).group(1)
        return page_num

    def get_pic_page(self, album_id):
        url = self.js_pic_url + str(album_id)
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        result = json.loads(response.read().decode(self.code_type))
        return result["totalPage"]

    def save_image(self, album_page, pic_page):
        index_pic = 1
        album_ids = self.get_album_ids(album_page)
        for album_id in album_ids:
            pic_urls = self.get_pic_urls(album_id, pic_page)
            for pic_url in pic_urls:
                # 要加https:
                response = urllib.request.urlopen(self._http + pic_url, timeout=5)
                # 以二进制打开 b
                with open(self.save_path + "//" + str(index_pic) + ".jpg", 'wb') as file:
                    file.write(response.read())
                index_pic += 1
                if index_pic % 100 == 0:
                    print("sleep 1 second")
                    time.sleep(1)
                if index_pic > 1000:
                    print("饱了...")
                    return

    def get_album_ids(self, album_page):
        url = self.url + "&page=" + str(album_page)
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        result = response.read().decode(self.code_type)
        return re.findall(self.one_pattern, result)

    def get_pic_urls(self, album_id, pic_page):
        url = self.js_pic_url + str(album_id) + "&page=" + str(pic_page)
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        result = json.loads(response.read().decode(self.code_type))
        pic_ids_small = []
        pic_ids = []
        for i in result["picList"]:
            pic_ids_small.append(i["picUrl"])
        for j in pic_ids_small:
            pic_ids.append(j.replace("290", "620"))
        return pic_ids

    def start(self):
        album_all_page = self.get_album_page()
        album_now_page = 1



if __name__ == "__main__":
    spider = TAOBAOMMSpider()
    spider.save_image(1, 1)
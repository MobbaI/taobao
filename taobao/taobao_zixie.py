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
        self.one_pattern = re.compile('<h4>.*?&album id=(.*?)&', re.S)
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

    def save_image(self):
        image_url = "https://img.alicdn.com/imgextra/i1/1062991248/TB1WSGePXXXXXaTapXXXXXXXXXX_!!" \
                    "0-tstar.jpg_620x10000.jpg"
        response = urllib.request.urlopen(image_url, timeout=5)
        # 以二进制打开 b
        with open(self.save_path + "//" + "1" + ".jpg", 'wb') as file:
            file.write(response.read())



if __name__ == "__main__":
    spider = TAOBAOMMSpider()
    a = spider.save_image()
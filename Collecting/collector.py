import requests as req
import re
from bs4 import BeautifulSoup


def edit_distance(s1, s2):
    l1, l2 = len(s1), len(s2)
    if l2 > l1:
        return edit_distance(s2, s1)
    if l2 is 0:
        return l1
    prev_row = list(range(l2 + 1))
    current_row = [0] * (l2 + 1)
    for i, c1 in enumerate(s1):
        current_row[0] = i + 1
        for j, c2 in enumerate(s2):
            d_ins = current_row[j] + 1
            d_del = prev_row[j + 1] + 1
            d_sub = prev_row[j] + (1 if c1 != c2 else 0)
            current_row[j + 1] = min(d_ins, d_del, d_sub)
        prev_row[:] = current_row[:]
    return prev_row[-1]


class lyrics(object):
    '''
        Collecting lyrics of song matched gaon chart id from other sources.
        call_stack:
            match_id -> source_parser -> get_lyrics -> lyric_parser
        methods:
            match_id:
                match id gaon to source site by comparing title
                return lyric_url
            get_lyric:
                parse lyric from source site
                return lyric
        variables:
            source:
                source is the site to get lyric
                melon, bugs, genie, Mnet Etc
    '''
    def __init__(self, source):
        self.source = source
        self.source_links = {
                    'melon': 3715,
                    'bugs': 1594,
                    'genie': 2407,
                    'mnet': 1316
                }

    def match_id(self, gaon_id, title):
        def melon_parser(soup, title):
            song_tags = list(soup.find_all('a', class_='btn btn_icon_detail'))

            for tag in song_tags:
                parsed_span = tag.find('span', class_='odd_span').text.split(" 상세정보 페이지 이동")[0]

                distance_threshold = 3
                if len(title) < distance_threshold:
                    distance_threshold = 1

                if edit_distance(parsed_span, title) < distance_threshold:
                    _song_id = re.match("javascript:melon.link.goSongDetail\('(\d+)'\);",
                    tag.attrs['href']).group(1)
                    return "http://www.melon.com/song/detail.htm?songId=%s" % str(_song_id)

        def bugs_parser(soup, title):
            song_tags = soup.select("table.list > tbody > tr")

            for tag in song_tags:
                print("_------------")
                parsed_title = tag.th.text.strip()
                lyric_info = tag.find('a', class_="trackInfo")
                #lyric_url = lyric_info['href']

                distance_threshold = 3
                if len(title) < distance_threshold:
                    distance_threshold = 1

                if edit_distance(parsed_title, title) < distance_threshold:
                    #print(parsed_title)

                    lyric_info = tag.find('a', class_="trackInfo")
                    print(title, tag.th.text.strip())
                    return lyric_info['href']

        site_id = self.source_links[self.source]
        target_url = 'http://www.gaonchart.co.kr/main/section/chart/ReturnUrl.gaon?' \
                'serviceGbn=ALL&seq_company=%d&seq_mom=%s' % (site_id, str(gaon_id))

        res = req.get(url=target_url)
        print(res.url)
        if not self.source in res.url:
            raise Exception("%s, cant find album info" % self.source)
        soup = BeautifulSoup(res.text, 'html.parser')

        parser_closers = {
                    'melon': melon_parser,
                    'bugs': bugs_parser,
                }

        lyric_url = parser_closers[self.source](soup, title)
        print(title, lyric_url, site_id)
        if not lyric_url:
            print(title)

        return lyric_url

    def get_lyrics(self, lyric_url):
        def parse_melon_lyrics(lyric_url):
            _res = req.get(lyric_url)
            _soup = BeautifulSoup(_res.text, 'html.parser')
            check_lyric_exist = _soup.find("div", class_="lyric_none")
            if bool(check_lyric_exist):
                print(lyric_url, "Not exist")
                raise ValueError("No lyrics")

            _txt = _soup.find("div", class_="lyric", id="d_video_summary")
            try:
                _lyrics = re.sub("<br>|<\\br>|\t",' ',_txt.text)
            except AttributeError as e:
                print("Attribue error", lyric_url, e)
                return None
            return _lyrics.strip()

        def parse_bugs_lyrics(lyric_url):
            _res = req.get(lyric_url)
            _soup = BeautifulSoup(_res.text, 'html.parser')
            check_lyric_exist = _soup.find("p", class_="comingsoon")
            if bool(check_lyric_exist):
                print(lyric_url, "Not exist")
                raise ValueError("No lyrics")
            lyric_tag = _soup.select_one("div.lyricsContainer")
            dusted_lyric = lyric_tag.xmp.text
            lyric = " ".join([re.sub('\r','',line) for line in dusted_lyric.split('\n')])
            return lyric.strip()

        lyric_closers = {
                    'melon': parse_melon_lyrics,
                    'bugs': parse_bugs_lyrics
                }

        return lyric_closers[self.source](lyric_url)


if __name__ == '__main__':
    ly = lyrics('bugs')
    lyric_url = ly.match_id('599187', '향수')
    print(lyric_url)
    print(ly.get_lyrics(lyric_url))


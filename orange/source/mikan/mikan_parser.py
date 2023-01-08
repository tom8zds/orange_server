from datetime import datetime
import re
from typing import List
from orange.core.util.utils import write_log
from orange.source.mikan.mikan_define import MIKAN_BASE, MikanWeekDay
from orange.core.source.model import *

import bs4
import xml.etree.ElementTree as ET


class MikanParser:
    def parse_season(text: str) -> dict[WeekDay, List[Bangumi]]:

        result: dict[WeekDay, List[Bangumi]] = {}

        soup = bs4.BeautifulSoup(text, "html.parser")
        rowElements = soup.find_all("div", attrs={"class": "sk-bangumi"})

        for row in rowElements:
            titleElem = row.find("div", attrs={"class": "row"})
            if (titleElem != None):
                day = re.sub('\s+', '', titleElem.text)
                weekDay: WeekDay = MikanWeekDay[day]
                anime_list = row.find_all("li")

                bangumi_list: List[Bangumi] = []
                for anime in anime_list:
                    cover = MIKAN_BASE + anime.find("span").attrs["data-src"]
                    # cover = anime.find("span").attributes("background-image")
                    anime_info = anime.find("div", attrs={"class": "an-info"})
                    anime_info_group = anime_info.find(
                        "div", attrs={"class": "an-info-group"})

                    if (anime_info_group.find("a") is None):
                        anime_name = anime_info_group.find_all("div")[
                            1].attrs["title"]
                    else:
                        anime_name = anime_info_group.find("a").attrs["title"]

                    anime_id = anime.find("span").attrs["data-bangumiid"]

                    bangumi: Bangumi = Bangumi(anime_id, anime_name, cover)

                    bangumi_list.append(bangumi)

                result[weekDay.value] = bangumi_list
        return result

    def parse_detail(text: str) -> BangumiDetail:
        soup = bs4.BeautifulSoup(text, "html.parser")

        # parse info
        coverImg = soup.find("div", attrs={"class": "bangumi-poster"})
        urls = re.findall("url\('(.*)'\)", coverImg.attrs["style"])

        write_log(urls[0])

        title = soup.find("p", attrs={"class": "bangumi-title"}).text

        id = soup.find("button", attrs={
                       "class": "js-subscribe_bangumi_page"}).attrs["data-bangumiid"]

        bangumi: Bangumi = Bangumi(int(id), title.strip(), urls[0])

        # parse subgroups
        rowElements = soup.find_all("li", attrs={"class": "leftbar-item"})

        write_log(len(rowElements))

        subGroups: List[SubGroup] = []

        for row in rowElements:
            titleElem = row.find("a", attrs={"class": "subgroup-name"})
            subGroups.append(SubGroup(
                name=titleElem.text, id=titleElem.attrs["data-anchor"].replace('#', '')))

        return BangumiDetail(info=bangumi, subGroups=subGroups)

    def parse_rss_channel(xml: str) -> SubscribeChannel:
        xml = re.sub(r'\sxmlns="[^"]+"', '', xml)
  
        # create element tree object
        tree = ET.fromstring(xml)

        items = []

        title = tree.findtext('./channel/title')
        link = tree.findtext('./channel/link')
        description = tree.findtext('./channel/description')

        # iterate news items
        for item in tree.findall('./channel/item'):
            item_link= item.findtext('./link')
            item_title= item.findtext('./title')
            item_description= item.findtext('./description')
            item_torrent= item.find('./enclosure').get("url")
            item_size= item.findtext('./torrent/contentLength')
            item_update= item.findtext('./torrent/pubDate')
            if(len(item_update) <23 and len(item_update) > 20):
                item_update = item_update + "0"

            items.append(SubscribeItem(item_link, item_title, item_description,
                         item_torrent, item_size, datetime.fromisoformat(item_update).timestamp()))

        return SubscribeChannel(title, link, description, items)

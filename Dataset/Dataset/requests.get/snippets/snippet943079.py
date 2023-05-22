from typing import Any, Dict, List, Union
import pycountry
import requests
from urllib.parse import urlencode
from itunespy import artist
from itunespy import music_artist
from itunespy import music_album
from itunespy import movie_artist
from itunespy import ebook_artist
from itunespy import track
from itunespy import result_item


def search(term: str, country: str='US', media: str='all', entity: str=None, attribute: str=None, limit: int=50) -> List[result_item.ResultItem]:
    "\n    Returns the result of the search of the specified term in an array of result_item(s)\n    :param term: String. The URL-encoded text string you want to search for. Example: Steven Wilson.\n                 The method will take care of spaces so you don't have to.\n    :param country: String. The two-letter country code for the store you want to search.\n                    For a full list of the codes: http://en.wikipedia.org/wiki/%20ISO_3166-1_alpha-2\n    :param media: String. The media type you want to search for. Example: music\n    :param entity: String. The type of results you want returned, relative to the specified media type. Example: musicArtist.\n                   Full list: musicArtist, musicTrack, album, musicVideo, mix, song\n    :param attribute: String. The attribute you want to search for in the stores, relative to the specified media type.\n    :param limit: Integer. The number of search results you want the iTunes Store to return.\n    :return: An array of result_item(s)\n    "
    search_url = _url_search_builder(term, country, media, entity, attribute, limit)
    r = requests.get(search_url)
    try:
        json = r.json()['results']
        result_count = r.json()['resultCount']
    except:
        raise ConnectionError(general_no_connection)
    if (result_count == 0):
        raise LookupError((search_error + str(term)))
    return _get_result_list(json, country)

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


def lookup(id: Union[(str, int)]=None, artist_amg_id: Union[(str, int)]=None, upc: Union[(str, int)]=None, country: str='US', media: str='all', entity: str=None, attribute: str=None, limit: int=50) -> List[result_item.ResultItem]:
    '\n    Returns the result of the lookup of the specified id, artist_amg_id or upc in an array of result_item(s)\n    :param id: String. iTunes ID of the artist, album, track, ebook or software\n    :param artist_amg_id: String. All Music Guide ID of the artist\n    :param upc: String. UPCs/EANs\n    :param country: String. The two-letter country code for the store you want to search.\n                    For a full list of the codes: http://en.wikipedia.org/wiki/%20ISO_3166-1_alpha-2\n    :param media: String. The media type you want to search for. Example: music\n    :param entity: String. The type of results you want returned, relative to the specified media type. Example: musicArtist.\n                   Full list: musicArtist, musicTrack, album, musicVideo, mix, song\n    :param attribute: String. The attribute you want to search for in the stores, relative to the specified media type.\n    :param limit: Integer. The number of search results you want the iTunes Store to return.\n    :return: An array of result_item(s)\n    '
    if ((id is None) and (artist_amg_id is None) and (upc is None)):
        raise ValueError(lookup_no_ids)
    lookup_url = _url_lookup_builder(id, artist_amg_id, upc, country, media, entity, attribute, limit)
    r = requests.get(lookup_url)
    try:
        json = r.json()['results']
        result_count = r.json()['resultCount']
    except KeyError:
        raise ConnectionError(general_no_connection)
    if (result_count == 0):
        raise LookupError(lookup_error)
    return _get_result_list(json, country)

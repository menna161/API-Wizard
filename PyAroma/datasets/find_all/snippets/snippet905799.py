from psaripper.metadata import EpisodeMetadata
from psaripper.util import create_scraper, decrypt_url


def get_torrent_urls(self):
    torrindex = self.entry[1].find_all('div')[self.torr_index].find_all('p')
    torrent = None
    for para in torrindex:
        if (para.text.strip() == 'TORRENT'):
            torrent = para.strong.a['href']
    if (not torrent):
        return []
    try:
        torrenturl = decrypt_url(torrent, self.scraper)
    except Exception:
        self.scraper = create_scraper()
        torrenturl = decrypt_url(torrent, self.scraper)
    return torrenturl

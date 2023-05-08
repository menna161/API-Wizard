from psaripper.metadata import EpisodeMetadata
from psaripper.util import create_scraper, decrypt_url


def get_ddl_parts(self, entry):
    all_parts = self.entry[1].find_all('div', class_='dropshadowboxes-container')
    return [(part.a.text.strip(), part.a['href']) for part in all_parts if ('Download' in part.a.text)]

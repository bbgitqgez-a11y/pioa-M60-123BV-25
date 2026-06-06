from .db import DataBase
from .errors import ProtectedRecordError
from .table import AlbumTable, ArtistTable


class MemoryDataBase(DataBase):
    def __init__(self):
        self.artists = ArtistTable()
        self.albums = AlbumTable(self.artists)

    def create_artist(self, artist_id, nickname, main_genre):
        return self.artists.create(artist_id, nickname, main_genre)

    def select_artists(self, artist_id=None, nickname=None, main_genre=None):
        return self.artists.select(artist_id, nickname, main_genre)

    def update_artist(self, artist_id, nickname=None, main_genre=None):
        return self.artists.update(artist_id, nickname, main_genre)

    def delete_artist(self, artist_id):
        if self.albums.has_albums_by_artist(artist_id):
            raise ProtectedRecordError(
                f"Нельзя удалить артиста с id={artist_id}: сначала удалите его альбомы."
            )
        return self.artists.delete(artist_id)

    def create_album(self, album_id, title, artist_id, release_year, label):
        return self.albums.create(album_id, title, artist_id, release_year, label)

    def select_albums(
            self,
            album_id=None,
            title=None,
            artist_id=None,
            release_year=None,
            label=None,
    ):
        return self.albums.select(album_id, title, artist_id, release_year, label)

    def update_album(self, album_id, title=None, artist_id=None, year=None, label=None):
        return self.albums.update(album_id, title, artist_id, year, label)

    def delete_album(self, album_id):
        return self.albums.delete(album_id)

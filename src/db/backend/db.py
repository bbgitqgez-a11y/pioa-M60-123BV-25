from abc import ABC, abstractmethod


class DataBase(ABC):
    @abstractmethod
    def create_artist(self, artist_id, nickname, main_genre):
        pass

    @abstractmethod
    def select_artists(self, artist_id=None, nickname=None, main_genre=None):
        pass

    @abstractmethod
    def update_artist(self, artist_id, nickname=None, main_genre=None):
        pass

    @abstractmethod
    def delete_artist(self, artist_id):
        pass

    @abstractmethod
    def create_album(self, album_id, title, artist_id, release_year, label):
        pass

    @abstractmethod
    def select_albums(
        self,
        album_id=None,
        title=None,
        artist_id=None,
        release_year=None,
        label=None,
    ):
        pass

    @abstractmethod
    def update_album(self, album_id, title=None, artist_id=None, year=None, label=None):
        pass

    @abstractmethod
    def delete_album(self, album_id):
        pass

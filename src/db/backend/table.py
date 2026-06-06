from .errors import (
    DuplicateIdError,
    ForeignKeyError,
    RecordNotFoundError,
    ValidationError,
)
from .record import AlbumRecord, ArtistRecord


class ArtistTable:
    def __init__(self, records=None):
        self.records = records if records is not None else []

    def create(self, artist_id, nickname, main_genre):
        if artist_id < 0:
            raise ValidationError("ID артиста должен быть неотрицательным числом.")
        if self.exists(artist_id):
            raise DuplicateIdError(f"Артист с id={artist_id} уже существует.")

        nickname = nickname.strip()
        if not nickname:
            raise ValidationError("Псевдоним артиста не может быть пустым.")

        artist = ArtistRecord(artist_id, nickname, main_genre.strip())
        self.records.append(artist)
        return artist

    def select(self, artist_id=None, nickname=None, main_genre=None):
        result = []

        for artist in self.records:
            if artist_id is not None and artist.artist_id != artist_id:
                continue
            if nickname is not None and artist.nickname != nickname:
                continue
            if main_genre is not None and artist.main_genre != main_genre:
                continue
            result.append(artist)

        return result

    def update(self, artist_id, nickname=None, main_genre=None):
        for index, artist in enumerate(self.records):
            if artist.artist_id != artist_id:
                continue

            if nickname is None:
                nickname = artist.nickname
            else:
                nickname = nickname.strip()
                if not nickname:
                    raise ValidationError("Псевдоним артиста не может быть пустым.")

            if main_genre is None:
                main_genre = artist.main_genre
            else:
                main_genre = main_genre.strip()

            updated_artist = ArtistRecord(artist_id, nickname, main_genre)
            self.records[index] = updated_artist
            return updated_artist

        raise RecordNotFoundError(f"Артист с id={artist_id} не найден.")

    def delete(self, artist_id):
        for index, artist in enumerate(self.records):
            if artist.artist_id == artist_id:
                return self.records.pop(index)

        raise RecordNotFoundError(f"Артист с id={artist_id} не найден.")

    def exists(self, artist_id):
        for artist in self.records:
            if artist.artist_id == artist_id:
                return True
        return False


class AlbumTable:
    def __init__(self, artists, records=None):
        self.artists = artists
        self.records = records if records is not None else []

    def create(self, album_id, title, artist_id, release_year, label):
        if album_id < 0:
            raise ValidationError("ID альбома должен быть неотрицательным числом.")
        if self.exists(album_id):
            raise DuplicateIdError(f"Альбом с id={album_id} уже существует.")

        title = title.strip()
        if not title:
            raise ValidationError("Название альбома не может быть пустым.")
        if not self.artists.exists(artist_id):
            raise ForeignKeyError(f"Артист с id={artist_id} не существует.")
        if release_year < 1 or release_year > 2100:
            raise ValidationError("Год выпуска должен быть от 1 до 2100.")

        album = AlbumRecord(album_id, title, artist_id, release_year, label.strip())
        self.records.append(album)
        return album

    def select(
            self,
            album_id=None,
            title=None,
            artist_id=None,
            release_year=None,
            label=None,
    ):
        result = []

        for album in self.records:
            if album_id is not None and album.album_id != album_id:
                continue
            if title is not None and album.title != title:
                continue
            if artist_id is not None and album.artist_id != artist_id:
                continue
            if release_year is not None and album.release_year != release_year:
                continue
            if label is not None and album.label != label:
                continue
            result.append(album)

        return result

    def update(self, album_id, title=None, artist_id=None, year=None, label=None):
        for index, album in enumerate(self.records):
            if album.album_id != album_id:
                continue

            if title is None:
                title = album.title
            else:
                title = title.strip()
                if not title:
                    raise ValidationError("Название альбома не может быть пустым.")

            if artist_id is None:
                artist_id = album.artist_id
            elif not self.artists.exists(artist_id):
                raise ForeignKeyError(f"Артист с id={artist_id} не существует.")

            if year is None:
                year = album.release_year
            elif year < 1 or year > 2100:
                raise ValidationError("Год выпуска должен быть от 1 до 2100.")

            if label is None:
                label = album.label
            else:
                label = label.strip()

            updated_album = AlbumRecord(album_id, title, artist_id, year, label)
            self.records[index] = updated_album
            return updated_album

        raise RecordNotFoundError(f"Альбом с id={album_id} не найден.")

    def delete(self, album_id):
        for index, album in enumerate(self.records):
            if album.album_id == album_id:
                return self.records.pop(index)

        raise RecordNotFoundError(f"Альбом с id={album_id} не найден.")

    def exists(self, album_id):
        for album in self.records:
            if album.album_id == album_id:
                return True
        return False

    def has_albums_by_artist(self, artist_id):
        for album in self.records:
            if album.artist_id == artist_id:
                return True
        return False

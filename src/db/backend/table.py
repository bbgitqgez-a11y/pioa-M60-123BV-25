from .errors import (
    DuplicateIdError,
    ForeignKeyError,
    RecordNotFoundError,
    ValidationError,
)
from .record import AlbumRecord, ArtistRecord


ALBUM_RELEASE_YEAR_MIN = 1
ALBUM_RELEASE_YEAR_MAX = 2026


def _validate_int(value, field_name):
    if type(value) is not int:
        raise ValidationError(f"{field_name} должен быть целым числом.")
    return value


def _validate_optional_int(value, field_name):
    if value is None:
        return None
    return _validate_int(value, field_name)


def _validate_string(value, field_name):
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} должен быть строкой.")
    return value


def _validate_optional_string(value, field_name):
    if value is None:
        return None
    return _validate_string(value, field_name)


def _validate_artist_id(artist_id):
    artist_id = _validate_int(artist_id, "ID артиста")
    if artist_id < 0:
        raise ValidationError("ID артиста должен быть неотрицательным числом.")
    return artist_id


def _validate_album_id(album_id):
    album_id = _validate_int(album_id, "ID альбома")
    if album_id < 0:
        raise ValidationError("ID альбома должен быть неотрицательным числом.")
    return album_id


def _validate_release_year(release_year):
    release_year = _validate_int(release_year, "Год выпуска")
    if (
        release_year < ALBUM_RELEASE_YEAR_MIN
        or release_year > ALBUM_RELEASE_YEAR_MAX
    ):
        raise ValidationError("Год выпуска должен быть от 1 до 2026.")
    return release_year


class ArtistTable:
    def __init__(self, records=None):
        self.records = records if records is not None else []

    def create(self, artist_id, nickname, main_genre):
        artist_id = _validate_artist_id(artist_id)
        if self.exists(artist_id):
            raise DuplicateIdError(f"Артист с id={artist_id} уже существует.")

        nickname = _validate_string(nickname, "Псевдоним артиста").strip()
        if not nickname:
            raise ValidationError("Псевдоним артиста не может быть пустым.")

        main_genre = _validate_string(main_genre, "Основной жанр").strip()
        artist = ArtistRecord(artist_id, nickname, main_genre)
        self.records.append(artist)
        return artist

    def select(self, artist_id=None, nickname=None, main_genre=None):
        artist_id = _validate_optional_int(artist_id, "ID артиста")
        nickname = _validate_optional_string(nickname, "Псевдоним артиста")
        main_genre = _validate_optional_string(main_genre, "Основной жанр")

        return [
            ArtistRecord.from_dict(artist.to_dict())
            for artist in self.records
            if (artist_id is None or artist.artist_id == artist_id)
            and (nickname is None or artist.nickname == nickname)
            and (main_genre is None or artist.main_genre == main_genre)
        ]

    def update(self, artist_id, nickname=None, main_genre=None):
        artist_id = _validate_artist_id(artist_id)

        for index, artist in enumerate(self.records):
            if artist.artist_id != artist_id:
                continue

            if nickname is None:
                nickname = artist.nickname
            else:
                nickname = _validate_string(nickname, "Псевдоним артиста").strip()
                if not nickname:
                    raise ValidationError("Псевдоним артиста не может быть пустым.")

            if main_genre is None:
                main_genre = artist.main_genre
            else:
                main_genre = _validate_string(main_genre, "Основной жанр").strip()

            updated_artist = ArtistRecord(artist_id, nickname, main_genre)
            self.records[index] = updated_artist
            return updated_artist

        raise RecordNotFoundError(f"Артист с id={artist_id} не найден.")

    def delete(self, artist_id):
        artist_id = _validate_artist_id(artist_id)

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
        album_id = _validate_album_id(album_id)
        if self.exists(album_id):
            raise DuplicateIdError(f"Альбом с id={album_id} уже существует.")

        title = _validate_string(title, "Название альбома").strip()
        if not title:
            raise ValidationError("Название альбома не может быть пустым.")
        artist_id = _validate_artist_id(artist_id)
        if not self.artists.exists(artist_id):
            raise ForeignKeyError(f"Артист с id={artist_id} не существует.")
        release_year = _validate_release_year(release_year)

        label = _validate_string(label, "Лейбл").strip()
        album = AlbumRecord(album_id, title, artist_id, release_year, label)
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
        album_id = _validate_optional_int(album_id, "ID альбома")
        title = _validate_optional_string(title, "Название альбома")
        artist_id = _validate_optional_int(artist_id, "ID артиста")
        release_year = _validate_optional_int(release_year, "Год выпуска")
        label = _validate_optional_string(label, "Лейбл")

        return [
            AlbumRecord.from_dict(album.to_dict())
            for album in self.records
            if (album_id is None or album.album_id == album_id)
            and (title is None or album.title == title)
            and (artist_id is None or album.artist_id == artist_id)
            and (release_year is None or album.release_year == release_year)
            and (label is None or album.label == label)
        ]

    def update(self, album_id, title=None, artist_id=None, year=None, label=None):
        album_id = _validate_album_id(album_id)

        for index, album in enumerate(self.records):
            if album.album_id != album_id:
                continue

            if title is None:
                title = album.title
            else:
                title = _validate_string(title, "Название альбома").strip()
                if not title:
                    raise ValidationError("Название альбома не может быть пустым.")

            if artist_id is None:
                artist_id = album.artist_id
            else:
                artist_id = _validate_artist_id(artist_id)
                if not self.artists.exists(artist_id):
                    raise ForeignKeyError(f"Артист с id={artist_id} не существует.")

            if year is None:
                year = album.release_year
            else:
                year = _validate_release_year(year)

            if label is None:
                label = album.label
            else:
                label = _validate_string(label, "Лейбл").strip()

            updated_album = AlbumRecord(album_id, title, artist_id, year, label)
            self.records[index] = updated_album
            return updated_album

        raise RecordNotFoundError(f"Альбом с id={album_id} не найден.")

    def delete(self, album_id):
        album_id = _validate_album_id(album_id)

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

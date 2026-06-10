import json
from pathlib import Path

from .db import DataBase
from .errors import FileDataBaseError, ProtectedRecordError
from .record import AlbumRecord, ArtistRecord
from .table import (
    ALBUM_RELEASE_YEAR_MAX,
    ALBUM_RELEASE_YEAR_MIN,
    AlbumTable,
    ArtistTable,
)


class FileDataBase(DataBase):
    ARTIST_FIELDS = ["artist_id", "nickname", "main_genre"]
    ALBUM_FIELDS = ["album_id", "title", "artist_id", "release_year", "label"]

    def __init__(self, path):
        self.artists = ArtistTable()
        self.albums = AlbumTable(self.artists)
        self.folder = Path(path)
        self.storage = self.folder / "database.json"
        self._prepare_folder()

        if self.storage.exists():
            self._load()
        else:
            self._save()

    def create_artist(self, artist_id, nickname, main_genre):
        result = self.artists.create(artist_id, nickname, main_genre)
        self._save()
        return result

    def select_artists(self, artist_id=None, nickname=None, main_genre=None):
        return self.artists.select(artist_id, nickname, main_genre)

    def update_artist(self, artist_id, nickname=None, main_genre=None):
        result = self.artists.update(artist_id, nickname, main_genre)
        self._save()
        return result

    def delete_artist(self, artist_id):
        if self.albums.has_albums_by_artist(artist_id):
            raise ProtectedRecordError(
                f"Нельзя удалить артиста с id={artist_id}: сначала удалите его альбомы."
            )
        result = self.artists.delete(artist_id)
        self._save()
        return result

    def create_album(self, album_id, title, artist_id, release_year, label):
        result = self.albums.create(album_id, title, artist_id, release_year, label)
        self._save()
        return result

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
        result = self.albums.update(album_id, title, artist_id, year, label)
        self._save()
        return result

    def delete_album(self, album_id):
        result = self.albums.delete(album_id)
        self._save()
        return result

    def _prepare_folder(self):
        try:
            self.folder.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            raise FileDataBaseError(f"Не удалось подготовить папку: {error}") from error

    def _load(self):
        data = self._read_file()
        artists_data = self._read_table(data, "artists", self.ARTIST_FIELDS)
        albums_data = self._read_table(data, "albums", self.ALBUM_FIELDS)

        try:
            artists = [ArtistRecord.from_dict(item) for item in artists_data]
            albums = [AlbumRecord.from_dict(item) for item in albums_data]
        except (KeyError, TypeError, ValueError) as error:
            raise FileDataBaseError("Файл базы содержит некорректные записи.") from error

        self._validate(artists, albums)
        self.artists.records = artists
        self.albums.records = albums

    def _read_file(self):
        try:
            with open(self.storage, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise FileDataBaseError("Файл базы содержит некорректный JSON.") from error
        except OSError as error:
            raise FileDataBaseError(f"Не удалось прочитать базу: {error}") from error

        if not isinstance(data, dict) or not isinstance(data.get("tables"), dict):
            raise FileDataBaseError("Структура файла базы некорректна.")
        return data

    def _read_table(self, data, name, fields):
        table = data["tables"].get(name)
        if not isinstance(table, dict):
            raise FileDataBaseError(f"Таблица {name} отсутствует.")
        if table.get("fields") != fields:
            raise FileDataBaseError(f"Структура таблицы {name} некорректна.")
        if not isinstance(table.get("records"), list):
            raise FileDataBaseError(f"Записи таблицы {name} должны быть списком.")
        return table["records"]

    def _validate(self, artists, albums):
        artist_ids = set()
        album_ids = set()

        for artist in artists:
            if artist.artist_id in artist_ids:
                raise FileDataBaseError("В таблице артистов повторяются id.")
            if artist.artist_id < 0 or not artist.nickname.strip():
                raise FileDataBaseError("В таблице артистов есть некорректная запись.")
            artist_ids.add(artist.artist_id)

        for album in albums:
            if album.album_id in album_ids:
                raise FileDataBaseError("В таблице альбомов повторяются id.")
            if album.album_id < 0 or not album.title.strip():
                raise FileDataBaseError("В таблице альбомов есть некорректная запись.")
            if (
                album.release_year < ALBUM_RELEASE_YEAR_MIN
                or album.release_year > ALBUM_RELEASE_YEAR_MAX
            ):
                raise FileDataBaseError("В таблице альбомов указан некорректный год.")
            if album.artist_id not in artist_ids:
                raise FileDataBaseError("В альбоме указан несуществующий артист.")
            album_ids.add(album.album_id)

    def _save(self):
        data = {
            "tables": {
                "artists": {
                    "fields": self.ARTIST_FIELDS,
                    "records": [artist.to_dict() for artist in self.artists.records],
                },
                "albums": {
                    "fields": self.ALBUM_FIELDS,
                    "records": [album.to_dict() for album in self.albums.records],
                },
            }
        }

        try:
            with open(self.storage, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError as error:
            raise FileDataBaseError(f"Не удалось сохранить базу: {error}") from error

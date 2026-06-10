import unittest
from dataclasses import FrozenInstanceError

from src.db.backend.errors import (
    DuplicateIdError,
    ForeignKeyError,
    ProtectedRecordError,
    RecordNotFoundError,
    ValidationError,
)
from src.db.backend.memory import MemoryDataBase


class TestMemoryDataBase(unittest.TestCase):
    def setUp(self):
        self.db = MemoryDataBase()
        self.db.create_artist(1, "Кино", "Рок")
        self.db.create_artist(2, "Земфира", "Рок")

    def test_create_artist_positive(self):
        artist = self.db.create_artist(3, "Би-2", "Рок")

        self.assertEqual(artist, (3, "Би-2", "Рок"))
        self.assertEqual(len(self.db.select_artists()), 3)

    def test_create_artist_strips_fields(self):
        artist = self.db.create_artist(3, "  Сплин  ", "  Рок  ")

        self.assertEqual(artist, (3, "Сплин", "Рок"))

    def test_create_artist_duplicate_id(self):
        with self.assertRaises(DuplicateIdError):
            self.db.create_artist(1, "Другой артист", "Поп")

    def test_create_artist_negative_id(self):
        with self.assertRaises(ValidationError):
            self.db.create_artist(-1, "Неверный артист", "Рок")

    def test_create_artist_empty_nickname(self):
        with self.assertRaises(ValidationError):
            self.db.create_artist(3, "   ", "Рок")

    def test_artist_methods_validate_argument_types(self):
        cases = [
            lambda: self.db.create_artist("3", "Би-2", "Рок"),
            lambda: self.db.create_artist(3, None, "Рок"),
            lambda: self.db.create_artist(3, "Би-2", None),
            lambda: self.db.select_artists(artist_id="1"),
            lambda: self.db.select_artists(nickname=1),
            lambda: self.db.update_artist("1", main_genre="Постпанк"),
            lambda: self.db.update_artist(1, nickname=1),
            lambda: self.db.update_artist(1, main_genre=1),
            lambda: self.db.delete_artist("1"),
        ]

        for case in cases:
            with self.subTest(case=case):
                with self.assertRaises(ValidationError):
                    case()

    def test_select_artists_by_id(self):
        artists = self.db.select_artists(artist_id=1)

        self.assertEqual(artists, [(1, "Кино", "Рок")])

    def test_select_artists_by_name_and_genre(self):
        artists = self.db.select_artists(nickname="Земфира", main_genre="Рок")

        self.assertEqual(artists, [(2, "Земфира", "Рок")])

    def test_select_artists_no_match(self):
        artists = self.db.select_artists(main_genre="Джаз")

        self.assertEqual(artists, [])

    def test_select_artists_returns_copy(self):
        artists = self.db.select_artists()
        artists.clear()

        self.assertEqual(len(self.db.select_artists()), 2)

    def test_select_artists_returns_immutable_records(self):
        artist = self.db.select_artists(artist_id=1)[0]

        with self.assertRaises(FrozenInstanceError):
            artist.nickname = "Новый псевдоним"

        self.assertEqual(self.db.select_artists(artist_id=1), [(1, "Кино", "Рок")])

    def test_update_artist_positive(self):
        updated = self.db.update_artist(1, main_genre="Постпанк")

        self.assertEqual(updated, (1, "Кино", "Постпанк"))

    def test_update_artist_empty_nickname(self):
        with self.assertRaises(ValidationError):
            self.db.update_artist(1, nickname="")

    def test_update_artist_wrong_id(self):
        with self.assertRaises(RecordNotFoundError):
            self.db.update_artist(99, nickname="Нет такого артиста")

    def test_delete_artist_positive(self):
        deleted = self.db.delete_artist(2)

        self.assertEqual(deleted, (2, "Земфира", "Рок"))
        self.assertEqual(self.db.select_artists(artist_id=2), [])

    def test_delete_artist_wrong_id(self):
        with self.assertRaises(RecordNotFoundError):
            self.db.delete_artist(99)

    def test_delete_artist_with_albums(self):
        self.db.create_album(1, "Группа крови", 1, 1988, "Мелодия")

        with self.assertRaises(ProtectedRecordError):
            self.db.delete_artist(1)

    def test_create_album_positive(self):
        album = self.db.create_album(1, "Группа крови", 1, 1988, "Мелодия")

        self.assertEqual(album, (1, "Группа крови", 1, 1988, "Мелодия"))
        self.assertEqual(len(self.db.select_albums()), 1)

    def test_create_album_strips_fields(self):
        album = self.db.create_album(1, "  Звезда по имени Солнце  ", 1, 1989, "  Мелодия  ")

        self.assertEqual(album, (1, "Звезда по имени Солнце", 1, 1989, "Мелодия"))

    def test_create_album_duplicate_id(self):
        self.db.create_album(1, "Группа крови", 1, 1988, "Мелодия")

        with self.assertRaises(DuplicateIdError):
            self.db.create_album(1, "Другой альбом", 1, 1990, "Лейбл")

    def test_create_album_unknown_artist(self):
        with self.assertRaises(ForeignKeyError):
            self.db.create_album(1, "Неизвестный альбом", 99, 2020, "Лейбл")

    def test_create_album_empty_title(self):
        with self.assertRaises(ValidationError):
            self.db.create_album(1, "", 1, 2020, "Лейбл")

    def test_create_album_negative_id(self):
        with self.assertRaises(ValidationError):
            self.db.create_album(-1, "Неверный альбом", 1, 2020, "Лейбл")

    def test_create_album_wrong_year(self):
        with self.assertRaises(ValidationError):
            self.db.create_album(1, "Альбом из будущего", 1, 2200, "Лейбл")

    def test_album_methods_validate_argument_types(self):
        self.db.create_album(1, "Группа крови", 1, 1988, "Мелодия")

        cases = [
            lambda: self.db.create_album("2", "Альбом", 1, 2020, "Лейбл"),
            lambda: self.db.create_album(2, None, 1, 2020, "Лейбл"),
            lambda: self.db.create_album(2, "Альбом", "1", 2020, "Лейбл"),
            lambda: self.db.create_album(2, "Альбом", 1, "2020", "Лейбл"),
            lambda: self.db.create_album(2, "Альбом", 1, 2020, None),
            lambda: self.db.select_albums(album_id="1"),
            lambda: self.db.select_albums(title=1),
            lambda: self.db.select_albums(artist_id="1"),
            lambda: self.db.select_albums(release_year="1988"),
            lambda: self.db.select_albums(label=1),
            lambda: self.db.update_album("1", title="Альбом"),
            lambda: self.db.update_album(1, title=1),
            lambda: self.db.update_album(1, artist_id="1"),
            lambda: self.db.update_album(1, year="1988"),
            lambda: self.db.update_album(1, label=1),
            lambda: self.db.delete_album("1"),
        ]

        for case in cases:
            with self.subTest(case=case):
                with self.assertRaises(ValidationError):
                    case()

    def test_select_albums_by_fields(self):
        self.db.create_album(1, "Группа крови", 1, 1988, "Мелодия")
        self.db.create_album(2, "Вендетта", 2, 2005, "Real Records")

        albums = self.db.select_albums(artist_id=2, label="Real Records")

        self.assertEqual(albums, [(2, "Вендетта", 2, 2005, "Real Records")])

    def test_select_albums_all(self):
        self.db.create_album(1, "Группа крови", 1, 1988, "Мелодия")
        self.db.create_album(2, "Вендетта", 2, 2005, "Real Records")

        self.assertEqual(len(self.db.select_albums()), 2)

    def test_select_albums_no_match(self):
        self.db.create_album(1, "Группа крови", 1, 1988, "Мелодия")

        self.assertEqual(self.db.select_albums(title="Нет такого альбома"), [])

    def test_select_albums_returns_copy(self):
        self.db.create_album(1, "Группа крови", 1, 1988, "Мелодия")
        albums = self.db.select_albums()
        albums.clear()

        self.assertEqual(len(self.db.select_albums()), 1)

    def test_update_album_positive(self):
        self.db.create_album(1, "Группа крови", 1, 1988, "Мелодия")

        updated = self.db.update_album(1, title="Группа крови", label="Moroz Records")

        self.assertEqual(updated, (1, "Группа крови", 1, 1988, "Moroz Records"))

    def test_update_album_artist(self):
        self.db.create_album(1, "Альбом", 1, 2000, "Лейбл")

        updated = self.db.update_album(1, artist_id=2)

        self.assertEqual(updated[2], 2)

    def test_update_album_wrong_id(self):
        with self.assertRaises(RecordNotFoundError):
            self.db.update_album(99, title="Нет такого альбома")

    def test_update_album_unknown_artist(self):
        self.db.create_album(1, "Группа крови", 1, 1988, "Мелодия")

        with self.assertRaises(ForeignKeyError):
            self.db.update_album(1, artist_id=99)

    def test_update_album_empty_title(self):
        self.db.create_album(1, "Группа крови", 1, 1988, "Мелодия")

        with self.assertRaises(ValidationError):
            self.db.update_album(1, title=" ")

    def test_update_album_wrong_year(self):
        self.db.create_album(1, "Группа крови", 1, 1988, "Мелодия")

        with self.assertRaises(ValidationError):
            self.db.update_album(1, year=0)

    def test_delete_album_positive(self):
        self.db.create_album(1, "Группа крови", 1, 1988, "Мелодия")

        deleted = self.db.delete_album(1)

        self.assertEqual(deleted, (1, "Группа крови", 1, 1988, "Мелодия"))
        self.assertEqual(self.db.select_albums(), [])

    def test_delete_album_wrong_id(self):
        with self.assertRaises(RecordNotFoundError):
            self.db.delete_album(99)


if __name__ == "__main__":
    unittest.main()

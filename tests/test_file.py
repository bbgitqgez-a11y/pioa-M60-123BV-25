import json
import unittest
from tempfile import TemporaryDirectory

from src.db.backend.errors import (
    DuplicateIdError,
    FileDataBaseError,
    ForeignKeyError,
    ProtectedRecordError,
)
from src.db.backend.file import FileDataBase


class TestFileDataBase(unittest.TestCase):
    def make_file(self, folder, data):
        with open(f"{folder}/database.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)

    def empty_data(self):
        return {
            "tables": {
                "artists": {
                    "fields": ["artist_id", "nickname", "main_genre"],
                    "records": [],
                },
                "albums": {
                    "fields": [
                        "album_id",
                        "title",
                        "artist_id",
                        "release_year",
                        "label",
                    ],
                    "records": [],
                },
            }
        }

    def test_create_and_load_data_again(self):
        with TemporaryDirectory() as folder:
            db = FileDataBase(folder)
            db.create_artist(1, "Кино", "Рок")
            db.create_album(1, "Группа крови", 1, 1988, "Мелодия")

            loaded = FileDataBase(folder)

            self.assertEqual(loaded.select_artists(), [(1, "Кино", "Рок")])
            self.assertEqual(
                loaded.select_albums(),
                [(1, "Группа крови", 1, 1988, "Мелодия")],
            )

    def test_update_and_delete_data(self):
        with TemporaryDirectory() as folder:
            db = FileDataBase(folder)
            db.create_artist(1, "Кино", "Рок")
            db.create_album(1, "Группа крови", 1, 1988, "Мелодия")
            db.update_artist(1, main_genre="Постпанк")
            db.update_album(1, title="Звезда по имени Солнце", year=1989)
            db.delete_album(1)
            db.delete_artist(1)

            loaded = FileDataBase(folder)

            self.assertEqual(loaded.select_artists(), [])
            self.assertEqual(loaded.select_albums(), [])

    def test_json_structure(self):
        with TemporaryDirectory() as folder:
            db = FileDataBase(folder)
            db.create_artist(1, "Кино", "Рок")

            with open(f"{folder}/database.json", "r", encoding="utf-8") as file:
                data = json.load(file)

            self.assertIn("artists", data["tables"])
            self.assertIn("albums", data["tables"])
            self.assertEqual(data["tables"]["artists"]["records"][0]["nickname"], "Кино")

    def test_file_database_uses_common_validation(self):
        with TemporaryDirectory() as folder:
            db = FileDataBase(folder)
            db.create_artist(1, "Кино", "Рок")
            db.create_album(1, "Группа крови", 1, 1988, "Мелодия")

            with self.assertRaises(DuplicateIdError):
                db.create_artist(1, "Другой артист", "Поп")
            with self.assertRaises(ForeignKeyError):
                db.create_album(2, "Альбом", 99, 2020, "Лейбл")
            with self.assertRaises(ProtectedRecordError):
                db.delete_artist(1)

    def test_wrong_json(self):
        with TemporaryDirectory() as folder:
            with open(f"{folder}/database.json", "w", encoding="utf-8") as file:
                file.write("{неверный json")

            with self.assertRaises(FileDataBaseError):
                FileDataBase(folder)

    def test_wrong_root_structure(self):
        with TemporaryDirectory() as folder:
            self.make_file(folder, {"неверное поле": {}})

            with self.assertRaises(FileDataBaseError):
                FileDataBase(folder)

    def test_wrong_table_structure(self):
        with TemporaryDirectory() as folder:
            data = self.empty_data()
            data["tables"]["artists"]["fields"] = ["неверное поле"]
            self.make_file(folder, data)

            with self.assertRaises(FileDataBaseError):
                FileDataBase(folder)

    def test_records_are_not_list(self):
        with TemporaryDirectory() as folder:
            data = self.empty_data()
            data["tables"]["artists"]["records"] = {}
            self.make_file(folder, data)

            with self.assertRaises(FileDataBaseError):
                FileDataBase(folder)

    def test_wrong_artist_data(self):
        with TemporaryDirectory() as folder:
            data = self.empty_data()
            data["tables"]["artists"]["records"] = [
                {"artist_id": -1, "nickname": "", "main_genre": ""}
            ]
            self.make_file(folder, data)

            with self.assertRaises(FileDataBaseError):
                FileDataBase(folder)

    def test_duplicate_artist_id(self):
        with TemporaryDirectory() as folder:
            data = self.empty_data()
            data["tables"]["artists"]["records"] = [
                {"artist_id": 1, "nickname": "Кино", "main_genre": "Рок"},
                {"artist_id": 1, "nickname": "Земфира", "main_genre": "Рок"},
            ]
            self.make_file(folder, data)

            with self.assertRaises(FileDataBaseError):
                FileDataBase(folder)

    def test_album_with_unknown_artist(self):
        with TemporaryDirectory() as folder:
            data = self.empty_data()
            data["tables"]["albums"]["records"] = [
                {
                    "album_id": 1,
                    "title": "Альбом",
                    "artist_id": 99,
                    "release_year": 2020,
                    "label": "Лейбл",
                }
            ]
            self.make_file(folder, data)

            with self.assertRaises(FileDataBaseError):
                FileDataBase(folder)

    def test_wrong_album_year(self):
        with TemporaryDirectory() as folder:
            data = self.empty_data()
            data["tables"]["artists"]["records"] = [
                {"artist_id": 1, "nickname": "Кино", "main_genre": "Рок"}
            ]
            data["tables"]["albums"]["records"] = [
                {
                    "album_id": 1,
                    "title": "Альбом",
                    "artist_id": 1,
                    "release_year": 2027,
                    "label": "Лейбл",
                }
            ]
            self.make_file(folder, data)

            with self.assertRaises(FileDataBaseError):
                FileDataBase(folder)

    def test_path_is_not_folder(self):
        with TemporaryDirectory() as folder:
            path = f"{folder}/database.json"
            with open(path, "w", encoding="utf-8") as file:
                file.write("")

            with self.assertRaises(FileDataBaseError):
                FileDataBase(path)


if __name__ == "__main__":
    unittest.main()

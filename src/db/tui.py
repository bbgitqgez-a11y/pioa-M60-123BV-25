from .backend.memory import MemoryDataBase


class ConsoleApplication:
    def __init__(self, database=None):
        if database is None:
            database = MemoryDataBase()
        self.database = database

    def _read_int(self, prompt):
        while True:
            try:
                return int(input(prompt).strip())
            except ValueError:
                print("Ошибка: введите целое число.")

    def _read_optional_int(self, prompt):
        while True:
            raw = input(prompt).strip()
            if raw == "":
                return None
            try:
                return int(raw)
            except ValueError:
                print("Ошибка: введите целое число или оставьте поле пустым.")

    def _read_nonempty_string(self, prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Ошибка: значение не может быть пустым.")

    def _print_artists(self, artist_list):
        if not artist_list:
            print("Артисты не найдены.")
            return

        print("ID | Псевдоним | Жанр")
        print("-" * 45)
        for artist in artist_list:
            print(f"{artist[0]} | {artist[1]} | {artist[2]}")

    def _print_albums(self, album_list):
        if not album_list:
            print("Альбомы не найдены.")
            return

        print("ID | Название | Артист ID | Год | Лейбл")
        print("-" * 65)
        for album in album_list:
            print(f"{album[0]} | {album[1]} | {album[2]} | {album[3]} | {album[4]}")

    def _add_artist(self):
        print("\n  Добавление артиста  ")
        artist_id = self._read_int("ID артиста: ")
        nickname = self._read_nonempty_string("Псевдоним: ")
        main_genre = input("Основной жанр: ").strip()
        try:
            artist = self.database.create_artist(artist_id, nickname, main_genre)
            self._print_artists([artist])
        except ValueError as error:
            print(f"Ошибка: {error}")

    def _find_artists(self):
        print("\n  Поиск артистов  ")
        print("Введите критерии поиска (пустое поле = пропустить фильтр):")
        artist_id = self._read_optional_int("ID артиста: ")
        nickname = input("Псевдоним: ").strip() or None
        main_genre = input("Основной жанр: ").strip() or None
        self._print_artists(
            self.database.select_artists(artist_id, nickname, main_genre)
        )

    def _update_artist(self):
        print("\n  Обновление артиста  ")
        artist_id = self._read_int("ID артиста для обновления: ")
        print("Введите новые значения (пустое поле = без изменений):")
        nickname = input("Новый псевдоним: ").strip() or None
        main_genre = input("Новый жанр: ").strip() or None
        try:
            artist = self.database.update_artist(artist_id, nickname, main_genre)
            self._print_artists([artist])
        except ValueError as error:
            print(f"Ошибка: {error}")

    def _delete_artist(self):
        print("\n  Удаление артиста  ")
        artist_id = self._read_int("ID артиста для удаления: ")
        try:
            self._print_artists([self.database.delete_artist(artist_id)])
        except ValueError as error:
            print(f"Ошибка: {error}")

    def _add_album(self):
        print("\n  Добавление альбома  ")
        album_id = self._read_int("ID альбома: ")
        title = self._read_nonempty_string("Название: ")
        artist_id = self._read_int("ID артиста: ")
        year = self._read_int("Год выпуска: ")
        label = input("Лейбл: ").strip()
        try:
            album = self.database.create_album(album_id, title, artist_id, year, label)
            self._print_albums([album])
        except ValueError as error:
            print(f"Ошибка: {error}")

    def _find_albums(self):
        print("\n  Поиск альбомов  ")
        print("Введите критерии поиска (пустое поле = пропустить фильтр):")
        album_id = self._read_optional_int("ID альбома: ")
        title = input("Название: ").strip() or None
        artist_id = self._read_optional_int("ID артиста: ")
        year = self._read_optional_int("Год выпуска: ")
        label = input("Лейбл: ").strip() or None
        self._print_albums(
            self.database.select_albums(album_id, title, artist_id, year, label)
        )

    def _update_album(self):
        print("\n  Обновление альбома  ")
        album_id = self._read_int("ID альбома для обновления: ")
        print("Введите новые значения (пустое поле = без изменений):")
        title = input("Новое название: ").strip() or None
        artist_id = self._read_optional_int("Новый ID артиста: ")
        year = self._read_optional_int("Новый год выпуска: ")
        label = input("Новый лейбл: ").strip() or None
        try:
            album = self.database.update_album(album_id, title, artist_id, year, label)
            self._print_albums([album])
        except ValueError as error:
            print(f"Ошибка: {error}")

    def _delete_album(self):
        print("\n  Удаление альбома  ")
        album_id = self._read_int("ID альбома для удаления: ")
        try:
            self._print_albums([self.database.delete_album(album_id)])
        except ValueError as error:
            print(f"Ошибка: {error}")

    def _artists_menu(self):
        while True:
            print("\n  Меню артистов  ")
            print("1. Добавить артиста")
            print("2. Найти артистов")
            print("3. Обновить артиста")
            print("4. Удалить артиста")
            print("5. Показать всех артистов")
            print("0. Назад")
            choice = input("Выберите действие: ").strip()
            if choice == "0":
                break

            if choice == "1":
                self._add_artist()
            elif choice == "2":
                self._find_artists()
            elif choice == "3":
                self._update_artist()
            elif choice == "4":
                self._delete_artist()
            elif choice == "5":
                self._print_artists(self.database.select_artists())
            else:
                print("Неверный ввод. Пожалуйста, выберите пункт из меню.")

    def _albums_menu(self):
        while True:
            print("\n  Меню альбомов  ")
            print("1. Добавить альбом")
            print("2. Найти альбомы")
            print("3. Обновить альбом")
            print("4. Удалить альбом")
            print("5. Показать все альбомы")
            print("0. Назад")
            choice = input("Выберите действие: ").strip()
            if choice == "0":
                break

            if choice == "1":
                self._add_album()
            elif choice == "2":
                self._find_albums()
            elif choice == "3":
                self._update_album()
            elif choice == "4":
                self._delete_album()
            elif choice == "5":
                self._print_albums(self.database.select_albums())
            else:
                print("Неверный ввод. Пожалуйста, выберите пункт из меню.")

    def run(self):
        while True:
            print("\nБаза данных 'Артисты и альбомы'")
            print("1. Работа с артистами")
            print("2. Работа с альбомами")
            print("0. Выход")
            choice = input("Выберите раздел: ").strip()
            if choice == "0":
                print("Выход из программы.")
                break

            if choice == "1":
                self._artists_menu()
            elif choice == "2":
                self._albums_menu()
            else:
                print("Неверный ввод. Повторите.")


def run(database=None):
    ConsoleApplication(database).run()

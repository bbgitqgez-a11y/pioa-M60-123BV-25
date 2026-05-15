from .backend.memory import (
    add_artist, find_artists, edit_artist, remove_artist,
    add_album, find_albums, edit_album, remove_album,
)


def _ask_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Ошибка: введите целое число.")


def _ask_optional_int(prompt: str) -> int | None:
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число или оставьте поле пустым.")


def _ask_nonempty_string(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: значение не может быть пустым.")


def _show_artists(artist_list: list) -> None:
    if not artist_list:
        print("Артисты не найдены.")
        return
    print(f"{'ID'} | {'Псевдоним'} | {'Жанр'}")
    print("-" * 45)
    for a in artist_list:
        print(f"{a[0]} | {a[1]} | {a[2]}")


def _show_albums(album_list: list) -> None:
    if not album_list:
        print("Альбомы не найдены.")
        return
    print(f"{'ID'} | {'Название'} | {'Артист ID'} | {'Год'} | {'Лейбл'}")
    print("-" * 65)
    for a in album_list:
        print(f"{a[0]} | {a[1]} | {a[2]} | {a[3]} | {a[4]}")


def _create_artist() -> None:
    print("\n--- Добавление артиста ---")
    artist_id = _ask_int("ID артиста: ")
    nickname = _ask_nonempty_string("Псевдоним: ")
    main_genre = input("Основной жанр: ").strip()
    try:
        _show_artists([add_artist(artist_id, nickname, main_genre)])
    except ValueError as e:
        print(f"Ошибка: {e}")


def _search_artists() -> None:
    print("\n--- Поиск артистов ---")
    print("Введите критерии поиска (пустое поле = пропустить фильтр):")
    artist_id = _ask_optional_int("ID артиста: ")
    nickname = input("Псевдоним: ").strip() or None
    main_genre = input("Основной жанр: ").strip() or None
    _show_artists(find_artists(artist_id, nickname, main_genre))


def _modify_artist() -> None:
    print("\n--- Обновление артиста ---")
    artist_id = _ask_int("ID артиста для обновления: ")
    print("Введите новые значения (пустое поле — без изменений):")
    nickname = input("Новый псевдоним: ").strip() or None
    main_genre = input("Новый жанр: ").strip() or None
    try:
        _show_artists([edit_artist(artist_id, nickname, main_genre)])
    except ValueError as e:
        print(f"Ошибка: {e}")


def _drop_artist() -> None:
    print("\n--- Удаление артиста ---")
    artist_id = _ask_int("ID артиста для удаления: ")
    try:
        _show_artists([remove_artist(artist_id)])
    except ValueError as e:
        print(f"Ошибка: {e}")


def _create_album() -> None:
    print("\n--- Добавление альбома ---")
    album_id = _ask_int("ID альбома: ")
    title = _ask_nonempty_string("Название: ")
    artist_id = _ask_int("ID артиста: ")
    year = _ask_int("Год выпуска: ")
    label = input("Лейбл: ").strip()
    try:
        _show_albums([add_album(album_id, title, artist_id, year, label)])
    except ValueError as e:
        print(f"Ошибка: {e}")


def _search_albums() -> None:
    print("\n--- Поиск альбомов ---")
    print("Введите критерии поиска (пустое поле = пропустить фильтр):")
    album_id = _ask_optional_int("ID альбома: ")
    title = input("Название: ").strip() or None
    artist_id = _ask_optional_int("ID артиста: ")
    year = _ask_optional_int("Год выпуска: ")
    label = input("Лейбл: ").strip() or None
    _show_albums(find_albums(album_id, title, artist_id, year, label))


def _modify_album() -> None:
    print("\n--- Обновление альбома ---")
    album_id = _ask_int("ID альбома для обновления: ")
    print("Введите новые значения (пустое поле — без изменений):")
    title = input("Новое название: ").strip() or None
    artist_id = _ask_optional_int("Новый ID артиста: ")
    year = _ask_optional_int("Новый год выпуска: ")
    label = input("Новый лейбл: ").strip() or None
    try:
        _show_albums([edit_album(album_id, title, artist_id, year, label)])
    except ValueError as e:
        print(f"Ошибка: {e}")


def _drop_album() -> None:
    print("\n--- Удаление альбома ---")
    album_id = _ask_int("ID альбома для удаления: ")
    try:
        _show_albums([remove_album(album_id)])
    except ValueError as e:
        print(f"Ошибка: {e}")


def _artists_menu() -> None:
    actions = {
        "1": _create_artist,
        "2": _search_artists,
        "3": _modify_artist,
        "4": _drop_artist,
        "5": lambda: _show_artists(find_artists()),
    }
    while True:
        print("\n--- Меню артистов ---")
        print("1. Добавить артиста")
        print("2. Найти артистов")
        print("3. Обновить артиста")
        print("4. Удалить артиста")
        print("5. Показать всех артистов")
        print("0. Назад")
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Неверный ввод. Пожалуйста, выберите пункт из меню.")


def _albums_menu() -> None:
    actions = {
        "1": _create_album,
        "2": _search_albums,
        "3": _modify_album,
        "4": _drop_album,
        "5": lambda: _show_albums(find_albums()),
    }
    while True:
        print("\n--- Меню альбомов ---")
        print("1. Добавить альбом")
        print("2. Найти альбомы")
        print("3. Обновить альбом")
        print("4. Удалить альбом")
        print("5. Показать все альбомы")
        print("0. Назад")
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Неверный ввод. Пожалуйста, выберите пункт из меню.")


def run() -> None:
    sections = {
        "1": _artists_menu,
        "2": _albums_menu,
    }
    while True:
        print("\n=== Музыкальная база 'Артисты и альбомы' (in-memory) ===")
        print("1. Работа с артистами")
        print("2. Работа с альбомами")
        print("0. Выход")
        choice = input("Выберите раздел: ").strip()
        if choice == "0":
            print("Выход из программы.")
            break
        section = sections.get(choice)
        if section:
            section()
        else:
            print("Неверный ввод. Повторите.")
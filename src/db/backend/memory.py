type ArtistEntry = tuple[int, str, str]
type AlbumEntry = tuple[int, str, int, int, str]

Artists: list[ArtistEntry] = []
Albums: list[AlbumEntry] = []


def _artist_exists(artist_id: int) -> bool:
    return any(entry[0] == artist_id for entry in Artists)


def add_artist(artist_id: int, nickname: str, main_genre: str) -> ArtistEntry:
    if artist_id < 0:
        raise ValueError("ID должен быть неотрицательным числом.")
    if _artist_exists(artist_id):
        raise ValueError(f"Артист с ID = {artist_id} уже существует.")
    if not nickname.strip():
        raise ValueError("Псевдоним артиста не может быть пустым.")

    entry: ArtistEntry = (artist_id, nickname.strip(), main_genre.strip())
    Artists.append(entry)
    return entry


def find_artists(
        artist_id: int | None = None,
        nickname: str | None = None,
        main_genre: str | None = None,
) -> list[ArtistEntry]:
    if artist_id is None and nickname is None and main_genre is None:
        return Artists.copy()

    return [
        e for e in Artists
        if (artist_id is None or e[0] == artist_id)
           and (nickname is None or e[1] == nickname)
           and (main_genre is None or e[2] == main_genre)
    ]


def edit_artist(
        artist_id: int,
        nickname: str | None = None,
        main_genre: str | None = None,
) -> ArtistEntry:
    for i, entry in enumerate(Artists):
        if entry[0] == artist_id:
            new_nickname = nickname.strip() if nickname is not None else entry[1]
            new_genre = main_genre.strip() if main_genre is not None else entry[2]

            if nickname is not None and not new_nickname:
                raise ValueError("Псевдоним артиста не может быть пустым.")

            modified: ArtistEntry = (artist_id, new_nickname, new_genre)
            Artists[i] = modified
            return modified

    raise ValueError(f"Артист с ID = {artist_id} не найден.")


def remove_artist(artist_id: int) -> ArtistEntry:
    if any(a[2] == artist_id for a in Albums):
        raise ValueError(
            f"Нельзя удалить артиста с id={artist_id}: сначала удалите его альбомы."
        )

    for i, entry in enumerate(Artists):
        if entry[0] == artist_id:
            return Artists.pop(i)

    raise ValueError(f"Артист с id={artist_id} не найден.")


def add_album(
        album_id: int,
        title: str,
        artist_id: int,
        release_year: int,
        label: str,
) -> AlbumEntry:
    if album_id < 0:
        raise ValueError("ID альбома должен быть положительным числом.")
    if any(e[0] == album_id for e in Albums):
        raise ValueError(f"Альбом с ID={album_id} уже существует.")
    if not _artist_exists(artist_id):
        raise ValueError(f"Артист с id={artist_id} не существует. Сначала создайте артиста.")
    if not title.strip():
        raise ValueError("Название альбома не может быть пустым.")

    entry: AlbumEntry = (album_id, title.strip(), artist_id, release_year, label.strip())
    Albums.append(entry)
    return entry


def find_albums(
        album_id: int | None = None,
        title: str | None = None,
        artist_id: int | None = None,
        release_year: int | None = None,
        label: str | None = None,
) -> list[AlbumEntry]:
    if album_id is None and title is None and artist_id is None and release_year is None and label is None:
        return Albums.copy()

    return [
        e for e in Albums
        if (album_id is None or e[0] == album_id)
           and (title is None or e[1] == title)
           and (artist_id is None or e[2] == artist_id)
           and (release_year is None or e[3] == release_year)
           and (label is None or e[4] == label)
    ]


def edit_album(
        album_id: int,
        title: str | None = None,
        artist_id: int | None = None,
        year: int | None = None,
        label: str | None = None,
) -> AlbumEntry:
    for i, entry in enumerate(Albums):
        if entry[0] == album_id:
            if artist_id is not None and not _artist_exists(artist_id):
                raise ValueError(f"Артист с id={artist_id} не существует.")

            new_title = title.strip() if title is not None else entry[1]
            new_artist_id = artist_id if artist_id is not None else entry[2]
            new_year = year if year is not None else entry[3]
            new_label = label.strip() if label is not None else entry[4]

            if title is not None and not new_title:
                raise ValueError("Название альбома не может быть пустым.")
            if year is not None and (year <= 0 or year > 2100):
                raise ValueError("Год должен быть положительным числом и не превышать 2100.")

            modified = (album_id, new_title, new_artist_id, new_year, new_label)
            Albums[i] = modified
            return modified

    raise ValueError(f"Альбом с id={album_id} не найден.")


def remove_album(album_id: int) -> AlbumEntry:
    for i, entry in enumerate(Albums):
        if entry[0] == album_id:
            return Albums.pop(i)

    raise ValueError(f"Альбом с id={album_id} не найден.")

from dataclasses import dataclass


@dataclass(frozen=True)
class ArtistRecord:
    artist_id: int
    nickname: str
    main_genre: str

    def __iter__(self):
        return iter((self.artist_id, self.nickname, self.main_genre))

    def __getitem__(self, index):
        return tuple(self)[index]

    def __len__(self):
        return 3

    def __eq__(self, other):
        return tuple(self) == other

    def __repr__(self):
        return repr(tuple(self))

    def to_dict(self):
        return {
            "artist_id": self.artist_id,
            "nickname": self.nickname,
            "main_genre": self.main_genre,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            int(data["artist_id"]),
            str(data["nickname"]),
            str(data["main_genre"]),
        )


@dataclass(frozen=True)
class AlbumRecord:
    album_id: int
    title: str
    artist_id: int
    release_year: int
    label: str

    def __iter__(self):
        return iter(
            (
                self.album_id,
                self.title,
                self.artist_id,
                self.release_year,
                self.label,
            )
        )

    def __getitem__(self, index):
        return tuple(self)[index]

    def __len__(self):
        return 5

    def __eq__(self, other):
        return tuple(self) == other

    def __repr__(self):
        return repr(tuple(self))

    def to_dict(self):
        return {
            "album_id": self.album_id,
            "title": self.title,
            "artist_id": self.artist_id,
            "release_year": self.release_year,
            "label": self.label,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            int(data["album_id"]),
            str(data["title"]),
            int(data["artist_id"]),
            int(data["release_year"]),
            str(data["label"]),
        )

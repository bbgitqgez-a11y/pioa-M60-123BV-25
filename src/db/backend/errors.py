class DuplicateIdError(ValueError):
    pass


class RecordNotFoundError(ValueError):
    pass


class ValidationError(ValueError):
    pass


class ForeignKeyError(ValueError):
    pass


class ProtectedRecordError(ValueError):
    pass


class FileDataBaseError(ValueError):
    pass

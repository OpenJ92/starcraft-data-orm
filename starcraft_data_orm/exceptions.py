class ReplayExistsError(Exception):
    """Raised when a replay already exists in the database."""

    def __init__(self, filehash):
        super().__init__(f"Replay with filehash '{filehash}' already exists.")

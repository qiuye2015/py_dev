class User:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def __str__(self) -> str:
        return self.username

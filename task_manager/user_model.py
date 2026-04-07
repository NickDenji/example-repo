class User:
    """
    A class to represent a user's username and password in the system.
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return (f"username: {self.username}\n"
                f"password: {self.password}")

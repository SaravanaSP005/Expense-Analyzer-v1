from pwdlib import PasswordHash


class PasswordService:

    def __init__(self):
        self.password_hash = PasswordHash.recommended()

    # Create a new Password Hassing for user Creating.
    def hash_password(self, password: str) -> str:
        return self.password_hash.hash(password)

    # This function using verify the password.
    def verify_password(self,plain_password: str,hashed_password: str) -> bool:

        return self.password_hash.verify(plain_password,hashed_password)

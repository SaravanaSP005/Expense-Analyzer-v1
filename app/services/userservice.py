from app.models.userdb import UserEntity
from app.crud.userrepository import UserRepository
from app.services.passwordservice import PasswordService
from app.schemas.userschema import UserCreateRequest
from app.exceptions.exceptions import ConflictException, NotFoundException, ValidationException

class UserService:

    def __init__(self, user_repository: UserRepository, password_service: PasswordService):
        self.user_repository = user_repository
        self.password_service = password_service

    def get_by_email(self, email: str, tenant_id: int) -> UserEntity | None:
        return self.user_repository.get_by_email(email, tenant_id)
    
    # login user details
    def login_user(self, email: str, password: str, tenant_id: int) -> UserEntity | None:
        loginuser = self.user_repository.get_by_email(email, tenant_id)
        if loginuser is None:
            return None

        is_password_valid = self.password_service.verify_password(password, loginuser.password_hash)

        if not is_password_valid:
            return None
        
        return loginuser

    # Create User Function
    def create_user(self, user_request: UserCreateRequest) -> UserEntity:
        existing_user = self.user_repository.get_by_email(user_request.email, user_request.tenant_id)

        if existing_user is not None:
            raise ConflictException(
                message="User email already exists",
                code="USER_EXISTS",
                field="email"
            )

        user_data = user_request.model_dump(exclude={"password", "display_name"})
        user_entity = UserEntity(**user_data)
        user_entity.displayname = user_request.display_name
        user_entity.password_hash = self.password_service.get_password_hash(user_request.password)
        
        return self.user_repository.add(user_entity)

    # User Update 
    def update_user(self, id: int, user_request: UserCreateRequest) -> UserEntity:
        existing_user = self.user_repository.first(UserEntity.id == id, UserEntity.tenant_id == user_request.tenant_id)
        if existing_user is None:
            raise NotFoundException(message="User not found", code="USER_NOT_FOUND", field="id")

        existing_by_email = self.user_repository.get_by_email(user_request.email, user_request.tenant_id)
        if existing_by_email and existing_by_email.id != id:
            raise ConflictException(
                message="User email already exists",
                code="USER_EXISTS",
                field="email"
            )

        existing_user.username = user_request.username
        existing_user.email = user_request.email
        existing_user.displayname = user_request.display_name
        
        if user_request.password:
            existing_user.password_hash = self.password_service.get_password_hash(user_request.password)
        
        return self.user_repository.add(existing_user)

from app.models.userdb import UserEntity
from app.crud.userrepository import UserRepository
from app.services.passwordservice import PasswordService
from app.schemas.userschema import UserCreateRequest
from fastapi import HTTPException, status


class UserService:

    def __init__(self,user_repository: UserRepository,password_service: PasswordService,):
        self.user_repository = user_repository
        self.password_service = password_service

    def get_by_email(self,email: str) -> UserEntity | None:

        return self.user_repository.get_by_email(email,1)

    
    #login user details
    
    def login_user(self,email:str,password : str ) -> UserEntity | None:

        loginuser = self.user_repository.get_by_email(email,1)
        if loginuser is None:
            return None

        is_password_valid = self.password_service.verify_password(password,loginuser.password_hash)

        if not is_password_valid:
            return None
        
        return loginuser


    # Create User Function

    def create_user(self,user_request : UserCreateRequest) -> UserEntity | None:
        existing_user = self.user_repository.get_by_email(user_request.email,user_request.tenant_id)

        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User email already exists",
            )

        return self.user_repository.add(user_request)

    #User Update 

    def update_user(self,user_request : UserCreateRequest) -> UserEntity | None:
            existing_user = self.user_repository.get_by_email(user_request.email,user_request.tenant_id)
    
            if existing_user is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User email already exists",
                )
    
            return self.user_repository.add(user_request)

Below is a reusable **FastAPI + Python Naming & Project Structure Standard** you can save as your team's development guideline.

 # FastAPI + Python Naming Convention & Project Structure Standard

 **Version:** 1.0\
 **Technology:** Python + FastAPI + SQLAlchemy + Pydantic\
 **Purpose:** Standardize project structure, naming conventions, API design, database entities, services, repositories, schemas, and variables.

---

 ## 1\. General Python Naming Rules

 This project follows **PEP 8** naming conventions.

 ### Naming summary

 | Item | Convention | Example |
| --- | --- | --- |
| Folder | `snake_case` | `services/` |
| Python file | `snake_case` | `user_service.py` |
| Class | `PascalCase` | `UserService` |
| Function | `snake_case` | `create_user()` |
| Method | `snake_case` | `get_by_email()` |
| Variable | `snake_case` | `user_id` |
| Boolean | `is_` / `has_` / `can_` | `is_active` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_LOGIN_ATTEMPTS` |
| Database table | `snake_case`, preferably plural | `users` |
| Database column | `snake_case` | `tenant_id` |
| SQLAlchemy Entity | `PascalCase` | `UserEntity` |
| Pydantic Request | `PascalCase` \+ `Request` | `UserCreateRequest` |
| Pydantic Response | `PascalCase` \+ `Response` | `UserResponse` |
| Router variable | `router` | `router = APIRouter()` |
| Dependency | `get_...` | `get_user_service()` |

---

 # 2\. C# / .NET Equivalent

 Developers coming from C# can use this mental mapping:

 | C# / .NET | FastAPI / Python |
| --- | --- |
| Controller | Router |
| Controller class | `APIRouter` |
| DTO | Pydantic Schema |
| Request DTO | `UserCreateRequest` |
| Response DTO | `UserResponse` |
| Entity | SQLAlchemy Model |
| Entity Framework | SQLAlchemy |
| DbContext | SQLAlchemy Session |
| Repository | Repository |
| Service | Service |
| Dependency Injection | `Depends()` |
| AutoMapper | Pydantic `model_validate()` |
| appsettings.json | Pydantic Settings |
| Middleware | FastAPI Middleware |

 Example:

 ### C#

```
UserController.cs
UserService.cs
UserRepository.cs
UserDto.cs
```

 ### FastAPI

```
user_router.py
user_service.py
user_repository.py
user_schema.py
```

---

 # 3\. Recommended Project Structure

 The recommended application structure is:

```
web-api/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   │
│   ├── dependencies/
│   │   └── services.py
│   │
│   ├── models/
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── tenant.py
│   │   ├── product.py
│   │   ├── expense_config.py
│   │   ├── expense_list.py
│   │   └── expense_details.py
│   │
│   ├── repositories/
│   │   ├── user_repository.py
│   │   ├── tenant_repository.py
│   │   ├── product_repository.py
│   │   └── expense_repository.py
│   │
│   ├── services/
│   │   ├── user_service.py
│   │   ├── tenant_service.py
│   │   ├── product_service.py
│   │   ├── expense_service.py
│   │   ├── token_service.py
│   │   └── password_service.py
│   │
│   ├── schemas/
│   │   ├── base_schema.py
│   │   ├── auth_schema.py
│   │   ├── user_schema.py
│   │   ├── tenant_schema.py
│   │   ├── product_schema.py
│   │   └── expense_schema.py
│   │
│   ├── routers/
│   │   ├── auth_router.py
│   │   ├── user_router.py
│   │   ├── tenant_router.py
│   │   ├── product_router.py
│   │   └── expense_router.py
│   │
│   └── exceptions/
│       └── handlers.py
│
├── tests/
│   ├── test_auth.py
│   ├── test_users.py
│   └── test_tenants.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

 # 4\. Router Naming

 FastAPI does not use controllers in the same way as ASP.NET Core.

 Use `router`.

 ### File

```
user_router.py
```

 ### Router

```
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)
```

 ### Endpoint

```
@router.post("")
def create_user():
    ...
```

 Do not use:

```
UserController.py
userController.py
User_Controller.py
```

 Prefer:

```
user_router.py
```

---

 # 5\. Router Responsibilities

 A router should handle HTTP-related concerns:

 - Request data
- Response data
- HTTP status codes
- Dependency injection
- Authentication dependencies
- Calling services

 A router should **not contain complex business logic**.

 Example:

```
@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    request: LoginRequest,
    user_service: UserService = Depends(get_user_service),
    token_service: TokenService = Depends(get_token_service),
):
    user = user_service.login_user(
        request.email,
        request.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = token_service.create_access_token(
        user.id,
        user.tenant_id,
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        tenant_id=user.tenant_id,
    )
```

---

 # 6\. Service Naming

 Service files use `snake_case`.

```
user_service.py
tenant_service.py
product_service.py
token_service.py
password_service.py
```

 Classes use `PascalCase`.

```
class UserService:
    ...

class TenantService:
    ...

class TokenService:
    ...

class PasswordService:
    ...
```

 Methods use `snake_case`.

```
def create_user():
    ...

def get_user_by_id():
    ...

def login_user():
    ...

def update_user():
    ...
```

---

 # 7\. Service Responsibilities

 Services contain **business logic**.

 Example:

```
class UserService:

    def __init__(
        self,
        user_repository: UserRepository,
        password_service: PasswordService,
    ):
        self.user_repository = user_repository
        self.password_service = password_service

    def login_user(
        self,
        email: str,
        password: str,
    ) -> UserEntity | None:

        user = self.user_repository.get_by_email(email)

        if user is None:
            return None

        is_valid = self.password_service.verify_password(
            password,
            user.password_hash,
        )

        if not is_valid:
            return None

        return user
```

 The service should not be responsible for HTTP response formatting.

---

 # 8\. Repository Naming

 Repository files:

```
user_repository.py
tenant_repository.py
product_repository.py
expense_repository.py
```

 Repository classes:

```
class UserRepository:
    ...

class TenantRepository:
    ...

class ProductRepository:
    ...
```

 Common repository methods:

```
def get_by_id():
    ...

def get_by_email():
    ...

def get_all():
    ...

def create():
    ...

def update():
    ...

def delete():
    ...
```

---

 # 9\. Repository Responsibilities

 Repositories should handle database operations.

 Example:

```
class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(
        self,
        email: str,
    ) -> UserEntity | None:

        stmt = select(UserEntity).where(
            UserEntity.email == email
        )

        return self.db.scalar(stmt)
```

 Avoid putting business rules in repositories.

 For example, password verification belongs in a service, not a repository.

---

 # 10\. SQLAlchemy Entity Naming

 SQLAlchemy entities use `PascalCase`.

 Recommended:

```
class UserEntity(BaseEntity):
    ...

class TenantEntity(BaseEntity):
    ...

class ProductEntity(BaseEntity):
    ...

class ExpenseListEntity(BaseEntity):
    ...
```

 The `Entity` suffix is optional, but if your project uses it, use it consistently.

---

 # 11\. Database Table Naming

 Database tables should use `snake_case`.

 Prefer plural names:

```
class UserEntity(BaseEntity):
    __tablename__ = "users"
```

```
class TenantEntity(BaseEntity):
    __tablename__ = "tenants"
```

```
class ProductEntity(BaseEntity):
    __tablename__ = "products"
```

```
class ExpenseListEntity(BaseEntity):
    __tablename__ = "expense_lists"
```

 Foreign keys must match the actual table names:

```
tenant_id: Mapped[int] = mapped_column(
    ForeignKey("tenants.id"),
    nullable=False,
)
```

```
user_id: Mapped[int] = mapped_column(
    ForeignKey("users.id"),
    nullable=False,
)
```

---

 # 12\. Database Column Naming

 Always use `snake_case`.

 Correct:

```
tenant_id
user_id
create_user_id
created_at
updated_at
password_hash
contact_number
display_name
expense_config_id
product_id
```

 Avoid:

```
tenantId
userId
createUserId
createdAt
passwordHash
```

---

 # 13\. SQLAlchemy Relationships

 Many-to-one relationships should generally use a singular name:

```
tenant: Mapped["TenantEntity"] = relationship()

product: Mapped["ProductEntity"] = relationship()

create_user: Mapped["UserEntity"] = relationship()
```

 One-to-many relationships should generally use a plural name:

```
expense_details: Mapped[list["ExpenseDetails"]] = relationship(
    back_populates="expense_list"
)
```

 Bidirectional relationships should use matching `back_populates`.

 Example:

```
# ExpenseListEntity

expense_details: Mapped[list["ExpenseDetails"]] = relationship(
    back_populates="expense_list"
)
```

```
# ExpenseDetails

expense_list: Mapped["ExpenseListEntity"] = relationship(
    back_populates="expense_details"
)
```

---

 # 14\. Pydantic Schema Naming

 Pydantic schemas use `PascalCase`.

 Request:

```
class UserCreateRequest(BaseRequest):
    username: str
    password: str
    email: EmailStr
```

 Response:

```
class UserResponse(BaseResponse):
    id: int
    username: str
    email: EmailStr
```

 Login:

```
class LoginRequest(BaseRequest):
    email: EmailStr
    password: str

class LoginResponse(BaseResponse):
    access_token: str
    token_type: str
    user_id: int
    tenant_id: int
```

---

 # 15\. Request vs Response

 Use clear suffixes.

 ### Create

```
UserCreateRequest
```

 ### Update

```
UserUpdateRequest
```

 ### Response

```
UserResponse
```

 ### List response

 If required:

```
UserListResponse
```

 ### Login

```
LoginRequest
LoginResponse
```

 Avoid mixing:

```
UserDto
UserDTO
UserRequestDto
UserSchema
UserResponseDto
```

 Choose one standard and use it throughout the project.

 Recommended:

```
Request
Response
```

---

 # 16\. Pydantic ORM Mapping

 When returning SQLAlchemy entities, use Pydantic's attribute-based validation.

```
from pydantic import ConfigDict

class UserResponse(BaseResponse):
    id: int
    username: str
    email: EmailStr
    tenant_id: int

    model_config = ConfigDict(
        from_attributes=True
    )
```

 Then:

```
return UserResponse.model_validate(user)
```

 This avoids manually mapping every property:

```
UserResponse(
    id=user.id,
    username=user.username,
    email=user.email,
    tenant_id=user.tenant_id,
)
```

---

 # 17\. Variable Naming

 Variables must use `snake_case`.

 Correct:

```
user
user_id
tenant_id
access_token
password_hash
user_repository
token_service
password_service
login_user
```

 Incorrect:

```
userId
tenantId
accessToken
passwordHash
userRepository
tokenService
```

---

 # 18\. Function and Method Naming

 Functions and methods use `snake_case`.

 Correct:

```
def create_user():
    ...

def get_user_by_id():
    ...

def get_by_email():
    ...

def login_user():
    ...

def create_access_token():
    ...
```

 Incorrect:

```
def CreateUser():
    ...

def createUser():
    ...

def Create_User():
    ...
```

---

 # 19\. Boolean Naming

 Boolean variables should clearly communicate true/false.

 Recommended prefixes:

```
is_
has_
can_
should_
```

 Examples:

```
is_active
is_valid
is_verified
has_permission
has_access
can_login
```

 Example:

```
is_valid = password_service.verify_password(
    password,
    user.password_hash,
)

if not is_valid:
    return None
```

---

 # 20\. Constants

 Constants use `UPPER_SNAKE_CASE`.

```
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
MAX_LOGIN_ATTEMPTS = 5
```

 Pydantic Settings fields are normally lowercase snake\_case:

```
class Settings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
```

---

 # 21\. Dependency Naming

 Dependency provider functions should use `get_`.

 Example:

```
def get_user_service():
    ...

def get_token_service():
    ...

def get_password_service():
    ...
```

 Example:

```
def get_user_service(
    db: Session = Depends(get_db),
    password_service: PasswordService = Depends(
        get_password_service
    ),
) -> UserService:

    user_repository = UserRepository(db)

    return UserService(
        user_repository=user_repository,
        password_service=password_service,
    )
```

---

 # 22\. Password Service

 Password-related functionality should be isolated.

 File:

```
password_service.py
```

 Class:

```
class PasswordService:

    def hash_password(
        self,
        password: str,
    ) -> str:
        ...

    def verify_password(
        self,
        password: str,
        password_hash: str,
    ) -> bool:
        ...
```

 Use:

```
hash_password()
```

 during user creation.

 Use:

```
verify_password()
```

 during login.

 Never store plain-text passwords.

---

 # 23\. Token Service

 JWT functionality should be isolated.

 File:

```
token_service.py
```

 Class:

```
class TokenService:

    def create_access_token(
        self,
        user_id: int,
        tenant_id: int,
    ) -> str:
        ...
```

 The router should not contain JWT implementation details.

---

 # 24\. API URL Naming

 Use REST-style resource names.

 Recommended:

```
POST   /users
GET    /users
GET    /users/{user_id}
PUT    /users/{user_id}
PATCH  /users/{user_id}
DELETE /users/{user_id}
```

 Authentication:

```
POST /auth/login
POST /auth/logout
POST /auth/refresh
```

 Avoid:

```
POST /createUser
POST /getUser
POST /users/create
GET  /getAllUsers
```

---

 # 25\. HTTP Status Codes

 Use appropriate HTTP status codes.

 | Situation | Status |
| --- | --- |
| Successful GET | `200` |
| Successful POST | `201` |
| Successful DELETE | `204` |
| Bad request | `400` |
| Authentication failed | `401` |
| Permission denied | `403` |
| Resource not found | `404` |
| Conflict | `409` |
| Validation error | `422` |
| Server error | `500` |

 Example:

```
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid email or password",
)
```

---

 # 26\. Exception Handling

 Expected business/API errors can use `HTTPException`.

 Example:

```
if user is None:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
    )
```

 For larger applications, unexpected exceptions should preferably be handled by global exception handlers rather than adding:

```
try:
    ...
except Exception:
    ...
```

 to every endpoint.

 Recommended structure:

```
exceptions/
└── handlers.py
```

---

 # 27\. Import Naming

 Group imports in this order:

```
# Python standard library
from datetime import datetime
from decimal import Decimal

# Third-party libraries
from fastapi import APIRouter, Depends
from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Application imports
from app.models.basedb import BaseEntity
from app.services.user_service import UserService
```

 Avoid random import ordering.

---

 # 28\. Circular Model Imports

 For SQLAlchemy models that reference each other, `TYPE_CHECKING` can help avoid circular imports.

 Example:

```
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import UserEntity
    from app.models.tenant import TenantEntity
```

 Then:

```
user: Mapped["UserEntity"] = relationship()
tenant: Mapped["TenantEntity"] = relationship()
```

 This is especially useful in projects with many related entities.

---

 # 29\. Complete User Example

 ### Model

```
class UserEntity(BaseEntity):
    __tablename__ = "users"

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id"),
        nullable=False,
    )

    username: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    display_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
```

 ### Schema

```
class UserCreateRequest(BaseRequest):
    username: str
    password: str
    email: EmailStr
    display_name: str
    tenant_id: int

class UserResponse(BaseResponse):
    id: int
    username: str
    email: EmailStr
    display_name: str
    tenant_id: int

    model_config = ConfigDict(
        from_attributes=True
    )
```

 ### Repository

```
class UserRepository:

    def get_by_email(
        self,
        email: str,
    ) -> UserEntity | None:
        ...

    def create(
        self,
        user: UserEntity,
    ) -> UserEntity:
        ...
```

 ### Service

```
class UserService:

    def create_user(
        self,
        request: UserCreateRequest,
    ) -> UserEntity:
        ...

    def login_user(
        self,
        email: str,
        password: str,
    ) -> UserEntity | None:
        ...
```

 ### Router

```
router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    request: UserCreateRequest,
    user_service: UserService = Depends(
        get_user_service
    ),
):
    user = user_service.create_user(request)

    return UserResponse.model_validate(user)
```

---

 # 30\. Final Recommended Standard

 For this project, use the following rules consistently:

```
Folders       → snake_case
Files         → snake_case
Classes       → PascalCase
Functions     → snake_case
Methods       → snake_case
Variables     → snake_case
Booleans      → is_/has_/can_
Constants     → UPPER_SNAKE_CASE

Entities      → PascalCase + Entity
Schemas       → PascalCase + Request/Response
Services      → PascalCase + Service
Repositories  → PascalCase + Repository
Routers       → APIRouter + router variable

DB tables     → snake_case, preferably plural
DB columns    → snake_case
API URLs      → lowercase REST resources
Dependencies  → get_...
```

 ### Golden rule

 **Python code:**

```
snake_case
```

 **Python classes:**

```
PascalCase
```

 **Database:**

```
snake_case
```

 **API paths:**

```
lowercase / plural / REST-style
```

 Following this consistently will give your FastAPI project a clean, professional Python structure while preserving the familiar **Controller → Service → Repository → Entity/DTO** architecture from C#.
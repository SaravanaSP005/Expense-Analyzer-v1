**1\. Recommended Structure for Your Existing Project**

 Your current structure is:

```
app/
├── api/
├── core/
├── crud/
├── dependencies/
├── models/
├── schemas/
├── services/
├── main.py
└── ...
```

 You do **not** need a large restructuring.

 Add only these two directories:

```
app/
├── api/
├── core/
├── crud/
├── dependencies/
├── exceptions/          # NEW
│   ├── __init__.py
│   └── exceptions.py
├── handlers/            # NEW
│   ├── __init__.py
│   └── exception_handler.py
├── models/
├── schemas/
├── services/
├── main.py
└── ...
```

 I recommend this architecture:

```
Router
   ↓
Service
   ↓
CRUD / Repository
   ↓
Database

Exception
   ↓
Global Exception Handler
   ↓
Standard API Response
```

---

 **2\. Your Standard Response Format**

 Use one consistent format for both success and error responses.

 ### Error

```
{
  "success": false,
  "statusCode": 404,
  "message": "Expense list not found",
  "data": null,
  "errors": [
    {
      "code": "RESOURCE_NOT_FOUND",
      "field": "expense_id",
      "message": "Expense list not found"
    }
  ]
}
```

 ### Validation Error

```
{
  "success": false,
  "statusCode": 422,
  "message": "Validation error",
  "data": null,
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "field": "email",
      "message": "Email is required"
    }
  ]
}
```

 ### Success

```
{
  "success": true,
  "statusCode": 200,
  "message": "Expense updated successfully",
  "data": {
    "id": 10,
    "active": false
  },
  "errors": []
}
```

---

 **3\. Create Your Common Response Schema**

 Create:

```
app/schemas/response.py
```

 Put this code inside:

```
from typing import Generic, TypeVar

from pydantic import BaseModel
from typing import Optional

T = TypeVar("T")

class ErrorDetail(BaseModel):
    code: str
    field: Optional[str] = None
    message: str

class APIResponse(BaseModel, Generic[T]):
    success: bool
    statusCode: int
    message: str
    data: Optional[T] = None
    errors: list[ErrorDetail] = []
```

 Now you have one common response model.

---

 **4\. Create Custom Exceptions**

 Create:

```
app/exceptions/__init__.py
```

 It can be empty.

 Then create:

```
app/exceptions/exceptions.py
```

 Put:

```
class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        message: str,
        code: str,
        field: str | None = None,
    ):
        self.status_code = status_code
        self.message = message
        self.code = code
        self.field = field

        super().__init__(message)

class BadRequestException(AppException):
    def __init__(
        self,
        message: str = "Invalid request",
        code: str = "BAD_REQUEST",
        field: str | None = None,
    ):
        super().__init__(
            status_code=400,
            message=message,
            code=code,
            field=field,
        )

class UnauthorizedException(AppException):
    def __init__(
        self,
        message: str = "Authentication required",
        code: str = "UNAUTHORIZED",
        field: str | None = None,
    ):
        super().__init__(
            status_code=401,
            message=message,
            code=code,
            field=field,
        )

class ForbiddenException(AppException):
    def __init__(
        self,
        message: str = "You do not have permission",
        code: str = "FORBIDDEN",
        field: str | None = None,
    ):
        super().__init__(
            status_code=403,
            message=message,
            code=code,
            field=field,
        )

class NotFoundException(AppException):
    def __init__(
        self,
        message: str = "Resource not found",
        code: str = "RESOURCE_NOT_FOUND",
        field: str | None = None,
    ):
        super().__init__(
            status_code=404,
            message=message,
            code=code,
            field=field,
        )

class ConflictException(AppException):
    def __init__(
        self,
        message: str = "Resource conflict",
        code: str = "CONFLICT",
        field: str | None = None,
    ):
        super().__init__(
            status_code=409,
            message=message,
            code=code,
            field=field,
        )

class ValidationException(AppException):
    def __init__(
        self,
        message: str = "Validation error",
        code: str = "VALIDATION_ERROR",
        field: str | None = None,
    ):
        super().__init__(
            status_code=422,
            message=message,
            code=code,
            field=field,
        )
```

---

 **5\. Why Create These Exceptions?**

 Instead of writing this everywhere:

```
raise HTTPException(
    status_code=404,
    detail="Expense list not found"
)
```

 you can write:

```
raise NotFoundException(
    message="Expense list not found",
    code="EXPENSE_NOT_FOUND",
    field="expense_id",
)
```

 Your service does not need to construct the HTTP response.

 The exception handler will do that.

---

 **6\. Create Global Exception Handler**

 Create:

```
app/handlers/__init__.py
```

 This can be empty.

 Then:

```
app/handlers/exception_handler.py
```

 Put:

```
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.exceptions.exceptions import AppException

async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "statusCode": exc.status_code,
            "message": exc.message,
            "data": None,
            "errors": [
                {
                    "code": exc.code,
                    "field": exc.field,
                    "message": exc.message,
                }
            ],
        },
    )
```

---

 **7\. Handle FastAPI Validation Errors**

 FastAPI/Pydantic can automatically generate validation errors.

 For example:

```
class ExpenseRequest(BaseModel):
    email: EmailStr
```

 If the client sends invalid data, FastAPI raises `RequestValidationError`.

 Add this to:

```
app/handlers/exception_handler.py
```

```
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    errors = []

    for error in exc.errors():
        location = error.get("loc", [])

        field = ".".join(
            str(item)
            for item in location
            if item != "body"
        )

        errors.append(
            {
                "code": "VALIDATION_ERROR",
                "field": field,
                "message": error.get("msg", "Invalid value"),
            }
        )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "statusCode": 422,
            "message": "Validation error",
            "data": None,
            "errors": errors,
        },
    )
```

---

 **8\. Handle Unexpected Errors**

 You should also have a handler for unexpected errors.

 Add:

```
async def generic_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "statusCode": 500,
            "message": "Internal server error",
            "data": None,
            "errors": [
                {
                    "code": "INTERNAL_SERVER_ERROR",
                    "field": None,
                    "message": "An unexpected error occurred",
                }
            ],
        },
    )
```

 **Important:** Don't return the actual Python exception to the client in production.

 Don't do:

```
"message": str(exc)
```

 because database/internal information could be exposed.

 Log the real exception on the server instead.

---

 **9\. Register the Exception Handlers**

 Your:

```
app/main.py
```

 currently exists.

 Change it to something like:

```
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.exceptions.exceptions import AppException
from app.handlers.exception_handler import (
    app_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)

app = FastAPI()

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    Exception,
    generic_exception_handler,
)
```

 Your existing routers can then be included as usual:

```
app.include_router(expense_router)
```

---

 **10\. How Your Service Should Use It**

 Now your service becomes very clean.

 For example:

```
app/services/expense_service.py
```

```
from datetime import datetime, timezone

from app.exceptions.exceptions import (
    NotFoundException,
    ConflictException,
)

def disable(
    self,
    tenant_id: int,
    id: int,
    active: bool,
):

    expense_list = self.expense_repository.first(
        ExpenseListEntity.tenant_id == tenant_id,
        ExpenseListEntity.id == id,
    )

    if expense_list is None:
        raise NotFoundException(
            message="Expense list not found",
            code="EXPENSE_NOT_FOUND",
            field="id",
        )

    if expense_list.active == active:
        raise ConflictException(
            message="Expense list is already in the requested state",
            code="EXPENSE_ALREADY_IN_STATE",
            field="active",
        )

    now = datetime.now(timezone.utc)

    expense_list.active = active
    expense_list.last_modified = now

    for item in expense_list.expense_details:
        item.active = active
        item.last_modified = now

    self.db.commit()
    self.db.refresh(expense_list)

    return expense_list
```

 Notice there is **no `HTTPException` here**.

---

 **11\. How Your Router Should Look**

 Your router should be simple.

 For example:

```
app/api/expense.py
```

```
from fastapi import APIRouter, Depends, status

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
)

@router.patch(
    "/{expense_id}/status",
    status_code=status.HTTP_200_OK,
)
def disable_expense(
    expense_id: int,
    active: bool,
    service: ExpenseService = Depends(
        get_expense_service
    ),
):
    return service.disable(
        tenant_id=1,
        id=expense_id,
        active=active,
    )
```

 That's it.

 You don't need:

```
try:
    ...
except:
    ...
```

 in every router.

---

 **12\. Complete Request → Error Flow**

 For:

```
PATCH /expenses/100/status?active=false
```

 the flow is:

```
Router
   ↓
Service
   ↓
Repository
   ↓
Database
```

 Suppose the database doesn't find ID `100`.

 Repository returns:

```
None
```

 Service:

```
if expense_list is None:
    raise NotFoundException(
        message="Expense list not found",
        code="EXPENSE_NOT_FOUND",
        field="id",
    )
```

 Exception goes to:

```
Global Exception Handler
```

 Handler generates:

```
{
  "success": false,
  "statusCode": 404,
  "message": "Expense list not found",
  "data": null,
  "errors": [
    {
      "code": "EXPENSE_NOT_FOUND",
      "field": "id",
      "message": "Expense list not found"
    }
  ]
}
```

 HTTP status:

```
404 Not Found
```

---

 **13\. When Should You Use `HTTPException`?**

 With the architecture above:

 ### Router

 You can use:

```
HTTPException
```

 for HTTP-specific concerns.

 For example, authentication/dependency handling.

 ### Service

 Prefer:

```
NotFoundException
ConflictException
BadRequestException
ForbiddenException
```

 instead of:

```
HTTPException
```

 ### Repository

 Do not normally use:

```
HTTPException
```

 The repository should not know about HTTP.

---

 **14\. Try/Except — Which Layer?**

 Use `try/except` where you can actually handle the error.

 ### Database transaction

 Service/repository transaction boundary:

```
try:
    expense_list.active = active

    self.db.commit()

except SQLAlchemyError:
    self.db.rollback()
    raise
```

 This is correct because you need:

```
self.db.rollback()
```

---

 **15\. Handling Specific Database Errors**

 For example, duplicate data:

```
from sqlalchemy.exc import IntegrityError

try:
    self.db.commit()

except IntegrityError:
    self.db.rollback()

    raise ConflictException(
        message="Expense already exists",
        code="EXPENSE_ALREADY_EXISTS",
    )
```

 The flow becomes:

```
Database
   ↓
IntegrityError
   ↓
Service
   ↓
ConflictException
   ↓
Global Handler
   ↓
409 Conflict
```

 Response:

```
{
  "success": false,
  "statusCode": 409,
  "message": "Expense already exists",
  "data": null,
  "errors": [
    {
      "code": "EXPENSE_ALREADY_EXISTS",
      "field": null,
      "message": "Expense already exists"
    }
  ]
}
```

---

 **16\. Don't Do This**

 Avoid:

```
try:
    ...
except Exception as e:
    return {
        "success": false,
        "message": str(e)
    }
```

 Also avoid:

```
try:
    ...
except Exception:
    raise HTTPException(
        status_code=500,
        detail="Something went wrong"
    )
```

 everywhere.

 You will hide programming errors and make debugging difficult.

---

 **17\. Correct `try/except` Pattern**

 Use:

```
try:
    # database operation

except IntegrityError:
    self.db.rollback()

    raise ConflictException(
        message="Duplicate data",
        code="DUPLICATE_DATA",
    )

except SQLAlchemyError:
    self.db.rollback()

    raise
```

 The important part is:

```
raise
```

 You're not swallowing the exception.

 Your global handler can deal with the unexpected error.

---

 # **18\. HTTP Status Code Guide**

 Here is the practical list you should use in your application.

 | Status | Name | When to use | Example |
| --- | --- | --- | --- |
| `200` | OK | Successful GET/update | Expense updated |
| `201` | Created | New resource created | User created |
| `202` | Accepted | Request accepted for async processing | Report generation started |
| `204` | No Content | Success with no response body | Delete successful |
| `400` | Bad Request | Request is invalid | Invalid operation |
| `401` | Unauthorized | Authentication missing/invalid | Invalid token |
| `403` | Forbidden | Authenticated but no permission | User cannot delete |
| `404` | Not Found | Resource doesn't exist | Expense not found |
| `405` | Method Not Allowed | HTTP method isn't supported | POST on GET-only endpoint |
| `409` | Conflict | Request conflicts with resource state | Duplicate email |
| `415` | Unsupported Media Type | Unsupported request format | Wrong Content-Type |
| `422` | Unprocessable Content | Input validation failure | Invalid email |
| `429` | Too Many Requests | Rate limit exceeded | Too many requests |
| `500` | Internal Server Error | Unexpected application error | Unhandled exception |
| `502` | Bad Gateway | Invalid response from upstream service | External API failure |
| `503` | Service Unavailable | Service temporarily unavailable | Database/service unavailable |
| `504` | Gateway Timeout | Upstream service timed out | External API timeout |

For your normal CRUD application, you'll probably use:

```
200
201
204
400
401
403
404
409
422
500
503
```

 most frequently.

---

 # **19\. Status Code Examples**

 ### `200` — Successful update

```
@router.patch(
    "/{id}",
    status_code=200
)
```

 Response:

```
{
  "success": true,
  "statusCode": 200,
  "message": "Expense updated successfully",
  "data": {},
  "errors": []
}
```

---

 ### `201` — Created

```
@router.post(
    "/",
    status_code=201
)
```

 Response:

```
{
  "success": true,
  "statusCode": 201,
  "message": "Expense created successfully",
  "data": {},
  "errors": []
}
```

---

 ### `204` — Delete with no body

 Use when you intentionally return no response body:

```
@router.delete(
    "/{id}",
    status_code=204
)
```

 Don't return your standard JSON body with `204`.

---

 ### `400` — Bad request

```
raise BadRequestException(
    message="Invalid expense request",
    code="INVALID_EXPENSE_REQUEST",
)
```

---

 ### `401` — Authentication

```
raise UnauthorizedException(
    message="Invalid or expired token",
    code="INVALID_TOKEN",
)
```

---

 ### `403` — Permission

```
raise ForbiddenException(
    message="You do not have permission to update this expense",
    code="EXPENSE_UPDATE_FORBIDDEN",
)
```

---

 ### `404` — Not found

 Your case:

```
if expense_list is None:
    raise NotFoundException(
        message="Expense list not found",
        code="EXPENSE_NOT_FOUND",
        field="id",
    )
```

---

 ### `409` — Conflict

```
if existing_expense:
    raise ConflictException(
        message="Expense already exists",
        code="EXPENSE_ALREADY_EXISTS",
        field="name",
    )
```

---

 ### `422` — Validation

 Usually let FastAPI/Pydantic handle this automatically.

 For example:

```
class ExpenseRequest(BaseModel):
    amount: float
```

 Invalid request:

```
{
  "amount": "abc"
}
```

 FastAPI generates a validation exception, and your global handler converts it to your standard format.

---

 ### `500` — Unexpected error

 You generally **don't manually raise this for normal business logic**.

 Something unexpected happens:

```
raise RuntimeError(...)
```

 or an unhandled database/programming error occurs.

 Your global handler returns:

```
{
  "success": false,
  "statusCode": 500,
  "message": "Internal server error",
  "data": null,
  "errors": [
    {
      "code": "INTERNAL_SERVER_ERROR",
      "field": null,
      "message": "An unexpected error occurred"
    }
  ]
}
```

---

 # **20\. Which Status Code Should You Choose?**

 Use this decision table:

 | Question | Status |
| --- | --- |
| Did the request succeed? | `200` |
| Did I create something? | `201` |
| Did I succeed with no response body? | `204` |
| Is the request itself invalid? | `400` |
| Is authentication missing/invalid? | `401` |
| Is the user authenticated but not allowed? | `403` |
| Does the requested resource not exist? | `404` |
| Does the operation conflict with existing state/data? | `409` |
| Did request schema validation fail? | `422` |
| Did an unexpected error occur? | `500` |
| Is a dependency temporarily unavailable? | `503` |

---

 # **21\. Error Code vs HTTP Status Code**

 These are different things.

 HTTP status:

```
404
```

 tells the client the **general HTTP category**.

 Your application error code:

```
EXPENSE_NOT_FOUND
```

 tells the client **exactly what happened**.

 Therefore:

```
{
  "success": false,
  "statusCode": 404,
  "message": "Expense list not found",
  "data": null,
  "errors": [
    {
      "code": "EXPENSE_NOT_FOUND",
      "field": "id",
      "message": "Expense list not found"
    }
  ]
}
```

 Think:

```
HTTP status
    ↓
404

Application error code
    ↓
EXPENSE_NOT_FOUND
```

 This is very useful for frontend applications.

---

 # **22\. Your Final Folder Structure**

 Based on your current project, I recommend:

```
app/
│
├── api/
│   ├── __init__.py
│   └── expense.py
│
├── core/
│   ├── config.py
│   └── database.py
│
├── crud/
│   ├── __init__.py
│   └── expense.py
│
├── dependencies/
│   └── ...
│
├── exceptions/
│   ├── __init__.py
│   └── exceptions.py
│
├── handlers/
│   ├── __init__.py
│   └── exception_handler.py
│
├── models/
│   └── expense.py
│
├── schemas/
│   ├── expense.py
│   └── response.py
│
├── services/
│   ├── __init__.py
│   └── expense_service.py
│
└── main.py
```

---

 # **23\. Final Responsibility Guide**

 Keep this as your project rule:

```
┌──────────────────────────────────────┐
│              ROUTER                  │
│                                      │
│  - HTTP request                      │
│  - Query/path/body                   │
│  - Authentication dependencies       │
│  - Call Service                      │
│  - HTTP status for successful call   │
└─────────────────┬────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────┐
│              SERVICE                 │
│                                      │
│  - Business logic                    │
│  - Business validation               │
│  - Raise custom exceptions           │
│  - Transaction handling              │
└─────────────────┬────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────┐
│             CRUD / REPOSITORY        │
│                                      │
│  - SELECT                             │
│  - INSERT                             │
│  - UPDATE                             │
│  - DELETE                             │
│  - Database operations               │
└─────────────────┬────────────────────┘
                  │
                  ▼
             DATABASE
```

 Errors:

```
Service
   │
   │ raise NotFoundException
   ▼
Global Exception Handler
   │
   ▼
HTTP 404
   │
   ▼
Standard JSON Response
```

---

 # **24\. The Pattern You Should Use Going Forward**

 For your current project, use this pattern:

 ### Router

```
return service.disable(...)
```

 ### Service

```
if expense is None:
    raise NotFoundException(
        message="Expense not found",
        code="EXPENSE_NOT_FOUND",
        field="id",
    )
```

 ### Database error

```
try:
    self.db.commit()

except IntegrityError:
    self.db.rollback()

    raise ConflictException(
        message="Expense already exists",
        code="EXPENSE_ALREADY_EXISTS",
    )

except SQLAlchemyError:
    self.db.rollback()
    raise
```

 ### Global handler

 Converts:

```
NotFoundException
       ↓
404
```

```
ConflictException
       ↓
409
```

```
RequestValidationError
       ↓
422
```

```
Unexpected Exception
       ↓
500
```

 ### Client receives

 Always the same format:

```
{
  "success": false,
  "statusCode": 404,
  "message": "Expense not found",
  "data": null,
  "errors": [
    {
      "code": "EXPENSE_NOT_FOUND",
      "field": "id",
      "message": "Expense not found"
    }
  ]
}
```

 **This is the structure I recommend you adopt in your existing project.** You don't need to put `try/except` in every Router or Service method; use `raise` for expected application/business errors, handle database exceptions where rollback/translation is needed, and let the global exception handler produce the final HTTP response.
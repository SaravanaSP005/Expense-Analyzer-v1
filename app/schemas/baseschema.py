from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseResponse(BaseModel):
    id: int
    active: bool
    create_datetime: datetime
    create_user_id: int | None
    last_user_id: int | None
    last_modified: datetime | None
    row_version: int

    model_config = ConfigDict(
        from_attributes=True
    )

class BaseRequest(BaseModel):
    id: int
    active: bool
    create_datetime: datetime
    create_user_id: int | None
    last_user_id: int | None
    last_modified: datetime | None
    row_version: int

    model_config = ConfigDict(
        from_attributes=True
    )

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True


class ProjectResponse(BaseModel):
    id: int
    name: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    # user: Optional[UserResponse]  # リレーション

    class Config:
        from_attributes = True


class RunResponse(BaseModel):
    id: int
    project_id: int
    file_name: str
    checksum: str
    user_id: int
    added_at: datetime
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    status: str
    storage_address: str
    deleted_at: datetime | None
    # project: Optional[ProjectResponse]  # リレーション
    # user: Optional[UserResponse]  # リレーション

    class Config:
        from_attributes = True


class RunResponseWithProjectName(BaseModel):
    id: int
    project_id: int
    project_name: str
    file_name: str
    checksum: str
    user_id: int
    added_at: datetime
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    status: str
    storage_address: str
    # project: Optional[ProjectResponse]  # リレーション
    # user: Optional[UserResponse]  # リレーション

    class Config:
        from_attributes = True


class ProcessResponse(BaseModel):
    id: int
    name: str
    run_id: int
    storage_address: str

    class Config:
        from_attributes = True


class OperationResponse(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    status: str
    storage_address: str
    is_transport: bool
    is_data: bool
    log: Optional[str]
    # process: Optional["ProcessResponse"]  # リレーション
    # parent: Optional["OperationResponse"]  # 自己リレーション

    class Config:
        from_attributes = True

# # 自己参照モデルのための更新
# OperationResponse.update_forward_refs()


class OperationResponseWithProcessStorageAddress(BaseModel):
    id: int
    name: str
    process_id: int
    process_name: str
    parent_id: Optional[int]
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    status: str
    storage_address: str
    process_storage_address: str
    is_transport: bool
    log: Optional[str]
    # process: Optional["ProcessResponse"]  # リレーション
    # parent: Optional["OperationResponse"]  # 自己リレーション

    class Config:
        from_attributes = True

# # 自己参照モデルのための更新
# OperationResponse.update_forward_refs()


class EdgeResponse(BaseModel):
    id: int
    run_id: int
    from_id: int
    to_id: int
    # from_: Optional[OperationResponse]  # リレーション
    # to: Optional[OperationResponse]  # リレーション

    class Config:
        from_attributes = True
from define_db.models import Run, Project, User, Operation, Process
from define_db.database import SessionLocal
from api.response_model import RunResponse, OperationResponseWithProcessStorageAddress
from fastapi import APIRouter
from fastapi import Form
from fastapi import HTTPException
from datetime import datetime
from typing import List

router = APIRouter()


@router.post("/runs/", tags=["runs"], response_model=RunResponse)
def create(
        project_id: int = Form(),
        file_name: str = Form(),
        checksum: str = Form(),
        user_id: int = Form(),
        storage_address: str = Form()
):
    with SessionLocal() as session:
        # Check project existence
        project = session.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=400, detail=f"Project with id {project_id} not found")
        # Check user existence
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=400, detail=f"User with id {user_id} not found")
        run_to_add = Run(
            project_id=project_id,
            file_name=file_name,
            checksum=checksum,
            user_id=user_id,
            status="not started",
            added_at=datetime.now(),
            storage_address=storage_address
        )
        session.add_all([run_to_add])
        session.commit()
        session.refresh(run_to_add)
        return RunResponse.model_validate(run_to_add)


@router.get("/runs/{id}", tags=["runs"], response_model=RunResponse)
def read(id: int):
    with SessionLocal() as session:
        run = session.query(Run).filter(Run.id == id).first()
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
        return RunResponse.model_validate(run)


@router.get("/runs/{id}/operations", tags=["runs"], response_model=List[OperationResponseWithProcessStorageAddress])
def read_operations(id: int):
    with SessionLocal() as session:
        operations = session.query(
            Operation,
            Process.name.label('process_name'),
            Process.storage_address.label('process_storage_address')
        ).join(Process).filter(Process.run_id == id).all()
        return [
            {
                **operation.__dict__,
                "process_name": process_name,
                "process_storage_address": process_storage_address
            }
            for operation, process_name, process_storage_address in operations
        ]


@router.put("/runs/{id}", tags=["runs"], response_model=RunResponse)
def update(id: int, project_id: int = Form(), file_name: str = Form(), checksum: str = Form(), user_id: int = Form(), storage_address: str = Form()):
    with SessionLocal() as session:
        run = session.query(Run).filter(Run.id == id).first()
        # Check run existence
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
        # Check project existence
        project = session.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=400, detail=f"Project with id {project_id} not found")
        # Check user existence
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=400, detail=f"User with id {user_id} not found")
        run.project_id = project_id
        run.file_name = file_name
        run.checksum = checksum
        run.user_id = user_id
        run.storage_address = storage_address
        session.commit()
        session.refresh(run)
        return RunResponse.model_validate(run)


@router.patch("/runs/{id}", tags=["runs"], response_model=RunResponse)
def patch(id: int, attribute: str = Form(), new_value: str = Form()):
    with SessionLocal() as session:
        run = session.query(Run).filter(Run.id == id).first()
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
        match attribute:
            case "project_id":
                project = session.query(Project).filter(Project.id == new_value).first()
                if not project:
                    raise HTTPException(status_code=400, detail=f"Project with id {new_value} not found")
                run.project_id = new_value
            case "file_name":
                run.file_name = new_value
            case "checksum":
                run.checksum = new_value
            case "user_id":
                user = session.query(User).filter(User.id == new_value).first()
                if not user:
                    raise HTTPException(status_code=400, detail=f"User with id {new_value} not found")
                run.user_id = new_value
            case "storage_address":
                run.storage_address = new_value
            case "started_at":
                new_datetime = datetime.fromisoformat(new_value)
                run.started_at = new_datetime
            case "finished_at":
                new_datetime = datetime.fromisoformat(new_value)
                run.finished_at = new_datetime
            case "status":
                run.status = new_value
            case _:
                raise HTTPException(status_code=400, detail="Invalid attribute")
        session.commit()
        session.refresh(run)
        return RunResponse.model_validate(run)


@router.delete("/runs/{id}", tags=["runs"])
def delete(id: int):
    with SessionLocal() as session:
        run = session.query(Run).filter(Run.id == id).first()
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
        session.delete(run)
        session.commit()
        return {"detail": "Run deleted successfully"}

from define_db.models import Process, Run
from define_db.database import SessionLocal
from api.response_model import ProcessResponse
from fastapi import APIRouter
from fastapi import Form
from fastapi import HTTPException

router = APIRouter()


@router.post("/processes/", tags=["processes"], response_model=ProcessResponse)
def create(
        name: str = Form(),
        run_id: int = Form(),
        storage_address: str = Form()
):
    with SessionLocal() as session:
        # Check run existence
        run = session.query(Run).filter(Run.id == run_id).first()
        if not run:
            raise HTTPException(status_code=400, detail=f"Run with id {run_id} not found")
        process_to_add = Process(
            name=name,
            run_id=run_id,
            storage_address=storage_address
        )
        session.add_all([process_to_add])
        session.commit()
        session.refresh(process_to_add)
        return ProcessResponse.model_validate(process_to_add)


@router.get("/processes/{id}", tags=["processes"], response_model=ProcessResponse)
def read(id: int):
    with SessionLocal() as session:
        process = session.query(Process).filter(Process.id == id).first()
        if not process:
            raise HTTPException(status_code=404, detail="Process not found")
        return ProcessResponse.model_validate(process)


@router.put("/processes/{id}", tags=["processes"], response_model=ProcessResponse)
def update(
        id: int,
        name: str = Form(),
        run_id: int = Form(),
        storage_address: str = Form()
):
    with SessionLocal() as session:
        # Check process existence
        process = session.query(Process).filter(Process.id == id).first()
        if not process:
            raise HTTPException(status_code=404, detail="Process not found")
        # Check run existence
        run = session.query(Run).filter(Run.id == run_id).first()
        if not run:
            raise HTTPException(status_code=400, detail=f"Run with id {run_id} not found")
        process.name = name
        process.run_id = run_id
        process.storage_address = storage_address
        session.commit()
        session.refresh(process)
        return ProcessResponse.model_validate(process)


@router.patch("/processes/{id}", tags=["processes"], response_model=ProcessResponse)
def patch(id: int, attribute: str = Form(), new_value: str = Form()):
    with SessionLocal() as session:
        process = session.query(Process).filter(Process.id == id).first()
        if not process:
            raise HTTPException(status_code=404, detail="Process not found")
        match attribute:
            case "name":
                process.name = new_value
            case "run_id":
                # Check run existence
                run = session.query(Run).filter(Run.id == new_value).first()
                if not run:
                    raise HTTPException(status_code=400, detail=f"Run with id {new_value} not found")
                process.run_id = new_value
            case "storage_address":
                process.storage_address = new_value
            case _:
                raise HTTPException(status_code=400, detail="Invalid attribute")
        session.commit()
        session.refresh(process)
        return ProcessResponse.model_validate(process)


@router.delete("/processes/{id}", tags=["processes"])
def delete(id: int):
    with SessionLocal() as session:
        process = session.query(Process).filter(Process.id == id).first()
        if not process:
            raise HTTPException(status_code=404, detail="Process not found")
        session.delete(process)
        session.commit()
        return {"message": "Process deleted successfully"}

from define_db.models import Run, Operation, Edge
from define_db.database import SessionLocal
from api.response_model import EdgeResponse
from fastapi import APIRouter
from fastapi import Form
from fastapi import HTTPException
from typing import List

router = APIRouter()


@router.post("/edges/", tags=["edges"], response_model=EdgeResponse)
def create(
        run_id: int = Form(),
        from_id: int = Form(),
        to_id: int = Form()
):
    with SessionLocal() as session:
        # Check run existence
        run = session.query(Run).filter(Run.id == run_id).first()
        if not run:
            raise HTTPException(status_code=400, detail=f"Run with id {run_id} not found")
        # Check from operation existence
        from_operation = session.query(Operation).filter(Operation.id == from_id).first()
        if not from_operation:
            raise HTTPException(status_code=400, detail=f"From operation with id {from_id} not found")
        # Check to operation existence
        to_operation = session.query(Operation).filter(Operation.id == to_id).first()
        if not to_operation:
            raise HTTPException(status_code=400, detail=f"To operation with id {to_id} not found")
        edge_to_add = Edge(
            run_id=run_id,
            from_id=from_id,
            to_id=to_id
        )
        session.add_all([edge_to_add])
        session.commit()
        session.refresh(edge_to_add)
        return EdgeResponse.model_validate(edge_to_add)


@router.get("/edges/{id}", tags=["edges"], response_model=EdgeResponse)
def read(id: int):
    with SessionLocal() as session:
        edge = session.query(Edge).filter(Edge.id == id).first()
        if not edge:
            raise HTTPException(status_code=404, detail="Edge not found")
        return EdgeResponse.model_validate(edge)


@router.get("/edges/run/{run_id}", tags=["edges"], response_model=List[EdgeResponse])
def read_by_run_id(run_id: int):
    with SessionLocal() as session:
        edges = session.query(Edge).filter(Edge.run_id == run_id).all()
        return [EdgeResponse.model_validate(edge) for edge in edges]

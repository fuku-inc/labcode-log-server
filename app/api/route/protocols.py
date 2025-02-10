from define_db.models import Protocol, User
from define_db.database import SessionLocal
from fastapi import APIRouter
from api.response_model import ProtocolResponse
from fastapi import Form
from fastapi import HTTPException
import datetime as dt

router = APIRouter()


@router.post("/protocols/", tags=["protocols"], response_model=ProtocolResponse)
def create(user_id: int = Form(), name: str = Form(), checksum: str = Form()) -> Protocol:
    with SessionLocal() as session:
        # ユーザーの存在確認
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=400, detail=f"User with id {user_id} not found")
        protocol_to_add = Protocol(
            user_id=user_id,
            name=name,
            checksum=checksum,
            added_at=dt.datetime.now()
        )
        session.add_all([protocol_to_add])
        session.commit()
        session.refresh(protocol_to_add)
        return ProtocolResponse.model_validate(protocol_to_add)


@router.get("/protocols/{id}", tags=["protocols"], response_model=ProtocolResponse)
def read(id: int):
    with SessionLocal() as session:
        protocol = session.query(Protocol).filter(Protocol.id == id).first()
        if not protocol:
            raise HTTPException(status_code=404, detail="Protocol not found")
        return ProtocolResponse.model_validate(protocol)


@router.put("/protocols/{id}", tags=["protocols"], response_model=ProtocolResponse)
def update(id: int, user_id: int = Form(), name: str = Form(), checksum: str = Form()):
    with SessionLocal() as session:
        protocol = session.query(Protocol).filter(Protocol.id == id).first()
        if not protocol:
            raise HTTPException(status_code=404, detail="Protocol not found")
        # ユーザーの存在確認
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=400, detail=f"User with id {user_id} not found")
        protocol.user_id = user_id
        protocol.name = name
        protocol.checksum = checksum
        session.commit()
        session.refresh(protocol)
        return ProtocolResponse.model_validate(protocol)


@router.patch("/protocols/{id}", tags=["protocols"], response_model=ProtocolResponse)
def patch(id: int, attribute: str = Form(), new_value: str = Form()):
    with SessionLocal() as session:
        protocol = session.query(Protocol).filter(Protocol.id == id).first()
        if not protocol:
            raise HTTPException(status_code=404, detail="Protocol not found")
        match attribute:
            case "user_id":
                protocol.user_id = new_value
            case "name":
                protocol.name = new_value
            case "checksum":
                protocol.checksum = new_value
            case _:
                raise HTTPException(status_code=400, detail="Invalid attribute")
        session.commit()
        session.refresh(protocol)
        return ProtocolResponse.model_validate(protocol)


@router.delete("/protocols/{id}", tags=["protocols"])
def delete(id: int):
    with SessionLocal() as session:
        protocol = session.query(Protocol).filter(Protocol.id == id).first()
        if not protocol:
            raise HTTPException(status_code=404, detail="Protocol not found")
        session.delete(protocol)
        session.commit()
        return {"message": "Protocol deleted successfully"}

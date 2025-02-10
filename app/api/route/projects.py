from define_db.models import Project, User
from define_db.database import SessionLocal
from api.response_model import ProjectResponse
from fastapi import APIRouter
from fastapi import Form
from fastapi import HTTPException
import datetime as dt

router = APIRouter()


@router.post("/projects/", tags=["projects"], response_model=ProjectResponse)
def create(name: str = Form(), user_id: int = Form()):
    with SessionLocal() as session:
        # ユーザーの存在確認
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=400, detail=f"User with id {user_id} not found")
        project_to_add = Project(
            name=name,
            user_id=user_id,
            created_at=dt.datetime.now(),
            updated_at=dt.datetime.now()
        )
        session.add_all([project_to_add])
        session.commit()
        session.refresh(project_to_add)
        return ProjectResponse.model_validate(project_to_add)


@router.get("/projects/{id}", tags=["projects"], response_model=ProjectResponse)
def read(id: int):
    with SessionLocal() as session:
        project = session.query(Project).filter(Project.id == id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return ProjectResponse.model_validate(project)


@router.put("/projects/{id}", tags=["projects"], response_model=ProjectResponse)
def update(id: int, name: str = Form(), description: str = Form(), user_id: int = Form()):
    with SessionLocal() as session:
        project = session.query(Project).filter(Project.id == id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        # ユーザーの存在確認
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=400, detail=f"User with id {user_id} not found")
        project.name = name
        project.user_id = user_id
        project.updated_at = dt.datetime.now()
        session.commit()
        session.refresh(project)
        return ProjectResponse.model_validate(project)


@router.patch("/projects/{id}", tags=["projects"], response_model=ProjectResponse)
def patch(id: int, attribute: str = Form(), new_value: str = Form()):
    with SessionLocal() as session:
        project = session.query(Project).filter(Project.id == id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        match attribute:
            case "name":
                project.name = new_value
            case "description":
                project.description = new_value
            case "user_id":
                # ユーザーの存在確認
                user = session.query(User).filter(User.id == new_value).first()
                if not user:
                    raise HTTPException(status_code=400, detail=f"User with id {new_value} not found")
                project.user_id = new_value
            case _:
                raise HTTPException(status_code=400, detail="Invalid attribute")
        project.updated_at = dt.datetime.now()
        session.commit()
        session.refresh(project)
        return ProjectResponse.model_validate(project)


@router.delete("/projects/{id}", tags=["projects"])
def delete(id: int):
    with SessionLocal() as session:
        project = session.query(Project).filter(Project.id == id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        session.delete(project)
        session.commit()
        return {"message": "Project deleted successfully"}

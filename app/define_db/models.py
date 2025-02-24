from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.types import String
from sqlalchemy.types import TIMESTAMP as Timestamp
from define_db.database import Base, engine
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
        # index=True
    )
    email: Mapped[str] = mapped_column(
        # Gmailアドレスは最大40文字（ユーザー名30文字 + "@gmail.com"10文字）
        # 参考：https://support.google.com/mail/answer/9211434?hl=ja
        # 10文字のバッファをもたせる
        String(50),
        # index=True
    )


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
        # index=True
    )
    name: Mapped[str] = mapped_column(
        String(256),
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    user: Mapped["User"] = relationship(
        foreign_keys=[user_id]
    )
    created_at: Mapped[str] = mapped_column(
        Timestamp(),
    )
    updated_at: Mapped[str] = mapped_column(
        Timestamp(),
    )


class Run(Base):
    __tablename__ = "runs"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship(
        foreign_keys=[project_id]
    )
    file_name: Mapped[str] = mapped_column(String(256))
    checksum: Mapped[str] = mapped_column(String(256))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    user: Mapped["User"] = relationship(
        foreign_keys=[user_id]
    )
    added_at: Mapped[str] = mapped_column(
        Timestamp(),
    )
    started_at: Mapped[datetime] = mapped_column(
        # Timestamp(),
        DateTime(),
        nullable=True,
        # default=None
    )
    finished_at: Mapped[datetime] = mapped_column(
        # Timestamp(),
        DateTime(),
        nullable=True,
        # default=None
    )
    # finished_at: Mapped[str] = mapped_column(
    #     Timestamp(),
    #     nullable=True,
    #     default=""
    # )
    status: Mapped[str] = mapped_column(String(10))
    storage_address: Mapped[str] = mapped_column(String(256))


class Process(Base):
    __tablename__ = "processes"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id"))
    run: Mapped["Run"] = relationship(
        foreign_keys=[run_id]
    )
    storage_address: Mapped[str] = mapped_column(String(256))


class Operation(Base):
    __tablename__ = "operations"
    id: Mapped[int] = mapped_column(primary_key=True)
    process_id: Mapped[int] = mapped_column(ForeignKey("processes.id"))
    process: Mapped["Process"] = relationship(
        foreign_keys=[process_id]
    )
    name: Mapped[str] = mapped_column(String(256))
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("operations.id"),
        nullable=True
    )
    parent: Mapped["Operation"] = relationship(
        foreign_keys=[parent_id]
    )
    started_at: Mapped[datetime] = mapped_column(
        # Timestamp(),
        DateTime(),
        nullable=True
    )
    finished_at: Mapped[datetime] = mapped_column(
        # Timestamp(),
        DateTime(),
        nullable=True
    )
    status: Mapped[str] = mapped_column(String(10))
    storage_address: Mapped[str] = mapped_column(String(256))
    is_transport: Mapped[bool] = mapped_column(
        nullable=False
    )
    is_data: Mapped[bool] = mapped_column(
        nullable=False
    )


class Edge(Base):
    __tablename__ = "edges"
    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id"))
    run: Mapped["Run"] = relationship(
        foreign_keys=[run_id]
    )
    from_id: Mapped[int] = mapped_column(ForeignKey("operations.id"))
    from_: Mapped["Operation"] = relationship(
        foreign_keys=[from_id]
    )
    to_id: Mapped[int] = mapped_column(ForeignKey("operations.id"))
    to: Mapped["Operation"] = relationship(
        foreign_keys=[to_id]
    )


if __name__ == "__main__":
    Base.metadata.create_all(engine)

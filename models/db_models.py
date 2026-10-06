from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean, Float
from datetime import datetime

class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

class MeasureUnit(Base):
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    short_name: Mapped[str] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

class Department(Base):
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    short_name: Mapped[str] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

class Category(Base):
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    sort: Mapped[Float] = mapped_column(Float, nullable=False)
    parent_id:Mapped[int | None] = mapped_column(ForeignKey('Category.id', ondelete='SET NULL'), nullable=True)
    children: Mapped[list["Category"]] = relationship(
        'Category',
        back_populates='parent',
        cascade='all, delete-orphan',
    )
    parent: Mapped['Category' | None] = relationship(
        'Category',
        back_populates='children',
        remote_side='Category.id',
    )

    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name!r} parent_id={self.parent_id}>"

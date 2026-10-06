from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean, Float
from datetime import datetime

class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

class MeasureUnit(Base):
    __tablename__ = 'measure_unit'
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    short_name: Mapped[str] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

class Department(Base):
    __tablename__ = 'department'
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    short_name: Mapped[str] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

class Category(Base):
    __tablename__ = 'category'
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    sort: Mapped[Float] = mapped_column(Float, nullable=False)
    parent_id:Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='SET NULL'), nullable=True)
    children: Mapped[list["Category"]] = relationship(
        'category',
        back_populates='parent',
        cascade='all, delete-orphan',
        lazy='joined',
    )
    parent: Mapped['Category'] = relationship(
        'category',
        back_populates='children',
        remote_side='category.id',
        lazy='joined',
    )

    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name!r} parent_id={self.parent_id}>"

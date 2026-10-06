from more_itertools.more import map_except
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean, Float, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)


class CreateDateMixin(object):

    create_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(timezone.utc))


class MeasureUnit(Base, CreateDateMixin):
    __tablename__ = 'measure_unit'
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    short_name: Mapped[str] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    items: Mapped[list['Items']] = relationship('Items', back_populates='measure_unit')


class Department(Base, CreateDateMixin):
    __tablename__ = 'department'
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    short_name: Mapped[str] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    users: Mapped[list['UserDepartment']] = relationship(back_populates='department')


class Category(Base, CreateDateMixin):
    __tablename__ = 'category'
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    sort: Mapped[Float] = mapped_column(Float, nullable=False)
    parent_id:Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='SET NULL'), nullable=True)
    children: Mapped[list['Category']] = relationship(
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
    items: Mapped[list['Items']] = relationship('Items', back_populates='category')

    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name!r} parent_id={self.parent_id}>"


class Branch(Base):
    __tablename__ = 'branch'

    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    short_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_main: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    plan: Mapped[list['Plan']] = relationship('Plan', back_populates='branch')
    users: Mapped[list['UserBranch']] = relationship(back_populates='branch')


class FileStore(Base, CreateDateMixin):
    __tablename__ = 'file_store'

    name: Mapped[str] = mapped_column(String(500), nullable=False)


class Items(Base, CreateDateMixin):
    __tablename__ = 'item'

    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='SET NULL'), nullable=False)
    measure_unit_id: Mapped[int] = mapped_column(ForeignKey('measure_unit.id', ondelete='SET NULL'), nullable=False)
    preferred_unit_id: Mapped[int] = mapped_column(ForeignKey('measure_unit.id', ondelete='SET NULL'), nullable=False)
    transform_ratio: Mapped[DECIMAL] = mapped_column(DECIMAL(10,4), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    category: Mapped['Category'] = relationship('Category', back_populates='items')
    measure_unit: Mapped['MeasureUnit'] = relationship('MeasureUnit', back_populates='items')
    plan: Mapped[list['Plan']] = relationship('Plan', back_populates='items')


class Period(Base, CreateDateMixin):
    __tablename__ = 'period'

    short_name: Mapped[str] = mapped_column(String(250), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    stop_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    plan: Mapped[list['Plan']] = relationship('Plan', back_populates='period')


class Plan(Base, CreateDateMixin):
    __tablename__ = 'plan'
    branch_id: Mapped[int] = mapped_column(ForeignKey('branch.id', ondelete='CASCADE'), nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey('item.id', ondelete='CASCADE'), nullable=False)
    period_id: Mapped[int] = mapped_column(ForeignKey('period.id', ondelete='CASCADE'), nullable=False)
    modify_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    quantity: Mapped[DECIMAL] = mapped_column(DECIMAL(10,4), nullable=True)

    branch: Mapped['Branch'] = relationship('Branch', back_populates='plan')
    items: Mapped['Items'] = relationship('Items', back_populates='plan')
    period: Mapped['Period'] = relationship('Period', back_populates='plan')


class PlanModHistory(Base, CreateDateMixin):
    __tablename__ = 'plan_mod_history'

    plan_id: Mapped[int] = mapped_column(ForeignKey('plan.id', ondelete='CASCADE'), nullable=False)
    prev_quantity: Mapped[DECIMAL] = mapped_column(DECIMAL(10,4), nullable=False)


class User(Base, CreateDateMixin):
    __tablename__ = 'user'

    login: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    surname: Mapped[str] = mapped_column(String(150), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(100), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    departments: Mapped[list['UserDepartment']] = relationship(back_populates='user')
    branches: Mapped[list['UserBranch']] = relationship(back_populates='user')

class UserDepartment(Base, CreateDateMixin):
    __tablename__ = 'user_department'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    department_id: Mapped[int] = mapped_column(ForeignKey('department.id', ondelete='CASCADE'), primary_key=True)

    user: Mapped['User'] = relationship(back_populates='departments')
    department: Mapped['Department'] = relationship(back_populates='users')

class UserBranch(Base, CreateDateMixin):
    __tablename__ = 'user_branch'
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey('branch.id', ondelete='CASCADE'), primary_key=True)

    user: Mapped['User'] = relationship(back_populates='branches')
    branch: Mapped['Branch'] = relationship(back_populates='users')


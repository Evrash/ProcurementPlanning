from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, Boolean, Float, DECIMAL
from datetime import datetime, timezone

class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)


class CreateDateMixin(object):

    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))


class MeasureUnit(Base, CreateDateMixin):
    __tablename__ = 'measure_unit'

    name: Mapped[str] = mapped_column(String(250), nullable=False)
    short_name: Mapped[str] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    items: Mapped[list['Items']] = relationship('Items', back_populates='measure_unit', foreign_keys='Items.measure_unit_id')


class Department(Base, CreateDateMixin):
    __tablename__ = 'department'

    name: Mapped[str] = mapped_column(String(250), nullable=False)
    short_name: Mapped[str] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    users: Mapped[list['UserDepartment']] = relationship(back_populates='department')


class Category(Base, CreateDateMixin):
    __tablename__ = 'category'
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    path: Mapped[str] = mapped_column(String(1024), nullable=False, index=True)
    sort: Mapped[Float] = mapped_column(Float, nullable=False)

    @property
    def parent_path(self) -> str:
        return self.path.rsplit('/', 1)[0] + '/' if '/' in self.path else '/'
    # parent_id:Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='SET NULL'), nullable=True)
    # children: Mapped[list['Category']] = relationship(
    #     'Category',
    #     back_populates='parent',
    #     cascade='all, delete-orphan',
    #     lazy='joined'
    # )
    # parent: Mapped['Category'] = relationship(
    #     'Category',
    #     back_populates='children',
    #     remote_side='Category.id',
    #     lazy='joined'
    # )
    items: Mapped[list['Items']] = relationship(
        'Items',
        back_populates='category',
        foreign_keys=lambda: Items.category_id
    )

    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name!r} parent_id={self.path}>"


class Branch(Base):
    __tablename__ = 'branch'

    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    short_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_main: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    plan: Mapped[list['Plan']] = relationship('Plan', back_populates='branch')
    users: Mapped[list['UserBranch']] = relationship(back_populates='branch')


class Items(Base, CreateDateMixin):
    __tablename__ = 'item'

    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='SET NULL'), nullable=False)
    measure_unit_id: Mapped[int] = mapped_column(ForeignKey('measure_unit.id', ondelete='SET NULL'), nullable=False)
    preferred_unit_id: Mapped[int] = mapped_column(ForeignKey('measure_unit.id', ondelete='SET NULL'), nullable=False)
    transform_ratio: Mapped[DECIMAL] = mapped_column(DECIMAL(10,4), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    category: Mapped['Category'] = relationship('Category', back_populates='items', foreign_keys=lambda: Items.category_id)
    measure_unit: Mapped['MeasureUnit'] = relationship('MeasureUnit', back_populates='items', foreign_keys='Items.measure_unit_id')
    plan: Mapped[list['Plan']] = relationship('Plan', back_populates='items')
    tz_examples: Mapped[list['TzExample']] = relationship(back_populates='item')


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
    plan_history: Mapped[list['PlanModHistory']] = relationship('PlanModHistory', back_populates='plans')


class PlanModHistory(Base, CreateDateMixin):
    __tablename__ = 'plan_mod_history'

    plan_id: Mapped[int] = mapped_column(ForeignKey('plan.id', ondelete='CASCADE'), nullable=False)
    prev_quantity: Mapped[DECIMAL] = mapped_column(DECIMAL(10,4), nullable=False)

    plans: Mapped[Plan] = relationship('Plan', back_populates='plan_history')

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


class FileStorage(Base, CreateDateMixin):
    __tablename__ = 'file_storage'

    name: Mapped[str] = mapped_column(String(250), nullable=False)
    tz_examples: Mapped[list['TzExample']] = relationship('TzExample', back_populates='file')


class TzExample(Base, CreateDateMixin):
    __tablename__ = 'tz_example'

    item_id: Mapped[int] = mapped_column(ForeignKey('item.id', ondelete='SET NULL'))
    text: Mapped[str] = mapped_column(String(10000), nullable=True)
    file_id: Mapped[int] = mapped_column(ForeignKey('file_storage.id', ondelete='SET NULL'))

    item: Mapped['Items'] = relationship('Items', back_populates='tz_examples')
    file:Mapped['FileStorage'] = relationship('FileStorage', back_populates='tz_examples')

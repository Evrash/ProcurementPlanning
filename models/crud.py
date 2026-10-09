from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import db_helper, MeasureUnit, Department, Category, Items, Plan, Period
from schemas.measure_unit import MeasureUnitCreate

async def set_category(name:str) -> Category | None:
    async with db_helper.session_factory() as conn:
        new_category = Category()
        new_category.name = name
        conn.add(new_category)
        new_category.path = f'/'
        new_category.sort = 1.0
        await conn.commit()

async def get_categories() -> list[Category]:
    async with db_helper.session_factory() as conn:
        query = select(Category).order_by(Category.path)
        result = await conn.execute(query)
        return result.scalars().all()

async def get_items() -> list[Items]:
    async with db_helper.session_factory() as conn:
        query = select(Items).options(selectinload(Items.measure_unit)).options(selectinload(Items.category))
        result = await conn.execute(query)
        return result.scalars().all()


async def set_item() -> Items:
    async with db_helper.session_factory() as conn:
        item = Items()
        item.name = 'new item2'
        # measure_unit = (await get_measure_unit())[0]
        item.category_id = 4
        item.measure_unit_id = 2
        # item.measure_unit = measure_unit
        item.preferred_unit_id = 3
        item.transform_ratio = 0.5
        conn.add(item)
        # stmt = insert(Items).values(name='new item', measure_unit_id=2, preferred_unit_id = 3,
        #                             transform_ratio = 0.5, is_active = True, category_id = 4)
        # await conn.execute(stmt)
        await conn.commit()
        return item

async def get_plans() -> list[Plan]:
    async with db_helper.session_factory() as conn:
        query = select(Plan).options(selectinload(Plan.branch))
        result = await conn.execute(query)
        return result.scalars().all()


# async def get_categories(root_id: int) -> list[Category]:
    # async with db_helper.session_factory() as conn:
    #     base = (
    #         select(Category.id, Category.name, Category.parent_id)
    #         .where(Category.id == root_id)
    #         .cte(name='subtree', recursive=True)
    #     )
    #     parent = base.alias('parent')
    #     child = Category.__table__.alias('child')
    #
    #     recursive = select(child.c.id, child.c.name, child.c.parent_id).join(
    #         parent, child.c.parent_id == parent.c.id
    #     )
    #     cte = base.union_all(recursive)
    #
    #     stmt = select(Category).from_statement(
    #         select(Category).where(Category.id.in_(select(cte.c.id)))
    #     )
    #
    #     return list(conn.scalars(stmt))

async def get_departments() -> list[Department]:
    async with db_helper.session_factory() as conn:
        query = select(Department)
        result = await conn.execute(query)
        return result.scalars().all()

async def get_measure_units(is_active: bool | None = None) -> list[MeasureUnit]:
    async with db_helper.session_factory() as conn:
        if is_active is not None:
            query = select(MeasureUnit).where(MeasureUnit.is_active == is_active).order_by(MeasureUnit.name)
        else:
            query = select(MeasureUnit).order_by(MeasureUnit.name)
        result = await conn.execute(query)
        return result.scalars().all()

async def set_measure_unit(name: str, short_name: str) -> MeasureUnit | None:
    async with db_helper.session_factory() as conn:
        measure_unit = MeasureUnit()
        measure_unit.name = name
        measure_unit.short_name = short_name
        conn.add(measure_unit)
        await conn.commit()
        return measure_unit

async def get_measure_units2(session: AsyncSession) -> list[MeasureUnit]:
    stmt = select(MeasureUnit).order_by(MeasureUnit.name)
    result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)

# async def get_departments() -> list[Department]:
#     async with db_helper.session_factory() as session:
#         query = (select(Department))
#         result = await session.execute(query)
#         return result.scalars().all()
#
# async def add_department(name: str, short_name: str) -> Department:
#     async with db_helper.session_factory() as session:
#         department = Department()
#         department.name = name
#         department.short_name = short_name
#         await session.add(department)
#         await session.commit()
#         return department
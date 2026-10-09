from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models import crud, MeasureUnit
from models import db_helper

import uvicorn

app = FastAPI()

@app.get("/measure_units/")
async def get_measure_units(is_active: bool | None = None):
    measure_units: list[MeasureUnit] = await crud.get_measure_units(is_active=is_active)
    return measure_units

@app.get("/measure_units2/")
async def get_measure_units2(session: AsyncSession = Depends(db_helper.session_getter)):
    measure_units: list[MeasureUnit] = await crud.get_measure_units(is_active=is_active)
    return measure_units

if __name__ == '__main__':
    uvicorn.run(app, port=19000)


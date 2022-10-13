import typing as t
from app import app
from home.tables import Business
from piccolo_api.crud.serializers import create_pydantic_model
from fastapi.responses import JSONResponse

BusinessModelIn: t.Any = create_pydantic_model(table=Business, model_name="BusinessModelIn")
BusinessModelOut: t.Any = create_pydantic_model(
    table=Business, include_default_columns=True, model_name="BusinessModelOut"
)

@app.get("/business/", response_model=t.List[BusinessModelOut], tags=["Business"])
async def business():
    return await Business.select().order_by(Business.id)


@app.post("/business/", response_model=BusinessModelOut, tags=["Business"])
async def create_business(business_model: BusinessModelIn):
    business = Business(**business_model.dict())
    await business.save()
    return business.to_dict()


@app.put("/business/{business_id}/", response_model=BusinessModelOut, tags=["Business"])
async def update_business(business_id: int, business_model: BusinessModelIn):
    business = await Business.objects().get(Business.id == business_id)
    if not business:
        return JSONResponse({}, status_code=404)

    for key, value in business_model.dict().items():
        setattr(business, key, value)

    await business.save()

    return business.to_dict()


@app.delete("/business/{business_id}/", tags=["Business"])
async def delete_business(business_id: int):
    business = await Business.objects().get(Business.id == business_id)
    if not business:
        return JSONResponse({}, status_code=404)

    await business.remove()

    return JSONResponse({})
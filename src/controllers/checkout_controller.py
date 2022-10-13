import typing as t
from app import app
from home.tables import Checkout
from piccolo_api.crud.serializers import create_pydantic_model
from fastapi.responses import JSONResponse

CheckoutModelIn: t.Any = create_pydantic_model(table=Checkout, model_name="CheckoutModelIn")
CheckoutModelOut: t.Any = create_pydantic_model(
    table=Checkout, include_default_columns=True, model_name="CheckoutModelOut"
)

@app.get("/checkout/", response_model=t.List[CheckoutModelOut], tags=["Checkout"])
async def checkout():
    return await Checkout.select().order_by(Checkout.id)


@app.post("/checkout/", response_model=CheckoutModelOut, tags=["Checkout"])
async def create_checkout(checkout_model: CheckoutModelIn):
    checkout = Checkout(**checkout_model.dict())
    await checkout.save()
    return checkout.to_dict()


@app.put("/checkout/{checkout_id}/", response_model=CheckoutModelOut, tags=["Checkout"])
async def update_checkout(checkout_id: int, checkout_model: CheckoutModelIn):
    checkout = await Checkout.objects().get(Checkout.id == checkout_id)
    if not checkout:
        return JSONResponse({}, status_code=404)

    for key, value in checkout_model.dict().items():
        setattr(checkout, key, value)

    await checkout.save()

    return checkout.to_dict()


@app.delete("/checkout/{checkout_id}/", tags=["Checkout"])
async def delete_checkout(checkout_id: int):
    checkout = await Checkout.objects().get(Checkout.id == checkout_id)
    if not checkout:
        return JSONResponse({}, status_code=404)

    await checkout.remove()

    return JSONResponse({})
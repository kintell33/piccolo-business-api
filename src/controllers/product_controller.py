import typing as t
from app import app
from home.tables import Product
from piccolo_api.crud.serializers import create_pydantic_model
from fastapi.responses import JSONResponse

ProductModelIn: t.Any = create_pydantic_model(table=Product, model_name="ProductModelIn")
ProductModelOut: t.Any = create_pydantic_model(
    table=Product, include_default_columns=True, model_name="ProductModelOut"
)

@app.get("/product/", response_model=t.List[ProductModelOut], tags=["Product"])
async def product():
    return await Product.select().order_by(Product.id)


@app.post("/product/", response_model=ProductModelOut, tags=["Product"])
async def create_product(product_model: ProductModelIn):
    product = Product(**product_model.dict())
    await product.save()
    return product.to_dict()


@app.put("/product/{product_id}/", response_model=ProductModelOut, tags=["Product"])
async def update_product(product_id: int, product_model: ProductModelIn):
    product = await Product.objects().get(Product.id == product_id)
    if not product:
        return JSONResponse({}, status_code=404)

    for key, value in product_model.dict().items():
        setattr(product, key, value)

    await product.save()

    return product.to_dict()


@app.delete("/product/{product_id}/", tags=["Product"])
async def delete_product(product_id: int):
    product = await Product.objects().get(Product.id == product_id)
    if not product:
        return JSONResponse({}, status_code=404)

    await product.remove()

    return JSONResponse({})
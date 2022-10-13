import typing as t
from app import app
from home.tables import Cart, CartProduct, Product
from piccolo_api.crud.serializers import create_pydantic_model
from fastapi.responses import JSONResponse
from home.models import CartProductModelIn, CartProductModelOut

CartModelIn: t.Any = create_pydantic_model(table=Cart, model_name="CartModelIn")
CartModelOut: t.Any = create_pydantic_model(
    table=Cart, include_default_columns=True, model_name="CartModelOut"
)

@app.get("/cart/", response_model=t.List[CartModelOut], tags=["Cart"])
async def cart():
    return await Cart.select().order_by(Cart.id)


@app.post("/cart/", response_model=CartModelOut, tags=["Cart"])
async def create_cart(cart_model: CartModelIn):
    cart = Cart(**cart_model.dict())
    await cart.save()
    return cart.to_dict()


@app.put("/cart/{cart_id}/", response_model=CartModelOut, tags=["Cart"])
async def update_cart(cart_id: int, cart_model: CartModelIn):
    cart = await Cart.objects().get(Cart.id == cart_id)
    if not cart:
        return JSONResponse({}, status_code=404)

    for key, value in cart_model.dict().items():
        setattr(cart, key, value)

    await cart.save()

    return cart.to_dict()


@app.delete("/cart/{cart_id}/", tags=["Cart"])
async def delete_cart(cart_id: int):
    cart = await Cart.objects().get(Cart.id == cart_id)
    if not cart:
        return JSONResponse({}, status_code=404)

    await cart.remove()

    return JSONResponse({})

@app.post("/cart/{cart_id}/product", response_model=CartProductModelOut, tags=["Cart"])
async def create_cart_product(cart_id:int, cart_product_model: CartProductModelIn):
    cart = await Cart.objects().get(Cart.id == cart_id)
    product = await Product.objects().get(Product.id == cart_product_model.productId)
    cartProduct = CartProduct(cart=cart, product=product)
    await cartProduct.save()
    return {"cartUuid":cart.uuid, "productName":product.name}
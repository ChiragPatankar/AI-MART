from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from functools import lru_cache
from src.database import get_db
from src.database.models import Cart, Product
from src.schemas.cart import CartItem, CartItemCreate, CartItemUpdate
from src.agents import CartAgent

router = APIRouter()
cart_agent = CartAgent()

@lru_cache(maxsize=1000)
def get_cached_product(product_id: int, db: Session) -> Product:
    return db.query(Product).filter(Product.id == product_id).first()

@router.get("/cart/items", response_model=List[CartItem])
def get_cart_items(customer_id: int = 1, db: Session = Depends(get_db)):
    try:
        cart_items = (
            db.query(Cart)
            .filter(Cart.customer_id == customer_id)
            .join(Product)
            .all()
        )
        
        return [
            CartItem(
                product_id=item.product_id,
                quantity=item.quantity,
                name=item.product.name,
                price=item.product.price,
                image_url=item.product.image_url
            )
            for item in cart_items
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cart/items", response_model=CartItem)
def add_to_cart(item: CartItemCreate, customer_id: int = 1, db: Session = Depends(get_db)):
    try:
        product = get_cached_product(item.product_id, db)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        existing_item = (
            db.query(Cart)
            .filter(
                Cart.customer_id == customer_id,
                Cart.product_id == item.product_id
            )
            .first()
        )

        if existing_item:
            existing_item.quantity += item.quantity
            db.commit()
            cart_item = existing_item
        else:
            cart_item = Cart(
                customer_id=customer_id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            db.add(cart_item)
            db.commit()

        # Update recommendations based on cart changes
        cart_agent.update_recommendations(customer_id, item.product_id)

        return CartItem(
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            name=product.name,
            price=product.price,
            image_url=product.image_url
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/cart/items/{product_id}", response_model=CartItem)
def update_cart_item(
    product_id: int,
    item: CartItemUpdate,
    customer_id: int = 1,
    db: Session = Depends(get_db)
):
    try:
        cart_item = (
            db.query(Cart)
            .filter(
                Cart.customer_id == customer_id,
                Cart.product_id == product_id
            )
            .first()
        )

        if not cart_item:
            raise HTTPException(status_code=404, detail="Item not found in cart")

        product = get_cached_product(product_id, db)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        cart_item.quantity = item.quantity
        db.commit()

        return CartItem(
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            name=product.name,
            price=product.price,
            image_url=product.image_url
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/cart/items/{product_id}")
def remove_from_cart(product_id: int, customer_id: int = 1, db: Session = Depends(get_db)):
    try:
        cart_item = (
            db.query(Cart)
            .filter(
                Cart.customer_id == customer_id,
                Cart.product_id == product_id
            )
            .first()
        )

        if not cart_item:
            raise HTTPException(status_code=404, detail="Item not found in cart")

        db.delete(cart_item)
        db.commit()

        return {"status": "success"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.models import Cart, Product
from src.database.database_manager import DatabaseManager

class CartAgent:
    def __init__(self, agent_id: str, db_manager: DatabaseManager):
        self.agent_id = agent_id
        self.db_manager = db_manager

    async def process(self, data: Dict[str, Any], db: AsyncSession) -> Dict[str, Any]:
        action_type = data.get("action_type", "get_cart")
        
        if action_type == "get_cart":
            return await self._get_cart(data, db)
        elif action_type == "add_to_cart":
            return await self._add_to_cart(data, db)
        elif action_type == "update_quantity":
            return await self._update_quantity(data, db)
        elif action_type == "remove_from_cart":
            return await self._remove_from_cart(data, db)
        else:
            raise ValueError(f"Unknown action type: {action_type}")

    async def _get_cart(self, data: Dict[str, Any], db: AsyncSession) -> Dict[str, Any]:
        # For now, using a default customer_id of 1
        customer_id = data.get("customer_id", 1)
        
        # Get cart items for the customer
        stmt = select(Cart, Product).join(Product).where(Cart.customer_id == customer_id)
        result = await db.execute(stmt)
        cart_items = result.all()

        # Format cart items
        items = []
        for cart_item, product in cart_items:
            items.append({
                "product_id": product.id,
                "name": product.name,
                "description": product.description,
                "price": float(product.price),
                "category": product.category,
                "image_url": product.image_url,
                "quantity": cart_item.quantity
            })

        return {"items": items}

    async def _add_to_cart(self, data: Dict[str, Any], db: AsyncSession) -> Dict[str, Any]:
        customer_id = data.get("customer_id", 1)
        product_id = data.get("product_id")
        quantity = data.get("quantity", 1)

        if not product_id:
            raise ValueError("Product ID is required")

        # Check if item already exists in cart
        stmt = select(Cart).where(
            Cart.customer_id == customer_id,
            Cart.product_id == product_id
        )
        result = await db.execute(stmt)
        cart_item = result.scalar_one_or_none()

        if cart_item:
            # Update quantity if item exists
            cart_item.quantity += quantity
        else:
            # Create new cart item
            cart_item = Cart(
                customer_id=customer_id,
                product_id=product_id,
                quantity=quantity
            )
            db.add(cart_item)

        await db.commit()
        return {"message": "Item added to cart successfully"}

    async def _update_quantity(self, data: Dict[str, Any], db: AsyncSession) -> Dict[str, Any]:
        customer_id = data.get("customer_id", 1)
        product_id = data.get("product_id")
        quantity = data.get("quantity")

        if not product_id or quantity is None:
            raise ValueError("Product ID and quantity are required")

        # Get cart item
        stmt = select(Cart).where(
            Cart.customer_id == customer_id,
            Cart.product_id == product_id
        )
        result = await db.execute(stmt)
        cart_item = result.scalar_one_or_none()

        if not cart_item:
            raise ValueError("Item not found in cart")

        if quantity <= 0:
            # Remove item if quantity is 0 or negative
            await db.delete(cart_item)
        else:
            cart_item.quantity = quantity

        await db.commit()
        return {"message": "Cart updated successfully"}

    async def _remove_from_cart(self, data: Dict[str, Any], db: AsyncSession) -> Dict[str, Any]:
        customer_id = data.get("customer_id", 1)
        product_id = data.get("product_id")

        if not product_id:
            raise ValueError("Product ID is required")

        # Get cart item
        stmt = select(Cart).where(
            Cart.customer_id == customer_id,
            Cart.product_id == product_id
        )
        result = await db.execute(stmt)
        cart_item = result.scalar_one_or_none()

        if not cart_item:
            raise ValueError("Item not found in cart")

        await db.delete(cart_item)
        await db.commit()
        return {"message": "Item removed from cart successfully"} 
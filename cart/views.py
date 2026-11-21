from datetime import datetime, timezone
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from project.mongodb import products_collection, cart_collection


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def add_to_cart(request):
    
    try:
        user_id = getattr(request.user, "user_id", None)

        if not user_id:
            return Response({
                "status": False,
                "message": "User authentication failed"
            }, status=401)

        # 2. Get request data
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)
        variant_name = request.data.get("variant_name")

        if not product_id:
            return Response({
                "status": False,
                "message": "Product ID is required"
            }, status=400)

        # Validate quantity
        try:
            quantity = int(quantity)

            if quantity <= 0:
                raise ValueError

        except (ValueError, TypeError):
            return Response({
                "status": False,
                "message": "Quantity must be a positive integer"
            }, status=400)

        # 3. Fetch product
        product = products_collection.find_one({
            "product_id": product_id,
            "is_deleted": {"$ne": True},
            "status": "Active"
        })

        if not product:
            return Response({
                "status": False,
                "message": "Product not found or inactive"
            }, status=404)

        # 4. Get product price and stock
        variants = product.get("variants", [])

        selected_variant = None

        if variants:

            if not variant_name:
                return Response({
                    "status": False,
                    "message": "Please select a product variant"
                }, status=400)

            selected_variant = next(
                (
                    v for v in variants
                    if v.get("variant_name") == variant_name
                ),
                None
            )

            if not selected_variant:
                return Response({
                    "status": False,
                    "message": "Invalid product variant"
                }, status=400)

            unit_price = float(selected_variant.get("price", 0))
            available_stock = int(selected_variant.get("stock", 0))

        else:

            variant_name = None

            unit_price = float(product.get("unit_price", 0))
            available_stock = int(product.get("stock", 0))

        if available_stock <= 0:
            return Response({
                "status": False,
                "message": "Product is out of stock"
            }, status=400)

        # 5. Check existing cart item
        cart_item = cart_collection.find_one({
            "user_id": str(user_id),
            "product_id": product_id,
            "variant_name": variant_name
        })

        existing_quantity = (
            int(cart_item.get("quantity", 0))
            if cart_item else 0
        )

        # 6. Check available stock
        total_quantity = existing_quantity + quantity

        if total_quantity > available_stock:
            return Response({
                "status": False,
                "message": f"Only {available_stock - existing_quantity} more items can be added"
            }, status=400)

        # 7. Prepare product details
        images = product.get("images", {})

        if not isinstance(images, dict):
            images = {}

        now = datetime.now(timezone.utc)

        cart_data = {

            "user_id": str(user_id),

            "product_id": product_id,

            "product_name": product.get("product_name"),

            "product_type": product.get("product_type"),

            "category_name": product.get("category_name"),

            "variant_name": variant_name,

            "unit_price": unit_price,

            "quantity": total_quantity,

            "subtotal": unit_price * total_quantity,

            "image": images.get("image_1"),

            "updated_at": now
        }

        # 8. Update or insert cart
        if cart_item:

            cart_collection.update_one(
                {"_id": cart_item["_id"]},
                {"$set": cart_data}
            )

            message = "Cart quantity updated successfully"

        else:

            cart_data["created_at"] = now

            cart_collection.insert_one(cart_data)

            message = "Product added to cart successfully"

        return Response({
            "status": True,
            "message": message,
            "data": cart_data
        }, status=200)

    except Exception as e:

        return Response({
            "status": False,
            "message": "Something went wrong",
            "error": str(e)
        }, status=500)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_cart(request):

    try:

        # 1. Get logged-in user ID
        user_id = getattr(request.user, "user_id", None)

        if not user_id:
            return Response({
                "status": False,
                "message": "User authentication failed"
            }, status=401)

        # 2. Fetch only logged-in user's cart
        cart_items = list(cart_collection.find({
            "user_id": str(user_id)
        }))

        # 3. Prepare response
        cart_data = []

        total_amount = 0
        total_items = 0

        for item in cart_items:

            quantity = int(item.get("quantity", 0))

            unit_price = float(item.get("unit_price", 0))

            subtotal = unit_price * quantity

            total_amount += subtotal
            total_items += quantity

            cart_data.append({

                "product_id": item.get("product_id"),

                "product_name": item.get("product_name"),

                "product_type": item.get("product_type"),

                "category_name": item.get("category_name"),

                "variant_name": item.get("variant_name"),

                "unit_price": unit_price,

                "quantity": quantity,

                "subtotal": subtotal,

                "image": item.get("image")

            })

        # 4. Return cart
        return Response({

            "status": True,

            "message": "Cart fetched successfully",

            "total_items": total_items,

            "total_amount": round(total_amount, 2),

            "cart": cart_data

        }, status=200)

    except Exception as e:

        return Response({

            "status": False,

            "message": "Something went wrong",

            "error": str(e)

        }, status=500)
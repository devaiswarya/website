import json
from rest_framework.decorators import (api_view,parser_classes)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from bson import ObjectId
from bson.errors import InvalidId
from project.mongodb import db
from .serializer import ProductSerializer
from  datetime import datetime , timezone
from bson import ObjectId
from uuid import uuid4
import math


categories_collection = db["category"]
products_collection = db["products"]


@api_view(["POST"])
@parser_classes([JSONParser])
def create_product(request):
    serializer = ProductSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {"message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    data = serializer.validated_data

    product_id = data["product_id"]
    product_name = data["product_name"]
    category_id = data["category_id"]

    primary_category_id = (
        data.get("primary_category_id") or None
    )
    secondary_category_id = (
        data.get("secondary_category_id") or None
    )

    unit_price = data["unit_price"]
    initial_stock_level = data["initial_stock_level"]
    short_description = data["short_description"]

    image_1 = data["image_1"]
    image_2 = data.get("image_2") or None
    image_3 = data.get("image_3") or None
    image_4 = data.get("image_4") or None

    variants = data.get("variants", [])
    product_status = data.get("status", "Active")

    if not isinstance(variants, list):
        return Response(
            {"message": "Variants must be a list"},
            status=status.HTTP_400_BAD_REQUEST
        )

    product_variants = []
    total_variant_stock = 0

    for variant in variants:

        if not isinstance(variant, dict):
            return Response(
                {"message": "Invalid variant format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        variant_name = variant.get("variant_name")
        variant_price = variant.get("price")
        variant_stock = variant.get("stock")

        if (
            not isinstance(variant_name, str)
            or not variant_name.strip()
        ):
            return Response(
                {"message": "Variant name is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if variant_price is None or variant_stock is None:
            return Response(
                {
                    "message": (
                        f"Price and stock are required "
                        f"for {variant_name}"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if isinstance(variant_price, bool):
                raise ValueError

            if isinstance(variant_stock, bool):
                raise ValueError

            variant_price = float(variant_price)

            if isinstance(variant_stock, float):
                if not math.isfinite(variant_stock):
                    raise ValueError
                if not variant_stock.is_integer():
                    raise ValueError

            variant_stock = int(variant_stock)

        except (ValueError, TypeError, OverflowError):
            return Response(
                {
                    "message": (
                        f"Invalid price or stock for "
                        f"{variant_name}"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if (
            not math.isfinite(variant_price)
            or variant_price < 0
        ):
            return Response(
                {
                    "message": (
                        f"Invalid or negative price "
                        f"for {variant_name}"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if variant_stock < 0:
            return Response(
                {
                    "message": (
                        f"Variant stock cannot be negative "
                        f"for {variant_name}"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        product_variants.append({
            # "variant_id": str(uuid4()),
            "variant_name": variant_name.strip(),
            "price": variant_price,
            "stock": variant_stock
        })
        total_variant_stock += variant_stock
    if (
        product_variants
        and total_variant_stock != initial_stock_level
    ):
        return Response(
            {
                "message": (
                    "Initial stock level must match "
                    "the total variant stock"
                ),
                "initial_stock_level": initial_stock_level,
                "variant_stock_total": total_variant_stock
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        category_object_id = ObjectId(category_id)
        product_category = categories_collection.find_one({
            "_id": category_object_id,
            # "is_deleted": {"$ne": True}
        })
    except (InvalidId, TypeError):
        return Response(
            {"message": "Invalid category ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    if not product_category:
        return Response(
            {"message": "Category not found"},
            status=status.HTTP_404_NOT_FOUND
        )

# //

    print("Database Name:", categories_collection.database.name)
    print("Collection Name:", categories_collection.name)

    print("Received Category ID:", category_id)

    category_object_id = ObjectId(category_id)

    print("Converted Category ID:", category_object_id)

    print("Total Categories:", categories_collection.count_documents({}))

    product_category = categories_collection.find_one({
    "_id": category_object_id
})

    print("Category Result:", product_category)

    primary_category = None
    if primary_category_id:
        try:
            primary_object_id = ObjectId(primary_category_id)
            primary_category = categories_collection.find_one({
                "_id": primary_object_id,
                "is_deleted": {"$ne": True}
            })
        except (InvalidId, TypeError):
            return Response(
                {"message": "Invalid primary category ID"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not primary_category:
            return Response(
                {"message": "Primary category not found"},
                status=status.HTTP_404_NOT_FOUND
            )
    secondary_category = None
    if secondary_category_id:
        try:
            secondary_object_id = ObjectId(
                secondary_category_id
            )
            secondary_category = categories_collection.find_one({
                "_id": secondary_object_id,
                "is_deleted": {"$ne": True}
            })
        except (InvalidId, TypeError):
            return Response(
                {"message": "Invalid secondary category ID"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not secondary_category:
            return Response(
                {"message": "Secondary category not found"},
                status=status.HTTP_404_NOT_FOUND
            )
    category_inactive = (
        product_category.get("status") == "Inactive"
        or (
            primary_category is not None
            and primary_category.get("status") == "Inactive"
        )
        or (
            secondary_category is not None
            and secondary_category.get("status") == "Inactive"
        )
    )
    if category_inactive:
        product_status = "Inactive"
    if initial_stock_level == 0:
        stock_status = "Out of Stock"
    elif initial_stock_level <= 5:
        stock_status = "Low Stock"
    else:
        stock_status = "In Stock"
    images = {
        "image_1": str(image_1),
        "image_2": str(image_2) if image_2 else None,
        "image_3": str(image_3) if image_3 else None,
        "image_4": str(image_4) if image_4 else None
    }
    product = {
        "product_id": product_id,
        "product_name": product_name,
        "category_id": str(category_object_id),
        "category_name": product_category.get("name"),
        "primary_category_id": (
            str(primary_object_id)
            if primary_category is not None
            else None
        ),
        "primary_category_name": (
            primary_category.get("name")
            if primary_category is not None
            else None
        ),
        "secondary_category_id": (
            str(secondary_object_id)
            if secondary_category is not None
            else None
        ),
        "secondary_category_name": (
            secondary_category.get("name")
            if secondary_category is not None
            else None
        ),
        "unit_price": float(unit_price),
        "initial_stock_level": initial_stock_level,
        "stock": initial_stock_level,
        "status": product_status,
        "stock_status": stock_status,
        "short_description": short_description,
        "images": images,
        "variants": product_variants,
        "is_deleted": False,
        "created_at": datetime.now(timezone.utc)
    }
    result = products_collection.insert_one(product)
    product_id = result.inserted_id
    return Response(
        {
            "message": "Product created successfully",
            "product": {
                "product_id": str(product_id),
                "product_name": product_name,
                "category_id": str(category_object_id),
                "category_name": product_category.get("name"),
                "primary_category_id": (
                    str(primary_object_id)
                    if primary_category is not None
                    else None
                ),
                "primary_category_name": (
                    primary_category.get("name")
                    if primary_category is not None
                    else None
                ),
                "secondary_category_id": (
                    str(secondary_object_id)
                    if secondary_category is not None
                    else None
                ),
                "secondary_category_name": (
                    secondary_category.get("name")
                    if secondary_category is not None
                    else None
                ),
                "unit_price": float(unit_price),
                "initial_stock_level": initial_stock_level,
                "stock": initial_stock_level,
                "status": product_status,
                "stock_status": stock_status,

                "short_description": short_description,

                "images": images,
                "variants": product_variants,

                "is_deleted": False
            }
        },
        status=status.HTTP_201_CREATED
    )

@api_view(["GET"])
def get_new_arrivals(request):

    try:
        new_arrivals = list(
            products_collection.find({
                "is_deleted": {"$ne": True},
                "status": "Active"
            })
            .sort("created_at", -1)
            .limit(10)
        )

        products = []

        for product in new_arrivals:

            products.append({
                "product_id": str(product["_id"]),
                "custom_product_id": product.get("product_id"),
                "product_name": product.get("product_name"),
                "category_id": product.get("category_id"),
                "category_name": product.get("category_name"),
                "unit_price": product.get("unit_price"),
                "initial_stock_level": product.get(
                    "initial_stock_level", 0
                ),
                "stock": product.get("stock", 0),
                "stock_status": product.get("stock_status"),
                "short_description": product.get(
                    "short_description"
                ),
                "images": product.get("images", {}),
                "variants": product.get("variants", []),
                "status": product.get("status"),
                "created_at": product.get("created_at")
            })

        return Response(
            {
                "message": "New arrivals fetched successfully",
                "total": len(products),
                "products": products
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:

        return Response(
            {
                "message": "Failed to fetch new arrivals",
                "error": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
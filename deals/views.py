from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from bson import ObjectId
from datetime import datetime, timezone
from decimal import Decimal
from django.utils import timezone as django_timezone
from project.mongodb import deals_collection, products_collection
from .serializer import DealSerializer

# def check_admin(request):

#     is_staff = getattr(request.user, "is_staff", False)
#     is_superuser = getattr(request.user, "is_superuser", False)

#     return is_staff or is_superuser

@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def create_deal(request):
    serializer = DealSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            "errors": serializer.errors
        }, status=400)

    data = serializer.validated_data


    product = products_collection.find_one({
        "product_id": data["product_id"],
        "is_deleted": {"$ne": True}
    })

    if not product:
        return Response({
            "message": "Product not found"
        }, status=404)

    # Get original price
    try:
        original_price = Decimal(str(product["unit_price"]))
        offer_price = data["offer_price"]

    except (KeyError, ValueError, TypeError):
        return Response({
            "message": "Product price is invalid"
        }, status=400)

    if original_price <= 0:
        return Response({
            "message": "Original product price is invalid"
        }, status=400)

    if offer_price >= original_price:
        return Response({
            "message": "Offer price must be less than original price"
        }, status=400)

    # Calculate discount
    discount = round(
        ((original_price - offer_price) / original_price) * 100,
        2
    )

    # MongoDB document
    deal_data = {
        "product_id": data["product_id"],
        "product_name": product.get("product_name", ""),
        "original_price": float(original_price),
        "offer_price": float(offer_price),
        "discount_percentage": float(discount),
        "offer_title": data["offer_title"],
        "start_date": data["start_date"].isoformat(),
        "end_date": data["end_date"].isoformat(),
        "status": data["status"],
        "is_deleted": False,
        "created_at": datetime.now(timezone.utc)
    }

    result = deals_collection.insert_one(deal_data)

    return Response({
        "message": "Deal created successfully",
        "deal_id": str(result.inserted_id),
        "product_name": deal_data["product_name"],
        "original_price": float(original_price),
        "offer_price": float(offer_price),
        "discount_percentage": float(discount)
    }, status=201)




@api_view(["GET"])
def get_today_deals(request):

    today = django_timezone.localdate().isoformat()

    deals = deals_collection.find({
        "status": "Active",
        "is_deleted": {"$ne": True},
        "start_date": {"$lte": today},
        "end_date": {"$gte": today}
    }).sort("created_at", -1)

    result = [
        serialize_deal(deal)
        for deal in deals
    ]

    return Response({
        "message": "Today's active deals fetched successfully",
        "date": today,
        "count": len(result),
        "deals": result
    }, status=200)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_deal(request, deal_id):

    if not check_admin(request):
        return Response({
            "message": "Admin access required"
        }, status=403)

    if not ObjectId.is_valid(deal_id):
        return Response({
            "message": "Invalid deal ID"
        }, status=400)

    deal = deals_collection.find_one({
        "_id": ObjectId(deal_id),
        "is_deleted": {"$ne": True}
    })

    if not deal:
        return Response({
            "message": "Deal not found"
        }, status=404)

    if "product_id" in request.data:
        return Response({
            "message": "Product ID cannot be changed"
        }, status=400)

    serializer = DealSerializer(
        data=request.data,
        partial=True
    )

    if not serializer.is_valid():
        return Response({
            "errors": serializer.errors
        }, status=400)

    data = serializer.validated_data

    try:
        original_price = Decimal(str(deal["original_price"]))
        offer_price = data.get(
            "offer_price",
            Decimal(str(deal["offer_price"]))
        )

        start_date = data.get(
            "start_date",
            datetime.strptime(
                deal["start_date"], "%Y-%m-%d"
            ).date()
        )

        end_date = data.get(
            "end_date",
            datetime.strptime(
                deal["end_date"], "%Y-%m-%d"
            ).date()
        )

    except (KeyError, ValueError, TypeError):
        return Response({
            "message": "Existing deal data is invalid"
        }, status=400)

    if offer_price <= 0 or offer_price >= original_price:
        return Response({
            "message": "Offer price must be less than original price"
        }, status=400)

    if start_date > end_date:
        return Response({
            "message": "Start date cannot be after end date"
        }, status=400)

    discount = round(
        ((original_price - offer_price) / original_price) * 100,
        2
    )

    update_data = {
        "offer_price": float(offer_price),
        "discount_percentage": float(discount),
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "offer_title": data.get(
            "offer_title",
            deal.get("offer_title", "Deal of the Day")
        ),
        "status": data.get("status", deal.get("status", True)),
        "updated_at": datetime.now(timezone.utc)
    }

    deals_collection.update_one(
        {"_id": ObjectId(deal_id)},
        {"$set": update_data}
    )

    return Response({
        "message": "Deal updated successfully",
        "discount_percentage": float(discount)
    }, status=200)
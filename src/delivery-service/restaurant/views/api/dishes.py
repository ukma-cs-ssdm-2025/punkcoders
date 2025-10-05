# restaurant/views/api/dishes.py
from rest_framework import status, viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from restaurant.serializers.dishes import DishSerializer
from restaurant.services.dishes import get_all_dishes
from django.http.response import HttpResponseServerError


@extend_schema(tags=["Dishes"])
class DishViewSet(viewsets.ViewSet):
	"""CRUD endpoints for Dish (mock data, no DB yet)."""

	@extend_schema(
		summary="List dishes",
		description="Return hardcoded example dishes (no database yet).",
		responses={
			200: DishSerializer(many=True),
			500: OpenApiResponse(description="Internal server error"),
		},
	)
	def list(self, request):
		data = get_all_dishes()
		serializer = DishSerializer(data, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@extend_schema(
		summary="Retrieve a dish by ID",
		responses={
			200: DishSerializer,
			404: OpenApiResponse(description="Dish not found"),
			500: OpenApiResponse(description="Internal server error"),
		},
	)
	def retrieve(self, request, pk=None):
		data = next((d for d in get_all_dishes() if str(d["id"]) == str(pk)), None)
		if not data:
			return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
		serializer = DishSerializer(data)
		return Response(serializer.data, status=status.HTTP_200_OK)


	@extend_schema(
		summary="Create a dish (mock)",
		responses={
			201: DishSerializer,
			400: OpenApiResponse(description="Bad request"),
			500: OpenApiResponse(description="Internal server error"),
		},
	)
	def create(self, request):
		serializer = DishSerializer(data=request.data)
		if serializer.is_valid():
			# Mock: assign a fake ID and echo back
			data = serializer.validated_data.copy()
			data["id"] = 999
			return Response(data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	@extend_schema(
		summary="Update a dish (mock)",
		responses={
			200: DishSerializer,
			400: OpenApiResponse(description="Bad request"),
			404: OpenApiResponse(description="Dish not found"),
			500: OpenApiResponse(description="Internal server error"),
		},
	)
	def update(self, request, pk=None):
		# Find mock dish
		dish = next((d for d in get_all_dishes() if str(d["id"]) == str(pk)), None)
		if not dish:
			return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
		serializer = DishSerializer(data=request.data)
		if serializer.is_valid():
			data = serializer.validated_data.copy()
			data["id"] = dish["id"]
			return Response(data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	# def partial_update(self, request, pk=None):
	# 	pass


	@extend_schema(
		summary="Delete a dish (mock)",
		responses={
			204: OpenApiResponse(description="Dish deleted"),
			404: OpenApiResponse(description="Dish not found"),
			500: OpenApiResponse(description="Internal server error"),
		},
	)
	def destroy(self, request, pk=None):
		dish = next((d for d in get_all_dishes() if str(d["id"]) == str(pk)), None)
		if not dish:
			return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
		# Mock: pretend to delete
		return Response(status=status.HTTP_204_NO_CONTENT)
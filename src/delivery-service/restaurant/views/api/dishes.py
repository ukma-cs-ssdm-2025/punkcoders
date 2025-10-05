# restaurant/views/api/dishes.py
from rest_framework import status, viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from restaurant.serializers.dishes import DishSerializer
from restaurant.services.dishes import *
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
		if pk is None:
			return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
		data = get_dish_by_id(pk)
		if not data:
			return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
		serializer = DishSerializer(data)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@extend_schema(
		summary="Create a dish (mock)",
		responses={
			201: DishSerializer,
			400: OpenApiResponse(description="Bad request"),
			401: OpenApiResponse(description="Not authorized"),
			403: OpenApiResponse(description="Forbidden"),
			500: OpenApiResponse(description="Internal server error"),
		},
	)
	def create(self, request):
		serializer = DishSerializer(data=request.data)
		if serializer.is_valid():
			# Mock: assign a fake ID and echo back
			data = create_dish(serializer.validated_data.copy())
			return Response(data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@extend_schema(
		summary="Update a dish (mock)",
		responses={
			200: DishSerializer,
			400: OpenApiResponse(description="Bad request"),
			401: OpenApiResponse(description="Not authorized"),
			403: OpenApiResponse(description="Forbidden"),
			404: OpenApiResponse(description="Dish not found"),
			500: OpenApiResponse(description="Internal server error"),
		},
	)
	def update(self, request, pk=None):
		if pk is None:
			return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
		if not has_dish:
			return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
		serializer = DishSerializer(data=request.data)
		if serializer.is_valid():
			data = update_dish(serializer.validated_data.copy())
			return Response(data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	# def partial_update(self, request, pk=None):
	# 	pass

	@extend_schema(
		summary="Delete a dish (mock)",
		responses={
			204: OpenApiResponse(description="Dish deleted"),
			401: OpenApiResponse(description="Not authorized"),
			403: OpenApiResponse(description="Forbidden"),
			404: OpenApiResponse(description="Dish not found"),
			500: OpenApiResponse(description="Internal server error"),
		},
	)
	def destroy(self, request, pk=None):
		if pk is None:
			return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
		if not has_dish(pk):
			return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
		delete_dish(pk)
		return Response(status=status.HTTP_204_NO_CONTENT)
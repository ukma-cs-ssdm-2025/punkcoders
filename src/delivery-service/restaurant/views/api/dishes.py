from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from restaurant.serializers.dishes import DishSerializer
from restaurant.services.dishes import get_all_dishes


class DishListView(APIView):
	"""Returns a list of all dishes (mock data)."""

	@extend_schema(
		summary="List dishes",
		description="Returns hardcoded example dishes (no database yet).",
		responses={200: DishSerializer(many=True)},
		tags=["Dishes"],
	)
	def get(self, request):
		data = get_all_dishes()
		serializer = DishSerializer(data, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

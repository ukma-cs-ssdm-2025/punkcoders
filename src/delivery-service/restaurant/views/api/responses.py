from drf_spectacular.utils import OpenApiResponse

RESPONSES = {
    204: lambda thing : OpenApiResponse(description=f"{thing} deleted"),
    400: lambda: OpenApiResponse(description="Bad request"),
    401: lambda: OpenApiResponse(description="Not authorized - use the admin panel for now"),
    403: lambda: OpenApiResponse(description="Forbidden - use the admin panel for now"),
    404: lambda thing : OpenApiResponse(description=f"{thing} not found"),
    500: lambda: OpenApiResponse(description="Internal server error"),
}
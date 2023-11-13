from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from .schemaSerializer import *

getReportedChannelSchema = extend_schema(
    summary="Get list of all reported channels",
    description="You need permission from admin to get information of all reported channels",
    responses = {
        200: OpenApiResponse(response=SuccessGetReportedChannelSerializer, description="Get list of reported channels successfully"),
        401: OpenApiResponse(response=GeneralMessageSerializer, description="You need permission to make this action")
    }
)

getReportedUserSchema = extend_schema(
    summary="Get list of all reported users",
    description="You need permission from admin to get information of all reported users",
    responses = {
        200: OpenApiResponse(response=SuccessGetReportedUserSerializer, description="Get list of reported users successfully"),
        401: OpenApiResponse(response=GeneralMessageSerializer, description="You need permission to make this action")
    }
)

createReportSchema = extend_schema(
    summary="Create a particular report",
    description="You need to provide access token to report a user or a channel \n\n \
    Note:  In your request, you need to provide reported user or reported channel and they have to exist",
    responses= {
        200: OpenApiResponse(response=SuccessCreateReportSerializer, description="Reported successfully"),
        400: OpenApiResponse(response=GeneralMessageSerializer, description="Reported fail!"),
        401: OpenApiResponse(response=GeneralMessageSerializer, description="You need access token to report an user or a channel"),
    }
)

getReportDetailSchema = extend_schema(
    summary="Get detailf of some reports",
    description="You need permission from admin to get detail information of reports",
    responses = {
        200: OpenApiResponse(response=SuccessGetReportDetailSerializer, description="Get detail information of some reports successfully"),
        401: OpenApiResponse(response=GeneralMessageSerializer, description="You need permission to make this action"),
        404: OpenApiResponse(response=GeneralMessageSerializer, description="Report not found")
    }
)

processReportSchema = extend_schema(
    summary="Handle a particular report",
    description="You need permission from admin to handle a particular report",
    responses= {
        200: OpenApiResponse(response=GeneralMessageSerializer, description="The report was processed successfully!"),
        401: OpenApiResponse(response=GeneralMessageSerializer, description="You need permission to make this action"),
        404: OpenApiResponse(response=GeneralMessageSerializer, description="Report not found")
    }
)

deleteReportSchema = extend_schema(
    summary="Delete a particular report",
    description="You need permission from admin to make this action",
    responses={
        200: OpenApiResponse(response=GeneralMessageSerializer, description="Delete the report successfully"),
        401: OpenApiResponse(response=GeneralMessageSerializer, description="You need permission to make this action"),
        404: OpenApiResponse(response=GeneralMessageSerializer, description="Report not found")
    }
)
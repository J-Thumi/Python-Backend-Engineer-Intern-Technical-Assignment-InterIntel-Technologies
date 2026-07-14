import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    SenderSerializer,
    SenderResponseSerializer
)


logger = logging.getLogger(__name__)


class BulkNotificationView(APIView):

    def post(self, request):

        logger.info(
            "Bulk notification request received"
        )

        serializer = SenderSerializer(
            data=request.data
        )


        if not serializer.is_valid():

            logger.warning(
                "Notification validation failed. Errors=%s",
                serializer.errors
            )

            return Response(
                {
                    "success": False,
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


        try:

            sender = serializer.save()

            logger.info(
                "Bulk notification processing completed for sender id=%s",
                sender.id
            )


            sender_data = SenderResponseSerializer(sender)


            return Response(
                {
                    "message": "Notifications created successfully.",
                    "sender": sender_data.data,
                    "notifications_created": sender.notifications.count(),
                },
                status=status.HTTP_201_CREATED,
            )


        except Exception as e:

            logger.exception(
                "Bulk notification creation failed. Error=%s",
                str(e)
            )

            return Response(
                {
                    "success": False,
                    "message": "Unable to create notifications."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
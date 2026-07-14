import logging

from rest_framework import serializers
from django.db import transaction

from .models import Sender, Notification


logger = logging.getLogger(__name__)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "title",
            "message",
            "channel"
        ]


class SenderSerializer(serializers.ModelSerializer):

    notifications = NotificationSerializer(
        many=True
    )

    class Meta:
        model = Sender
        fields = [
            "name",
            "email",
            "notifications"
        ]


    @transaction.atomic
    def create(self, validated_data):

        notifications_data = validated_data.pop("notifications")

        logger.info(
            "Creating sender with email=%s and notifications_count=%s",
            validated_data.get("email"),
            len(notifications_data)
        )

        try:
            sender = Sender.objects.create(**validated_data)

            notifications = [
                Notification(
                    title=data["title"],
                    message=data["message"],
                    channel=data["channel"],
                    sender=sender,
                )
                for data in notifications_data
            ]

            Notification.objects.bulk_create(notifications)

            logger.info(
                "Successfully created sender id=%s with %s notifications",
                sender.id,
                len(notifications)
            )

            return sender

        except Exception as e:

            logger.exception(
                "Failed creating sender email=%s. Error=%s",
                validated_data.get("email"),
                str(e)
            )

            raise

class SenderResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sender
        fields = [
            "id",
            "name",
            "email",
        ]
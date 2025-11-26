from rest_framework import serializers


class PaginationSerializer(serializers.Serializer):
    offset = serializers.IntegerField(default=0, required=False)
    limit = serializers.IntegerField(default=0, required=False)


class APIResponseSerializer(serializers.Serializer):
    data = serializers.JSONField(required=False, allow_null=True)
    meta = serializers.DictField(
        child=serializers.JSONField(),
        required=False,
        allow_null=True,
        default=dict,
    )
    errors = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        default=list,
    )
    pagination = PaginationSerializer(required=False)

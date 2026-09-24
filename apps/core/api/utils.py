from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers


def get_object(model_or_queryset, **kwargs):
    """
    Reuse `get_object_or_404` since it already supports both a Model
    and a queryset, but return `None` instead of raising, so callers
    (services/selectors) can decide what "not found" means for them.
    """
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None


def inline_serializer(*, fields, data=None, **kwargs):
    """
    Build a throwaway nested serializer without declaring a class for it.

    Example:

        weeks = inline_serializer(many=True, fields={
            "id": serializers.IntegerField(),
            "number": serializers.IntegerField(),
        })
    """
    serializer_class = type("InlineSerializer", (serializers.Serializer,), fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)

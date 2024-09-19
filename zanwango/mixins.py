from typing import Any

from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from zanwango.generics import GenericReadAPIView


class RetrieveModelMixin(mixins.RetrieveModelMixin):
    def retrieve(
        self: GenericAPIView, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        if isinstance(self, GenericReadAPIView):
            if schema_out := self.get_schema_out():
                instance = self.get_object()
                model = schema_out.model_validate(instance)
                return Response(model.model_dump())

        return super().retrieve(request, *args, **kwargs)

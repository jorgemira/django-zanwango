from typing import Any

from pydantic import TypeAdapter
from rest_framework import mixins
from rest_framework.generics import GenericAPIView as DRFGenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from zanwango.generics import GenericReadAPIView


class RetrieveModelMixin(mixins.RetrieveModelMixin):
    def retrieve(
        self: DRFGenericAPIView, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        if isinstance(self, GenericReadAPIView):
            if schema_out := self.get_schema_out():
                instance = self.get_object()
                model_dump = schema_out.model_validate(instance).model_dump()
                return Response(model_dump)

        return super().retrieve(request, *args, **kwargs)


class ListModelMixin(mixins.ListModelMixin):
    def list(
        self: DRFGenericAPIView, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        if isinstance(self, GenericReadAPIView):
            if schema_out := self.get_schema_out():
                type_adapter = TypeAdapter(list[schema_out])  # type: ignore[valid-type]
                queryset = self.filter_queryset(self.get_queryset())

                if (page := self.paginate_queryset(queryset)) is not None:
                    models = type_adapter.validate_python(page)
                    model_dumps = [model.model_dump() for model in models]
                    return self.get_paginated_response(model_dumps)

                models = type_adapter.validate_python(queryset)
                model_dumps = [model.model_dump() for model in models]
                return Response(model_dumps)

        return super().list(request, *args, **kwargs)

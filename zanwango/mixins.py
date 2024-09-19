from typing import Any

from pydantic import TypeAdapter
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


class ListModelMixin(mixins.ListModelMixin):
    def list(
        self: GenericAPIView, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        if isinstance(self, GenericReadAPIView) and ():
            if schema_out := self.get_schema_out():
                type_adapter = TypeAdapter(list[schema_out])  # type: ignore[valid-type]
                queryset = self.filter_queryset(self.get_queryset())

                if (page := self.paginate_queryset(queryset)) is not None:
                    models = type_adapter.validate_python(page)
                    dumped_models = [model.model_dump() for model in models]
                    return self.get_paginated_response(dumped_models)

                models = type_adapter.validate_python(queryset)
                return Response([model.model_dump() for model in models])

        return super().list(request, *args, **kwargs)

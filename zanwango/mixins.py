from typing import Any

from django.db.models import Model
from pydantic import TypeAdapter
from rest_framework import mixins
from rest_framework.generics import GenericAPIView as DRFGenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from zanwango.generics import GenericReadAPIView, GenericWriteAPIView
from zanwango.schemas import Schema


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


class CreateModelMixin(mixins.CreateModelMixin):
    def create(
        self: DRFGenericAPIView, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        if not isinstance(self, (GenericWriteAPIView | GenericReadAPIView)):
            return super().create(request, *args, **kwargs)

        serializer = None

        if isinstance(self, GenericWriteAPIView) and (
            schema_in := self.get_schema_in()
        ):
            schema_data = schema_in.model_validate(request.data)
            instance = self.perform_create_dz(schema_data)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            instance = serializer.instance

        if isinstance(self, GenericReadAPIView) and (
            schema_out := self.get_schema_out()
        ):
            data = schema_out.model_validate(instance).model_dump()
        else:
            if serializer is None:
                serializer = self.get_serializer(instance)
            data = serializer.data

        headers = self.get_success_headers(data)
        return Response(data, status=HTTP_201_CREATED, headers=headers)

    def perform_create_dz(self: GenericWriteAPIView, schema_data: Schema) -> Model:
        return self.get_model()._default_manager.create(**schema_data.model_dump())

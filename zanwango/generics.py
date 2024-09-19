from django.db import models
from rest_framework import generics

from zanwango import schemas


class GenericReadAPIView(generics.GenericAPIView):
    schema_out: type[schemas.Schema] | None = None

    def get_schema_out(self) -> type[schemas.Schema] | None:
        return self.schema_out


class GenericWriteAPIView(generics.GenericAPIView):
    schema_in: type[schemas.Schema] | None = None
    model: type[models.Model] | None = None

    def get_schema_in(self) -> type[schemas.Schema] | None:
        return self.schema_in

    def get_model(self) -> type[models.Model]:
        if self.model is not None:
            return self.model
        model: type[models.Model] = self.get_queryset().model
        return model


class GenericAPIView(GenericReadAPIView, GenericWriteAPIView):
    pass

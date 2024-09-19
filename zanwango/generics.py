from rest_framework import generics

from zanwango import schemas


class GenericReadAPIView(generics.GenericAPIView):
    schema_out: type[schemas.Schema] | None = None

    def get_schema_out(self) -> type[schemas.Schema] | None:
        return self.schema_out

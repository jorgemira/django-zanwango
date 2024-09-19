from rest_framework import viewsets

from zanwango import generics, mixins


class GenericReadViewSet(viewsets.ViewSetMixin, generics.GenericReadAPIView):
    pass


class ReadOnlyModelViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericReadViewSet
):
    pass

import datetime
from haystack import indexes
from szach.models import Szach


class SzachIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='stamp')
    content_auto = indexes.EdgeNgramField(model_attr='subject')

    def get_model(self):
        return Szach

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


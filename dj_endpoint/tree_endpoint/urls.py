from django.urls import path
from tree_endpoint.views import ParaphraseView

urlpatterns = [
    path('paraphrase', ParaphraseView.as_view(), name='paraphrase'),
]

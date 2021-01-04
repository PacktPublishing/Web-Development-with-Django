from django.urls import path

from .views import BookRecordFormView, FormSuccessView

urlpatterns = [
    path('new_book_record', BookRecordFormView.as_view(), name='book_record_form'),
    path('entry_success', FormSuccessView.as_view(), name='form_success')
]

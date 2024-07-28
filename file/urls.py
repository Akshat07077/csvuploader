from django.urls import path
from . import views
from .views import SignupAPIView, LoginAPIView, CSVUploadAPIView


urlpatterns = [
    path('api/signup/', SignupAPIView.as_view(), name='api_signup'),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/upload-csv/', CSVUploadAPIView.as_view(), name='api_upload_csv'),
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
    path('view/<int:file_id>/', views.view_csv, name='view_csv'),
    path('edit/<int:file_id>/<int:row_index>/', views.edit_csv_row, name='edit_csv_row'),
    path('delete/<int:file_id>/', views.delete_csv, name='delete_csv'),
    path('export/<int:file_id>/', views.exportCsv, name='exportCsv'),
]

from django.urls import path


from . import views

app_name = 'site'
urlpatterns = [
    path('site_home/', views.home, name='home'),
    path('new_project/', views.new_project, name='new_project'),
    path('project/<project_id>/', views.project, name='project'),
    path('edit_project/<project_id>/', views.edit_project, name='edit_project'),
    path('delete_project/<project_id>/', views.delete_project, name='delete_project'),
    path('delete_item/<project_id>/', views.delete_item, name='delete_item'),
    path('delete_all/<project_id>/', views.delete_all, name='delete_all'),
    path('add_zip_file/<project_id>/', views.add_zip_file, name='add_zip_file'),
    path('create_subfolder/<project_id>/', views.create_subfolder, name='create_subfolder'),
    path('add_file/<project_id>/', views.add_file, name='add_file'),
]

from django.urls import path
from . import views

urlpatterns=[
    # Home page
    path('', views.loginPage, name='loginPage'),
    path('home/',views.home,name = 'home'),
    # path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('registerUser/',views.registerUser,name='registerUser'),

    #proposals urls

    path('list/', views.list_proposals, name='list_proposals'),
    path('create/', views.create_proposal, name='create_proposal'),
    path('<int:proposal_id>/', views.view_proposal, name='view_proposal'),
    path('<int:proposal_id>/edit/', views.edit_proposal, name='edit_proposal'),
    path('<int:proposal_id>/delete/', views.delete_proposal, name='delete_proposal'),
    path('proposals/', views.create_section_proposal,name='create_section_proposal'),
    path('reorder_proposals/', views.reorder_proposals, name='reorder_proposals'),
    path('save_record/<int:record_id>/',views.save_record,name='save_record'),
    path('saved_prop_display/',views.saved_prop_display,name = 'saved_prop_display'),
    path('view_saved_proposal/<int:proposal_id>/',views.view_saved_proposal,name='view_saved_proposal'),
    path('proposal/<int:proposal_id>/pdf/', views.generate_pdf, name='proposal_pdf'),

    # path('reorder_sections/<int:proposal_id>/', views.reorder_sections, name='reorder_sections'),


]
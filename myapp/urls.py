
from django.contrib import admin
from django.urls import path, include

from myapp import views
from scrapnet import settings

urlpatterns = [
    path('',views.login),
    path('logout',views.logout),
    path('login_post',views.login_post),
    path('admin_home',views.admin_home),
    path('add_category',views.add_category),
    path('admin_view_category',views.admin_view_category),

    path('feedback_list_view',views.feedback_list_view),
    path('feedback_list_view_search',views.feedback_list_view_search),

    path('complaint_list_view',views.complaint_list_view),
    path('complaint_list_view_search',views.complaint_list_view_search),

    path('admin_view_user',views.admin_view_user),
    path('admin_view_agency',views.admin_view_agency),
    path('delete_cat/<id>',views.delete_cat),
    path('accept_agency/<id>',views.accept_agency),
    path('reject_agency/<id>',views.reject_agency),
    path('send_reply/<id>',views.send_reply),
    path('sendreply_post',views.sendreply_post),
    path('view_scrap',views.view_scrap),



    path('agency_reg',views.agency_reg),
    path('agency_home',views.agency_home),
    path('view_profile',views.view_profile),
    path('add_scrap',views.add_scrap),
    path('agency_view_scrap',views.agency_view_scrap),
    path('agency_view_feedback',views.agency_view_feedback),
    path('agency_view_request',views.agency_view_request),
    path('delete_scrap/<id>',views.delete_scrap),
    path('edit_scrap/<id>',views.edit_scrap),
    path('accept_request/<id>',views.accept_request),
    path('reject_request/<id>',views.reject_request),
    path('edit_scrap_post',views.edit_scrap_post),
    path('edit_profile',views.edit_profile),
    path('edit_profile_post',views.edit_profile_post),



    path('user_reg',views.user_reg),
    path('user_home',views.user_home),
    path('user_view_profile',views.user_view_profile),
    path('user_edit_profile',views.user_edit_profile),
    path('user_edit_profile_post',views.user_edit_profile_post),
    path('user_view_agency',views.user_view_agency),
    path('user_view_scarp',views.user_view_scarp),
    path('user_send_request_post',views.user_send_request_post),
    path('user_view_more/<id>',views.user_view_more),
    path('user_send_request/<id>',views.user_send_request),
    path('user_view_request',views.user_view_request),
    path('send_complaint',views.send_complaint),
    path('user_view_complaint',views.user_view_complaint),
    path('user_send_feedback/<id>',views.user_send_feedback),


]

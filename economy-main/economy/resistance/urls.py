from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('login/', auth_views.LoginView.as_view(
        template_name='resistance/login.html',
        redirect_authenticated_user=True),
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.admin_profile, name='admin_profile'),
    path('users/', views.MyUserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.MyUserDetailView.as_view(), name='user-detail'),
    path('users/new/', views.MyUserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/edit/', views.MyUserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', views.MyUserDeleteView.as_view(), name='user-delete'),

    path('infofunds/', views.InformationFundListView.as_view(), name='informationfund-list'),
    path('infofunds/<int:pk>/', views.InformationFundDetailView.as_view(), name='informationfund-detail'),
    path('infofunds/new/', views.InformationFundCreateView.as_view(), name='informationfund-create'),
    path('infofunds/<int:pk>/edit/', views.InformationFundUpdateView.as_view(), name='informationfund-update'),
    path('infofunds/<int:pk>/delete/', views.InformationFundDeleteView.as_view(), name='informationfund-delete'),

    path('infofunds/<int:infofund_pk>/fund/new/', views.FundCreateView.as_view(), name='fund-create-for-infofund'),
    path('funds/new/', views.FundCreateView.as_view(), name='fund-create'),
    path('funds/<int:pk>/', views.FundDetailView.as_view(), name='fund-detail'),
    path('funds/<int:pk>/edit/', views.FundUpdateView.as_view(), name='fund-update'),
    path('funds/<int:pk>/delete/', views.FundDeleteView.as_view(), name='fund-delete'),
    path('funds/', views.FundListView.as_view(), name='fund-list'),

    path('deprivations/', views.DeprivationListView.as_view(), name='deprivation-list'),
    path('deprivations/<int:pk>/', views.DeprivationDetailView.as_view(), name='deprivation-detail'),
    path('deprivations/new/', views.DeprivationCreateView.as_view(), name='deprivation-create'),
    path('deprivations/<int:pk>/edit/', views.DeprivationUpdateView.as_view(), name='deprivation-update'),
    path('deprivations/<int:pk>/delete/', views.DeprivationDeleteView.as_view(), name='deprivation-delete'),

    path('deprivations/<int:deprivation_pk>/report/new/', views.ReportCreateView.as_view(), name='report-create'),
    path('reports/<int:pk>/', views.ReportDetailView.as_view(), name='report-detail'),
    path('reports/<int:pk>/edit/', views.ReportUpdateView.as_view(), name='report-update'),
    path('reports/<int:pk>/delete/', views.ReportDeleteView.as_view(), name='report-delete'),
    path('reports/', views.ReportListView.as_view(), name='report-list'),
    path("dashboard/", views.AdminDashboardView.as_view(), name="dashboard"),

]
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse


from .models import MyUser, InformationFund, Fund, Deprivation, Report
from .forms import MyUserForm, InformationFundForm, FundForm, DeprivationForm, ReportForm


def is_admin(user):
    return user.is_authenticated and user.is_admin


admin_required = method_decorator(user_passes_test(is_admin), name='dispatch')
login_required_m = method_decorator(login_required, name='dispatch')


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'resistance/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['funds_count'] = InformationFund.objects.count()
        context['deprivations_count'] = Deprivation.objects.count()
        context['reports_count'] = Report.objects.count()
        context['users_count'] = MyUser.objects.count()
        return context

@admin_required
class MyUserListView(ListView):
    model = MyUser
    template_name = 'resistance/myuser_list.html'
    context_object_name = 'users'


@admin_required
class MyUserDetailView(DetailView):
    model = MyUser
    template_name = 'resistance/myuser_detail.html'
    context_object_name = 'user'


@admin_required
class MyUserCreateView(CreateView):
    model = MyUser
    form_class = MyUserForm
    template_name = 'resistance/myuser_form.html'
    success_url = reverse_lazy('user-list')


@admin_required
class MyUserUpdateView(UpdateView):
    model = MyUser
    form_class = MyUserForm
    template_name = 'resistance/myuser_form.html'
    success_url = reverse_lazy('user-list')


@admin_required
class MyUserDeleteView(DeleteView):
    model = MyUser
    template_name = 'resistance/myuser_confirm_delete.html'
    success_url = reverse_lazy('user-list')


@login_required_m
class InformationFundListView(ListView):
    model = InformationFund
    template_name = 'resistance/informationfund_list.html'
    context_object_name = 'funds'


@login_required_m
class InformationFundDetailView(DetailView):
    model = InformationFund
    template_name = 'resistance/informationfund_detail.html'
    context_object_name = 'fund'


@login_required_m
class InformationFundCreateView(CreateView):
    model = InformationFund
    form_class = InformationFundForm
    template_name = 'resistance/informationfund_form.html'

    def get_success_url(self):
        return reverse_lazy('informationfund-detail', kwargs={'pk': self.object.pk})


@login_required_m
class InformationFundUpdateView(UpdateView):
    model = InformationFund
    form_class = InformationFundForm
    template_name = 'resistance/informationfund_form.html'

    def get_success_url(self):
        return reverse_lazy('informationfund-detail', kwargs={'pk': self.object.pk})


@login_required_m
class InformationFundDeleteView(DeleteView):
    model = InformationFund
    template_name = 'resistance/informationfund_confirm_delete.html'
    success_url = reverse_lazy('informationfund-list')


@login_required_m
class FundListView(ListView):
    model = Fund
    template_name = 'resistance/fund_list.html'
    context_object_name = 'funds'


@login_required_m
class FundDetailView(DetailView):
    model = Fund
    template_name = 'resistance/fund_detail.html'
    context_object_name = 'fund'


@login_required_m
class FundCreateView(CreateView):
    model = Fund
    form_class = FundForm
    template_name = 'resistance/fund_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['fund'] = self.kwargs.get('infofund_pk')
        return initial

    def get_success_url(self):
        return reverse_lazy('informationfund-detail', kwargs={'pk': self.object.fund.pk})


@login_required_m
class FundUpdateView(UpdateView):
    model = Fund
    form_class = FundForm
    template_name = 'resistance/fund_form.html'

    def get_success_url(self):
        return reverse_lazy('informationfund-detail', kwargs={'pk': self.object.fund.pk})


@login_required_m
class FundDeleteView(DeleteView):
    model = Fund
    template_name = 'resistance/fund_confirm_delete.html'

    def get_success_url(self):
        infofund_pk = self.object.fund.pk
        return reverse_lazy('informationfund-detail', kwargs={'pk': infofund_pk})


@login_required_m
class DeprivationListView(ListView):
    model = Deprivation
    template_name = 'resistance/deprivation_list.html'
    context_object_name = 'deprivations'


@login_required_m
class DeprivationDetailView(DetailView):
    model = Deprivation
    template_name = 'resistance/deprivation_detail.html'
    context_object_name = 'deprivation'


@login_required_m
class DeprivationCreateView(CreateView):
    model = Deprivation
    form_class = DeprivationForm
    template_name = 'resistance/deprivation_form.html'

    def get_success_url(self):
        return reverse_lazy('deprivation-detail', kwargs={'pk': self.object.pk})


@login_required_m
class DeprivationUpdateView(UpdateView):
    model = Deprivation
    form_class = DeprivationForm
    template_name = 'resistance/deprivation_form.html'

    def get_success_url(self):
        return reverse_lazy('deprivation-detail', kwargs={'pk': self.object.pk})


@login_required_m
class DeprivationDeleteView(DeleteView):
    model = Deprivation
    template_name = 'resistance/deprivation_confirm_delete.html'
    success_url = reverse_lazy('deprivation-list')


@login_required_m
class ReportListView(ListView):
    model = Report
    template_name = 'resistance/report_list.html'
    context_object_name = 'reports'


@login_required_m
class ReportDetailView(DetailView):
    model = Report
    template_name = 'resistance/report_detail.html'
    context_object_name = 'report'


@login_required_m
class ReportCreateView(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'resistance/report_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['deprivation'] = self.kwargs.get('deprivation_pk')
        return initial

    def get_success_url(self):
        return reverse_lazy('deprivation-detail', kwargs={'pk': self.object.deprivation.pk})


@login_required_m
class ReportUpdateView(UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'resistance/report_form.html'

    def get_success_url(self):
        return reverse_lazy('deprivation-detail', kwargs={'pk': self.object.deprivation.pk})


@login_required_m
class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'resistance/report_confirm_delete.html'

    def get_success_url(self):
        deprivation_pk = self.object.deprivation.pk
        return reverse_lazy('deprivation-detail', kwargs={'pk': deprivation_pk})
class export_reports_excel():
    def export_reports_excel(request):
        reports = Report.objects.all().values('deprivation__name', 'date', 'address', 'subject', 'desc', 'member')
        df = pd.DataFrame(list(reports))
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="reports.xlsx"'
        df.to_excel(response, index=False)
        return responseeconomy-main/economy/resistance/templates
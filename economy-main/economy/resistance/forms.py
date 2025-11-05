from django import forms
from .models import MyUser, InformationFund, Fund, Deprivation, Report

class MyUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['phone', 'username', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class InformationFundForm(forms.ModelForm):
    class Meta:
        model = InformationFund
        fields = ['name', 'nCode', 'fName', 'phone', 'cGroup']

class FundForm(forms.ModelForm):
    class Meta:
        model = Fund
        fields = ['fund', 'member', 'NumberOfLoans', 'mony', 'quantity', 'AfterTheSize', 'course', 'bazaar', 'name_course', 'member_course', 'name_teacher', 'phone_teacher', 'bazzar_desc']
        widgets = {
            'fund': forms.HiddenInput(),
            'course': forms.RadioSelect,
            'bazaar': forms.RadioSelect,
        }

class DeprivationForm(forms.ModelForm):
    class Meta:
        model = Deprivation
        fields = ['name', 'nCode', 'fName', 'phone', 'cGroup', 'fund_name']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['deprivation', 'date', 'address', 'subject', 'desc', 'member']
        widgets = {
            'deprivation': forms.HiddenInput(),
        }

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'profile_image']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'profile_image': forms.FileInput(attrs={'class':'form-control'}),
        }
# resistance/tests.py

import datetime
from django.test import TestCase, Client
from django.urls import reverse
from .models import MyUser, InformationFund, Fund, Deprivation, Report


# --- تست‌های مدل MyUser ---

class MyUserViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = MyUser.objects.create_user(
            phone='09123456789',
            username='testuser',
            password='testpassword123'
        )

        self.create_data = {
            'phone': '09987654321',
            'username': 'newuser',
            'password': 'newpassword123'
        }

        self.update_data = {
            'phone': '09123456789',
            'username': 'updateduser',
            'password': 'updatedpassword'
        }

    def test_user_list_view(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertTemplateUsed(response, 'resistance/myuser_list.html')

    def test_user_detail_view(self):
        response = self.client.get(reverse('user-detail', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertTemplateUsed(response, 'resistance/myuser_detail.html')

    def test_user_create_view(self):
        response = self.client.post(reverse('user-create'), self.create_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MyUser.objects.count(), 2)
        new_user = MyUser.objects.get(phone=self.create_data['phone'])
        self.assertEqual(new_user.username, self.create_data['username'])

    def test_user_update_view(self):
        response = self.client.post(reverse('user-update', args=[self.user.pk]), self.update_data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, self.update_data['username'])

    def test_user_delete_view(self):
        response = self.client.post(reverse('user-delete', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MyUser.objects.count(), 0)


# --- تست‌های مدل InformationFund ---

class InformationFundViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.info_fund = InformationFund.objects.create(
            name="صندوق نمونه",
            nCode="1234567890",
            fName="پدر نمونه",
            phone="09111111111"
        )

        self.create_data = {
            'name': 'صندوق جدید',
            'nCode': '0987654321',
            'fName': 'پدر جدید',
            'phone': '09222222222',
            'cGroup': 'G1'
        }

        self.update_data = {
            'name': 'صندوق ویرایش شده',
            'nCode': '1234567890',
            'fName': 'پدر ویرایش شده',
            'phone': '09111111111',
            'cGroup': 'G2'
        }

    def test_informationfund_list_view(self):
        response = self.client.get(reverse('informationfund-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.info_fund.name)
        self.assertTemplateUsed(response, 'resistance/informationfund_list.html')

    def test_informationfund_detail_view(self):
        response = self.client.get(reverse('informationfund-detail', args=[self.info_fund.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.info_fund.name)
        self.assertTemplateUsed(response, 'resistance/informationfund_detail.html')

    def test_informationfund_create_view(self):
        response = self.client.post(reverse('informationfund-create'), self.create_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(InformationFund.objects.count(), 2)
        self.assertTrue(InformationFund.objects.filter(name=self.create_data['name']).exists())

    def test_informationfund_update_view(self):
        response = self.client.post(reverse('informationfund-update', args=[self.info_fund.pk]), self.update_data)
        self.assertEqual(response.status_code, 302)
        self.info_fund.refresh_from_db()
        self.assertEqual(self.info_fund.name, self.update_data['name'])

    def test_informationfund_delete_view(self):
        response = self.client.post(reverse('informationfund-delete', args=[self.info_fund.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(InformationFund.objects.count(), 0)


# --- تست‌های مدل Fund ---

class FundViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.info_fund1 = InformationFund.objects.create(name="صندوق پایه ۱", nCode="111", fName="پدر ۱", phone="09111")
        self.info_fund2 = InformationFund.objects.create(name="صندوق پایه ۲", nCode="222", fName="پدر ۲", phone="09222")

        self.fund = Fund.objects.create(
            fund=self.info_fund1,
            member="10",
            NumberOfLoans="5",
            mony="100000",
            quantity="50000",
            AfterTheSize="1000",
            course="Y",
            bazaar="N"
        )

        self.create_data = {
            'fund': self.info_fund2.pk,
            'member': '20',
            'NumberOfLoans': '10',
            'mony': '200000',
            'quantity': '100000',
            'AfterTheSize': '2000',
            'course': 'N',
            'bazaar': 'Y',
            'bazzar_desc': 'توضیحات بازارچه'
        }

        self.update_data = dict(self.create_data)
        self.update_data['member'] = '25'  # Data must be complete for update
        self.update_data['fund'] = self.info_fund1.pk  # fund is OneToOne, must use existing pk for update

    def test_fund_list_view(self):
        response = self.client.get(reverse('fund-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.fund.member)
        self.assertTemplateUsed(response, 'resistance/fund_list.html')

    def test_fund_detail_view(self):
        response = self.client.get(reverse('fund-detail', args=[self.fund.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.fund.member)
        self.assertTemplateUsed(response, 'resistance/fund_detail.html')

    def test_fund_create_view(self):
        response = self.client.post(reverse('fund-create'), self.create_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Fund.objects.count(), 2)
        self.assertTrue(Fund.objects.filter(member=self.create_data['member']).exists())

    def test_fund_update_view(self):
        # Note: self.update_data uses self.info_fund1.pk which is already linked to self.fund
        response = self.client.post(reverse('fund-update', args=[self.fund.pk]), self.update_data)
        self.assertEqual(response.status_code, 302)
        self.fund.refresh_from_db()
        self.assertEqual(self.fund.member, self.update_data['member'])

    def test_fund_delete_view(self):
        response = self.client.post(reverse('fund-delete', args=[self.fund.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Fund.objects.count(), 0)


# --- تست‌های مدل Deprivation ---

class DeprivationViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.deprivation = Deprivation.objects.create(
            name="فرد محروم",
            nCode="1234567890",
            fName="پدر فرد",
            phone="09333333333",
            cGroup="G1"
        )

        self.create_data = {
            'name': 'فرد جدید',
            'nCode': '0987654321',
            'fName': 'پدر جدید',
            'phone': '09444444444',
            'cGroup': 'G2',
            'fund_name': 'صندوق الف'
        }

        self.update_data = dict(self.create_data)
        self.update_data['name'] = 'فرد ویرایش شده'
        self.update_data['phone'] = '09333333333'  # Keep unique phone for update

    def test_deprivation_list_view(self):
        response = self.client.get(reverse('deprivation-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.deprivation.name)
        self.assertTemplateUsed(response, 'resistance/deprivation_list.html')

    def test_deprivation_detail_view(self):
        response = self.client.get(reverse('deprivation-detail', args=[self.deprivation.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.deprivation.name)
        self.assertTemplateUsed(response, 'resistance/deprivation_detail.html')

    def test_deprivation_create_view(self):
        response = self.client.post(reverse('deprivation-create'), self.create_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Deprivation.objects.count(), 2)

    def test_deprivation_update_view(self):
        response = self.client.post(reverse('deprivation-update', args=[self.deprivation.pk]), self.update_data)
        self.assertEqual(response.status_code, 302)
        self.deprivation.refresh_from_db()
        self.assertEqual(self.deprivation.name, self.update_data['name'])

    def test_deprivation_delete_view(self):
        response = self.client.post(reverse('deprivation-delete', args=[self.deprivation.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Deprivation.objects.count(), 0)


# --- تست‌های مدل Report ---

class ReportViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.deprivation1 = Deprivation.objects.create(name="فرد ۱", nCode="111", fName="پدر ۱", phone="09111",
                                                       cGroup="G1")
        self.deprivation2 = Deprivation.objects.create(name="فرد ۲", nCode="222", fName="پدر ۲", phone="09222",
                                                       cGroup="G2")

        self.report = Report.objects.create(
            deprivation=self.deprivation1,
            date=datetime.date(2025, 1, 1),
            address="آدرس نمونه",
            subject="موضوع نمونه",
            desc="توضیحات نمونه",
            member="5"
        )

        self.create_data = {
            'deprivation': self.deprivation2.pk,
            'date': '2025-02-01',  # jDateField accepts YYYY-MM-DD string
            'address': 'آدرس جدید',
            'subject': 'موضوع جدید',
            'desc': 'توضیحات جدید',
            'member': '10'
        }

        self.update_data = dict(self.create_data)
        self.update_data['subject'] = 'موضوع ویرایش شده'
        self.update_data['deprivation'] = self.deprivation1.pk  # Use existing pk for update

    def test_report_list_view(self):
        response = self.client.get(reverse('report-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.report.subject)
        self.assertTemplateUsed(response, 'resistance/report_list.html')

    def test_report_detail_view(self):
        response = self.client.get(reverse('report-detail', args=[self.report.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.report.subject)
        self.assertTemplateUsed(response, 'resistance/report_detail.html')

    def test_report_create_view(self):
        response = self.client.post(reverse('report-create'), self.create_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Report.objects.count(), 2)
        self.assertTrue(Report.objects.filter(subject=self.create_data['subject']).exists())

    def test_report_update_view(self):
        response = self.client.post(reverse('report-update', args=[self.report.pk]), self.update_data)
        self.assertEqual(response.status_code, 302)
        self.report.refresh_from_db()
        self.assertEqual(self.report.subject, self.update_data['subject'])

    def test_report_delete_view(self):
        response = self.client.post(reverse('report-delete', args=[self.report.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Report.objects.count(), 0)
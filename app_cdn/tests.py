from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from app_cdn.models import Project, Item

User = get_user_model()


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='user1', email='user@mail.com1')
        self.user.set_password('testpass1')
        self.user.is_confirmed = True
        self.user.is_active = True
        self.user.save()

        self.admin = User.objects.create(
            username='admin',
            is_superuser=True,
            is_staff=True,
        )
        self.admin.set_password('testpass1')
        self.admin.save()

        self.project = Project.objects.create(
            name='project1',
            description='description1',
        )
        self.item = Item.objects.create(
            project=self.project,
            category='category1',
            description='description1',
            file='file1',
        )

    def test_home_GET(self):
        self.client.login(username='user1', password='testpass1')
        response = self.client.get(reverse('cdn:home'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='admin', password='testpass1')
        response = self.client.get(reverse('cdn:home'))
        self.assertEqual(response.status_code, 200)

    def test_new_project_GET(self):
        self.client.login(username='user1', password='testpass1')
        response = self.client.get(reverse('cdn:new_project'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='admin', password='testpass1')
        response = self.client.get(reverse('cdn:new_project'))
        self.assertEqual(response.status_code, 200)

    def test_new_project_POST(self):
        self.client.login(username='admin', password='testpass1')
        response = self.client.post(reverse('cdn:new_project'), {
            'name': 'project2',
            'description': 'description2',
        })
        self.assertEqual(response.status_code, 200)

    def test_project(self):
        self.client.login(username='user1', password='testpass1')
        response = self.client.get(reverse('cdn:project', args=[self.project.id]))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='admin', password='testpass1')
        response = self.client.get(reverse('cdn:project', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)

    def test_replace_item_GET(self):
        self.client.login(username='user1', password='testpass1')
        response = self.client.get(reverse('cdn:replace_item', args=[self.item.id]))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='admin', password='testpass1')
        response = self.client.get(reverse('cdn:replace_item', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)

    def test_edit_project_GET(self):
        self.client.login(username='user1', password='testpass1')
        response = self.client.get(reverse('cdn:edit_project', args=[self.project.id]))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='admin', password='testpass1')
        response = self.client.get(reverse('cdn:edit_project', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)

    def test_new_item_GET(self):
        self.client.login(username='user1', password='testpass1')
        response = self.client.get(reverse('cdn:new_item', args=[self.project.id]))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='admin', password='testpass1')
        response = self.client.get(reverse('cdn:new_item', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)

    def test_edit_item_GET(self):
        self.client.login(username='user1', password='testpass1')
        response = self.client.get(reverse('cdn:edit_item', args=[self.item.id]))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='admin', password='testpass1')
        response = self.client.get(reverse('cdn:edit_item', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)

    def test_edit_item_POST(self):
        self.client.login(username='admin', password='testpass1')
        response = self.client.post(reverse('cdn:edit_item', args=[self.item.id]), {
            'category': 'category2',
            'description': 'description2',
        })
        self.assertEqual(response.status_code, 200)

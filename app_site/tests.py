import uuid

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from app_site.models import Site

User = get_user_model()


class TestViews(TestCase):
    mock_project_number = 0

    def mock_a_project(self, name=''):
        if name == "":
            self.mock_project_number += 1
            name = 'mock_project_' + str(self.mock_project_number)
        self.client.post(reverse('site:new_project'), {
            'name': name,
        })
        project = Site.objects.get(name=name)
        return project

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass1',)
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.client = Client()
        self.client.login(username='testuser', password='testpass1')

        self.testproject = Site.objects.create(
            name='testproject',
            description='testdescription',
            url='testurl',
            github='testgit',
        )

    def test_home(self):

        response = self.client.get(reverse('site:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'site/home.html')

    def test_new_project_GET(self):
        response = self.client.get(reverse('site:new_project'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'site/new_project.html')

    def test_new_project_POST(self):
        response = self.client.post(reverse('site:new_project'), {
            'name': 'mock_new_project',
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('site:new_project'), {
            'name/name': '',
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('site:new_project'), {
            'name': '',
        })
        self.assertEqual(response.status_code, 200)

    def test_project(self):

        project = self.mock_a_project()

        self.testproject = Site.objects.get(name=project.name)

        response = self.client.get(reverse('site:project', args=[project.id]))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('site:project', args=[str(uuid.uuid4())]))
        self.assertEqual(response.status_code, 404)

    def test_edit_project_GET(self):
        response = self.client.get(reverse('site:edit_project', args=[self.testproject.id]))
        self.assertEqual(response.status_code, 200)

    def test_edit_project_POST(self):
        project = self.mock_a_project('mock_project_3')
        response = self.client.post(
            reverse('site:edit_project', args=[project.id]),
            data={'name': 'mock_project_renamed'}
            )
        self.assertEqual(response.status_code, 200)

        project_1 = self.mock_a_project('mock_project_1')
        response = self.client.post(
            reverse('site:edit_project', args=[project.id]),
            data={'name': project_1.name}
            )
        self.assertIn('already exists', response.context['error'])

        response = self.client.post(
            reverse('site:edit_project', args=[str(uuid.uuid4())]),
            data={'name': 'mock_project_fail_to_renamed'})
        self.assertEqual(response.status_code, 404)

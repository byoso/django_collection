import shutil
import os
from zipfile import ZipFile, is_zipfile
from pprint import pprint

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .models import Site
from .forms import SiteForm

from .helpers import folder_to_dict

SITEFILES_DIR = os.path.abspath(os.path.join(settings.MEDIA_ROOT, 'sitefiles'))


@user_passes_test(lambda u: u.is_superuser)
def home(request):
    sites = Site.objects.all()
    context = {
        'link': f"{request.get_host()}/site/",
        'projects': sites,
    }
    return render(request, 'site/home.html', context)


@user_passes_test(lambda u: u.is_superuser)
def project(request, project_id):
    project = get_object_or_404(Site, pk=project_id)
    content = folder_to_dict(os.path.join(SITEFILES_DIR, project.name))
    if settings.DEBUG:
        pprint(content)
    context = {
        'link': f"{request.get_host()}/site/{project.name}/",
        'project': project,
        'content': content,
        'project_path': os.path.join(SITEFILES_DIR, project.name),
    }
    return render(request, 'site/project.html', context)


@user_passes_test(lambda u: u.is_superuser)
def new_project(request):
    if request.method == 'POST':
        form = SiteForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if Site.objects.filter(name=name).exists() or '/' in name:
                context = {
                    'form': form,
                    'error': 'Project name already exists or not allowed',
                }
                return render(request, 'site/new_project.html', context)
            # os.makedirs(os.path.join(SITEFILES_DIR, name), exist_ok=True)
            form.save()
            return redirect('site:home')
        return render(request, 'site/new_project.html', {'form': form})
    form = SiteForm()
    context = {
        'form': form,
    }
    return render(request, 'site/new_project.html', context)


@user_passes_test(lambda u: u.is_superuser)
def edit_project(request, project_id):
    project = get_object_or_404(Site, pk=project_id)
    if request.method == 'POST':
        form = SiteForm(request.POST)
        if form.is_valid():
            if project.name and form.cleaned_data['name'] != project.name:
                name = form.cleaned_data['name']
                if Site.objects.filter(name=name).exists() or '/' in name:
                    context = {
                        'form': form,
                        'project': project,
                        'error': 'Project name already exists or not allowed',
                    }
                    return render(request, 'site/edit_project.html', context)
                # shutil.move(os.path.join(SITEFILES_DIR, project.name),
                #             os.path.join(SITEFILES_DIR, form.cleaned_data['name']))
                project.name = form.cleaned_data['name']
            project.description = form.cleaned_data['description']
            project.url = form.cleaned_data['url']
            project.github = form.cleaned_data['github']
            project.save()
            projects = Site.objects.all()
            context = {
                'projects': projects,
            }
            return render(request, 'site/home.html', context)

    form = SiteForm(instance=project)
    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'site/edit_project.html', context)


@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(['POST'])
def delete_project(request, project_id):
    project = get_object_or_404(Site, pk=project_id)
    project.delete()
    projects = Site.objects.all()
    context = {
        'projects': projects,
    }
    return render(request, 'site/home.html', context)


@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(['POST'])
def delete_item(request, project_id):
    path = request.POST.get('path')
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    return redirect('site:project', project_id=project_id)


@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(['POST'])
def delete_all(request, project_id):
    """delete all the content of the project, bu not the project folder itself"""
    project = get_object_or_404(Site, pk=project_id)
    if os.path.exists(os.path.join(SITEFILES_DIR, project.name)):
        for elem in os.listdir(os.path.join(SITEFILES_DIR, project.name)):
            if os.path.isdir(os.path.join(SITEFILES_DIR, project.name, elem)):
                shutil.rmtree(os.path.join(SITEFILES_DIR, project.name, elem))
            else:
                os.remove(os.path.join(SITEFILES_DIR, project.name, elem))

    return redirect('site:project', project_id=project_id)


@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(['POST'])
def create_subfolder(request, project_id):
    name = request.POST.get('folder_name').strip()
    path = request.POST.get('path').strip()
    print("=== path : ", path)
    if name != "" and '/' not in name:
        if os.path.exists(path) and os.path.isdir(path):
            if os.path.exists((os.path.join(path, name))):
                messages.add_message(
                    request, messages.ERROR,
                    "path already exists",
                    extra_tags="danger"
                    )
            else:
                os.makedirs(os.path.join(path, name), exist_ok=True)
                messages.add_message(
                    request, messages.SUCCESS,
                    "folder created",
                    extra_tags="success"
                    )
    else:
        messages.add_message(
            request, messages.ERROR,
            "Invalid folder name",
            extra_tags="danger"
            )
    return redirect('site:project', project_id=project_id)


@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(['POST'])
def add_zip_file(request, project_id):
    project = Site.objects.get(pk=project_id)
    zip_file = request.FILES.get('zip_file')
    if not is_zipfile(zip_file):
        messages.add_message(
            request, messages.ERROR,
            "Invalid zip file",
            extra_tags="danger"
            )
        return redirect('site:project', project_id=project_id)
    with open(os.path.join(SITEFILES_DIR, project.name, zip_file.name), 'wb+') as destination:
        for chunk in zip_file.chunks():
            destination.write(chunk)
    with ZipFile(os.path.join(SITEFILES_DIR, project.name, zip_file.name), 'r') as zipObj:
        zipObj.extractall(os.path.join(SITEFILES_DIR, project.name))
    os.remove(os.path.join(SITEFILES_DIR, project.name, zip_file.name))
    return redirect('site:project', project_id=project_id)


@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(['POST'])
def add_file(request, project_id):
    file = request.FILES.get('file')
    path = request.POST.get('path')
    if not file:
        messages.add_message(
            request, messages.ERROR,
            "Invalid filename",
            extra_tags="danger"
            )
        return redirect('site:project', project_id=project_id)

    with open(os.path.join(path, file.name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return redirect('site:project', project_id=project_id)

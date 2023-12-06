import os
import shutil

from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProjectForm, ItemForm, ItemEditForm, ReplaceItemForm
from .models import Project, Item
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.views.decorators.http import require_http_methods

from .config import CDN_DIRECTORY

@user_passes_test(lambda u: u.is_superuser)
def home(request):
    projects = Project.objects.all()
    context = {
        'projects': projects,
    }

    return render(request, 'cdn/home.html', context)


@user_passes_test(lambda u: u.is_superuser)
def new_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            projects = Project.objects.all()
            context = {
                'projects': projects,
            }
            return render(request, 'cdn/home.html', context)
        return render(request, 'cdn/new_project.html', {'form': form})
    form = ProjectForm()
    context = {
        'form': form,
    }
    return render(request, 'cdn/new_project.html', context)


@user_passes_test(lambda u: u.is_superuser)
def project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    items = Item.objects.filter(project=project)
    absolute_url = request.build_absolute_uri()
    base_url = f'http://{request.get_host()}'
    if settings.DEBUG:
        base_url += '/media'
    context = {
        'base_url': base_url,
        'absolute_url': absolute_url,
        'project': project,
        'items': items,
    }
    return render(request, 'cdn/project.html', context)


@user_passes_test(lambda u: u.is_superuser)
def replace_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    project = item.project
    category = item.category
    description = item.description
    base_url = f'http://{request.get_host()}'
    if settings.DEBUG:
        base_url += '/media'
    if request.method == 'POST':
        form = ReplaceItemForm(request.POST, request.FILES)
        if form.is_valid():
            name = item.file.name.split('/')[-1]
            file = request.FILES['file']
            file.name = name
            if os.path.exists(os.path.join(settings.MEDIA_ROOT, item.file.name)):
                os.remove(os.path.join(settings.MEDIA_ROOT, item.file.name))
            item.delete()
            Item.objects.create(
                project=project,
                category=category,
                description=description,
                file=file,
                )
            return redirect('cdn:project', project_id=project.id)
        context = {
            'base_url': base_url,
            'form': form,
            'item': item,
            'project': project,
        }
        return render(request, 'cdn/replace_item.html', {'form': form})
    form = ReplaceItemForm()
    context = {
        'base_url': base_url,
        'item': item,
        'form': form,
        'project': project,
    }
    return render(request, 'cdn/replace_item.html', context)



@user_passes_test(lambda u: u.is_superuser)
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            if project.name and form.cleaned_data['name'] != project.name:
                shutil.move(os.path.join(settings.MEDIA_ROOT, project.name),
                            os.path.join(settings.MEDIA_ROOT, form.cleaned_data['name'].strip()))
                items = Item.objects.filter(project=project)
                for item in items:
                    item.file.name = item.file.name.replace(project.name, form.cleaned_data['name'].strip())
                    item.save()
                project.name = form.cleaned_data['name'].strip()
            project.description = form.cleaned_data['description'].strip()
            project.url = form.cleaned_data['url'].strip() if form.cleaned_data['url'] else None
            project.github = form.cleaned_data['github'].strip() if form.cleaned_data['github'] else None
            project.save()
            projects = Project.objects.all()
            context = {
                'projects': projects,
            }
            return render(request, 'cdn/home.html', context)
    form = ProjectForm(instance=project)
    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'cdn/edit_project.html', context)


@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(['POST'])
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if os.path.exists(os.path.join(settings.MEDIA_ROOT, CDN_DIRECTORY, project.name)):
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, CDN_DIRECTORY, project.name))
    project.delete()
    projects = Project.objects.all()
    context = {
        'projects': projects,
    }
    return render(request, 'cdn/home.html', context)


@user_passes_test(lambda u: u.is_superuser)
def new_item(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            Item.objects.create(
                project=project,
                category=form.cleaned_data['category'].strip(),
                description=form.cleaned_data['description'].strip(),
                file=request.FILES['file'],
                )
            return redirect('cdn:project', project_id=project.id)
        return render(request, 'cdn/new_item.html', {'form': form})
    form = ItemForm()
    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'cdn/new_item.html', context)


@user_passes_test(lambda u: u.is_superuser)
def edit_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    project = item.project
    if request.method == 'POST':
        form = ItemEditForm(request.POST, request.FILES)
        if form.is_valid():
            # item.name = form.cleaned_data['name']
            if item.category != form.cleaned_data['category'].strip():
                if not os.path.exists(
                        os.path.join(settings.MEDIA_ROOT, CDN_DIRECTORY, project.name, form.cleaned_data['category'].strip())):
                    os.makedirs(os.path.join(settings.MEDIA_ROOT, CDN_DIRECTORY, project.name, form.cleaned_data['category'].strip()))
                shutil.move(os.path.join(settings.MEDIA_ROOT, item.file.name),
                            os.path.join(settings.MEDIA_ROOT, CDN_DIRECTORY, project.name, form.cleaned_data['category']))
                item.file.name = os.path.join(
                    CDN_DIRECTORY,
                    project.name,
                    form.cleaned_data['category'].strip(),
                    item.file.name.split('/')[-1]
                    )
            item.category = form.cleaned_data['category'].strip()
            item.description = form.cleaned_data['description'].strip()
            item.save()
            return redirect('cdn:project', project_id=item.project.id)
    form = ItemEditForm(instance=item)

    base_url = f'http://{request.get_host()}'
    if settings.DEBUG:
        base_url += '/media'
    context = {
        'base_url': base_url,
        'item': item,
        'form': form,
        'project': project,
    }
    return render(request, 'cdn/edit_item.html', context)


@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(['POST'])
def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    project = item.project
    if os.path.exists(os.path.join(settings.MEDIA_ROOT, item.file.name)):
        os.remove(os.path.join(settings.MEDIA_ROOT, item.file.name))
    item.delete()
    return redirect('cdn:project', project_id=project.id)

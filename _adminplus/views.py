from django.shortcuts import render, redirect


def adminplus(request):
    if not request.user.is_superuser or not request.user.is_active:
        return redirect('admin:index')
    context = {

    }
    return render(request, '_adminplus/adminplus_index.html', context)

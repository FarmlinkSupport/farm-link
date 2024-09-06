from django.http import HttpResponse

def allowed_user(allowed_group=[]):
    def decoratorfun(view_func):
        def wrapper_func(request, *args, **kwargs):
            print(request.user.groups,request.user)
            if request.user.groups.filter(name__in=allowed_group).exists():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorised to view this page!!', status=403)
        return wrapper_func
    return decoratorfun

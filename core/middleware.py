from django.shortcuts import redirect


class InviteOnlyMiddleware:
    EXEMPT_PATHS = ("/auth/login/", "/auth/register/", "/static/", "/admin/")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if not any(request.path.startswith(p) for p in self.EXEMPT_PATHS):
                return redirect("login")
        return self.get_response(request)

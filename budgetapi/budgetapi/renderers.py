from rest_framework.renderers import BrowsableAPIRenderer
import rest_framework.exceptions as exceptions

class MyBrowsableAPIRenderer(BrowsableAPIRenderer):
    """
    Only render the browsable API if there is no 404 error
    """

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        if args[2]['request'] in ('PUT', 'PATCH'):
            context['display_edit_forms'] = True
        return context

    def get_rendered_html_form(self, data, view, method, request):
        return super().get_rendered_html_form(data, view, method, request)

    def show_form_for_method(self, view, method, request, obj):
        """
        Bypass permission check and render forms for all allowed methods.
        see https://stackoverflow.com/questions/52730182/
        """
        if method not in view.allowed_methods:
            return False
        return True

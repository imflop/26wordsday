from django.views.generic import TemplateView


class LandingView(TemplateView):
    """
    View for landing page
    """

    template_name = 'landing.html'

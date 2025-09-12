from django.shortcuts import render
from django.views import View


class SocialNetworkView(View):
    template_name = 'base/social_network.html'

    def get(self, request):
        return render(request, self.template_name)
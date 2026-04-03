from django.views import generic

# Create your views here.
class Home(generic.TemplateView):
    template_name = 'home.html'

class ProductDetails(generic.TemplateView):
    template_name = 'product/product-details.html'
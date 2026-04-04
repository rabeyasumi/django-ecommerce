from django.views import generic
from .models import(
    Category,
    Product,
    Slider
)

# Create your views here.
class Home(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'featured_categories': Category.objects.filter(featured=True),
                'featured_products': Product.objects.filter(featured=True),
                'sliders': Slider.objects.filter(show=True)
            }
        )
        return context

class ProductDetails(generic.DetailView):
    model = Product # html get in lowercare product
    template_name = 'product/product-details.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = self.get_object().related # related func added in models.py
        return context
    
class CategoryDetails(generic.DetailView):
    model = Category # html get in lowercare 'category'
    template_name = 'product/category-details.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.get_object().products.all() # in models.py, for a specific category related name is 'products'
        return context
    
class ProductList(generic.ListView):
    model = Product
    template_name = 'product/product-list.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
           
        

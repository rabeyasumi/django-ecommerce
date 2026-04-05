from django.db.models import Q
from django.views import generic
from django.shortcuts import render
from django.core.paginator import(
    PageNotAnInteger,
    EmptyPage,
    InvalidPage,
    Paginator
)
from .models import(
    Category,
    Product,
    Slider
)

from cart.carts import Cart
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
    
class CustomPaginator:
    def __init__(self, request, queryset, paginated_by) -> None:
        self.paginator = Paginator(queryset, paginated_by)
        self.queryset = queryset
        self.page = request.GET.get('page', 1)

    def get_queryset(self):
        try:
            queryset = self.paginator.page(self.page)
        except PageNotAnInteger:
            queryset = self.paginator.page(1)
        except EmptyPage:
            queryset = self.paginator.page(1)
        except InvalidPage:
            queryset = self.paginator.page(1)

        return queryset
    

class ProductList(generic.ListView):
    model = Product
    template_name = 'product/product-list.html'
    context_object_name = 'object_list'
    paginate_by = None  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = self.get_queryset()

        page_obj = CustomPaginator(
            self.request,
            queryset,
            10
        )

        page = page_obj.get_queryset()

        context['object_list'] = page.object_list  
        context['page_obj'] = page                 
        context['paginator'] = page_obj.paginator
        context['is_paginated'] = True

        return context

           
class SearchProducts(generic.View):
    def get(self, *args, **kwargs):
        key = self.request.GET.get('key', '')
        products = Product.objects.filter(
            Q(title__icontains=key) |
            Q(category__title__icontains=key)
        )
        context = {
            'products': products,
            "key": key
        }
        return render(self.request, 'product/search-products.html', context)


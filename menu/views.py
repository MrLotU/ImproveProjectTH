from datetime import datetime
from operator import attrgetter

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import MenuForm
from .models import Menu, Item


def menu_list(request):
    """List all menus"""
    # Get all menus
    all_menus = Menu.objects.all().prefetch_related('items')
    menus = []
    # Check if the menu is expired
    for menu in all_menus:
        if menu.expiration_date >= timezone.now().date():
            menus.append(menu)

    # Sort menus and render them
    menus = sorted(menus, key=attrgetter('expiration_date'))
    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})

def menu_detail(request, pk):
    """Render the detail page for a menu"""
    menu = Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})

def item_detail(request, pk):
    """Render the detail page for an item"""
    try: 
        item = Item.objects.filter(pk=pk).prefetch_related('ingredients').get()
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/detail_item.html', {'item': item})

def create_new_menu(request):
    """Creates a new menu with the MenuForm"""
    # Check request method
    if request.method == "POST":
        # Create form
        form = MenuForm(request.POST)
        # Check validation
        if form.is_valid():
            # Create and save menu
            menu = form.save(commit=False)
            menu.created_date = timezone.now()
            menu.save()
            form.save_m2m()
            return redirect('menu_detail', pk=menu.pk)
    else:
        # Create form
        form = MenuForm()
    # Render creation page
    return render(request, 'menu/menu_edit.html', {'form': form})

def edit_menu(request, pk):
    """Edits a menu with the MenuForm"""
    # Get the menu and create the form
    menu = get_object_or_404(Menu, pk=pk)
    form = MenuForm(instance=menu)
    # Check request method
    if request.method == "POST":
        # Create form
        form = MenuForm(request.POST, instance=menu)
        # Check validation
        if form.is_valid():
            # Update and save menu
            menu = form.save(commit=False)
            menu.created_date = timezone.now()
            menu.save()
            form.save_m2m()
            return redirect('menu_list')
    # Render update page
    return render(request, 'menu/menu_edit.html', {'form': form})

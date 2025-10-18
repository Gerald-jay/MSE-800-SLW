from django.shortcuts import render

def welcome(request, name):
    """
    A simple Django view that renders a styled page
    with green background and red text.
    """
    return render(request, "welcome.html", {"name": name})

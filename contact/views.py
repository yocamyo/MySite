from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm


def contactView(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            try:
                send_mail(
                    subject,
                    message,
                    email,
                    [
                        "naviscam@gmail.com",
                    ],
                    "naviscam@gmail.com",
                )
            except BadHeaderError:
                return HttpResponse("Invalid header found")
            return redirect("success")
    form = ContactForm()
    return render(request, "contact/contact.html", {"form": form})


def successView(request):
    return render(request, "contact/success.html", {})

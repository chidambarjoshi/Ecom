from django.shortcuts import render
from  .forms import UsersForm

# Create your views here.
def userregister(request):
    form= UsersForm(request.POST or None)
    template="userreg.html"
    context={
        "form":form
    }
    return render(request,template,context)
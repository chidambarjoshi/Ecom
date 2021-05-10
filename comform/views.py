from django.shortcuts import render
from  .forms import UsersForm
from com.models import Users

# Create your views here.
def userregister(request):
    form= UsersForm(request.POST or None)
    template="userreg.html"
    user=Users.objects.filter(email='chidambar.joshi5@gmail.com')
    context={
        "form":form,
        'user':user
    }
    return render(request,template,context)
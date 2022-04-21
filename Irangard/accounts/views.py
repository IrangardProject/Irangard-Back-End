from django.shortcuts import render


def testHtml(request):
    return render(request, 'myemail/new_activation.html')

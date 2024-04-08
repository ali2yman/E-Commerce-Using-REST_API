# THIS FILE IS TO HANDLE ERRORES IN OUR PROJECT
from django.http import JsonResponse

def handler404(request,exception):
    message = ('Path not found ya Ali ')
    response = JsonResponse(data={'error':message})
    response.status_code = 404
    return response

def handler500(request):
    message = ('Internal server error ya Ali.')
    response = JsonResponse(data={'error':message})
    response.status_code = 500
    return response
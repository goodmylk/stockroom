from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from django.http import HttpResponse, JsonResponse
import slack

# Create your views here.
@csrf_exempt
def posttext(request):
    client = slack.WebClient(token=settings.BOT_USER_ACCESS_TOKEN)
    try:
        client.chat_postMessage(channel="#test", text="Hi")
        return render(request, 'lowstock.html', status=200)

    except Exception as error:
        return render(request, 'lowstock.html', status=403)

# from django.urls import path
# from .views import chatPage

# urlpatterns = [
#     path("", chatPage, name="chat-page"),
# ]


from django.urls import path
from .views import chatPage

urlpatterns = [
    path("<str:username>/", chatPage, name="chat-page"),
]

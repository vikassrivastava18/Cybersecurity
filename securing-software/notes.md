## Authentication
<p> Allowing only authenticated user to use the application</p>

> pip install Flask-Login

```
from flask import Flask
from flask_login import LoginManager, login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    return {"error": "Authentication required"}, 401


@app.route("/api/profile")
@login_required
def profile():
    return {"message": "You are authenticated"}

```

<p> Protect all API andpoints</p>

```
from flask import request
from flask_login import current_user

@app.before_request
def protect_api():
    if request.path.startswith("/api/"):
        if not current_user.is_authenticated:
            return {"error": "Authentication required"}, 401


@app.route("/api/users")
def users():
    return {"users": []}

@app.route("/api/orders")
def orders():
    return {"orders": []}
```

<p>How to implement in Django</p>

<p>For Django </p>

```
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return JsonResponse({
            "user": request.user.username
        })

```

<p>For DRF</p>

```
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "user": request.user.username
        })
```

<p>Protect all API's in DRF</p>

```
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

```


## Authorization
<p> Allow users with permission to access an API

```
class Product(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        permissions = [
            ("publish_product", "Can publish product"),
        ]


from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from django.http import JsonResponse


class PublishProductView(PermissionRequiredMixin, View):
    permission_required = "products.publish_product"

    def post(self, request):
        return JsonResponse({"message": "Product published"})

```

DRF
```
models.py
class BookInstance(models.Model):

    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (('can_mark_returned', 'Set book as returned'),)



# Create your views here.
class CanMarkReturnedPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('catalog.can_mark_returned')


class MarkBookAsReturnedView(generics.UpdateAPIView):
    serializer_class = BookInstanceSerializer
    queryset = BookInstance.objects.all()
    permission_classes = [CanMarkReturnedPermission]
```

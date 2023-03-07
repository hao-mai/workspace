# from django.test import RequestFactory
# from rest_framework.test import APIClient
# from django.contrib.auth.models import User

# @pytest.fixture
# def api_client():
#     return APIClient()

# @pytest.fixture
# def user():
#     user = User.objects.create_user(
#         username='testuser',
#         password='testpass'
#     )
#     return user

# @pytest.fixture
# def authenticated_api_client(api_client, user):
#     api_client.force_authenticate(user=user)
#     return api_client

# def test_authenticated_view(authenticated_api_client):
#     # create a fake request using RequestFactory
#     factory = RequestFactory()
#     request = factory.get('/api/my-authenticated-view/')
#     request.user = authenticated_api_client.user

#     # perform the request
#     response = my_authenticated_view(request)

#     # assert that the response is successful
#     assert response.status_code == 200

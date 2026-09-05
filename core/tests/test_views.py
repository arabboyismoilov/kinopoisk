import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_register_view_success(api_client):
    data = {
        "username": "ali2",
        "password": "1234"
    }
    
    res = api_client.post(
        "/api/register",
        data,
        format="json"   
    )
    
    assert res.status_code == 201
    assert "id"  in res.data
    assert "created_at"  in res.data
    

@pytest.mark.django_db
def test_register_view_fail_on_duplicate_username(api_client, user):
    data = {
        "username": user.username,
        "password": "1234"
    }
    
    res = api_client.post(
        "/api/register",
        data,
        format="json"   
    )
    
    assert res.status_code == 400


@pytest.mark.django_db
def test_movie_detail_view_fail_on_auth_not_provided(api_client):
    res = api_client.get(
        '/api/movie/1'
    )
    
    assert res.status_code == 401
    
    
# @pytest.mark.django_db
# def test_movie_detail_view_success(api_client, jwt_token):
#     res = api_client.get(
#         '/api/movie/1',
#         HTTP_AUTHORIZATION = f"Bearer {jwt_token}"
#     )
    
#     assert res.status_code == 404
    

# @pytest.mark.django_db
# def test_movie_detail_view_success_jwt(jwt_client):
#     res = jwt_client.get(
#         '/api/movie/1'
#     )
    
#     assert res.status_code == 404
    
    

@pytest.mark.django_db
def test_movie_detail_view_success_on_exist_bepul_movie(mock_client):
    res = mock_client.get(
        '/api/movie/1'
    )
    
    assert res.status_code == 200
    

@pytest.mark.django_db
def test_movie_detail_view_fail_on_exist_obuna_movie(mock_client, user2):
    mock_client.force_authenticate(user2)
    res = mock_client.get(
        '/api/movie/2'
    )
    
    assert res.status_code == 403
    

@pytest.mark.django_db
def test_movie_detail_view_success_on_exist_obuna_movie_has_subscription(mock_client):
    res = mock_client.get(
        '/api/movie/2'
    )
    
    assert res.status_code == 200
    
    
@pytest.mark.django_db
def test_movie_detail_view_fail_on_not_exist_movie(mock_client):
    res = mock_client.get(
        '/api/movie/3'
    )
    
    assert res.status_code == 404
    
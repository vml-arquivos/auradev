"""
Tests for Core app.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestUserAPI:
    """Test User API endpoints."""
    
    def setup_method(self):
        """Setup test client and test user."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            role='professor'
        )
    
    def test_create_user(self):
        """Test creating a new user."""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'aluno'
        }
        response = self.client.post('/api/v1/core/users/', data)
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_list_users(self):
        """Test listing users."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/core/users/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0
    
    def test_get_current_user(self):
        """Test getting current user profile."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/core/users/me/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'testuser'
        assert response.data['role'] == 'professor'

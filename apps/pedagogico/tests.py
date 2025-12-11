"""
Tests for Pedagogico app.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Turma, PlanejamentoAnual

User = get_user_model()


@pytest.mark.django_db
class TestTurmaAPI:
    """Test Turma API endpoints."""
    
    def setup_method(self):
        """Setup test client and test data."""
        self.client = APIClient()
        self.professor = User.objects.create_user(
            username='professor1',
            email='prof@example.com',
            password='pass123',
            role='professor'
        )
        self.turma = Turma.objects.create(
            nome='5º Ano A',
            nivel_ensino='5ef',
            professor=self.professor,
            ano_letivo=2025,
            semestre=1
        )
    
    def test_list_turmas(self):
        """Test listing classes."""
        self.client.force_authenticate(user=self.professor)
        response = self.client.get('/api/v1/pedagogico/turmas/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0
    
    def test_create_turma(self):
        """Test creating a new class."""
        self.client.force_authenticate(user=self.professor)
        data = {
            'nome': '6º Ano B',
            'nivel_ensino': '6ef',
            'professor': self.professor.id,
            'ano_letivo': 2025,
            'semestre': 1
        }
        response = self.client.post('/api/v1/pedagogico/turmas/', data)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestPlanejamentoAnualAPI:
    """Test PlanejamentoAnual API endpoints."""
    
    def setup_method(self):
        """Setup test client and test data."""
        self.client = APIClient()
        self.professor = User.objects.create_user(
            username='professor2',
            email='prof2@example.com',
            password='pass123',
            role='professor'
        )
        self.turma = Turma.objects.create(
            nome='5º Ano C',
            nivel_ensino='5ef',
            professor=self.professor,
            ano_letivo=2025,
            semestre=1
        )
        self.planejamento = PlanejamentoAnual.objects.create(
            professor=self.professor,
            turma=self.turma,
            titulo='Planejamento Anual 2025',
            introducao_geral='Introdução ao ano letivo...',
            status='rascunho'
        )
    
    def test_list_planejamentos(self):
        """Test listing annual plans."""
        self.client.force_authenticate(user=self.professor)
        response = self.client.get('/api/v1/pedagogico/planejamentos/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0
    
    def test_submit_planejamento(self):
        """Test submitting a plan for approval."""
        self.client.force_authenticate(user=self.professor)
        response = self.client.post(
            f'/api/v1/pedagogico/planejamentos/{self.planejamento.id}/submit/'
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'pendente'

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from model_bakery import baker

from fileprocessor.models import File
import pytest
from datetime import datetime, timezone

@pytest.fixture
def create_file(api_client):
    def do_create_file(file):
        return api_client.post('/api/upload/', file, format='multipart')
    return do_create_file


@pytest.mark.django_db
class TestCreateFile:
    def test_if_data_is_valid_returns_201(self, create_file):
        file_content_csv = b'Column1,Column2,Column3\nValue1,Value2,Value3\n'
        uploaded_file = SimpleUploadedFile("test.csv", file_content_csv)
        data = {
            "file": uploaded_file,  
            "uploaded_at": "2023-10-15T09:20:13.195372Z",
            "processed": False
        }

        response=create_file(data)
  
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

    def test_if_data_is_invalid_returns_400(self, create_file):
        uploaded_file = 'invalid file'
        data = {
            "file": uploaded_file,  
            "uploaded_at": "2023-10-15T09:20:13.195372Z",
            "processed": False
        }

        response=create_file(data)
  
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['file'] is not None


@pytest.mark.django_db
class TestRetrieveFile:
    def test_if_file_exists_returns_200(self, api_client):
        file_content_csv = b'Column1,Column2,Column3\nValue1,Value2,Value3\n'
        uploaded_file = SimpleUploadedFile("test.csv", file_content_csv)
        file = baker.make(File, file=uploaded_file)

        response = api_client.get(f'/api/files/{file.id}/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_file_does_not_exist_returns_404(self, api_client):

        response = api_client.get(f'/api/files/99/')

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateFile:
    def test_if_file_exists_and_can_be_updated_returns_200(self, api_client):
        file_content_csv = b'Column1,Column2,Column3\nValue1,Value2,Value3\n'
        uploaded_file = SimpleUploadedFile("test.csv", file_content_csv)
        file = baker.make(File, file=uploaded_file)

        # Update file 
        updated_file_content = b'This is an updated file content.'
        updated_file = SimpleUploadedFile("updated.txt", updated_file_content)

        updated_data = {
            "file": updated_file,
            "uploaded_at": "2023-10-16T10:00:00.000000Z",  
            "processed": True,
        }

        response = api_client.put(f'/api/files/{file.id}/', updated_data)

        assert response.status_code == status.HTTP_200_OK

    def test_if_file_does_not_exist_and_returns_404(self, api_client):
        file_content_csv = b'Column1,Column2,Column3\nValue1,Value2,Value3\n'
        uploaded_file = SimpleUploadedFile("test.csv", file_content_csv)
        file = baker.make(File, file=uploaded_file)

        # Update file 
        updated_file_content = b'This is an updated file content.'
        updated_file = SimpleUploadedFile("updated.txt", updated_file_content)

        updated_data = {
            "file": updated_file,
            "uploaded_at": "2023-10-16T10:00:00.000000Z",  
            "processed": True,
        }

        response = api_client.put(f'/api/files/999/', updated_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(self, api_client):
        file_content_csv = b'Column1,Column2,Column3\nValue1,Value2,Value3\n'
        uploaded_file = SimpleUploadedFile("test.csv", file_content_csv)
        file = baker.make(File, file=uploaded_file)

        # Update file 
        uploaded_file = 'invalid file'

        updated_data = {
            "file": uploaded_file,
            "uploaded_at": "2023-10-16T10:00:00.000000Z",  
            "processed": True,
        }

        response=api_client.put(f'/api/files/{file.id}/', updated_data)
  
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteFile:
    def test_if_file_exists_and_can_be_deleted_returns_204(self, api_client):
        
        file_content_csv = b'Column1,Column2,Column3\nValue1,Value2,Value3\n'
        uploaded_file = SimpleUploadedFile("test.csv", file_content_csv)
        file = baker.make(File, file=uploaded_file)

        response = api_client.delete(f'/api/files/{file.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

        with pytest.raises(File.DoesNotExist):
            File.objects.get(id=file.id)

    def test_if_file_does_not_exist_and_returns_404(self, api_client):

        response = api_client.delete('/api/files/900/')

        assert response.status_code == status.HTTP_404_NOT_FOUND
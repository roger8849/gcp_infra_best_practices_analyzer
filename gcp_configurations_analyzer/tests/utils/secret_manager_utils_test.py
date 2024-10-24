import unittest
from unittest.mock import MagicMock
from google.cloud import secretmanager
from '../../utils' import SecretManagerUtils  # Replace your_module

class SecretManagerUtilsTest(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.project_id = "test-project"
        self.secret_id = "test-secret"
        self.secret_value = "test-secret-value"

        # Mock the Secret Manager client
        self.mock_client = MagicMock(spec=secretmanager.SecretManagerServiceClient)
        self.mock_access_secret_version = MagicMock()
        self.mock_access_secret_version.payload.data.decode.return_value = self.secret_value
        self.mock_client.access_secret_version.return_value = self.mock_access_secret_version

        # Create an instance of SecretManagerUtils with the mock client
        self.utils = SecretManagerUtils(self.project_id)
        self.utils.client = self.mock_client

    def test_get_secret_success(self):
        """Test successful retrieval of a secret."""
        secret_value = self.utils.get_secret(self.secret_id)
        self.assertEqual(secret_value, self.secret_value)
        self.mock_client.access_secret_version.assert_called_once_with(
            request={"name": f"projects/{self.project_id}/secrets/{self.secret_id}/versions/latest"}
        )

    def test_get_secret_not_found(self):
        """Test when the secret is not found."""
        self.mock_access_secret_version.payload.data.decode.side_effect = Exception("Secret not found")
        secret_value = self.utils.get_secret("non-existent-secret")
        self.assertIsNone(secret_value)

if __name__ == "__main__":
    unittest.main()
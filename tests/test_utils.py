"""
Unit tests for app.utils module.
"""

import os
import tempfile
from unittest.mock import patch, MagicMock
import pytest
from app.utils import ensure_database, DB_PATH


class TestEnsureDatabase:
    """Test suite for database download and verification."""

    @patch("app.utils.hf_hub_download")
    @patch("app.utils.os.makedirs")
    @patch("app.utils.os.path.exists")
    def test_downloads_when_file_missing(
        self, mock_exists, mock_makedirs, mock_hf_download
    ):
        """Should download database from Hugging Face when local file is missing."""
        # Arrange
        mock_exists.return_value = False
        mock_hf_download.return_value = "/fake/path/trump_pulse.db"

        # Act
        result = ensure_database()

        # Assert
        mock_makedirs.assert_called_once_with("data", exist_ok=True)
        mock_hf_download.assert_called_once_with(
            repo_id="Rogersurf/trump_pulse_data",
            filename="trump_pulse.db",
            local_dir="data/",
            repo_type="dataset",
            revision="main"
        )
        assert result == DB_PATH

    @patch("app.utils.os.path.exists")
    def test_skips_download_when_file_exists(self, mock_exists):
        """Should skip download when database already exists locally."""
        # Arrange
        mock_exists.return_value = True

        # Act
        with patch("app.utils.hf_hub_download") as mock_hf_download:
            result = ensure_database()

        # Assert
        mock_hf_download.assert_not_called()
        assert result == DB_PATH

    @patch("app.utils.os.makedirs")
    @patch("app.utils.os.path.exists")
    def test_creates_data_directory_if_missing(self, mock_exists, mock_makedirs):
        """Should create data/ directory before downloading."""
        # Arrange
        mock_exists.return_value = False

        # Act
        with patch("app.utils.hf_hub_download"):
            ensure_database()

        # Assert
        mock_makedirs.assert_called_once_with("data", exist_ok=True)

    @patch("app.utils.hf_hub_download")
    @patch("app.utils.os.path.exists")
    def test_handles_download_failure(self, mock_exists, mock_hf_download):
        """Should raise exception when Hugging Face download fails."""
        # Arrange
        mock_exists.return_value = False
        mock_hf_download.side_effect = Exception("Network error")

        # Act & Assert
        with pytest.raises(Exception, match="Network error"):
            ensure_database()
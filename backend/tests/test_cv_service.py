import pytest
import os
from services.cv_service import ImageMatcher

class TestImageMatcher:
    @pytest.fixture
    def matcher(self):
        return ImageMatcher()
    
    def test_1_valid_image_matching(self, matcher):
        """Test 1: Poprawne dopasowanie obrazów"""
        cutout = "test_data/dataset/cut.jpg"
        ref = "test_data/dataset/z2.jpg"

        result = matcher.process(cutout, ref)

        assert "err" not in result
        assert result["matches"] >= 10
        print(f"Znaleziono {result['matches']} dopasowań")
    
    def test_2_invalid_path(self, matcher):
        """Test 2: Obsługa błędnej ścieżki"""
        result = matcher.process("fake.jpg", "fake2.jpg")

        assert "err" in result
        print(f"Błąd poprawnie obsłużony: {result['err']}")
    
    def test_3_no_matches(self, matcher):
        """Test 3: Obrazy bez dopasowań"""
        result = matcher.process("test_data/dataset/z3.jpg", "test_data/dataset/z5.jpg")

        if "err" not in result:
            assert result["matches"] < 10
        print("Brak dopasowań wykryty poprawnie")
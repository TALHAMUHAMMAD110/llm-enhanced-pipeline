import pytest
from unittest.mock import patch

# Import your functions
from lambda_transform import (
    processed_doc,
    llm_processing,
    process_monitoring_doc,
    flattened_doc,
)

# Sample input document fixture
@pytest.fixture
def sample_doc():
    return {
        "document_id": "123",
        "text": "Invoice number INV-001 from Lidl store",
        "shop": "lidl",
        "total": "25.50 EUR",
        "timestamp": "2024-01-01T10:00:00",
        "purchase": [
            {"item": "Milk", "price": "2.50"},
            {"item": "Bread", "price": "3.00"},
        ],
    }


# ----------------------------
# processed_doc tests
# ----------------------------

@patch("lambda_transform.fetching_numbers_from_text")
def test_processed_doc_success(mock_fetch, sample_doc):
    mock_fetch.return_value = "INV-001"

    result = processed_doc(sample_doc)

    assert result["document_id"] == 123
    assert result["raw_text"] == sample_doc["text"]
    assert result["invoice_number"] == "INV-001"
    assert result["shop"] == "LIDL"
    assert result["total"] == "25.50"
    assert result["currency"] == "EUR"
    assert result["timestamp"] == sample_doc["timestamp"]
    assert len(result["items"]) == 2


@patch("lambda_transform.fetching_numbers_from_text")
def test_processed_doc_empty_purchase(mock_fetch, sample_doc):
    mock_fetch.return_value = "INV-001"
    sample_doc["purchase"] = []

    result = processed_doc(sample_doc)

    assert result["items"] == []


@patch("lambda_transform.fetching_numbers_from_text")
def test_processed_doc_invalid_document_id(mock_fetch, sample_doc):
    mock_fetch.return_value = "INV-001"
    sample_doc["document_id"] = "999"

    result = processed_doc(sample_doc)

    assert isinstance(result["document_id"], int)


# ----------------------------
# llm_processing tests
# ----------------------------

@patch("lambda_transform.text_cosine_similarity")
def test_llm_processing_review_required(mock_similarity):

    mock_similarity.return_value = 0.5

    doc = {
        "document_id": 123,
        "raw_text": "Invoice number INV-001 from Lidl",
        "invoice_number": "INV-001",
        "shop": "LIDL",
    }

    result = llm_processing(doc)

    assert result["review_required"] is True
    assert result["llm_score"] == 0.5
    assert "invoice" not in result["raw_text_for_llm"].lower()


@patch("lambda_transform.text_cosine_similarity")
def test_llm_processing_no_review_required(mock_similarity):

    mock_similarity.return_value = 0.95

    doc = {
        "document_id": 123,
        "raw_text": "Invoice number INV-001 from Lidl",
        "invoice_number": "INV-001",
        "shop": "LIDL",
    }

    result = llm_processing(doc)

    assert result["review_required"] is False
    assert result["llm_score"] == 0.95


# ----------------------------
# process_monitoring_doc tests
# ----------------------------

@patch("lambda_transform.current_timestamp")
def test_process_monitoring_doc(mock_timestamp):

    mock_timestamp.return_value = "2025-01-01T00:00:00"

    processed = {
        "document_id": 123,
        "invoice_number": "INV-001",
        "raw_text": "text",
        "shop": "LIDL",
        "total": "25.50",
        "currency": "EUR",
        "raw_text_for_llm": "INV-001 Lidl",
        "rule_based_text": "INV-001 LIDL",
        "review_required": False,
        "llm_score": 0.9,
    }

    result = process_monitoring_doc(processed, 5)

    assert result["document_id"] == 123
    assert result["number_of_files_read_in_batch"] == 5
    assert result["timestamp"] == "2025-01-01T00:00:00"
    assert result["llm_score"] == 0.9


# ----------------------------
# flattened_doc tests
# ----------------------------

def test_flattened_doc_success():

    processed = {
        "document_id": 123,
        "raw_text": "text",
        "invoice_number": "INV-001",
        "shop": "LIDL",
        "total": "25.50",
        "currency": "EUR",
        "timestamp": "2024-01-01",
        "items": [
            {"item": "Milk", "price": "2.50"},
            {"item": "Bread", "price": "3.00"},
        ],
    }

    result = flattened_doc(processed)

    assert len(result) == 2
    assert result[0]["item"] == "Milk"
    assert result[1]["item"] == "Bread"
    assert result[0]["document_id"] == 123


def test_flattened_doc_empty():

    processed = {
        "document_id": 123,
        "raw_text": "text",
        "invoice_number": "INV-001",
        "shop": "LIDL",
        "total": "25.50",
        "currency": "EUR",
        "timestamp": "2024-01-01",
        "items": [],
    }

    result = flattened_doc(processed)

    assert result == []
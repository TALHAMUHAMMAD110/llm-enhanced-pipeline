from helper import fetching_numbers_from_text, current_timestamp
from model import text_cosine_similarity


def processed_doc(doc):
    processed_doc = {}

    processed_doc["document_id"] = int(doc["document_id"])
    processed_doc["raw_text"] = doc["text"]
    processed_doc["invoice_number"] = fetching_numbers_from_text(doc["text"])
    processed_doc["shop"] = doc["shop"].upper()
    processed_doc["total"] = doc["total"].split()[0]
    processed_doc["currency"] = doc["total"].split()[-1]
    processed_doc["timestamp"] = doc["timestamp"]
    processed_doc["items"] = doc["purchase"]

    return processed_doc


def llm_processing(processed_doc):
    llm_score_threshold = 0.8
    llm_score = 0

    raw_text = [
        w
        for w in processed_doc["raw_text"].split()
        if w.lower() not in {"invoice", "number", "from"}
    ]

    rule_based_text = processed_doc["invoice_number"] + " " + processed_doc["shop"]
    llm_score = text_cosine_similarity(" ".join(raw_text), rule_based_text)

    if llm_score < llm_score_threshold:
        processed_doc["review_required"] = True
    else:
        processed_doc["review_required"] = False

    processed_doc["llm_score"] = round(llm_score, 2)
    processed_doc["raw_text_for_llm"] = " ".join(raw_text)
    processed_doc["rule_based_text"] = rule_based_text

    return processed_doc


def process_monitoring_doc(processed_doc, number_of_items):
    monitoring_doc = {}
    monitoring_doc["document_id"] = processed_doc["document_id"]
    monitoring_doc["number_of_files_read_in_batch"] = number_of_items
    monitoring_doc["invoice_number"] = processed_doc["invoice_number"]
    monitoring_doc["raw_text"] = processed_doc["raw_text"]
    monitoring_doc["shop"] = processed_doc["shop"]
    monitoring_doc["total"] = processed_doc["total"]
    monitoring_doc["currency"] = processed_doc["currency"]
    monitoring_doc["timestamp"] = current_timestamp()
    monitoring_doc["raw_text_for_llm"] = processed_doc["raw_text_for_llm"]
    monitoring_doc["rule_based_text"] = processed_doc["rule_based_text"]
    monitoring_doc["review_required"] = processed_doc["review_required"]
    monitoring_doc["llm_score"] = processed_doc["llm_score"]

    return monitoring_doc


def flattened_doc(processed_doc):

    data = []
    for item in processed_doc["items"]:
        flattened_doc = {}
        flattened_doc["document_id"] = processed_doc["document_id"]
        flattened_doc["raw_text"] = processed_doc["raw_text"]
        flattened_doc["invoice_number"] = processed_doc["invoice_number"]
        flattened_doc["shop"] = processed_doc["shop"]
        flattened_doc["total"] = processed_doc["total"]
        flattened_doc["currency"] = processed_doc["currency"]
        flattened_doc["timestamp"] = processed_doc["timestamp"]
        flattened_doc["item"] = item["item"]
        flattened_doc["price"] = item["price"]
        data.append(flattened_doc)

    return data

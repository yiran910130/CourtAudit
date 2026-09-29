# Input schemas

## Dataset records: JSONL
Required: `record_id`, `source_id`, `text`.
Recommended: `split`, `record_hash`, `court`, `case_id`, `document_id`, `language`, `label`.

## Annotations: CSV
Required columns: `item_id`, `coder_id`, `label`.

## Predictions: CSV
Required columns: `y_true`, `y_pred`, `confidence` where confidence is the confidence assigned to `y_pred`.

## Agent outputs: JSONL
Audited fields include `request_id`, `response_text`, `completion_status`, `direct_model_inference`, `web_search_used`, and `external_sources_used`.

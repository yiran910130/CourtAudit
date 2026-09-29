# CourtAudit

CourtAudit is an open-source Python toolkit for auditable institutional-language NLP workflows. The pilot release checks dataset schema, provenance hashes, split leakage, annotation reliability, binary calibration, and model/agent-output policy fields. It writes machine-readable JSON and human-readable Markdown reports.

## Install

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e .[dev]
```

## Run the clean demo

```bash
courtaudit report demo_data/records_clean.jsonl \
  --annotations demo_data/annotations.csv \
  --predictions demo_data/predictions.csv \
  --agent-outputs demo_data/agent_outputs_clean.jsonl \
  --out-json demo_output/report_clean.json \
  --out-md demo_output/report_clean.md \
  --deterministic
```

## Run the flagged demo

```bash
courtaudit leakage demo_data/records_flagged.jsonl
courtaudit agent-audit demo_data/agent_outputs_flagged.jsonl
```

## Commands

- `courtaudit validate RECORDS.jsonl`
- `courtaudit provenance RECORDS.jsonl`
- `courtaudit leakage RECORDS.jsonl`
- `courtaudit reliability ANNOTATIONS.csv`
- `courtaudit calibration PREDICTIONS.csv --bins 10`
- `courtaudit agent-audit OUTPUTS.jsonl`
- `courtaudit report RECORDS.jsonl [--annotations ... --predictions ... --agent-outputs ...]`

## Input contracts

The minimum record schema contains `record_id`, `source_id`, and `text`. Leakage checks also use `split`. Annotation reliability expects `item_id,coder_id,label`. Binary calibration expects `y_true,y_pred,confidence`. Agent-output auditing accepts the fields documented in `docs/INPUT_SCHEMAS.md`.

## Scope

CourtAudit reports deterministic checks that are supported by the supplied records. It does not infer legal validity, adjudicate case outcomes, or diagnose the cause of annotation or model errors.

## License

MIT. Source text and third-party datasets keep their original licenses and access conditions.

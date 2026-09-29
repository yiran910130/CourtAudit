import json
from pathlib import Path
import pytest
from courtaudit.io import read_jsonl, write_json
from courtaudit.schema import validate_records
from courtaudit.provenance import record_hash, audit_record_hashes
from courtaudit.reliability import audit_annotations, cohens_kappa, krippendorff_alpha_nominal
from courtaudit.calibration import audit_binary_predictions
from courtaudit.agent import audit_agent_outputs
from courtaudit.report import build_report, report_markdown, write_report
from courtaudit.cli import main


def test_io_errors_and_write(tmp_path):
    bad=tmp_path/'bad.jsonl'; bad.write_text('{bad}\n',encoding='utf-8')
    with pytest.raises(ValueError): read_jsonl(bad)
    non=tmp_path/'non.jsonl'; non.write_text('[1,2]\n',encoding='utf-8')
    with pytest.raises(ValueError): read_jsonl(non)
    out=tmp_path/'x.json'; write_json(out, {'b':1}); assert json.loads(out.read_text())=={'b':1}


def test_schema_duplicate_and_text_type():
    r=validate_records([{'record_id':'x','source_id':'s','text':3},{'record_id':'x','source_id':'t','text':'ok'}])
    assert not r['valid']
    assert any(e['code']=='DUPLICATE_RECORD_ID' for e in r['errors'])
    assert any(e['code']=='TEXT_NOT_STRING' for e in r['errors'])


def test_provenance_mismatch():
    rec={'record_id':'x','source_id':'s','text':'a'}
    rec2=dict(rec, record_hash='deadbeef')
    a=audit_record_hashes([rec]); b=audit_record_hashes([rec2])
    assert a['n_declared_hashes_checked']==0
    assert b['n_mismatches']==1
    assert len(record_hash(rec))==64


def test_reliability_edge_cases():
    assert cohens_kappa([]) is None
    assert krippendorff_alpha_nominal({}) is None
    r=audit_annotations([{'item_id':'1','coder_id':'a','label':'X'},{'item_id':'1','coder_id':'b','label':'X'},{'item_id':'1','coder_id':'c','label':'Y'}])
    assert r['n_coders']==3
    assert r['cohens_kappa_two_coders'] is None


def test_calibration_invalid_and_empty():
    r=audit_binary_predictions([{'y_true':'x','y_pred':'1','confidence':'0.5'}])
    assert r['n']==0
    r=audit_binary_predictions([{'y_true':'1','y_pred':'1','confidence':'1.0'},{'y_true':'0','y_pred':'1','confidence':'0.6'}],bins=2)
    assert r['n']==2 and len(r['bin_details'])>=1


def test_agent_all_issue_types():
    rows=[{'request_id':'a','response_text':'','completion_status':'partial','direct_model_inference':False,'web_search_used':True,'external_sources_used':True},{}]
    r=audit_agent_outputs(rows)
    codes={x['code'] for x in r['issues']}
    assert {'INCOMPLETE_RESPONSE','NON_DIRECT_INFERENCE','WEB_SEARCH_USED','EXTERNAL_SOURCE_USED','EMPTY_RESPONSE','MISSING_AGENT_FIELD'} <= codes


def test_report_markdown_and_write(tmp_path):
    base=Path(__file__).parents[1]/'demo_data'
    r=build_report(str(base/'records_clean.jsonl'), str(base/'annotations.csv'), str(base/'predictions.csv'), str(base/'agent_outputs_clean.jsonl'), deterministic=True)
    md=report_markdown(r); assert 'Overall gate status' in md
    j=tmp_path/'r.json'; m=tmp_path/'r.md'; write_report(r,str(j),str(m)); assert j.exists() and m.exists()


def test_cli_commands(tmp_path, capsys):
    base=Path(__file__).parents[1]/'demo_data'
    assert main(['validate',str(base/'records_clean.jsonl')])==0
    assert main(['provenance',str(base/'records_clean.jsonl')])==0
    assert main(['leakage',str(base/'records_clean.jsonl')])==0
    assert main(['reliability',str(base/'annotations.csv')])==0
    assert main(['calibration',str(base/'predictions.csv'),'--bins','5'])==0
    assert main(['agent-audit',str(base/'agent_outputs_clean.jsonl')])==0
    j=tmp_path/'o.json'; m=tmp_path/'o.md'
    assert main(['report',str(base/'records_clean.jsonl'),'--annotations',str(base/'annotations.csv'),'--predictions',str(base/'predictions.csv'),'--agent-outputs',str(base/'agent_outputs_clean.jsonl'),'--out-json',str(j),'--out-md',str(m),'--deterministic'])==0
    assert j.exists() and m.exists()

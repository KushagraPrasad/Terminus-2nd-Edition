### Decision
GO

### Metadata
- Task name: wire-protocol-from-pcap-inference
- Title: Wire Protocol From PCAP Inference
- Category: software-engineering
- Task shape: reverse_engineering
- Languages: ["python"]
- Difficulty: hard
- Milestones: 4

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.pcap_runner` rebuilds `/app/output/wire_protocol_from_pcap_inference_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by PCAP excerpts imply inconsistent length-prefix rules across connection arms.

### subtype_milestone_plan
- milestone_count: 4
- sequential_dependency: strict

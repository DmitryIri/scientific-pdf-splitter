# Roadmap

This roadmap keeps the portfolio project honest about what is implemented now and what belongs to later phases.

## Phase 0 - Completed

Repository setup and publication:

- public GitHub repository created
- local clone created
- GitHub CLI workflow verified
- initial repository metadata configured

## Phase B.1 - Completed

Portfolio skeleton and synthetic demo:

- Python package structure under `src/pdf_splitter/`
- typed article metadata model
- CSV and JSON output writers
- validation helpers
- synthetic sample generator
- runnable quickstart example
- pytest and ruff configuration
- GitHub Actions CI
- MIT license

## Phase B.1.1 - Completed

Commercial polish:

- README clarified for a business and technical audience
- current scope stated explicitly as a synthetic demo and portfolio project
- potential business applications added
- next implementation layer documented without overclaiming
- repository description and topics aligned with the current implementation

## Phase B.2 - Planned

Extraction implementation layer:

- evaluate the public source project for reusable extraction patterns
- add PDF text extraction module
- add article boundary detection module
- add metadata parsing module
- add tests for realistic but non-private sample inputs
- keep internal paths, private data, and project-specific operating files out of the public repository

## Future Enhancements

Possible future work after Phase B.2:

- reference section isolation
- issue-level validation reports
- richer sample fixtures
- command-line interface
- benchmark notes for supported PDF layouts
- integration examples for downstream ETL workflows
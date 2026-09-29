# GitHub release guide for CourtAudit v0.1.0

This guide assumes Git is installed and you have a GitHub account.

## 1. Create the repository
1. Sign in to GitHub.
2. Select **New repository**.
3. Repository name: `CourtAudit`.
4. Description: `Open-source audit toolkit for institutional-language NLP.`
5. Choose **Public** for the SoftwareX release.
6. Do not initialize with a README, license, or `.gitignore`; the pilot package already contains them.
7. Create the repository.

## 2. Repository identity already configured
This release package is already configured for GitHub user `yiran910130`. The repository URL in `CITATION.cff` is `https://github.com/yiran910130/CourtAudit`. You may add an institutional support email later if you want it public.

## 3. Run the local checks
From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .[dev]
pytest -q
courtaudit report demo_data/records_clean.jsonl --annotations demo_data/annotations.csv --predictions demo_data/predictions.csv --agent-outputs demo_data/agent_outputs_clean.jsonl --out-json demo_output/report_clean.json --out-md demo_output/report_clean.md
```

Confirm that all tests pass and that the clean demo reports `overall_pass: true`.

## 4. Initialize Git and push `main`
Copy the repository URL shown by GitHub, then run:

```bash
git init
git branch -M main
git add .
git commit -m "CourtAudit v0.1.0 pilot release"
git remote add origin https://github.com/yiran910130/CourtAudit.git
git push -u origin main
```

## 5. Check GitHub Actions
Open the repository's **Actions** tab. The `tests` workflow should run on Python 3.10, 3.11, and 3.12. Do not create the release tag until all matrix jobs pass.

## 6. Create the version tag

```bash
git tag -a v0.1.0 -m "CourtAudit v0.1.0"
git push origin v0.1.0
```

## 7. Create the GitHub Release
1. Open **Releases** -> **Draft a new release**.
2. Select tag `v0.1.0`.
3. Release title: `CourtAudit v0.1.0 - pilot release`.
4. Copy the v0.1.0 notes from `CHANGELOG.md`.
5. Attach the source ZIP if desired. GitHub also generates source archives automatically.
6. Publish the release.

## 8. Create a citable archive
Recommended route: connect the GitHub repository to Zenodo, enable archiving for the repository, then create a new GitHub release after the connection is active. Zenodo will mint a DOI for the archived release. Add that DOI to `CITATION.cff`, the manuscript Code Availability statement, and the SoftwareX code-metadata table. Commit the DOI update and create a final archival tag if your workflow requires one.

## 9. Freeze the submission version
Before SoftwareX submission, record:
- GitHub release URL and tag;
- commit SHA;
- Zenodo DOI;
- Python versions tested in CI;
- SHA-256 of the pilot release ZIP;
- exact `requirements`/environment metadata.

## 10. Submission checks
Confirm that the repository contains the MIT license, installation instructions, test programs, demo data, CI configuration, documentation, and the exact tagged version referenced by the manuscript. These items map directly to SoftwareX reviewer checks.

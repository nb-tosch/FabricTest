Fabric Initial Deployment

Purpose
- This repository is prepared for an initial deployment to one customer Fabric workspace using fabric-cicd.
- It is intentionally set up for bootstrap deployment, not continuous bi-directional sync.

Important limitation
- fabric-cicd expects a repository that contains Fabric Source Control item definitions.
- If your files are custom JSON/IPYNB only, deployment may partially fail or only parameterization steps may apply.

Files in this setup
- config.yml: config-based deployment settings.
- parameter.yml: environment-based value replacements.
- deploy_fabric.py: run deployment with explicit auth.
- requirements.txt: Python dependencies.

One-time setup
1. Update workspace ID in config.yml for default.
2. Keep or adjust item_types_in_scope in config.yml.
3. Review replacements in parameter.yml and match them to real values for the target environment.
4. Install dependencies:
   - pip install -r requirements.txt

Authentication options
- Azure CLI:
  - az login
  - python deploy_fabric.py --environment default --auth azcli
- Azure PowerShell:
  - Connect-AzAccount
  - python deploy_fabric.py --environment default --auth azps
- Service Principal:
  - python deploy_fabric.py --environment default --auth spn --tenant-id <tenant> --client-id <client> --client-secret <secret>

Recommended first rollout flow
1. Deploy to default first.
2. Validate created items in Fabric workspace.
3. Keep unpublish.skip=true in initial phase to avoid accidental deletions.

Fabric notebook option
1. Open fabric_notebook_deploy.ipynb in Fabric.
2. Run cell 1 (install dependencies).
3. Run cell 2 after setting workspace_id/repo_url/repo_ref values.

Troubleshooting hints
- Environment key must exist in config.yml and parameter.yml.
- Config path is resolved absolutely by deploy_fabric.py.
- If publish fails with unsupported structure, export items from Fabric Source Control and replace local custom structure with item-name.item-type folders.

import argparse
from pathlib import Path

from azure.identity import AzureCliCredential, AzurePowerShellCredential, ClientSecretCredential
from fabric_cicd import deploy_with_config


def build_credential(args: argparse.Namespace):
    auth = args.auth.lower()

    if auth == "azcli":
        return AzureCliCredential()

    if auth == "azps":
        return AzurePowerShellCredential()

    if auth == "spn":
        missing = [
            name
            for name, value in [
                ("tenant_id", args.tenant_id),
                ("client_id", args.client_id),
                ("client_secret", args.client_secret),
            ]
            if not value
        ]
        if missing:
            raise ValueError(f"Missing required --auth spn arguments: {', '.join(missing)}")

        return ClientSecretCredential(
            tenant_id=args.tenant_id,
            client_id=args.client_id,
            client_secret=args.client_secret,
        )

    raise ValueError("Unsupported auth method. Use: azcli, azps, or spn")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Initial Fabric deployment using fabric-cicd config deployment."
    )
    parser.add_argument(
        "--environment",
        required=True,
        choices=["default", "dev", "test", "prod"],
        help="Environment key to select in config.yml",
    )
    parser.add_argument(
        "--config",
        default="config.yml",
        help="Path to config.yml (default: config.yml)",
    )
    parser.add_argument(
        "--auth",
        default="azcli",
        choices=["azcli", "azps", "spn"],
        help="Authentication method",
    )
    parser.add_argument("--tenant-id", dest="tenant_id", help="Required for --auth spn")
    parser.add_argument("--client-id", dest="client_id", help="Required for --auth spn")
    parser.add_argument("--client-secret", dest="client_secret", help="Required for --auth spn")

    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    credential = build_credential(args)

    result = deploy_with_config(
        config_file_path=str(config_path),
        environment=args.environment,
        token_credential=credential,
    )

    print(f"Deployment status: {result.status}")
    print(f"Deployment message: {result.message}")


if __name__ == "__main__":
    main()

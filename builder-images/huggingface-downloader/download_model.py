import argparse
import os
import fnmatch
import subprocess
from huggingface_hub import list_repo_files, hf_hub_url, snapshot_download

def expand_env_var(value: str) -> str:
    """Expand ${VAR} in the value using os.environ"""
    if not value:
        return value
    return os.path.expandvars(value)

def aria2_download(url: str, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cmd = [
        "aria2c",
        "-x", "16",
        "-s", "16",
        "-j", "16",
        "-k", "1M",
        "-c",
        "-d", os.path.dirname(output_path),
        "-o", os.path.basename(output_path),
        url,
    ]
    print(f"[aria2] Downloading: {url}")
    subprocess.run(cmd, check=True)

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-m", 
        "--model-repo", 
        type=str, 
        help="HuggingFace model repo"
    )
    parser.add_argument(
        "-t", 
        "--target-dir", 
        type=str, 
        default="./models", 
        help="Target directory"
    )
    parser.add_argument(
        "-a", 
        "--allow-patterns", 
        nargs="+", 
        help="Allowed patterns to download"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--use-aria2", 
        dest="use_aria2", 
        action="store_true", 
        help="Use aria2 to download files"
    )
    group.add_argument(
        "--no-aria2", 
        dest="use_aria2", 
        action="store_false", 
        help="Do not use aria2, use snapshot_download instead"
        )
    parser.set_defaults(use_aria2=True)
    args = parser.parse_args()

    model_repo = args.model_repo or os.environ.get("MODEL_REPO")
    target_dir = args.target_dir or os.environ.get("TARGET_DIR", "./models")

    model_repo = expand_env_var(model_repo)
    target_dir = expand_env_var(target_dir)

    default_allow_patterns = ["*.safetensors", "*.json", "*.txt", "*.sig", "*.jinja"]
    allow_patterns_env = os.environ.get("ALLOW_PATTERNS")
    if args.allow_patterns:
        allow_patterns = args.allow_patterns
    elif allow_patterns_env:
        allow_patterns = [p.strip() for p in allow_patterns_env.replace(",", " ")
                          .split()]
    else:
        allow_patterns = default_allow_patterns

    print(f"MODEL_REPO     = {model_repo}")
    print(f"TARGET_DIR     = {target_dir}")
    print(f"ALLOW_PATTERNS = {allow_patterns}")
    print(f"USE_ARIA2      = {args.use_aria2}")

    os.makedirs(target_dir, exist_ok=True)

    all_files = list_repo_files(model_repo)
    matched = [f for f in all_files if any(fnmatch.fnmatch(f, p) for p in allow_patterns)]

    if not matched:
        print("No files matched patterns!")
        return

    print(f"Matched {len(matched)} files:")
    for f in matched:
        print(f"  - {f}")

    for f in matched:
        url = hf_hub_url(model_repo, f)
        out_path = os.path.join(target_dir, f)
        if args.use_aria2:
            aria2_download(url, out_path)
        else:
            snapshot_download(
                repo_id=model_repo,
                local_dir=os.path.dirname(out_path),
                allow_patterns=[os.path.basename(out_path)]
            )

    print("\nAll files downloaded successfully!")

if __name__ == "__main__":
    main()

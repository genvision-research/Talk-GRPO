from pathlib import Path
import shutil

from app import app, load_data

BASE_DIR = Path(__file__).resolve().parent
BUILD_DIR = BASE_DIR / "docs"

STATIC_DIRS = [
    "assets",
    "images",
    "test_videos",
    "qualitative_results",
]


def copy_directory(name: str):
    src = BASE_DIR / name
    dst = BUILD_DIR / name

    if not src.exists():
        print(f"[SKIP] {src} does not exist")
        return

    shutil.copytree(src, dst, dirs_exist_ok=True)
    print(f"[COPY] {src} -> {dst}")


def main():
    # Clean previous build
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    # Render Jinja template into static HTML
    data = load_data()

    with app.app_context():
        html = app.jinja_env.get_template("index.html").render(data=data)

    output_file = BUILD_DIR / "index.html"
    output_file.write_text(html, encoding="utf-8")
    print(f"[BUILD] {output_file}")

    # Copy static folders
    for directory in STATIC_DIRS:
        copy_directory(directory)

    # Prevent Jekyll processing
    (BUILD_DIR / ".nojekyll").touch()

    print("\nBuild completed.")
    print(f"Static site: {BUILD_DIR}")
    print("\nTest locally with:")
    print("  cd docs")
    print("  python -m http.server 8000")


if __name__ == "__main__":
    main()
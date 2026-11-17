"""檢查技能的必要格式，不執行技能內容。"""

import argparse
from pathlib import Path
import re
import sys

try:
    import yaml
except ImportError:
    raise SystemExit("請先執行 python -m pip install -r requirements-dev.txt") from None


REPO_ROOT = Path(__file__).resolve().parents[1]
NAME_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def validate_skill(directory: Path) -> list[str]:
    """回傳單一技能的格式錯誤；空清單表示格式通過。"""
    skill_file = directory / "SKILL.md"
    try:
        lines = skill_file.read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError) as error:
        return [f"無法讀取 SKILL.md：{error}"]

    if not lines or lines[0].strip() != "---":
        return ["SKILL.md 必須以 YAML frontmatter 開始（---）。"]

    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return ["YAML frontmatter 缺少結束標記（---）。"]

    try:
        metadata = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as error:
        return [f"frontmatter 不是有效的 YAML：{error}"]
    if not isinstance(metadata, dict):
        return ["frontmatter 必須是 YAML mapping。"]

    errors = []
    name = metadata.get("name")
    if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name) or len(name) > 64:
        errors.append("name 必須為 1–64 字元的小寫英數名稱，可使用單一連字號分隔。")
    elif name != directory.name:
        errors.append(f"name（{name}）必須與目錄名稱（{directory.name}）一致。")

    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("description 必須是非空白字串。")
    elif len(description) > 1024:
        errors.append("description 不得超過 1024 個字元。")

    if not "\n".join(lines[end + 1 :]).strip():
        errors.append("SKILL.md 必須包含操作指引內文。")

    agent_file = directory / "agents" / "openai.yaml"
    if agent_file.exists():
        try:
            agent_metadata = yaml.safe_load(agent_file.read_text(encoding="utf-8-sig"))
            if not isinstance(agent_metadata, dict):
                errors.append("agents/openai.yaml 必須是 YAML mapping。")
        except (OSError, UnicodeError, yaml.YAMLError) as error:
            errors.append(f"無法解析 agents/openai.yaml：{error}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directories", nargs="*", type=Path, help="技能目錄；預設檢查 skills/ 與 templates/")
    arguments = parser.parse_args()
    directories = arguments.directories
    if not directories:
        directories = []
        for collection in (REPO_ROOT / "skills", REPO_ROOT / "templates"):
            if not collection.is_dir():
                print(f"錯誤：找不到目錄 {collection}", file=sys.stderr)
                return 1
            directories.extend(sorted(path for path in collection.iterdir() if path.is_dir() and not path.name.startswith(".")))

    failed = 0
    for directory in directories:
        errors = validate_skill(directory)
        if errors:
            failed += 1
            for error in errors:
                print(f"錯誤 {directory}：{error}", file=sys.stderr)
        else:
            print(f"通過 {directory}")

    print(f"共檢查 {len(directories)} 個技能／範本，{failed} 個未通過。")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

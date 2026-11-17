"""以暫存技能驗證有效與錯誤輸入的行為。"""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.validate_skills import REPO_ROOT, validate_skill


VALID_SKILL = "---\nname: sample-skill\ndescription: 處理測試資料。\n---\n\n# 測試技能\n\n檢查處理結果。\n"


class ValidateSkillsTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.skill = Path(self.workspace.name) / "sample-skill"
        self.skill.mkdir()

    def write_skill(self, content=VALID_SKILL):
        (self.skill / "SKILL.md").write_text(content, encoding="utf-8")

    def test_valid_skill_with_optional_resources(self):
        self.write_skill()
        (self.skill / "references").mkdir()
        (self.skill / "agents").mkdir()
        (self.skill / "agents" / "openai.yaml").write_text('interface:\n  display_name: "測試技能"\n', encoding="utf-8")
        self.assertEqual(validate_skill(self.skill), [])

    def test_rejects_missing_skill_file(self):
        self.assertTrue(validate_skill(self.skill))

    def test_rejects_invalid_frontmatter(self):
        for content in ("# 沒有 frontmatter", "---\nname: sample-skill", "---\nname: [\n---\n內文", "---\n- name\n---\n內文"):
            with self.subTest(content=content):
                self.write_skill(content)
                self.assertTrue(validate_skill(self.skill))

    def test_rejects_invalid_or_mismatched_names(self):
        for name in ("other-skill", "Sample-Skill", "sample--skill", "a" * 65, "true"):
            with self.subTest(name=name):
                self.write_skill(VALID_SKILL.replace("name: sample-skill", f"name: {name}"))
                self.assertTrue(validate_skill(self.skill))

    def test_rejects_missing_or_invalid_description(self):
        for value in ('""', "true", "[]", '"' + "字" * 1025 + '"'):
            with self.subTest(value=value):
                self.write_skill(VALID_SKILL.replace("description: 處理測試資料。", f"description: {value}"))
                self.assertTrue(validate_skill(self.skill))

    def test_rejects_empty_body(self):
        self.write_skill("---\nname: sample-skill\ndescription: 測試。\n---\n\n")
        self.assertTrue(validate_skill(self.skill))

    def test_rejects_invalid_agent_yaml(self):
        self.write_skill()
        (self.skill / "agents").mkdir()
        (self.skill / "agents" / "openai.yaml").write_text("interface: [", encoding="utf-8")
        self.assertTrue(validate_skill(self.skill))

    def test_cli_reports_failure_with_nonzero_exit_code(self):
        result = subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "validate_skills.py"), str(self.skill)], capture_output=True)
        self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()

# 個人 Skills

個人維護的 AI Agent Skills 集合。每個技能以獨立目錄保存，透過 `SKILL.md` 說明適用情境與操作方式。

## 專案結構

```text
skills/
├── .github/workflows/validate.yml  # 推送與 PR 的自動驗證
├── skills/                        # 正式技能，目前尚未加入
├── templates/skill-template/
│   └── SKILL.md                    # 新技能的起點
├── scripts/validate_skills.py      # 格式驗證工具
├── tests/test_validate_skills.py   # 驗證工具的測試
├── requirements-dev.txt           # 開發依賴
├── AGENTS.md                       # 協作慣例
└── README.md
```

## 新增技能

以下指令使用 PowerShell，請先安裝 Python 3.11 以上版本：

```powershell
git clone https://github.com/yurychang/skills.git
cd skills
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements-dev.txt
Copy-Item -Recurse templates/skill-template skills/my-skill
```

編輯 `skills/my-skill/SKILL.md`：

- 將 frontmatter 的 `name` 改成 `my-skill`，與目錄名稱一致。
- 用 `description` 說明技能的用途與何時使用。
- 將內文換成實際操作指引，保留會影響判斷的必要資訊。
- 有需要時才新增 `scripts/`、`references/`、`assets/` 或 `agents/openai.yaml`。

完成後執行：

```powershell
.venv/Scripts/python scripts/validate_skills.py
.venv/Scripts/python -m unittest discover -s tests -v
```

macOS／Linux 的虛擬環境執行檔路徑為 `.venv/bin/python`；複製範本可使用 `cp -R templates/skill-template skills/my-skill`。

## 技能格式

```markdown
---
name: my-skill
description: 說明這個技能完成什麼工作，以及適用的請求。
---

# 技能名稱

具體的操作指引。
```

名稱使用小寫英文字母、數字與連字號，最多 64 個字元。技能應能獨立使用；參考文件與資產透過相對路徑引用。

## 驗證範圍

驗證工具檢查 `skills/` 與 `templates/` 下各個技能的 frontmatter、名稱、描述及內文；若有 `agents/openai.yaml`，也會檢查它是有效的 YAML mapping。可傳入單一技能目錄：

```powershell
.venv/Scripts/python scripts/validate_skills.py skills/my-skill
```

格式通過不代表技能的實際行為已驗證。發布前仍需用對應的真實請求確認結果。

# 個人 Agent Skills

[![驗證技能](https://github.com/yurychang/skills/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/yurychang/skills/actions/workflows/validate.yml)

由 [@yurychang](https://github.com/yurychang) 維護的個人 AI Agent 技能集合，將可重複使用的工作方法整理成獨立的 `SKILL.md`、腳本與參考資料，方便持續改進與分享。

> **目前提供 1 個正式技能：[optimize-ui](skills/optimize-ui/SKILL.md)。**
> 改善既有網頁或桌面 App 的 UI／UX，沿用原有技術與設計系統，提供視覺示意並以實際畫面與操作驗證。

**[技能清單](#技能清單) · [安裝與使用](#安裝與使用) · [新增技能](#新增技能) · [格式規範](#格式規範) · [驗證與測試](#驗證與測試) · [貢獻方式](#貢獻方式)**

## 這個專案提供什麼

Skill 是一個包含操作指引與必要資源的目錄，讓支援技能的 Agent 在對應情境使用既定的工作方法。本專案採用 [Agent Skills 格式](https://agentskills.io/specification) 作為基本結構。

| 內容 | 用途 | 入口 |
| --- | --- | --- |
| 正式技能 | 可獨立使用的工作指引與資源，目前提供 `optimize-ui` | [`skills/`](skills/) |
| 技能範本 | 建立新技能時的起點 | [`SKILL.md`](templates/skill-template/SKILL.md) |
| 格式驗證 | 檢查技能名稱、描述與必要結構 | [`validate_skills.py`](scripts/validate_skills.py) |
| 自動檢查 | 推送至 `main`、提出 PR 或手動觸發時執行驗證與工具測試 | [GitHub Actions](https://github.com/yurychang/skills/actions/workflows/validate.yml) |
| 協作規範 | 撰寫與維護技能的共同慣例 | [`AGENTS.md`](AGENTS.md) |

## 技能清單

| 技能 | 用途 | 適用情境 |
| --- | --- | --- |
| [`optimize-ui`](skills/optimize-ui/SKILL.md) | 審查並改善既有介面的排版、元件樣式、資訊層級與互動可用性，產出示意圖並驗證修改後的實際畫面 | UI polish、畫面太亂、設定頁整理、表單操作不順、動態狀態與版面位移檢查 |

每個技能的依賴、操作方式及驗證限制，以該目錄的 `SKILL.md` 為準。新增技能可從[範本](templates/skill-template/SKILL.md)開始。

## 安裝與使用

目前可安裝 `optimize-ui`。請在需要使用它的專案目錄執行以下指令。

### 使用 Skills CLI

依 [Skills CLI 官方說明](https://github.com/vercel-labs/skills#install-a-skill)，需先安裝 Node.js 22.20 以上版本。在要使用技能的專案目錄執行：

```sh
npx skills add yurychang/skills --skill optimize-ui
```

依 CLI 提示選擇目標 Agent；預設安裝到目前專案。若要跨專案使用，可在上述指令加上 `-g`。CLI 會處理不同 Agent 的安裝位置，完整選項請參考其官方文件。

### 手動安裝

也可以複製選定技能的**完整目錄**，放到目標 Agent 支援的技能路徑。若技能內有 `scripts/`、`references/` 或 `assets/`，請一起保留；只複製 `SKILL.md` 可能遺漏必要資源。

安裝後可在 Agent 中明確提出請求，例如：

```text
請使用 optimize-ui 優化這個專案的設定頁。
沿用現有元件與設計系統，改善分組、資訊層級與操作回饋，保留原有功能及未保存草稿。
提供視覺示意圖，完成實作後檢查實際畫面、相關操作與動態狀態的版面位移。
```

各 Agent 的載入、重新整理與呼叫方式，依該產品文件為準。技能格式相同不代表工具權限與執行環境相同；目前本 repo 尚未完成任何 Agent 的實際安裝或行為驗證。

### optimize-ui 的使用條件與成果

- 審查可從使用者描述、截圖、程式碼或可操作畫面開始；落實修改時需有可編輯的目標專案。
- 技能不綁定特定前端或原生框架，實作沿用目標專案的技術、元件與設計 token。
- 視覺優化需產出並展示示意圖，且與實際產品驗證證據分開。實際畫面與互動驗證需有可用且獲允許的瀏覽器或原生介面工具；遵守目標專案既有的測試限制。
- 交付包含具體改善、對應情境、示意圖、實際驗證結果與未驗證範圍。只要求審查時提供問題與改法；要求實作且已有專案時，依授權範圍完成修改。

## 專案結構

```text
skills/
├── .github/
│   └── workflows/validate.yml      # GitHub Actions 自動檢查
├── skills/                        # 正式技能，每個技能一個目錄
│   └── optimize-ui/
│       ├── SKILL.md                # UI／UX 優化指引
│       └── agents/openai.yaml      # 技能介面 metadata
├── templates/
│   └── skill-template/
│       └── SKILL.md                # 新技能範本
├── scripts/
│   └── validate_skills.py          # repo 格式驗證工具
├── tests/
│   └── test_validate_skills.py      # 驗證工具的行為測試
├── .gitattributes                  # 文字檔換行設定
├── .gitignore                      # 本機環境與暫存檔排除規則
├── requirements-dev.txt            # 驗證工具的開發依賴
├── AGENTS.md                       # 協作規範
└── README.md
```

repo 根目錄的 `scripts/` 用於維護整個集合；`skills/<skill-name>/scripts/` 則是該技能自身需要的工具。

## 新增技能

### 環境需求

| 項目 | 何時需要 |
| --- | --- |
| Git | 複製 repo、提交變更 |
| Python 3.11 以上，含 `venv` 與 `pip` | 執行格式驗證與工具測試 |
| `requirements-dev.txt` 中的依賴 | 開發驗證，目前為 PyYAML |
| Node.js 22.20 以上 | 選用 Skills CLI 安裝技能時才需要 |

每個技能的執行依賴另行記錄於自身的 `SKILL.md`；開發驗證環境不等於所有技能的使用需求。

### 複製 repo 與範本

Windows／PowerShell：

```powershell
git clone https://github.com/yurychang/skills.git
cd skills
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements-dev.txt
Copy-Item -Recurse templates/skill-template skills/my-skill
```

macOS／Linux：

```sh
git clone https://github.com/yurychang/skills.git
cd skills
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
cp -R templates/skill-template skills/my-skill
```

這些指令使用虛擬環境中的 Python，不需啟用虛擬環境，也不會要求全域安裝套件。

### 完成技能內容

1. 將目錄 `my-skill` 與 frontmatter 的 `name` 改成相同的實際名稱。
2. 改寫 `description`，說明技能做什麼、適用哪些請求。
3. 將範本內文換成實際指引，交代必要輸入、操作方式、交付成果與驗證方式。
4. 有實際需要時再加入腳本、參考文件或資產，並從 `SKILL.md` 連結。
5. 用代表性的請求驗證技能行為，記錄實際結果與尚未驗證的限制。
6. 更新本 README 的技能清單、正式技能數量與狀態說明，再執行[格式驗證與工具測試](#驗證與測試)。

## 格式規範

每個技能至少包含一份 `SKILL.md`，由 YAML frontmatter 與 Markdown 操作指引組成：

```markdown
---
name: my-skill
description: 將指定來源整理成可核對的摘要；適用於使用者要求彙整文件重點並保留來源連結時。
---

# 技能名稱

說明需要哪些輸入、如何完成任務，以及如何驗證交付成果。
```

| 項目 | 本 repo 的要求 |
| --- | --- |
| 目錄 | `skills/<skill-name>/` |
| `name` | 與目錄名稱一致；1–64 字元，小寫英文字母、數字與連字號；連字號不得在開頭、結尾或連續出現 |
| `description` | 1–1024 字元的非空白字串，清楚描述用途與適用情境 |
| Markdown 內文 | 必須有內容，提供可執行的操作指引 |
| 檔案編碼 | UTF-8 |

可依技能需求加入以下內容，無須建立空目錄：

| 路徑 | 適用內容 |
| --- | --- |
| `scripts/` | 值得重複執行或需要確定性結果的工具 |
| `references/` | 按需讀取的詳細參考資料 |
| `assets/` | 產出會用到的範本、圖片或其他資源 |
| `agents/openai.yaml` | 適用產品使用的介面 metadata 與選用設定，非必要檔案 |

保持主指引精簡，將較長的參考資料拆到獨立檔案，使用相對路徑連結。其他 frontmatter 欄位與格式細節請參考 [Agent Skills 規格](https://agentskills.io/specification)。

## 驗證與測試

在 repo 根目錄執行以下指令。

Windows／PowerShell：

```powershell
# 檢查全部正式技能與範本
.venv/Scripts/python scripts/validate_skills.py

# 只檢查已建立的單一技能
.venv/Scripts/python scripts/validate_skills.py skills/my-skill

# 執行驗證工具的測試
.venv/Scripts/python -m unittest discover -s tests -v
```

macOS／Linux：

```sh
.venv/bin/python scripts/validate_skills.py
.venv/bin/python scripts/validate_skills.py skills/my-skill
.venv/bin/python -m unittest discover -s tests -v
```

未指定技能目錄時，工具會檢查 `skills/` 與 `templates/` 下的技能目錄。成功時結束碼為 `0`，出現格式錯誤時為 `1`。

| 會檢查 | 不涵蓋 |
| --- | --- |
| `SKILL.md` 是否存在且可讀取 | 技能是否完成使用者的實際任務 |
| frontmatter 是否為有效 YAML mapping | 未列出的選用欄位是否符合完整規格 |
| 名稱、目錄、描述與內文的必要條件 | 範本文字是否已完整替換、參考連結是否有效 |
| 若有 `agents/openai.yaml`，是否為有效 YAML mapping | 該檔所有產品專屬欄位是否正確 |
| 驗證工具對有效與錯誤輸入的行為 | 技能腳本、外部服務、Agent 載入或端到端流程 |

驗證工具只解析格式，不會執行技能內文或技能腳本。**格式通過與技能行為通過須分別確認。**

[GitHub Actions](https://github.com/yurychang/skills/actions/workflows/validate.yml) 會在推送至 `main`、提出 PR 或手動觸發時，安裝開發依賴並執行相同的格式檢查與工具測試。

## 貢獻方式

歡迎透過 [Issues](https://github.com/yurychang/skills/issues) 提出技能需求、使用回饋或問題，也可以透過 [Pull Requests](https://github.com/yurychang/skills/pulls) 提交變更。

提交前請確認：

- 技能用途明確、可獨立使用，相關依賴與資源都有說明。
- 已替換範本內容，README 技能清單與目前狀態同步更新。
- 格式驗證與驗證工具測試通過。
- PR 說明包含具體用途、代表性的使用請求、實際驗證結果與限制。
- 引用第三方內容時保留來源與原有授權資訊。

協作細節請見 [`AGENTS.md`](AGENTS.md)。

## 常見問題

**如何確認選到正式技能而不是範本？**

以[技能清單](#技能清單)為準，安裝時指定 `--skill optimize-ui`。`templates/skill-template/` 僅供建立新技能使用，不列為正式技能。

**只想閱讀技能，需要安裝 Python 或 Node.js 嗎？**

直接在 GitHub 閱讀即可。Python 用於本 repo 的開發驗證；Node.js 僅在選用 Skills CLI 時需要。執行個別技能的其他需求請閱讀它的 `SKILL.md`。

**格式檢查通過，是否代表每個 Agent 都能使用？**

仍需在目標 Agent 與實際工具環境驗證。格式驗證不檢查模型輸出品質、服務存取權限或產品專屬行為。

## 授權狀態

本 repo 目前尚未新增 `LICENSE`，也尚未指定專案授權條款。第三方來源的授權資訊應隨對應內容保留。

## 參考資料

本 README 的組織方式參考以下專案：將用途、可用技能、安裝與維護入口清楚呈現；技能內容由本 repo 獨立維護。

- [Anthropic Skills](https://github.com/anthropics/skills)：專案定位、技能集合與建立方式。
- [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills)：技能用途、適用情境與安裝入口。
- [Agent Skills 規格](https://agentskills.io/specification)：技能目錄、frontmatter 與資源組織方式。
- [Skills CLI](https://github.com/vercel-labs/skills)：安裝指令、支援的 Agent 與選項。

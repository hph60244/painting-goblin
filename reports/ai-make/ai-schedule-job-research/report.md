# Comparative Analysis: Code Agent 根據需求文件自動製作排程任務系統

## 結論摘要

本專案 painting-goblin 已是 AI Agent 自動產生排程任務的**先驅參考範例**，其設計模式在多個面向領先現有工具。以下為三大類參考範例的比較分析：

---

## 第一類：AI Agent 自動產生排程/工作定義的工具

| 工具 | 方式 | 排程定義位置 | 參數化支援 | AI Agent 整合 |
|------|------|-------------|-----------|--------------|
| **painting-goblin** ✅ | config.ini [job:] + scheduler.py | 獨立於 job 檔案 | ✅ 組合式參數化 (xxx=a,b) | OpenCode CLI |
| **Claude Code Routines** | `/schedule` CLI 指令 / 雲端管理 | Anthropic 雲端基礎設施 | ❌ 無參數化 | 原生 Claude Code |
| **GitHub Copilot Agent** | 從 Issue/PR 產生 `.github/workflows/*.yml` | YAML 內嵌 cron | ❌ 基本參數 | Copilot Agent |
| **Dagu** | `~/.config/dagu/dags/` YAML | YAML workflow 定義 | ✅ YAML 參數 | harness/agent steps |
| **Apache Airflow** | `dags_folder/` Python DAG | Python code | ✅ Python 參數 | 外部整合 |

### 關鍵發現
- **painting-goblin 的組合式參數化 (`xxx = a, b` → 4 variants) 是獨特優勢**，其他工具均無此功能
- **Claude Code Routines** 是唯一支援雲端管理排程（不需本機持續執行）的工具
- **Dagu** (3.3k stars) 是最接近的檔案系統優先排程系統，同為無資料庫、檔案即狀態

---

## 第二類：OpenCode Skills.sh 生態系中的規劃技能

| 技能 | 安裝數 | 用途 | 可借鏡於排程系統的部分 |
|------|--------|------|---------------------|
| `create-implementation-plan` (github/awesome-copilot) | 9.7K/週 | 產出結構化實作計畫 | 嚴格模板、前綴標籤系統、machine-parseable 輸出 |
| `writing-plans` (obra/superpowers) | 76.3K/週 | TDD 粒度任務分解 | 任務 2-5 分鐘、完整程式碼範例、無 placeholder 政策 |
| `executing-plans` (obra/superpowers) | 61.8K/週 | 順序執行計畫 | 阻斷偵測、驗證檢查點、subagent 驅動 |

### 關鍵發現
- **skills.sh 上不存在專門產生 cron/schedule 設定的技能** — 這是空白機會
- 現有技能的模板模式可直接套用：`SKILL.md` 定義結構化模板 → Agent 輸出 machine-parseable 排程設定 → 排程器執行
- `create-implementation-plan` 的 `REQ-`/`TASK-` 前綴系統可應用於排程任務的依賴管理

---

## 第三類：程式化排程系統與檔案系統佇列

| 系統 | Stars | 核心模式 | 排程方式 |
|------|-------|---------|---------|
| **Dagu** | 3.3k | YAML 檔案系統 workflow | cron + 重疊策略 |
| **Cronicle** | 5.6k | Node.js 多伺服器排程器 | cron + REST API |
| **K8s CronJob** | - | YAML 宣告式 | cron 表達式 |
| **robfig/cron** | 14.1k | Go 程式化排程 | 程式化建立 cron |
| **Airflow** | 45.3k | Python DAG 目錄自動發現 | cron/timedelta |
| **Prefect** | 22.3k | Python 裝飾器流程 | cron/interval/事件 |

### 關鍵發現
- **沒有專門的 markdown-to-cron 轉換工具** — 這是 greenfield 機會
- Airflow 的 `dags_folder` 自動發現模式是 painting-goblin 可參考的目錄掃描模式
- Dagu 的 `harness` step 直接支援 AI coding agent CLI (Claude Code, OpenCode, Copilot) 作為 workflow 步驟

---

## 給 painting-goblin 的建議

### 已驗證優勢（保持）
1. **Markdown-first 設計** — AI Agent 最擅長讀寫 `.md` 格式
2. **組合式參數化** — 其他工具均無此功能
3. **簡潔純 Python** — 無需 binary、無需資料庫

### 可改進方向
1. **Auto-discovery of jobs/**: 掃描目錄自動發現 job 檔案（類似 Airflow `dags_folder`），不需要手動在 config.ini 列舉
2. **Inline schedule in frontmatter**: 在 `.md` YAML frontmatter 中嵌入 `schedule:` 欄位，讓 Agent 寫 job 檔案時同時定義排程
3. **Event-based triggers**: 除 cron 外增加檔案變更/webhook 觸發
4. **建立 skills.sh 排程技能**: 建立一個 SKILL.md 讓 Code Agent 能根據需求文件自動產生排程設定
5. **Cloud-managed 排程**: 參考 Claude Code Routines，讓排程不依賴本機持續執行

---

## 參考來源

| 資源 | URL |
|------|-----|
| painting-goblin | 本專案 |
| Claude Code Routines | https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview |
| OpenCode Docs | https://opencode.ai/docs/ |
| Dagu | https://github.com/dagucloud/dagu |
| create-implementation-plan | https://skills.sh/github/awesome-copilot/create-implementation-plan |
| writing-plans | https://skills.sh/obra/superpowers/writing-plans |
| executing-plans | https://skills.sh/obra/superpowers/executing-plans |
| Apache Airflow | https://github.com/apache/airflow |
| GitHub Actions | https://github.com/features/actions |
| skills.sh | https://skills.sh |

# AI Agent / LLM 評測任務分類總表

## 總覽：14 大類任務

本文件整合 LLM 評測、AI Agent 評測、NLP 核心維度與領域特定評測，彙整為完整的分類總表。

---

## 一、知識與問答 (Knowledge & QA)

| 子類別 | 具體任務 | 評測基準 | 評分方式 |
|--------|---------|---------|---------|
| 廣泛知識問答 | 57學科多選題 | MMLU | Accuracy |
| 科學問答 | 小學科學多選題 | ARC (AI2 Reasoning Challenge) | Accuracy |
| 閱讀理解問答 | 閱讀文章後回答 | SQuAD 2.0, RACE, BoolQ, MultiRC | F1, Exact Match, Accuracy |
| 多跳推理問答 | 跨段落/跨文件推論 | HotpotQA, 2WikiMultihop, MuSiQue | F1, Exact Match |
| 對話問答 | 對話式情境理解 | CoQA, QuAC, DREAM | F1, HEAQ, Accuracy |
| 封閉式知識檢索 | 不提供外部知識 | Natural Questions, TriviaQA, WebQuestions | Exact Match, F1 |
| 長尾知識問答 | 罕見知識 recall | PopQA | Accuracy |

## 二、推理 (Reasoning)

| 子類別 | 具體任務 | 評測基準 | 評分方式 |
|--------|---------|---------|---------|
| 數學文字題 | 小學算術推理 (2-8步) | GSM8K, SVAMP, MultiArith | Exact Match, Accuracy |
| 競賽數學 | 高中/大學數學競賽 | MATH (競賽級), AIME, AMC | Accuracy |
| 邏輯推理 | 演繹、歸納、類比推理 | BIG-Bench (59項邏輯任務), BBH | Accuracy |
| 離散推理 | 段落內數值推理 | DROP | F1, Exact Match |
| 策略推理 | 是/否多跳推理 | StrategyQA | Accuracy |
| 代數推理 | SAT級代數應用題 | AQuA | Accuracy |
| 形式證明 | 數學定理形式化證明 | ProofNet, MiniF2F | Proof Completion Rate |

## 三、常識推理 (Commonsense Reasoning)

| 子類別 | 具體任務 | 評測基準 | 評分方式 |
|--------|---------|---------|---------|
| 情境完成 | 選擇最合理的結尾 | HellaSwag | Accuracy |
| 代詞指代消解 | 判斷代詞所指對象 | WinoGrande, Winogender, WinoBias | Accuracy |
| 物理常識 | 物理世界互動推理 | BIG-bench (物理推理), PIQA | Accuracy |
| 因果推理 | 因果關係判斷 | BIG-bench (因果推理 17項) | Accuracy |
| 社會推理 | 社會互動理解 | BIG-bench (社會推理 19項) | Accuracy |
| 心理理論 | 理解他人信念意圖 | BIG-bench (Theory of Mind 10項) | Accuracy |
| 情感理解 | 情緒辨識與理解 | BIG-bench (情感理解 16項) | Accuracy |

## 四、生成 (Generation)

| 子類別 | 具體任務 | 評測基準 | 評分方式 |
|--------|---------|---------|---------|
| 摘要生成 | 新聞/對話摘要 | CNN/DailyMail, XSum, SamSum | ROUGE-1/2/L |
| 機器翻譯 | 跨語言翻譯 | WMT, FLORES-200 | BLEU, chrF++, COMET |
| 創意寫作 | 故事/文案生成 | BIG-bench (創意 15項) | Human Eval, GPT Judge |
| 對話生成 | 多輪對話品質 | MT-Bench, Chatbot Arena | GPT-4 Score (1-10), Elo |
| 句子壓縮 | 生成標題/摘要 | GigaWord | ROUGE |
| 跨語言摘要 | 多語言摘要 | WikiLingua | ROUGE, BLEU |
| 釋義/改寫 | 句子改寫表達 | BIG-bench (paraphrase), PAWS | Accuracy, BLEU |

## 五、程式碼 (Coding)

| 子類別 | 具體任務 | 評測基準 | 評分方式 |
|--------|---------|---------|---------|
| 函數生成 | 從 docstring 生成 Python 函數 | HumanEval, MBPP | pass@k (功能正確性) |
| 競賽程式設計 | 競賽級演算法題 | APPS (10,000題), CodeContests | pass@k, Test Case Accuracy |
| 程式修復 | GitHub Issue 修補 | SWE-bench (2,294實例), SWE-bench Lite | % Resolved (測試通過率) |
| 跨語言程式修復 | 多語言版本 | SWE-bench Multilingual | % Resolved |
| 資料科學編碼 | 函式庫特定編碼 (pandas, numpy) | DS-1000 | pass@k |
| 程式執行推理 | 預測程式輸出結果 | CRUXEval | Output Prediction Accuracy |
| 程式碼審查 | 自動化 Code Review 品質 | CodeReviewEval | Precision, Recall |
| 程式修復 | Bug 定位與修正 | DeepFix, DrRepair | Fix Rate |
| 多語言程式修復 | 視覺領域程式碼 (HTML/CSS/GUI) | SWE-bench Multimodal | % Resolved |

## 六、工具使用與 API 調用 (Tool Use & API Calling)

| 子類別 | 具體任務 | 評測基準 | 評分方式 |
|--------|---------|---------|---------|
| 單一工具調用 | 單次 API 完成指令 | ToolBench (G1), API-Bank (Level 2) | Pass Rate, Success Rate |
| 跨類別多工具 | 同領域多 API 協作 | ToolBench (G2) | Pass Rate + Win Rate |
| 跨領域多工具 | 跨類別 API 規劃執行 | ToolBench (G3), API-Bank (Level 3) | End-to-End Success |
| API 檢索 | 從大量 API 中選出正確 API | API-Bank (Level 1) | Retrieval Accuracy |
| 工具規劃+調用 | 複雜指令規劃 API 序列 | API-Bank (Level 3) | Plan Success Rate |

## 七、網頁互動 (Web Interaction)

| 子類別 | 具體任務 | 評測基準 | 評分方式 |
|--------|---------|---------|---------|
| 網頁購物 | 商品搜尋、比價、購買 | WebArena (Shopping), WebShop | 執行通過率 |
| 社群論壇操作 | Reddit 風格發文/回覆 | WebArena (Social Forum) | 執行通過率 |
| 軟體開發平台 | GitLab Issue/PR 操作 | WebArena (Software Dev) | 執行通過率 |
| 內容管理 | WordPress 後台操作 | WebArena (Content Management) | 執行通過率 |
| 地圖導航 | OpenStreetMap 查詢操作 | WebArena (Map/Navigation) | 執行通過率 |
| 視覺網頁理解 | 截圖/圖片理解任務 | VisualWebArena (241項) | 執行通過率 |
| 商務工作流 | 真實商業流程模擬 | TheAgentCompany | 執行通過率 |
| 點擊操作 | 按鈕/連結/選單/對話框 | MiniWoB++ (Clicking tasks) | Cumulative Reward |
| 表單填寫 | 文字/日期/密碼輸入 | MiniWoB++ (Form Filling) | Cumulative Reward |
| 選擇操作 | 日期/列表選擇 | MiniWoB++ (Selection) | Cumulative Reward |
| 拖放操作 | 拖曳方塊/圓形/項目 | MiniWoB++ (Drag & Drop) | Cumulative Reward |
| 文字操作 | 複製貼上/高亮/編輯 | MiniWoB++ (Text Manipulation) | Cumulative Reward |

## 八、作業系統與電腦操作 (OS & Computer Use)

| 子類別 | 具體任務 | 評測基準 | 評分方式 |
|--------|---------|---------|---------|
| Linux 命令列 | 安裝套件、管理檔案、設定服務 | AgentBench (OS) | Success Rate |
| 桌面應用操作 | LibreOffice, VS Code, GIMP, VLC | OSWorld (Desktop Applications) | 執行通過率 |
| 跨應用工作流 | 下載→處理→郵件發送 | OSWorld (Cross-App Workflows) | 執行通過率 |
| 多應用序列 | 複雜跨應用任務鏈 | OSWorld (Multi-App Sequences) | 執行通過率 |
| 檔案 I/O | 檔案管理、權限操作 | OSWorld (OS File I/O) | 執行通過率 |
| 圖形化介面操作 | 滑鼠/鍵盤動作 (螢幕截圖+Accessibility Tree) | OSWorld (Full VM) | 執行通過率 (Human: 72%, AI: 12%) |

## 九、資料庫與知識圖譜 (Database & Knowledge Graph)

| 子類別 | 具體任務 | 評測基準 | 評分方式 |
|--------|---------|---------|---------|
| SQL 查詢 | 撰寫 SQL 操作 MySQL 資料庫 | AgentBench (DB) | Success Rate |
| SPARQL 查詢 | 查詢 Freebase 多跳推理 | AgentBench (KG) | Success Rate |

## 十、安全性與對齊 (Safety & Alignment)

| 子類別 | 具體任務 | 評測基準 | 評分方式 |
|--------|---------|---------|---------|
| 真實性/幻覺 | 避免散布錯誤觀念 | TruthfulQA | Truthfulness %, Informativeness |
| 社會偏見 | 年齡/性別/種族/宗教等9維度 | BBQ, StereoSet, CrowS-Pairs | Bias Score, Differential |
| 性別偏見 | 代詞共指偏見 | Winogender, WinoBias | Bias Rate |
| 毒性檢測 | 生成內容毒性評估 | RealToxicityPrompts, BOLD | Toxicity Probability |
| 有害內容拒絕 | 拒絕回答不安全輸入 | Safety-Prompts, Beaver | Refusal Rate |
| 紅隊攻擊 | 對抗性攻擊成功率 | GARCON, Red-Teaming | Attack Success Rate, Harmfulness |
| 有用性/無害性偏好 | 偏好數據對齊 | Anthropic HH-RLHF | Preference Accuracy |
| 偏見/毒性/公平性 | 全面評估 | BIG-bench (pro-social: bias, toxicity, alignment) | Multiple Metrics, HELM |

## 十一、指令遵循 (Instruction Following)

| 子類別 | 具體任務 | 評測基準 | 評分方式 |
|--------|---------|---------|---------|
| 多輪對話品質 | 8輪對話 GPT-4 評分 | MT-Bench | GPT-4 Judge (1-10) |
| 對比評測 | 與 GPT-4 基準比較勝率 | AlpacaEval | Win Rate, LC Win Rate |
| 可驗證指令遵循 | 格式/長度/關鍵詞約束 | IFEval | Strict/Loose Accuracy |
| 多層級約束 | 逐步滿足複合約束 | FollowBench | Step-wise Accuracy |
| 多樣化 NLP 指令 | 1600+ 多樣指令執行 | Natural Instructions | ROUGE-L, Exact Match |
| 通用指令遵循 | 6領域多輪對話 | AgentInstruct (1.8M+ 範例) | Downstream Metrics |

## 十二、長上下文處理 (Long Context)

| 子類別 | 具體任務 | 評測基準 | 評分方式 |
|--------|---------|---------|---------|
| 長文問答 | 5k-15k tokens 長文理解 | LongBench (6類別, 21數據集) | F1, ROUGE, Accuracy |
| 超長文理解 | 100k+ tokens 極長文本 | L-Eval (20任務) | Accuracy, F1 |
| 長文摘要/QA | 長文件處理 | SCROLLS | Exact Match, ROUGE |
| 大海撈針 | 長文中精確事實檢索 | Needle In A Haystack (NIAH), CLRT | Retrieval Accuracy |
| 超長上下文推理 | 超過訓練長度的推理 | RULER | Task-specific Accuracy |

## 十三、領域特定評測 (Domain-Specific)

| 領域 | 子類別 | 具體任務 | 評測基準 | 評分方式 |
|------|--------|---------|---------|---------|
| **醫療** | 醫學考試 | USMLE 執照考試 | MedQA (USMLE), MedMCQA | Accuracy |
| 醫療 | 生物醫學 QA | 生物醫學文獻問答 | PubMedQA, BioASQ | Accuracy, F1 |
| 醫療 | 臨床 NER | 臨床命名實體識別 | ClinicalBERT/BioBERT Eval | F1, Precision, Recall |
| 醫療 | 藥物交互 | 藥物-藥物交互預測 | DDInter | F1, AUROC |
| 醫療 | 診斷生成 | 鑑別診斷生成 | DiagnosisBench | Recall@k |
| 醫療 | 放射報告 | 放射報告理解 | MedUnderstanding | ROUGE, BLEU |
| **法律** | 法律推理 | 判決結果預測 | ECHR (歐洲人權法院) | Accuracy |
| 法律 | 合約分析 | 合約條款 QA/風險識別 | CUAD | F1, AUPR |
| 法律 | 法律 NLU | 6項法律 NLU 任務 | LexGLUE | Accuracy, F1 |
| 法律 | 法律文書檢索 | 法律文件檢索與蘊涵 | COLIEE | R Precision, F1 |
| 法律 | 判例推翻檢測 | 判例法推翻識別 | Overruling | F1, Accuracy |
| 法律 | 法規問答 | 法規/條例 QA | NLLP | Accuracy, F1 |
| **金融** | 財務 QA | 財報問答 + 數值推理 | FinQA, ConvFinQA | Exact Match, Program Acc |
| 金融 | 表格+文本 QA | 表格與文本混合問答 | TAT-QA | Exact Match, F1 |
| 金融 | 情感分析 | 財經新聞情緒分類 | FiQA SA | Accuracy, F1 |
| 金融 | 金融 NER | 金融命名實體識別 | NER-Finance | F1 |
| 金融 | SEC 申報分析 | 證監會申報文件摘要 | EDGAR Corpus | ROUGE, Factual Consistency |
| 金融 | 金融推理 | 預測邏輯推理 | AlphaFactor | Directional Accuracy |

## 十四、多語言與多模態 (Multilingual & Multimodal)

### 多語言 (Multilingual)

| 子類別 | 具體任務 | 評測基準 | 評分方式 |
|--------|---------|---------|---------|
| 跨語言 NLU | 9項任務 × 40種語言 | XTREME, XTREME-R | Accuracy, F1 |
| 機器翻譯品質 | 200+ 語言對翻譯 | WMT, FLORES-200 | BLEU, chrF++, COMET |
| 跨語言閱讀理解 | 122種語言理解 | Belebele | Accuracy |
| 多語言 NLU | 51種語言理解 | MASSIVE | Accuracy, F1 |
| 多語言問答 | 11種語言問答 | TyDiQA, MLQA | F1, Exact Match |
| 跨語言 NER | 跨語言命名實體識別 | WikiAnn | F1 |

### 多模態 (Multimodal)

| 子類別 | 具體任務 | 評測基準 | 評分方式 |
|--------|---------|---------|---------|
| 影像描述 | 生成影像文字描述 | COCO Captions, Flickr30k, NoCaps | CIDEr, BLEU, ROUGE, SPICE |
| 視覺問答 | 圖片內容問答 | VQA v2, GQA, OK-VQA, VizWiz | Accuracy |
| 文件理解 | 掃描文件/PDF 問答 | DocVQA | ANLS |
| 圖中文字識別 | 圖片內文字問答 | TextVQA | Accuracy |
| 多模態指令遵循 | 多模態多輪對話 | LLaVA-Bench, MMBench | GPT-4 Judge, Accuracy |
| 多學科多模態 | 大學級跨學科多模態問題 | MMMU | Accuracy |
| 視覺數學推理 | 圖表/幾何數學推理 | MathVista, ChartQA | Accuracy |

---

## 附錄：評測方法論綜合比較

| 評測方法 | 說明 | 代表案例 | 優點 | 缺點 |
|---------|------|---------|------|------|
| **準確率 (Accuracy)** | 標準答案匹配 | MMLU, GSM8K, ARC | 簡單直觀、可重現 | 對生成任務不適用 |
| **F1 / Exact Match** | 部分匹配與精確匹配 | SQuAD, HotpotQA | 平衡精確率與召回率 | 對創意生成不適用 |
| **pass@k** | k次嘗試內通過測試 | HumanEval, MBPP, APPS | 功能正確性檢驗 | 需執行環境 (Docker) |
| **ROUGE / BLEU** | n-gram 重疊度量 | 摘要、翻譯任務 | 自動化評估 | 不捕捉語義品質 |
| **GPT Judge** | LLM 作為評審員 | MT-Bench, AlpacaEval | 近似人類判斷 | 評審模型本身有偏見 |
| **Elo Rating** | 群眾兩兩偏好投票 | Chatbot Arena | 去中心化、無偏 | 需大量人工投票 |
| **執行通過率** | 真實環境執行檢驗 | SWE-bench, WebArena, OSWorld | 真實可靠、無幻覺 | 成本高、環境複雜 |
| **Bias Score** | 偏見程度量化 | BBQ, StereoSet | 可量化安全維度 | 覆蓋範圍有限 |

---

## 總表：任務類型彙整

| 大類 | 編號 | 任務類別 | 細項任務數量 | 代表評測數 |
|------|------|---------|------------|-----------|
| 知識型任務 | 1 | 知識與問答 | 7 | 15+ |
| 推理型任務 | 2 | 推理 (數學/邏輯) | 7 | 15+ |
| 推理型任務 | 3 | 常識推理 | 7 | 12+ |
| 生成型任務 | 4 | 生成 | 7 | 10+ |
| 程式碼任務 | 5 | 程式碼 | 9 | 12+ |
| 工具型任務 | 6 | 工具使用與 API 調用 | 5 | 4 |
| 互動型任務 | 7 | 網頁互動 | 10 | 8+ |
| 互動型任務 | 8 | 作業系統與電腦操作 | 6 | 3 |
| 知識型任務 | 9 | 資料庫與知識圖譜 | 2 | 2 |
| 安全型任務 | 10 | 安全性與對齊 | 8 | 15+ |
| 理解型任務 | 11 | 指令遵循 | 6 | 8+ |
| 理解型任務 | 12 | 長上下文處理 | 5 | 6+ |
| 領域型任務 | 13 | 領域特定評測 (醫療/法律/金融) | 18 | 25+ |
| 多模態任務 | 14 | 多語言與多模態 | 11 | 18+ |

**總計：14 大類，108+ 細項任務類別，150+ 個以上代表評測基準**

---

*報告生成日期：2026-04-28*
*資料來源：MMLU, HumanEval, GSM8K, HellaSwag, ARC, TruthfulQA, BIG-bench, BBQ, WinoGrande, GLUE/SuperGLUE, HELM, SWE-bench, AgentBench, WebArena, GAIA, ToolBench, API-Bank, ALFWorld, MiniWoB++, OSWorld, AgentInstruct, SQuAD, RACE, MT-Bench, AlpacaEval, IFEval, LongBench, NIAH, MedQA, FinQA, XTREME, MMMU, Chatbot Arena 等*

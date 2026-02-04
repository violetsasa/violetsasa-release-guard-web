# Release Manager Encyclopedia (版本管理百科)

這份文件旨在統整 iOS、Android、Steam、PC 等平台的發布管理知識，包含平台政策、送審注意事項、支付金流以及裝置優化經驗。

## 一、平台政策與送審 (Platform Policies & Submission)

### 1. iOS (App Store)
*   **Xcode & SDK 版本要求 (Upcoming Requirements)**
    *   **Xcode 16 / iOS 18**: 自 **2025年4月24日** 起，所有提交至 App Store 的 App 更新必須使用 Xcode 16 或更高版本建置，並支援 iOS 18 SDK。
    *   **Privacy Manifest (隱私清單)**: 
        *   自 **2025年2月** 起全面強制執行。App 或第三方 SDK (如 Firebase, AppsFlyer) 必須包含 `PrivacyInfo.xcprivacy` 檔案，明確宣告使用的 API (Required Reasons API) 與數據收集用途，否則將無法上傳或被退審。
*   **Game Center Entitlement**
    *   曾發生因缺少 Game Center Entitlement 設定而被警告或退審的情況，需確保 Provisioning Profile 中包含此權限。
*   **16 KB Page Size (iOS)**
    *   雖然主要討論集中在 Android，但 iOS 自 iOS 18 起也對記憶體管理有嚴格要求，需持續關注 Apple 對於 binary alignment 的規範。

### 2. Android (Google Play)
*   **16 KB Page Size 記憶體分頁規定**
    *   **生效日期**: **2025年11月1日** (Android 15+ 強制要求)。
    *   **內容**: 提交的新應用程式與更新版本，若支援 Android 15，必須支援 **16 KB page size** (原為 4 KB)。
    *   **檢查方式**:
        *   Mac: `check_elf_alignment` 工具。
        *   Windows: 使用 Mars 團隊提供的 `CheckAndroid16KB` 工具。
        *   實機測試: 使用 Pixel 8/9 系列，解鎖 Bootloader 後開啟 "16 KB 模式" 驗證 App 是否閃退。
    *   **解決方案**: 升級 NDK，移除不支援的舊版 .so 檔，或升級 Unity Play Asset Delivery (PAD) 版本 (推薦 1.9.5+)。
*   **API Level (Target SDK)**
    *   **Android 15 (API 35)**: 自 **2025年8月31日** 起，新應用與更新都必須支援 Target API 35。
    *   Google 每年會強制要求提升 Target SDK Version (通常在 8/31 ~ 11/1)。
    *   **歷史案例**: 升級至 API Level 31 時，曾導致 Google 模擬器黑屏，原因是 `android.permission.WAKE_LOCK` 權限錯誤或 AndroidNativeProxy 設定衝突。
*   **App Bundle (AAB)**
    *   Google Play 目前強制要求使用 AAB (Android App Bundle) 上傳，不再接受單一 APK。
    *   **注意事項**: AAB 上傳後由 Google 重新簽署派發 APK，需注意簽名金鑰 (Keystore) 的管理。
*   **權限設定**
    *   `AndroidNativeProxy`: 曾因 `exported=true` 被 Google 退審 (安全性漏洞)，但設為 `false` 又導致模擬器無法開啟。需依照當時的 Android 版本規範調整。
*   **個人帳號封測規定 (Closed Testing)**
    *   **針對對象**: 2023年11月13日後註冊的「個人開發者帳號」。
    *   **規則**: 正式發布前，必須先進行封閉測試，且需有至少 **12位測試人員** (原為20人) **連續測試 14 天**。
    *   **影響**: 新專案若使用全新個人帳號，務必預留這 2 週以上的測試緩衝期，否則無法申請正式上架 (Production Access)。

### 3. Steam (PC)
*   **審核時程緩衝 (Review Buffer)**
    *   **建議時間**: 雖然官方宣稱審核需 3-5 個工作天，但強烈建議至少預留 **7 個工作天**。
    *   **注意**: 「Store Page」與「Game Build」是分開審核的，兩者都必須 Pass 才能發布。
*   **版本更新與換包**
    *   **大包機制**: Steam 不同於手遊的熱更新 (Hotfix) 彈性，若有涉及執行檔 (exe) 或底層 SDK (如社群登入、視窗化功能) 的修改，必須更換「大包」(Build)。
    *   **社群登入 (Social Login)**: 需確保 Steam Overlay 功能正常開啟，否則瀏覽器驗證流程可能會被阻擋。
    *   **瀏覽器相容性**: Chrome 新政策限制網頁存取 Local Network，可能導致 Steam 版使用 Google 帳號登入時驗證失敗 (沒反應)。
        *   *解法*: 引導玩家在 Chrome 跳出「允許區域網路存取權」視窗時點選允許。
*   **交易限制**
    *   Steam 購買後，物品可能會被鎖定交易 **74小時** (或是依照帳號狀態)，這是 Steam 平台的防詐騙機制，無法透過廠商端解除。

### 4. PC 版 (Google Play Games on PC / 官方 PC 版)
*   **模擬器相容性**
    *   **黑屏/閃退**: 常見於升級 Unity 版本或 Android API Level 後。需特別注意 `x86` 架構的支援度 (雖然現在多用 ARM translation)。
    *   **權限錯誤**: 模擬器環境可能不支援部分手機特有的權限 (如特定 Wifi 狀態讀取)，導致 Crash。

---

## 二、登入、支付與儲值 (Login, Payment & Top-up)

### 1. 支付金流 (Payment)
*   **通路區分 (MyCard vs Google/Apple)**
    *   **MyCard (APK 版)**: 通常由官網下載的 APK 使用，利潤較高，且避開了 Google Play 的政策限制 (如抽成、審核)。
    *   **Google Play / App Store (IAP)**: 官方商店版，需符合平台規範 (如不可在 App 內引導至外部儲值)。
*   **Steam 支付**
    *   **Steam Wallet**: 必須介接 Steam Wallet，且需注意退款政策。
    *   **退款機制**: 玩家遊玩時間 **2小時內** 可無條件申請退款。營運端需注意此機制可能導致的「刷退」或「白嫖」風險 (例如買了虛寶用掉後退款)。
*   **儲值異常排查**
    *   Steam 版曾發生「已扣款但未入帳」，需檢查是否因 Steam Overlay 未開啟導致 callback 沒收到。

### 2. 資料與登入 (Login & Data)
*   **社群登入問題**:
    *   使用 Facebook/Google 登入時，若遇到瀏覽器安全性更新 (如 Chrome 區域網路限制)，可能會導致 callback 失敗。
*   **帳號綁定**:
    *   Steam 版與手機版帳號互通，通常透過綁定社群帳號 (Google/FB) 或官方會員帳號來實現。

---

## 三、裝置優化與卡頓排查 (Device Optimization & Lag)

### 1. 卡頓 (Lag/FPS Drop) 排查經驗
*   **MyCard APK vs Google Play Build**
    *   **現象**: 曾發生 Google Play 下載的版本比 MyCard 官網 APK 版本明顯卡頓 (FPS 30 vs FPS 15)。
    *   **原因分析**:
        *   **加固 (Hardening)**: 商店版通常會為了安全性進行加固 (Obfuscation/Encryption)，可能影響效能。
        *   **App Bundle (AAB)**: AAB 轉 APK 的過程可能引入了額外的 overhead (較少見，但曾被懷疑)。
        *   **PGS (Play Games Services)**: 登入 Google Play 服務可能在背景執行導致部分資源佔用。
    *   **測試結論**: 在特定模擬器 (雷電 64位元) 上差異最明顯。MyCard 無加固版本最順暢。
*   **壓力測試指令**:
    *   `clua3 ptbot 40 1 0`: 在角色身邊生成 40 個玩家模型，用於測試多人同屏的效能壓力。

### 2. iOS 特定優化
*   **Unity AUP (Async Upload Pipeline)**
    *   **問題**: iPhone (特別是 14/15/16) 發生載入卡頓。
    *   **優化方案**: 調整 Unity AUP 參數。
        *   **緩衝區 (Buffer)**: 擴大至 128MB。
        *   **Time Slice**: 延長至 8ms (以換取載入速度)。
        *   **Persistent**: 設定為 `false` (載入後釋放記憶體，避免 iPhone 記憶體壓力過大)。
    *   **設定檔**: `SGCInitSettings.xml` 可動態開關此設定 (`asyncUploadAutoConfig`)。

### 3. 模擬器 (Emulator) 優化
*   **卡頓與閃退**:
    *   **雷電模擬器 (LDPlayer)**: 曾發生 64位元版本閃退，需更新模擬器版本或調整 App 架構 (32-bit vs 64-bit)。
    *   **VT (Virtualization Technology)**: 提醒玩家開啟 BIOS 的 VT 功能，對模擬器效能影響巨大。
*   **CPU 核心數**: 測試發現將模擬器 CPU 設定為 1 核心可能導致嚴重掉幀，建議至少設定 2 核心以上。

---

## 四、各國伺服器發布地圖 (Regional Release Strategy)

針對不同市場的 SDK 環境與平台限制，發布時需遵循以下特殊規範：

### 1. 越南版 (Vietnam - ESG SDK)
* **iOS 安裝限制**: 越南 iOS 版本因不明原因（與當地網路或簽證有關）無法直接安裝在 iOS 15 以上的實體裝置。
* **送審 SOP**: 為了確保相容性，iOS 統一 **必須先送 TestFlight 測試**，確認可下載安裝後才可轉為正式發布。
* **支付規範**: 支援 Storekit v2，但最低系統要求需設為 iOS 15。

### 2. 日版 (Japan - Mars SDK)
* **商店合規檢查**: 送審版本必須進入「儲值頁面」，確認已 **隱藏【平台切換】按鈕**。這是為了避免被 Apple/Google 判定為引導至第三方儲值而遭退審。
* **包檔順序**: 務必先包 Android Console 再包 Final；包第三方包前需通知程式（長偉）提取安卓符號檔 (Symbols)。

### 3. 亞服 & 國服 (Asia/China - 鳳俠 SDK)
* **免審機制**: 
    * **亞服**: 雙平台皆無須經過商店送審（不適用 GP/App Store 規範），可自主控制放包時間。
    * **國服**: Android 需送各渠道審核（如 TapTap），但同樣無須適用 Google Play 框架規定。
* **效能優化**: 曾透過拿掉封包中的 `pcUID` 與關閉 `protocol checksum` 來節省封包大小。

---

## 五、大版本進版實戰 (Unity Upgrade SOP)

根據 Unity 2018 / 2020 / 2022 的進版經驗，整理標準作業流程：

### 1. 進版關鍵四部曲
1.  **末代備份**: 使用舊版 Unity 包完最後一個「末代 Bundle」，確保強更前的玩家仍有資源可用。
2.  **獨立環境**: 程式需在獨立的 **Branch** 進行升版，避免與日常 patch 產生嚴重的 SVN/Git 合併衝突。
3.  **主線重拉**: 進版完成後重拉主線，並人工蓋回支線的差異檔案。
4.  **SDK 聯動**: 隨 Unity 升版，務必同步更新 **Mars SDK** 至對應版本（例如配合 Unity 2022 需升至 4.5.0.4）。

### 2. 時程預警：包檔緩衝 (Build Buffer)
* **現象**: 歷史紀錄顯示，大版本更新（或 Unity 漏洞修正作業）時，包檔時間可能因緩存重算而大幅膨脹。
* **對策**: 在規劃重大更新時程時，必須在「包檔」與「測試」之間預留至少 **1-2 天的「包檔緩衝時間」**。

---

## 六、技術避坑與漏洞修正 (Bug Fixes & Security)

### 1. Android 15 & 16 KB 專區
* **強制要求**: 自 2025 年 11 月 1 日起，所有更新必須支援 16 KB 頁面大小。
* **配套清單**: 需升級 Unity 至 2022.3.62 以上、更新 Firebase SDK，並將 Play Asset Delivery 更新至 1.9.5。

### 2. 系統權限清理
* 為符合隱私政策，應主動檢查並移除不必要的敏感權限：
    * `READ_PHONE_STATE` (已移除)
    * `ACCESS_WIFI_STATE` (已移除)
    * `READ_MEDIA_IMAGES` / `VIDEO` (Android 13+ 需改用相片挑選器)

### 3. 平台專屬修正
* **iOS 遊戲模式**: 若發生 iOS 版本隨機卡死，嘗試在包檔設定中「預設關閉 iOS 遊戲模式 (Game Mode)」。
* **Steam 登入**: 升級 `Steamworks.NET` 後，需改用 `GetAuthTicketForWebApi` 取得 ticket 以完成 Billing 初始化。

---

## 七、團隊聯絡索引 (Internal Contacts)

若遇到特定模組問題，優先諮詢以下負責人員：
* **SDK 整合 / 登入 / 金流**: Mars
* **Unity 引擎 / 包檔工具 / PC版**: 長偉
* **Android 15 / Firebase / 16KB**: 貓排
* **各國送審進度 / 測試協調**: 亞臻

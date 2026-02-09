# Release Manager Encyclopedia (版本管理百科)


## :newspaper: 最新平台動態 (2026-02-09)
- [Apple] [Updated App Review Guidelines now available](https://developer.apple.com/news/?id=d75yllv4)
- [Apple] [Swift Student Challenge submissions are now open](https://developer.apple.com/news/?id=f0xw4t5r)
- [Apple] [Upcoming SDK minimum requirements](https://developer.apple.com/news/?id=ueeok6yw)

## :newspaper: 最新平台動態 (2026-02-08)
- [Apple] [Updated App Review Guidelines now available](https://developer.apple.com/news/?id=d75yllv4)
- [Apple] [Swift Student Challenge submissions are now open](https://developer.apple.com/news/?id=f0xw4t5r)
- [Apple] [Upcoming SDK minimum requirements](https://developer.apple.com/news/?id=ueeok6yw)

## :newspaper: 最新平台動態 (2026-02-07)
- [Apple] [Updated App Review Guidelines now available](https://developer.apple.com/news/?id=d75yllv4)
- [Apple] [Swift Student Challenge submissions are now open](https://developer.apple.com/news/?id=f0xw4t5r)
- [Apple] [Upcoming SDK minimum requirements](https://developer.apple.com/news/?id=ueeok6yw)

## :newspaper: 最新平台動態 (2026-02-06)
- [Apple] [Upcoming SDK minimum requirements](https://developer.apple.com/news/?id=ueeok6yw)
- [Apple] [Price updates for apps, In-App Purchases, and subscriptions](https://developer.apple.com/news/?id=gvnljl3f)
- [Apple] [Update on age requirements for apps distributed in Texas](https://developer.apple.com/news/?id=8jzbigf4)

## :newspaper: 最新平台動態 (2026-02-05)
- [Apple] [Upcoming SDK minimum requirements](https://developer.apple.com/news/?id=ueeok6yw)
- [Apple] [Price updates for apps, In-App Purchases, and subscriptions](https://developer.apple.com/news/?id=gvnljl3f)
- [Apple] [Update on age requirements for apps distributed in Texas](https://developer.apple.com/news/?id=8jzbigf4)
這份文件旨在統整 iOS、Android、Steam、PC 等平台的發布管理知識，包含平台政策、送審注意事項、支付金流以及裝置優化經驗。

## 重要時程與規範 (Deadlines)

| 平台 | 日期 | 事項 | 影響範圍 |
| :--- | :--- | :--- | :--- |
| **iOS** | **2025/02** | 強制 **Privacy Manifest** | 未包含 `PrivacyInfo.xcprivacy` 將被退審 |
| **iOS** | **2025/04/24** | 強制 **Xcode 16 / iOS 18 SDK** | 所有 App 更新必須符合 |
| **Android** | **2025/08/31** | 強制 **Target API 35** | 新應用與更新 |
| **Android** | **2025/11/01** | 強制 **16 KB Page Size** | Android 15+ 裝置支援 |

---

## 一、平台政策與送審 (Platform Policies & Submission)

### 1. iOS (App Store)
*   **Xcode & SDK 版本要求**
    *   **Xcode 16 / iOS 18**: 自 **2025年4月24日** 起，所有提交至 App Store 的 App 更新必須使用 Xcode 16 或更高版本建置，並支援 iOS 18 SDK。
    *   **Privacy Manifest (隱私清單)**: 
        *   自 **2025年2月** 起全面強制執行。App 或第三方 SDK (如 Firebase, AppsFlyer) 必須包含 `PrivacyInfo.xcprivacy` 檔案，明確宣告使用的 API (Required Reasons API) 與數據收集用途，否則將無法上傳或被退審。
*   **Game Center Entitlement**
    *   **注意**: 曾發生因缺少 Game Center Entitlement 設定而被警告或退審的情況，需確保 Provisioning Profile 中包含此權限。
*   **16 KB Page Size (iOS)**
    *   雖然主要討論集中在 Android，但 iOS 自 iOS 18 起也對記憶體管理有嚴格要求，需持續關注 Apple 對於 binary alignment 的規範。

### 2. Android (Google Play)
#### 16 KB Page Size 記憶體分頁規定
*   **生效日期**: **2025年11月1日** (Android 15+ 強制要求)。
*   **內容**: 提交的新應用程式與更新版本，若支援 Android 15，必須支援 **16 KB page size** (原為 4 KB)。
*   **檢查與處理建議**:
    *   **Mac**: 使用 `check_elf_alignment` 工具。
    *   **Windows**: 使用 Mars 團隊提供的 `CheckAndroid16KB` 工具。
    *   **實機測試**: 使用 Pixel 8/9 系列，解鎖 Bootloader 後開啟 "16 KB 模式" 驗證 App 是否閃退。
    *   **解決方案**: 升級 NDK，移除不支援的舊版 .so 檔，或升級 Unity Play Asset Delivery (PAD) 版本 (推薦 1.9.5+)。

#### API Level & 其他規範
*   **Target SDK**: Android 15 (API 35) 自 **2025年8月31日** 起強制生效。
*   **歷史案例**: 升級至 API Level 31 時，曾導致 Google 模擬器黑屏，原因是 `android.permission.WAKE_LOCK` 權限錯誤或 AndroidNativeProxy 設定衝突。
*   **App Bundle (AAB)**: 強制使用 AAB 上傳。需注意簽名金鑰 (Keystore) 的管理，因為 APK 是由 Google 重新簽署派發。
*   **權限設定**: `AndroidNativeProxy` 的 `exported` 屬性。設 `true` 可能因安全性被退審，設 `false` 可能導致模擬器無法開啟，需依當時規範調整。
*   **個人帳號封測規定**: 2023年11月後註冊的個人帳號，正式發布前需有 **12位測試人員** 連續測試 **14 天**。

### 3. Steam (PC)
*   **審核時程**: 雖然官方說 3-5 天，但強烈建議預留 **7 個工作天** (Store Page 與 Game Build 是分開審的)。
*   **版本更新**: 不同於手遊熱更新，若涉及執行檔或 SDK 修改，必須更換「大包」。
*   **社群登入**: 需確保 Steam Overlay 正常開啟，否則瀏覽器驗證流程可能會失敗。
*   **瀏覽器相容性**: Chrome 新政策限制 Local Network 存取，可能導致 Steam 版使用 Google 帳號登入沒反應。需引導玩家在瀏覽器視窗點選「允許」。
*   **交易限制**: 購買後物品鎖定交易 **74小時** (防詐騙機制)，無法由廠商端解除。

### 4. PC 版 / 模擬器
*   **模擬器黑屏/閃退**: 常見於 Unity 版本或 API Level 升級後，需注意 x86 支援度。
*   **權限錯誤**: 模擬器環境可能不支援部分手機特有權限 (如特定 Wifi 狀態讀取)，導致 Crash。

---

## 二、登入、支付與儲值 (Login, Payment & Top-up)

### 1. 支付金流比較

| 通路 | 特性 | 風險與注意 |
| :--- | :--- | :--- |
| **MyCard (APK)** | 利潤高、無平台抽成 | 需引導玩家去官網下載 APK |
| **Google/iOS (IAP)** | 官方商店版、方便 | 嚴禁 App 內引導至外部儲值 |
| **Steam Wallet** | 必須介接官方錢包 | **2小時無條件退款** (需防範刷退/白嫖) |

### 2. 常見問題排查
*   **Steam 扣款未入帳**: 檢查 **Steam Overlay** 是否開啟，這是 Callback 接收失敗的主因。
*   **社群登入失敗**: Facebook/Google 登入若遇到瀏覽器安全性更新 (如 Chrome 區域網路限制)，可能會導致 Callback 失敗。
*   **帳號綁定**: Steam 與手遊版互通通常需綁定社群帳號或官方會員帳號。

---

## 三、裝置優化與卡頓排查 (Optimization)

### 1. 效能優化撇步
*   **iOS 特定優化 (iPhone 卡頓)**:
    *   調整 Unity AUP (Async Upload Pipeline) 相關參數 (`SGCInitSettings.xml`)：
        *   Buffer: `128MB`
        *   Time Slice: `8ms`
        *   Persistent: `false` (載入後釋放記憶體)
*   **模擬器優化**:
    *   **卡頓/閃退**: 建議使用 64 位元版本模擬器，並開啟 BIOS 的 VT (虛擬化技術)。
    *   **CPU 核心**: 建議至少設定 **2 核心**，單核心可能導致嚴重掉幀。

### 2. 壓力測試指令
```bash
clua3 ptbot 40 1 0
# 在角色旁生成 40 個模型，測試同屏壓力
```

### 3. Build 版本差異
*   **MyCard APK vs Google Play Build**: 曾發現 Google Play 版比 MyCard 版卡頓 (FPS 30 vs 15)。可能原因包含商店版的加固 (Hardening)、AAB 轉換 Overhead 或 Play Services 背景執行影響。

---

## 四、各國伺服器發布地圖 (Regional Release Strategy)

### 越南版 (Vietnam)
*   **iOS 安裝**: 無法直接安裝在 iOS 15+ 實體機。
*   **送審 SOP**: iOS 必須先送 **TestFlight** 測試下載，確認可安裝後才轉正式。
*   **支付**: 支援 Storekit v2，但最低系統要求需設 iOS 15。

### 日版 (Japan)
*   **合規檢查**: 送審版本進入儲值頁面時，務必 **隱藏【平台切換】按鈕**，避免被 Apple/Google 判定為引導第三方儲值。
*   **包檔順序**: 先包 Android Console -> 再包 Final -> 通知程式提取 Symbols。

### 亞服 & 國服
*   **免審機制**: 亞服雙平台免審；國服 Android 需送各渠道審核 (如 TapTap)。
*   **效能優化**: 透過移除封包中的 `pcUID` 與關閉 `protocol checksum` 來節省流量。

---

## 五、大版本進版實戰 (Unity Upgrade SOP)

### 進版標準流程
1.  **末代備份**: 使用舊版 Unity 包完最後一個「末代 Bundle」，確保強更前的玩家仍有資源可用。
2.  **獨立 Branch**: 程式需在獨立的 Branch 進行升版，避免與日常 Patch 產生衝突。
3.  **主線重拉**: 進版完成後重拉主線，並人工蓋回支線的差異檔案。
4.  **SDK 聯動**: 隨 Unity 升版，務必同步更新 **Mars SDK** 至對應版本 (如 4.5.0.4)。

> **包檔緩衝 (Buffer Time)**
> 大版本更新時，包檔時間常因 Cache 重算而大幅膨脹。務必在時程上預留 **1-2 天** 的緩衝時間。

---

## 六、技術避坑與漏洞修正 (Bug Fixes)

### 1. 系統權限清理 (Privacy)
為符合隱私政策，應主動檢查並移除以下敏感權限：
*   `READ_PHONE_STATE` (已移除)
*   `ACCESS_WIFI_STATE` (已移除)
*   `READ_MEDIA_IMAGES` / `VIDEO` (Android 13+ 需改用相片挑選器)

### 2. 平台專屬修正
*   **iOS 遊戲模式**: 若發生版本隨機卡死，嘗試在包檔設定中「預設關閉 iOS 遊戲模式 (Game Mode)」。
*   **Steam Billing**: 升級 `Steamworks.NET` 後，需改用 `GetAuthTicketForWebApi` 取得 ticket。

---

## 七、團隊聯絡索引 (Internal Contacts)

若遇到特定模組問題，優先諮詢以下負責人員：

| 模組 | 負責人 |
| :--- | :--- |
| **SDK / 登入 / 金流** | Mars |
| **Unity / 包檔 / PC版** | 長偉 |
| **Android 15 / Firebase** | 貓排 |
| **送審進度 / 測試協調** | 亞臻 |

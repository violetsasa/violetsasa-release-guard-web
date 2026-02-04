# Release Manager Encyclopedia (版本管理百科)

> 這份文件旨在統整 iOS、Android、Steam、PC 等平台的發布管理知識，包含平台政策、送審注意事項、支付金流以及裝置優化經驗。

## :rotating_light: 緊急與重要時程 (Deadlines)

| 平台 | 日期 | 事項 | 影響範圍 |
| :--- | :--- | :--- | :--- |
| **iOS** | **2025/02** | 強制 **Privacy Manifest** | 未包含 `PrivacyInfo.xcprivacy` 將被退審 |
| **iOS** | **2025/04/24** | 強制 **Xcode 16 / iOS 18 SDK** | 所有 App 更新必須符合 |
| **Android** | **2025/08/31** | 強制 **Target API 35** | 新應用與更新 |
| **Android** | **2025/11/01** | 強制 **16 KB Page Size** | Android 15+ 裝置支援 |

---

## 一、平台政策與送審 (Platform Policies & Submission)

### 1. iOS (App Store)
*   :warning: **Game Center Entitlement**
    *   曾發生因缺少設定而被退審，務必檢查 Provisioning Profile。
*   :memo: **iOS 記憶體管理**
    *   關注 Apple 對於 binary alignment 的 16 KB page size 規範 (隨 iOS 18 變嚴格)。

### 2. Android (Google Play)
#### :hammer_and_wrench: 16 KB Page Size 檢查清單
- [ ] **Mac**: 使用 `check_elf_alignment` 檢查。
- [ ] **Windows**: 使用 Mars 團隊工具 `CheckAndroid16KB`。
- [ ] **實機驗證**: 在 Pixel 8/9 解鎖 Bootloader 開啟「16 KB 模式」測試是否閃退。
- [ ] **解決方案**: 升級 NDK 或 Unity Play Asset Delivery (PAD) 至 1.9.5+。

#### 其他注意事項
*   **App Bundle (AAB)**: 必須使用 AAB 上傳，需注意 Google 重簽後的 Keystore 管理。
*   **AndroidNativeProxy**: 權限 `exported` 需依 Android 版本調整 (設 `true` 安全性風險 vs 設 `false` 模擬器打不開)。
*   **新帳號封測**: 2023/11 後註冊的個人帳號，正式上架前需 **12人 x 14天** 封閉測試。

### 3. Steam (PC)
*   :hourglass_flowing_sand: **審核時程**: 建議預留 **7 個工作天** (Store Page 與 Build 分開審)。
*   **版本更新**: 涉及執行檔 (exe) 或底層 SDK 修改時，必須換「大包」。
*   **交易限制**: 購買後物品鎖定交易 **74小時** (防詐騙機制)。

### 4. PC 版 / 模擬器
| 問題 | 可能原因 | 解決方向 |
| :--- | :--- | :--- |
| **模擬器黑屏** | Android API 升級 / 權限錯誤 | 檢查 `WAKE_LOCK` 權限 / 模擬器是否支援該權限 |
| **效能卡頓** | CPU 核心數設定過低 | 建議模擬器至少設定 **2 核心** |

---

## 二、登入、支付與儲值 (Login, Payment & Top-up)

### 1. 支付金流比較

| 通路 | 特性 | 風險與注意 |
| :--- | :--- | :--- |
| **MyCard (APK)** | 利潤高、無平台抽成 | 需引導玩家去官網下載 APK |
| **Google/iOS (IAP)** | 官方管道、方便 | 嚴禁 App 內引導外部儲值 |
| **Steam Wallet** | 必須介接官方錢包 | **2小時無條件退款** (需防範刷退/白嫖) |

### 2. 常見問題排查
*   **Steam 扣款未入帳**: 檢查 **Steam Overlay** 是否開啟 (Callback 失敗主因)。
*   **社群登入沒反應**: Chrome 若限制 Local Network 存取，會導致 Callback 失敗 (需引導玩家點「允許」)。

---

## 三、裝置優化與卡頓排查 (Optimization)

### 1. :rocket: 效能優化撇步 (Tips)
*   **Unity AUP (iPhone 卡頓解法)**:
    *   調整 `SGCInitSettings.xml`：
        *   Buffer: `128MB`
        *   Time Slice: `8ms`
        *   Persistent: `false`
*   **模擬器優化**:
    *   更新至 64 位元版本 (避免舊版閃退)。
    *   提醒玩家開啟 BIOS 的 **VT (虛擬化技術)**。

### 2. 壓力測試指令
```bash
clua3 ptbot 40 1 0
# 在角色旁生成 40 個模型，測試同屏壓力
```

---

## 四、各國伺服器發布地圖 (Global Release)

### :vietnam: 越南版 (Vietnam)
- [ ] **iOS 安裝**: 無法直接安裝在 iOS 15+ 實體機。
- [ ] **送審 SOP**: iOS 必須先送 **TestFlight** 測試下載。
- [ ] **支付**: 支援 Storekit v2，最低系統要求需設 iOS 15。

### :jp: 日版 (Japan)
- [ ] **合規檢查**: 確認儲值頁面已 **隱藏【平台切換】按鈕**。
- [ ] **包檔順序**: 先包 Android Console -> 再包 Final -> 通知程式提取 Symbols。

### :cn: 亞服/國服
- [ ] **免審機制**: 亞服雙平台免審；國服 Android 需送渠道審核。
- [ ] **封包優化**: 移除 `pcUID` 與關閉 `protocol checksum`。

---

## 五、大版本進版實戰 (Unity Upgrade SOP)

### 進版標準流程
1.  **末代備份**: 先包最後一個舊版 Bundle，確保強更前玩家有資源用。
2.  **獨立 Branch**: 程式在獨立分支升版，避免影響主線。
3.  **SDK 聯動**: Unity 升級時，同步升級 **Mars SDK** (如 4.5.0.4)。
4.  **主線重拉**: 完成後合併回主線。

> [!IMPORTANT]
> **包檔緩衝 (Buffer Time)**
> 大版本更新時，包檔時間常因 Cache 重算而變長。務必預留 **1-2 天** 的緩衝時間。

---

## 六、技術避坑與漏洞修正 (Bug Fixes)

### 系統權限清理 (Privacy)
請檢查並移除以下敏感權限：
- [x] `READ_PHONE_STATE`
- [x] `ACCESS_WIFI_STATE`
- [x] `READ_MEDIA_IMAGES` / `VIDEO` (改用相片挑選器)

### 平台專屬修正
*   **iOS 遊戲模式**: 若隨機卡死，嘗試在包檔設定中「預設關閉 iOS Game Mode」。
*   **Steam Billing**: 升級 `Steamworks.NET` 後，改用 `GetAuthTicketForWebApi`。

---

## 七、團隊聯絡索引 (Contacts)

若遇到特定模組問題，請優先諮詢：

| 模組 | 負責人 |
| :--- | :--- |
| **SDK / 登入 / 金流** | Mars |
| **Unity / 包檔 / PC版** | 長偉 |
| **Android 15 / Firebase** | 貓排 |
| **送審進度 / 測試協調** | 亞臻 |

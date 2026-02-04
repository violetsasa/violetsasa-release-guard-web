# 如何更新 Release Guard 網站

## 1. 更新內容 (Wiki)
修改 `public/encyclopedia.md` 檔案，這是網站顯示的內容來源。

## 2. 上傳變更 (自動發布)
修改完成後，在終端機 (Terminal) 執行以下三個指令：

```powershell
# 1. 加入變更 (讓 Git 知道你改了什麼)
git add .

# 2. 提交說明 (讓未來的自己知道改了什麼)
# 範例：git commit -m "新增 iOS 送審注意事項"
git commit -m "這裡打你的修改說明"

# 3. 推送到 GitHub (這會觸發自動更新網站)
git push origin main
```

## 3. 等待發布
執行完 `push` 後，等待約 1-2 分鐘，網站就會自動更新。
狀態可以在 GitHub Repo 的 [Actions] 分頁查看。

## 常見問題
- **Error loading document**: 通常是路徑設錯，請檢查 `vite.config.js` 的 `base` 設定或 fetch 路徑。

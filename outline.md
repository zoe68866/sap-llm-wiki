# 簡報大綱：SAP 是什麼？

由 AI 讀 `wiki/index.md` 後查詢相關頁面產生。每張投影片寫明用到的 wiki 頁面，執行 `checks/check_outline.py` 通過後才產生 HTML。

## 01 SAP 是什麼？
- 頁面：sap-company.md、erp.md
- 內容：給修課同學的 SAP 入門：SAP 是一家德國企業軟體公司，它做的 ERP 系統是很多公司每天在用的工作系統

## 02 今天會學到
- 頁面：index.md
- 內容：ERP 是什麼；SAP 是誰、產品怎麼演進；模組與資料整合；怎麼操作 SAP；為什麼大家都在談 2027

## 03 先想一個問題
- 頁面：erp.md
- 內容：如果業務、倉庫、財務各用自己的 Excel，客戶下了一張訂單，會發生什麼事？資料要重複輸入、數字對不起來、要互相打電話確認

## 04 ERP 是什麼
- 頁面：erp.md
- 內容：ERP 是 enterprise resource planning（企業資源規劃），把採購、生產、銷售、財務、人資的資料集中在同一套系統，大家看到同一份資料

## 05 沒有 ERP 與有 ERP
- 頁面：erp.md
- 內容：左邊每個部門各自的資料庫，右邊一個中央資料庫；比喻：全班共用一份 Google 試算表

## 06 SAP 是誰
- 頁面：sap-company.md
- 內容：1972 年由五位前 IBM 員工在德國創立，總部在瓦爾多夫；名字來自德文「系統分析與程式開發」；員工超過 105,000 人

## 07 SAP 產品演進
- 頁面：sap-products.md
- 內容：時間軸：1979 R/2、1992 R/3（主從式架構）、2004 ECC、2011 HANA、2015 S/4HANA

## 08 SAP 的模組
- 頁面：sap-modules.md
- 內容：FI/CO 財務、SD 銷售、MM 物料、PP 生產、HCM 人資；全部共用一個中央資料庫

## 09 一張訂單在 SAP 裡怎麼流動
- 頁面：sap-modules.md、erp.md
- 內容：業務在 SD 建立訂單 → 倉庫在 MM 出貨 → 財務在 FI 產生應收帳款；資料只輸入一次

## 10 怎麼操作 SAP：SAP GUI
- 頁面：sap-gui.md
- 內容：登入要用戶端、帳號、密碼、語言；畫面可能是中文、英文或德文，同一個按鈕有三種名稱

## 11 交易碼 T-code
- 頁面：sap-gui.md
- 內容：在命令欄輸入交易碼進入功能，例如 SE11；最長 20 個字元；/n 取消目前交易、/oSE11 開新工作階段；沒存檔就用 /n 會遺失修改

## 12 開發者的角度：ABAP
- 頁面：abap.md
- 內容：ABAP 是 SAP 自己的程式語言；ABAP Dictionary（SE11）定義資料型態和資料表；建表順序：網域 → 資料元素 → 資料表

## 13 為什麼大家都在談 2027
- 頁面：ecc-2027.md、sap-products.md
- 內容：ECC 主流維護在 2027 年底結束，之後還能用，但沒有更新和安全修補，所以很多公司正在換成 S/4HANA；這個期限 SAP 已經延過兩次

## 14 重點回顧
- 頁面：erp.md、sap-company.md、sap-modules.md、sap-gui.md、ecc-2027.md
- 內容：ERP 讓資料集中；SAP 是做 ERP 的公司；模組共用資料；用 SAP GUI 和交易碼操作；ECC 維護在 2027 年底結束

## 15 小測驗
- 頁面：erp.md、sap-products.md、sap-gui.md
- 內容：三題選擇題：ERP 主要解決什麼問題、S/4HANA 建立在什麼資料庫上、/oSE11 的作用

## 16 資料來源
- 頁面：index.md
- 內容：列出 S01 到 S07 的標題與網址

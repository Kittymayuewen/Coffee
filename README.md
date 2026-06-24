# 上海咖啡花园 · 扁平插画地图版

当前视觉采用 Mid-Century Modern（世纪中期现代主义）配色与几何构图。交互层级与原 Three.js 原型一致：上海总览展示全部花束，点击行政区进入区级聚焦，再点击单株花进入门店详情。

页面包含双底图机制：通过 HTTP 访问时优先加载高德 3D 地图；直接以 `file://` 打开或高德加载失败时，自动使用本地 Mid-Century 插画地图，花束与三级交互仍然可用。

## 快速启动

1. 在本目录运行 `python3 -m http.server 8080`。
2. 浏览器访问 `http://localhost:8080/`。

项目已配置高德 Web Key 与安全密钥。若部署域名发生变化，请在高德控制台确认该域名已加入安全设置。

## 当前数据状态

- 已接入 54 家门店，覆盖 15 个行政区。
- 已匹配 51 张独立花朵 PNG；`Cafe del Volcan`、`BLUE TERRIA 瑰夏星球`、`PETITGEORGECAFE 小乔治` 暂用占位图。
- 原始工作簿没有地址或经纬度，当前标记按行政区近似分布，不能视为门店真实位置。
- 原始工作簿没有评分、评论数和人均价格，对应位置显示“暂无”。
- 用户提供的 `biaoge.csv` 实际文件格式为 Excel 工作簿；网站数据已经从工作簿正确解析并嵌入。

## 替换门店数据

1. 复制 `data/shops-template.csv`，按模板填写真实数据并保存为 UTF-8 CSV。
2. 执行：

   ```bash
   python3 tools/embed_csv.py data/shops.csv index.html
   ```

3. 将每家店对应的透明 PNG 放入 `assets/flowers/`，文件名与 CSV 的 `image` 字段一致。

坐标系支持 `GCJ02`、`WGS84`、`BD09`、`UNKNOWN`。未知坐标系不会被猜测或绘制，页面的数据质量面板会列出问题记录。

## 数据字段

`id,name,district,address,lng,lat,coord_system,type,rating,reviews,avg_price,tags,description,image,bean_flavor,social,space,service,location_accuracy`

- 必填：`id`、`name`、`district`、`address`、`lng`、`lat`。
- `type` 建议使用 `indep`、`chain` 或 `hot`。
- `tags` 用中文或英文逗号分隔。
- 缺少 `image` 或图片加载失败时自动使用 `placeholder.png`。

## 高德配置

高德开放平台需要 Web 端 Key；2021-12-02 后申请的 Key 还需安全密钥。部署时应将网站域名加入 Key 的安全设置。

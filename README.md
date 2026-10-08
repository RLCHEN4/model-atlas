# MODEL ATLAS · 公开分享版

免费、适合发给朋友和团队的静态 AI 模型选型网站。**纯 HTML/CSS/JavaScript，不需要数据库、API Key、Node.js 或付费套餐**。

## 当前内容（不会误导为实时跑分）

- 四档**原创任务选型建议**（旗舰深推理 / 高推理 / 中等推理 / 轻量快速）。
- 14 个工作场景，支持搜索与分类筛选、移动端布局、打印 / 保存 PDF、一键复制网址。
- 跳转 Artificial Analysis 与 OpenAI 官方资料的原站链接。
- **不包含**第三方智能指数、模型排名、单任务成本、第三方原始数据文件或其 CSV 导出。
- GitHub Actions **每次 push 自动发布**；每天北京时间大约 08:17 **检查来源链接能否访问**并显示上次检查时间。**注意：这是每日检查链接，不是每日刷新模型排名或测评分数。**

## 5 步上线（GitHub 免费账户）

1. 进入 <https://github.com/new>，新建 `model-atlas` 仓库；选择 **Public**，勾选不添加 README / `.gitignore` / License，然后点击 **Create repository**。
2. 将这个文件夹中的所有文件和隐藏 `.github` 文件夹上传至仓库根目录，**不要直接上传 zip 压缩包**；或者把仓库网址发给已连接 GitHub 的助手，请它逐个创建源码文件。
3. 在仓库 `Settings → Pages → Build and deployment` 里把 **Source** 设置为 `GitHub Actions`。
4. 进入 `Actions` 查看“发布 MODEL ATLAS 公开版”是否运行成功。如果未自动运行，可以在该工作流中选择 **Run workflow**。
5. 打开 `https://你的GitHub用户名.github.io/model-atlas/`，复制网址分享给朋友。首次发布可能稍有延迟。

## 内容更新与每日检查

- **手动修改内容：** `app.js` 的 `tasks` 数组中可以新增任务（需审阅内容）；提交到 `main` 后网站自动发布。
- **每天检查：** 定时访问来源主页以检测 HTTP 可达性，不解析、保存或转载网页中的任何模型数据。结果仅保存到 `data/source-status.json`。
- **免费计划注意：** GitHub 对 60 天无仓库活动的公开仓库可能自动停止定时工作流。进入 `Actions` 可恢复。
- **版权和许可：** 若将来要公开显示第三方完整模型排行榜、成本、分数或进行模型对比服务，应先与原始数据方核实并取得所需授权。本版避免发布此类数据。
- **网址公开性：** GitHub Pages 免费账号需公开仓库，网站任何人都可访问，不要存放团队敏感信息、密钥或个人数据。

## 在电脑预览

直接双击 `index.html` 即可查看完整正文和任务筛选；如果希望显示 JSON 里的最近链接检查记录，可在文件夹中启动 HTTP 服务器：

```bash
python -m http.server 8000
```

浏览器访问 `http://localhost:8000/`。

## 文件结构

```text
index.html                         网站页面
styles.css                         响应式视觉样式
app.js                             原创任务速查交互
favicon.svg                        站点图标
data/source-status.json            每日来源链接可访问性检查状态
scripts/check_sources.py           仅检测链接，不提取数据
.github/workflows/pages.yml        GitHub Pages 发布与每日来源链接检测
tests/test_check_sources.py        离线测试
.nojekyll                          告诉 Pages 不进行 Jekyll 转换
```

参考来源和条款：
- https://artificialanalysis.ai/models
- https://artificialanalysis.ai/data-api/docs
- https://artificialanalysiscdn.com/legal/ProDataPlatformTerms.pdf
- https://docs.github.com/en/pages
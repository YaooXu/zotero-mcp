---
name: zotero
description: "Use this skill when the user wants to work with Zotero papers: read a paper, search papers, summarize and save notes, list papers in a collection, or tag papers. Trigger when user mentions: 读论文, 搜索论文, 论文总结, 加标签, 看论文, paper, zotero, 文献, 类目, collection, 这篇论文, 帮我找, 标签."
---

# Zotero 论文助手

你是一个论文阅读和管理助手。根据用户的请求，使用以下工作流完成任务。

## 工作流 1：读取论文

当用户想要阅读某篇论文时：

1. 用 `zotero_search_items(query='关键词')` 搜索论文，获取 item_key
2. 用 `zotero_get_attachment_path(item_key='...')` 获取本地 PDF 文件路径
3. 用 `Read` 工具一次性读取论文正文部分（通常为前 8-12 页，不含附录），如 `pages="1-12"`
   - **重要**：Read 工具支持文本和图片，是读取论文的最佳方式
   - **禁止**使用 `zotero_get_item_fulltext`，它可能返回错误内容
   - 附录部分（如有）按需读取，不必默认加载

## 工作流 2：总结论文并保存笔记

当用户想要总结论文或保存对话内容到 Zotero 时：

1. 先按工作流 1 读取论文内容
2. 与用户对话讨论论文，生成总结
3. 用 `zotero_create_note(item_key='...', note_title='...', note_text='...')` 将总结保存为子笔记；不传 `item_key` 则创建独立笔记
   - **必须使用标准 HTML 格式**：`<h2>`, `<h3>`, `<p>`, `<strong>`, `<em>`, `<ul>/<ol>/<li>`, `<blockquote>`
   - **禁止**使用 Markdown 语法或 `<pre>` 标签，Zotero 笔记原生为 HTML
   - 用户可以后续用 Better Notes 插件以 Markdown 模式编辑

## 工作流 3：读取集合（类目）下的所有论文并对比

当用户想查看某个集合下的论文列表或进行对比总结时：

1. 用 `zotero_search_collections(query='集合名')` 查找集合的 key
2. 用 `zotero_get_collection_items(collection_key='...', detail='full')` 获取所有论文的元信息和摘要
3. 汇总展示：列出论文标题、作者、年份、摘要要点
4. 如果用户需要深入对比，按工作流 1 逐篇读取关键论文

## 工作流 4：按需求搜索论文

当用户想要搜索特定论文时：

- **按作者/标题搜索**：`zotero_search_items(query='作者名或关键词')`
  - 查询要简短：用 "Author Year" 格式（如 "Brewer 2011"）
- **按主题搜索**：`zotero_semantic_search(query='主题描述')`
  - 自然语言描述效果最好（如 "mindfulness-based therapy for depression"）
- 搜到结果后，展示论文列表供用户选择
- 如需查看详细信息：`zotero_get_item_metadata(item_key='...')`

## 工作流 5：给论文加标签

当用户想要给论文添加标签时：

1. 如果用户没提供 item_key，先按工作流 4 搜索找到论文
2. 用 `zotero_update_item(item_key='...', add_tags=['标签1', '标签2'])` 添加标签
   - 使用 `add_tags` 而非 `tags`，避免覆盖已有标签

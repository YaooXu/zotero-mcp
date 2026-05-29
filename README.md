# Zotero MCP Lite: 用 Claude Code 高效管理你的论文库

基于 [zotero-mcp-server](https://github.com/anthropics/zotero-mcp-server) 的精简版本，专为 Claude Code + Skill 工作流优化。

## 与原版的区别

| | 原版 zotero-mcp | 本 fork (Lite) |
|---|---|---|
| 工具数量 | 55 个（全部注入 system prompt） | **8 个**（Lite 模式） |
| 读取论文 | `get_item_fulltext`（可能返回错误内容） | `get_attachment_path` + `Read`（支持图片） |
| 创建笔记 | 仅子笔记 | 支持子笔记 + **独立笔记** |
| Skill 支持 | 无 | 内置 Zotero Skill，自动触发 |

### 核心改动

1. **Lite 模式**：通过 `ZOTERO_MCP_LITE=true` 只保留 8 个核心工具，减少 system prompt 占用
2. **工具描述优化**：引导 AI 使用 `get_attachment_path` + `Read` 读取论文（支持图片/图表）
3. **`create_note` 增强**：`item_key` 改为可选参数，不传则创建独立笔记
4. **内置 Skill**：提供 5 个预定义工作流（读论文、总结、搜索、浏览集合、加标签）

## 安装

### 1. 安装 zotero-mcp-server

```bash
# 使用 uv（推荐）
uv tool install zotero-mcp-server

# 或使用 pip
pip install zotero-mcp-server
```

### 2. 应用本 fork 的代码改动

找到已安装的包路径，将本仓库的源码覆盖过去：

```bash
# 找到安装路径
SITE_PACKAGES=$(python3 -c "import zotero_mcp; print(zotero_mcp.__file__)" | sed 's|/__init__.py||')

# 覆盖修改过的文件
cp src/zotero_mcp/tools/__init__.py "$SITE_PACKAGES/tools/__init__.py"
cp src/zotero_mcp/tools/annotations.py "$SITE_PACKAGES/tools/annotations.py"
cp src/zotero_mcp/tools/retrieval.py "$SITE_PACKAGES/tools/retrieval.py"
cp src/zotero_mcp/tools/read_pdf.py "$SITE_PACKAGES/tools/read_pdf.py"
```

### 3. 配置 MCP Server

编辑 Claude Desktop 配置文件：

- macOS: `~/Library/Application Support/Claude Desktop/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude Desktop\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "zotero": {
      "command": "zotero-mcp",
      "env": {
        "ZOTERO_LOCAL": "true",
        "ZOTERO_MCP_LITE": "true",
        "ZOTERO_API_KEY": "你的API Key",
        "ZOTERO_LIBRARY_ID": "你的Library ID",
        "ZOTERO_LIBRARY_TYPE": "user"
      }
    }
  }
}
```

**环境变量说明：**

| 变量 | 必需 | 说明 |
|------|------|------|
| `ZOTERO_LOCAL` | 是 | 设为 `true` 启用本地模式 |
| `ZOTERO_MCP_LITE` | 否 | 设为 `true` 启用 Lite 模式（55→8 工具） |
| `ZOTERO_API_KEY` | 推荐 | 用于创建子笔记，在 [zotero.org/settings/keys](https://www.zotero.org/settings/keys) 获取 |
| `ZOTERO_LIBRARY_ID` | 推荐 | 你的 Zotero 用户 ID（在 Zotero 网站 URL 中可见） |
| `ZOTERO_LIBRARY_TYPE` | 推荐 | `user` 或 `group` |

### 4. 安装 Skill（Claude Code 用户）

将 `skills/zotero/SKILL.md` 复制到 Claude Code 的 skills 目录：

```bash
mkdir -p ~/.claude/skills/zotero
cp skills/zotero/SKILL.md ~/.claude/skills/zotero/SKILL.md
```

安装后，当你提到"读论文"、"搜索论文"、"论文总结"等关键词时，Claude Code 会自动触发 Zotero Skill。

## Lite 模式保留的 8 个工具

| 工具 | 用途 |
|------|------|
| `zotero_search_items` | 按标题/作者搜索论文 |
| `zotero_semantic_search` | 按主题语义搜索 |
| `zotero_get_item_metadata` | 查看论文元信息 |
| `zotero_get_attachment_path` | 获取本地 PDF 路径 |
| `zotero_get_collection_items` | 列出集合下的论文 |
| `zotero_search_collections` | 搜索集合 |
| `zotero_create_note` | 创建笔记（子笔记或独立笔记） |
| `zotero_update_item` | 更新论文信息（如加标签） |

不需要 Lite 模式时，去掉 `ZOTERO_MCP_LITE` 环境变量即可恢复全部 55 个工具。

## Skill 工作流

### 1. 读取论文
搜索 → 获取 PDF 路径 → Read 工具读取（支持文本+图片）

### 2. 总结并保存笔记
读取论文 → 对话讨论 → 以 HTML 格式保存到 Zotero 笔记

### 3. 浏览集合
搜索集合 → 列出所有论文 → 对比总结

### 4. 搜索论文
按作者/标题精确搜索 或 按主题语义搜索

### 5. 加标签
搜索论文 → `add_tags` 添加标签（不覆盖已有标签）

## 常见问题

### `zotero_get_item_fulltext` 返回网页内容而非 PDF 正文

**原因**：Zotero 保存论文时会同时保存 HTML 快照，全文索引可能优先缓存了快照内容。

**解决方案**：
1. 使用 `get_attachment_path` + `Read` 读取 PDF（Skill 默认使用此方式）
2. 在 Zotero 设置中关闭自动快照：设置 → 常规 → 取消勾选"保存条目时自动生成快照"
3. 批量删除已有快照：在 Zotero 桌面端 → 工具 → 开发者 → Run JavaScript：

```javascript
var s = new Zotero.Search();
s.libraryID = Zotero.Libraries.userLibraryID;
s.addCondition('itemType', 'is', 'attachment');
var ids = await s.search();
var items = await Zotero.Items.getAsync(ids);
var snapshotIds = items
    .filter(item => item.attachmentContentType === 'text/html' && !item.deleted)
    .map(item => item.id);
await Zotero.Items.trashTx(snapshotIds);
return `Trashed ${snapshotIds.length} HTML snapshot attachments.`;
```

### 创建笔记时提示 "standalone note, not attached to the paper"

**原因**：本地模式的 connector API 不支持 `parentItem`，需要配置 Web API。

**解决方案**：在 MCP 配置中添加 `ZOTERO_API_KEY`、`ZOTERO_LIBRARY_ID`、`ZOTERO_LIBRARY_TYPE`。

### 想创建独立笔记但工具强制要求 `item_key`

**原因**：原版 `create_note` 的 `item_key` 是必填参数。

**解决方案**：本 fork 已修复，`item_key` 改为可选。不传 `item_key` 即创建独立笔记。

### Lite 模式不生效，仍然看到 55 个工具

**检查项**：
1. 确认 `ZOTERO_MCP_LITE=true` 已添加到 MCP 配置的 `env` 中
2. 重启 Claude Code / Claude Desktop
3. 确认使用的是本 fork 修改后的 `tools/__init__.py`

### 笔记中 Markdown 没有正确渲染

**原因**：Zotero 笔记原生格式是 HTML，不是 Markdown。

**解决方案**：
- Skill 会自动使用 HTML 格式（`<h2>`, `<ul>` 等）保存笔记
- 安装 [Better Notes](https://github.com/windingwind/zotero-better-notes) 插件后，可以在 Zotero 中以 Markdown 模式编辑 HTML 笔记

## 致谢

基于 [zotero-mcp-server](https://github.com/anthropics/zotero-mcp-server) 开发。

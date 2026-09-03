# PM 分析 Skills

产品经理竞品调研相关的 Agent Skills 合集（WorkBuddy / Claude Code 通用）。

> **注意**：本仓库为私有仓库，包含氢离子（Ali-Doctor）内部参考资料（功能清单、使用手册），请勿外传或公开。

## 包含的 Skills

| Skill | 作用 | 目录 |
| --- | --- | --- |
| **complete-competitor-analysis** | 把半成品竞品调研报告补全为可直接交付的成稿：自动补「总结（优点/缺点/启示）」和「功能对比清单（分模块表格）」，统一排版并插入目录 | `skills/complete-competitor-analysis/` |
| **product-analysis-report** | 基于产品官网 + 截图文件夹，生成一份标准的「竞品产品功能拆解报告」（核心定位 / 树状总览 / 分模块表格） | `skills/product-analysis-report/` |

## 安装

### WorkBuddy

把 skill 文件夹复制到用户级目录即可全局生效：

```bash
cp -r skills/complete-competitor-analysis ~/.workbuddy/skills/
cp -r skills/product-analysis-report ~/.workbuddy/skills/
```

或只装到单个项目：`{项目}/.workbuddy/skills/`

### Claude Code

```bash
cp -r skills/complete-competitor-analysis ~/.claude/skills/
cp -r skills/product-analysis-report ~/.claude/skills/
```

## 使用

- **complete-competitor-analysis**：先完成竞品的「功能盘点」，再对助手说「帮我补充/完善这份竞品调研报告」，并附上参考示例与氢离子功能手册。
- **product-analysis-report**：对助手说「帮我拆解 XX 产品」并给出产品名称/官网链接和截图文件夹。

## 目录结构

```
skills/
├── complete-competitor-analysis/
│   ├── SKILL.md
│   ├── references/          # 参考示例、氢离子功能清单、使用手册
│   └── scripts/
└── product-analysis-report/
    ├── SKILL.md
    └── references/
```

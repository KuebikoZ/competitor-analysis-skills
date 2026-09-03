# PM 分析 Skills

产品经理竞品调研相关的 Agent Skills 合集（WorkBuddy / Claude Code 通用），包含一个**配套的两步工作流**：先用功能拆解 skill 产出竞品的功能盘点，再用竞品报告完善 skill 补全为可交付的成稿。

## 包含的 Skills

| Skill | 作用 | 目录 |
| --- | --- | --- |
| **product-analysis-report**（第 1 步·功能拆解） | 基于产品官网 + 截图文件夹，生成一份标准的「竞品产品功能拆解报告」（核心定位 / 树状总览 / 分模块功能盘点表格） | `skills/product-analysis-report/` |
| **complete-competitor-analysis**（第 2 步·报告完善） | 把半成品竞品调研报告补全为可直接交付的成稿：自动补「总结（优点/缺点/启示）」和「功能对比清单（分模块表格）」，统一排版并插入目录 | `skills/complete-competitor-analysis/` |

## 使用流程（两个 skill 配套使用）

建议按以下顺序执行，形成完整的竞品调研产出：

1. **第 1 步：功能拆解** — 使用 `product-analysis-report`
   对助手说「帮我拆解 XX 产品」，并提供产品名称/官网链接、截图文件夹，得到一份标准的**产品功能拆解报告**（含分模块功能盘点），这是后续分析的素材基础。

2. **第 2 步：报告完善** — 使用 `complete-competitor-analysis`
   把第 1 步拆解出的「功能盘点」部分作为输入，对助手说「帮我补充/完善这份竞品调研报告」，自动补齐「总结（优点/缺点/启示）」与「功能对比清单」，输出可直接交付的完整成稿。

> 也可以单独使用其中任意一个 skill：`product-analysis-report` 独立产出功能拆解报告；`complete-competitor-analysis` 可完善任意已有的竞品功能盘点文档。

## 安装

### WorkBuddy

把 skill 文件夹复制到用户级目录即可全局生效：

```bash
cp -r skills/product-analysis-report ~/.workbuddy/skills/
cp -r skills/complete-competitor-analysis ~/.workbuddy/skills/
```

或只装到单个项目：`{项目}/.workbuddy/skills/`

### Claude Code

```bash
cp -r skills/product-analysis-report ~/.claude/skills/
cp -r skills/complete-competitor-analysis ~/.claude/skills/
```

## 目录结构

```
skills/
├── product-analysis-report/          # 第 1 步：功能拆解
│   ├── SKILL.md
│   └── references/                   # 报告格式参考
└── complete-competitor-analysis/     # 第 2 步：报告完善
    ├── SKILL.md
    ├── references/                   # 参考示例、氢离子功能清单、公开手册
    └── scripts/
```

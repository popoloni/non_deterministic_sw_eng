# AI-Assisted Engineering Examples

> Companion repository for **"Non-Deterministic Software Engineering"** by Enrico Papalini

[![Validate Configs](https://github.com/popoloni/non_deterministic_sw_eng/actions/workflows/validate-configs.yml/badge.svg)](https://github.com/popoloni/non_deterministic_sw_eng/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📖 About This Repository

This repository contains **working code examples, configuration templates, and practical materials** from the book. Unlike typical code snippets, these examples are designed to be:

- ✅ **Complete** — Ready to use, not just illustrative fragments
- ✅ **Tested** — Validated with current tool versions
- ✅ **Documented** — Each example links back to the relevant book chapter

---

## � Book Structure

The book is organized into **5 Parts** containing **10 Chapters** plus **4 Appendices**:

| Part | Focus | Chapters |
|------|-------|----------|
| **Part I** | Understanding the Transformation | Ch. 1–3 |
| **Part II** | Practical Implementation | Ch. 4–6 |
| **Part III** | Organizational Adaptation | Ch. 8–9 |
| **Part IV** | Patterns, Tools & Practices | Ch. 7, 10 |
| **Part V** | Appendices | A–D |

### Chapter Overview

| Chapter | Title | Focus |
|---------|-------|-------|
| 1 | The Fundamental Shift | Determinism → Non-determinism paradigm |
| 2 | Vibe Coding vs. AI-Assisted Engineering | The 70% problem |
| 3 | The Experience Divide | How AI affects different career stages |
| 4 | New Workflows for the AI Era | 10 practical workflows |
| 5 | The Quality Crisis | Multi-layer verification |
| 6 | Measuring What Matters | Metrics framework |
| 7 | The Pattern Catalog | 18 patterns + 8 antipatterns |
| 8 | The Adaptation Imperative | Organizational transformation |
| 9 | Looking Forward | Future trajectories |
| 10 | Tools & Practices | Implementation guide |

---

## 🗂️ Repository Structure

| Folder | Description | Book Reference |
|--------|-------------|----------------|
| [01-fundamentals](./01-fundamentals/) | Conceptual overview | Part I (Ch. 1–3) |
| [02-specifications](./02-specifications/) | Spec-first development templates | Ch. 7 (Pattern 1) |
| [03-migrations](./03-migrations/) | Code migration examples | Ch. 7 (Pattern 12) |
| [04-context-engineering](./04-context-engineering/) | AGENTS.md, Cursor rules, Copilot instructions | Ch. 10 (Sections 3–4) |
| [05-mcp-servers](./05-mcp-servers/) | Model Context Protocol server examples | Ch. 10 (Section 5) |
| [06-custom-agents](./06-custom-agents/) | Custom agent definitions for AI tools | Ch. 10 (Section 6) |
| [07-enterprise-workflow](./07-enterprise-workflow/) | Multi-agent orchestration patterns | Appendix C |
| [08-security](./08-security/) | Security checklists and review guides | Ch. 7 (Pattern 9) |
| [09-exercises](./09-exercises/) | Hands-on exercises with solutions | Appendix C |

---

## 🚀 Quick Start

### For Context Engineering (Most Popular)

```bash
# Copy the minimal AGENTS.md to your project
cp 04-context-engineering/agents-md/minimal.md YOUR_PROJECT/AGENTS.md

# Or use Cursor rules
cp -r 04-context-engineering/cursor-rules/.cursor YOUR_PROJECT/
```

### For MCP Servers

```bash
cd 05-mcp-servers/company-docs-server
pip install -r requirements.txt
python server.py
```

### For Custom Agents

Copy agent definitions to your project's `.github/agents/` folder (for GitHub Copilot) or reference them in Claude Code.

---

## 📚 Book Information

**Title:** Non-Deterministic Software Engineering  
**Subtitle:** How to Build Reliable Software with AI Assistants Without Losing Quality, Security, or Control  
**Author:** Enrico Papalini  
**Year:** 2025  

- 📕 [Paperback ISBN: 979-8-278715-41-2]
- 📘 [Hardcover ISBN: 979-8-278829-88-1]

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

**Ways to contribute:**
- 🐛 Report outdated examples (tool configs change frequently)
- 📝 Add language variants (TypeScript ↔ Python)
- 🔧 Expand snippets into complete projects
- 📖 Improve documentation

---

## 📋 Version Compatibility

All examples include metadata indicating tool versions:

```yaml
---
tool: cursor
tool_version: "1.0"
last_verified: 2025-12-16
---
```

Check the `last_verified` date and tool version before using in production.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

## ⭐ Star This Repo

If you find these examples helpful, please star the repository to help others discover it!

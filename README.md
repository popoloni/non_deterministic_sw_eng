# Non-Deterministic Software Engineering — Companion Repository

Companion code for both editions of **Non-Deterministic Software Engineering** by Enrico Papalini.

<table>
  <tr>
    <th width="50%">Second edition · 2026 · v13.7.3</th>
    <th width="50%">First edition · 2025</th>
  </tr>
  <tr>
    <td align="center">
      <a href="https://www.amazon.com/dp/B0HN9KQLNG">
        <img src="https://m.media-amazon.com/images/I/814bnsFHfKL._SL1500_.jpg" alt="Non-Deterministic Software Engineering, Second Edition — book cover" width="220">
      </a>
    </td>
    <td align="center">
      <a href="https://www.amazon.com/dp/B0G7LPR4KB">
        <img src="https://m.media-amazon.com/images/I/71mLAazNLyL._SL1500_.jpg" alt="Non-Deterministic Software Engineering, First Edition — book cover" width="220">
      </a>
    </td>
  </tr>
  <tr>
    <td>
      <em>Engineering Trustworthy Change in the Age of AI and Coding Agents</em><br><br>
      📕 <a href="https://www.amazon.com/dp/B0HN9KQLNG">Buy on Amazon</a><br>
      🧪 Laboratory: <a href="ndse2/lab/README_EN.md">English guide</a> · <a href="ndse2/lab/README_ITA.md">Guida italiana</a><br>
      📦 Download: <a href="https://github.com/popoloni/non_deterministic_sw_eng/releases/download/v13.7.3/NDSE_v13.7.3_Companion.zip">NDSE_v13.7.3_Companion.zip</a> (<a href="https://github.com/popoloni/non_deterministic_sw_eng/releases/tag/v13.7.3">release v13.7.3</a>)<br>
      🗺️ <a href="https://popoloni.github.io/">Knowledge Atlas</a>
    </td>
    <td>
      <em>How to Build Reliable Software with AI Assistants Without Losing Quality, Security, or Control</em><br><br>
      📕 <a href="https://www.amazon.com/dp/B0G7LPR4KB">Buy on Amazon</a><br>
      📂 Examples: chapter folders <a href="01-fundamentals/">01</a>–<a href="09-exercises/">09</a> (see <a href="#first-edition-companion-material">below</a>)
    </td>
  </tr>
</table>

---

## Second edition laboratory / Laboratorio della seconda edizione

The second-edition laboratory is self-contained in [`ndse2/`](ndse2/). It follows one synthetic maintenance case through the book's 13 chapters and needs only Python 3.10+ and its standard library:

```sh
cd ndse2
python3 scripts/run_lab_checks.py
```

Il laboratorio della seconda edizione è autonomo nella cartella [`ndse2/`](ndse2/): segue un unico caso sintetico attraverso i 13 capitoli e richiede solo Python 3.10 o successivo con la libreria standard.

The book identifies the laboratory by commit [`de019b7`](https://github.com/popoloni/non_deterministic_sw_eng/tree/de019b7e7659c3b227c44b491364268d2a04f6e0/ndse2). The release ZIP extracts to `NDSE_Companion/`; its SHA-256 is `97a4032e107706a07ef1c1333c586aeb0492cbed1ce420f5f4f1d0376f2d78e1` (also listed in the release's `SHA256SUMS.txt`). GitHub's automatically generated "Source code" archives are not the companion ZIP.

---

## First edition companion material

> Companion material for the first edition of **["Non-Deterministic Software Engineering"](https://www.amazon.com/dp/B0G7LPR4KB)** by Enrico Papalini

[![Validate Configs](https://github.com/popoloni/non_deterministic_sw_eng/actions/workflows/validate-configs.yml/badge.svg)](https://github.com/popoloni/non_deterministic_sw_eng/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📖 About This Repository

This repository contains **working code examples, configuration templates, and practical materials** from the book. Unlike typical code snippets, these examples are designed to be:

- ✅ **Complete** — Ready to use, not just illustrative fragments
- ✅ **Tested** — Validated with current tool versions
- ✅ **Documented** — Each example links back to the relevant book chapter

---

## 📑 Book Structure (first edition)

The first edition is organized into **5 Parts** containing **10 Chapters** plus **4 Appendices**:

| Part | Focus | Chapters |
|------|-------|----------|
| **Part I** | Understanding the Transformation | Ch. 1–3 |
| **Part II** | Practical Implementation | Ch. 4–6 |
| **Part III** | Organizational Adaptation | Ch. 7-8 |
| **Part IV** | Patterns, Tools & Practices | Ch. 9-10 |
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
| 7 | The Adaptation Imperative | Organizational transformation |
| 8 | Looking Forward | Future trajectories |
| 9 | The Pattern Catalog | 18 patterns + 8 antipatterns |
| 10 | Tools & Practices | Implementation guide |

---

## 🗂️ Repository Structure

| Folder | Description | Book Reference |
|--------|-------------|----------------|
| [01-fundamentals](./01-fundamentals/) | Conceptual overview | Part I (Ch. 1–3) |
| [02-specifications](./02-specifications/) | Spec-first development templates | Ch. 9 (Pattern 1) |
| [03-migrations](./03-migrations/) | Code migration examples | Ch. 9 (Pattern 12) |
| [04-context-engineering](./04-context-engineering/) | AGENTS.md, Cursor rules, Copilot instructions | Ch. 10 (Sections 3–4) |
| [05-mcp-servers](./05-mcp-servers/) | Model Context Protocol server examples | Ch. 10 (Section 5) |
| [06-custom-agents](./06-custom-agents/) | Custom agent definitions for AI tools | Ch. 10 (Section 6) |
| [07-enterprise-workflow](./07-enterprise-workflow/) | Multi-agent orchestration patterns | Appendix C |
| [08-security](./08-security/) | Security checklists and review guides | Ch. 9 (Pattern 9) |
| [09-exercises](./09-exercises/) | Hands-on exercises with solutions | Appendix C |
| [ndse2](./ndse2/) | **Second-edition** laboratory (v13.7.3) | Second edition, Ch. 1–13 |

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

### Second edition

**Title:** Non-Deterministic Software Engineering — Second Edition  
**Subtitle:** Engineering Trustworthy Change in the Age of AI and Coding Agents  
**Author:** Enrico Papalini  
**Year:** 2026  

📕 **[Buy on Amazon](https://www.amazon.com/dp/B0HN9KQLNG)** · 🧪 **[Laboratory](ndse2/)** · 📦 **[Release v13.7.3](https://github.com/popoloni/non_deterministic_sw_eng/releases/tag/v13.7.3)**

### First edition

**Title:** Non-Deterministic Software Engineering  
**Subtitle:** How to Build Reliable Software with AI Assistants Without Losing Quality, Security, or Control  
**Author:** Enrico Papalini  
**Year:** 2025  

📕 **[Buy on Amazon](https://www.amazon.com/dp/B0G7LPR4KB)**

- Paperback ISBN: 979-8-278715-41-2
- Hardcover ISBN: 979-8-278829-88-1

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

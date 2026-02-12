# Polyglot Code Playground

A browser-based code playground supporting **multiple languages** via WebAssembly and browser-native runtimes.

**Languages currently supported:**
- JavaScript / TypeScript (native)
- Python (Pyodide)
- Rust (WebAssembly)
- Go (TinyGo + WASM)
- Lua (Fengari)

Features:
- Split-pane editor + output
- Syntax highlighting (Monaco Editor or CodeMirror)
- Live run / share via URL
- Dark mode + modern UI (shadcn/ui + Tailwind)
- No backend needed (all client-side)

## Tech Stack

- React + TypeScript + Vite
- Tailwind CSS + shadcn/ui
- Monaco Editor / CodeMirror (choose one)
- Pyodide (Python in WASM)
- wasm-pack (Rust → WASM)
- TinyGo (Go → WASM)
- Fengari (Lua → JS)

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/polyglot-code-playground.git
cd polyglot-code-playground
npm install
npm run dev

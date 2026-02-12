let rustModule: any = null

export async function runRust(code: string): Promise<string> {
  if (!rustModule) {
    // Dynamic import or preloaded
    rustModule = await import(/* @vite-ignore */ '/wasm/rust_runner/pkg/rust_runner.js')
    await rustModule.default()
  }

  try {
    const result = rustModule.run_code(code)
    return result
  } catch (err: any) {
    return `Rust error: ${err}`
  }
}

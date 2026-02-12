import { loadPyodide, PyodideInterface } from 'pyodide'

let pyodide: PyodideInterface | null = null

export async function runPython(code: string): Promise<string> {
  if (!pyodide) {
    pyodide = await loadPyodide({
      indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.26.2/full/',
    })
  }

  try {
    const output = await pyodide.runPythonAsync(code)
    return output ?? 'No output'
  } catch (err: any) {
    return `Error: ${err.message}`
  }
}

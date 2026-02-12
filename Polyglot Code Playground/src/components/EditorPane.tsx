import Editor from '@monaco-editor/react'
import { useState } from 'react'
import { Language } from '@/types'

interface Props {
  language: Language
  value: string
  onChange: (value: string | undefined) => void
}

export function EditorPane({ language, value, onChange }: Props) {
  const [mounted, setMounted] = useState(false)

  return (
    <div className="h-full border rounded-md overflow-hidden">
      <Editor
        height="100%"
        language={language === 'typescript' ? 'typescript' : language}
        theme="vs-dark"
        value={value}
        onChange={onChange}
        onMount={() => setMounted(true)}
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          lineNumbers: 'on',
          scrollBeyondLastLine: false,
        }}
      />
    </div>
  )
}

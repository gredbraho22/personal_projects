export type Language =
  | 'javascript'
  | 'typescript'
  | 'python'
  | 'rust'
  | 'go'
  | 'lua'
  | 'cpp'

export interface CodeState {
  language: Language
  code: string
  output: string
  isRunning: boolean
}

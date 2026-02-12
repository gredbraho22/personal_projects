export interface Trade {
  date: Date
  symbol: string
  side: 'long' | 'short'
  entryPrice: number
  exitPrice: number
  quantity: number
  pnl: number
  rMultiple?: number
  strategy?: string
  notes?: string
}

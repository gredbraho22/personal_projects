import Papa from 'papaparse'
import { Trade } from '@/types'

export function parseTrades(file: File): Promise<Trade[]> {
  return new Promise((resolve, reject) => {
    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: (results) => {
        const trades: Trade[] = results.data
          .map((row: any) => {
            try {
              const date = new Date(row.date || row.Date || row['Trade Date'])
              const entry = parseFloat(row.entry || row['Entry Price'] || row.avgPrice)
              const exit = parseFloat(row.exit || row['Exit Price'] || row.avgPriceExit)
              const qty = parseFloat(row.quantity || row['Qty'] || row.shares)
              const pnl = parseFloat(row.pnl || row['P/L $'] || row['Net P/L'])

              return {
                date,
                symbol: (row.symbol || row.Symbol || '').trim(),
                side: (row.side || row.Direction || 'long').toLowerCase() as 'long' | 'short',
                entryPrice: entry,
                exitPrice: exit,
                quantity: qty,
                pnl: pnl || (exit - entry) * qty * (row.side?.toLowerCase() === 'short' ? -1 : 1),
                rMultiple: pnl && entry ? pnl / (qty * Math.abs(entry * 0.01)) : undefined,
                strategy: row.strategy || row['Strategy Tag'],
                notes: row.notes || row['Note'],
              }
            } catch {
              return null
            }
          })
          .filter((t): t is Trade => t !== null && !isNaN(t.pnl))

        resolve(trades)
      },
      error: reject,
    })
  })
}

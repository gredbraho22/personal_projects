import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Trade } from '@/types'
import { format } from 'date-fns'

interface Props {
  trades: Trade[]
}

export function PerformanceCards({ trades }: Props) {
  if (trades.length === 0) return null

  const totalPnL = trades.reduce((sum, t) => sum + t.pnl, 0)
  const wins = trades.filter(t => t.pnl > 0).length
  const winRate = (wins / trades.length) * 100
  const avgWin = trades.filter(t => t.pnl > 0).reduce((sum, t) => sum + t.pnl, 0) / wins || 0
  const avgLoss = trades.filter(t => t.pnl < 0).reduce((sum, t) => sum + t.pnl, 0) / (trades.length - wins) || 0
  const expectancy = (winRate / 100 * avgWin) + ((1 - winRate / 100) * avgLoss)
  const profitFactor = Math.abs(trades.filter(t => t.pnl > 0).reduce((s, t) => s + t.pnl, 0) /
    trades.filter(t => t.pnl < 0).reduce((s, t) => s + t.pnl, 0)) || 0

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mt-8">
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium">Total PnL</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            ${totalPnL.toFixed(2)}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium">Win Rate</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            {winRate.toFixed(1)}%
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium">Expectancy</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            ${expectancy.toFixed(2)}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium">Profit Factor</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            {profitFactor.toFixed(2)}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

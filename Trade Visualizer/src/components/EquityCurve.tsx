import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { Trade } from '@/types'
import { format } from 'date-fns'

interface Props {
  trades: Trade[]
}

export function EquityCurve({ trades }: Props) {
  const sorted = [...trades].sort((a, b) => a.date.getTime() - b.date.getTime())
  let cum = 0
  const data = sorted.map(t => {
    cum += t.pnl
    return { date: format(t.date, 'MMM dd'), equity: cum }
  })

  return (
    <div className="h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="equity" stroke="#10b981" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

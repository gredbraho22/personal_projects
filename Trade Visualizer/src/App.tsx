import { TradeUploader } from '@/components/TradeUploader'
import { PerformanceCards } from '@/components/PerformanceCards'
import { EquityCurve } from '@/components/EquityCurve'
import { MonthlyHeatmap } from '@/components/MonthlyHeatmap'
import { TradeTable } from '@/components/TradeTable'
import { RiskCalculator } from '@/components/RiskCalculator'
import { ThemeToggle } from '@/components/ThemeToggle'
import { Header } from '@/components/Header'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useState } from 'react'
import { Trade } from '@/types'

function App() {
  const [trades, setTrades] = useState<Trade[]>([])

  return (
    <div className="min-h-screen bg-background text-foreground antialiased">
      <Header />
      <main className="container mx-auto py-8 px-4 md:px-6">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold tracking-tight">Trade Visualizer</h1>
          <ThemeToggle />
        </div>

        <TradeUploader onTradesLoaded={setTrades} />

        {trades.length > 0 && (
          <>
            <PerformanceCards trades={trades} />

            <div className="grid gap-6 md:grid-cols-2 mt-8">
              <Card>
                <CardHeader>
                  <CardTitle>Equity Curve</CardTitle>
                </CardHeader>
                <CardContent>
                  <EquityCurve trades={trades} />
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Monthly Heatmap</CardTitle>
                </CardHeader>
                <CardContent>
                  <MonthlyHeatmap trades={trades} />
                </CardContent>
              </Card>
            </div>

            <Card className="mt-8">
              <CardHeader>
                <CardTitle>Trade List</CardTitle>
              </CardHeader>
              <CardContent>
                <TradeTable trades={trades} />
              </CardContent>
            </Card>

            <Card className="mt-8">
              <CardHeader>
                <CardTitle>Risk & Position Sizing Calculator</CardTitle>
              </CardHeader>
              <CardContent>
                <RiskCalculator />
              </CardContent>
            </Card>
          </>
        )}
      </main>
    </div>
  )
}

export default App

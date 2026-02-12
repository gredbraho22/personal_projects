import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { parseTrades } from '@/lib/tradeParser'
import { Trade } from '@/types'
import { Upload } from 'lucide-react'

interface Props {
  onTradesLoaded: (trades: Trade[]) => void
}

export function TradeUploader({ onTradesLoaded }: Props) {
  const handleFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    try {
      const trades = await parseTrades(file)
      onTradesLoaded(trades)
    } catch (err) {
      console.error(err)
      alert('Error parsing CSV. Please check the file format.')
    }
  }

  return (
    <div className="border-2 border-dashed rounded-lg p-8 text-center">
      <Upload className="mx-auto h-12 w-12 text-muted-foreground" />
      <h3 className="mt-4 text-lg font-medium">Upload your trade history CSV</h3>
      <p className="mt-2 text-sm text-muted-foreground">
        Supported formats: Thinkorswim, Interactive Brokers, Tradovate, NinjaTrader, etc.
      </p>
      <Input
        type="file"
        accept=".csv"
        onChange={handleFile}
        className="mt-6 max-w-xs mx-auto"
      />
    </div>
  )
}

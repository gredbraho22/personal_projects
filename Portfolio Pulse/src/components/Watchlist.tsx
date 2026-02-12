import { Badge } from '@/components/ui/badge'
import { watchlistItems } from '@/data/mockData'

export function Watchlist() {
  return (
    <div className="space-y-4">
      {watchlistItems.map((item) => (
        <div key={item.symbol} className="flex justify-between items-center p-4 border rounded-lg">
          <div>
            <div className="font-medium">{item.symbol}</div>
            <div className="text-sm text-muted-foreground">{item.name}</div>
          </div>
          <div className="text-right">
            <div className="font-medium">${item.price.toFixed(2)}</div>
            <Badge variant={item.change >= 0 ? "default" : "destructive"}>
              {item.change >= 0 ? '+' : ''}{item.change.toFixed(2)}%
            </Badge>
          </div>
        </div>
      ))}
    </div>
  )
}

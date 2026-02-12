export interface PortfolioEntry {
  date: string
  value: number
}

export interface AllocationItem {
  name: string
  value: number
}

export interface Metric {
  metric: string
  value: string
}

export interface WatchlistItem {
  symbol: string
  name: string
  price: number
  change: number
}

import { Dashboard } from '@/components/Dashboard'
import { ThemeToggle } from '@/components/ThemeToggle'
import { Header } from '@/components/Header'

function App() {
  return (
    <div className="min-h-screen bg-background text-foreground antialiased">
      <Header />
      <main className="container mx-auto py-8 px-4 md:px-6">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold tracking-tight">Portfolio Pulse</h1>
          <ThemeToggle />
        </div>
        <Dashboard />
      </main>
    </div>
  )
}

export default App

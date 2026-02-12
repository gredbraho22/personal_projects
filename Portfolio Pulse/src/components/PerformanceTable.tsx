import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { performanceMetrics } from '@/data/mockData'

export function PerformanceTable() {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Metric</TableHead>
          <TableHead className="text-right">Value</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {performanceMetrics.map((item) => (
          <TableRow key={item.metric}>
            <TableCell className="font-medium">{item.metric}</TableCell>
            <TableCell className="text-right">{item.value}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}

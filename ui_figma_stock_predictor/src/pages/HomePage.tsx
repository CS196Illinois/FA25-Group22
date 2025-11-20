import React from 'react'
import ChartPlaceholder from '@/components/ChartPlaceholder'
import StatCard from '@/components/StatCard'

const HomePage: React.FC = () => {
  return (
    <div className="mx-auto max-w-7xl px-4 pb-10">
      {/* Top section: Title + Sidebar stats */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-4">
        <div className="lg:col-span-2">
          <h1 className="font-display text-[56px] md:text-[80px] leading-tight text-paper-50">
            Stock Name
          </h1>
        </div>
        <div className="lg:col-span-1 space-y-4">
          <StatCard title="Profit / Loss Win Rate" value="62.4%" />
          <StatCard title="Win Rate" value="55.1%" />
          <StatCard title="Max Markdown" value="-8.3%" />
        </div>
      </div>

      {/* Chart area */}
      <div className="mt-8 lg:mt-10 grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="rounded-2xl bg-ink-800/60 ring-1 ring-white/20 p-6">
            <div className="text-[32px] md:text-[48px] text-paper-50 mb-4 font-sans">Line Chart</div>
            <ChartPlaceholder />
          </div>
        </div>
        <div className="lg:col-span-1">
          <div className="rounded-2xl bg-paper-50/10 backdrop-blur-[2px] ring-1 ring-white/20 p-6 h-full">
            <div className="text-lg text-paper-50 mb-3 font-heading">Alpha</div>
            <div className="text-paper-50/70">
              Add auxiliary indicators, notes, or filters here.
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default HomePage




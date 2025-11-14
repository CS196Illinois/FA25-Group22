import React from 'react'

interface StatCardProps {
  title: string
  value?: string
  children?: React.ReactNode
}

const StatCard: React.FC<StatCardProps> = ({ title, value, children }) => {
  return (
    <div className="rounded-2xl bg-paper-50/10 backdrop-blur-[2px] ring-1 ring-white/20 p-5 text-paper-50">
      <div className="text-[20px] md:text-[28px] tracking-wide text-paper-50/80 font-heading">
        {title}
      </div>
      {value ? (
        <div className="mt-1 text-2xl md:text-3xl font-semibold">
          {value}
        </div>
      ) : null}
      {children ? (
        <div className="mt-3">
          {children}
        </div>
      ) : null}
    </div>
  )
}

export default StatCard




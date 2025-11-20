import React from 'react'

interface LayoutProps {
  children: React.ReactNode
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen w-full relative bg-gradient-to-b from-[#3C24B3] to-[#502D69] text-paper-50">
      {/* Decorative ellipses based on Figma */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <div className="absolute -top-10 -left-12 h-[220px] w-[560px] rounded-full bg-[#8C8AFD] opacity-20 blur-2xl" />
        <div className="absolute top-[300px] left-[360px] h-[64px] w-[604px] rounded-full bg-[#8C8AFD] opacity-25 blur-xl" />
        <div className="absolute top-[400px] right-[120px] h-[200px] w-[256px] rounded-full bg-[#070606] opacity-10 blur-xl" />
      </div>
      <header className="w-full">
        <div className="mx-auto max-w-7xl px-4 py-6 flex items-center justify-end">
          <div className="relative w-full max-w-md">
            <input
              type="text"
              placeholder="Feature search"
              className="w-full rounded-xl bg-[#8C8AFD] placeholder-black/80 text-black px-4 py-3 pr-10 outline-none ring-1 ring-black/10 focus:ring-2 focus:ring-black/20 font-condensed"
            />
            <span className="absolute inset-y-0 right-3 flex items-center text-black/80 font-icon">
              🔎
            </span>
          </div>
        </div>
      </header>
      <main className="w-full">
        {children}
      </main>
    </div>
  )
}

export default Layout






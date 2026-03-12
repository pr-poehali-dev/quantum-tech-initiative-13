import { ReactNode } from 'react'
import { Squares } from "./squares-background"

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="h-screen overflow-hidden bg-black relative">
      <div
        className="absolute inset-0 z-0"
        style={{
          backgroundImage: 'url(https://cdn.poehali.dev/projects/4f3fedfe-47b9-42a8-9581-71aa9df7a468/files/3abe17f4-5318-4707-a11e-e4d45b18e758.jpg)',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          opacity: 0.25,
        }}
      />
      <div className="absolute inset-0 z-10">
        <Squares
          direction="diagonal"
          speed={0.5}
          squareSize={40}
          borderColor="#1a3a2a"
          hoverFillColor="#0d2a1a"
        />
      </div>
      <div className="relative z-20 h-full">
        {children}
      </div>
    </div>
  )
}
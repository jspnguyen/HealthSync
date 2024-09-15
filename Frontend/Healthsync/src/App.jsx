import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import ForceDirectedLayout from './components/networkx-visualizer'

function App() {
  return (

    <div className="App">

      <ForceDirectedLayout />
    </div>
  )
}

export default App

import { Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import Layout from './components/Layout'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HomePage />} />
        {/* Add more routes here as pages are added */}
      </Routes>
    </Layout>
  )
}

export default App





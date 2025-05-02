import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './HomePage.jsx';
import ModifyPage from './ModifyPage.jsx';
import ReportPage from './ReportPage.jsx';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage/>} />
        <Route path="/modify" element={<ModifyPage/>} />
        <Route path="/report" element={<ReportPage/>} />
      </Routes>
      </BrowserRouter>
    </div>
  )
}

export default App

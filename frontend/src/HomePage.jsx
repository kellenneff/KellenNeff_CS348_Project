import React from 'react';
import Button from '@mui/material/Button';

function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center w-screen h-screen bg-gray-50">
      <div className="p-8 rounded-lg shadow-lg bg-white max-w-2xl w-full">
        <h1 className="text-3xl font-bold text-center mb-8 text-blue-700">
          Animal Adoption Treatment Management
        </h1>
        
        <div className="flex flex-col md:flex-row justify-center items-center gap-4">
          <Button 
            variant="contained" 
            color="primary" 
            className="w-full md:w-auto py-3"
            size="large"
            onClick={() => window.location.href='/modify'}
          >
            Modify Records
          </Button>
          
          <Button 
            variant="contained" 
            color="primary" 
            className="w-full md:w-auto py-3"
            size="large"
            onClick={() => window.location.href='/report'}
          >
            Generate Report
          </Button>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
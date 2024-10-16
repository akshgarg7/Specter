import React, { useState, useEffect } from "react"

function RunsPage() {
    const [loadingStates, setLoadingStates] = useState(Array(10).fill(true));
  
    useEffect(() => {
      const checkTaskStatus = async (index: number) => {
        try {
          const response = await fetch(`http://localhost:8080/status?task_id=${index + 1}`);
          const data = await response.json();
          console.log(data)
          if (data === true) {
            setLoadingStates((prevStates) => {
              const newStates = [...prevStates];
              newStates[index] = false;
              return newStates;
            });
          }
        } catch (error) {
          console.error("Error fetching task status:", error);
        }
      };
  
      loadingStates.forEach((_, index) => {
        checkTaskStatus(index);
      });
  
      const intervalId = setInterval(() => {
        loadingStates.forEach((_, index) => {
          checkTaskStatus(index);
        });
      }, 5000); // Check every 5 seconds
  
      return () => clearInterval(intervalId); // Cleanup interval on unmount
    }, [loadingStates]);
  
    const runs = Array.from({ length: 10 }, (_, index) => ({
      simulation: `Simulation ${index + 1}`,
      details: "(For case GTI vs. EPS - Triggered by Aksh)"
    }));
  
    const allTasksComplete = loadingStates.every(state => !state);
  
    return (
      <div className="min-h-screen bg-white p-8 flex flex-col">
        <div className="flex-1">
          <h1 className="text-4xl font-serif mb-8">View all your runs here</h1>
          <div className="bg-gray-50 rounded-lg shadow-sm">
            <ul className="divide-y divide-gray-200">
              {runs.map((run, index) => (
                <li key={index} className="p-4 flex justify-between items-center">
                  <div>
                    <span className="text-lg font-bold text-gray-900">{run.simulation}</span>
                    <span className="text-sm text-gray-500"> {run.details}</span>
                  </div>
                  {loadingStates[index] && (
                    <div className="loader border-t-2 border-b-2 border-gray-900 w-6 h-6 rounded-full animate-spin"></div>
                  )}
                </li>
              ))}
            </ul>
          </div>
        </div>
        {allTasksComplete && (
          <button
            onClick={() => window.location.href = 'https://playground.outspeed.com/'}
            className="mt-4 mb-8 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-500 transition-colors"
          >
            Click to Negotiate
          </button>
        )}
      </div>
    );
  }

export default RunsPage;
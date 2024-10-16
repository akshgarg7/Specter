import React, { useState, useEffect } from "react"
import { BACKEND_URL } from '../lib/config';
interface Message {
    speaker: string;
    message: string;
}

function ViewRunsPage() {
    const [conversations, setConversations] = useState<Message[]>([]);
    const [selectedRun, setSelectedRun] = useState<string | null>(null);
  
    useEffect(() => {
      const fetchConversations = async () => {
        try {
          const response = await fetch(`${BACKEND_URL}/get-trajectory?task_id=${selectedRun}`);
          const data = await response.json();
  
          console.log(data)
          
          // Access the 'conversation' array from the response
          if (data && Array.isArray(data.conversation)) {
            setConversations(data.conversation);
          } else {
            console.error("Unexpected data format:", data);
            setConversations([]);
          }
        } catch (error) {
          console.error("Error fetching conversations:", error);
          setConversations([]);
        }
      };
  
      if (selectedRun !== null) {
        fetchConversations();
      }
    }, [selectedRun]);
  
    const handleRunChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
      setSelectedRun(event.target.value);
    };
  
    return (
      <div className="min-h-screen bg-white p-8">
        <h2 className="text-2xl font-serif mb-4">View Runs</h2>
        <select onChange={handleRunChange} className="mb-4 p-2 border rounded">
          <option value="">Select a run</option>
          {Array.from({ length: 10 }, (_, index) => (
            <option key={index} value={index + 1}>
              Run {index + 1}
            </option>
          ))}
        </select>
        <div className="bg-gray-50 rounded-lg shadow-sm p-4">
          {selectedRun !== null && conversations.map((message, index) => (
            <div key={index} className={`p-2 ${message.speaker.includes("GTI") ? "text-blue-600" : "text-green-600"}`}>
              <strong>{message.speaker}:</strong> {message.message}
            </div>
          ))}
        </div>
      </div>
    );
  }

export default ViewRunsPage;
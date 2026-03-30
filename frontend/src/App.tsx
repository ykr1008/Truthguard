import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [claim, setClaim] = useState("")
  const [jobId, setJobId] = useState<string | null>(null)
  const [status, setStatus] = useState<"idle" | "processing" | "completed" | "failed">("idle")
  const [result, setResult] = useState<string | null>(null)

  // 1. Send the claim to FastAPI to start the job
  const handleStartResearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!claim.trim()) return

    setStatus("processing")
    setResult(null)

    try {
      const response = await axios.post('http://localhost:8000/api/fact-check', {
        claim: claim
      })
      setJobId(response.data.job_id) // Save the ID so we can track it
    } catch (error) {
      console.error("Failed to start:", error)
      setStatus("failed")
      setResult("Could not connect to the TruthGuard backend.")
    }
  }

  // 2. The "Polling" Loop: Check the status every 2 seconds
  useEffect(() => {
    let pollInterval: ReturnType<typeof setInterval>;

    if (jobId && status === 'processing') {
      pollInterval = setInterval(async () => {
        try {
          const response = await axios.get(`http://localhost:8000/api/status/${jobId}`)
          const data = response.data

          if (data.status === 'completed') {
            setStatus("completed")
            setResult(data.result)
            clearInterval(pollInterval) // Stop asking!
          } else if (data.status === 'failed') {
            setStatus("failed")
            setResult(data.error)
            clearInterval(pollInterval) // Stop asking!
          }
        } catch (error) {
          console.error("Polling error:", error)
        }
      }, 2000) // 2000 milliseconds = 2 seconds
    }

    // Cleanup interval if component unmounts
    return () => clearInterval(pollInterval)
  }, [jobId, status])

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '40px', fontFamily: 'system-ui' }}>
      <h1>TruthGuard AI 🛡️</h1>
      <p>Enter a claim below to unleash the multi-agent fact-checking crew.</p>

      {/* The Input Form */}
      <form onSubmit={handleStartResearch} style={{ display: 'flex', gap: '10px', marginBottom: '30px' }}>
        <input 
          type="text" 
          value={claim}
          onChange={(e) => setClaim(e.target.value)}
          placeholder="e.g., Did the Eiffel Tower fall down today?"
          style={{ flex: 1, padding: '12px', borderRadius: '6px', border: '1px solid #ccc' }}
          disabled={status === "processing"}
        />
        <button 
          type="submit" 
          disabled={status === "processing" || !claim}
          style={{ padding: '12px 24px', backgroundColor: '#0066cc', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}
        >
          {status === "processing" ? "Researching..." : "Verify Claim"}
        </button>
      </form>

      {/* The Status / Loading Area */}
      {status === "processing" && (
        <div style={{ padding: '20px', backgroundColor: '#fff3cd', borderRadius: '8px', color: '#856404' }}>
          <strong>⏳ Agents are currently researching...</strong>
          <p style={{ fontSize: '14px', margin: '5px 0 0 0' }}>Job ID: {jobId}</p>
        </div>
      )}

      {/* The Results Area */}
      {status === "completed" && result && (
        <div style={{ padding: '20px', backgroundColor: '#d4edda', borderRadius: '8px', border: '1px solid #c3e6cb' }}>
          <h3 style={{ color: '#155724', marginTop: 0 }}>Verdict Received:</h3>
          <div style={{ whiteSpace: 'pre-wrap', color: '#155724' }}>{result}</div>
        </div>
      )}

      {/* The Error Area */}
      {status === "failed" && (
        <div style={{ padding: '20px', backgroundColor: '#f8d7da', borderRadius: '8px', color: '#721c24' }}>
          <strong>❌ Something went wrong:</strong>
          <p>{result}</p>
        </div>
      )}
    </div>
  )
}

export default App
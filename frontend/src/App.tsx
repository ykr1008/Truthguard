import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [claim, setClaim] = useState("")
  const [jobId, setJobId] = useState<string | null>(null)
  const [status, setStatus] = useState<"idle" | "processing" | "completed" | "failed">("idle")
  const [result, setResult] = useState<string | null>(null)
  
  // NEW: State for our agents' thoughts
  const [thoughts, setThoughts] = useState<string[]>([])
  const [showThoughts, setShowThoughts] = useState(false)
  const thoughtsEndRef = useRef<HTMLDivElement>(null)

  // NEW: Auto-scroll the thoughts window to the bottom as new ones arrive
  useEffect(() => {
    if (showThoughts && thoughtsEndRef.current) {
      thoughtsEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [thoughts, showThoughts])

  const handleStartResearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!claim.trim()) return

    setStatus("processing")
    setResult(null)
    setThoughts([]) // Clear old thoughts
    setShowThoughts(true) // Auto-open the thinking box on new run

    try {
      const response = await axios.post('http://localhost:8000/api/fact-check', {
        claim: claim
      })
      setJobId(response.data.job_id)
    } catch (error) {
      console.error("Failed to start:", error)
      setStatus("failed")
      setResult("Could not connect to the TruthGuard backend.")
    }
  }

  // The Upgraded Polling Loop
  useEffect(() => {
    let pollInterval: ReturnType<typeof setInterval>;

    if (jobId && status === 'processing') {
      pollInterval = setInterval(async () => {
        try {
          // 1. Check Status
          const statusRes = await axios.get(`http://localhost:8000/api/status/${jobId}`)
          const statusData = statusRes.data

          // 2. Fetch the latest Thoughts!
          const thoughtsRes = await axios.get(`http://localhost:8000/api/thoughts/${jobId}`)
          setThoughts(thoughtsRes.data.thoughts || [])

          if (statusData.status === 'completed') {
            setStatus("completed")
            setResult(statusData.result)
            clearInterval(pollInterval)
          } else if (statusData.status === 'failed') {
            setStatus("failed")
            setResult(statusData.error)
            clearInterval(pollInterval)
          }
        } catch (error) {
          console.error("Polling error:", error)
        }
      }, 2000)
    }

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
          placeholder="e.g., Are the pyramids older than the woolly mammoth?"
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

      {/* --- NEW: The "Show Thinking" UI --- */}
      {(status === "processing" || thoughts.length > 0) && (
        <div style={{ marginBottom: '20px' }}>
          <button 
            onClick={() => setShowThoughts(!showThoughts)}
            style={{ padding: '8px 16px', backgroundColor: '#e2e8f0', border: 'none', borderRadius: '4px', cursor: 'pointer', marginBottom: '10px', fontSize: '14px' }}
          >
            {showThoughts ? '▼ Hide Agent Thinking' : '▶ Show Agent Thinking'}
          </button>

          {showThoughts && (
            <div style={{ 
              backgroundColor: '#1e293b', 
              color: '#10b981', 
              padding: '15px', 
              borderRadius: '8px', 
              fontFamily: 'monospace', 
              fontSize: '13px',
              maxHeight: '300px',
              overflowY: 'auto',
              whiteSpace: 'pre-wrap',
              boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.5)'
            }}>
              {thoughts.length === 0 ? "Waking up agents..." : thoughts.map((t, index) => (
                <div key={index} style={{ marginBottom: '10px', borderBottom: '1px solid #334155', paddingBottom: '10px' }}>
                  {t}
                </div>
              ))}
              {status === "processing" && <div style={{ color: '#94a3b8', fontStyle: 'italic' }}>Agents are thinking... ⏳</div>}
              <div ref={thoughtsEndRef} />
            </div>
          )}
        </div>
      )}

      {/* The Results Area */}
      {status === "completed" && result && (
        <div style={{ padding: '20px', backgroundColor: '#d4edda', borderRadius: '8px', border: '1px solid #c3e6cb' }}>
          <h3 style={{ color: '#155724', marginTop: 0 }}>Final Editor's Report:</h3>
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
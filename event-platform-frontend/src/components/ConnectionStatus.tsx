"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { checkBackendStatus } from "../services/api"

const ConnectionStatus: React.FC = () => {
  const [isConnected, setIsConnected] = useState<boolean | null>(null)
  const [isChecking, setIsChecking] = useState(true)

  useEffect(() => {
    const checkConnection = async () => {
      setIsChecking(true)
      const connected = await checkBackendStatus()
      setIsConnected(connected)
      setIsChecking(false)
    }

    checkConnection()

    // Check connection every 30 seconds
    const interval = setInterval(checkConnection, 30000)

    return () => clearInterval(interval)
  }, [])

  if (isChecking) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded-md mb-4">
        <div className="flex items-center">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-yellow-600 mr-2"></div>
          Checking backend connection...
        </div>
      </div>
    )
  }

  if (isConnected === false) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-md mb-4">
        <div className="flex items-center justify-between">
          <div>
            <strong>❌ Backend Not Connected</strong>
            <p className="text-sm mt-1">Cannot connect to the API server at http://localhost:8080</p>
            <p className="text-sm mt-1">
              Please make sure your backend is running: <code className="bg-red-100 px-1 rounded">python main.py</code>
            </p>
          </div>
          <button
            onClick={() => window.location.reload()}
            className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  if (isConnected === true) {
    return (
      <div className="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded-md mb-4">
        <div className="flex items-center">
          <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
          <strong>✅ Backend Connected</strong>
          <span className="text-sm ml-2">(http://localhost:8080)</span>
        </div>
      </div>
    )
  }

  return null
}

export default ConnectionStatus

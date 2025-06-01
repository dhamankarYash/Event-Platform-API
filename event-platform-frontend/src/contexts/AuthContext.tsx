"use client"

import type React from "react"
import { createContext, useContext, useState, useEffect, type ReactNode } from "react"
import type { User, LoginCredentials, SignupData } from "../types"
import { authApi, testConnection } from "../services/api"

interface AuthContextType {
  user: User | null
  userRole: string | null
  login: (credentials: LoginCredentials) => Promise<void>
  signup: (userData: SignupData) => Promise<void>
  creatorSignup: (userData: SignupData & { creator_code: string }) => Promise<void>
  logout: () => void
  isLoading: boolean
  backendConnected: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}

interface AuthProviderProps {
  children: ReactNode
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [userRole, setUserRole] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [backendConnected, setBackendConnected] = useState(false)

  useEffect(() => {
    const initializeAuth = async () => {
      // Test backend connection first
      const connected = await testConnection()
      setBackendConnected(connected)

      if (!connected) {
        console.error("❌ Backend not connected!")
        setIsLoading(false)
        return
      }

      // Check for existing token
      const token = localStorage.getItem("token")
      const storedRole = localStorage.getItem("userRole")

      if (token && storedRole) {
        try {
          const userData = await authApi.getCurrentUser()
          setUser(userData)
          setUserRole(storedRole)
          console.log("✅ User authenticated:", userData)
        } catch (error) {
          console.error("❌ Token validation failed:", error)
          // Clear invalid token
          localStorage.removeItem("token")
          localStorage.removeItem("userRole")
          localStorage.removeItem("userId")
          localStorage.removeItem("userName")
        }
      }

      setIsLoading(false)
    }

    initializeAuth()
  }, [])

  const login = async (credentials: LoginCredentials) => {
    try {
      const response = await authApi.login(credentials)

      // Store token and user info
      localStorage.setItem("token", response.access_token)
      localStorage.setItem("userRole", response.user_role)
      localStorage.setItem("userId", response.user_id.toString())
      localStorage.setItem("userName", response.user_name)

      // Get full user data
      const userData = await authApi.getCurrentUser()
      setUser(userData)
      setUserRole(response.user_role)

      console.log("✅ Login successful:", userData)
    } catch (error) {
      console.error("❌ Login failed:", error)
      throw error
    }
  }

  const signup = async (userData: SignupData) => {
    try {
      await authApi.signup(userData)
      console.log("✅ User signup successful")
    } catch (error) {
      console.error("❌ User signup failed:", error)
      throw error
    }
  }

  const creatorSignup = async (userData: SignupData & { creator_code: string }) => {
    try {
      await authApi.creatorSignup(userData)
      console.log("✅ Creator signup successful")
    } catch (error) {
      console.error("❌ Creator signup failed:", error)
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem("token")
    localStorage.removeItem("userRole")
    localStorage.removeItem("userId")
    localStorage.removeItem("userName")
    setUser(null)
    setUserRole(null)
    console.log("✅ Logout successful")
  }

  const value = {
    user,
    userRole,
    login,
    signup,
    creatorSignup,
    logout,
    isLoading,
    backendConnected,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

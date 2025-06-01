import axios from "axios"
import type { User, Event, PaginatedEvents, LoginCredentials, SignupData, Token, EventRegistration } from "../types"

// IMPORTANT: Make sure this matches your backend port
const API_BASE_URL = "http://localhost:8080"

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 second timeout
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token")
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle auth errors and log responses
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Success: ${response.config.method?.toUpperCase()} ${response.config.url}`, response.data)
    return response
  },
  (error) => {
    console.error(
      `❌ API Error: ${error.config?.method?.toUpperCase()} ${error.config?.url}`,
      error.response?.data || error.message,
    )

    if (error.response?.status === 401) {
      localStorage.removeItem("token")
      localStorage.removeItem("userRole")
      localStorage.removeItem("userId")
      localStorage.removeItem("userName")
      window.location.href = "/login"
    }
    return Promise.reject(error)
  },
)

// Test API connection
export const testConnection = async () => {
  try {
    const response = await api.get("/")
    console.log("🔗 API Connection Test:", response.data)
    return true
  } catch (error) {
    console.error("🔗 API Connection Failed:", error)
    return false
  }
}

// Auth API
export const authApi = {
  // Regular user signup
  signup: async (userData: SignupData): Promise<User> => {
    const response = await api.post("/auth/signup", userData)
    return response.data
  },

  // Creator signup (requires creator code)
  creatorSignup: async (userData: SignupData & { creator_code: string }): Promise<User> => {
    const response = await api.post("/auth/creator-signup", userData)
    return response.data
  },

  // Universal login
  login: async (credentials: LoginCredentials): Promise<Token> => {
    const response = await api.post("/auth/login", credentials)
    return response.data
  },

  // Get current user info
  getCurrentUser: async (): Promise<User> => {
    const response = await api.get("/auth/me")
    return response.data
  },
}

// Events API
export const eventApi = {
  // Get events (public endpoint)
  getEvents: async (params: {
    skip?: number
    limit?: number
    search?: string
    location?: string
  }): Promise<PaginatedEvents> => {
    const response = await api.get("/events", { params })
    return response.data
  },

  // Get single event (public endpoint)
  getEvent: async (id: number): Promise<Event> => {
    const response = await api.get(`/events/${id}`)
    return response.data
  },

  // Create event (creators only)
  createEvent: async (eventData: {
    name: string
    description: string
    location: string
    date_time: string
    capacity: number
  }): Promise<Event> => {
    const response = await api.post("/events", eventData)
    return response.data
  },

  // Update event (creators only - own events)
  updateEvent: async (
    id: number,
    eventData: {
      name?: string
      description?: string
      location?: string
      date_time?: string
      capacity?: number
    },
  ): Promise<Event> => {
    const response = await api.put(`/events/${id}`, eventData)
    return response.data
  },

  // Delete event (creators only - own events)
  deleteEvent: async (id: number): Promise<void> => {
    await api.delete(`/events/${id}`)
  },

  // Register for event (users only)
  registerForEvent: async (id: number): Promise<EventRegistration> => {
    const response = await api.post(`/events/${id}/register`)
    return response.data
  },

  // Unregister from event (users only)
  unregisterFromEvent: async (id: number): Promise<void> => {
    await api.delete(`/events/${id}/register`)
  },

  // Get user's registrations (users only)
  getMyRegistrations: async (): Promise<EventRegistration[]> => {
    const response = await api.get("/my-registrations")
    return response.data
  },

  // Get creator's events (creators only)
  getMyEvents: async (): Promise<Event[]> => {
    const response = await api.get("/my-events")
    return response.data
  },
}

// Admin API (admin only)
export const adminApi = {
  getStats: async () => {
    const response = await api.get("/admin/stats")
    return response.data
  },
}

// Utility function to check if backend is running
export const checkBackendStatus = async (): Promise<boolean> => {
  try {
    await api.get("/health")
    return true
  } catch (error) {
    return false
  }
}

export interface User {
  id: number
  email: string
  full_name: string
  role: "user" | "creator" | "admin"
  is_active: boolean
  created_at: string
}

export interface Event {
  id: number
  name: string
  description: string
  location: string
  date_time: string
  capacity: number
  registered_count: number
  created_by: number
  creator_name: string
  created_at: string
  is_registered?: boolean
  can_edit?: boolean
  can_delete?: boolean
}

export interface EventRegistration {
  id: number
  user_id: number
  event_id: number
  registered_at: string
}

export interface PaginatedEvents {
  events: Event[]
  total: number
  skip: number
  limit: number
  has_next: boolean
  has_prev: boolean
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface SignupData {
  email: string
  password: string
  full_name: string
}

export interface Token {
  access_token: string
  token_type: string
  user_role: string
  user_id: number
  user_name: string
}

"use client"

import type React from "react"
import { useParams, useNavigate } from "react-router-dom"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { Calendar, MapPin, Users, Clock, ArrowLeft } from "lucide-react"
import { eventApi } from "../services/api"
import { useAuth } from "../contexts/AuthContext"
import LoadingSpinner from "../components/LoadingSpinner"

const EventDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { user } = useAuth()
  const queryClient = useQueryClient()

  const {
    data: event,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["event", id],
    queryFn: () => eventApi.getEvent(Number(id)),
    enabled: !!id,
  })

  const registerMutation = useMutation({
    mutationFn: () => eventApi.registerForEvent(Number(id)),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["event", id] })
    },
  })

  const unregisterMutation = useMutation({
    mutationFn: () => eventApi.unregisterFromEvent(Number(id)),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["event", id] })
    },
  })

  const handleRegister = () => {
    if (!user) {
      navigate("/login")
      return
    }
    registerMutation.mutate()
  }

  const handleUnregister = () => {
    unregisterMutation.mutate()
  }

  if (isLoading) return <LoadingSpinner />
  if (error || !event) return <div className="text-center py-8 text-red-600">Event not found</div>

  const isEventFull = event.registered_count >= event.capacity
  const registrationPercentage = (event.registered_count / event.capacity) * 100

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back Button */}
      <button
        onClick={() => navigate(-1)}
        className="flex items-center text-gray-600 hover:text-gray-900 mb-6 transition-colors"
      >
        <ArrowLeft className="h-5 w-5 mr-2" />
        Back to Events
      </button>

      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        {/* Event Image */}
        <img src="/placeholder.svg?height=400&width=800" alt={event.name} className="w-full h-64 object-cover" />

        <div className="p-8">
          {/* Event Header */}
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">{event.name}</h1>
            <p className="text-lg text-gray-600">{event.description}</p>
          </div>

          {/* Event Details */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="space-y-4">
              <div className="flex items-center text-gray-700">
                <Calendar className="h-5 w-5 mr-3 text-blue-600" />
                <div>
                  <p className="font-medium">Date & Time</p>
                  <p className="text-sm">
                    {new Date(event.date_time).toLocaleDateString("en-US", {
                      weekday: "long",
                      year: "numeric",
                      month: "long",
                      day: "numeric",
                    })}
                  </p>
                  <p className="text-sm">
                    {new Date(event.date_time).toLocaleTimeString("en-US", {
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </p>
                </div>
              </div>

              <div className="flex items-center text-gray-700">
                <MapPin className="h-5 w-5 mr-3 text-blue-600" />
                <div>
                  <p className="font-medium">Location</p>
                  <p className="text-sm">{event.location}</p>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex items-center text-gray-700">
                <Users className="h-5 w-5 mr-3 text-blue-600" />
                <div>
                  <p className="font-medium">Capacity</p>
                  <p className="text-sm">
                    {event.registered_count} / {event.capacity} registered
                  </p>
                </div>
              </div>

              <div className="flex items-center text-gray-700">
                <Clock className="h-5 w-5 mr-3 text-blue-600" />
                <div>
                  <p className="font-medium">Created</p>
                  <p className="text-sm">{new Date(event.created_at).toLocaleDateString("en-US")}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Registration Progress */}
          <div className="mb-8">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-gray-700">Registration Progress</span>
              <span className="text-sm text-gray-500">{Math.round(registrationPercentage)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className={`h-3 rounded-full transition-all duration-300 ${
                  registrationPercentage >= 90
                    ? "bg-red-500"
                    : registrationPercentage >= 70
                      ? "bg-yellow-500"
                      : "bg-blue-600"
                }`}
                style={{ width: `${registrationPercentage}%` }}
              ></div>
            </div>
          </div>

          {/* Registration Button */}
          <div className="flex justify-center">
            {!user ? (
              <button
                onClick={() => navigate("/login")}
                className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-md font-medium transition-colors"
              >
                Login to Register
              </button>
            ) : event.is_registered ? (
              <button
                onClick={handleUnregister}
                disabled={unregisterMutation.isPending}
                className="bg-red-600 hover:bg-red-700 text-white px-8 py-3 rounded-md font-medium transition-colors disabled:opacity-50"
              >
                {unregisterMutation.isPending ? "Unregistering..." : "Unregister"}
              </button>
            ) : isEventFull ? (
              <button disabled className="bg-gray-400 text-white px-8 py-3 rounded-md font-medium cursor-not-allowed">
                Event Full
              </button>
            ) : (
              <button
                onClick={handleRegister}
                disabled={registerMutation.isPending}
                className="bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-md font-medium transition-colors disabled:opacity-50"
              >
                {registerMutation.isPending ? "Registering..." : "Register for Event"}
              </button>
            )}
          </div>

          {/* Error Messages */}
          {registerMutation.error && (
            <div className="mt-4 bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md text-sm text-center">
              Failed to register for event
            </div>
          )}
          {unregisterMutation.error && (
            <div className="mt-4 bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md text-sm text-center">
              Failed to unregister from event
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default EventDetailPage

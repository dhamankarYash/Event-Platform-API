"use client"

import type React from "react"
import { useQuery } from "@tanstack/react-query"
import { Calendar, Users, Plus, MapPin } from "lucide-react"
import { Link } from "react-router-dom"
import { eventApi } from "../services/api"
import { useAuth } from "../contexts/AuthContext"
import LoadingSpinner from "../components/LoadingSpinner"

const DashboardPage: React.FC = () => {
  const { user } = useAuth()

  const { data: myEvents, isLoading: eventsLoading } = useQuery({
    queryKey: ["myEvents"],
    queryFn: eventApi.getMyEvents,
  })

  const { data: myRegistrations, isLoading: registrationsLoading } = useQuery({
    queryKey: ["myRegistrations"],
    queryFn: eventApi.getMyRegistrations,
  })

  if (eventsLoading || registrationsLoading) return <LoadingSpinner />

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Welcome back, {user?.full_name}!</h1>
        <p className="text-lg text-gray-600 mt-2">Manage your events and registrations</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-blue-100">
              <Calendar className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Events Created</p>
              <p className="text-2xl font-bold text-gray-900">{myEvents?.length || 0}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-green-100">
              <Users className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Events Registered</p>
              <p className="text-2xl font-bold text-gray-900">{myRegistrations?.length || 0}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-purple-100">
              <MapPin className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Total Attendees</p>
              <p className="text-2xl font-bold text-gray-900">
                {myEvents?.reduce((sum, event) => sum + event.registered_count, 0) || 0}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* My Events */}
        <div className="bg-white rounded-lg shadow-md">
          <div className="p-6 border-b border-gray-200">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold text-gray-900">My Events</h2>
              <Link
                to="/create-event"
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center space-x-2 transition-colors"
              >
                <Plus className="h-4 w-4" />
                <span>Create Event</span>
              </Link>
            </div>
          </div>
          <div className="p-6">
            {myEvents && myEvents.length > 0 ? (
              <div className="space-y-4">
                {myEvents.slice(0, 3).map((event) => (
                  <div key={event.id} className="border border-gray-200 rounded-lg p-4">
                    <h3 className="font-medium text-gray-900 mb-2">{event.name}</h3>
                    <div className="flex items-center text-sm text-gray-500 mb-2">
                      <Calendar className="h-4 w-4 mr-2" />
                      {new Date(event.date_time).toLocaleDateString()}
                    </div>
                    <div className="flex items-center text-sm text-gray-500 mb-2">
                      <Users className="h-4 w-4 mr-2" />
                      {event.registered_count} / {event.capacity} registered
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full"
                        style={{
                          width: `${(event.registered_count / event.capacity) * 100}%`,
                        }}
                      ></div>
                    </div>
                  </div>
                ))}
                {myEvents.length > 3 && (
                  <p className="text-sm text-gray-500 text-center">And {myEvents.length - 3} more events...</p>
                )}
              </div>
            ) : (
              <div className="text-center py-8">
                <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500 mb-4">You haven't created any events yet</p>
                <Link
                  to="/create-event"
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Create Your First Event
                </Link>
              </div>
            )}
          </div>
        </div>

        {/* My Registrations */}
        <div className="bg-white rounded-lg shadow-md">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">My Registrations</h2>
          </div>
          <div className="p-6">
            {myRegistrations && myRegistrations.length > 0 ? (
              <div className="space-y-4">
                {myRegistrations.slice(0, 3).map((registration) => (
                  <div key={registration.id} className="border border-gray-200 rounded-lg p-4">
                    <p className="text-sm text-gray-500 mb-2">
                      Registered on {new Date(registration.registered_at).toLocaleDateString()}
                    </p>
                    <Link
                      to={`/events/${registration.event_id}`}
                      className="text-blue-600 hover:text-blue-800 font-medium"
                    >
                      View Event Details →
                    </Link>
                  </div>
                ))}
                {myRegistrations.length > 3 && (
                  <p className="text-sm text-gray-500 text-center">
                    And {myRegistrations.length - 3} more registrations...
                  </p>
                )}
              </div>
            ) : (
              <div className="text-center py-8">
                <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500 mb-4">You haven't registered for any events yet</p>
                <Link
                  to="/events"
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Browse Events
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default DashboardPage

import React, { useState } from 'react'

// Dummy data for submitted classes
const dummyClasses = [
  {
    id: 1,
    subject: 'Data Structures',
    venue: 'Room 101',
    date: '2024-01-15',
    time: '09:00'
  },
  {
    id: 2,
    subject: 'Algorithms',
    venue: 'Lab 205',
    date: '2024-01-15',
    time: '11:00'
  },
  {
    id: 3,
    subject: 'Database Systems',
    venue: 'Room 302',
    date: '2024-01-16',
    time: '14:00'
  }
]

function CRPanel() {
  const [formData, setFormData] = useState({
    subject: '',
    venue: '',
    date: '',
    time: ''
  })
  const [classes, setClasses] = useState(dummyClasses)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    // In a real app, this would submit to a backend
    console.log('Form submitted:', formData)
    alert('Class submitted! (This is just a prototype)')
    
    // Reset form
    setFormData({
      subject: '',
      venue: '',
      date: '',
      time: ''
    })
  }

  return (
    <div className="space-y-8">
      {/* Form Section */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Submit New Class</h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="subject" className="block text-sm font-medium text-gray-700 mb-1">
                Subject
              </label>
              <input
                type="text"
                id="subject"
                name="subject"
                value={formData.subject}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter subject name"
              />
            </div>
            
            <div>
              <label htmlFor="venue" className="block text-sm font-medium text-gray-700 mb-1">
                Venue
              </label>
              <input
                type="text"
                id="venue"
                name="venue"
                value={formData.venue}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter venue/room"
              />
            </div>
            
            <div>
              <label htmlFor="date" className="block text-sm font-medium text-gray-700 mb-1">
                Date
              </label>
              <input
                type="date"
                id="date"
                name="date"
                value={formData.date}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            
            <div>
              <label htmlFor="time" className="block text-sm font-medium text-gray-700 mb-1">
                Time
              </label>
              <input
                type="time"
                id="time"
                name="time"
                value={formData.time}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
          
          <div className="pt-4">
            <button
              type="submit"
              className="w-full md:w-auto px-6 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
            >
              Submit Class
            </button>
          </div>
        </form>
      </div>

      {/* Submitted Classes List */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Submitted Classes</h2>
        
        {classes.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No classes submitted yet.</p>
        ) : (
          <div className="space-y-4">
            {classes.map((classItem) => (
              <div key={classItem.id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-medium text-gray-900">{classItem.subject}</h3>
                    <div className="mt-1 text-sm text-gray-600">
                      <span className="inline-flex items-center">
                        📍 {classItem.venue}
                      </span>
                      <span className="mx-2">•</span>
                      <span className="inline-flex items-center">
                        📅 {new Date(classItem.date).toLocaleDateString()}
                      </span>
                      <span className="mx-2">•</span>
                      <span className="inline-flex items-center">
                        🕐 {classItem.time}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default CRPanel


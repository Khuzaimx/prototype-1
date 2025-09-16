import React from 'react'

// Dummy data for today's classes
const todaysClasses = [
  {
    id: 1,
    subject: 'Data Structures',
    venue: 'Room 101',
    time: '09:00'
  },
  {
    id: 2,
    subject: 'Algorithms',
    venue: 'Lab 205',
    time: '11:00'
  },
  {
    id: 3,
    subject: 'Web Development',
    venue: 'Room 203',
    time: '14:00'
  },
  {
    id: 4,
    subject: 'Machine Learning',
    venue: 'Lab 301',
    time: '16:00'
  }
]

function StudentPanel() {
  const getCurrentTime = () => {
    return new Date().toLocaleTimeString('en-US', { 
      hour12: false, 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  const getTimeUntilClass = (classTime) => {
    const now = new Date()
    const [hours, minutes] = classTime.split(':')
    const classDateTime = new Date()
    classDateTime.setHours(parseInt(hours), parseInt(minutes), 0, 0)
    
    const diffMs = classDateTime - now
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
    const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60))
    
    if (diffMs < 0) {
      return 'Class has ended'
    } else if (diffHours > 0) {
      return `${diffHours}h ${diffMinutes}m until class`
    } else {
      return `${diffMinutes}m until class`
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
          <h2 className="text-xl font-semibold text-gray-900">Today's Classes</h2>
          <div className="mt-2 sm:mt-0 text-sm text-gray-600">
            Current time: <span className="font-medium">{getCurrentTime()}</span>
          </div>
        </div>
      </div>

      {/* Classes List */}
      <div className="space-y-4">
        {todaysClasses.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-8 text-center">
            <p className="text-gray-500 text-lg">No classes scheduled for today!</p>
            <p className="text-gray-400 text-sm mt-2">Enjoy your free time! 🎉</p>
          </div>
        ) : (
          todaysClasses.map((classItem) => (
            <div key={classItem.id} className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow">
              <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{classItem.subject}</h3>
                  
                  <div className="flex flex-col sm:flex-row sm:items-center text-sm text-gray-600 space-y-1 sm:space-y-0 sm:space-x-4">
                    <span className="inline-flex items-center">
                      📍 {classItem.venue}
                    </span>
                    <span className="inline-flex items-center">
                      🕐 {classItem.time}
                    </span>
                  </div>
                  
                  <div className="mt-3 text-sm text-gray-500">
                    {getTimeUntilClass(classItem.time)}
                  </div>
                </div>
                
                <div className="mt-4 sm:mt-0 sm:ml-6">
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 text-center">
                    <div className="text-blue-600 text-sm font-medium">
                      ⏰ Alarm set 20 minutes before class
                    </div>
                    <div className="text-blue-500 text-xs mt-1">
                      {(() => {
                        const [hours, minutes] = classItem.time.split(':')
                        const alarmTime = new Date()
                        alarmTime.setHours(parseInt(hours), parseInt(minutes) - 20, 0, 0)
                        return `Alarm at ${alarmTime.toLocaleTimeString('en-US', { 
                          hour12: false, 
                          hour: '2-digit', 
                          minute: '2-digit' 
                        })}`
                      })()}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Summary */}
      {todaysClasses.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Today's Summary</h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="text-2xl font-bold text-gray-900">{todaysClasses.length}</div>
              <div className="text-sm text-gray-600">Total Classes</div>
            </div>
            <div className="bg-green-50 rounded-lg p-4">
              <div className="text-2xl font-bold text-green-600">
                {todaysClasses.filter(c => {
                  const [hours, minutes] = c.time.split(':')
                  const classTime = new Date()
                  classTime.setHours(parseInt(hours), parseInt(minutes), 0, 0)
                  return classTime > new Date()
                }).length}
              </div>
              <div className="text-sm text-green-600">Upcoming</div>
            </div>
            <div className="bg-blue-50 rounded-lg p-4">
              <div className="text-2xl font-bold text-blue-600">
                {todaysClasses.filter(c => {
                  const [hours, minutes] = c.time.split(':')
                  const classTime = new Date()
                  classTime.setHours(parseInt(hours), parseInt(minutes), 0, 0)
                  const alarmTime = new Date(classTime.getTime() - 20 * 60 * 1000)
                  return alarmTime > new Date() && classTime > new Date()
                }).length}
              </div>
              <div className="text-sm text-blue-600">Alarms Set</div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default StudentPanel


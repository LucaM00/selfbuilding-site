import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import LiveAgentConsole from './components/LiveAgentConsole'
import { Globe, Users, Bot, Lightbulb } from 'lucide-react'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('home')

  const renderContent = () => {
    switch (activeTab) {
      case 'console':
        return <LiveAgentConsole />
      case 'community':
        return (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5" />
                Community Input
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">Community input features coming soon...</p>
            </CardContent>
          </Card>
        )
      default:
        return (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Globe className="h-5 w-5" />
                  Self-Building Site
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-lg text-gray-700 mb-4">
                  Welcome to the Self-Building Site - an autonomous, self-improving multi-agent system 
                  devoted to long-term, humanity-benefitting projects.
                </p>
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="p-4 border rounded-lg">
                    <h3 className="font-semibold mb-2 flex items-center gap-2">
                      <Bot className="h-4 w-4" />
                      Autonomous Agents
                    </h3>
                    <p className="text-sm text-gray-600">
                      Our multi-agent system continuously designs, builds, tests, and deploys improvements.
                    </p>
                  </div>
                  <div className="p-4 border rounded-lg">
                    <h3 className="font-semibold mb-2 flex items-center gap-2">
                      <Lightbulb className="h-4 w-4" />
                      Community Driven
                    </h3>
                    <p className="text-sm text-gray-600">
                      Major changes are subject to community voting and input collection.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        )
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">Self-Building Site</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Button
                variant={activeTab === 'home' ? 'default' : 'ghost'}
                onClick={() => setActiveTab('home')}
              >
                Home
              </Button>
              <Button
                variant={activeTab === 'console' ? 'default' : 'ghost'}
                onClick={() => setActiveTab('console')}
              >
                Live Console
              </Button>
              <Button
                variant={activeTab === 'community' ? 'default' : 'ghost'}
                onClick={() => setActiveTab('community')}
              >
                Community
              </Button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        {renderContent()}
      </main>
    </div>
  )
}

export default App

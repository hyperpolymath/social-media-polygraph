import { Link } from 'react-router-dom'
import { Shield, Search, BarChart3, Clock, CheckCircle, AlertTriangle } from 'lucide-react'

export default function HomePage() {
  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-600 to-primary-800 text-white py-20">
        <div className="container">
          <div className="max-w-3xl">
            <h1 className="text-5xl font-bold mb-6">
              Verify Social Media Claims with AI
            </h1>
            <p className="text-xl text-primary-100 mb-8">
              Combat misinformation with our AI-powered fact-checking system.
              Analyze claims, verify sources, and get reliable verdicts in seconds.
            </p>
            <div className="flex gap-4">
              <Link
                to="/verify"
                className="btn bg-white text-primary-700 hover:bg-gray-100 px-8 py-3 text-lg"
              >
                <Search className="mr-2 h-5 w-5" />
                Verify a Claim
              </Link>
              <Link
                to="/about"
                className="btn border-2 border-white text-white hover:bg-white hover:text-primary-700 px-8 py-3 text-lg"
              >
                Learn More
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16">
        <div className="container">
          <h2 className="text-3xl font-bold text-center mb-12">
            How It Works
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="card text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Search className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Submit Claims</h3>
              <p className="text-gray-600">
                Paste text, URLs, or social media posts you want to verify
              </p>
            </div>

            <div className="card text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <BarChart3 className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">AI Analysis</h3>
              <p className="text-gray-600">
                Our AI analyzes claims using NLP, fact-checking databases, and source credibility
              </p>
            </div>

            <div className="card text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Shield className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Get Results</h3>
              <p className="text-gray-600">
                Receive detailed verification results with sources and credibility scores
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Key Features */}
      <section className="py-16 bg-gray-100">
        <div className="container">
          <h2 className="text-3xl font-bold text-center mb-12">
            Key Features
          </h2>
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <div className="flex items-start space-x-4">
              <CheckCircle className="h-6 w-6 text-success mt-1 flex-shrink-0" />
              <div>
                <h3 className="font-semibold text-lg mb-1">Multi-Source Verification</h3>
                <p className="text-gray-600">
                  Cross-reference claims with multiple fact-checking services and databases
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <Clock className="h-6 w-6 text-primary-600 mt-1 flex-shrink-0" />
              <div>
                <h3 className="font-semibold text-lg mb-1">Temporal Tracking</h3>
                <p className="text-gray-600">
                  Track how claim verifications change over time
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <BarChart3 className="h-6 w-6 text-primary-600 mt-1 flex-shrink-0" />
              <div>
                <h3 className="font-semibold text-lg mb-1">Credibility Scoring</h3>
                <p className="text-gray-600">
                  Advanced algorithms evaluate source reliability and claim credibility
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <AlertTriangle className="h-6 w-6 text-warning mt-1 flex-shrink-0" />
              <div>
                <h3 className="font-semibold text-lg mb-1">Bias Detection</h3>
                <p className="text-gray-600">
                  Identify potential bias and sentiment in claims
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16">
        <div className="container">
          <div className="bg-primary-600 rounded-2xl p-12 text-center text-white">
            <h2 className="text-3xl font-bold mb-4">
              Ready to Fight Misinformation?
            </h2>
            <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
              Start verifying claims now and help create a more informed digital community
            </p>
            <Link
              to="/verify"
              className="btn bg-white text-primary-700 hover:bg-gray-100 px-8 py-3 text-lg inline-flex items-center"
            >
              <Search className="mr-2 h-5 w-5" />
              Verify Your First Claim
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}

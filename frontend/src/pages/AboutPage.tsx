import { Shield, Zap, Lock, Globe } from 'lucide-react'

export default function AboutPage() {
  return (
    <div className="container py-12">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-6">About Social Media Polygraph</h1>

        <div className="prose max-w-none mb-12">
          <p className="text-xl text-gray-600 mb-6">
            Social Media Polygraph is an AI-powered fact-checking platform designed to
            combat misinformation and help users verify the truthfulness of claims shared
            on social media.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-12">
          <div className="card">
            <Shield className="h-10 w-10 text-primary-600 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Our Mission</h3>
            <p className="text-gray-600">
              To empower users with the tools they need to identify misinformation,
              verify claims, and make informed decisions about the content they consume
              and share.
            </p>
          </div>

          <div className="card">
            <Zap className="h-10 w-10 text-primary-600 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Advanced Technology</h3>
            <p className="text-gray-600">
              We use state-of-the-art NLP, machine learning, and integration with
              multiple fact-checking databases to provide accurate, reliable
              verification results.
            </p>
          </div>

          <div className="card">
            <Lock className="h-10 w-10 text-primary-600 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Privacy First</h3>
            <p className="text-gray-600">
              We respect your privacy and handle all data responsibly. Claims are
              processed securely, and we never sell or share your information.
            </p>
          </div>

          <div className="card">
            <Globe className="h-10 w-10 text-primary-600 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Open & Transparent</h3>
            <p className="text-gray-600">
              Our verification process is transparent, showing sources and reasoning
              behind each verdict. We believe in open, auditable fact-checking.
            </p>
          </div>
        </div>

        <div className="card bg-gray-50">
          <h2 className="text-2xl font-bold mb-4">How We Verify Claims</h2>
          <div className="space-y-4">
            <div className="flex items-start">
              <div className="flex-shrink-0 w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center font-semibold mr-4">
                1
              </div>
              <div>
                <h4 className="font-semibold mb-1">Natural Language Processing</h4>
                <p className="text-gray-600">
                  We extract entities, analyze sentiment, and identify key claims using
                  advanced NLP techniques.
                </p>
              </div>
            </div>

            <div className="flex items-start">
              <div className="flex-shrink-0 w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center font-semibold mr-4">
                2
              </div>
              <div>
                <h4 className="font-semibold mb-1">Fact-Checking Database Query</h4>
                <p className="text-gray-600">
                  We search multiple reputable fact-checking services and databases for
                  related claims and verifications.
                </p>
              </div>
            </div>

            <div className="flex items-start">
              <div className="flex-shrink-0 w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center font-semibold mr-4">
                3
              </div>
              <div>
                <h4 className="font-semibold mb-1">Source Credibility Analysis</h4>
                <p className="text-gray-600">
                  We evaluate the credibility and historical accuracy of sources to
                  provide context.
                </p>
              </div>
            </div>

            <div className="flex items-start">
              <div className="flex-shrink-0 w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center font-semibold mr-4">
                4
              </div>
              <div>
                <h4 className="font-semibold mb-1">Aggregation & Scoring</h4>
                <p className="text-gray-600">
                  We combine all signals using our credibility scoring algorithm to
                  produce a final verdict with confidence scores.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-12 card border-2 border-primary-600">
          <h2 className="text-2xl font-bold mb-4">Technology Stack</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-semibold mb-2">Backend</h4>
              <ul className="text-gray-600 space-y-1">
                <li>• Python with FastAPI</li>
                <li>• ArangoDB (Multi-model database)</li>
                <li>• XTDB (Temporal data tracking)</li>
                <li>• Dragonfly (High-performance cache)</li>
                <li>• spaCy & Transformers (NLP)</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-2">Frontend</h4>
              <ul className="text-gray-600 space-y-1">
                <li>• React with TypeScript</li>
                <li>• TailwindCSS</li>
                <li>• React Query</li>
                <li>• Vite build system</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

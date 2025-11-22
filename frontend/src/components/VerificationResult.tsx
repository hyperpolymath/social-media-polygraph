import { Link } from 'react-router-dom'
import {
  CheckCircle,
  XCircle,
  AlertTriangle,
  Info,
  ExternalLink,
  Clock,
  TrendingUp,
} from 'lucide-react'
import type { ClaimAnalysis } from '@/types'

interface Props {
  analysis: ClaimAnalysis
  processingTime: number
  claimId: string
}

export default function VerificationResult({ analysis, processingTime, claimId }: Props) {
  const { claim, verification } = analysis

  const getVerdictColor = (verdict: string) => {
    switch (verdict) {
      case 'true':
        return 'success'
      case 'mostly_true':
        return 'success'
      case 'mixed':
        return 'warning'
      case 'mostly_false':
        return 'danger'
      case 'false':
        return 'danger'
      default:
        return 'gray'
    }
  }

  const getVerdictIcon = (verdict: string) => {
    switch (verdict) {
      case 'true':
      case 'mostly_true':
        return <CheckCircle className="h-12 w-12" />
      case 'false':
      case 'mostly_false':
        return <XCircle className="h-12 w-12" />
      case 'mixed':
        return <AlertTriangle className="h-12 w-12" />
      default:
        return <Info className="h-12 w-12" />
    }
  }

  const getVerdictLabel = (verdict: string) => {
    return verdict
      .split('_')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }

  const color = getVerdictColor(verification.verdict)

  return (
    <div className="space-y-6">
      {/* Verdict Card */}
      <div className={`card border-2 border-${color}`}>
        <div className="flex items-start justify-between mb-6">
          <div className="flex items-start space-x-4">
            <div className={`text-${color}`}>
              {getVerdictIcon(verification.verdict)}
            </div>
            <div>
              <h2 className="text-2xl font-bold mb-2">
                {getVerdictLabel(verification.verdict)}
              </h2>
              <div className="flex items-center space-x-4 text-sm text-gray-600">
                <span className="flex items-center">
                  <TrendingUp className="h-4 w-4 mr-1" />
                  Confidence: {(verification.confidence * 100).toFixed(0)}%
                </span>
                {verification.credibility_score && (
                  <span className="flex items-center">
                    Credibility: {(verification.credibility_score * 100).toFixed(0)}%
                  </span>
                )}
                <span className="flex items-center">
                  <Clock className="h-4 w-4 mr-1" />
                  {processingTime.toFixed(2)}s
                </span>
              </div>
            </div>
          </div>
          <Link
            to={`/claim/${claimId}`}
            className="btn-secondary text-sm"
          >
            View Details
          </Link>
        </div>

        <div className="prose max-w-none">
          <p className="text-gray-700 leading-relaxed">
            {verification.explanation}
          </p>
        </div>
      </div>

      {/* Claim Details */}
      <div className="card">
        <h3 className="text-lg font-semibold mb-4">Claim Details</h3>
        <div className="bg-gray-50 rounded-lg p-4 mb-4">
          <p className="text-gray-900">{claim.text}</p>
        </div>
        {claim.url && (
          <a
            href={claim.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-primary-600 hover:text-primary-700 text-sm flex items-center"
          >
            <ExternalLink className="h-4 w-4 mr-1" />
            View Source
          </a>
        )}
      </div>

      {/* Fact Checks */}
      {verification.fact_checks.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Fact Check Sources</h3>
          <div className="space-y-3">
            {verification.fact_checks.map((fc, index) => (
              <div
                key={index}
                className="border border-gray-200 rounded-lg p-4"
              >
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <div className="font-medium text-gray-900">{fc.source}</div>
                    <div className="text-sm text-gray-600">
                      Verdict: {getVerdictLabel(fc.verdict)}
                    </div>
                  </div>
                  {fc.url && (
                    <a
                      href={fc.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary-600 hover:text-primary-700"
                    >
                      <ExternalLink className="h-4 w-4" />
                    </a>
                  )}
                </div>
                {fc.explanation && (
                  <p className="text-sm text-gray-700">{fc.explanation}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Entities */}
      {verification.entities.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Extracted Entities</h3>
          <div className="flex flex-wrap gap-2">
            {verification.entities.map((entity, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm"
              >
                {entity}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Sentiment */}
      {verification.sentiment && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Sentiment Analysis</h3>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <div className="text-sm text-gray-600 mb-1">Classification</div>
              <div className="font-medium capitalize">
                {verification.sentiment.classification}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600 mb-1">Polarity</div>
              <div className="font-medium">
                {verification.sentiment.polarity.toFixed(2)}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600 mb-1">Subjectivity</div>
              <div className="font-medium">
                {verification.sentiment.subjectivity.toFixed(2)}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

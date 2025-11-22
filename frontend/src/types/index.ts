export interface Claim {
  id: string
  text: string
  url?: string
  platform?: string
  author?: string
  text_hash: string
  created_at: string
  updated_at: string
  status: string
  metadata?: Record<string, any>
}

export interface VerificationResult {
  verdict: 'true' | 'mostly_true' | 'mixed' | 'mostly_false' | 'false' | 'unverifiable'
  confidence: number
  explanation: string
  sources: Array<{
    source: string
    url?: string
    rating?: number
  }>
  fact_checks: Array<{
    source: string
    verdict: string
    rating: number
    explanation?: string
    url?: string
  }>
  entities: string[]
  sentiment?: {
    polarity: number
    subjectivity: number
    classification: string
  }
  credibility_score?: number
  checked_at: string
}

export interface ClaimAnalysis {
  claim: Claim
  verification: VerificationResult
  temporal_history?: Array<{
    verified_at: string
    verdict: string
    confidence: number
    credibility_score: number
  }>
}

export interface ClaimResponse {
  success: boolean
  claim_id: string
  analysis?: ClaimAnalysis
  error?: string
  processing_time: number
}

export interface ClaimCreate {
  text: string
  url?: string
  platform?: string
  author?: string
  metadata?: Record<string, any>
}

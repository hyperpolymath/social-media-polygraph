import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Loader2, AlertCircle } from 'lucide-react'
import { claimsApi } from '@/services/api'
import VerificationResult from '@/components/VerificationResult'

export default function ClaimDetailPage() {
  const { id } = useParams<{ id: string }>()

  const { data, isLoading, error } = useQuery({
    queryKey: ['claim', id],
    queryFn: () => claimsApi.getClaim(id!),
    enabled: !!id,
  })

  if (isLoading) {
    return (
      <div className="container py-12">
        <div className="flex flex-col items-center justify-center min-h-[400px]">
          <Loader2 className="h-12 w-12 animate-spin text-primary-600 mb-4" />
          <p className="text-gray-600">Loading claim analysis...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container py-12">
        <div className="max-w-2xl mx-auto">
          <div className="card border-2 border-danger">
            <div className="flex items-start">
              <AlertCircle className="h-6 w-6 text-danger mr-3 mt-1" />
              <div>
                <h2 className="text-lg font-semibold text-danger mb-2">
                  Error Loading Claim
                </h2>
                <p className="text-gray-700">
                  {error instanceof Error
                    ? error.message
                    : 'Failed to load claim analysis'}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (!data) {
    return null
  }

  return (
    <div className="container py-12">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Claim Analysis</h1>
        <VerificationResult
          analysis={data}
          processingTime={0}
          claimId={id!}
        />
      </div>
    </div>
  )
}

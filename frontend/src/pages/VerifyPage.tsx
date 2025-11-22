import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { Search, Loader2, AlertCircle } from 'lucide-react'
import { claimsApi } from '@/services/api'
import type { ClaimCreate } from '@/types'
import VerificationResult from '@/components/VerificationResult'

interface FormData extends ClaimCreate {}

export default function VerifyPage() {
  const navigate = useNavigate()
  const [showResult, setShowResult] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>()

  const mutation = useMutation({
    mutationFn: claimsApi.verifyClaim,
    onSuccess: () => {
      setShowResult(true)
    },
  })

  const onSubmit = (data: FormData) => {
    setShowResult(false)
    mutation.mutate(data)
  }

  return (
    <div className="container py-12">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">Verify a Claim</h1>
          <p className="text-xl text-gray-600">
            Submit a social media claim for fact-checking and credibility analysis
          </p>
        </div>

        {/* Form */}
        <div className="card mb-8">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Claim Text */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Claim Text *
              </label>
              <textarea
                {...register('text', {
                  required: 'Please enter a claim to verify',
                  minLength: {
                    value: 10,
                    message: 'Claim must be at least 10 characters',
                  },
                })}
                className="textarea"
                rows={4}
                placeholder="Enter the claim you want to verify..."
              />
              {errors.text && (
                <p className="mt-1 text-sm text-danger flex items-center">
                  <AlertCircle className="h-4 w-4 mr-1" />
                  {errors.text.message}
                </p>
              )}
            </div>

            {/* Optional Fields */}
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Source URL (optional)
                </label>
                <input
                  {...register('url')}
                  type="url"
                  className="input"
                  placeholder="https://example.com/post"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Platform (optional)
                </label>
                <select {...register('platform')} className="input">
                  <option value="">Select platform...</option>
                  <option value="twitter">Twitter/X</option>
                  <option value="facebook">Facebook</option>
                  <option value="instagram">Instagram</option>
                  <option value="tiktok">TikTok</option>
                  <option value="reddit">Reddit</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Author (optional)
              </label>
              <input
                {...register('author')}
                type="text"
                className="input"
                placeholder="@username or Author Name"
              />
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={mutation.isPending}
              className="btn-primary w-full py-3 text-base"
            >
              {mutation.isPending ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Verifying...
                </>
              ) : (
                <>
                  <Search className="mr-2 h-5 w-5" />
                  Verify Claim
                </>
              )}
            </button>
          </form>
        </div>

        {/* Error */}
        {mutation.isError && (
          <div className="bg-danger-light border border-danger text-danger-dark rounded-lg p-4 mb-8">
            <div className="flex items-start">
              <AlertCircle className="h-5 w-5 mt-0.5 mr-3 flex-shrink-0" />
              <div>
                <h3 className="font-semibold mb-1">Verification Failed</h3>
                <p className="text-sm">
                  {mutation.error instanceof Error
                    ? mutation.error.message
                    : 'An error occurred while verifying the claim'}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Results */}
        {showResult && mutation.data && mutation.data.success && mutation.data.analysis && (
          <VerificationResult
            analysis={mutation.data.analysis}
            processingTime={mutation.data.processing_time}
            claimId={mutation.data.claim_id}
          />
        )}
      </div>
    </div>
  )
}

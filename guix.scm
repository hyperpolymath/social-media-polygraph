; SPDX-License-Identifier: MPL-2.0
;; guix.scm — GNU Guix package definition for social-media-polygraph
;; Usage: guix shell -f guix.scm

(use-modules (guix packages)
             (guix build-system gnu)
             (guix licenses))

(package
  (name "social-media-polygraph")
  (version "0.1.0")
  (source #f)
  (build-system gnu-build-system)
  (synopsis "social-media-polygraph")
  (description "social-media-polygraph — part of the hyperpolymath ecosystem.")
  (home-page "https://github.com/hyperpolymath/social-media-polygraph")
  (license ((@@ (guix licenses) license) "PMPL-1.0-or-later"
             "https://github.com/hyperpolymath/palimpsest-license")))

{
  description = "Social Media Polygraph - Memory-safe, type-safe fact-checking";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    rust-overlay.url = "github:oxalica/rust-overlay";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, rust-overlay, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        overlays = [ (import rust-overlay) ];
        pkgs = import nixpkgs {
          inherit system overlays;
        };
        rustToolchain = pkgs.rust-bin.stable.latest.default.override {
          extensions = [ "rust-src" "rust-analyzer" ];
          targets = [ "wasm32-unknown-unknown" ];
        };
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Rust
            rustToolchain
            cargo-watch
            wasm-pack
            wasm-bindgen-cli

            # Elixir
            elixir
            erlang

            # Deno
            deno

            # ReScript
            nodejs_20

            # Database clients
            arangodb
            redis

            # Tools
            just
            podman
            podman-compose

            # Development
            git
            jq
            curl

            # SSL
            openssl
            pkg-config
          ];

          shellHook = ''
            echo "Social Media Polygraph Development Environment"
            echo "=============================================="
            echo ""
            echo "Available commands:"
            echo "  just --list       # Show all available tasks"
            echo "  cargo build       # Build Rust backend"
            echo "  deno task dev     # Start frontend dev server"
            echo "  mix deps.get      # Get Elixir dependencies"
            echo ""
            echo "Toolchain:"
            echo "  Rust:     $(rustc --version)"
            echo "  Elixir:   $(elixir --version | head -1)"
            echo "  Deno:     $(deno --version | head -1)"
            echo "  Node:     $(node --version)"
            echo ""
          '';

          RUST_SRC_PATH = "${rustToolchain}/lib/rustlib/src/rust/library";
        };

        packages = {
          default = pkgs.rustPlatform.buildRustPackage {
            pname = "polygraph";
            version = "0.2.0";
            src = ./backend;
            cargoLock.lockFile = ./backend/Cargo.lock;

            nativeBuildInputs = with pkgs; [ pkg-config ];
            buildInputs = with pkgs; [ openssl ];

            meta = with pkgs.lib; {
              description = "Social Media Polygraph - AI-powered fact-checking";
              homepage = "https://github.com/hyperpolymath/social-media-polygraph";
              license = with licenses; [ mit ];
            };
          };

          wasm = pkgs.rustPlatform.buildRustPackage {
            pname = "polygraph-wasm";
            version = "0.2.0";
            src = ./backend;
            cargoLock.lockFile = ./backend/Cargo.lock;

            nativeBuildInputs = with pkgs; [ wasm-pack ];

            buildPhase = ''
              wasm-pack build --target web --out-dir pkg
            '';

            installPhase = ''
              mkdir -p $out
              cp -r pkg/* $out/
            '';
          };
        };

        apps.default = flake-utils.lib.mkApp {
          drv = self.packages.${system}.default;
        };
      }
    );
}

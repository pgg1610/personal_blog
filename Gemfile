source "https://rubygems.org"

gem "jekyll", "4.2.2"
gem "jekyll-feed", "~> 0.17"
gem "webrick", "~> 1.8"
gem "csv"

# The macOS system Ruby (2.6) cannot build recent ffi releases, so pin an older
# one there. Netlify runs a newer Ruby and resolves its own compatible version.
# Gemfile.lock stays untracked, so each environment resolves independently.
gem "ffi", "~> 1.15.5" if Gem::Version.new(RUBY_VERSION) < Gem::Version.new("3.0")

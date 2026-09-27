# Adds a short content hash to static asset filenames after the site is
# written, then rewrites references in the generated output. This lets the
# CDN cache assets forever (see netlify.toml) because a change to a file
# produces a new filename. No external gem is required.
require 'digest'

module AssetFingerprint
  EXTENSIONS = %w[css js mjs jpg jpeg png gif svg webp avif ico woff woff2].freeze

  def self.run(site)
    assets_root = File.join(site.dest, 'assets')
    return unless Dir.exist?(assets_root)

    baseurl = site.baseurl.to_s
    mapping = {}

    Dir.glob(File.join(assets_root, '**', '*')).sort.each do |path|
      next unless File.file?(path)

      ext = File.extname(path).delete('.').downcase
      next unless EXTENSIONS.include?(ext)

      relative = path.sub(%r{\A#{Regexp.escape(site.dest)}/}, '')
      digest = Digest::SHA1.file(path).hexdigest[0, 8]
      directory = File.dirname(path)
      new_name = "#{File.basename(path, '.*')}-#{digest}.#{ext}"

      File.rename(path, File.join(directory, new_name))

      new_relative = relative.sub(%r{[^/]+\z}, new_name)
      mapping["#{baseurl}/#{relative}"] = "#{baseurl}/#{new_relative}"
    end

    return if mapping.empty?

    Dir.glob(File.join(site.dest, '**', '*.{html,xml,css,json}')).each do |file|
      content = File.read(file)
      updated = content.dup
      mapping.each { |old_url, new_url| updated.gsub!(old_url, new_url) }
      File.write(file, updated) if updated != content
    end
  end
end

Jekyll::Hooks.register :site, :post_write do |site|
  AssetFingerprint.run(site)
end

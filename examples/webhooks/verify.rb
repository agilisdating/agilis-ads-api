# Verifies an Agilis webhook signature. Usage: AGILIS_WEBHOOK_SECRET=whsec_... AGILIS_SIGNATURE='t=...,v1=...' ruby verify.rb body.json
require "json"
require "openssl"

# raw_body: the request body exactly as received (request.raw_post / request.body.read).
def verify_agilis_webhook(raw_body, header, secret, tolerance = 300)
  parts = header.to_s.split(",").map { |p| p.strip.split("=", 2) }.select { |p| p.size == 2 }
  t = parts.find { |k, _| k == "t" }&.last.to_s
  signatures = parts.select { |k, _| k == "v1" }.map(&:last)
  raise ArgumentError, "Invalid signature header" unless t.match?(/\A\d+\z/) && !signatures.empty?
  expected = OpenSSL::HMAC.hexdigest("SHA256", secret, "#{t}.".b + raw_body.to_s.b)
  raise ArgumentError, "Signature does not match" unless signatures.any? { |s| OpenSSL.secure_compare(expected, s) }
  raise ArgumentError, "Timestamp outside the tolerance" if (Time.now.to_i - t.to_i).abs > tolerance
  JSON.parse(raw_body.to_s.dup.force_encoding(Encoding::UTF_8))
end

if $PROGRAM_NAME == __FILE__
  begin
    event = verify_agilis_webhook(File.binread(ARGV[0]), ENV.fetch("AGILIS_SIGNATURE", ""), ENV.fetch("AGILIS_WEBHOOK_SECRET"))
    puts "verified #{event["type"]}"
  rescue ArgumentError => e
    warn "rejected: #{e.message}"
    exit 1
  end
end

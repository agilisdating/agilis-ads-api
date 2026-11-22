# Checks that every client.<resource>.<method> call in the Ruby examples exists in the SDK.
require "agilis_ads"

client = AgilisAds::Client.new(api_key: "pk_test_00000000000000000000")
missing = []
Dir[File.join(__dir__, "*.rb")].sort.each do |file|
  next if File.basename(file) == File.basename(__FILE__)

  File.read(file).scan(/client\.(\w+)\.(\w+)/).each do |resource, method|
    target = client.public_send(resource)
    missing << "#{File.basename(file)}: client.#{resource}.#{method}" unless target.respond_to?(method)
  end
end
abort("Missing:\n#{missing.join("\n")}") unless missing.empty?
puts "Every Ruby example calls a method the SDK has."

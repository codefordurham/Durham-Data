require 'csv'
require 'pp'
require 'active_support/all'
#require 'geocoder'
require 'colored'
require 'httparty'

csv_path = '../Restaurants/export-converted.csv'
options = { :headers => :first_row, :header_converters => [:symbol, :downcase]}

#Geocoder::Configuration.timeout = 90

restaurants = []

CSV.open(csv_path, "r", options) do |csv|
  csv.each_with_index do |row, index|
    #puts "#{row[:insp_type]}: #{row[:premise_name].titlecase} at #{row[:premise_address1].titlecase}"
    restaurant = row.to_hash
    restaurant[:premise_name_titlecase] = row[:premise_name].titlecase

    address_str = ""
    address_str << " #{row[:premise_address1].titlecase}" unless row[:premise_address1].to_i == 0
    address_str << " #{row[:premise_address2].titlecase}" unless row[:premise_address2].to_i == 0
    address_str << " Durham,"
    address_str << " NC"
    address_str << " #{row[:premise_zip]}" unless row[:premise_zip].nil?

    puts "#{index}: #{address_str.green}"

    #geo_info = Geocoder.search(address_str)[0].data

    geo_info = JSON.parse(HTTParty.get("http://www.datasciencetoolkit.org/maps/api/geocode/json?sensor=false&address=#{CGI::escape(address_str)}").response.body['results'])

    restaurant[:geo_results] = {}
    restaurant[:geo_results] = geo_info

    restaurants << restaurant

    sleep 1

  end
end

File.open("../Restaurants/json/with-location-info/export-data-science.json","w") do |f|
   f.write(restaurants.to_json)
end

puts restaurants.to_json



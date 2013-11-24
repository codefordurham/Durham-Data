require 'pp'
require 'active_support/all'
# require 'colored'
require 'json'

results = JSON.parse(File.read("../Restaurants/json/with-location-info/export-data-science.json"))

geo_json = {
    :type => "FeatureCollection",
    :features => []
  }

food_types = []

results.each_with_index do |location, index|
  puts location['premise_name_titlecase']

  venue = {
    :type => "Feature",
    :id => location['est_id'],
    :geometry => {
      :type => "Point",
      :coordinates => [location['geo_results']['results'][0]['geometry']['location']['lng'], location['geo_results']['results'][0]['geometry']['location']['lat']]
    },
    :properties => location.except!("geo_results")
  }
  # venue = {
  #     :type => "Point",
  #     :coordinates => [location['geo_results']['geometry']['location']['lng'], location['geo_results']['geometry']['location']['lat']]
  #   }

  geo_json[:features] << venue
end

pp geo_json.to_json

File.open("../Restaurants/json/geo-json/food-geojson.json","w") do |f|
  f.write(geo_json.to_json)
end
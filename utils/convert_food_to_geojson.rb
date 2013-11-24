require 'pp'
require 'active_support/all'
require 'colored'
require 'json'

results = JSON.parse(File.read("../Restaurants/json/with-location-info/export-data-science.json"))

geo_json = {
    :type => "FeatureCollection",
    :features => []
  }

food_types = []

results.each_with_index do |location, index|
  print location['premise_name_titlecase']

  unless location['transitional_type_desc'].downcase == "food"
    print " is not food \n".red
    next
  end

  description = "<strong>Score:</strong> #{location['final_score_sum']}"
  description << "<br><strong>Comments:</strong> #{location['comments']}" unless location['comments'].nil?

  venue = {
    :type => "Feature",
    :id => location['est_id'],
    :geometry => {
      :type => "Point",
      :coordinates => [location['geo_results']['results'][0]['geometry']['location']['lng'], location['geo_results']['results'][0]['geometry']['location']['lat']]
    },
    :properties => {
      :title => location['premise_name_titlecase'],
      :description => description
    }
  }

  marker_properties = {
      :'marker-color' => '#3698d4', # change color based on rating at some point?
      :'marker-size' => "large",
      :'marker-symbol' => "restaurant"
    }

  venue[:properties].merge!(marker_properties)

  geo_json[:features] << venue
end

pp geo_json.to_json

File.open("../Restaurants/json/geo-json/food-geojson.json","w") do |f|
  f.write(geo_json.to_json)
end
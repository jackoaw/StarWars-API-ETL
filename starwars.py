import requests
import json

PEOPLE_API_ENDPOINT = "https://swapi.dev/api/people/"
SPECIES_API_ENDPOINT = "http://swapi.dev/api/species"
HTTPBIN_API_ENDPOINT = "http://httpbin.org/post"
# curl -X POST "http://httpbin.org/post" -H "accept: application/json"

# Generic method for pulling from the Star Wars API when there are multiple pages
def pullAPIpages(api_endpoint):
	api_list = []
	current_page = 1
	# Go through all the pages to get all the people
	while True:
		response = requests.get(url = "%s?page=%i"%(api_endpoint, current_page))
		# After the last page, you will typically get a 404, if so, you're done.
		if response.status_code is not 200:
			break
		api_list += json.loads(response.content)["results"]
		current_page += 1

	return api_list


# Will return the whole species list
def getSpecies():
	# return json.loads(requests.get(url = SPECIES_API_ENDPOINT).content)["results"]
	return pullAPIpages(SPECIES_API_ENDPOINT)


# Will return the list of all people
def getPeople():
	return pullAPIpages(PEOPLE_API_ENDPOINT)


# Will return the species by the url and the list given
def getSpeciesIndex(url, species_list):
	# Check to see if unidentified
	if not len(url):
		return ""
	# Get the end of the URL
	split_url = url[0].split("/")
	# Subtrace one from index, to adjust for index of an array 
	index = int(split_url[len(split_url)-2]) - 1
	return species_list[index]["name"]


def postToHttpbin(csv):
	return requests.post(url=HTTPBIN_API_ENDPOINT, data=csv)


def main():
	# First get the initial data
	people_list = getPeople()

	# Then find the 10 most popular people, you can just sort the list in descending order and take the first 10
	# Another way to do this is while getting the people from the api, do an insertion, sorting that new entry 
	# by how many movies they appear in.
	popular_list = sorted(people_list, key=lambda person: len(person["films"]), reverse=True)[:10]

	# Next do a descending sort to order those popular characters from tallest to shortest
	height_ordered_list = sorted(popular_list, key=lambda person: int(person["height"]), reverse=True)

	csv_str = "" 

	# API calls are the most expenisve operation here (bottleneck), it is better to get all pages at once as opposed to 10
	species_list = getSpecies()

	# Next we will form a CSV from the height ordered people_json
	for person in height_ordered_list:
		csv_str += "%s,%s,%s,%s\n" %(person["name"], getSpeciesIndex(person["species"], species_list), person["height"], len(person["films"]))

	print(csv_str)

	# Last, we will post the results to httpbin
	if postToHttpbin(csv_str).status_code == 200:
		print("CSV posted to httpbin successfully")
	else:
		print("CSV posting to httbin failed")




if __name__ == "__main__":
    main()

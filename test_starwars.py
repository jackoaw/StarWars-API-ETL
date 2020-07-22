import starwars
import json


def test_getSpecies():
	results = starwars.getSpecies()
	# Checks to make sure thre are still valid entries
	check_list = ['name', 'classification', 'people']
	for result in results:
		for check in check_list:
			if check not in result:
				assert False

	# Will then check the actual contents
	f = open('species.json', 'r')
	assert f.read() == str(results)


def test_getSpeciesIndex():
	results = starwars.getSpecies()

	# We can test out two known ones
	# R2-D2: Droid
	assert "Droid" == starwars.getSpeciesIndex(["http://swapi.dev/api/species/2/"], results)
	# Chewbaka : Wookie
	assert "Wookie" == starwars.getSpeciesIndex(["http://swapi.dev/api/species/3/"], results)


def test_getPeople():
	people_list = starwars.getPeople()
	check_list = ["name", "films", "species", "height"]
	for person in people_list:
		for check in check_list:
			if check not in person:
				assert False

	f = open('people.json', 'r')
	assert f.read() == str(people_list)


def test_postToHttpbin():
	sample_csv = "Andrew Chuba,Wookie,165,0\nDarth Vader,,202,4"
	http_result = starwars.postToHttpbin(sample_csv)
	assert http_result.status_code == 200
	content = json.loads(http_result.content)
	assert int(content["headers"]["Content-Length"]) == len(sample_csv)
	assert content["data"] == "Andrew Chuba,Wookie,165,0\nDarth Vader,,202,4"


from bs4 import BeautifulSoup
import unittest
import requests

#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their requirements, and what you need to understand. Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!


######### PART 0 #########

# Write your code for Part 0 here.

# cache file
try:
	newmantaylor_data = open("newmantaylor_data.html","r").text
except:
	newmantaylor_data = requests.get("http://newmantaylor.com/gallery.html").text
	f = open("newmantaylor_data.html","w")
	f.write(newmantaylor_data)
	f.close()

soup = BeautifulSoup(newmantaylor_data, 'html.parser')

img_list = soup.find_all("img")
#print(img_list)

for x in img_list:
	try:
		print(x['alt'])
	except:
		print("No alternative text provided!")


######### PART 1 #########

# Get the main page data...

# Try to get and cache main page data if not yet cached
# Result of a following try/except block should be that
# there exists a file nps_gov_data.html,
# and the html text saved in it is stored in a variable 
# that the rest of the program can access.

# We've provided comments to guide you through the complex try/except, but if you prefer to build up the code to do this scraping and caching yourself, that is OK.

baseurl = "https://www.nps.gov/"
state_list = ['','Arkansas','California','Michigan']
file_names = ['nps_gov_data','arkansas_data','california_data','michigan_data']

# get state data
for i in range(len(file_names)):
	try:
		soup = BeautifulSoup(open(file_names[i] + ".html", "r"),'html.parser')
		print("Successfully found cache for %s" % file_names[i])
	except:
		soup = BeautifulSoup(requests.get(baseurl + "/index.html").text,'html.parser')

		# if there's a state in the state_list, then go to another page		
		if state_list != '':
			div_one = soup.find('ul',{'class':'dropdown-menu SearchBar-keywordSearch'})
			list_points = div_one.find_all('li')
			for p in list_points:
				if p.text in state_list:
					soup = BeautifulSoup(requests.get(baseurl + p.find('a')['href']).text,'html.parser')

		f = open(file_names[i] + ".html", "w")
		f.write(soup.encode('ascii','replace'))
		f.close()
		print("Downloaded %s data from internet" % (file_names[i]))


######### PART 2 #########

## Before truly embarking on Part 2, we recommend you do a few things:

# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects. What data do you have about each state? How is it organized in HTML?

# HINT: remember the method .prettify() on a BeautifulSoup object -- might be useful for your investigation! So, of course, might be .find or .find_all, etc...

# HINT: Remember that the data you saved is data that includes ALL of the parks/sites/etc in a certain state, but you want the class to represent just ONE park/site/monument/lakeshore.

# We have provided, in sample_html_of_park.html an HTML file that represents the HTML about 1 park. However, your code should rely upon HTML data about Michigan, Arkansas, and Califoria you saved and accessed in Part 1.

# However, to begin your investigation and begin to plan your class definition, you may want to open this file and create a BeautifulSoup instance of it to do investigation on.

# Remember that there are things you'll have to be careful about listed in the instructions -- e.g. if no type of park/site/monument is listed in input, one of your instance variables should have a None value...

################### TEST MATERIAL ####################

sample_link = BeautifulSoup(requests.get("https://www.nps.gov/isro/index.htm").text,'html.parser')
######################################################


## Define your class NationalSite here:
class NationalSite(object):
	def __init__(self,data):
		self.data = data
		self.location = data.find('span',{'class':'Hero-location'}).text
		self.name = data.find('a',{'class':'Hero-title'}).text
		self.type = data.find('span',{'class':'Hero-designation'}).text
		self.description = data.find('div',{'class':'Component text-content-size text-content-style'}).find('p').text

	def __str__(self):
		return "{} | {}".format(self.name, self.location)

	# Remember to test this code for a park with no address
	def get_mailing_address(self):
		mailing_site = self.data.find('div',{'class':'UtilityNav','id':'UtilityNav'}).find('li').find('a')['href']
		mail_soup_data = BeautifulSoup(requests.get(baseurl + mailing_site).text,'html.parser')
		
		try:
			div_one = mail_soup_data.find('div',{'class':'mailing-address'})
			street_address = div_one.find('span',{'itemprop':'streetAddress'}).text.strip()
			locality = div_one.find('span',{'itemprop':'addressLocality'}).text.strip()
			state = div_one.find('span',{'itemprop':'addressRegion'}).text.strip()
			postal_code = div_one.find('span',{'itemprop':'postalCode'}).text.strip()

			address_list = [street_address, locality, state, postal_code]

			return " / ".join(address_list)
		except:
			return ""

	def __contains__(self, var):
		return var in self.get_mailing_address()


# create sample instance
test = NationalSite(sample_link)

# test mailing address
print(test.get_mailing_address())

# Test contains method
print("Yosemite" in test)




######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.




##Code to help you test these out:
# for p in california_natl_sites:
# 	print(p)
# for a in arkansas_natl_sites:
# 	print(a)
# for m in michigan_natl_sites:
# 	print(m)



######### PART 4 #########

## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your data make take a minute or few to run -- so it's a good idea to test any methods/functions you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that may occur, you might run into some problems and have to debug for where you need to put in some None value / error handling!


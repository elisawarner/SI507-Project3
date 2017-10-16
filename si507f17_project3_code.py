from bs4 import BeautifulSoup
import unittest
import requests
import csv

#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their requirements, and what you need to understand. Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!


######### PART 0 #########

# Write your code for Part 0 here.

print("**************** PART 0 ******************\n")

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

print("**************** PART 1 ******************\n")

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

# get state data or check if there's a cache

def get_data(state, file_name='', notice=False):
	if notice:
		print("Looking for a cache...")
	
	try:
		soup = BeautifulSoup(open(file_name + ".html", "r"),'html.parser')
		if notice:
			print("Successfully found a cache for %s" % file_name)
		return soup
	except:
		raw_data = requests.get(baseurl + "/index.html").text
		soup = BeautifulSoup(raw_data,'html.parser')

		# if there's a state in the state_list, then go to another page		
		if file_name != '':
			div_one = soup.find('ul',{'class':'dropdown-menu SearchBar-keywordSearch'})
			list_points = div_one.find_all('li')
			for p in list_points:
				if p.text in state:
					raw_data = requests.get(baseurl + p.find('a')['href']).text

		f = open(file_name + ".html", "w")
		f.write(raw_data)
		f.close()
		
		if notice:
			print("Downloaded %s data from internet" % (file_names[i]))
		
		return BeautifulSoup(raw_data,'html.parser')


for i in range(len(file_names)):
	get_data(state_list[i], file_names[i], notice=True)


######### PART 2 #########

print("**************** PART 2 ******************\n")

## Before truly embarking on Part 2, we recommend you do a few things:

# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects. What data do you have about each state? How is it organized in HTML?

# HINT: remember the method .prettify() on a BeautifulSoup object -- might be useful for your investigation! So, of course, might be .find or .find_all, etc...

# HINT: Remember that the data you saved is data that includes ALL of the parks/sites/etc in a certain state, but you want the class to represent just ONE park/site/monument/lakeshore.

# We have provided, in sample_html_of_park.html an HTML file that represents the HTML about 1 park. However, your code should rely upon HTML data about Michigan, Arkansas, and Califoria you saved and accessed in Part 1.

# However, to begin your investigation and begin to plan your class definition, you may want to open this file and create a BeautifulSoup instance of it to do investigation on.

# Remember that there are things you'll have to be careful about listed in the instructions -- e.g. if no type of park/site/monument is listed in input, one of your instance variables should have a None value...


## Define your class NationalSite here:
class NationalSite(object):
	def __init__(self,data):
		self.data = data
		self.name = data.find('h3').text
		self.location = data.find('h4').text
		self.type = data.find('h2').text
		self.description = data.find('p').text.strip()

	def __str__(self):
		return "{} | {}".format(self.name, self.location)

	# Remember to test this code for a park with no address
	def get_mailing_address(self):

		for li in self.data.find_all('ul'):
			if 'Basic' in li.text.split() and 'Information' in li.text.split():
				mailing_site = li.find('a')['href']
			else:
				return ""

		mail_soup_data = BeautifulSoup(requests.get(mailing_site).text,'html.parser')

		try:
			div_one = mail_soup_data.find('div',{'class':'mailing-address'})
			street_address = div_one.find('span',{'itemprop':'streetAddress'}).text.strip()
			locality = div_one.find('span',{'itemprop':'addressLocality'}).text.strip()
			state = div_one.find('span',{'itemprop':'addressRegion'}).text.strip()
			postal_code = div_one.find('span',{'itemprop':'postalCode'}).text.strip()

			address_list = [self.name, street_address, locality, state, postal_code]

			return " / ".join(address_list)
		except:
			return ""

	def __contains__(self, var):
		return var in self.get_mailing_address()



################### TEST MATERIAL ####################
f = open("sample_html_of_park.html",'r')
soup_park_inst = BeautifulSoup(f.read(), 'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
sample_inst = NationalSite(soup_park_inst)
f.close()

print(sample_inst.get_mailing_address())
######################################################


######### PART 3 #########

print("**************** PART 3 ******************\n")

# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.

michigan_natl_sites = [NationalSite(x) for x in get_data('Michigan', 'michigan').find_all(lambda tag: tag.name == 'li' and tag.get('class') == ['clearfix'])]
california_natl_sites = [NationalSite(x) for x in get_data('California','california').find_all(lambda tag: tag.name == 'li' and tag.get('class') == ['clearfix'])]
arkansas_natl_sites = [NationalSite(x) for x in get_data('Arkansas','arkansas').find_all(lambda tag: tag.name == 'li' and tag.get('class') == ['clearfix'])]

print([x.name for x in california_natl_sites])
	
##Code to help you test these out:
#for p in california_natl_sites:
# 	print(p)
#for a in arkansas_natl_sites:
# 	print(a)
#for m in michigan_natl_sites:
#	print(m)
#	break


######### PART 4 #########

print("**************** PART 4 ******************\n")

## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your data make take a minute or few to run -- so it's a good idea to test any methods/functions you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that may occur, you might run into some problems and have to debug for where you need to put in some None value / error handling!

#title_list = [x.lower() for x in state_list[1:]]

def export_data(state, sites_list):
	fhnd = open(state + '.csv','w')

	fhnd.write('Name,Location,Address,Description\n')
	outfile = csv.writer(fhnd, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

	for inst in sites_list:
		outfile.writerow([inst.name, inst.location, inst.get_mailing_address(), inst.description])

	fhnd.close()


print("Exporting Michigan Data...")
export_data('michigan', michigan_natl_sites)
print("Exporting California Data...")
export_data('california', california_natl_sites)
print("Exporting Arkansas Data...")
export_data('arkansas', arkansas_natl_sites)

print("Done")


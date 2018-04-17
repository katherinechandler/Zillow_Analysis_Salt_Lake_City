
import zillow


slc_zip_codes = [84101, 84102, 84103, 84104, 84105, 84106, 84107, 84108, 84109, 84111, 84112, 84113, 84114, 
				84115, 84116, 84117, 84118, 84119, 84120, 84121, 84123, 84124, 84128, 84129, 84133, 84138, 84180]


all_zip_code_listings = []

for zipcode in slc_zip_codes:

	print ("Fetching data for %s" % (zipcode))
	listings_in_zipcode = zillow.parse(zipcode)
	all_zip_code_listings.extend(listings_in_zipcode)

print ("Writing data to output file")
zillow.out_to_file('slc_active_listings', all_zip_code_listings)


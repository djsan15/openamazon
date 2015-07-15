WHAT IT IS
__________
This is a simple python library to crawl data from "Amazon.in"

WHAT ALL INFORMATION IT RETRIEVES
_________________________________
Current version(0.1) has the following functionality-
1) Search- It will get the Name, Price and Product URL for any search term.
2) Product Search- It will return the MRP(not the selling price), rating, description, no. of reviews and no. of images 	for any product.
3) Sellers- It will return the list of sellers for any product along with the offered price for each seller.


HOW IT WORKS
____________
Following is a sample code that describes the usage of this library-

   To get the SEARCH RESULTS: 
```
	from openamazon.openamazon import amazon
	
	object=amazon()
	results= object.search("soap")
	for product in results:
		print product['name']	#This will print the product name
		print product['price']	#This will print the current price
		print product['url']	#This will print the product url
		print product['reference_code']	#This will print the unique amazon reference code
```
 Note- It will return first 16 results.

   To get the product details:
```
	result=object.product_details(product['url'])  #pass the product url fetched in search results
	print result['mrp']	#This will print the MRP(not current selling price)
	print result['reviews']	#This will print the No. of reviews
	print result['images']	#This will print the No. of images
	print result['rating']	#This will print the rating
	print result['description']	#This will print the description
```
   To get the list of SELLERS:
```
	sellers=object.offer_listing(product['url'])  #pass the product url fetched in search results
	for seller in sellers:
		print seller['seller']	#This will print the Seller Name
		print seller['price']	#This will print the current price offered by that seller
```
 Note- This method might take some time depending upon the number of sellers as it opens multiple URLs.
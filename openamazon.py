# This is not a crawler for amazon.in which has been created by Sanchit Sokhey.
# He do not own any rights in amazon.in and there is no legal permission taken for crawling there website.

from urllib2 import urlopen
from bs4 import BeautifulSoup
import tablib
from urlparse import urlparse

base_url="http://www.amazon.in/s/ref=nb_sb_noss?url=search-alias=aps&field-keywords="
class amazon:
	max_attempts=0
	def __init__(self):
		pass

	def product_details(self,url):
		print "AMAZON...product details"
		product={}
		html=urlopen(url).read()
		soup=BeautifulSoup(html,"lxml")

		r1= soup.find(id="price")
		r2= r1.table.find_all("tr")
		mrp= r2[0].find_all("td")[1].text.strip()
		r3= soup.find(id="averageCustomerReviews")
		if(r3.find(id="acrPopover")):
			rating= r3.find(id="acrPopover")['title'].strip()[0]
		else:
			rating="0"
		if(r3.find(id="acrCustomerReviewText")):
			reviews= r3.find(id="acrCustomerReviewText").text.strip()[:-17]
		elif(r3.find(id="acrCustomerWriteReviewText")):
			reviews="0"
		else:
			reviews="not available"
		if(soup.find(id="altImages")):
			images=len(soup.find(id="altImages").find_all("li",{"class":"a-spacing-small item"}))
		else:
			images=0
		if(soup.find(id="productDescription")):
			description=soup.find(id="productDescription").find("div",{"class":"productDescriptionWrapper"}).text.strip()
		else:
			description="Not Available"
		product['mrp']=mrp
		product['reviews']=reviews
		product['images']=images
		product['rating']=rating
		product['description']=description
		print "....Done"
		return product	

	def search(self,keyword):
		try:
			pages=1
			num_of_results=pages*16
			search_results=[]
			html=urlopen(base_url+keyword+"&page="+str(pages)).read()
			soup=BeautifulSoup(html,"lxml")
			for x in range(0,num_of_results):
				s_res={}
				res_obj=soup.find(id="result_"+str(x))
				r1=res_obj.find("div",{"class":"a-fixed-left-grid-col a-col-right"})
				if(r1):
					name=r1.find("div").a.h2.text.strip()
					link=str(r1.find("div").a['href'].strip())
					ref_link=urlparse(link).path.split('/')[3]
					price=r1.find_all("div",recursive=False)[1].find_all("div",recursive=False)[0].find_all("div",recursive=False)[0].a.span.text.strip()
					s_res['name'] = name
					s_res['url']=link
					s_res['reference_code']=ref_link
					s_res['price']=price
					search_results.append(s_res)
			return search_results
		except AttributeError:
			pass

	def get_seller_name(self,link):
		while(True):
			try:
				html=urlopen(link).read()
				soup=BeautifulSoup(html,"lxml")
				r1=soup.find("div",{"id":"s-result-info-bar-content"})
				name=r1.div.div.h2.span.span.text.strip()
				return name
			except Exception:
				pass
			else:
				break

	def offer_listing(self,url):
		ref_link=urlparse(url).path.split('/')[3]
		ol_url='http://www.amazon.in/gp/offer-listing/'
		offers=[]
		soup=None
		print "AMAZON...offer listing"
		while(True):
			try:
				html=urlopen(ol_url+ref_link).read()
				soup=BeautifulSoup(html,"lxml")
			except Exception,e:
				print "Fetching Again: "+ str(e)
			else:
				break
		r1=soup.find_all("div",{"class":"a-row a-spacing-mini olpOffer"})
		for x in range(0,len(r1)):
			r2=r1[x].find("div",{"class":"a-column a-span2"})
			price=r2.span.span.text.strip()
			r3=r1[x].find("div",{"class":"a-column a-span2 olpSellerColumn"})
			if(not r3.p.a.text):
				seller_link=r3.p.a['href']
				seller_name=self.get_seller_name(seller_link)
				seller_name= seller_name.strip()[:-11]
			else:
				seller_name= r3.p.a.text
			print price,seller_name
			offer={}
			offer['seller']=seller_name
			offer['price']=price[4:]
			offers.append(offer)
		self.max_attempts=0
		print "....Done"
		return offers


	



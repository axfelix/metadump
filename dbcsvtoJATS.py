import csv
import sys
import re
import string
import xml.etree.cElementTree as ET
from django.utils.encoding import smart_str

rownum = 0
with open(sys.argv[1]) as dbcsv:
	csvreader = csv.reader(dbcsv, delimiter=',')
	for row in csvreader:
		rownum += 1
		if 1 < rownum < 1500:
			try:
				article = ET.Element("article")
				article.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
				article.set("article-type", "research-article")
				front = ET.SubElement(article, "front")

				journalmeta = ET.SubElement(front, "journal-meta")
				journaltitle = ET.SubElement(journalmeta, "journal-title")
				journaltitle.text = row[4].encode('utf-8')

				articlemeta = ET.SubElement(front, "article-meta")
				titlegroup = ET.SubElement(articlemeta, "title-group")
				articletitle = ET.SubElement(titlegroup, "article-title")
				articletitle.text = smart_str(row[5]).encode('utf-8')

				contribgroup = ET.SubElement(articlemeta, "contrib-group")
				authorlist = row[7].split(";")
				authornumber = 0
				emaillist = row[8].split(";")
				corresplist = row[9].split(";")
				afflist = row[10].split(";")

				contrib = {}
				name = {}
				surname = {}
				givennames = {}
				email = {}
				xref = {}
				aff = {}
				label = {}

				for author in authorlist:
					contrib[author] = ET.SubElement(contribgroup, "contrib")
					if corresplist[authornumber] == 1:
						contrib[author].set("corresp","yes")

					name[author] = ET.SubElement(contrib[author], "name")
					authornames = author.split(",")
					surname[author] = ET.SubElement(name[author], "surname")
					surname[author].text = authornames[0].encode('utf-8')
					givennames[author] = ET.SubElement(name[author], "given-names")
					givennames[author].text = authornames[1].encode('utf-8')

					email[author] = ET.SubElement(contrib[author], "email")
					email[author].text = emaillist[authornumber].encode('utf-8')

					xref[author] = ET.SubElement(contrib[author], "xref")
					xref[author].set("ref-type", "aff")
					xref[author].set("rid", "I"+str(authornumber+1))
					xref[author].text = str(authornumber+1).encode('utf-8')

# this was dying because one record had fewer affiliations listed than authors. not sure if it's an artifact of my SQL query or what, but I have more known-good records than I need, so not going to investigate.
					try:
						aff[author] = ET.SubElement(articlemeta, "aff")
						aff[author].set("id", "I"+str(authornumber+1))
						aff[author].text = afflist[authornumber].encode('utf-8')
						label[author] = ET.SubElement(aff[author], "label")
						label[author].text = str(authornumber+1).encode('utf-8')
					except:
						pass

					authornumber += 1

				pubdate = ET.SubElement(articlemeta, "pub-date")
				pubdate.set("pub-type", "epub")
				year = ET.SubElement(pubdate, "year")
				year.text = row[3].encode('utf-8')

				volume = ET.SubElement(articlemeta, "volume")
				volume.text = row[1]
				issue = ET.SubElement(articlemeta, "issue")
				issue.set("content-type", "volume")
				issue.text = row[2].encode('utf-8')

				abstract = ET.SubElement(articlemeta, "abstract")
				abstract.text = row[6].encode('utf-8')

				tree = ET.ElementTree(article)
				shortpath = re.search('/[0-9]*/.*', row[0])
				filename = re.sub('\/', '-', shortpath.group(0))
				print filename

				tree.write(filename + '.xml', encoding="utf-8")
			except:
				pass
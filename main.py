import webapp2
import os
import jinja2
import ast
import json
# import xmltodict
from models import WordBank
# from google.cloud import vision
from google.appengine.api import urlfetch
# from collections import defaultdict
# from xml.etree import cElementTree as ET
# import untangle

theJinjaEnvironment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = [],
    autoescape = True)

# #xml to json
# def etree_to_dict(t):
#     d = {t.tag: {} if t.attrib else None}
#     children = list(t)
#     if children:
#         dd = defaultdict(list)
#         for dc in map(etree_to_dict, children):
#             for k, v in dc.items():
#                 dd[k].append(v)
#         d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
#     if t.attrib:
#         d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
#     if t.text:
#         text = t.text.strip()
#         if children or t.attrib:
#             if text:
#               d[t.tag]['#text'] = text
#         else:
#             d[t.tag] = text
#     return d

# OCR API Call
# def convertFetch():
#     # key =
#     client = vision.ImageAnnotatorClient()
#     response = client.annotate_image({
#        'image': {'source': {'image_uri': "https://cdn.psychologytoday.com/sites/default/files/styles/image-article_inline_full/public/field_blog_entry_images/STOP.jpg?itok=S3B7WgUc"}}
#     })
#     return response

# Difficulty API Call
def diffFetch(wordSearch):
    headers = {"X-Mashape-Key": "9exudehMOfmshNrJJbbbzboGC5KAp1O0OMwjsncunodfJUcM0n",
                "Accept": "application/json"}

    diffSearch = "https://twinword-word-graph-dictionary.p.mashape.com/difficulty/?entry="+ wordSearch
    searchDiffResult = urlfetch.fetch(url = diffSearch, headers = headers)
    searchDiffResult = ast.literal_eval(searchDiffResult.content)
    if ("ten_degree" not in searchDiffResult):
        return 10
    else:
        difficulty = searchDiffResult["ten_degree"]
        return int(difficulty)

def parseList(wordList):
    answerList= []
    for word in wordList:
        if(diffFetch(word) >= 5):
            answerList.append(word)
    return answerList

# Dictionary API Call
def defFetch(wordSearch):
    headers = {"X-Mashape-Key": "9exudehMOfmshNrJJbbbzboGC5KAp1O0OMwjsncunodfJUcM0n",
                "Accept": "application/json"}

    defSearch = "https://twinword-word-graph-dictionary.p.mashape.com/definition/?entry="+ wordSearch
    searchDefResult = urlfetch.fetch(url = defSearch, headers = headers)
    searchDefResult = ast.literal_eval(searchDefResult.content)
    if ("meaning" not in searchDefResult):
        return "";
    if (searchDefResult["meaning"]["noun"] == ""):
        definition = searchDefResult["meaning"]["adjective"]
    else:
        definition = searchDefResult["meaning"]["noun"]
    return definition


# # Medical Dictionary API Call
# def medDictFetch(wordSearch):
#     medSearch = "https://wsearch.nlm.nih.gov/ws/query?db=healthTopics&term="+ wordSearch
#     searchResult = urlfetch.fetch(url = medSearch).toString()
#     # medResult = ET.XML(searchResult)
#     # searchMedResult = json.dumps(xmltodict.parse(searchMedResult))
#     #with open(searchMedResult) as fd:
#     medDefinition = etree_to_dict(searchResult)
#     # medDefinition = untangle.parse(searchResult)
#
#     # searchMedResult = ast.literal_eval(searchMedResult.content)
#     return medDefinition

# HomePage
class HomePage(webapp2.RequestHandler):
    def get(self):
        homeTemplate = theJinjaEnvironment.get_template('templates/home.html')
        self.response.write(homeTemplate.render())

# DocAnalysisPage
class DocAnalysisPage(webapp2.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        docAnalysisTemplate = theJinjaEnvironment.get_template('templates/docAnalysis.html')

        userText = self.request.get("userText")
        content = userText.split(" ")

        diffWords = parseList(content)

        for word in diffWords:
            diffWord = WordBank(word = word, definition = defFetch(word))
            diffWord.put()

        wordBankDatabase = WordBank.query().fetch()

        wordSearch = self.request.get("wordSearch")

        if (not wordSearch == ""):
            searchWord = WordBank(word = wordSearch, definition = defFetch(wordSearch))
            searchWord.put()

        wordBankDatabase = WordBank.query().fetch()

        wordList = []
        definitionList = []

        for i in range(len(wordBankDatabase)):
            if(wordBankDatabase[i].word not in wordList):
                wordList.append(wordBankDatabase[i].word)
                definitionList.append(wordBankDatabase[i].definition)

        templateDict = {
            "userText": userText,
            "words": wordList,
            "definitions": definitionList
        }

        self.response.write(docAnalysisTemplate.render(templateDict))

class CiscoPage(webapp2.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        ciscoTemplate = theJinjaEnvironment.get_template('templates/Cisco.html')
        self.response.write(ciscoTemplate.render())

app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/docAnalysis', DocAnalysisPage),
    ('/Cisco', CiscoPage)
], debug=True)

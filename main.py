import webapp2
import os
import jinja2
import ast
from models import WordBank
from google.appengine.api import urlfetch

theJinjaEnvironment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = [],
    autoescape = True)

# OCR API Call
def convertFetch(allergySearch):
    return allergySearch

# Difficulty API Call
def diffFetch(wordSearch):
    headers = {"X-Mashape-Key": "iiToENZRoxmshW5FvuANkOISJ0RBp1vf08fjsntXGdecY2QYnf",
                "Accept": "application/json"}

    diffSearch = "https://twinword-word-graph-dictionary.p.mashape.com/difficulty/?entry="+ wordSearch
    searchDiffResult = urlfetch.fetch(url = diffSearch, headers = headers)
    searchDiffResult = ast.literal_eval(searchDiffResult.content)
    difficulty = searchDiffResult["meaning"]["noun"]

    return difficulty

# Dictionary API Call
def defFetch(wordSearch):
    headers = {"X-Mashape-Key": "iiToENZRoxmshW5FvuANkOISJ0RBp1vf08fjsntXGdecY2QYnf",
                "Accept": "application/json"}

    defSearch = "https://twinword-word-graph-dictionary.p.mashape.com/definition/?entry="+ wordSearch
    searchDefResult = urlfetch.fetch(url = defSearch, headers = headers)
    searchDefResult = ast.literal_eval(searchDefResult.content)
    definition = searchResult["meaning"]["noun"]

    return definition

# Medical Dictionary API Call
def medDictFetch(word):
    return word

# HomePage
class HomePage(webapp2.RequestHandler):
    def get(self):
        homeTemplate = theJinjaEnvironment.get_template('templates/test.html')
        word = "cardiovascular"
        diff = diffFetch(word)
        def = defFetch(word)
        templateDict = {
            "word": word,
            "diff": diff,
            "def": def
        }
        self.response.write(allergyTemplate.render(templateDict))

# # DocAnalysisPage
# class DocAnalysisPage(webapp2.RequestHandler):
#     def get(self):
#         self.post()
#
#     def post(self):
#         docAnalysisTemplate = theJinjaEnvironment.get_template('templates/docAnalysis.html')
#         allergyName = self.request.get("allergyName")
#         templateDict = {
#             "allergyName": allergyName
#         }
#         self.response.write(recipeSubmitTemplate.render(templateDict))
#
# #
# class GenInfoPage(webapp2.RequestHandler):
#     def get(self):
#         self.post()
#
#     def post(self):
#         genInfoTemplate = theJinjaEnvironment.get_template('templates/genInfo.html')
#
#         questionsDatabase = Questions.query().fetch()
#
#         userQuestion = self.request.get("userQuestion")
#
#         question = None
#
#         for i in range(len(questionsDatabase)):
#             if (questionsDatabase[i].question == userQuestion):
#                 question = questionsDatabase[i]
#
#         if question == None and not userQuestion == "":
#             question = Questions(question = userQuestion)
#             question.put()
#
#         answerName = self.request.get("answerName")
#         answer = self.request.get("answer")
#         questionKey = self.request.get("questionKey")
#
#         if (not answerName == "" and not answer == ""):
#             for i in range(len(questionsDatabase)):
#                 if (questionsDatabase[i].question == questionKey):
#                     question = questionsDatabase[i]
#             question.answerNames.append(answerName)
#             question.answers.append(answer)
#             question.put()
#
#         questionsDatabase = Questions.query().fetch()
#
#         # if (not question == None):
#         #     if (not question in questionsDatabase):
#         #         questionsDatabase.append(question)
#         #
#         # print(questionsDatabase)
#
#         templateDict = {
#             "questionsDatabase": questionsDatabase
#         }
#
#         self.response.write(genInfoTemplate.render(templateDict))
#
# class AllergyInfoPage(webapp2.RequestHandler):
#     def get(self):
#         self.post()
#
#     def post(self):
#         allergyTemplate = theJinjaEnvironment.get_template('templates/allergyInfo.html')
#
#         allergyName = self.request.get("allergyName")
#
#         allergy = allergySearch(allergyName)
#
#         # posts the selected recipe- if there is a link, goes to the link. if not, go to recipe html template
#         if (allergy == None):
#             self.redirect("/submitAllergy")
#             return
#
#         ingredientsSearch = self.request.get("ingredients") + ",-" + allergyName
#         typeSearch = self.request.get("type")
#
#         # comments about the allergy
#         commentName = self.request.get("commentName")
#         comment = self.request.get("comment")
#
#         if (not commentName == "" and not comment == ""):
#             allergy.commentNames.append(commentName)
#             allergy.comments.append(comment)
#
#         allergy.put()
#
#         templateDict = {
#             "allergyName": allergy.allergy,
#             "symptoms": allergy.symptoms,
#             "toAvoid": allergy.toAvoid,
#             "images": allergy.images,
#             "dataRecipes": recipesSearch(allergy.allergy),
#             "apiRecipes": recipeFetch(ingredientsSearch, typeSearch),
#             "commentName": allergy.commentNames,
#             "comment": allergy.comments
#         }
#
#         self.response.write(allergyTemplate.render(templateDict))
#
# # allergy submit page will just go back home
# class AllergySubmitPage(webapp2.RequestHandler):
#     def get(self):
#         self.post()
#
#     def post(self):
#         allergySubmitTemplate = theJinjaEnvironment.get_template('templates/allergySubmit.html')
#         self.response.write(allergySubmitTemplate.render())
#
# class RecipePage(webapp2.RequestHandler):
#     def get(self):
#         self.post()
#
#     def post(self):
#         recipeTemplate = theJinjaEnvironment.get_template('templates/recipe.html')
#
#         recipeName = self.request.get("recipeName")
#
#         recipesDatabase = Recipe.query().fetch()
#
#         recipe = None
#
#         for i in range(len(recipesDatabase)):
#             if (recipesDatabase[i].title == recipeName):
#                 recipe = recipesDatabase[i]
#
#         allergyName = self.request.get("allergyName")
#
#         templateDict = {
#             "allergyName": allergyName,
#             "title": recipe.title,
#             "allergenFree": recipe.allergenFree,
#             "otherTags": recipe.otherTags,
#             "basicIngredients": recipe.basicIngredients,
#             "ingredients": recipe.ingredients,
#             "steps": recipe.steps,
#         }
#
#         self.response.write(recipeTemplate.render(templateDict))
#
# class ThanksPage(webapp2.RequestHandler):
#     def post(self):
#         thanksTemplate = theJinjaEnvironment.get_template('templates/thanks.html')
#
#         allergyName = self.request.get("allergyName")
#         submission = self.request.get("submission")
#
#         message = ""
#         destination = ""
#
#         if (submission == "recipe"):
#             #recipe submit
#             title = self.request.get("title")
#             allergenFree = self.request.get("allergenFree")
#             basicIngredients = self.request.get("basicIngredients") #list
#             ingredients = self.request.get("ingredients") #list
#             ingredients = formatString(ingredients)
#             otherTags = self.request.get("otherTags") #list
#             otherTags = formatString(otherTags)
#             steps = self.request.get("steps") #list
#             steps = steps.replace("\r", "")
#             steps = formatString(steps)
#
#             recipe = Recipe(title = title, allergenFree = allergenFree, basicIngredients = basicIngredients)
#
#             for ingredient in ingredients:
#                 recipe.ingredients.append(ingredient)
#             for otherTag in otherTags:
#                 recipe.otherTags.append(otherTag)
#             for step in steps:
#                 recipe.steps.append(step)
#
#             recipe.put()
#
#             message = "Thanks for submitting a new recipe."
#             destination = "/allergyInfo?allergyName=" + allergenFree
#
#         if (submission == "allergy"):
#             # allergy submit
#             allergy = self.request.get("allergen")
#             symptoms = self.request.get("symptoms")
#             symptoms = formatString(symptoms)
#             toAvoid = self.request.get("toAvoid")
#             toAvoid = formatString(toAvoid)
#             images = self.request.get("allergenImg")
#             images = formatString(images)
#
#             allergy = Allergy(allergy = allergy)
#
#             for symptom in symptoms:
#                 allergy.symptoms.append(symptom)
#             for product in toAvoid:
#                 allergy.toAvoid.append(product)
#             for link in images:
#                 allergy.images.append(link)
#
#             allergy.put()
#
#             message = "Thanks for submitting a new allergy."
#             destination = "/"
#
#         templateDict = {
#             # "allergyName": allergyName,
#             "message": message,
#             "destination": destination
#         }
#
#         self.response.write(thanksTemplate.render(templateDict))

app = webapp2.WSGIApplication([
    ('/', WelcomePage)
], debug=True)

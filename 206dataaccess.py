###### INSTRUCTIONS ###### 

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. You should specify variable names and processes to use. For example, "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts, where the keys represent tags on flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

# Put all import statements you need here.
import unittest  ## for testing
import itertools ## for generators and list comprehension
import collections ## for containers and Counter
import tweepy ## for using the twitter api
import twitter_info  ## for connecting to my personal key
import json ## for downloading api and formating api data for python manipulation
import sqlite3 ## for creating and querying my 3 Tables (Movies, Tweets, Users)
import omdb
import re

# Begin filling in instructions....


consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

## CACHING
## need cache file
CACHE_FNAME = "SI206_finalproject_cache.json"
## try
try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)

except:
	CACHE_DICTION = {}

## except, create new cache diction 


## ombdb.search_movie("Frozen")
## example of pulling title from list and finding info on it
Test_list = ["Frozen", "21 Jump Street", "Mean Girls"]
for title in Test_list:
	x = omdb.title(title)
	# print(x)
ombdb_test_request = omdb.title("Mean Girls")
# print(ombdb_test_request)
# print(ombdb_test_request)
# print(ombdb_test_request["language"])
# print(type(ombdb_test_request["language"]))

# print(ombdb_test_request)
# print(len(ombdb_test_request))
# print(type(ombdb_test_request))
# print(ombdb_test_request["title"])

## why does this return a string? 
# x = json.dumps(ombdb_test_request)
# print(ombdb_test_request)
# print(type(ombdb_test_request))
# print(len(ombdb_test_request))
# print(ombdb_test_request[0])
# print(type(ombdb_test_request[0]))

## Task 1: Creating 3 Tables 



## Tweets table:
## rows: tweet_text TEXT, tweet_id STRING PRIMARY KEY, user_id INTEGER, movie_title TEXT, num_favs INTEGER, num_retweets INTEGER 

## Users table (for Twitter users)
## user_id STRING PRIMARY KEY, screen_name TEXT, num_favorites INTEGER, description TEXT


## Movies table
## ID PRIMARY KEY, movie_title TEXT, director TEXT, num_lang INTEGER, IMDB_rating FLOAT, first_actor TEXT, 




## here, use the lists of instances/dictionaries/etc . . . 

## Task 2: Write functions

def get_tweet_search_term_data(search_term):
	if search_term in CACHE_DICTION:
		search_data = CACHE_DICTION[search_term]
		return(search_data)
	else:
		search_data = api.search(search_term)
		CACHE_DICTION[search_term] = search_data
		f = open(CACHE_FNAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()
		return search_data


def get_twitter_user_data(user_name):
	if user_name in CACHE_DICTION:
		print('using cached data for', user_name)
		user_data = CACHE_DICTION[user_name]
	else:
		print('getting data from internet for', user_name)
		user_data = api.get_user(user_name)

		CACHE_DICTION[user_name] = user_data
		f = open(CACHE_FNAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		c.close()
	return user_data




# x = api.search("Donald Trump")
# ## search gets 2 tweets, so 
# print(json.dumps(x))
# print(len(x))

def get_omdb_data(movie_title):
# 		#accepts a string movie title
# 		#check to see if there's cached data for the movie. If there is, fetch that dictionary object.
	if movie_title in CACHE_DICTION:
		print('using cached data for', movie_title)
		movie_info = CACHE_DICTION[movie_title]
	else:
		print('getting data from the internet for', movie_title)
		movie_info = omdb.title(movie_title)
		CACHE_DICTION[movie_title] = movie_info
		f= open(CACHE_FNAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()
	return movie_info

		# if there is no cached data for the movie title, request data from omdb api to get a dictionary about that one movie
		# return the dictionary object (cached or not for that movie)



## This creates an instance of the movie, allows you to calculate the number of languages in it, its box office profit, and the run_time --> important for summary stats page. 
class Movie(object): 
	def __init__(self, dictionary_data):
			self.movie_title = dictionary_data["title"]
			self.movie_director = dictionary_data["director"]
			self.movie_imdb_rating = dictionary_data["imdb_rating"]
			actor_data = dictionary_data["actors"]
			regex0 = r'(\w+ \w+)'
			actor_list = re.findall(regex0, actor_data)
			self.actor = actor_list[0]

			run_time_data = dictionary_data["runtime"]
			regex1 = r'(\d+)'
			run_time_digits = re.findall(regex1, run_time_data)
			self.run_time = run_time_digits


			languages = dictionary_data["language"]
			regex = r'([a-zA-Z]+)'
			return_languages = re.findall(regex, languages)
			num_languages = len(return_languages)
			self.num_languages = num_languages
			
			profit_data = dictionary_data["box_office"]
			regex2 = r'[$](.+).\d\d'
			profit = re.findall(regex2, profit_data)
			self.box_office = profit
			

		

	def __str__(self):
		return "Movie title: {}, directed by {}, and has a {} IMDB rating".format(self.movie_title, self.movie_director, self.movie_imdb_rating)

	def get_actor_search_data(self):
		actor_search = Tweet(self.actor)
		search_result = actor_search.get_tweet_data()
	# search_result = get_tweet_search_term_data(self.movie_title)
		return search_result

# def num_languages(self):
# 	languages = dictionary_data["language"]
# 	regex = r'([a-zA-Z]+)'
# 	return_languages = re.findall(regex, languages)
# 	num_languages = len(return_languages)
# 	return num_languages

# def box_office_profit(self):
# 	profit_data = dictionary_data["box_office"]
# 	regex = r'[$](.+).\d\d'
# 	profit = re.findall(regex, profit_data)
# 	return profit

# def run_time(self):
# 	run_time = dictionary_data["runtime"]
# 	return run_time



# 	# investigate the type. if List, iterate through and count
# 	return 


##  def get_director_data(self):
		## it takes a dictionary for a movie
		## create a Tweet instance with self.movie_director as the search term
		## this looks like: tweet_instance = Tweet(self.movie_director)
		## return tweet_instance.



class Tweet(object):
	def __init__(self, actor_name):
		self.actor = actor_name

	def get_tweet_data(self):
		if self.actor in CACHE_DICTION:
			print('using cached data for', self.actor)
			actor_tweet_data = CACHE_DICTION[self.actor]
		else:
			print('using cached data for', self.actor)
			actor_tweet_data = api.search(str(self.actor))
			CACHE_DICTION[self.actor] = actor_tweet_data
			f= open(CACHE_FNAME, 'w')
			f.write(json.dumps(CACHE_DICTION))
			f.close()
			return actor_tweet_data


		# if the self.movie_title_search name is in the cache diction, grab that data
		# if it's not in the cache diction, use the twitter search api to get data for the first 20 search results 
		# write that data to the cache file
		# return list of 20 dictionaries containing tweet data

## class TwitterUser(object):
	##def __init__(self, single_tweet_dictionary):
		## users_mentioned = single_tweet_dictionary["mentions"]
		## user_who_posted = single_tweet_dictionary["user"]["screen_name"]





# Task Pre-3: Set up code for putting into database
Movie_Titles = ["Frozen", "Mean Girls", "The Notebook"]
# list comprehension creates list of dicionaries with the movie data 
movie_data_list = [get_omdb_data(movie) for movie in Movie_Titles]
movie_class_instances = [Movie(item) for item in movie_data_list]
tweet_class_instances = [Tweet(item.actor) for item in movie_class_instances]

## We know tweet_class_instances is working if the actor names are stores in the Tweet instances 
# for item in tweet_class_instances:
# 	print(item.actor)
real_list_of_tweet_instances = [item.actor for item in tweet_class_instances]

##actor data is list of tuples
actor_data = [actor.get_tweet_data() for actor in tweet_class_instances]
# print(actor_data)
# print(actor_data)

user_mentions = []
users_who_posted = []
for item in actor_data:
	## give me info about the posters of the tweets and info about the users mentioned in the tweets
	print(item)
	print("\n")
	print("\n")
	mentions_in_tweet = item["statuses"]["entities"]["user_mentions"]
	for item in mentions_in_tweet:
		user_mentions.append(item)

	users_who_posted.append(item["user"]["id_str"])




## testing that list of instances works correctly 
# for instance in movie_class_instances:
# 	print(instance.movie_title, instance.movie_director, instance.movie_imdb_rating, instance.run_time, instance.num_languages, instance.box_office)
# 	print("\n")




##Task 3: Process Data, create output file
## MAke queries to the database to grab intersections of  data, use at last 4 of the processing mechanisms in the project requirements to find out something interesting or cool or weird about it. 

## write this data to a text file (summary stats page) with TITLE








# Put your tests here, with any edits you now need from when you turned them in with your project plan.

# class MovieTests(unittest.TestCase):
# 	# def test_movie_init(self):

# 	def test_movie_constructor1(self):
# 		dictionary_data = {}
# 		m = Movie(dictionary_data)
# 		## test type
# 		self.assertEqual(type(m.movie_title), type("string"))

# 	def test_movie_constructor2(self):
# 		dictionary_data = {}
# 		m = Movie(dictionary_data)
# 		self.assertEqual(type(m.movie_director), type("string"))

# 	def test_movie_constructor3(self):
# 		dictionary_data = {}
# 		m = Movie(dictionary_data)
# 		self.assertEqual(type(m.movie_imdb_rating), type(9.2))

# 	def test_get_director_data1(self):
# 		d = {}
# 		t = Tweet("Steven Spielberg")
# 		self.assertEqual(type(get_director_data(d)), type(t))

# class TweetTests(unittest.TestCase):
# ## these tests are for the Tweet class methods

# 	def test_tweet_constructor1(self):
# 		t = Tweet("Steven Spielberg")
# 		self.assertEqual(type(t.movie_director), type("string"))

# 	def test_get_tweet_data1(self):
# 		tweet_data = Tweet("Steven Spielberg")
# 		t = get_tweet_data(tweet_data.movie_director)
# 		self.assertEqual(type(t), type([]))

# 	def test_get_tweet_data2(self):
# 		tweet_data = Tweet("Steven Spielberg")
# 		t = get_tweet_data(tweet_data.movie_director)
# 		self.assertEqual(len(t), 20)

# 	def test_get_tweet_data3(self):
# 		tweet_data = Tweet("Steven Spielberg")
# 		t = get_tweet_data(tweet_data.movie_director)
# 		self.assertEqual(type(t)[0], type({}))
# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)
if __name__ == "__main__":
	unittest.main(verbosity=2)
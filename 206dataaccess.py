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

Movie_Titles = ["Frozen", "Mean Girls", "The Notebook", "Argo"]


## Task 1: Creating 3 Tables 
## Create a Tweet, Users, and Movies table.

## Movies table
## ID PRIMARY KEY, movie_title TEXT, director TEXT, num_lang INTEGER, IMDB_rating FLOAT, first_actor TEXT, 

conn = sqlite3.connect('si2016finalproject.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Movies')
statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Movies (ID INTEGER PRIMARY KEY, movie_title TEXT, directors TEXT, IMDB_rating REAL, run_time INTEGER, num_lang INTEGER, box_office$ INTEGER, first_actor TEXT)'

cur.execute(statement)



# Users table (for Twitter users)
# user_id STRING PRIMARY KEY, screen_name TEXT, num_favorites INTEGER, description TEXT

# self.user_id = single_tweet_dictionary["id_str"]
# 		self.screen_name = single_tweet_dictionary["screen_name"]
# 		self.num_favorites = single_tweet_dictionary["favourites_count"]
# 		self.description = single_tweet_dictionary["description"]
# 		self.followers = single_tweet_dictionary["followers_count"]

cur.execute('DROP TABLE IF EXISTS Users')
statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Users (user_id STRING PRIMARY KEY, screen_name TEXT, num_favorites INTEGER, description TEXT, num_followers INTEGER)'

cur.execute(statement)


# Tweets table:
# rows: tweet_text TEXT, tweet_id STRING PRIMARY KEY, user_id INTEGER, movie_title TEXT, num_favs INTEGER, num_retweets INTEGER 

cur.execute('DROP TABLE IF EXISTS Tweets')
statement = ('CREATE TABLE IF NOT EXISTS ')
statement += 'Tweets (tweet_id STRING PRIMARY KEY, tweet_text TEXT, user_id STRING, first_actor TEXT, num_favs INTEGER, num_retweets INTEGER, FOREIGN KEY(user_id) REFERENCES Users(user_id) ON UPDATE SET NULL, FOREIGN KEY (first_actor) REFERENCES Movies ON UPDATE SET NULL)'

cur.execute(statement)





conn.commit()


## here, use the lists of instances/dictionaries/etc . . . 

## Task 2: Write functions

## Might put search term function under the Tweet class
# def get_tweet_search_term_data(search_term):
# 	if search_term in CACHE_DICTION:
# 		search_data = CACHE_DICTION[search_term]
# 		return(search_data)
# 	else:
# 		search_data = api.search(search_term)
# 		CACHE_DICTION[search_term] = search_data
# 		f = open(CACHE_FNAME, 'w')
# 		f.write(json.dumps(CACHE_DICTION))
# 		f.close()
# 		return search_data


## takes user_name OR id, so str_id will be fine
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
		f.close()
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

## invoke the function for tests
omdb_test_object = get_omdb_data("Frozen")
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
			self.run_time = run_time_digits[0]


			languages = dictionary_data["language"]
			regex = r'([a-zA-Z]+)'
			return_languages = re.findall(regex, languages)
			num_languages = len(return_languages)
			self.num_languages = num_languages
			
			profit_data = dictionary_data["box_office"]
			regex2 = r'[$](.+).\d\d'
			profit = re.findall(regex2, profit_data)
			self.box_office = profit[0]
			

		

	def __str__(self):
		return "{}, directed by {}, has a {} IMDB rating. Its first actor is {}, with a total run time of {} minutes. It contains {} languages and brought in a total of ${} in box office profits.".format(self.movie_title, self.movie_director, self.movie_imdb_rating, self.actor, self.run_time, self.num_languages, self.box_office)


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

	def get_actor_data(self):
		if self.actor in CACHE_DICTION:
			print('using cached data for', self.actor)
			actor_tweet_data = CACHE_DICTION[self.actor]
		else:
			print('using internet data for', self.actor)
			##actor_tweet_Data is json object
			actor_tweet_data = api.search(str(self.actor))
			CACHE_DICTION[self.actor] = actor_tweet_data
			f= open(CACHE_FNAME, 'w')
			f.write(json.dumps(CACHE_DICTION))
			f.close()
		## need this outside the if and else, because it will never execute if the if is true
		return actor_tweet_data


		## tweet_id (primary key)
		## tweet text,
		## user who posted the tweet
		## the actor search this tweet came from (reference the movies table)
		## ## number favorites
		## number retweets

		# if the self.movie_title_search name is in the cache diction, grab that data
		# if it's not in the cache diction, use the twitter search api to get data for the first 20 search results 
		# write that data to the cache file
		# return list of 20 dictionaries containing tweet data



# Users table (for Twitter users)
# user_id STRING PRIMARY KEY, screen_name TEXT, num_favorites INTEGER, description TEXT, followers INTEGER

class TwitterUser(object):
	def __init__(self, single_tweet_dictionary):
		self.user_id = single_tweet_dictionary["id_str"]
		self.screen_name = single_tweet_dictionary["screen_name"]
		self.num_favorites = single_tweet_dictionary["favourites_count"]
		self.description = single_tweet_dictionary["description"]
		self.followers = single_tweet_dictionary["followers_count"]



# Task Pre-3: Set up code for putting into database

# list comprehension creates list of dicionaries with the movie data 
movie_data_list = [get_omdb_data(movie) for movie in Movie_Titles]
movie_class_instances = [Movie(item) for item in movie_data_list]
tweet_class_instances = [Tweet(item.actor) for item in movie_class_instances]

## We know tweet_class_instances is working if the actor names are stores in the Tweet instances 
# for item in tweet_class_instances:
# 	print(item.actor)
# real_list_of_tweet_instances = [item.actor for item in tweet_class_instances]

##actor data is list of tuples
actor_data = [actor.get_actor_data() for actor in tweet_class_instances]

## Tweet data from three searches 
# print(len(actor_data))
# print(actor_data)

## trying to make two lists, so I can call get_twitter_user_data on each of the items in both lists
## set guarantees element inside set is unique 
user_mentions = set()
user_who_posted = set()

tweet_info_tuple_list_2 = []
## for every dictionary of data associated with one of the actors
for item in actor_data:


	## give me info about the posters of the tweets and info about the users mentioned in the tweets
	print(item)
	print(type(item))
	print("\n")
	print("\n")
	# mentions_in_tweet = item["statuses"]["entities"]["user_mentions"]
	## give me the list of dictionaries (statuses)
	mentions_in_tweet = item["statuses"]


	## for each dictionary, item (get this attribute), unless there are none
	for list_item in mentions_in_tweet:
		tuple_instance = list_item["id_str"], list_item["text"], list_item["user"]["id_str"], item["search_metadata"]["query"], list_item["favorite_count"], list_item["retweet_count"]
		tweet_info_tuple_list_2.append(tuple_instance)
		get_user_mentions = list_item["entities"]["user_mentions"]
		for name in get_user_mentions:
			name_id = name["id_str"]
			# print(name_id)
			user_mentions.add(name_id)
	for list_item in mentions_in_tweet:
		get_user_who_posted = list_item["user"]["id_str"]
		user_who_posted.add(get_user_who_posted)

# instance_tuple = instance.tweet_id, instance.tweet_text, instance.user_id, instance.first_actor, instance.num_favs, instance.num_retweets


		# print(get_user_mentions)
		# print("\n")
		# print("\n")
# 		user_mentions.add(get_user_mentions)
# print(user_mentions)
# print(user_who_posted)
set_of_both_mentions_and_users = (user_mentions | user_who_posted)
# print(set_of_both_mentions_and_users)
data_from_both = []
for id_str in set_of_both_mentions_and_users:
	try:
		the_data = get_twitter_user_data(id_str)
		data_from_both.append(the_data)
	except: 
		## if there is no such existing id_str still, pass
		pass


# print(data_from_both)



twitter_user_instances  = [TwitterUser(data_dic) for data_dic in data_from_both]
user_tuple_list = []
for instance in twitter_user_instances:
	instance_tuple = instance.user_id, instance.screen_name, instance.num_favorites, instance.description, instance.followers

	user_tuple_list.append(instance_tuple)

# print(user_tuple_list[0])


	## statuses is a list of dictionaries 

	# for item in mentions_in_tweet:
# add is for sets
	# user_mentions.add(item)

	# users_who_posted.append(item["user"]["id_str"])

	# self.tweet_id= dic["id_str"]
	# 		self.tweet_text = dic["text"]
	# 		self.user_id = dic["user"]["id_str"]
	# 		self.num_favs = dic["favorite_count"]
	# 		self.num_retweets = dic["retweet_count"]



## testing that list of instances works correctly 
movie_tuple_list = []
for instance in movie_class_instances:
	instance_tuple = None, instance.movie_title, instance.movie_director, instance.movie_imdb_rating, instance.run_time, instance.num_languages, instance.box_office, instance.actor
	# print(instance_tuple)
	movie_tuple_list.append(instance_tuple)
	# print("\n")

# print(movie_tuple_list)

statement = 'INSERT OR IGNORE INTO Movies VALUES (?, ?, ? ,? , ?, ?, ?, ?)'
for item in movie_tuple_list:
	cur.execute(statement, item)

conn.commit()


statement = 'INSERT OR IGNORE INTO Users VALUES (?, ?, ?, ?, ?)'
for item in user_tuple_list:
	cur.execute(statement,item)

conn.commit()

statement = 'INSERT OR IGNORE INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'
for item in tweet_info_tuple_list_2:
	cur.execute(statement,item)

conn.commit()


##Task 3: Process Data, create output file

## MAke queries to the database to grab intersections of  data, use at last 4 of the processing mechanisms in the project requirements to find out something interesting or cool or weird about it. 

## This query grabs the text of tweets from users that have more than 1000 followers, which is interesting, because they will likely have the greatest number of views.
query1 = 'SELECT Tweets.tweet_text FROM Tweets INNER JOIN Users on Tweets.user_id = Users.user_id WHERE Users.num_followers > 1000'
cur.execute(query1)
query1_obj = cur.fetchall()
popular_text_list = [x[0] for x in 	query1_obj]
# print(popular_text_list)
regex1 = '@(\w+)'

joined_text = ''.join(popular_text_list)

regex_text = re.findall(regex1, joined_text)

## Give all of the usernames mentioned in these tweets
the_mentions = {x for x in regex_text}
the_mentions_str = str(the_mentions)
# print(the_mentions_str)



## Give the most commonly mentioned names 
mention_count = collections.Counter(regex_text)
# print(mention_count)
for name, count in mention_count.most_common(1):
	most_common_name = name
# print(most_common_name)
# print(regex_text)

# print(joined_text)
# joined_2 = joined_text.split()
# print(joined_2)


query2 = 'SELECT tweet_text from Tweets WHERE num_retweets>1000'
cur.execute(query2)
query2_obj = cur.fetchall()
popular_tweets = [x[0] for x in query2_obj]
popular_tweets_joined = ', '.join(popular_tweets)

query3= 'SELECT screen_name from Users WHERE num_favorites > 5000'
cur.execute(query3)
query3_obj = cur.fetchall()
popular_users = [x[0] for x in query3_obj]
popular_users_joined = ', '.join(popular_users)


my_file = open("statsfile.txt", "w")
my_file.write("Summary stats for the following movies: ")

movie_title_str = ', '.join(Movie_Titles)
my_file.write(movie_title_str)
my_file.write(" on 4/20/2017")
my_file.write("\n")
for movie in Movie_Titles:
	d = get_omdb_data(movie)
	s = Movie(d)
	my_file.write(str(s))
	my_file.write("\n")
	my_file.write("\n")
my_file.write("After searching twitter data about the first star actor of each of these movies, the text from tweets posted by the most influential users identified in the search (those with more than 1000 followers) were collected. ")
my_file.write("\n")
my_file.write("Although all of the mentioned screen names within these tweets were: ")
my_file.write(the_mentions_str)
my_file.write("\n")
my_file.write("The most mentioned screen name of these screen names was: ")
my_file.write(most_common_name)


my_file.write("\n")
my_file.write("\n")
my_file.write("The most popular tweets, each with greater than 1000 retweets, were: ")
my_file.write("\n")
my_file.write(str(popular_tweets_joined))
my_file.write("\n")
my_file.write("\n")
my_file.write("The most popular users, each with greater than 5000 favorited tweets total were: ")
my_file.write("\n")
my_file.write(str(popular_users_joined))

my_file.close()

##find the most popular hashtags on the most influential twitter users' (more than 1000 followers)





## write this data to a text file (summary stats page) with TITLE




## CLOSES THE DATABASE

cur.close()

# Put your tests here, with any edits you now need from when you turned them in with your project plan.

class MovieTests(unittest.TestCase):
	# def test_movie_init(self):

	def test_movie_constructor1(self):
		# dictionary_data = {}
		d = get_omdb_data("Frozen")
		m = Movie(d)
		## test type
		self.assertEqual(type(m.movie_title), type("string"))

	def test_movie_constructor2(self):
		d = get_omdb_data("Frozen")
		m = Movie(d)
		self.assertEqual(type(m.movie_director), type("string"))

	def test_movie_constructor3(self):
		d = get_omdb_data("Frozen")
		m = Movie(d)
		self.assertEqual(type(m.movie_imdb_rating), type("string"))

	def test_movie_constructor_actor(self):
		d= get_omdb_data("Frozen")
		m = Movie(d)
		self.assertEqual(m.actor, "Kristen Bell")

	def test_movie_constructor4(self):
		d = get_omdb_data("Frozen")
		m = Movie(d)
		self.assertEqual(m.num_languages, 2)

	def test_movie_constructor5(self):
		d = get_omdb_data("Frozen")
		m = Movie(d)
		self.assertEqual(type(m.num_languages), type(2))

	def test_movie_constructor_runtime(self):
		d= get_omdb_data("Frozen")
		m = Movie(d)
		self.assertEqual(m.run_time, "102")

	def test_get_actor_data1(self):
		d= Tweet("Lindsay Lohan")
		self.assertEqual(type(d.get_actor_data()), type({}))

	def test_movie_constructor4(self):
		d = get_omdb_data("Frozen")
		m = Movie(d)
		self.assertEqual(type(m.run_time), type("string"))

	def test_movie_constructor5(self):
		d = get_omdb_data("Frozen")
		m = Movie(d)
		self.assertEqual(type(m.box_office), type("string"))

	def test_movie_str_constructor(self):
		d = get_omdb_data("Mean Girls")
		s = Movie(d)
		str_version = str(s)
		self.assertEqual(str_version, "Mean Girls, directed by Mark Waters, has a 7.0 IMDB rating. Its first actor is Lindsay Lohan, with a total run time of 97 minutes. It contains 4 languages and brought in a total of $85,974,306 in box office profits.")



class Tweet_Data(unittest.TestCase):
## these tests are for the Tweet class methods

	def test_get_twitter_user_data(self):
		x = get_twitter_user_data("172403197")
		self.assertEqual(type(x), type({}))

	def test_2(self):
		x = Tweet("Lindsay Lohan")
		y = x.get_actor_data()
		self.assertEqual(type(y), type({}))

class OMDB_Data(unittest.TestCase):
	def test_get_omdb_data(self):
		omdb_frozen = get_omdb_data("Frozen")
		self.assertEqual(type(omdb_frozen), type({}))


class Twitter_UserTests(unittest.TestCase):
	def test_twitter_user_constr1(self):
		s = TwitterUser(data_from_both[1])
		self.assertEqual(type(s.user_id), type("string"))

	def test_twitter_user_constr2(self):
		s = TwitterUser(data_from_both[1])
		self.assertEqual(type(s.screen_name), type("string"))

	def test_twitter_user_constr3(self):
		s = TwitterUser(data_from_both[1])
		self.assertEqual(type(s.num_favorites), type(9))

	def test_twitter_user_constr4(self):
		s = TwitterUser(data_from_both[1])
		self.assertEqual(type(s.description), type("string"))
	def test_twitter_user_constr5(self):
		s = TwitterUser(data_from_both[1])
		self.assertEqual(type(s.followers), type(9))




	## write mor tests to test the omdb_data_get_function


		## num_favorites
		## description
		#followers

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)
if __name__ == "__main__":
	unittest.main(verbosity=2)
## Your name:
## The option you've chosen: Option 2

# Put import statements you expect to need here!
# import unittest  ## for testing
# import itertools ## for generators and list comprehension
# import collections ## for containers and Counter
# import tweepy ## for using the twitter api
# import twitter_info  ## for connecting to my personal key
# import json ## for downloading api and formating api data for python manipulation
# import sqlite3 ## for creating and querying my 3 Tables (Movies, Tweets, Users)

## Pseudocode for functions begins here

#def get_omdb_data(movie_title):
		##accepts a string movie title
		##check to see if there's cached data for the movie. If there is, fetch that dictionary object.
		## if there is no cached data for the movie title, request data from omdb api to get a dictionary about that one movie
		## return the dictionary object (cached or not for that movie)


# class Movie(object): 

# 	def __init__(self, dictionary_data):
			##self.movie_title = dictionary_data["title"]
			## self.movie_director = dictionary_data["director"]
			## self.movie_imdb_rating = dictionary_data["rating"]

# ## def __str__(self):
# 		return "Movie title: {}, directed by {}, and has a {} IMDB rating".format(self.movie_title, self.movie_director, self.movie_imdb_rating)

## def num_languages(self):
	## languages = dictionary_data["Language"], investigate the type. if List, iterate through and count
	## return count of total languages


##  def get_director_data(self):
		## it takes a dictionary for a movie
		## create a Tweet instance with self.movie_director as the search term
		## this looks like: tweet_instance = Tweet(self.movie_director)
		## return tweet_instance.


## class Tweet(object):
	## def __init__(self, director_name):
		## self.movie_director = director_name 


	##def get_tweet_data(self):
		## if the self.movie_director name is in the cache diction, grab that data
		## if it's not in the cache diction, use the twitter search api to get data for the first 20 search results 
		## write that data to the cache file
		## return list of 20 dictionaries containing tweet data

## class TwitterUser(object):
	##def __init__(self, single_tweet_dictionary):
		## users_mentioned = single_tweet_dictionary["mentions"]
		## user_who_posted = single_tweet_dictionary["user"]["screen_name"]




# Write your test cases here.
class MovieTests(unittest.TestCase):
	# def test_movie_init(self):

	def test_movie_constructor1(self):
		dictionary_data = {}
		m = Movie(dictionary_data)
		## test type
		self.assertEqual(type(m.movie_title), type("string"))

	def test_movie_constructor2(self):
		dictionary_data = {}
		m = Movie(dictionary_data)
		self.assertEqual(type(m.movie_director), type("string"))

	def test_movie_constructor3(self):
		dictionary_data = {}
		m = Movie(dictionary_data)
		self.assertEqual(type(m.movie_imdb_rating), type(9.2))

	def test_get_director_data1(self):
		d = {}
		t = Tweet("Steven Spielberg")
		self.assertEqual(type(get_director_data(d)), type(t))

class TweetTests(unittest.TestCase):

	def test_tweet_constructor1(self):
		t = Tweet("Steven Spielberg")
		self.assertEqual(type(t.movie_director), type("string"))

	def test_get_tweet_data1(self):
		tweet_data = Tweet("Steven Spielberg")
		t = get_tweet_data(tweet_data.movie_director)
		self.assertEqual(type(t), type([]))

	def test_get_tweet_data2(self):
		tweet_data = Tweet("Steven Spielberg")
		t = get_tweet_data(tweet_data.movie_director)
		self.assertEqual(len(t), 20)

	def test_get_tweet_data3(self):
		tweet_data = Tweet("Steven Spielberg")
		t = get_tweet_data(tweet_data.movie_director)
		self.assertEqual(type(t)[0], type({}))






		

		


## Remember to invoke all your tests...
if __name__ == "__main__":
	unittest.main(verbosity=2)
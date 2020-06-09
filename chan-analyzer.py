#!/usr/bin/python3

import requests
from time import sleep

# GLOBALS

# Endpoints
api_base = "https://a.4cdn.org"
board = ""
thread_endpoint = "threads.json"
thread_post_endpoint = "thread/"
request_threads = None

# Values
token = "bitcoin"
mention_count = 0
nb_page = 0
current_page = 1

def countMentionInBoard(board):
  global mention_count
  global nb_page
  global current_page
  request_threads = requests.get(api_base + board + thread_endpoint)
  sleep(1)
  if request_threads.status_code != 200:
    print("Error " + str(request_threads.status_code) + ": cannot get threads from board \"" + board + "\"")
  else:
    nb_page = len(request_threads.json())
    for page in request_threads.json():
      print("Start analyzing page " + str(current_page) + "/" + str(nb_page))
      for thread in page['threads']:
        #debug: print current thread ID
        # print("Thread ID: " + str(thread['no']))
        #debug: print thread data url
        # print(api_base + board + thread_post_endpoint + str(thread['no']) + ".json")
        posts = requests.get(api_base + board + thread_post_endpoint + str(thread['no']) + ".json")
        sleep(1)
        if posts.status_code != 200:
          print("Error " + str(posts.status_code) + ": cannot get posts from thread \"" + str(thread['no']) + "\"")
        else:
          #debug: print all posts
          # print(posts.json())
          for post in posts.json()['posts']:
            #debug: print current post ID
            # print("Post ID: " + str(post['no']))
            if "com" in post:
              mention_count += str.lower(post['com']).count(token)
              #debug: print current mention count
              # print(mention_count)
      print("Page " + str(current_page) + "/" + str(nb_page) + " done")
      current_page += 1

# MAIN

def main():
  global token
  global board
  global mention_count
  print("\n")
  print("======= chan-analyzer =======")
  print("   4chan keyword analyzer    ")
  print("\n")
  board = input("Type a board name (ex: /biz/):\n")
  token = input("Type a keyword to scan:\n")
  print("Scanning keyword \"" + token + "\" in board \"" + board + "\"")
  print("It can last several minutes due to rate limit.")
  print("Please wait ...")
  print("\n")
  countMentionInBoard(board)
  print("\nEnd of analyze\n")
  print("Number of mentions for keyword \"" + token + "\" in board \"" + board + "\": " + str(mention_count))

main()

# SneakPeek Bot v1.1 (Testing Phase)
# Problem 1: 'promoted' category not present in 'sort' param of 'get_post' function

# **************************************
# ************* IMPORTS ****************
# **************************************

from steem import Steem
from steem.blockchain import Blockchain
from steem.post import Post
from steem.steemd import Steemd
from steem.transactionbuilder import TransactionBuilder
from steembase.operations import Comment
import random, threading
import re
import time
import sys
import os
import sys, traceback, logging

# **************************************
# ****** Globals + ENV variables *******
# **************************************

steemPostingKey = os.environ.get('PostKey')
author_m = os.environ.get('Author')
#steem = Steem(wif=steemPostingKey)
steem = Steem(keys = steemPostingKey)
# for debugging with single poster on steemit
debug_acc = os.environ.get('DebugAuthor')
#replyString = ""
blck = Blockchain()
#flag = 0

# **************************************
# ************* FUNCTIONS **************
# **************************************

#This function will get all the posts from given category(tag) and print top 3 posts from "created", "hot", and "trending" sections of that category(tag)
#Argument: Category str

class printposts(threading.Thread):
	def __init__(self, cat, comment_t, section, no_of_post):
		threading.Thread.__init__(self)
		self.cat_c = cat
		self.comment = comment_t
		self.section = section
		self.no_of_post = no_of_post
		flag = 0
		global steem
		global debug_acc
		global author_m
	
	def run(self):
		self.prepReply()

	def prepReply(self):
		start_time = time.time()
		createdposts = steem.get_posts(limit=self.no_of_post, sort="created", category=self.cat_c)
		hotposts = steem.get_posts(limit=self.no_of_post, sort="hot", category=self.cat_c) 
		trendingposts = steem.get_posts(limit=self.no_of_post, sort="trending", category=self.cat_c)
		#promotedposts = steem.get_posts(limit=self.no_of_post, sort="promoted", category=self.cat_c)
		
		print("[Normal Process] CAT (prepReply): %s | Section (prepReply): %s | No of Posts (prepReply): %d" % (self.cat_c, self.section, self.no_of_post))
		replyString = ""
		flag = 0
		strList = ["And Roger was crazy with his bots and everything.",
			"Bots... I think that is a hot topic.",
			"We're fascinated with bots because they are reflections of ourselves.",
			"Our worst comes out when we behave like bots or professionals.",
			"Kids love robots. They're this fanciful, cool thing.",
			"In the twenty-first century, the robot will take the place which slave labor occupied in ancient civilization.",
			"I'm such a robot when it comes to work."
		]
		initStr = random.randint(0, 6)
		replyString += "<center><em>"+strList[initStr]+"</em></center>"
	
		print("[Normal Process] Received Category(Tag): %s" % cat)
		replyString += "<h3> Hello @"+self.comment['author']+" | Here's a sneak peek of #"+self.cat_c+" posts in "+self.section+" section.</h3>"

		i = 0

		if (self.section == "new" and len(createdposts) >= 1):
			replyString += "<h3>Top "+str(len(createdposts))+" Recently Created Posts</h3>"
			for i in range(0, len(createdposts)):
				firstpost = createdposts[i]
				postLink = "https://steemit.com/@"+firstpost["author"]+"/"+firstpost["permlink"]
				print("[Normal Process] https://steemit.com/@%s/%s" % (firstpost["author"], firstpost["permlink"]))
				replyString += "<br/><b>#"+str(i+1)+".</b> <a href='"+postLink+"' target='_blank'>"+firstpost["title"]+"</a> | by @"+firstpost["author"]
				if i == 9:
					break
		else:
			print("[Normal Process] No 'Created' posts in given tag")
			flag = 1
	
		#replyString += "<hr/>"
	
		if (self.section == "hot" and len(hotposts) >= 1):
			replyString += "<h3>Top "+str(len(hotposts))+" Hot Posts</h3>"
			for i in range(0, len(hotposts)):
				firstpost = hotposts[i]
				postLink = "https://steemit.com/@"+firstpost["author"]+"/"+firstpost["permlink"]
				print("[Normal Process] https://steemit.com/@%s/%s" % (firstpost["author"], firstpost["permlink"]))
				replyString += "<br/><b>#"+str(i+1)+".</b> <a href='"+postLink+"' target='_blank'>"+firstpost["title"]+"</a> | by @"+firstpost["author"]
				if i == 9:
					break
		else:
			print("[Normal Process] No 'Hot' posts in given tag")
			flag = 1
	
		#replyString += "<hr/>"
		
		if (self.section == "trending" and len(trendingposts) >= 1):
			replyString += "<h4>Top "+str(len(trendingposts))+" Trending Posts</h4>"
			for i in range(0, len(trendingposts)):
				firstpost = trendingposts[i]
				postLink = "https://steemit.com/@"+firstpost["author"]+"/"+firstpost["permlink"]
				print("[Normal Process] Post in category: https://steemit.com/@%s/%s" % (firstpost["author"], firstpost["permlink"]))
				replyString += "<br/><b>#"+str(i+1)+".</b> <a href='"+postLink+"' target='_blank'>"+firstpost["title"]+"</a> | by @"+firstpost["author"]
				if i == 9:
					break
		else:
			print("[Normal Process] No 'Trending' posts in given tag")
			flag = 1
		
		'''
		if (self.section == "promoted" and len(promotedposts) >= 1):
			replyString += "<h4>Top "+str(len(promotedposts))+" Promoted Posts</h4>"
			for i in range(0, len(promotedposts)):
				firstpost = promotedposts[i]
				postLink = "https://steemit.com/@"+firstpost["author"]+"/"+firstpost["permlink"]
				print("[Normal Process] Post in category: https://steemit.com/@%s/%s" % (firstpost["author"], firstpost["permlink"]))
				replyString += "<br/><b>#"+str(i+1)+".</b> <a href='"+postLink+"' target='_blank'>"+firstpost["title"]+"</a> | by @"+firstpost["author"]
				if i == 9:
					break
		else:
			print("[Normal Process] No 'Promoted' posts in given tag")
			flag = 1
		'''
		
		replyString += "<hr/>"
		replyString += "<sub> I'm a bot, beep boop | Inspired By <a href='https://www.reddit.com/user/sneakpeekbot/' target='_blank'>Reddit SneakPeekBot</a> | Recreated By @miserableoracle"
	
		if (self.comment["author"] == debug_acc) and (flag == 0):
			print("[Normal Process] REPLY IN PROGRESS")
			self.comment.reply(replyString, '', author=author_m, meta=None)
		elif (flag == 1):
			print("[Normal Process] No posts found in mentioned tag. Skip the comment.")
		else:
			print("[Normal Process] Out of testing phase. Comment is not the Debug Account.")

		print("[Normal Process] PROCESS FINISH TIME: %s" % (time.time() - start_time))
		#os._exit(0)
# **************************************
# ************ MAIN FUNC ***************
# **************************************

if __name__ == "__main__":
	# Main loop		
	while 1:
		# Certain posts are receiving "PostDoesNotExist" exeption. Yet to find out the reason.
		try: 
			for comment in steem.stream_comments():
				#Testing phase only print
				#print("[All Trace] NEED TO CHECK : https://steemit.com/@%s/%s" % (comment["author"], comment["permlink"])) [_]*
				#match = re.search(r'(?i)(#)(\w+)[\w-]+(?: promoted| new| trending| hot)*(?: [0-9])*', comment["body"])
				match = re.search(r'(?i)(#)(\w+)[\w-]+(?: new| trending| hot)*(?: [0-9])*', comment["body"])
				if match is None:
					continue
				else:
					# Check if the author of the post is sneakpeek bot, if TRUE ignore the rest of the part and go to next iteration
					if (comment["author"] == author_m):
						continue
					# Check if the comment is main post, if TRUE ignore the rest of the part and go to next iteration
					if (comment.is_main_post()):
						print("[Future] Main Post: https://steemit.com/@%s/%s" % (comment["author"], comment["permlink"]))
						continue
					
					print("[Normal Process] MATCHED: https://steemit.com/@%s/%s" % (comment["author"], comment["permlink"]))
					
					# Matched group will be split, checking for provided arguments
					# Arguments - #Arg1 Arg2 Arg3
					# Arg1 is Category | Arg2 (default - trending) is promoted OR hot OR new OR trending | Arg3 (default - 3) is number between 0 and 9
					temp = match.group(0)
					temp2 = temp.split()
					cat = temp2[0].replace("#", "")
					if(len(temp2) == 1):
						section = "trending"
						no_of_post_int = 3
					if(len(temp2) == 2):
						section = temp2[1]
						no_of_post_int = 3
					if(len(temp2) == 3):
						section = temp2[1]
						no_of_post = temp2[2]
						if(no_of_post.isdigit()):
							no_of_post_int = int(no_of_post)
							if(no_of_post_int == 0):
								print("[Normal Process] Argument 3 is Zero. Changing it to Max(5)")
								no_of_post_int = 3
						else:
							no_of_post_int = 3

					if not cat:
						continue
					else:
						#Check whether the sub-comments already include the comment from sneakpeek bot, if TRUE ignore the rest of the part and go to next iteration
						t_ignore = 0
						sub_comm_list = steem.get_content_replies(comment["author"], comment["permlink"])
						for subcoms in sub_comm_list:
							if (subcoms['author'] == author_m):
								print("[Normal Process] SneakPeek Bot comment already present. Ignore and go to next iteration")
								t_ignore = 1
								break
								
						if (t_ignore == 1):
							continue
						#newpid = os.fork()
						print("[Debug] Category: %s" % cat)
						print("[Debug] Section: %s" % section)
						print("[Debug] No. of Posts: %d" % no_of_post_int)
						# Threading is required in order to make sure
						# that main loop doesn't miss a single block on the blockchain 
						# while processing the current match. 
						# Time processing traces added
						nthread = printposts(cat, comment, section, no_of_post_int)
						nthread.start()	
		except:
			print("[Exception] Error Occurred @ Block No: ", blck.get_current_block_num())
			exc_type, exc_value, exc_traceback = sys.exc_info()
			print("[Exception] Type : ", exc_type)
			print("[Exception] Value : ", exc_value)
			#Enough information present in Type and Value, incase further information is required then use following
			print("[Exception] Traceback : ")
			traceback.print_tb(exc_traceback)
			
# Filter tags for Alerts Settings
# [Normal Process]
# [All Trace]
# [Future]
# [Exception]
# [Debug]

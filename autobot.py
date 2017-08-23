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
#steem = Steem(wif="5K1YAMfF8PfLmoYpFzPGLqVjgqVrYEhVXSV5s1iERDUopi33Jiv")
steem = Steem(keys = steemPostingKey)
# for debugging with single poster on steemit
debug_acc = os.environ.get('DebugAuthor')
#replyString = ""
blck = Blockchain()
#flag = 0

# **************************************
# ************* FUNCTIONS **************
# **************************************

#If you wannt to manually build the transaction and broadcast onto the network, use below function.
'''
def TransBuilder(comment, author, cbody):
	#try:
		tx = TransactionBuilder()
		tx.appendOps(Comment(
			**{"parent_author": comment["author"],
				"parent_permlink": comment["permlink"],
				"author": author,
				"permlink": comment["permlink"],
				"title": "",
				"body": cbody,
				"json_metadata": ""}
		))
		tx.appendWif(wif)
		tx.appendSigner("reminderbot", "posting")
		tx = tx.sign()
		tx = TransactionBuilder.json(tx)
		tx.broadcast()
	#except:
	#	print("[Exception] Unexpected error (Sleep for 3) : ", sys.exc_info()[0])
	#	return False
	#else:
		return True
'''	

#This function will get all the posts from given category(tag) and print top 3 posts from "created", "hot", and "trending" sections of that category(tag)
#Argument: Category str

class printposts(threading.Thread):
	def __init__(self, cat, comment_t):
		threading.Thread.__init__(self)
		self.cat_c = cat
		self.comment = comment_t
		flag = 0
		global steem
		global debug_acc
		global author_m
	
	def run(self):
		self.prepReply()

	def prepReply(self):
		start_time = time.time()
		createdposts = steem.get_posts(limit=3, sort="created", category=self.cat_c)
		hotposts = steem.get_posts(limit=3, sort="hot", category=self.cat_c) 
		trendingposts = steem.get_posts(limit=3, sort="trending", category=self.cat_c)
		
		print("[Normal Process] CAT (prepReply): %s" % self.cat_c)
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
		replyString += "<h3> Hello @"+self.comment['author']+" | Here's a sneak peek of #"+self.cat_c+" posts</h3>"

		i = 0
		'''	********************************************************************************
		# For initial release, use only trending posts display. Reduces the length of reply.
		************************************************************************************
		if len(createdposts) >= 1:
			replyString += "<h3>Top "+str(len(createdposts))+" Recently Created Posts</h3>"
			for i in range(0, len(createdposts)):
				firstpost = createdposts[i]
				postLink = "https://steemit.com/@"+firstpost["author"]+"/"+firstpost["permlink"]
				print("[Normal Process] https://steemit.com/@%s/%s" % (firstpost["author"], firstpost["permlink"]))
				replyString += "<br/><b>#"+str(i+1)+".</b> <a href='"+postLink+"' target='_blank'>"+firstpost["title"]+"</a> | by @"+firstpost["author"]
				if i == 3:
					break
		else:
			print("[Normal Process] No posts in given tag")
			flag = 1
	
		replyString += "<hr/>"
	
		if len(hotposts) >= 1:
			replyString += "<h3>Top "+str(len(hotposts))+" Hot Posts</h3>"
			for i in range(0, len(hotposts)):
				firstpost = hotposts[i]
				postLink = "https://steemit.com/@"+firstpost["author"]+"/"+firstpost["permlink"]
				print("[Normal Process] https://steemit.com/@%s/%s" % (firstpost["author"], firstpost["permlink"]))
				replyString += "<br/><b>#"+str(i+1)+".</b> <a href='"+postLink+"' target='_blank'>"+firstpost["title"]+"</a> | by @"+firstpost["author"]
				if i == 3:
					break
		else:
			print("[Normal Process] No posts in given tag")
			flag = 1
	
		replyString += "<hr/>"
		******************************************************************************** '''
		
		if len(trendingposts) >= 1:
			replyString += "<h4>Top "+str(len(trendingposts))+" Trending Posts</h4>"
			for i in range(0, len(trendingposts)):
				firstpost = trendingposts[i]
				postLink = "https://steemit.com/@"+firstpost["author"]+"/"+firstpost["permlink"]
				print("[Normal Process] Post in category: https://steemit.com/@%s/%s" % (firstpost["author"], firstpost["permlink"]))
				replyString += "<br/><b>#"+str(i+1)+".</b> <a href='"+postLink+"' target='_blank'>"+firstpost["title"]+"</a> | by @"+firstpost["author"]
				if i == 3:
					break
		else:
			print("[Normal Process] No posts in given tag")
			flag = 1
		
		replyString += "<hr/>"
		replyString += "<sub> I'm a bot, beep boop | Inspired By <a href='https://www.reddit.com/user/sneakpeekbot/' target='_blank'>Reddit SneakPeekBot</a> | Recreated By @miserableoracle"
	
		if (self.comment["author"] == debug_acc) and (flag == 0):
			print("[Normal Process] REPLY IN PROGRESS")
			self.comment.reply(replyString, '', author=author_m, meta=None)
		elif (flag == 1):
			print("[Normal Process] No posts found in mentioned tag. Skip the comment.")
		else:
			print("[Normal Process] Out of testing phase")

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
				#print("[All Trace] NEED TO CHECK : https://steemit.com/@%s/%s" % (comment["author"], comment["permlink"]))
				match = re.search(r'(?i)(#)(\w+)[\w-]+', comment["body"])
				if match is None:
					continue
				else:
					# Check if the author of the post is sneakpeek bot, if TRUE ignore the rest of the part and go to next iteration
					if (comment["author"] == author_m):
						continue
					# Check if the comment is main post, if TRUE ignore the rest of the part and go to next iteration
					if (comment.is_main_post()):
						print("[Future] MATCHED: https://steemit.com/@%s/%s" % (comment["author"], comment["permlink"]))
						print("[Future] This is a main post. SneakPeek works on comments only (as of now)")
						continue
					
					print("[Normal Process] MATCHED: https://steemit.com/@%s/%s" % (comment["author"], comment["permlink"]))
					temp = match.group(0)
					cat = temp.replace("#", "")
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
						print("[Normal Process] CAT (Func-MAIN()): %s" % cat)
						# Threading is required in order to make sure
						# that main loop doesn't miss a single block on the blockchain 
						# while processing the current match. 
						# Time processing traces added
						nthread = printposts(cat, comment)
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
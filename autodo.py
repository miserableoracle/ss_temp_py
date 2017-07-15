from steem import Steem
from steem.post import Post
from steem.steemd import Steemd
from steem.transactionbuilder import TransactionBuilder
from steembase.operations import Comment
import random
import re
import time
import sys
import os

steemPostingKey = os.environ.get('steemPostingKey')
author_m = os.environ.get("Author")
steem = Steem(wif=steemPostingKey)
#s = Steemd()
replyString = ""
'''
def TransBuilder(comment, author, cbody):
		global wif
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
	#	print("Unexpected error (Sleep for 3) : ", sys.exc_info()[0])
	#	return False
	#else:
		return True
'''	
#This function will get all the posts from given category(tag) and print top 3 posts from "created", "hot", and "trending" sections of that category(tag)
#Argument: Category str
def printposts(cat):
	global replyString
	global steem
	createdposts = steem.get_posts(limit=3, sort="created", category=cat)
	hotposts = steem.get_posts(limit=3, sort="hot", category=cat) 
	trendingposts = steem.get_posts(limit=3, sort="trending", category=cat)
	flag = 0
	i = 0

	if len(createdposts) >= 1:
		replyString += "### Top 3 Recently Created Posts"
		for i in range(0, len(createdposts)):
			firstpost = createdposts[i]
			postLink = "https://steemit.com/@"+firstpost["author"]+"/"+firstpost["permlink"]
			print("https://steemit.com/@%s/%s" % (firstpost["author"], firstpost["permlink"]))
			replyString += "<b>#"+str(i)+".</b> <a href='"+postLink+"' target='_blank'>"+firstpost["title"]+"</a> | by @"+firstpost["author"]
			if i == 3:
				break
	else:
		print("No posts in given tag")
	
	replyString += "<hr>"
	
	if len(hotposts) >= 1:
		replyString += "### Top 3 Hot Posts"
		for i in range(0, len(hotposts)):
			firstpost = hotposts[i]
			postLink = "https://steemit.com/@"+firstpost["author"]+"/"+firstpost["permlink"]
			print("https://steemit.com/@%s/%s" % (firstpost["author"], firstpost["permlink"]))
			replyString += "<b>#"+str(i)+".</b> <a href='"+postLink+"' target='_blank'>"+firstpost["title"]+"</a> | by @"+firstpost["author"]
			if i == 3:
				break
	else:
		print("No posts in given tag")
	
	replyString += "<hr>"
	
	if len(trendingposts) >= 1:
		replyString += "### Top 3 Trending Posts"
		for i in range(0, len(trendingposts)):
			firstpost = trendingposts[i]
			postLink = "https://steemit.com/@"+firstpost["author"]+"/"+firstpost["permlink"]
			print("https://steemit.com/@%s/%s" % (firstpost["author"], firstpost["permlink"]))
			replyString += "<b>#"+str(i)+".</b> <a href='"+postLink+"' target='_blank'>"+firstpost["title"]+"</a> | by @"+firstpost["author"]
			if i == 3:
				break
	else:
		print("No posts in given tag")
		
	replyString += "<hr>"
	replyString += "<sub> I'm a bot, beep boop | Inspired By <a href='https://www.reddit.com/user/sneakpeekbot/' target='_blank'>Reddit SneakPeekBot</a> | Recreated By @miserableoracle"

if __name__ == "__main__":
	# Main loop		
	while 1:
		# Certain posts are receiving "PostDoesNotExist" exeption. Yet to find out the reason.
		#try: 
			for comment in steem.stream_comments():
				match = re.search(r'(?i)(#)(\w+)[\w-]+', comment["body"])
				if match is None:
					continue
				else:
					strList = ["And Roger was crazy with his bots and everything.",
								"Bots... I think that is a hot topic.",
								"We're fascinated with bots because they are reflections of ourselves.",
								"Our worst comes out when we behave like bots or professionals.",
								"Kids love robots. They're this fanciful, cool thing.",
								"In the twenty-first century, the robot will take the place which slave labor occupied in ancient civilization.",
								"I'm such a robot when it comes to work."
					]
					initStr = random.randint(0, 6)
					replyString += "<em>"+strList[initStr]+"</em>"
					print("https://steemit.com/@%s/%s" % (comment["author"], comment["permlink"]))
					temp = match.group(0)
					cat = temp.replace("#", "")
					if not cat:
						continue
					else:
						print("Received Category(Tag): %s" % cat)
						replyString += "<h2> Here's a sneak peek of #"+cat+" tagged posts</h2>"
						printposts(cat)
						if comment["author"] == "miserableoracle":
							replyid = "@"+comment["author"]+"/"+comment["permlink"]
							#post = Post(Steem(), replyid)
							#post.reply('', replyString, author='reminderbot', reply_identifier=replyid)
							#tx = TransactionBuilder()
							#tx.appendWif(wif)
							comment.reply(replyString, '', author=author_m, meta=None)
							'''if TransBuilder(comment, 'reminderbot', replyString):
								print("Posted!!")
							else:
								print("Transaction Failed. Couldn't Post!")'''
						else:
							print("Out of testing phase")
		#except:
		#	print("Unexpected error (Sleep for 3) : ", sys.exc_info()[0])
		#	time.sleep(3)

from flask import Flask, render_template, request
import random
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)

client = MongoClient()

userdb = client.userdb
user_course_col = userdb.user_course_col

@app.route('/results', methods=['POST'])
def results():
	course_list = list(client.db.course_col.find())
	return render_template('results.html', course_list=course_list)

@app.route('/remove', methods=['POST'])
def remove():
	userdb.user_course_col.remove()
	user_course_list = list(userdb.user_course_col.find())
	return render_template('results.html', user_course_list=user_course_list)

@app.route('/class/setfavorite/<course_id>', methods=['POST','GET'])
def setFavorite(course_id):
	#course = list(client.db.course_col.find_one({"_id['ObjectId']": class_id}))
	#return str(course_id)
	if course_id is not None:
		client.db.course_col.update({"_id": ObjectId(course_id)},
		{
			'$set': { 'favorite': True }
		}
		)
	return str((client.db.course_col.find_one({"_id": ObjectId(course_id)})))
	# str(client.db.collection_names())
	
@app.route('/class/unsetfavorite/<course_id>', methods=['POST','GET'])
def unsetFavorite(course_id):
	#course = list(client.db.course_col.find_one({"_id['ObjectId']": class_id}))
	#return str(course_id)
	if course_id is not None:

		client.db.course_col.update({"_id": ObjectId(course_id)},
		{
			'$set': { 'favorite': False }
		}
		)
	return str((client.db.course_col.find_one({"_id": ObjectId(course_id)})))
	# str(client.db.collection_names())
	
@app.route('/')
def index():
	course_list = list(client.db.course_col.find())
	random.shuffle(course_list)
	return render_template('index.html', course_list=course_list)

if __name__ == '__main__':
    app.run(debug=True)
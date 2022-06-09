# One to One Chat Using Python & Graphene 

## One to One Chat Using Python & Graphene for a React Based front end

### Chat system
This chat is losely based on [kimutaiRop's Graphene Chat](https://github.com/kimutaiRop/django-graphene-chat), and is still a work in progress!

I wanted a One to One chat system for a React Based front end/ Android App. 

### Create Room:
```mutation {
	createChat( userName: "jatin" ) {
		room {
			id
			name
			userId{
				username
			}			
			target{
				username
			}
		}
	}
}```

### Subscribe
```subscription {
        onNewMessage(chatroom:"rahul"){
    				message{
              roomId {
                id
              }
              userId {
                id
                username
              }
              content
              timestamp
              read
            }
        }
      }```

### Send Message
```mutation{
	sendMessage( message: "This is a message", roomId: 3 ) {
     message{
      roomId{
        lastModified
      }
      userId{
        username
      }
      content
      timestamp
      read
    }
	}
}```

You can find more in the explorer.

### Installation:
`pip install -r requirements.txt`

`python manage.py runserver`

### Bugs:
let me know if u find any bugs, or if you have anything that can be done better. Heppy to help!

import graphene
import graphql_jwt
import channels
import channels_graphql_ws

import chat.schema

class Query(chat.schema.Query, graphene.ObjectType):
    pass

class Mutation(chat.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

class Subscription(chat.schema.Subscription, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)

class MyGraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    schema = schema

    async def on_connect(self, payload):
        self.scope['user'] = await channels.auth.get_user(self.scope)
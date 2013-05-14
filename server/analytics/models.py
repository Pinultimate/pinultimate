from mongoengine import DynamicDocument, DateTimeField, StringField, IntField, ReferenceField

class User(DynamicDocument):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)

    def __unicode__(self):
        return self.email

#    def get_session_count(self):
 #       return self.

class UsageSession(DynamicDocument):
    user = ReferenceField(User)
    login = DateTimeField()
    logout = DateTimeField()
    cluster_taps = IntField()

    def __unicode__(self):
        return '%s: %s - %s' % (user, login, logout)    

    meta = {
        'ordering': ['user']
    }
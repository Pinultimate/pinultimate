from mongoengine import DynamicDocument, DateTimeField, StringField, IntField, ReferenceField

class User(DynamicDocument):
    username = StringField(required=True, max_length=15)

    def __unicode__(self):
        return self.username

    def get_all_sessions(self):
        return UsageSession.objects(user=self)

    def get_session_count(self):
        return len(self.get_all_sessions())

    def get_total_active_seconds(self):
        active_seconds = 0
        sessions = self.get_all_sessions()
        for session in sessions:
            active_seconds = active_seconds + session.get_active_seconds()
        return active_seconds

    def get_total_cluster_taps(self):
        taps = 0
        sessions = self.get_all_sessions()
        for session in sessions:
            taps = taps + session.cluster_taps
        return taps

class Session(DynamicDocument):
    #user = ReferenceField(User)
    username = StringField(required=True)
    login = DateTimeField()
    logout = DateTimeField()
    cluster_taps = IntField()

    def __unicode__(self):
        return '%s: %s - %s' % (user, login, logout)    

    def get_active_seconds(self):
        span = self.logout - self.login
        return span.seconds

    meta = {
        'ordering': ['user']
    }
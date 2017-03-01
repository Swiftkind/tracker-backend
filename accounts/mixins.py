
class AccountMixin(object):

    def update_profile(self, instance, data):
        instance.username = data.get('email', '')
        instance.save()

    def update_profile_photo(self, instance, files):
        if 'profile_photo' in files:
            image = files['profile_photo']
            instance.profile_photo.save(image.name, image)
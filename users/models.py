import hashlib
import re
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from authtools.models import AbstractEmailUser
from django.utils.translation import ugettext_lazy as _

NICK_PATTERN = r"[a-zA-Z][a-zA-Z0-9_]{3,15}"
NICK_RE = re.compile(NICK_PATTERN)
NICK_HELPTEXT = _("Nicks must start with an English letter, and contain at least 4 letters, numbers or "
                  "underscores, and may not be longer than 16 characters")


class UserManager(BaseUserManager):
    def create_user(self, nick, email, password=None, **kwargs):
        email = self.normalize_email(email)
        user = self.model(nick=nick, email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class PrivacyLevel(object):
    PUBLIC = 1
    COMMUNITY = 2
    PRIVATE = 3

    choices = (
        (PUBLIC, _('Public (All viewers)')),
        (COMMUNITY, _('Community members only')),
        (PRIVATE, _('Site administrators only')),
    )


class UserSkill(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name

    def count_users(self):
        return User.objects.filter(skills = self).count()


class User(AbstractEmailUser):
    nick = models.CharField(_('nick'), max_length=255, unique=True, validators=[
        RegexValidator(NICK_RE)
    ], help_text=NICK_HELPTEXT)
    privacy = models.IntegerField(_('profile viewable by'), choices=PrivacyLevel.choices, default=PrivacyLevel.PUBLIC)
    email_privacy = models.IntegerField(_('email viewable by'), choices=PrivacyLevel.choices,
                                        default=PrivacyLevel.COMMUNITY)

    english_name = models.CharField(_('name in English'), max_length=255, blank=True, null=True)
    hebrew_name = models.CharField(_('name in Hebrew'), max_length=255, blank=True, null=True)

    phone_number = models.CharField(_('phone number'), max_length=255, blank=True, null=True)
    phone_privacy = models.IntegerField(_('phone number viewable by'), choices=PrivacyLevel.choices,
                                        default=PrivacyLevel.COMMUNITY)

    biography = models.TextField(null=True, blank=True)

    github_username = models.CharField(_('github username'), max_length=255, unique=True, null=True, blank=True)

    facebook_username = models.CharField(_('facebook username'), max_length=255, unique=True, null=True, blank=True)
    facebook_privacy = models.IntegerField(_('facebook number viewable by'), choices=PrivacyLevel.choices,
                                        default=PrivacyLevel.COMMUNITY)
    
    skills = models.ManyToManyField(UserSkill, related_name="users", blank=True)
    

    objects = UserManager()

    REQUIRED_FIELDS = [
        'nick',
        'privacy',
    ]

    def get_full_name(self):
        return self.english_name if self.english_name else self.nick

    def get_short_name(self):
        return self.nick

    def gravatar_url(self):
        return "http://www.gravatar.com/avatar/{}?d=blank".format(hashlib.md5(self.email.lower()).hexdigest())

    @staticmethod
    def filter_by_skill(skill):
        return User.objects.filter(skills=skill)


    def save(self, *args, **kwargs):
        qs = User.objects.filter(nick__iexact=self.nick)
        if self.id:
            qs = qs.exclude(id=self.id)
        if qs.exists():
            raise ValidationError("Nick already in use")
        return super(User, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'slug': self.nick})

    def __unicode__(self):
        return self.get_full_name()

    class Meta:
        ordering = ['nick']
        verbose_name = _('user')
        verbose_name_plural = _('users')



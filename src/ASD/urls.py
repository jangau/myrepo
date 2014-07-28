from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
import contacts
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ASD.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^/$', include('contacts.urls', namespace="contact")),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^register$', contacts.views.CreateUserView.as_view(),
        name = 'users-new'),
    url(r'^home/$',
                           contacts.views.ProfileView.as_view(),
                           name='profiles_profile_detail'),
    url(r'^edit/(?P<pk>\w+)/$', contacts.views.EditProfileView.as_view(),
                                                           name='profiles_edit_profile'),
    url(r'^ajaxexample$', 'contacts.views.main'),
    url(r'^ajaxexample_json$', 'contacts.views.ajax'),
    url(r'^ajaxlike$', 'contacts.views.mlikes'),
    url(r'^ajaxlike_json$', 'contacts.views.likes'),
    url(r'^view/(?P<pk>\w+)/$', contacts.views.OtherProfileView.as_view(),),
)

urlpatterns += staticfiles_urlpatterns()
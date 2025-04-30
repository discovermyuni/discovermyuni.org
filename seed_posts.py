# seed_posts.py
from django.contrib.auth import get_user_model
from posts.models import Post, PostLocation
from taggit.models import Tag
from django.utils import timezone

User = get_user_model()

# 1) Ensure there’s an “admin” user:
admin, _ = User.objects.get_or_create(
    email='admin@example.com',
    defaults={'username': 'admin', 'is_staff': True, 'is_superuser': True}
)

# 2) Create some sample tags
tag_names = ['Announcement', 'Event', 'Reminder']
tags = {}
for name in tag_names:
    t, _ = Tag.objects.get_or_create(name=name)
    tags[name] = t

# 3) Create three test posts
titles = [
    "Welcome to Discover UTM!",
    "Campus Cleanup Day",
    "Last-Minute Study Group"
]

for i, title in enumerate(titles):
    loc_name = f"Building {100+i}, UTM Campus"
    loc, _ = PostLocation.objects.get_or_create(name=loc_name)

    post, created = Post.objects.get_or_create(
        title=title,
        defaults={
            'author': admin,
            'description': f"This is a sample description for “{title}”.",
            'start_date': timezone.now() + timezone.timedelta(days=i),
            'end_date': timezone.now() + timezone.timedelta(days=i, hours=2),
            'location': loc,
        }
    )
    post.tags.set([tags[tag_names[i]]])
    post.save()

print("✅ 3 test posts created.")

import random
import sys
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from faker import Faker
from PIL import Image as PilImage

from posts.models import Image, Post, Tag
from posts.services.image_utils import generate_thumbnail
from posts.services.tag_services import extract_tag_names

fake = Faker()
User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with test users, posts, images and tags"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing fake data before seeding',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='Number of fake users to create (default: 5)',
        )

    def create_fake_post(self, user: User) -> Post:
        """
        Create a fake post for the given user,
        including random tags and images.

        The post caption is generated with lorem text and 1–3 hashtags
        selected from a predefined pool. Each post is tagged accordingly,
        and 1–3 random JPEG images are created and associated with the post,
        including thumbnail generation.

        Args:
            user (User): The user who will be set as the author of the post.

        Returns:
            Post: The created Post instance with tags and images attached.
        """
        tags_pool = ['fitness', 'django', 'ai', 'crypto', 'python', 'travel']

        caption_tags = ' '.join(
            f"#{random.choice(tags_pool)}" for _ in range(
                random.randint(
                    1, 3)))
        post = Post.objects.create(
            author=user,
            caption=fake.sentence() + "\n" + caption_tags
        )

        tag_names = extract_tag_names(post.caption)
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)

        for _ in range(random.randint(1, 3)):
            image = self.generate_fake_image()
            img_obj = Image.objects.create(post=post, image=image)

            thumb = generate_thumbnail(img_obj.image)
            img_obj.thumbnail.save(thumb.name, thumb, save=True)

        return post

    def handle(self, *args: object, **options: dict) -> None:
        """
        Handle command execution.

        If '--clear' is passed, clears existing fake users,
        posts, images and tags.
        If '--count' is passed (or default value is used),
        creates that number of fake users, each with 2–5 posts
        and 1–3 images per post.

        Args:
            *args: Unused positional arguments.
            **options: Contains 'clear' (bool) and 'count' (int) keys.
        """
        user_count = options['count']
        clear_only = options['clear'] and '--count' not in sys.argv

        if options['clear']:
            self.stdout.write(self.style.WARNING(
                "Clearing existing fake data..."
            ))
            self.clear_fake_data()
            self.stdout.write(self.style.SUCCESS("Fake data cleared."))

        if clear_only:
            return

        self.stdout.write(self.style.SUCCESS(
            f"Seeding {user_count} fake user(s)..."))

        users = []
        for i in range(user_count):
            email = f"user{i}@example.com"
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    username=f"user{i}",
                    email=email,
                    password="password1234",
                    is_active=True
                )
                users.append(user)

        self.stdout.write(self.style.SUCCESS(
            "All fake users created with password: password1234"
        ))

        for user in users:
            for _ in range(random.randint(2, 5)):
                self.create_fake_post(user)

        self.stdout.write(self.style.SUCCESS("Seeding complete."))

    def clear_fake_data(self) -> None:
        """
        Remove all fake users, posts, images,
        and unlinked tags created by this seed command.

        Users are identified by email matching 'user<digit>@example.com'.
        All associated posts and images are deleted via Django ORM.
        """
        fake_users = User.objects.filter(
            email__regex=r'^user\d+@example\.com$')

        post_count = 0
        image_count = 0
        file_deleted_count = 0
        tags_checked = set()
        tags_deleted = 0

        for user in fake_users:
            posts = Post.objects.filter(author=user)
            post_count += posts.count()

            for post in posts:
                tags_checked.update(post.tags.all())

                for img in post.images.all():
                    image_count += 1
                    img.delete()

            post_count += posts.count()
            posts.delete()

        for tag in tags_checked:
            if not tag.posts.exists():
                tag.delete()
                tags_deleted += 1

        user_count = fake_users.count()
        fake_users.delete()

        self.stdout.write(self.style.SUCCESS("Clear summary:"))
        self.stdout.write(f" - Users deleted:      {user_count}")
        self.stdout.write(f" - Posts deleted:      {post_count}")
        self.stdout.write(f" - Images deleted:     {image_count}")
        self.stdout.write(f" - Media files deleted:{file_deleted_count}")
        self.stdout.write(
            f" - Tags deleted:       {tags_deleted} (only unused)")

    def generate_fake_image(self) -> ContentFile:
        """
        Generate a random JPEG image as a Django ContentFile.

        Returns:
            ContentFile: In-memory image file ready for
            saving to an ImageField.
        """
        img = PilImage.new(
            "RGB", (800, 600), color=tuple(
                random.randint(
                    0, 255) for _ in range(3)))
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)
        return ContentFile(
            buffer.read(),
            name=f"seed_{random.randint(1000, 9999)}.jpg")

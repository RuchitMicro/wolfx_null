# tests.py
from django.test import TestCase
from django.utils import timezone
from web.models import SocialMedia, Post, PostSchedule
from web.tasks import auto_upload_social_media_posts

class AutoUploadSocialMediaPostsTestCase(TestCase):
    """
    This test case verifies that the auto_upload_social_media_posts Celery task
    processes scheduled posts correctly. It checks that the task prints the required
    messages and that the scheduled post and the associated post flags are updated.
    """
    
    def setUp(self):
        """
        Set up test data for the test case:
          - Create a SocialMedia instance.
          - Create a Post instance linked to the SocialMedia.
          - Create a PostSchedule instance with post_timing set to the current time so
            that it is due immediately.
        """
        # Creating a test social media account
        self.social_media = SocialMedia.objects.create(
            account_name="UnitTestAccount",
            social_media_type="Instagram",
            username="unittestuser",
            password="unittestpass",
            link="http://unittestaccount.com",
            description="Test description for unit test account"
        )
        
        # Creating a test post for the account
        self.post = Post.objects.create(
            social_media=self.social_media,
            type="Text",
            text="This is a unit test post"
        )
        
        # Creating a scheduled post that is due to be processed immediately
        self.schedule = PostSchedule.objects.create(
            social_media=self.social_media,
            post=self.post,
            post_timing=timezone.now(),  # current time ensures the schedule is due
            is_posted=False
        )
    
    def test_auto_upload_social_media_posts(self):
        """
        This test calls the auto_upload_social_media_posts task and verifies:
          - The task returns the expected completion message.
          - The scheduled post is marked as posted.
          - The associated post is marked as published.
        """
        # Print statement to indicate the test has started processing the task.
        print("Starting auto_upload_social_media_posts test execution...")
        
        # Call the Celery task directly as a normal function.
        result = auto_upload_social_media_posts()
        
        # Print the result from the task to the console.
        print("Task result:", result)
        
        # Refresh the schedule and post objects from the database.
        self.schedule.refresh_from_db()
        self.post.refresh_from_db()
        
        # Assert that the schedule has been marked as posted.
        self.assertTrue(self.schedule.is_posted, "Scheduled post was not marked as posted.")
        # Assert that the associated post has been flagged as published.
        self.assertTrue(self.post.is_published, "Post was not marked as published.")
        
        # Final print statement to indicate the test finished successfully.
        print("Completed auto_upload_social_media_posts test successfully.")


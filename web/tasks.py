# tasks.py
from celery       import shared_task
from django.utils import timezone
from datetime     import timedelta, datetime
from .models      import PostSchedule, VideoScriptGeneration, SocialMedia, Post

@shared_task
def auto_upload_social_media_posts():
   """
   Celery task to automatically upload scheduled social media posts.
   
   This task performs the following steps:
   1. Retrieves the current time using Django's timezone utilities.
   2. Queries the PostSchedule model for entries where the scheduled post timing
      (post_timing) is less than or equal to the current time and the post has not
      been processed (is_posted is False).
   3. For each due schedule, it simulates the upload process. In a real-world scenario,
      this is where you would integrate with the API of the corresponding social media
      platform (using the credentials stored in the SocialMedia model).
   4. After a successful "upload," the task marks the schedule as processed by setting
      is_posted to True and flags the associated post as published by updating its
      is_published field.
   5. Saves the updated states to the database.
   
   Note:
   - Replace the print statement with your actual API integration code.
   - Handle exceptions and retries as needed for production-level code.
   """
   # Get the current time (timezone-aware)
   current_time = timezone.now()
   
   # Query all PostSchedule objects that are due for posting and have not been processed.
   due_schedules = PostSchedule.objects.filter(post_timing__lte = current_time, is_posted = False)
   
   # Iterate through each due schedule to process the auto upload.
   for schedule in due_schedules:
      # Here, implement the logic to upload the post.
      # For now, we simulate this by printing a message.
      print(f"Uploading post ID {schedule.post.id} for social media account {schedule.social_media.account_name}")
      
      # After successful upload, mark the schedule as posted and the associated post as published.
      schedule.is_posted = True
      schedule.post.is_published = True
      
      # Save the updated post and schedule to the database.
      schedule.post.save()
      schedule.save()
   
   # Return a completion message (useful for monitoring/logging purposes).
   return "Completed auto uploading social media posts."


@shared_task
def auto_create_social_media_post():
   """
   Celery task to automatically create and schedule a social media post based on the posting timetable.
   
   For each SocialMedia account:
   1. Iterate over all timetable entries (which specify a day and time to post).
   2. Compute the next occurrence (DateTime) of that timetable slot relative to now.
   3. Check if an unsent PostSchedule entry exists with that exact post_timing.
   4. If no such entry exists, automatically generate a post:
      a. Create a VideoScriptGeneration record with default/sample content.
      b. Run its full process to simulate generating a video script and video file.
      c. Create a new Post record using the generated content.
      d. Create a new PostSchedule record scheduled for the computed next occurrence.
   
   Returns:
   A summary message indicating the number of posts auto-created and scheduled.
   """
   now = timezone.now()
   created_count = 0

   # Iterate through all SocialMedia accounts.
   for social_media in SocialMedia.objects.all():

      # Iterate over each posting timetable for the account.
      for timetable in social_media.timetables.all():
         # Compute the next occurrence of the timetable entry.
         target_day  = timetable.day_of_week  # integer (0=Monday,...,6=Sunday)
         current_day = now.weekday()  # integer (0=Monday,...,6=Sunday)
         
         # Calculate days ahead: if the target day is today but the posting time has passed, roll over to next week.
         days_ahead = target_day - current_day
         if days_ahead < 0 or (days_ahead == 0 and now.time() > timetable.posting_time):
               days_ahead += 7
         
         # Calculate next occurrence date
         next_occurrence_date = (now + timedelta(days=days_ahead)).date()
         # Combine the date with the posting time from the timetable.
         next_occurrence = timezone.make_aware(
               datetime.combine(next_occurrence_date, timetable.posting_time)
         )
         
         # Ensure next_occurrence is in the future.
         if next_occurrence < now:
               next_occurrence += timedelta(days=7)
         
         # Check if there's already an unsent PostSchedule entry for this social_media at this scheduled time.
         existing_schedule    =  PostSchedule.objects.filter(
               social_media   =  social_media,
               is_posted      =  False,
               post_timing    =  next_occurrence
         )
         
         if not existing_schedule.exists():
               # Create a VideoScriptGeneration record using the social media's default prompt if available.
               video_script_record  = VideoScriptGeneration.objects.create(
                  source            = None,  # Optionally set a default source URL.
                  topic             = f"Auto-generated topic for {social_media.account_name}",
                  content           = "This is auto-generated content for creating a video script.",
                  llm_prompt        = social_media.default_llm_prompt or VideoScriptGeneration.DEFUALT_PROMPT
               )
               
               # Run the full process to generate the video script and create the video.
               video_script_record.run_full_process()
               
               # Create a new Post record using the generated video information.
               new_post          =  Post.objects.create(
                  type           =  'Video',  # Assuming a video post type since we are generating a video.
                  text           =  video_script_record.generated_video_script,
                  video          =  video_script_record.video_file,
                  is_published   =  False
               )
               
               # Create a PostSchedule record for the computed next occurrence.
               PostSchedule.objects.create(
                  social_media   =  social_media,
                  post           =  new_post,
                  post_timing    =  next_occurrence,
                  is_posted      =  False
               )
               
               created_count += 1
               print(f"Auto-created and scheduled post for {social_media.account_name} at {next_occurrence}")

   return f"Auto-created and scheduled {created_count} posts."


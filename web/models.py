# Code generated from Spectre
from django.db                          import models, IntegrityError
from django.db.models.aggregates        import Max
from django.contrib.sessions.models     import Session
from django.contrib.auth.models         import User
from django.db.models                   import Avg
from django.core.exceptions             import ValidationError
from django.core.serializers            import serialize

# Timezone
from django.utils   import timezone

# Signals
from django.db.models.signals       import post_save
from django.dispatch                import receiver

# HTML Safe String  
from django.utils.safestring        import mark_safe

# Send mail Django's Inbuilt function
from django.core.mail               import send_mail
from django.template.loader         import render_to_string

# Json
import json

# Forms
from django                 import forms       

# Regex
import re

# Django Settings
from django.conf            import settings

# UUID
import uuid

# Django Validators
from django.core.validators import MaxValueValidator, MinValueValidator

# Urllib
import urllib.parse

# Simple History Model
from simple_history.models import HistoricalRecords

# Model Utils
from model_utils        import FieldTracker
from model_utils.fields import MonitorField, StatusField






class CommonModel(models.Model):
    extra_params    =   models.JSONField        (blank=True, null=True)
    created_at      =   models.DateTimeField    (auto_now_add=True, blank=True, null = True)
    updated_at      =   models.DateTimeField    (auto_now=True, blank=True, null=True)
    created_by      =   models.CharField        (max_length=300, blank=True, null=True)
    updated_by      =   models.CharField        (max_length=300, blank=True, null=True)
    
    history                 =   HistoricalRecords(inherit=True)
    tracker                 =   FieldTracker()

    admin_meta      =   {}
    
    class Meta:
        abstract = True

    # Helper function to get json data of the model
    def get_json(self):
        # Serialize the model instance into JSON format
        data = serialize('json', [self], ensure_ascii=False)
        
        # Convert the serialized data into a Python object
        data = json.loads(data)
        
        # Return the first item in the list as we are serializing a single instance
        return data[0] if data else {}


# Global Settings
class SiteSetting(CommonModel):
    logo                    =   models.ImageField   (blank=True,null=True,upload_to='settings/')
    favicon                 =   models.FileField    (blank=True,null=True,upload_to='settings/')
    global_head             =   models.TextField    (blank=True,null=True, help_text='Common <head> data. It will appear in all pages.')

    address                 =   models.TextField    (blank=True,null=True,max_length=500)
    contact_number          =   models.CharField    (blank=True,null=True,max_length=13)
    email                   =   models.EmailField   (blank=True,null=True)
    gst                     =   models.CharField    (blank=True,null=True,max_length=15, help_text="GST Number")
    extra_contact_details   =   models.TextField           (blank=True,null=True)

    facebook                =   models.URLField     (blank=True,null=True,max_length=100)
    instagram               =   models.URLField     (blank=True,null=True,max_length=100)
    twitter                 =   models.URLField     (blank=True,null=True,max_length=100)
    linkedin                =   models.URLField     (blank=True,null=True,max_length=100)

    vision                  =   models.TextField    (blank=True,null=True)
    mission                 =   models.TextField    (blank=True,null=True)
    values                  =   models.TextField    (blank=True,null=True)
    brochure                =   models.FileField    (blank=True,null=True,upload_to='settings/')
    
    navigation_menu         =   models.JSONField    (blank=True, null=True)

    about_us                =   models.TextField       (blank=True,null=True)
    terms_and_conditions    =   models.TextField       (blank=True,null=True)
    privacy_policy          =   models.TextField       (blank=True,null=True)
    return_policy           =   models.TextField       (blank=True,null=True)
    disclaimer              =   models.TextField       (blank=True,null=True)

    robots                  =   models.FileField    (blank=True,null=True,upload_to='settings/')
    

    # JSON FIELD SCHEMA
    key_value_pair_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "navMenu": {
            "type": "array",
            "items": {
                "$ref": "#/definitions/menuItem"
            }
            }
        },
        "definitions": {
            "menuItem": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Unique identifier for the menu item."
                },
                "label": {
                    "type": "string",
                    "description": "Display text for the menu item."
                },
                "url": {
                    "type": "string",
                    "format": "uri",
                    "description": "URL link for the menu item."
                },
                "children": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/menuItem"
                },
                "description": "Nested menu items under this menu item."
                }
            },
            "required": ["id", "label"],
            "additionalProperties": False
            }
        }
    }

        
    admin_meta = {
        "json_fields": {
            "navigation_menu": {"schema":  json.dumps(key_value_pair_schema)},
        }
    }
    
    def __str__(self):
        return 'Edit Site Settings'

    class Meta:
        verbose_name_plural = "Site Setting"
    
    def save(self, *args, **kwargs):
        super(SiteSetting, self).save(*args, **kwargs)


# Image Master
class ImageMaster(CommonModel):
    name                =   models.CharField        (max_length=300)
    image               =   models.ImageField       (upload_to="image_master/")
    
    created_at          =   models.DateTimeField    (auto_now_add=True, blank=True, null = True)
    updated_at          =   models.DateTimeField    (auto_now=True, blank=True, null=True)
    
    admin_meta = {
        'list_display': ['name', 'image','__str__', 'created_at', 'updated_at', 'created_by', 'updated_by',],   
    }

    def __str__(self):
        return mark_safe(
            '<div style="height:200px;width:200px;"><img src='+self.image.url+' style="object-fit:contain;height:100%;width:100%" alt=""></div>'
        )


# File Master
class FileMaster(CommonModel):
    name                =   models.CharField    (max_length=300)
    file                =   models.FileField    (upload_to='file_master/')

    created_at          =   models.DateTimeField    (auto_now_add=True, blank=True, null = True)
    updated_at          =   models.DateTimeField    (auto_now=True, blank=True, null=True)

    admin_meta = {
        'list_display': ['name', 'file', '__str__', 'created_at', 'updated_at', 'created_by', 'updated_by'],   
    }

    def __str__(self):
        return str(self.name)

# Contact
class Contact(CommonModel):
    full_name       =   models.CharField(max_length=300)
    email_id        =   models.EmailField(max_length=300)
    phone_number    =   models.CharField(max_length=20)
    company_name    =   models.CharField(max_length=300)  # Added this field
    budget          =   models.CharField(max_length=100)  # Added this field to store budget range
    services        =   models.TextField()  # Added this field to store selected services
    requirement     =   models.TextField()
    email_ok        =   models.BooleanField(default=False)
    journey_path    =   models.TextField(
        blank=True, null=True, help_text='A complete URL trace of the user journey that led them to fill the form.',
    )
    status          =   models.TextField(default='New', null=True, blank=True)

    admin_meta =    {
        'list_display'      :   ("full_name","email_id","phone_number","company_name","budget","services","requirement","status","journey_path_as_list","created_at"),
        'list_per_page'     :   50,
        'list_filter'       :   ("budget","status","created_at",),
        'search_fields'     :   ("full_name","email_id","phone_number","company_name","budget",),
    }

    def journey_path_as_list(self):
        paths = self.journey_path.split('|') if self.journey_path else []
        html = ''.join([f'<div style="display: inline; background-color: #e0e0e0; padding: 5px; border-radius: 4px;">{path}</div>' for path in paths])
        return mark_safe(f"<div style='display: flex; grid-gap: 5px; flex-wrap: wrap;'>{html}</div>")
    def __str__(self):
        return str(self.full_name)

    # Notification to Support about a new entry
    def send_mail_notification(self):
        from django.template.loader import render_to_string
        from django.core.mail import send_mail

        msg_html = render_to_string('email/new_enquiry.html', {'enquiry': self})
        send_mail(
            'New enquiry from WOLFx',
            'Hello',
            'hello@wolfx.io',
            ['hello@wolfx.io'],
            fail_silently=True,
            html_message=msg_html,
        )

    # Notification to User
    def send_mail_greeting(self):
        from django.template.loader import render_to_string
        from django.core.mail import send_mail

        msg_html = render_to_string('email/thank_you_for_contacting.html', {'enquiry': self})
        send_mail(
            'WOLFx: Thank you for Contacting us',
            'Hello',
            'hello@wolfx.io',
            [self.email_id],
            fail_silently=True,
            html_message=msg_html,
        )


# ------------------------------------------------------------------------------
# SocialMedia model stores social media account details.
# ------------------------------------------------------------------------------
class SocialMedia(CommonModel):
    account_name      = models.CharField(max_length=300)
    social_media_type = models.CharField(max_length=300, choices=[
        ('Instagram', 'Instagram'),
        ('YouTube', 'YouTube'),
        ('Facebook', 'Facebook'),
        ('LinkedIn', 'LinkedIn'),
        ('Twitter', 'Twitter'),
        ('Pinterest', 'Pinterest'),
        ('Snapchat', 'Snapchat'),
        ('TikTok', 'TikTok'),
        ('Other', 'Other')
    ])
    username          = models.CharField(max_length=300)
    password          = models.CharField(max_length=300)
    link              = models.URLField(max_length=300, blank=True, null=True)
    description       = models.TextField(blank=True, null=True)
    image             = models.ImageField(upload_to='social_media/', blank=True, null=True)

    default_llm_prompt = models.TextField(
        blank=True, null=True, help_text='Default prompt for LLM to auto generate content specific to this account.'
    )

    admin_meta = {
        'list_display': ['account_name', 'link', '__str__', 'created_at', 'updated_at', 'created_by', 'updated_by'],   
        'inline': [
            {'SocialMediaTimetable': 'social_media'},
        ],
    }

    def __str__(self):
        # Return the account_name for readable representation.
        return str(self.account_name)
    
    


# ------------------------------------------------------------------------------
# SocialMediaTimetable model represents the recurring posting schedule for a SocialMedia account.
# ------------------------------------------------------------------------------
class SocialMediaTimetable(CommonModel):
    # Define choices for days of the week (Monday=0, Sunday=6)
    DAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    # Foreign key linking this schedule to a specific SocialMedia account.
    social_media = models.ForeignKey(
        SocialMedia, 
        on_delete=models.CASCADE,
        related_name='timetables'
    )
    # Day of week when the post should be published.
    day_of_week = models.IntegerField(
        choices = DAY_CHOICES, 
        help_text = "Day of week when the post should be published"
    )
    # Time of day when the post should be published.
    posting_time = models.TimeField(
        help_text = "Time of day when the post should be published"
    )
    
    class Meta:
        unique_together = ('social_media', 'day_of_week', 'posting_time')
    
    def __str__(self):
        # Return a string like "Instagram: Monday 09:00"
        day_str = dict(self.DAY_CHOICES).get(self.day_of_week, "Unknown")
        return f"{self.social_media.account_name}: {day_str} {self.posting_time.strftime('%H:%M')}"


# ------------------------------------------------------------------------------
# Post model holds details of a social media post.
# ------------------------------------------------------------------------------
class Post(CommonModel):
    type         = models.CharField(max_length=300, choices=[
        ('Image', 'Image'),
        ('Video', 'Video'),
        ('Text', 'Text'),
        ('Link', 'Link'),
        ('Other', 'Other')
    ])
    text         = models.TextField(blank=True, null=True, help_text='Text content of the post')
    image        = models.TextField(blank=True, null=True, help_text='Absolute Media URL')
    video        = models.TextField(blank=True, null=True, help_text='Absolute Media URL')
    link         = models.URLField(max_length=300, blank=True, null=True)

    # Flag to indicate whether this post has been published.
    is_published = models.BooleanField(default=False)

    admin_meta = {
        'list_display': ['__str__', 'created_at', 'updated_at', 'created_by', 'updated_by'],   
    }

    def __str__(self):
        # Display the social media account and post id.
        return 'Post ID:' + str(self.id)

# ------------------------------------------------------------------------------
# PostSchedule model is used to schedule posts for automatic upload.
# ------------------------------------------------------------------------------
class PostSchedule(CommonModel):
    social_media = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    # Link the schedule to a specific post.
    post         = models.ForeignKey(Post, on_delete=models.CASCADE)
    # Use DateTimeField so that both date and time are considered.
    post_timing  = models.DateTimeField(blank=True, null=True)
    # Flag to mark whether the scheduled post has been processed.
    is_posted    = models.BooleanField(default=False)

    def __str__(self):
        return f"Schedule for {self.social_media.account_name} at {self.post_timing}"
    

# ------------------------------------------------------------------------------
# VideoScriptGeneration model handles the process of generating a video script
# based on a blog source, topic, big text, and an LLM prompt.
#
# This model accepts user inputs for the source of a blog, its topic,
# the full blog content, and a prompt for the language model. It includes
# member functions that simulate generating a video script and then creating
# a video from that script.
# ------------------------------------------------------------------------------
class VideoScriptGeneration(CommonModel):
    DEFUALT_PROMPT = """write a 60-second viral video script about this topic , keep the tone Conversational, direct, and provocative. I want the script to be natural, Speak like a person, not a narrator. Infuse curiosity, skepticism, and boldness. Challenge authority where relevant. Avoid complex jargon—keep it simple and sharp. Keep the script short, use punchy sentences to build energy. Break rhythm with longer lines when explaining complex ideas. Insert pauses with dashes or ellipses for dramatic effect. Aim for a natural, spoken-word cadence. For the title of the script I need A bold, intriguing headline that instantly conveys the topic or controversy it Must feel urgent or provocative to spark curiosity. Example: "The $LIBRA Scandal: Argentina's Presidential Crypto Catastrophe" For the opening hook I need 5 seconds of script that should Start with a provocative, emotionally charged line. Leverage curiosity, controversy, or shock value. Use cultural or financial buzzwords like "classic crypto pump-and-dump". Example: "Argentina's president is facing impeachment calls... after what looks like a classic crypto pump-and-dump." The main body of our script needs to Use the 'THEREFORE, BUT' framework where we should have context , conflict, insight. Context should Set the stage with familiar, relatable information. Conflict should Introduce an unexpected twist or challenge. Insight should Deliver a compelling explanation or key insight. Maintain a natural, conversational tone. Vary sentence length to create rhythm. Include 3-4 compelling facts or figures. Facts should spark surprise, disbelief, or curiosity. Example: 40,000 investors believed in $LIBRA. The token crashed within days, wiping out millions. Now, impeachment calls are flooding in. Conclude with a powerful, thought-provoking statement. Use language that evokes emotion and leaves viewers pondering the broader implications. Example: "The $LIBRA crash isn’t just Argentina’s problem—it’s a global warning. When hype replaces due diligence, the public pays the price." Include a call to action but Avoid generic commands like "Follow us". Instead, leave viewers with a warning, insight, or challenge. Example: "The future of real estate is fractional, digital, and accessible. Join the movement. Take back the market.". 
        Please avoid using structural labels such as 'HOOK,' 'OPENING,' 'INTRO,' or phrases like 'here's the lowdown' or 'here's the kicker' in the script. I want the entire script to read as a natural, flowing narrative—just like a clean news article or social media caption. No need to call out sections. Just give me the finished script in paragraph form, maintaining a strong tone, engaging style, and clear storytelling without introducing each part.
        Directly give me the script and do not include any explanation , we need to just have the script. do not bifurcate the sections of the script your output should be a huge paragraph of script"""

    # Field to accept a URL for the blog source if applicable.
    source = models.URLField(max_length = 300, blank = True, null = True, help_text = "URL of the text source (if available)")
    
    # Field to accept the topic of the script.
    topic = models.CharField(max_length = 300,blank = True, null = True)
    
    # Field to accept the main text content or big text from the blog.
    content = models.TextField(help_text = "Detailed content from the source", blank = True, null = True)
    
    # Field to accept the LLM prompt for generating the video script.
    llm_prompt = models.TextField(help_text = "Prompt for the LLM to generate a video script", blank = True, null = True, default=DEFUALT_PROMPT)
    
    # Field to store the generated video script.
    generated_video_script = models.TextField(blank = True, null = True, help_text = "The generated video script based on the LLM prompt and text content")
    
    # Field to store the generated video file.
    video_file = models.FileField(upload_to = 'video_scripts/', blank = True, null = True, help_text = "Generated video file from the video script")
    
    # Field to track the processing status of the video script generation and video creation.
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    status = models.CharField(max_length = 20, choices = STATUS_CHOICES, default = 'pending', help_text = "Processing status")
    
    # Field to store error messages in case the generation process fails.
    error_message = models.TextField(blank = True, null = True, help_text = "Error message if processing fails")

    admin_meta = {
        'list_display': ['topic', 'status', 'created_at', 'updated_at'],
    }

    def __str__(self):
        # Returns the blog topic as the string representation of the model.
        return self.topic

    def generate_video_script(self):
        """
        Generates a video script based on the provided blog content, topic, and LLM prompt.
        This member function simulates an integration with an LLM to produce a video script.
        
        Steps:
          1. Update the status to 'in_progress' to indicate that processing has started.
          2. Combine blog_topic, blog_content, and llm_prompt into a single prompt.
          3. Simulate calling an LLM to generate a video script.
          4. Update the generated_video_script field with the result.
          5. Update the status to 'completed' upon success.
          6. Handle exceptions by setting the status to 'failed' and storing the error message.
        
        Returns:
            The generated video script as a string if successful.
        
        Raises:
            Exception: Propagates any exception that occurs during processing.
        """
        try:
            # Mark the status as in_progress.
            self.status = 'in_progress'
            self.save(update_fields=['status'])
            
            # Construct a combined prompt using the blog topic, content, and the LLM prompt provided.
            combined_prompt = (
                f"Topic: {self.topic}\n"
                f"Content: {self.content}\n"
                f"LLM Prompt: {self.llm_prompt}\n"
                "Generate a detailed video script based on the above information."
            )
            
            # Simulate the process of generating a video script.
            # In production, this would involve making an API call to a language model (e.g., GPT).
            generated_script = f"Video Script based on: {combined_prompt}"
            
            # Save the generated script to the model and update the status.
            self.generated_video_script = generated_script
            self.status = 'completed'
            self.save(update_fields=['generated_video_script', 'status'])
            
            return generated_script
        except Exception as error:
            # If an error occurs, mark the process as failed and store the error message.
            self.status = 'failed'
            self.error_message = str(error)
            self.save(update_fields=['status', 'error_message'])
            raise error

    def create_video(self):
        """
        Creates a video file based on the generated video script.
        This member function simulates the video creation process.
        
        Steps:
          1. Check that a video script has been generated.
          2. Simulate the creation of a video file from the script.
          3. Save the path to the video file in the video_file field.
          4. Return the file path of the generated video.
        
        Returns:
            The file path of the generated video if successful.
        
        Raises:
            ValueError: If a video script has not been generated.
            Exception: Propagates any exception that occurs during video creation.
        """
        # Ensure that the video script exists before attempting video creation.
        if not self.generated_video_script:
            raise ValueError("Video script has not been generated yet.")
        
        try:
            # Simulate video creation process.
            # In a production scenario, integrate with video creation libraries or services here.
            simulated_video_file_path = "video_scripts/generated_video.mp4"
            
            # Save the simulated video file path.
            self.video_file = simulated_video_file_path
            self.save(update_fields=['video_file'])
            
            return simulated_video_file_path
        except Exception as error:
            # On failure, update the status and record the error.
            self.status = 'failed'
            self.error_message = str(error)
            self.save(update_fields=['status', 'error_message'])
            raise error

    def run_full_process(self):
        """
        Runs the complete process of generating a video script and then creating a video.
        
        This convenience function sequentially calls generate_video_script and create_video,
        and returns a summary of the results.
        
        Returns:
            A dictionary containing:
              - "generated_video_script": The video script generated by the LLM.
              - "video_file": The file path of the generated video.
        """
        generated_script = self.generate_video_script()
        video_file_path = self.create_video()
        return {
            "generated_video_script": generated_script,
            "video_file": video_file_path,
        }





# Blog Models
class BlogCategory(CommonModel):
    category    =   models.CharField(max_length=100, unique=True)
    slug        =   models.SlugField(max_length=100, unique=True)
    image       =   models.FileField(blank=True, null=True, upload_to='blog_category/')
    parent      =   models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        # Recursively build the full category path
        if self.parent:
            return f"{self.parent} -> {self.category}"
        return self.category
    
    def clean(self):
        # Ensure that no cyclic dependencies are created
        if self.parent:
            parent = self.parent
            while parent is not None:
                if parent == self:
                    raise ValidationError("A category cannot be a parent of itself or one of its descendants.")
                parent = parent.parent

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Blog Categories"
        ordering = ['category']

class Blog(CommonModel):

    head_default='''<meta name="title" content=" ">
    <meta name="description" content=" ">
    <meta name="keywords" content=" ">
    <meta name="robots" content="index, follow">'''

    title               =   models.CharField        (max_length=200)
    sub_title           =   models.CharField        (max_length=200, blank=True ,null=True)
    thumbnail           =   models.ImageField       (upload_to="blog/")
    category            =   models.ForeignKey       (BlogCategory, null=True, on_delete=models.SET_NULL)
    featured_text       =   models.TextField           (null=True, blank=True)
    text                =   models.TextField           (null=True, blank=True)
    slug                =   models.SlugField        (unique=True)
    readtime            =   models.CharField        (max_length=200,null=True, blank=True)
    tags                =   models.TextField        (null=True, blank=True, default='all')
    head                =   models.TextField        (null=True, blank=True, default=head_default)
    
    order_by            =   models.IntegerField     (default=0)
    
    created_at          =   models.DateTimeField    (auto_now_add=True, blank=True, null=True)
    updated_at          =   models.DateTimeField    (auto_now=True, blank=True, null=True)
    created_by          =   models.CharField        (max_length=300)

    admin_meta =    {
        'list_display'      :   ("__str__","category","created_at","updated_at"),
        'list_editable'     :   ("category",),
        'list_per_page'     :   50,
        'list_filter'       :   ("category",),
        'inline'            :   [
            {'BlogImage': 'blog'}
        ]
    }

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = "Blog"
        ordering = ['order_by'] #Sort in desc order

class BlogImage(CommonModel):
    blog                =   models.ForeignKey       (Blog, on_delete=models.CASCADE)
    image               =   models.ImageField       (upload_to="blog_images/")
    order_by            =   models.IntegerField     (default=0)

    def __str__(self):
        return str(self.blog)

    class Meta:
        verbose_name_plural = "Blog Image"
        ordering = ['order_by'] #Sort in desc order
    

# Case Study
class CaseStudyCategory(CommonModel):
    category    =   models.CharField    (max_length=100, unique=True)
    slug        =   models.SlugField    (max_length=100, unique=True)
    image       =   models.FileField    (blank=True,null=True,upload_to='case_study_category/')
   
    order_by    =   models.IntegerField (default=0)

    admin_meta =    {
        'list_display'      :   ("__str__","order_by"),
        'list_editable'     :   ("order_by",),
        'list_per_page'     :   50,
    }

    def __str__(self):
        return str(self.category)
    
    class Meta:
        verbose_name_plural = "Case Study Category"
        ordering = ['order_by']

class CaseStudy(CommonModel):
    head_default='''<meta name="title" content=" ">
<meta name="description" content=" ">
<meta name="keywords" content=" ">
<meta name="robots" content="index, follow">'''

    title               =   models.CharField        (max_length=200)
    sub_title           =   models.CharField        (max_length=200, blank=True ,null=True)
    category            =   models.ForeignKey       (CaseStudyCategory, null=True, on_delete=models.SET_NULL)
    thumbnail           =   models.ImageField       (upload_to="case-study-thumbnail/")
    featured_text       =   models.TextField        (null=True, blank=True)
    text                =   models.TextField        (null=True, blank=True)
    slug                =   models.SlugField        (unique=True)
    tags                =   models.TextField        (null=True, blank=True, default='all')
    head                =   models.TextField        (null=True, blank=True, default=head_default)
    
    related_case_study  =   models.ManyToManyField   ('self', blank=True, related_name='related_case_study')

    is_featured         =   models.BooleanField     (default=False)
    order_by            =   models.IntegerField     (default=0)
    
    admin_meta =    {
        'list_display'      :   ("__str__","is_featured","order_by","created_at","updated_at"),
        'list_editable'     :   ("order_by","is_featured",),
        'list_per_page'     :   50,
        'list_filter'       :   ("order_by","is_featured",),
        'filter_horizontal' :   ('related_case_study',),
        'inline'            :   [
            {'CaseStudyFAQ': 'case_study'}
        ],
    }

    def __str__(self):
        return str(self.title)

    def split_tags(self):
        return [t for t in self.tags.split(',')]

    class Meta:
        verbose_name_plural = "Case Study"
        ordering = ['order_by'] #Sort in desc order

class CaseStudyFAQ(CommonModel):
    case_study      =   models.ForeignKey       (CaseStudy, on_delete=models.CASCADE)
    question        =   models.CharField        (max_length=300)
    answer          =   models.TextField               ()
    order_by        =   models.IntegerField     (default=0)

    def __str__(self):
        return str(self.question)

    class Meta:
        verbose_name_plural = "Case Study FAQ"
        ordering = ['order_by'] #Sort in desc order



    
# FAQ
class FAQCategory(CommonModel):
    category    =   models.CharField    (max_length=100, unique=True)
    slug        =   models.SlugField    (max_length=100, unique=True)
    image       =   models.FileField    (blank=True,null=True,upload_to='faq_category/')
    
    order_by    =   models.IntegerField     (default=0)

    admin_meta =    {
        'list_display'      :   ("__str__","order_by"),
        'list_editable'     :   ("order_by",),
        'list_per_page'     :   50,
    }

    def __str__(self):
        return str(self.category)

    class Meta:
        ordering = ['order_by']    

class FAQ(CommonModel):
    category    =   models.ForeignKey       (FAQCategory, null=True, on_delete=models.SET_NULL)
    question    =   models.CharField        (max_length=300)
    answer      =   models.TextField               ()

    order_by    =   models.IntegerField     (default=0)
    
    admin_meta =    {
        'list_display'      :   ("__str__","answer","category","order_by"),
        'list_editable'     :   ("order_by",),
        'list_per_page'     :   50,
    }

    def __str__(self):
        return str(self.question)

    class Meta:
        ordering = ['order_by'] #Sort in desc order




# Dynamic Head
# Injects data inside <head> of a specific target url
# Used for SEO
class Head(CommonModel):
    target_url  =   models.URLField     (unique=True, help_text="Enter absolute URL of the target.  <br> Ex: https://wolfx.io/blog <br> https://wolfx.io/blog/ <br> https://wolfx.io/blog?category=UI-UX ")
    head        =   models.TextField    (help_text="Head Data")

    def __str__(self):
        return str(self.target_url)

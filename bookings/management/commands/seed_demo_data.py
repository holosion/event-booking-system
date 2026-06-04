from datetime import date, time, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from bookings.models import Category, Event


CATEGORIES = [
    ('Music', 'Concerts, festivals, listening sessions, and live performances.'),
    ('Technology', 'Hackathons, product demos, tech talks, and workshops.'),
    ('Business', 'Networking, seminars, pitch nights, and conferences.'),
    ('Food & Drink', 'Tastings, pop-ups, chef tables, and food festivals.'),
    ('Sports & Fitness', 'Matches, training sessions, races, and active meetups.'),
    ('Arts & Culture', 'Gallery nights, poetry, theatre, dance, and cultural showcases.'),
    ('Education', 'Classes, study days, bootcamps, and professional learning.'),
    ('Health & Wellness', 'Mindfulness, care, nutrition, and wellness experiences.'),
    ('Community', 'Neighborhood gatherings, volunteer days, and public forums.'),
    ('Travel & Outdoor', 'Outdoor adventures, tours, nature walks, and day trips.'),
    ('Fashion', 'Runway shows, styling sessions, markets, and designer showcases.'),
    ('Family', 'Parent-friendly activities, youth programs, and all-ages events.'),
    ('Film & Media', 'Screenings, creator talks, podcast rooms, and media workshops.'),
    ('Gaming', 'Esports, board games, tournaments, and interactive play sessions.'),
]

EVENTS = [
    ('Neon Nights Festival', 'Music', 'Downtown Park', 500, 45, 18, 30, 'A high-energy evening of DJs, food stalls, and live headline performances.'),
    ('Jazz Under the Stars', 'Music', 'Riverside Amphitheater', 200, 30, 19, 0, 'Smooth jazz, open-air seating, and a relaxed night beside the river.'),
    ('Acoustic Sunday Sessions', 'Music', 'Garden Lounge', 90, 16, 15, 30, 'A warm afternoon of stripped-back sets from local acoustic artists.'),
    ('Gospel Harmony Night', 'Music', 'Community Worship Hall', 350, 58, 17, 0, 'Choirs and soloists come together for an uplifting concert experience.'),
    ('Indie Band Showcase', 'Music', 'Warehouse Stage', 180, 72, 20, 0, 'Discover rising indie bands in an intimate standing-room venue.'),
    ('Django Developers Meetup', 'Technology', 'Innovation Hub', 80, 14, 18, 30, 'Developers share practical Django patterns, deployment tips, and project demos.'),
    ('AI and Machine Learning Workshop', 'Technology', 'Tech Campus Room 3', 40, 10, 10, 0, 'A hands-on workshop covering model basics, prompts, and useful AI workflows.'),
    ('Cybersecurity Basics Lab', 'Technology', 'Digital Skills Center', 65, 36, 9, 30, 'A guided lab on passwords, phishing awareness, and secure web practices.'),
    ('Cloud Deployment Bootcamp', 'Technology', 'Founders Lab', 55, 50, 13, 0, 'Learn how to ship a web app with environment variables, databases, and logs.'),
    ('Women in Tech Roundtable', 'Technology', 'Innovation Hub Auditorium', 120, 83, 17, 30, 'A conversation with women building products, teams, and careers in technology.'),
    ('Startup Pitch Night', 'Business', 'Co-Work Space Hall', 120, 18, 18, 0, 'Founders pitch new ideas to mentors, investors, and curious community members.'),
    ('Small Business Growth Clinic', 'Business', 'Enterprise Center', 75, 27, 9, 0, 'Practical coaching on pricing, customer discovery, and managing cash flow.'),
    ('Marketing Strategy Masterclass', 'Business', 'Summit Boardroom', 100, 41, 14, 0, 'Build sharper campaigns with positioning, audience research, and content planning.'),
    ('Finance for Founders', 'Business', 'City Business School', 85, 64, 11, 0, 'A clear session on budgets, forecasts, bookkeeping, and investor-ready numbers.'),
    ('Leadership Breakfast Forum', 'Business', 'Grand Hotel Conference Room', 160, 91, 8, 0, 'A morning forum for managers and team leads focused on practical leadership.'),
    ('Street Food Carnival', 'Food & Drink', 'Market Square', 600, 21, 12, 0, 'Food vendors serve bold street eats, fresh drinks, and festival favorites.'),
    ('Chef Table Tasting', 'Food & Drink', 'Lakeview Restaurant', 32, 33, 19, 30, 'A limited-seat tasting menu with chef commentary and paired drinks.'),
    ('Coffee Roasters Meetup', 'Food & Drink', 'Bean House Cafe', 70, 46, 10, 30, 'Coffee lovers compare roasts, brewing methods, and local cafe stories.'),
    ('Farmers Market Brunch', 'Food & Drink', 'Green Market Yard', 140, 61, 9, 30, 'A brunch built around seasonal produce, artisan breads, and fresh juice.'),
    ('Dessert Pop-Up Evening', 'Food & Drink', 'Sweet Studio', 95, 79, 17, 0, 'Bakers and pastry makers present a rotating menu of desserts and treats.'),
    ('City 10K Fun Run', 'Sports & Fitness', 'Central Stadium Gate', 900, 25, 7, 0, 'A friendly 10K route for runners, walkers, clubs, and first-time racers.'),
    ('Sunrise Yoga Flow', 'Sports & Fitness', 'Botanical Gardens Lawn', 120, 12, 6, 30, 'Start the day with a guided yoga flow and calm breathing practice.'),
    ('Community Football Final', 'Sports & Fitness', 'City Sports Grounds', 1200, 40, 16, 0, 'Local teams compete in a lively final with music and family seating.'),
    ('Basketball Skills Camp', 'Sports & Fitness', 'Indoor Sports Arena', 150, 54, 10, 0, 'Coaches lead drills on shooting, movement, defense, and team play.'),
    ('Cycling Safety Ride', 'Sports & Fitness', 'River Trail Start Point', 180, 68, 8, 0, 'A guided group ride focused on road safety and confident cycling.'),
    ('Gallery After Hours', 'Arts & Culture', 'Modern Arts Gallery', 110, 19, 18, 30, 'A relaxed evening of exhibits, artist talks, and ambient music.'),
    ('Poetry and Spoken Word Night', 'Arts & Culture', 'Black Box Theater', 130, 28, 19, 0, 'Poets, storytellers, and performers share new work with a live audience.'),
    ('Traditional Dance Showcase', 'Arts & Culture', 'Cultural Center Stage', 300, 44, 17, 30, 'Dance groups celebrate heritage through costumes, rhythm, and movement.'),
    ('Makers Craft Fair', 'Arts & Culture', 'Artisan Courtyard', 220, 59, 11, 0, 'Browse handmade crafts, prints, ceramics, jewelry, and creative demonstrations.'),
    ('Community Theatre Premiere', 'Arts & Culture', 'Town Playhouse', 240, 87, 19, 30, 'A new local stage production with cast talkback after the performance.'),
    ('Data Analysis Short Course', 'Education', 'Learning Lab A', 45, 22, 9, 0, 'A beginner-friendly introduction to spreadsheets, charts, and data storytelling.'),
    ('Exam Prep Study Marathon', 'Education', 'Public Library Hall', 160, 34, 8, 30, 'A structured study day with quiet zones, tutors, and revision breaks.'),
    ('Career Skills Workshop', 'Education', 'Youth Skills Center', 90, 49, 13, 30, 'Improve CVs, interviews, workplace communication, and job search strategy.'),
    ('Language Exchange Evening', 'Education', 'Community Library Cafe', 80, 63, 18, 0, 'Practice new languages through guided conversation tables and friendly games.'),
    ('Science Teachers Forum', 'Education', 'STEM Resource Center', 100, 96, 10, 0, 'Teachers share classroom experiments, assessment ideas, and lesson resources.'),
    ('Mindfulness Retreat Day', 'Health & Wellness', 'Wellness Garden', 85, 24, 9, 0, 'A calm day of guided meditation, reflection, breathing, and gentle movement.'),
    ('Healthy Cooking Class', 'Health & Wellness', 'Community Kitchen', 50, 38, 15, 0, 'Cook simple nutritious meals and learn practical weekly meal planning.'),
    ('Mental Health Awareness Forum', 'Health & Wellness', 'Civic Auditorium', 220, 57, 14, 0, 'Counselors and advocates discuss support systems, stress, and community care.'),
    ('Pilates for Beginners', 'Health & Wellness', 'Fit Studio One', 60, 73, 8, 0, 'A low-pressure class introducing alignment, strength, and mindful movement.'),
    ('Nutrition and Wellness Expo', 'Health & Wellness', 'Expo Pavilion', 300, 104, 10, 0, 'Wellness brands, nutrition experts, and demos gather for a practical expo.'),
    ('Neighborhood Cleanup Day', 'Community', 'Old Town Square', 250, 9, 8, 0, 'Volunteers team up to clean public spaces and plant fresh greenery.'),
    ('Youth Leadership Circle', 'Community', 'Community Center Room 2', 100, 31, 15, 0, 'Young leaders discuss service, confidence, and positive community action.'),
    ('Charity Auction Gala', 'Community', 'Grand Civic Hall', 260, 66, 18, 30, 'A formal fundraising evening with donated items, music, and dinner.'),
    ('Town Hall Listening Session', 'Community', 'Municipal Auditorium', 400, 81, 17, 0, 'Residents share ideas, questions, and priorities with local representatives.'),
    ('Volunteer Orientation Fair', 'Community', 'Public Library Plaza', 180, 101, 11, 0, 'Meet organizations looking for volunteers and find a cause that fits.'),
    ('Lake Day Adventure', 'Travel & Outdoor', 'Marina Dock', 120, 20, 8, 30, 'A guided lakeside day with boat views, picnic stops, and group activities.'),
    ('Nature Photography Walk', 'Travel & Outdoor', 'Forest Trail Entrance', 60, 29, 7, 0, 'Photographers explore natural light, framing, and scenic trail moments.'),
    ('Weekend Camping Basics', 'Travel & Outdoor', 'Outdoor Skills Camp', 75, 48, 14, 0, 'Learn tent setup, packing, safety, cooking, and campsite etiquette.'),
    ('City Heritage Walking Tour', 'Travel & Outdoor', 'Museum Front Steps', 90, 70, 10, 0, 'A guided walk through landmarks, stories, architecture, and local history.'),
    ('Waterfall Day Trip', 'Travel & Outdoor', 'Tour Bus Terminal', 55, 112, 6, 0, 'A scenic day trip with transport, nature stops, and time for photos.'),
    ('Urban Runway Night', 'Fashion', 'Design District Hall', 280, 23, 19, 0, 'Designers reveal bold streetwear, evening looks, and new local collections.'),
    ('Sustainable Fashion Market', 'Fashion', 'Creative Market Hall', 170, 43, 11, 0, 'Shop ethical clothing, upcycled pieces, accessories, and maker booths.'),
    ('Styling and Personal Brand Session', 'Fashion', 'Studio 14', 45, 55, 14, 30, 'A practical workshop on wardrobe choices, colors, and confident presentation.'),
    ('Bridal Expo Weekend', 'Fashion', 'Pearl Events Center', 320, 89, 10, 0, 'Vendors showcase gowns, suits, decor, photography, and celebration ideas.'),
    ('Designer Portfolio Review', 'Fashion', 'Fashion School Studio', 40, 118, 13, 0, 'Emerging designers receive feedback on sketches, lookbooks, and concepts.'),
    ('Kids Science Fair', 'Family', 'Children Discovery Hall', 260, 26, 10, 0, 'Hands-on experiments, demonstrations, and playful learning for young explorers.'),
    ('Family Movie Picnic', 'Family', 'Open Lawn Cinema', 500, 39, 17, 30, 'Bring blankets for an outdoor screening with snacks and family seating.'),
    ('Parenting Support Meetup', 'Family', 'Family Resource Center', 75, 52, 10, 30, 'Parents share advice and hear from facilitators on everyday family life.'),
    ('Board Game Family Day', 'Family', 'Community Hall', 160, 76, 12, 0, 'Classic and modern board games for all ages with guided tables.'),
    ('Holiday Craft Workshop', 'Family', 'Art Classroom B', 95, 122, 14, 0, 'Families create decorations, cards, and keepsakes with supplied materials.'),
    ('Documentary Screening Night', 'Film & Media', 'Independent Cinema', 190, 17, 19, 0, 'A thoughtful documentary screening followed by a moderated audience discussion.'),
    ('Podcast Production Studio', 'Film & Media', 'Media Lab', 35, 37, 13, 0, 'Plan, record, edit, and publish a short podcast episode in one session.'),
    ('Short Film Makers Mixer', 'Film & Media', 'Creative Loft', 115, 62, 18, 0, 'Film crews, editors, actors, and writers connect around new projects.'),
    ('Mobile Video Storytelling', 'Film & Media', 'Digital Media Classroom', 60, 84, 10, 0, 'Learn framing, audio, lighting, and editing for better phone-shot videos.'),
    ('Creators Content Day', 'Film & Media', 'Studio Warehouse', 150, 109, 11, 0, 'A collaborative day with sets, lighting corners, creator panels, and networking.'),
    ('Esports Open Tournament', 'Gaming', 'Arena Gaming Lounge', 220, 15, 15, 0, 'Players compete across brackets with live spectators and prize moments.'),
    ('Board Game Strategy Night', 'Gaming', 'Tabletop Cafe', 80, 32, 18, 30, 'A relaxed strategy night with hosted tables and beginner-friendly games.'),
    ('Game Design Jam', 'Gaming', 'Innovation Hub Lab', 70, 47, 9, 0, 'Teams prototype small games around a shared theme and demo their builds.'),
    ('Retro Arcade Evening', 'Gaming', 'Pixel Arcade', 140, 74, 18, 0, 'Classic cabinets, friendly score challenges, and nostalgic arcade energy.'),
    ('Family Gaming Expo', 'Gaming', 'Expo Hall 2', 300, 106, 10, 0, 'Interactive booths, casual tournaments, demos, and games for all ages.'),
]


class Command(BaseCommand):
    help = 'Load sample categories and events for demonstration'

    def handle(self, *args, **options):
        staff, created = User.objects.get_or_create(
            username='staff',
            defaults={
                'email': 'staff@eventbook.local',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            staff.set_password('StaffDemo123!')
            self.stdout.write(self.style.SUCCESS('Created staff user: staff / StaffDemo123!'))

        if not staff.is_staff or not staff.is_superuser:
            staff.is_staff = True
            staff.is_superuser = True
            staff.save(update_fields=['is_staff', 'is_superuser'])

        cat_map = {}
        for name, description in CATEGORIES:
            category, _ = Category.objects.get_or_create(name=name)
            if category.description != description:
                category.description = description
                category.save(update_fields=['description'])
            cat_map[name] = category

        created_count = 0
        updated_count = 0
        for title, cat_name, location, capacity, days_ahead, hour, minute, description in EVENTS:
            image_filename = f'{slugify(title)}.jpg'
            _, was_created = Event.objects.update_or_create(
                title=title,
                defaults={
                    'description': description,
                    'category': cat_map[cat_name],
                    'event_date': date.today() + timedelta(days=days_ahead),
                    'event_time': time(hour, minute),
                    'location': location,
                    'capacity': capacity,
                    'image': f'{Event.SEEDED_IMAGE_PREFIX}{image_filename}',
                    'created_by': staff,
                    'is_published': True,
                },
            )
            if was_created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Demo data loaded successfully: {len(CATEGORIES)} categories, '
                f'{created_count} events created, {updated_count} events updated.'
            )
        )

# config.py
# Centralized configuration file for the bot, containing role IDs, channel IDs, category IDs, and message filter words.

# Role IDs
# Unique identifiers for roles used to control access and permissions within the bot
STAFF_ROLE_ID = 1297999355860615209  # ID for the 'Staff' role, typically for support team members
ALLOWED_ROLE_IDS = [1297999091187581020, 1297999380745420822, STAFF_ROLE_ID]  # List of role IDs permitted to use restricted commands (e.g., Admin, Owner, Staff)
VERIFIED_CUSTOMER_ROLE_ID = [1297999210280517742, 1297999245592494241, STAFF_ROLE_ID]  # List of role IDs for verified customers and staff, granting access to customer-facing features (e.g., Verified, Customer, Staff)

# Category IDs
# IDs of channel categories where specific bot functionalities (e.g., ticket handling) are active
CATEGORY_IDS = [1298000300774260817, 1298000331036164218]  # List of category IDs for ticket-related channels monitored by the bot

# Channel IDs
# Specific channel IDs used for various bot features such as logging, announcements, and AI review
FILTERED_CHANNEL_ID = 1297999173592940564  # ID of the channel where message filtering is applied
LOG_CHANNEL_ID = 1298015864087511080  # ID of the channel where deleted messages and logs are sent
STATUS_CHANNEL_ID = 1298016167184695376  # ID of the channel displaying product status updates
ANNOUNCE_COMMAND_CHANNEL_ID = 1297999872829689999  # ID of the channel where the /announce command is used
ANNOUNCE_TARGET_CHANNEL_ID = 1297999047935791145  # ID of the channel where announcements are posted
UPDATE_COMMAND_CHANNEL_ID = 1297999872829689999  # ID of the channel where the /update command is used
UPDATE_TARGET_CHANNEL_ID = 1298001935948972043  # ID of the channel where updates are posted
AI_REVIEW_CHANNEL_ID = 1342292387392782346  # ID of the channel where AI suggestions are reviewed by staff

# Allowed Words for Message Filter
# List of words permitted in the filtered channel to prevent deletion by the message filter
ALLOWED_WORDS = [
    'insane', 'problems', 'problem', 'bad', 'issues', 'great', 'love', 'good', 'awesome',
    'fantastic', 'perfect', 'best', 'nice', '10/10', '/', '+', '-', 'support',
    'staff', 'team', 'amazing', 'incredible', 'outstanding', 'superb',
    'exceptional', 'wonderful', 'fabulous', 'phenomenal', 'spectacular', 'brilliant',
    'remarkable', 'stellar', 'terrific', 'marvelous', 'top-notch', 'impressive',
    'magnificent', 'high-quality', 'well-made', 'durable', 'reliable', 'affordable',
    'user-friendly', 'unique', 'creative', 'stylish', 'modern', 'beautiful', 'elegant',
    'comfortable', 'convenient', 'effective', 'efficient', 'love it', 'highly recommend',
    'worth every penny', 'exceeded expectations', 'better than expected', 'would buy again',
    'must-have', 'go-to choice', 'works perfectly', 'game-changer', 'life-saver',
    'excellent service', 'fast delivery', 'helpful staff', 'friendly', 'responsive',
    'polite', 'knowledgeable', 'fast', 'powerful', 'quiet', 'smooth', 'accurate', 'safe',
    'versatile', 'cost-effective', 'reasonable', 'good deal', 'great value',
    'worth it', 'kudos', '5-star', 'unbeatable', 'fantastic buy', 'thank you', '100%'
]  # Words and phrases allowed in the filtered channel, including positive feedback, support-related terms, and basic punctuation
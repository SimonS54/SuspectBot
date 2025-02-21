# config.py

# Role IDs
STAFF_ROLE_ID = 1297999355860615209 # Staff
ALLOWED_ROLE_IDS = [1297999091187581020, 1297999380745420822, STAFF_ROLE_ID] # Staff, Admin, Owner
VERIFIED_CUSTOMER_ROLE_ID = [1297999210280517742, 1297999245592494241, STAFF_ROLE_ID] # Verified, Customer

# Category IDs
CATEGORY_IDS = [
    1314011243173908503, 1310348839827406990, 1317240722377932952,
    1298000300774260817, 1298000331036164218, 1298000367384268880,
    1298000435579326556, 1298000476058685490, 1305201380180627466, 1333811568756129856
]

# Channel IDs
FILTERED_CHANNEL_ID = 1297999173592940564
LOG_CHANNEL_ID = 1298015864087511080
STATUS_CHANNEL_ID = 1298016167184695376
ANNOUNCE_COMMAND_CHANNEL_ID = 1297999872829689999
ANNOUNCE_TARGET_CHANNEL_ID = 1297999047935791145
UPDATE_COMMAND_CHANNEL_ID = 1297999872829689999
UPDATE_TARGET_CHANNEL_ID = 1298001935948972043
AI_REVIEW_CHANNEL_ID = 1342292387392782346

# Allowed Words for Message Filter
ALLOWED_WORDS = ['insane', 'problems', 'problem', 'bad', 'issues', 'great', 'love', 'good', 'awesome',
                 'fantastic', 'insane', 'perfect', 'best', 'nice', '10/10', '/', '+', '-', 'support',
                 'staff', 'team', 'amazing', 'fantastic', 'incredible', 'outstanding', 'superb',
                 'exceptional', 'wonderful', 'fabulous', 'phenomenal', 'spectacular', 'brilliant',
                 'remarkable', 'stellar', 'terrific', 'marvelous', 'top-notch', 'impressive',
                 'magnificent', 'high-quality', 'well-made', 'durable', 'reliable', 'affordable',
                 'user-friendly', 'unique', 'creative', 'stylish', 'modern', 'beautiful', 'elegant',
                 'comfortable', 'convenient', 'effective', 'efficient', 'love it', 'highly recommend',
                 'worth every penny', 'exceeded expectations', 'better than expected', 'would buy again',
                 'must-have', 'go-to choice', 'works perfectly', 'game-changer', 'life-saver',
                 'excellent service', 'fast delivery', 'helpful staff', 'friendly', 'responsive',
                 'polite', 'knowledgeable', 'fast', 'powerful', 'quiet', 'smooth', 'accurate', 'safe',
                 'versatile', 'affordable', 'cost-effective', 'reasonable', 'good deal', 'great value',
                 'worth it', 'kudos', '5-star', 'unbeatable', 'fantastic buy', 'thank you', '100%']
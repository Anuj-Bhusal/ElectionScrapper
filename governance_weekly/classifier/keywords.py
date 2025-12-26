# Corruption - Highest Priority
corruption_keywords = [
    "corruption", "bribery", "fraud", "embezzlement", "kickback",
    "CIAA", "commission for the investigation", "anti-corruption",
    "misuse of public fund", "irregularity", "scam", "graft",
    "abuse of authority", "money laundering", "corruption case",
    "arrested for corruption", "भ्रष्टाचार", "घुस", "अख्तियार",
    "financial irregularity", "audit report", "misappropriation",
    "corrupt practices", "kickbacks", "illegal payment",
    "corruption charge", "corruption allegations", "bribe case",
    "embezzlement case", "financial fraud", "procurement fraud",
    "tender manipulation", "fake bill", "commission on contract",
    "दुरुपयोग", "आर्थिक अनियमितता", "सम्पत्ति विवरण"
]

# Irregularity (closely related to corruption)
irregularity_keywords = [
    "irregularity", "irregularities", "financial irregularity",
    "procedural irregularity", "administrative irregularity",
    "audit irregularity", "अनियमितता", "procurement irregularity",
    "contract irregularity", "tender irregularity", "budget irregularity",
    "audit objection", "audit report irregularity", "financial mismanagement",
    "rule violation", "procedural violation", "contract breach",
    "ठेक्का अनियमितता", "खरिद अनियमितता", "लेखापरीक्षण"
]

# Gender Equality and Social Inclusion
gender_equality_keywords = [
    "gender equality", "women's rights", "gender discrimination",
    "women empowerment", "GESI", "social inclusion", "marginalized",
    "dalits", "inclusion", "discrimination", "equality",
    "महिला अधिकार", "समावेशीकरण", "gender-based violence",
    "women in politics", "quota system", "representation"
]

# Economy
economy_keywords = [
    "economy", "economic", "GDP", "inflation", "budget",
    "fiscal policy", "monetary policy", "trade", "investment",
    "employment", "unemployment", "poverty", "economic growth",
    "अर्थतन्त्र", "आर्थिक", "business", "industry", "commerce",
    "banking", "finance", "stock market", "revenue"
]

# Political
political_keywords = [
    "political", "politics", "coalition", "opposition", "ruling party",
    "government formation", "political crisis", "political agreement",
    "agreement", "deal", "consensus", "negotiation", "dialogue",
    "protest", "demonstration", "strike", "demand", "youth", "student union",
    "gen z", "youth leader", "student leader", "activist",
    "राजनीतिक", "राजनीति", "party", "leader", "political instability",
    "political reform", "constitution", "संविधान", "सम्झौता", "सहमति",
    "वार्ता", "आन्दोलन", "प्रदर्शन", "माग", "युवा", "विद्यार्थी"
]

# Service Delivery
service_delivery_keywords = [
    "service delivery", "public service", "government service",
    "सेवा प्रवाह", "service center", "one-door service",
    "citizen service", "municipal service", "service quality",
    "service improvement", "online service", "e-service"
]

# Human Rights
human_rights_keywords = [
    "human rights", "rights violation", "civil rights",
    "freedom of expression", "मानव अधिकार", "torture",
    "arbitrary detention", "due process", "fair trial",
    "National Human Rights Commission", "NHRC", "rights abuse"
]

# Election
election_keywords = [
    "election", "Election Commission", "voters", "ballot", "vote", "EVM",
    "polling", "candidate disqualified", "election code", "by-election",
    "voter registration", "electoral", "निर्वाचन", "मतदान",
    "political party registration", "election monitoring", "voting"
]

# Environment/Climate Change
environment_keywords = [
    "environment", "climate change", "pollution", "deforestation",
    "वातावरण", "जलवायु परिवर्तन", "carbon emission", "air quality",
    "waste management", "conservation", "biodiversity",
    "environmental protection", "sustainable development",
    "climate crisis", "global warming", "green energy"
]

# Education
education_keywords = [
    "education", "school", "university", "teacher", "student",
    "शिक्षा", "विद्यालय", "scholarship", "education policy",
    "education budget", "literacy", "education reform",
    "curriculum", "examination", "educational institution"
]

# Health
health_keywords = [
    "hospital", "health", "healthcare", "vaccine", "disease", "epidemic",
    "ministry of health", "health workers", "medicine shortage",
    "public health", "sanitation", "medical", "स्वास्थ्य",
    "health budget", "health policy", "health service",
    "ambulance", "health insurance", "pandemic", "COVID"
]

# Migration
migration_keywords = [
    "migration", "migrant", "labor migration", "foreign employment",
    "वैदेशिक रोजगार", "आप्रवासन", "remittance", "migrant workers",
    "labor rights", "trafficking", "manpower", "recruitment",
    "overseas employment", "migrant rights"
]

# Natural Disaster
natural_disaster_keywords = [
    "earthquake", "flood", "landslide", "disaster", "भूकम्प",
    "बाढी", "पहिरो", "प्रकोप", "natural calamity", "rescue",
    "relief", "emergency", "disaster management", "reconstruction",
    "rehabilitation", "disaster preparedness", "early warning"
]

# General Governance (catch-all for governance-related that don't fit above)
governance_keywords = [
    "policy", "reform", "digital governance", "transparency",
    "accountability", "local government", "municipality",
    "citizen charter", "federalism", "parliament", "bill", "act",
    "e-governance", "public administration", "civil service",
    "bureaucracy", "government office", "ministry", "department",
    "budget allocation", "infrastructure", "development project",
    "community initiative", "ward office", "mayor",
    "Right to Information", "RTI", "nagarpalika", "प्रदेश", "स्थानीय तह"
]

exclude_keywords = [
    # Sports & Entertainment
    "cricket", "football", "sports", "entertainment", "movie", 
    "celebrity", "horoscope", "arts", "lifestyle",
    "fashion", "music", "drama", "film", "actor", "actress",
    "singer", "tournament", "match", "player", "coach",
    "box office", "album", "concert", "festival",
    "फुटबल", "क्रिकेट",
    
    # Opinion & Commentary Content - STRENGTHENED
    "opinion", "op-ed", "editorial", "commentary", "column", "columnist",
    "विचार", "समीक्षा", "टिप्पणी", "विश्लेषण",
    "my view", "my opinion", "in my opinion", "i think", "i believe",
    "personal view", "viewpoint", "perspective", "personal opinion",
    "interview with", "exclusive interview", "in conversation with", "q&a", "qa",
    "अन्तर्वार्ता", "कुराकानी", "अन्तर्वार्ता",
    "expert opinion", "expert view", "analyst says", "analyst view",
    "political commentary", "political opinion", "political analysis",
    "writer's opinion", "author's view", "guest column", "guest post",
    "opinion piece", "opinion article", "my perspective", "personal take",
    "writes", "argues that", "opines", "suggests that",
    "लेखक", "विचार", "टिप्पणीकार",
    
    # Blog & Personal Content
    "blog", "blogger", "vlog", "vlogger", "personal story",
    "my experience", "my journey", "diary", "memoir",
    
    # Analysis & Think Pieces (subjective)
    "think piece", "deep dive", "explainer from perspective",
    "what i learned", "lessons from", "reflections on",
    
    # Non-news Content
    "photo gallery", "photo feature", "in pictures", "gallery",
    "तस्बिर", "तस्वीर", "फोटो फिचर",
    "recipe", "cooking", "beauty", "makeup", "dating",
    "bollywood", "hollywood", "netflix", "series", "show",
    "album", "concert", "festival", "video", "viral"
]

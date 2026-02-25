# =============================================================================
# NEPAL ELECTION MARCH 5, 2026 - WEIGHTED SCORING KEYWORDS
# Pre-election phase: Focus on political maneuvering + direct election terms
# =============================================================================

# =============================================================================
# TIER 1: DIRECT ELECTION TERMS (5 POINTS EACH)
# These are explicit election/voting references
# =============================================================================
tier1_election_keywords = [
    # Election Commission & Dates
    "election commission", "EC Nepal", "निर्वाचन आयोग",
    "march 5", "march 2026", "2026 election", "फागुन २१", "फागुन 21",
    "election date", "election schedule", "निर्वाचन मिति",
    
    # Voting & Polling
    "polling station", "polling booth", "polling center", "मतदान केन्द्र",
    "ballot paper", "ballot box", "मतपत्र", "मतपेटिका",
    "EVM", "electronic voting machine",
    "vote counting", "ballot counting", "मतगणना",
    "voter registration", "voter list", "voter ID", "voter card",
    "मतदाता नामावली", "मतदाता परिचयपत्र", "मतदाता सूची",
    
    # Voter Roll Operations
    "voter roll update", "voter roll revision", "voter roll publication",
    "voter roll verification", "BVR", "biometric voter registration",
    "mobile registration team", "मतदाता नामावली अद्यावधिक",
    "मतदाता नामावली प्रकाशन", "मतदाता नामावली संशोधन",
    
    # Electoral Process
    "by-election", "उपनिर्वाचन", "local election", "स्थानीय निर्वाचन",
    "provincial election", "प्रदेश निर्वाचन", "federal election",
    "general election", "आम निर्वाचन",
    "election result", "election results", "निर्वाचन परिणाम",
    
    # Candidate Nomination Lifecycle
    "candidate nomination", "nomination filing", "nomination verification",
    "nomination withdrawal", "nomination rejection", "final candidate list",
    "candidacy filing", "उम्मेदवारी दर्ता", "उम्मेदवारी मनोनयन",
    "उम्मेदवारी फिर्ता", "अन्तिम उम्मेदवार सूची",
    "मनोनयन दर्ता", "मनोनयन जाँच", "मनोनयन खारेज",
    
    # Polling Staff & Election Officers
    "polling officer", "election officer", "returning officer",
    "chief returning officer", "polling staff", "election staff",
    "मतदान अधिकृत", "निर्वाचन अधिकृत", "प्रमुख निर्वाचन अधिकृत",
    
    # Ballot & Polling Logistics
    "ballot distribution", "ballot printing", "polling logistics",
    "election material", "election logistics", "मतपत्र वितरण",
    "मतपत्र छपाइ", "निर्वाचन सामग्री",
    
    # Code of Conduct
    "code of conduct", "election code", "आचारसंहिता", "निर्वाचन आचारसंहिता",
    
    # Election Law & Regulation
    "election law", "election act", "election regulation", "election directive",
    "election dispute", "election petition", "election tribunal",
    "निर्वाचन ऐन", "निर्वाचन नियमावली", "निर्वाचन निर्देशिका",
    "निर्वाचन विवाद", "निर्वाचन उजुरी",
    
    # Election Fraud/Corruption
    "election fraud", "vote rigging", "vote buying", "मत खरिद",
    "election irregularity", "ballot fraud", "booth capturing",
    "election corruption", "निर्वाचन अनियमितता",
]

# =============================================================================
# TIER 2: HIGH-INTENT POLITICAL CONTEXT (3 POINTS EACH)
# Pre-election maneuvering: alliances, nominations, party politics
# =============================================================================
tier2_political_keywords = [
    # Major Political Parties - English
    "CPN-UML", "UML", "CPN UML",
    "nepali congress", "congress party", "NC",
    "maoist centre", "maoist center", "CPN-Maoist", "CPN Maoist",
    "rastriya swatantra party", "RSP",
    "rastriya prajatantra party", "RPP",
    "janata samajwadi party", "JSP",
    "unified socialist", "CPN unified socialist",
    "loktantrik samajwadi", "LSP",
    "janamat party",
    "nagarik unmukti party", "NUP",
    
    # Major Political Parties - Nepali
    "एमाले", "नेकपा एमाले", "ने क पा एमाले",
    "कांग्रेस", "नेपाली कांग्रेस",
    "माओवादी", "माओवादी केन्द्र", "नेकपा माओवादी",
    "रास्वपा", "राष्ट्रिय स्वतन्त्र पार्टी",
    "राप्रपा", "राष्ट्रिय प्रजातन्त्र पार्टी",
    "जसपा", "जनता समाजवादी पार्टी",
    "एकीकृत समाजवादी", "नेकपा एकीकृत समाजवादी",
    "जनमत पार्टी",
    
    # Alliance & Coalition
    "alliance", "गठबन्धन", "coalition", "गठबन्धन सरकार",
    "seat sharing", "seat-sharing", "सिट बाँडफाँड", "भागबण्डा",
    "electoral alliance", "चुनावी गठबन्धन", "तालमेल",
    "power sharing", "सत्ता साझेदारी",
    
    # Candidates & Nominations
    "candidate", "candidates", "उम्मेदवार", "उम्मेदवारी",
    "nomination", "मनोनयन", "candidacy", "उम्मेद्वारी दर्ता",
    "filed nomination", "candidate list", "उम्मेदवार सूची",
    "proportional representation", "PR list", "समानुपातिक",
    
    # Manifesto & Campaign
    "manifesto", "election manifesto", "घोषणापत्र", "चुनावी घोषणापत्र",
    "election campaign", "campaign rally", "चुनावी अभियान",
    "election promise", "campaign promise", "चुनावी वाचा",
    
    # Campaign Finance & Spending
    "campaign finance", "election spending", "election expenditure",
    "donation disclosure", "campaign donation", "campaign fundraising",
    "spending limit", "election fund", "चुनावी खर्च",
    "चुनावी कोष", "दान खुलासा", "खर्च सीमा",
    
    # Media Monitoring & Political Advertising
    "media monitoring", "equal airtime", "political advertisement",
    "political advertising", "media fairness", "press freedom election",
    "digital campaign", "online campaign", "मिडिया अनुगमन",
    "राजनीतिक विज्ञापन", "समान प्रसारण समय",
    
    # Social Media & Misinformation
    "social media election", "social media campaign",
    "election misinformation", "election disinformation",
    "fake news election", "online propaganda",
    "सामाजिक सञ्जाल अभियान", "भ्रामक सूचना", "गलत सूचना",
    
    # Election Observers & Monitoring
    "election observer", "election monitoring", "election monitor",
    "domestic observer", "international observer",
    "observer accreditation", "monitoring mission",
    "निर्वाचन पर्यवेक्षक", "निर्वाचन अनुगमन",
    "पर्यवेक्षक प्रत्यायन", "अनुगमन मिसन",
    
    # Voter Education & Civic Awareness
    "voter education", "civic education", "voter awareness",
    "mock voting", "information campaign", "voter outreach",
    "मतदाता शिक्षा", "नागरिक शिक्षा", "मतदाता जागरण",
    "मतदाता चेतना", "नमूना मतदान",
    
    # Election Official Training & Logistics
    "election official training", "polling staff training",
    "logistics distribution", "sensitive polling station",
    "election security", "security deployment",
    "निर्वाचन तालिम", "मतदान कर्मचारी तालिम",
    "संवेदनशील मतदान केन्द्र", "सुरक्षा तैनाथी",
    
    # Key Political Leaders (election context)
    "sher bahadur deuba", "देउवा",
    "KP oli", "केपी ओली", "ओली",
    "pushpa kamal dahal", "prachanda", "प्रचण्ड", "दाहाल",
    "rabi lamichhane", "रवि लामिछाने", "लामिछाने",
    "baburam bhattarai", "बाबुराम भट्टराई",
    
    # National Assembly (Rastriya Sabha)
    "national assembly", "rastriya sabha", "राष्ट्रिय सभा",
    "upper house", "माथिल्लो सदन",
    
    # Constituency
    "constituency", "निर्वाचन क्षेत्र", "प्रदेश",
    
    # Party Internal Elections/Decisions
    "central committee", "केन्द्रीय समिति",
    "standing committee", "स्थायी समिति",
    "party president", "पार्टी अध्यक्ष",
    "general secretary", "महामन्त्री",
    "working committee", "कार्यसम्पादन समिति",
]

# =============================================================================
# TIER 3: GENERAL ELECTION CONTEXT (1 POINT EACH)
# Broader political terms that add context
# =============================================================================
tier3_context_keywords = [
    # General Political Terms
    "political party", "राजनीतिक दल",
    "opposition", "प्रतिपक्ष", "ruling party", "सत्तारुढ दल",
    "parliament", "संसद", "house of representatives", "प्रतिनिधि सभा",
    
    # Government Formation
    "government formation", "सरकार गठन",
    "prime minister", "प्रधानमन्त्री", "PM",
    "chief minister", "मुख्यमन्त्री", "CM",
    
    # Political Events
    "press conference", "पत्रकार सम्मेलन",
    "party meeting", "दलको बैठक",
    "negotiation", "वार्ता", "dialogue", "संवाद",
    
    # Election Environment & Preparedness
    "electoral process", "निर्वाचन प्रक्रिया",
    "free and fair election", "स्वतन्त्र र निष्पक्ष निर्वाचन",
    "election preparedness", "निर्वाचन तयारी",
    "election environment", "निर्वाचन वातावरण",
]

# Combined for backward compatibility
election_keywords = tier1_election_keywords + tier2_political_keywords + tier3_context_keywords
core_election_keywords = tier1_election_keywords  # For backward compat
election_context_keywords = tier2_political_keywords
election_corruption_keywords = [k for k in tier1_election_keywords if "fraud" in k or "rigging" in k or "corruption" in k or "irregularity" in k]

# Governance - minimal, only election-related
governance_keywords = [
    "election commission", "निर्वाचन आयोग",
    "electoral reform", "निर्वाचन सुधार",
    "constitutional provision", "संवैधानिक व्यवस्था",
]

# Legacy - empty for backward compatibility
corruption_keywords = []
irregularity_keywords = []
gender_equality_keywords = []
economy_keywords = []
political_keywords = []
service_delivery_keywords = []
human_rights_keywords = []
environment_keywords = []
education_keywords = []
health_keywords = []
migration_keywords = []
natural_disaster_keywords = []

# =============================================================================
# STRICT EXCLUSION KEYWORDS - Remove irrelevant content
# Single merged list (no duplicates)
# =============================================================================
exclude_keywords = [
    # Stock Market & Finance (NOT election related)
    "NEPSE", "stock market", "share market", "stock index",
    "trading", "investor", "investment return", "IPO",
    "broker", "securities", "शेयर बजार", "सेयर",
    "mutual fund", "dividend", "bonus share",
    
    # Sports & Entertainment
    "cricket", "football", "sports", "entertainment", "movie",
    "celebrity", "horoscope", "arts", "lifestyle",
    "fashion", "music", "drama", "film", "actor", "actress",
    "singer", "tournament", "match", "player", "coach",
    "box office", "album", "concert", "world cup",
    "फुटबल", "क्रिकेट", "खेल",
    
    # Beauty Pageants
    "beauty pageant", "miss nepal", "mrs nepal", "mrs world",
    "miss world", "beauty queen", "pageant", "crown",
    
    # Tourism & Travel (NOT election)
    "tourist", "tourism", "pilgrimage", "pilgrim", "visitors",
    "travel", "hotel", "resort", "trekking", "mountaineering",
    "everest", "lumbini", "pokhara", "chitwan",
    
    # Foreign Affairs (NOT Nepal election)
    "trump", "biden", "china", "india", "USA", "america",
    "russia", "ukraine", "venezuela", "foreign policy",
    "international relations", "bilateral", "embassy",
    "UN", "united nations", "world bank", "IMF",
    
    # Poetry, Literature, Art
    "poem", "poetry", "poet", "novel", "book launch",
    "literature", "author", "writer", "कविता", "साहित्य",
    "art exhibition", "gallery", "painting",
    
    # Health & Disease
    "hospital", "disease", "pandemic", "COVID", "health ministry",
    "patient", "doctor", "medicine", "vaccine", "epidemic",
    "health", "स्वास्थ्य", "अस्पताल", "रोग",
    
    # Natural Disaster (unless election related)
    "earthquake", "flood", "landslide", "disaster relief",
    "rescue operation", "disaster",
    "भूकम्प", "बाढी", "पहिरो",
    
    # Education (NOT election)
    "school", "university", "college", "exam", "SEE result",
    "scholarship", "student", "teacher", "curriculum",
    "education", "शिक्षा", "विद्यालय", "परीक्षा",
    
    # Crime (NOT election related)
    "murder", "robbery", "theft", "arrested for", "drug",
    "smuggling", "rape", "kidnapping", "हत्या", "चोरी",
    
    # Migration & Remittance
    "remittance", "foreign employment", "migrant worker",
    "migration", "gulf", "malaysia", "korea", "वैदेशिक रोजगार",
    
    # Economy (general, NOT election)
    "GDP", "inflation", "economic growth", "trade deficit",
    "export", "import", "customs", "revenue", "economy",
    
    # Technology (NOT election)
    "hacking", "cyber attack", "website hacking", "data theft",
    "software", "app launch", "startup",
    
    # Opinion & Commentary
    "opinion", "op-ed", "editorial", "commentary", "column",
    "विचार", "समीक्षा", "टिप्पणी",
    "interview with", "exclusive interview", "in conversation",
    
    # Obituary & Personal
    "death", "funeral", "obituary", "passed away", "demise",
    "birthday", "anniversary", "wedding", "marriage",
    
    # Weather
    "weather", "rain", "cold wave", "temperature", "fog",
    "मौसम", "वर्षा", "हिमपात",
    
    # Other Non-Election Topics
    "corruption case", "bribery", "embezzlement", "scam",
    "environment", "climate change", "pollution",
    "gender", "women empowerment", "discrimination",
]

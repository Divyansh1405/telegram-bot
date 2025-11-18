import json
import os
import sqlite3
from typing import Optional, List, Tuple

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ============================
# INTERNAL CONFIG (11 LANGUAGES)

CONFIG = {
  "branding": {
    "bot_name": "UltraWisdom Bot",
    "description_en": "🌟 Welcome to The Ultra Wisdom — The New Era of Digital Leadership! 🇮🇳",
    "bio_en": "Dear Leader,\nCongratulations and welcome to the Ultra Wisdom Success Movement! 🎉\nYou are now part of a trusted global brand with a powerful Digital India Vision — empowering every Indian to grow, earn, and shine through beauty, wellness, and entrepreneurship.\n\n✨ What Makes This Journey Special:\n💎 Trusted Swedish Brand since 2000\n🌿 1000+ Quality Products for Daily Use & Wellness\n📱 100% Digital Platform — Work from Anywhere\n🚀 Earn, Learn & Lead with Your Own Team\n🤝 Together, We Build a Strong & Smart India\n\n— ⚡ Team Ultra Wisdom | Digital India Mission 2025-2026 🇮🇳"
  },

  "footer": {
    "en": "(You can change language anytime using /language)",
    "hi": "(आप किसी भी समय /language का उपयोग करके भाषा बदल सकते हैं)",
    "bn": "(আপনি যে কোনো সময় /language ব্যবহার করে ভাষা পরিবর্তন করতে পারবেন)",
    "te": "(మీరు ఎప్పుడైనా /language ద్వారా భాషను మార్చుకోవచ్చు)",
    "mr": "(आपण कधीही /language वापरून भाषा बदलू शकता)",
    "ta": "(நீங்கள் எப்போதும் /language மூலம் மொழியை மாற்றலாம்)",
    "gu": "(તમે ક્યારે પણ /language દ્વારા ભાષા બદલી શકો છો)",
    "kn": "(ನೀವು ಯಾವಾಗಲಾದರೂ /language ಬಳಸಿ ಭಾಷೆಯನ್ನು ಬದಲಾಯಿಸಬಹುದು)",
    "ml": "(നിങ്ങൾക്ക് ഏതെങ്കിലും സമയത്ത് /language ഉപയോഗിച്ച് ഭാഷ മാറ്റാൻ കഴിയും)",
    "pa": "(ਤੁਸੀਂ ਕਿਸੇ ਵੀ ਸਮੇਂ /language ਵਰਤ ਕੇ ਭਾਸ਼ਾ ਬਦਲ ਸਕਦੇ ਹੋ)",
    "or": "(ଆପଣ କେବେ ବି /language ବ୍ୟବହାର କରି ଭାଷା ପରିବର୍ତ୍ତନ କରିପାରିବେ)"
  },

  "languages": {

    "en": {
      "label": "English — 🇬🇧",
      "welcome_header": "🌟 Welcome to The Ultra Wisdom — The New Era of Digital Leadership! 🇮🇳",
      "bio": "Dear Leader,\nCongratulations and welcome to the Ultra Wisdom Success Movement! 🎉\nYou are now part of a trusted global brand with a powerful Digital India Vision — empowering every Indian to grow, earn, and shine through beauty, wellness, and entrepreneurship.\n\n✨ What Makes This Journey Special:\n💎 Trusted Swedish Brand since 2000\n🌿 1000+ Quality Products for Daily Use & Wellness\n📱 100% Digital Platform — Work from Anywhere\n🚀 Earn, Learn & Lead with Your Own Team\n🤝 Together, We Build a Strong & Smart India\n\n— ⚡ Team Ultra Wisdom | Digital India Mission 2025-2026 🇮🇳",

      "signup": "🎉 Welcome to THE ULTRA WISDOM™!\n\nYou can sign up on our platform using the link below and begin your journey with THE ULTRA WISDOM™.\n\n🪜 How to Sign Up:\n• Click the “Join Now” button\n• Fill in the registration page details\n• Submit the form and start your journey with THE ULTRA WISDOM™\n\nhttps://theultrawisdom.com/referral?get_sponsor=TUW258258\n\n💡 Note: Sign up is completely FREE — no payment required.",

      "login": "🔑 Welcome to THE ULTRA WISDOM™!\n\nYou can log in to our platform using the link below.\n\n• Enter your User ID and Password\n• After logging in you can manage your activities and access all features\n\nhttps://theultrawisdom.com/ultra/Dashboard\n\nIf you need any help, feel free to ask.",

      "telegram": "📢 THE ULTRA WISDOM™ — Telegram Channel\n\nJoin our official Telegram channel for the latest updates, announcements, and offers. Be part of the Ultra Wisdom community and never miss important news.\n\nJoin now for instant updates and support!",

      "contact": "📞 Contact THE ULTRA WISDOM™\n\nYou can reach us anytime at:\n📱 +91-6350638920\n\nOffice Address:\nSudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",

      "benefits": "⭐ THE ULTRA WISDOM™ — Company Benefits (How the company earns and sustains payouts)\n\nQ: How does the company earn? Where does revenue come from? How can the company afford to pay incentives?\n\nA: Currently the company operates primarily through two main streams and a third project (E-Commerce) will launch soon:\n\n1️⃣ Ad-View Tasks — partner clients provide ad-view tasks and the platform receives commissions per completed task.\n2️⃣ Referral-based Income — user referrals drive growth and generate referral bonuses and long-term customer acquisition value.\n3️⃣ (Upcoming) E-Commerce Project — will enable product sales and additional revenue channels.\n\nImportant notes:\n• Ad-view tasks are provided by client partners; THE ULTRA WISDOM receives commission for each completed task.\n• Withdrawals via UPI and net banking will be available from 05 December 2025.\n• The more activity/users, the healthier the company revenue — enabling sustainable payouts and platform growth.\n\nIf you want further details about revenue split or audits, please contact official support.",

      "working": "🛠 HOW TO WORK — Step-by-step\n\n1. Free Registration\nJoin: https://theultrawisdom.com/referral?get_sponsor=TUW258258\n\n2. ₹500 Signup Bonus — instantly credited on valid registration\n\n3. Daily Tasks (Play & Earn)\n• Watch 4 sponsor ads daily to earn up to ₹340/day (follow task rules for credit)\n\n4. Invite & Earn\n• Earn ₹540 per successful referral (terms apply)\n\n5. Telegram Channel Join\n• Join official Telegram channel — get ₹400 instant credit (as per campaign rules)\n\n6. Team Income (level-based)\nLevel | Income\n1st | ₹85\n2nd | ₹55\n3rd | ₹35\n4th | ₹25\n5th | ₹10\n\n7. Rank Income (example tiers)\nSR | Referrals | Income\n1st | 150 | ₹21,000\n2nd | 120 | ₹19,000\n3rd | 102 | ₹17,000\n4th | 95 | ₹15,000\n5th | 85 | ₹13,000\n6th | 65 | ₹11,000\n7th | 45 | ₹9,000\n8th | 25 | ₹7,000\n9th | 15 | ₹4,000\n10th | 5 | ₹2,000\n\nNotes:\n• Follow the in-app instructions for each task to ensure credits apply.\n• Campaigns, bonuses and terms may change — official channel announces updates.",

      "address": "📍 Office Address:\nSudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",

      "withdrawal": "🔔 WITHDRAWAL DETAILS\n\n• Minimum: ₹500\n• Maximum: ₹1,00,000\n• Start Date: 05 December 2025, 1:00 PM\n• Modes: Bank Account & UPI\n• No TDS / No Admin Charge!\n\nNOTE: JOINING and WITHDRAWAL are completely FREE.",

      "realfake": "🙏 We understand your concern.\n\nTHE ULTRA WISDOM™ is a legitimate and authentic company. We provide a transparent platform where users can earn by completing simple online tasks. Our processes are transparent and user security & satisfaction are top priorities.\n\nIf you have doubts, join our official Telegram channel for live updates and verifications.",

      "qa_prompt": "Please type your question. Type /cancel to exit Q/A."
    },


    "hi": {
      "label": "हिन्दी — 🇮🇳",
      "welcome_header": "🌟 अल्ट्रा विज़डम में आपका स्वागत — डिजिटल नेतृत्व का नया युग! 🇮🇳",
      "bio": "प्रिय लीडर,\nबधाई हो और Ultra Wisdom Success Movement में आपका स्वागत है! 🎉\nआप अब एक भरोसेमंद वैश्विक ब्रांड का हिस्सा हैं जिसका उद्देश्य डिजिटल इंडिया विज़न के माध्यम से हर भारतीय को बढ़ने, कमाने और सुंदरता, वेलनेस तथा उद्यमिता के जरिए चमकने में सक्षम बनाना है।\n\n✨ इस यात्रा को खास क्या बनाता है:\n💎 Trusted Swedish Brand since 2000\n🌿 दैनिक उपयोग और वेलनेस के लिए 1000+ गुणवत्ता उत्पाद\n📱 100% डिजिटल प्लेटफ़ॉर्म — कहीं से भी काम करें\n🚀 कमाएँ, सीखें और अपनी टीम के साथ नेतृत्व करें\n🤝 साथ मिलकर हम एक मजबूत और स्मार्ट इंडिया बनाएँगे\n\n— ⚡ Team Ultra Wisdom | Digital India Mission 2025-2026 🇮🇳",

      "signup": "🎉 स्वागत है THE ULTRA WISDOM™!\n\nआप नीचे दिए गए लिंक से हमारे प्लेटफ़ॉर्म पर साइन अप कर सकते हैं और THE ULTRA WISDOM™ के साथ अपनी यात्रा शुरू कर सकते हैं।\n\n🪜 साइन अप कैसे करें:\n• ऊपर दिए गए “Join Now” बटन पर क्लिक करें\n• रजिस्ट्रेशन पेज पर अपनी जानकारी भरें\n• फॉर्म सबमिट करें और अपनी यात्रा शुरू करें\n\nhttps://theultrawisdom.com/referral?get_sponsor=TUW258258\n\n💡 नोट: साइन अप पूरी तरह फ्री है — कोई भुगतान आवश्यक नहीं है।",

      "login": "🔑 THE ULTRA WISDOM™ पर स्वागत है!\n\nआप नीचे दिए गए बटन से हमारे प्लेटफ़ॉर्म पर लॉगिन कर सकते हैं।\n\n🔑 लॉगिन कैसे करें:\n• अपना User ID और Password दर्ज करें\n• लॉगिन करने के बाद आप अपनी गतिविधियाँ प्रबंधित कर सकते हैं और THE ULTRA WISDOM™ की सभी सुविधाएँ देख सकते हैं।\n\nhttps://theultrawisdom.com/ultra/Dashboard\n\nयदि आपको कोई सहायता चाहिए या कोई प्रश्न है, तो बेझिझक पूछें।",

      "telegram": "📢 THE ULTRA WISDOM™ — टेलीग्राम चैनल\n\nताज़ा अपडेट और जानकारी पाने के लिए हमारे आधिकारिक टेलीग्राम चैनल से जुड़ें।\n\nक्यों जुड़ें?\n• नई सुविधाएँ और घोषणाएँ\n• आने वाले ऑफर्स और लाभ\n• THE ULTRA WISDOM™ समुदाय का हिस्सा बनें\n\nअभी जुड़ें! 🚀",

      "contact": "📞 THE ULTRA WISDOM™ से संपर्क\n\nआप किसी भी समय हमसे इस नंबर पर संपर्क कर सकते हैं:\n📱 +91-6350638920\n\nकार्यालय का पता:\nSudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",

      "benefits": "⭐ THE ULTRA WISDOM™ — कंपनी लाभ (कंपनी आय और उसका मॉडल)\n\nप्रश्न: कंपनी लाभ कैसे कमाती है? कंपनी की आय कहाँ से आती है? कंपनी इतना भुगतान कैसे कर पाती है?\n\nउत्तर: कंपनी फिलहाल तीन स्तम्भों पर काम करती है — और तीसरा (E-Commerce) प्रोजेक्ट जल्द ही लाइव होगा:\n\n1️⃣ ऐड-व्यू टास्क — क्लाइंट पार्टनर कंपनियां ऐड-व्यू टास्क प्रोवाइड करती हैं; हर पूरा टास्क कंपनी को कमीशन दिलाता है।\n2️⃣ रेफरल-आधारित आय — सफल रेफरल प्लेटफॉर्म वृद्धि और दीर्घकालिक वैल्यू पैदा करते हैं।\n3️⃣ (आगामी) E-Commerce प्रोजेक्ट — प्रोडक्ट बिक्री से अतिरिक्त राजस्व चैनल।\n\nमहत्वपूर्ण नोट्स:\n• 05 दिसम्बर 2025 से UPI और नेट-बैंकिंग के जरिए विड्रॉल उपलब्ध होगा।\n• कंपनी का राजस्व जितना अधिक होगा, उतना ही बेहतर भुगतान मॉडल सुरक्षित रहेगा।\n\nऔर जानना है तो आधिकारिक सपोर्ट से संपर्क करें।",

      "working": "🛠 कैसे काम करें — स्टेप बाई स्टेप\n\n1. Free Registration\nJoin: https://theultrawisdom.com/referral?get_sponsor=TUW258258\n\n2. ₹500 Signup Bonus — वैध रजिस्ट्रेशन पर तुरंत क्रेडिट\n\n3. Daily Tasks (Play & Earn)\n• रोज़ 4 sponsor ads देखें और नियमों के अनुसार क्रेडिट प्राप्त करें — कुल ₹340/दिन तक\n\n4. Invite & Earn\n• प्रत्येक सफल रेफरल पर ₹540 (terms लागू)\n\n5. Telegram Channel Join\n• ऑफिशल चैनल जॉइन करें — कुछ कैंपेन में ₹400 इनस्टेंट क्रेडिट मिलता है\n\n6. Team Income (लेवल-आधारित)\nLevel | Income\n1st | ₹85\n2nd | ₹55\n3rd | ₹35\n4th | ₹25\n5th | ₹10\n\n7. Rank Income (उदाहरण)\n1st (150) | ₹21,000\n2nd (120) | ₹19,000\n3rd (102) | ₹17,000\n\nनोट्स:\n• प्रत्येक टास्क के निर्देश फॉलो करें ताकि क्रेडिट सही ढंग से मिले।\n• ऑफ़र्स और टर्म्स समय-समय पर अपडेट हो सकते हैं — आधिकारिक चैनल देखें।",

      "address": "📍 कार्यालय का पता:\nSudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",

      "withdrawal": "🔔 WITHDRAWAL DETAILS\n\n• Minimum: ₹500\n• Maximum: ₹1,00,000\n• Start Date: 05 December 2025, 1:00 PM\n• Modes: Bank Account & UPI\n• No TDS / कोई Admin Charge नहीं!\n\nNOTE: JOINING और WITHDRAWAL पूरी तरह FREE हैं।",

      "realfake": "🙏 हम आपकी चिंता समझते हैं।\n\nTHE ULTRA WISDOM™ पूर्णतः वैध और प्रमाणिक कंपनी है। हम उपयोगकर्ताओं के लिए पारदर्शी प्लेटफार्म देते हैं जहाँ सरल ऑनलाइन टास्क करके कमाया जा सकता है।\n\nयदि संदेह हो तो हमारे आधिकारिक टेलीग्राम चैनल से जुड़कर सभी अपडेट और प्रमाण देख सकते हैं।",

      "qa_prompt": "कृपया अपना प्रश्न टाइप करें। बंद करने के लिए /cancel टाइप करें।"
    },

    "bn": {
      "label": "বাংলা — 🇧🇩",
      "welcome_header": "🌟 Ultra Wisdom-এ স্বাগতম — ডিজিটাল নেতৃত্বের নতুন যুগ! 🇮🇳",
      "bio": "প্রিয় লিডার,\nঅভিনন্দন এবং Ultra Wisdom Success Movement-এ স্বাগতম! 🎉\nআপনি এখন একটি বিশ্বস্ত গ্লোবাল ব্র্যান্ডের অংশ; আমরা Digital India Vision-এর মাধ্যমে প্রত্যেক ভারতীয়কে বাড়তে, উপার্জন করতে এবং সৌন্দর্য, ওয়েলনেস ও উদ্যোগের মাধ্যমে উজ্জ্বল হতে সাহায্য করি।\n\n✨ বিশেষত্ব:\n💎 Trusted Swedish Brand since 2000\n🌿 দৈনন্দিন ব্যবহারের জন্য 1000+ মানসম্মত পণ্য\n📱 100% ডিজিটাল প্ল্যাটফর্ম — যে কোনো স্থান থেকে কাজ করুন\n🚀 উপার্জন করুন, শিখুন এবং আপনার টিমকে নেতৃত্ব দিন\n\n— ⚡ Team Ultra Wisdom | Digital India Mission 2025-2026 🇮🇳",

      "signup": "🎉 স্বাগতম THE ULTRA WISDOM™!\n\nনীচের লিঙ্ক থেকে সাইন আপ করে আপনার যাত্রা শুরু করুন:\nhttps://theultrawisdom.com/referral?get_sponsor=TUW258258\n\n💡 নোট: সাইন আপ সম্পূর্ণ বিনামূল্যে।",

      "login": "🔑 লগইন করুন:\nhttps://theultrawisdom.com/ultra/Dashboard\n\nসাহায্যের প্রয়োজন হলে জানান।",

      "telegram": "📢 অফিসিয়াল টেলিগ্রাম চ্যানেলে যোগ দিন — সর্বশেষ আপডেটের জন্য।",

      "contact": "📞 যোগাযোগ:\n📱 +91-6350638920\n\nঅফিস ঠিকানা:\nSudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",

      "benefits": "⭐ কোম্পানি আয়ের উৎস:\n\n1️⃣ Ad-View Tasks — ক্লায়েন্টরা টাস্ক দেয়, কোম্পানি প্রতি সম্পন্ন টাস্কে কমিশন পায়।\n2️⃣ Referral-আয় — ব্যবহারকারীর রেফারেল অংশীদারিত্ব ও লং-টার্ম ভ্যালু তৈরি করে।\n3️⃣ (আসছে) E-Commerce — প্রোডাক্ট সেল থেকে অতিরিক্ত আয়।\n\n05 ডিসেম্বর থেকে UPI/NetBanking দিয়ে উইথড্রয়াল উপলব্ধ হবে।",

      "working": "🛠 কীভাবে কাজ করবেন:\n\n1. Free Registration — https://theultrawisdom.com/referral?get_sponsor=TUW258258\n2. ₹500 Signup Bonus\n3. প্রতিদিন 4 sponsor ads দেখুন — ₹340/দিন পর্যন্ত\n4. Invite & Earn — ₹540/referral\n5. Telegram Join — ₹400 instant\n6. Team & Rank income তালিকা উপরে দেখুন।",

      "address": "📍 ঠিকানা:\nSudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",

      "withdrawal": "🔔 WITHDRAWAL: Min ₹500 — Max ₹1,00,000 — Start 05 Dec 2025 — Bank / UPI — No Charges",

      "realfake": "🙏 আমরা আপনার উদ্বেগ বুঝি। THE ULTRA WISDOM™ একটি বৈধ এবং বিশ্বাসযোগ্য কোম্পানি। অফিসিয়াল চ্যানেলে যাচাই করুন।",

      "qa_prompt": "আপনার প্রশ্ন টাইপ করুন। বের হতে /cancel টাইপ করুন।"
    },

    "te": {
      "label": "తెలుగు — 🇮🇳",
      "welcome_header": "🌟 Ultra Wisdom కి స్వాగతం — డిజిటల్ నాయకత్వం యొక్క కొత్త యుగం! 🇮🇳",
      "bio": "ప్రియ నాయకుడారా,\nఅభినందనలు! Ultra Wisdom Success Movementలోకి స్వాగతం! 🎉\nమీరు ఇప్పుడు ఒక విశ్వసనీయ గ్లోబల్ బ్రాండ్ భాగస్వామ్యంగా ఉన్నారు.\n\n— ⚡ Team Ultra Wisdom | Digital India Mission 2025-2026 🇮🇳",

      "signup": "🎉 సైన్ అప్:\nhttps://theultrawisdom.com/referral?get_sponsor=TUW258258\n\n💡 సైన్ అప్ ఉచితం.",

      "login": "🔑 లాగిన్:\nhttps://theultrawisdom.com/ultra/Dashboard",

      "telegram": "📢 టెలిగ్రామ్ చానల్ జాయిన్ చేయండి.",

      "contact": "📞 +91-6350638920\nOffice: Sudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",

      "benefits": "1️⃣ Ad-View Tasks\n2️⃣ Referral Income\n3️⃣ (Upcoming) E-Commerce",

      "working": "🛠 ఎలా పని చేయాలి:\n\n1. Free Registration\n2. ₹500 Signup Bonus\n3. రోజూ 4 sponsor ads — ₹340/రోజు వరకు\n4. Referral — ₹540\n5. Telegram Join — ₹400\n6. Team & Rank income వివరాలు పైన ఉన్నాయి.",

      "address": "📍 Sudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",

      "withdrawal": "🔔 Min ₹500 — Max ₹1,00,000 — Start 05 Dec 2025 — Bank/UPI — No Charges",

      "realfake": "🙏 THE ULTRA WISDOM™ ఒక నమ్మకమైన సంస్థ. అధికారిక చానెల్ ద్వారా ధృవీకరించండి.",

      "qa_prompt": "మీ ప్రశ్న రాయండి. /cancel తో బయటకివెళ్ళండి."
    },

    "mr": {
      "label": "मराठी — 🇮🇳",
      "welcome_header": "🌟 Ultra Wisdom मध्ये स्वागत — डिजिटल नेतृत्वाचा नवीन युग! 🇮🇳",
      "bio": "प्रिय लीडर,\nअभिनंदन! Ultra Wisdom Success Movement मध्ये आपले स्वागत आहे! 🎉",

      "signup": "🎉 साइन अप लिंक:\nhttps://theultrawisdom.com/referral?get_sponsor=TUW258258",

      "login": "🔑 Login:\nhttps://theultrawisdom.com/ultra/Dashboard",

      "telegram": "📢 Telegram चॅनेल जोडा.",

      "contact": "📞 +91-6350638920\nOffice: Sudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",

      "benefits": "1️⃣ Ad-View Tasks\n2️⃣ Referral Income\n3️⃣ (लवकरच) E-Commerce",

      "working": "🛠 काम कसे करावे:\n1. Free Registration\n2. ₹500 Signup Bonus\n3. दररोज 4 ads — ₹340/दिवस\n4. Referral — ₹540\n5. Telegram Join — ₹400\n6. Team & Rank income माहिती वर आहे.",

      "address": "📍 Sudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",

      "withdrawal": "🔔 Min ₹500 — Max ₹1,00,000 — 05 Dec 2025 — Bank/UPI — No Charges",

      "realfake": "🙏 Ultra Wisdom एक विश्वासार्ह कंपनी आहे.",

      "qa_prompt": "प्रश्न टाइप करा. /cancel."
    },

    "ta": {
      "label": "தமிழ் — 🇮🇳",
      "welcome_header": "🌟 Ultra Wisdom-க்கு வரவேற்பு — டிஜிட்டல் தலைமையின் புதிய யுகம்! 🇮🇳",
      "bio": "அன்புள்ள தலைவர்,\nவாழ்த்துகள்! Ultra Wisdom Success Movement-இல் வரவேற்கிறோம்! 🎉",

      "signup": "🎉 Sign Up:\nhttps://theultrawisdom.com/referral?get_sponsor=TUW258258",

      "login": "🔑 Login:\nhttps://theultrawisdom.com/ultra/Dashboard",

      "telegram": "📢 Telegram Channel சேரவும்.",

      "contact": "📞 +91-6350638920\nOffice: Sudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",

      "benefits": "1️⃣ Ad-View Tasks\n2️⃣ Referral Income\n3️⃣ (வெளியீடு) E-Commerce",

      "working": "🛠 எப்படி வேலை:\n1. Free Registration\n2. ₹500 Signup Bonus\n3. தினமும் 4 ads — ₹340/நாள்\n4. Referral — ₹540\n5. Telegram Join — ₹400",

      "address": "📍 Sudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",

      "withdrawal": "🔔 Min ₹500 — Max ₹1,00,000 — 05 Dec 2025 — Bank/UPI — No Charges",

      "realfake": "🙏 Ultra Wisdom ஒரு நம்பகமான நிறுவனம்.",

      "qa_prompt": "கேள்வியை தட்டச்சு செய்யவும். /cancel."
    },

    "gu": {
      "label": "ગુજરાતી — 🇮🇳",
      "welcome_header": "🌟 Ultra Wisdom માં આપનું સ્વાગત — ડિજિટલ લીડરશિપનો નવો યુગ! 🇮🇳",
      "bio": "પ્રિય લીડર,\nઅભિનંદન! Ultra Wisdom Success Movement માં આપનું સ્વાગત! 🎉",

      "signup": "🎉 Sign Up:\nhttps://theultrawisdom.com/referral?get_sponsor=TUW258258",

      "login": "🔑 Login:\nhttps://theultrawisdom.com/ultra/Dashboard",

      "telegram": "📢 Telegram Channel જોડાવો.",

      "contact": "📞 +91-6350638920\nOffice: Sudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",

      "benefits": "1️⃣ Ad-View Tasks\n2️⃣ Referral Income\n3️⃣ E-Commerce (શીઘ્ર)",

      "working": "🛠 કેવી રીતે કામ કરવું:\n1. Free Registration\n2. ₹500 Signup Bonus\n3. દરરોજ 4 ads — ₹340/દિવસ\n4. Referral — ₹540\n5. Telegram Join — ₹400",

      "address": "📍 Sudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",

      "withdrawal": "🔔 Min ₹500 — Max ₹1,00,000 — 05 Dec 2025 — Bank/UPI — No Charges",

      "realfake": "🙏 Ultra Wisdom એક વિશ્વસનીય કંપની છે.",

      "qa_prompt": "પ્રશ્ન લખો. /cancel."
    },

    "kn": {
      "label": "ಕನ್ನಡ — 🇮🇳",
      "welcome_header": "🌟 Ultra Wisdom ಗೆ ಸ್ವಾಗತ — ಡಿಜಿಟಲ್ ನಾಯಕತ್ವದ ಹೊಸ ಯುಗ! 🇮🇳",
      "bio": "ಪ್ರಿಯ ನಾಯಕ,\nಅಭಿನಂದನೆಗಳು! Ultra Wisdom Success Movement ಗೆ ಸ್ವಾಗತ! 🎉",

      "signup": "🎉 Sign Up:\nhttps://theultrawisdom.com/referral?get_sponsor=TUW258258",

      "login": "🔑 Login:\nhttps://theultrawisdom.com/ultra/Dashboard",

      "telegram": "📢 Telegram Channel ಸೇರಿ.",

      "contact": "📞 +91-6350638920\nOffice: Sudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",

      "benefits": "1️⃣ Ad-View Tasks\n2️⃣ Referral Income\n3️⃣ E-Commerce (coming)",

      "working": "🛠 ಹೇಗೆ ಕೆಲಸ ಮಾಡುವುದು:\n1. Free Registration\n2. ₹500 Signup Bonus\n3. ಪ್ರತಿ ದಿನ 4 ads — ₹340/ದಿನ\n4. Referral — ₹540\n5. Telegram Join — ₹400",

      "address": "📍 Sudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",

      "withdrawal": "🔔 Min ₹500 — Max ₹1,00,000 — 05 Dec 2025 — Bank/UPI — No Charges",

      "realfake": "🙏 Ultra Wisdom ಒಂದು ನಂಬಲರ್ಹ ಸಂಸ್ಥೆ.",

      "qa_prompt": "ಪ್ರಶ್ನೆ ಟೈಪ್ ಮಾಡಿ. /cancel."
    },

    "ml": {
      "label": "മലയാളം — 🇮🇳",
      "welcome_header": "🌟 Ultra Wisdom-ലേക്ക് സ്വാഗതം — ഡിജിറ്റൽ നേതൃത്ത്വത്തിന്റെ പുതിയ കാലം! 🇮🇳",
      "bio": "പ്രിയ നേതാവേ,\nസ്വാഗതം! Ultra Wisdom Success Movement-ൽ ചേരുന്നതിന് അഭിനന്ദനങ്ങൾ! 🎉",

      "signup": "🎉 Sign Up:\nhttps://theultrawisdom.com/referral?get_sponsor=TUW258258",
      "login": "🔑 Login:\nhttps://theultrawisdom.com/ultra/Dashboard",
      "telegram": "📢 Telegram Channel ചേരുക.",
      "contact": "📞 +91-6350638920\nOffice: Sudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",
      "benefits": "1️⃣ Ad-View Tasks\n2️⃣ Referral Income\n3️⃣ E-Commerce (coming)",
      "working": "🛠 Work steps: Free Registration → ₹500 Signup → 4 ads/day → Referral ₹540 → Telegram ₹400",
      "address": "📍 Sudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",
      "withdrawal": "🔔 Min ₹500 — Max ₹1,00,000 — 05 Dec 2025 — Bank/UPI — No Charges",
      "realfake": "🙏 Ultra Wisdom ഒരു വിശ്വസനീയ കമ്പനിയാണ്.",
      "qa_prompt": "ചോദ്യമിടൂ. /cancel."
    },

    "pa": {
      "label": "ਪੰਜਾਬੀ — 🇮🇳",
      "welcome_header": "🌟 Ultra Wisdom ਵਿੱਚ ਤੁਹਾਡਾ ਸਵਾਗਤ — ਡਿਜੀਟਲ ਲੀਡਰਸ਼ਿਪ ਦਾ ਨਵਾਂ ਯੁੱਗ! 🇮🇳",
      "bio": "ਪਿਆਰੇ ਲੀਡਰ,\nਤੁਹਾਨੂੰ ਸਵਾਗਤ ਅਤੇ ਸ਼ੁਭਕਾਮਨਾਵਾਂ! 🎉",

      "signup": "🎉 Sign Up:\nhttps://theultrawisdom.com/referral?get_sponsor=TUW258258",
      "login": "🔑 Login:\nhttps://theultrawisdom.com/ultra/Dashboard",
      "telegram": "📢 Telegram Channel ਜੁੜੋ.",
      "contact": "📞 +91-6350638920\nOffice: Sudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",
      "benefits": "1️⃣ Ad-View Tasks\n2️⃣ Referral Income\n3️⃣ E-Commerce (coming)",
      "working": "🛠 Steps: Register → ₹500 Signup → 4 ads/day → Referral ₹540 → Telegram ₹400",
      "address": "📍 Sudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",
      "withdrawal": "🔔 Min ₹500 — Max ₹1,00,000 — 05 Dec 2025 — Bank/UPI — No Charges",
      "realfake": "🙏 Ultra Wisdom ਇਕ ਭਰੋਸੇਯੋਗ ਕੰਪਨੀ ਹੈ.",
      "qa_prompt": "ਸਵਾਲ ਲਿਖੋ. /cancel."
    },

    "or": {
      "label": "ଓଡ଼ିଆ — 🇮🇳",
      "welcome_header": "🌟 Ultra Wisdom କୁ ସ୍ୱାଗତ — ଡିଜିଟାଲ ନେତୃତ୍ୱର ନୂଆ ଯୁଗ! 🇮🇳",
      "bio": "ପ୍ରିୟ ନେତା,\nଅଭିନନ୍ଦନ! Ultra Wisdom Success Movement କୁ ସ୍ୱାଗତ! 🎉",

      "signup": "🎉 Sign Up:\nhttps://theultrawisdom.com/referral?get_sponsor=TUW258258",
      "login": "🔑 Login:\nhttps://theultrawisdom.com/ultra/Dashboard",
      "telegram": "📢 Telegram Channel ଯୋଗ ଦିଅନ୍ତୁ.",
      "contact": "📞 +91-6350638920\nOffice: Sudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",
      "benefits": "1️⃣ Ad-View Tasks\n2️⃣ Referral Income\n3️⃣ E-Commerce (coming)",
      "working": "🛠 Process: Register → ₹500 Signup → 4 ads/day → Referral ₹540 → Telegram ₹400",
      "address": "📍 Sudha Villa, Behind Government Hospital, Channapatna, Ramanagara District, Karnataka - 562160",
      "withdrawal": "🔔 Min ₹500 — Max ₹1,00,000 — 05 Dec 2025 — Bank/UPI — No Charges",
      "realfake": "🙏 Ultra Wisdom ଏକ ବିଶ୍ୱସନୀୟ କମ୍ପାନୀ।",
      "qa_prompt": "ପ୍ରଶ୍ନ ଲେଖନ୍ତୁ. /cancel."
    }

  }  # end languages
}

BOT_TOKEN: str = ""   # <-- Paste your bot token here (string)
ADMIN_ID: Optional[int] = None  # <-- Your Telegram numeric user id (int)

# =====================================================
# DATABASE, HELPERS, UI CONTROLS AFTER CONFIG
# =====================================================


CHANNEL_LINK = ""  
# TODO: Replace CHANNEL_LINK when you create your Telegram channel


# -------- LANGUAGE LIST --------
LANGUAGES = {code: CONFIG["languages"][code]["label"] for code in CONFIG["languages"]}


# =====================================================
# DATABASE
# =====================================================
DB_PATH = "ultrawisdom.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            lang TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def set_user_lang(uid: int, lang: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users(user_id, lang) VALUES (?, ?) "
        "ON CONFLICT(user_id) DO UPDATE SET lang=?",
        (uid, lang, lang)
    )
    conn.commit()
    conn.close()

def get_user_lang(uid: int) -> str:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT lang FROM users WHERE user_id=?", (uid,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else "en"


# =====================================================
# TEXT HELPERS
# =====================================================
def cfg(lang: str, key: str) -> str:
    try:
        return CONFIG["languages"][lang][key]
    except Exception:
        return CONFIG["languages"]["en"].get(key, "")

def footer(lang: str) -> str:
    return CONFIG.get("footer", {}).get(lang, CONFIG["footer"]["en"])

def add_footer(text: str, lang: str) -> str:
    return text + "\n\n" + footer(lang)


# =====================================================
# KEYBOARDS
# =====================================================
def language_keyboard():
    rows = []
    items = list(LANGUAGES.items())
    for i in range(0, len(items), 2):
        row = []
        for code, label in items[i:i+2]:
            row.append(InlineKeyboardButton(label, callback_data=f"setlang:{code}"))
        rows.append(row)
    return InlineKeyboardMarkup(rows)


def main_menu(lang="en"):
    return ReplyKeyboardMarkup(
        [
            ["Sign Up", "Login"],
            ["Telegram Channel", "Connect Us"],
            ["Company Benefits", "Working"],
            ["Address", "Withdrawal"],
            ["Real Or Fake"]
        ],
        resize_keyboard=True
    )


def wide_button(text, url):
    return InlineKeyboardMarkup([[InlineKeyboardButton(text, url=url)]])


# =====================================================
# START HANDLERS
# =====================================================
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 Please select your language:",
        reply_markup=language_keyboard()
    )


async def language_select_callback(update, context):
    q = update.callback_query
    await q.answer()

    uid = q.from_user.id
    lang = q.data.split(":", 1)[1]
    set_user_lang(uid, lang)

    # PREMIUM MAIN MENU UI (like screenshot)
    ui_text = (
        "✅ Language Selected\n"
        "----------------------------------------\n\n"
        f"✨ Your language has been set to {LANGUAGES.get(lang)}\n\n"
        "----------------------------------------\n\n"
        "🎯 Main Menu\n"
        f"✨ {cfg(lang, 'welcome_header')}\n\n"
        "----------------------------------------\n\n"
        "💬 How can I help you today?\n\n"
        "📌 Select from the buttons below\n"
        "✨ OR type anything you want to know\n\n"
        "----------------------------------------"
    )

    await q.edit_message_text(add_footer(ui_text, lang))
    await q.message.reply_text("👇 Main Menu", reply_markup=main_menu(lang))


# =====================================================
# MESSAGE HANDLER
# =====================================================
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    uid = update.effective_user.id
    lang = get_user_lang(uid)
    text = msg.text.strip().lower()

    # ----------------------------- SIGN UP -----------------------------
    if text == "sign up":
        await msg.reply_text(
            add_footer(cfg(lang, "signup"), lang)
        )
        await msg.reply_text(
            "Join Now:\nhttps://theultrawisdom.com/referral?get_sponsor=TUW258258",
            reply_markup=wide_button("Join Now", "https://theultrawisdom.com/referral?get_sponsor=TUW258258")
        )
        return

    # ----------------------------- LOGIN -----------------------------
    if text == "login":
        await msg.reply_text(
            add_footer(cfg(lang, "login"), lang)
        )
        await msg.reply_text(
            "Login Here:\nhttps://theultrawisdom.com/ultra/Dashboard",
            reply_markup=wide_button("Open Login Page", "https://theultrawisdom.com/ultra/Dashboard")
        )
        return

    # ----------------------------- TELEGRAM CHANNEL -----------------------------
    if text == "telegram channel":
        await msg.reply_text(add_footer(cfg(lang, "telegram"), lang))
        await msg.reply_text(
            "Join Channel:\n" + (CHANNEL_LINK if CHANNEL_LINK else "No channel link added yet."),
            reply_markup=wide_button("Join Channel", CHANNEL_LINK if CHANNEL_LINK else "https://t.me/")
        )
        return

    # ----------------------------- CONNECT US -----------------------------
    if text == "connect us":
        await msg.reply_text(add_footer(cfg(lang, "contact"), lang))
        await msg.reply_text(
            "Call / WhatsApp:\n+916350638920",
            reply_markup=wide_button("Call / WhatsApp", "https://wa.me/916350638920")
        )
        return

    # ----------------------------- COMPANY BENEFITS -----------------------------
    if text == "company benefits":
        await msg.reply_text(add_footer(cfg(lang, "benefits"), lang))
        return

    # ----------------------------- WORKING -----------------------------
    if text == "working":
        await msg.reply_text(add_footer(cfg(lang, "working"), lang))
        await msg.reply_text(
            "Join:\nhttps://theultrawisdom.com/referral?get_sponsor=TUW258258",
            reply_markup=wide_button("Open Website", "https://theultrawisdom.com")
        )
        return

    # ----------------------------- ADDRESS -----------------------------
    if text == "address":
        await msg.reply_text(add_footer(cfg(lang, "address"), lang))
        return

    # ----------------------------- WITHDRAWAL -----------------------------
    if text == "withdrawal":
        await msg.reply_text(add_footer(cfg(lang, "withdrawal"), lang))
        await msg.reply_text(
            "Withdrawal Help Channel:\n" + (CHANNEL_LINK if CHANNEL_LINK else "No channel link added yet."),
            reply_markup=wide_button("Open Channel", CHANNEL_LINK if CHANNEL_LINK else "https://t.me/")
        )
        return

    # ----------------------------- REAL OR FAKE -----------------------------
    if text in ("real or fake", "real or fake?"):
        await msg.reply_text(add_footer(cfg(lang, "realfake"), lang))
        return

    # Default fallback
    await msg.reply_text(add_footer("Please select an option from the menu.", lang))


# =====================================================
# APPLICATION MAIN
# =====================================================
def main():
    if BOT_TOKEN == "" or ADMIN_ID is None:
        print("⚠️ SET BOT_TOKEN and ADMIN_ID FIRST!")
    init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CallbackQueryHandler(language_select_callback, pattern="^setlang:"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("🔥 UltraWisdom Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()

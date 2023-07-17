import json
from leads.models import Post

# Assuming you have the combined JSON object stored in a variable called 'combined_json'
combined_json = [
  {
    "account_name": "Kotak Life",
    "post_content": "At Kotak Life every employee’s well being is our top priority. With this in mind, we conducted a breast cancer screening camp and more than one hundred female employees got examined. Not just that with advanced, non invasive AI based technology that operates on a 'no touch, no see' principle, we ensured it was a comfortable process for everyone. This initiative helped us build a much stronger and healthier #KotakLife family. We urge you to get examined every year and stay sa… See more",
    "keyword": "lifeinsurance"
  },
  {
    "account_name": "ICICI Prudential Life Insurance",
    "post_content": "World’s leading T20 batsman, Suryakumar Yadav has got the field covered with his 360° batting. Similarly, for the challenges of life, ICICI Prudential Life has got you covered with its 360° life insurance plans. Visit - https://bit.ly/3vDopkj Disclaimer - https://bit.ly/3WG4BIR… See more",
    "keyword": "lifeinsurance"
  },
  {
    "account_name": "Life Insurance Agents Success Network",
    "post_content": "When does a life insurance policy not pay out the death benefit? Answer: When the client dies before paying their first premium - even if the policy is delivered. A couple of lessons for agents here. Client had a GAP in coverage - let his old term policy lapse 12 days before taking delivery of the new policy. Always avoid gaps in coverage when possible. Advise clients in WRITING the dangers of having even a short gap in coverage. The carrier is off the hook because th… See more",
    "keyword": "lifeinsurance"
  },
  {
    "account_name": "Mommy Grows Money",
    "post_content": "Protecting your loved ones is the greatest act of love. ❤️ Invest in a life insurance policy today and secure their future. 💼 #FamilyProtection #lifeinsurance #mommygrowsmoney #FWDLifeInsurance #tagteam #FinancialPlanning #family",
    "keyword": "lifeinsurance"
  },
  {
    "account_name": "Kotak Life",
    "post_content": "Stay updated to stay ahead in your tax planning. T&C : https://bit.ly/3YERrN0 #UnionBudget2023 #Budget2023 #TaxPlanning #LifeInsurance #KotakLife",
    "keyword": "lifeinsurance"
  },
  {
    "account_name": "LIC Advisor & Development Officers Kolkata",
    "post_content": "Why #LIC ? #adityalicpoint #insurance #lifeinsurance #lifeinsurancematters #insurancepolicy #insuranceclaim #retirementplan #retirementplanning",
    "keyword": "lifeinsurance"
  },
  {
    "account_name": "Jas Maligro",
    "post_content": "ℹ️ Fact check: Your life insurance benefit activates on day 1 upon approval of the insurance application! 🤓👍 For as low as ₱84-100 savings per day, you can insure yourself and protect all of your priorities! ♥️ ‼️Get a free 𝗜𝗡𝗦𝗨𝗥𝗔𝗩𝗘𝗦𝗧 quote based on your age and your preferred amount of coverage! Click here 👉 https://bit.ly/JasJaguarKnights *𝘐𝘯𝘴𝘶𝘳𝘢𝘷𝘦𝘴𝘵… See more",
    "keyword": "lifeinsurance"
  },
  {
    "account_name": "EFU Life Assurance Ltd",
    "post_content": "Witness the inspiring story of Taj Muhammad Rizvi, General Manager of the Industrial Facilitation Center (IFC), Islamabad, who firmly believes that insurance is an indispensable investment that individuals must undertake to protect their family's future, enabling them to be self-sufficient and self-reliant, amidst life's many challenges. #EFULife #BackupKahaniyaan #Insurance #lifeinsurance",
    "keyword": "lifeinsurance"
  },
  {
    "account_name": "Snupit Business Leads",
    "post_content": "Latest Insurance Broker Leads on Snupit: - Car / Vehicle Insurance (Yakash - Pietermaritzburg). - Review our insurance policy (Stephen - Nelspruit); - Life Insurance, Funeral plan (Refilwe - Potchefstroom).… See more",
    "keyword": "lifeinsurance"
  },
  {
    "account_name": "ICICI Prudential Life Insurance",
    "post_content": "This Father’s Day, ensure that your children’s dreams always stay financially secure. Protect their future with a life insurance plan, today Visit: http://bitly.ws/IJ53 Disclaimer: https://bit.ly/3tpPDcW… See more",
    "keyword": "lifeinsurance"
  },
  {
    "account_name": "Mike Watson - State Farm Insurance Agent",
    "post_content": "Our superpower - Keeping insurance simple for you & your family! 💪✨ Everyone on #TeamMikeWatson keeps your insurance simple by ✅ helping you make smart insurance decisions for your budget ✅ reviewing your coverage and discounts yearly - as your life changes, often your coverage does too. We don't want you under or overinsured.… See more",
    "keyword": "lifeinsurance"
  },
  {
    "account_name": "State Life Insurance Karachi",
    "post_content": "Secure a safe and prosperous future for your family and children by taking action today. Invest in their well-being by prioritizing financial planning, including Life Insurance, savings, and investments. Prepare for tomorrow and ensure their long-term. Don't hesitate any longer! Take action now by reaching out to us through a phone call or WhatsApp at 📞 0333 2167290 or visit and follow us our official Facebook page at 👉https://www.facebook.com/statelife.kashifali135. Our te… See more",
    "keyword": "lifeinsurance"
  },
  {
    "account_name": "Melvin De Las Llagas II",
    "post_content": "Issued Policy in 2 Minutes😊 41 Year Old Client Business Owner 🙌 Thank you for choosing us to protect your future! 🙌 W… See more",
    "keyword": "lifeinsurance"
  },
  {
    "account_name": "PNB MetLife",
    "post_content": "Celebrating the Spirit of Teamwork!🌟🏏 We conducted an exhilarating cricket tournament for our employees in Gurgaon and Delhi. The tournament brought together teams from different departments, fostering a sense of unity and camaraderie among our talented workforce. Delhi Rangers emerged as the champions of the PNB MetLife Cricket Tournament, with COMP-LIONS securing the runner-up position. Congratulations to both teams on their outstanding performances!… See more",
    "keyword": "lifeinsurance"
  },
  {
    "account_name": "Sri Muda Indian Makkal",
    "post_content": "Grab your LIFE INSURANCE from RM150 monthly (based on age) ‼️ Refundable upon maturity 👍💯✅ ✔️ Sum Assured from RM350k ✔️ Coverage up to 600%… See more",
    "keyword": "lifeinsurance"
  },
  {
    "account_name": "PHP Agency",
    "post_content": "🗽 🇺🇸 PHP Campaign 2023 is officially underway! Hold onto your hats, this is going to be the most incredible Big Event you have ever witnessed! We are Saving America🇺🇸 🗽 #phpagency #phpfreedom #phpcampaign2023 #savingamerica #lasvegas #lifeinsurance #lifeinsuranceagents #financialfreedom",
    "keyword": "lifeinsurance"
  },
  {
    "account_name": "Consider Yourself Covered",
    "post_content": "💭 When it comes to planning for the future, age is just a number. Here's why life insurance is an essential consideration for seniors: 1️⃣ **Peace of Mind:** Life insurance can alleviate the worry about leaving financial burdens to loved ones. It's about ensuring your final expenses or debts are covered. 2️⃣ **Legacy:** It's a way to leave an inheritance to your children, grandchildren, or even a cherished cause or charity.… See more",
    "keyword": "lifeinsurance"
  },
  {
    "account_name": "Design Brighter Future",
    "post_content": "𝗔𝗥𝗘 𝗬𝗢𝗨 𝗦𝗧𝗥𝗨𝗚𝗚𝗟𝗜𝗡𝗚 𝗧𝗢 𝗦𝗔𝗩𝗘 𝗠𝗢𝗡𝗘𝗬 ?? 😭 𝗙𝗶𝗻𝗮𝗻𝗰𝗶𝗮𝗹 𝗘𝗱𝘂𝗰𝗮𝘁𝗶𝗼𝗻 is one of the biggest reasons people have difficulty saving or investing money. Many people don't understand how to save or budget their money, which causes them to spend more than they earn. Ignorance can also lead them to make bad financial decisions that can further hurt their ability to save. Here are 3 simple steps to save consistently 🔥 𝗔𝘂𝘁𝗼𝗺𝗮𝘁𝗲 𝘆𝗼𝘂𝗿 𝘀𝗮𝘃𝗶𝗻𝗴𝘀 Set up an automatic … See more",
    "keyword": "lifeinsurance"
  }
]

# Parse the JSON object
posts_data = json.loads(combined_json)

# Iterate over the posts and save them
for post_data in posts_data:
    post = Post(
        account_name=post_data['account_name'],
        post_content=post_data['post_content'],
        keyword=post_data['keyword']
    )
    post.save()
print("done")

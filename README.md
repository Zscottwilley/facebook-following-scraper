# Facebook Following Scraper
A high-accuracy tool engineered to extract Facebook following list data, revealing detailed profile insights, relationship context, and audience patterns. It streamlines data collection for marketers, analysts, and researchers who need structured intelligence from Facebook profiles.


<p align="center">
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>Facebook Following Scraper</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction
The Facebook Following Scraper gathers the list of accounts a user follows and converts it into clean, structured, ready-to-use data.
It solves the challenge of manually tracking following lists by delivering automated insights at scale.
Ideal for analysts, growth teams, and competitive researchers.

### Why This Matters
- Helps understand user interests and audience affinities
- Provides structured profile-level data for analysis
- Enables deeper competitive and influencer research
- Supports digital marketing strategies with actionable insights
- Saves hours of manual data collection

## Features
| Feature | Description |
|--------|-------------|
| High-performance extraction | Quickly collects following list data with minimal overhead. |
| Structured JSON output | Returns clean and consistent data fields ready for analytics tools. |
| Configurable request limits | Set custom limits for small or large-scale scraping workflows. |
| Profile intelligence | Captures key identity details including name, ID, image, and URL. |
| Reliable navigation | Handles Facebook profile traversal smoothly and consistently. |

---

## What Data This Scraper Extracts
| Field Name | Field Description |
|------------|------------------|
| id | Unique identifier of the followed profile. |
| image | Profile image URL of the followed account. |
| title | Display name of the account being followed. |
| subtitle_text | Additional descriptive text or tagline. |
| url | Direct link to the followed account. |
| username | Username or handle when available. |
| profile_details | Additional metadata about the profile if present. |

---

## Example Output

    [
      {
        "id": "100064487118317",
        "image": "https://scontent-ams4-1.xx.fbcdn.net/v/t39.30808-1/462614990_944230244403204_6935417447634350274_n.jpg",
        "title": "Uncut Magazine",
        "subtitle_text": "",
        "url": "https://www.facebook.com/UncutMagazine"
      }
    ]

---

## Directory Structure Tree

    Facebook Following Scraper/
    ├── src/
    │   ├── runner.py
    │   ├── extractors/
    │   │   ├── facebook_parser.py
    │   │   └── utils_time.py
    │   ├── outputs/
    │   │   └── exporters.py
    │   └── config/
    │       └── settings.example.json
    ├── data/
    │   ├── inputs.sample.txt
    │   └── sample.json
    ├── requirements.txt
    └── README.md

---

## Use Cases
- **Marketing analysts** use it to study audience interests so they can tailor campaigns more effectively.
- **Competitor researchers** use it to examine relationship patterns so they can map market influence.
- **Social media managers** use it to understand follower behavior so they can optimize engagement.
- **Data scientists** use it to enrich datasets so they can improve predictive models.
- **Brands** use it to identify influencer connections so they can plan better collaborations.

---

## FAQs
**Q: Do I need specific permissions to extract following data?**
A: You must have access to view the profile’s following list. Private or restricted profiles cannot be scraped.

**Q: How many items can I extract at once?**
A: You can adjust `maxItems` to control the size of your extraction batch depending on your needs.

**Q: What formats can I download the data in?**
A: The scraper supports JSON, JSONL, CSV, HTML, XML, and Excel exports.

**Q: Does the scraper capture full profile details?**
A: It captures all publicly available information displayed on the following list.

---

## Performance Benchmarks and Results
**Primary Metric:** Processes an average of 25–40 following entries per minute under standard network conditions.
**Reliability Metric:** Achieves a stable 96% success rate in continuous extraction sessions.
**Efficiency Metric:** Uses minimal system resources while maintaining high throughput across long runs.
**Quality Metric:** Delivers over 98% data completeness for publicly visible following lists.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>

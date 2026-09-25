"""Shared settings for the Practo Delhi dental lead pipeline."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
DATA = ROOT / "data"
CACHE = ROOT / "cache"
DB_PATH = DATA / "leads.sqlite"
JSONL_PATH = DATA / "leads.jsonl"
MASTER_XLSX = ROOT / "reference" / "HealthGrow_Delhi_Dental_Prospects_Master.xlsx"
OUT_XLSX = REPO / "HealthGrow_Delhi_Dental_Prospects_Batch8.xlsx"

CHROMIUM = "/opt/pw-browsers/chromium"
PRACTO = "https://www.practo.com"
LISTING_URL = PRACTO + "/delhi/clinics/dental-clinics/{locality}"

TARGET_NEW = 300          # stop once this many accepted leads exist
START_NUMBER = 74         # '#' column continues after the master file's 73 rows
PUSH_EVERY = 25           # send the xlsx to the user after this many new accepted leads
DELAY = (2.0, 4.0)        # polite random delay between Practo page loads (seconds)



# Seed localities (Practo URL slugs). The collector also adds any locality
# links it discovers on listing pages, so this does not need to be complete.
LOCALITIES = """
rohini rohini-sector-3 rohini-sector-7 rohini-sector-8 rohini-sector-9 rohini-sector-11 rohini-sector-13
rohini-sector-15 rohini-sector-16 rohini-sector-24 pitampura shalimar-bagh ashok-vihar model-town
mukherjee-nagar gtb-nagar kamla-nagar civil-lines burari adarsh-nagar azadpur wazirpur prashant-vihar
janakpuri vikaspuri uttam-nagar dwarka dwarka-sector-6 dwarka-sector-7 dwarka-sector-10 dwarka-sector-12
dwarka-sector-23 palam najafgarh tilak-nagar rajouri-garden punjabi-bagh paschim-vihar kirti-nagar
moti-nagar patel-nagar karol-bagh rajinder-nagar naraina subhash-nagar hari-nagar nangloi
saket malviya-nagar hauz-khas green-park greater-kailash-1 greater-kailash-2 greater-kailash
lajpat-nagar south-extension-1 south-extension-2 defence-colony east-of-kailash kalkaji
chittaranjan-park nehru-place alaknanda sarita-vihar jasola okhla jamia-nagar vasant-kunj
vasant-vihar munirka safdarjung-enclave sheikh-sarai chhatarpur mehrauli sangam-vihar
kailash-colony panchsheel-park jangpura lodhi-colony connaught-place paharganj chanakyapuri
mayur-vihar-phase-1 mayur-vihar-phase-2 mayur-vihar-phase-3 patparganj ip-extension preet-vihar
laxmi-nagar shakarpur vivek-vihar karkardooma anand-vihar dilshad-garden shahdara krishna-nagar
geeta-colony gandhi-nagar yamuna-vihar mustafabad seelampur vasundhara-enclave kondli
chandni-chowk daryaganj sadar-bazar inderpuri
""".split()

# Brands that are chains (5+ branches) and therefore out of scope.
CHAIN_KEYWORDS = [
    "clove dental", "sabka dentist", "fms dental", "dentzz", "apollo white", "apollo dental",
    "smile dental chain", "partha dental", "dr smilez", "toothsi", "max hospital", "fortis",
    "manipal", "medanta", "blk", "sir ganga ram", "aiims", "hospital", "mydentalplan",
    "dental excellence", "dentique", "coast dental", "care dental chain", "bhatia dental",
]

NON_DELHI = ["gurgaon", "gurugram", "noida", "ghaziabad", "faridabad", "greater noida",
             "sonipat", "bahadurgarh", "indirapuram", "vaishali, ghaziabad"]

HEADERS = [
    "#", "Clinic", "Area", "Lead Dentist & Qualifications", "Phone", "Phone Confidence", "WhatsApp",
    "Email", "Website", "Address", "Branches", "Why Call / Notes", "Check First", "Fit (1-5)",
    "Signal (1-5)", "Reachability (1-5)", "Score", "Rank", "Status", "Channel", "Last Contact",
    "Next Step", "Google Ads Status", "Ads Evidence / Last Shown", "Message Angle",
    "Practo Ads (Sponsored/Prime)", "Practo Ads Evidence", "Practo URL",
]

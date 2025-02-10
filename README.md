# UCSC-Class-Tracker
The UCSC Course Availability Tracker is a web-based application that monitors enrollment in UCSC courses and notifies students when a spot opens up in their desired classes. Students can add courses to their watch list, and the system will automatically check for openings at regular intervals. When a seat becomes available, the system sends a real-time notification via email or text message, ensuring that students can register as soon as possible.

Key Features:
- Automated Course Monitoring: Tracks UCSC course enrollment status in real-time.
- Custom Watch List: Students can add and manage courses they want to enroll in.
- Instant Notifications: Sends alerts via email or text when a seat opens up.
- User-Friendly Interface: Simple and intuitive dashboard to manage watch-listed courses.
- Integration with UCSC Course System: Ensures accurate and up-to-date enrollment data.

This tool helps students secure spots in high-demand classes by eliminating the need for manual course availability checks.

## How to Use
The script presently doesn't have any interface or database but has a UI and web app interface planner, to use the script before the release of UI, you can follow the steps below:
1. Clone the repository locally
2. create a .env file as given below \
   ```
   AUTH="[Your Twilio Auth Key]"
   PHONE_NUMBER="[Your Phone Number with Whatsapp]"
   SID="[Your Account SID]"
   ```
3. create a python virtual environment and install dependencies using the command below:
   ```bash
   pip install -r requirements.txt
   ```
4. Change the classes, Subject, and term accoring to the parameter details given.
5. Run the script using command below locally
  ```bash
  python main.py
  ```

The script will start running and send you all the updated classes you added to your watch list;

## Parameter Details
### classes
 The Class Code, for example 115a for a class with CSE 115a
### Subject
The Subject code according to the list below:
| Code | Subject |
|---------|------|
|ACEN | Academic English |
|AM | Applied Mathematics |
|ANTH | Anthropology |
|APLX | Applied Linguistics |
|ARBC | Arabic |
|ART | Art |
|ARTG | Art & Design: Games + Playable Media |
|ASTR | Astronomy and Astrophysics |
|BIOC | Biochemistry and Molecular Biology |
|BIOE | Biology Ecology and Evolutionary |
|BIOL | Biology Molecular Cell and Developmental |
|BME | Biomolecular Engineering |
|CHEM | Chemistry and Biochemistry |
|CHIN | Chinese |
|CLNI | College Nine |
|CLST | Classical Studies |
|CMMU | Community Studies |
|CMPM | Computational Media |
|COWL | Cowell College |
|CRES | Critical Race and Ethnic Studies |
|CRSN | Carson College |
|CT | Creative Technologies |
|CRWN | Crown College |
|CSE | Computer Science and Engineering |
|CSP | Coastal Science and Policy |
|DANM | Digital Arts and New Media |
|EART | Earth Sciences |
|ECE | Electrical and Computer Engineering |
|ECON | Economics |
|EDUC | Education |
|ENVS | Environmental Studies |
|ESCI | Environmental Sciences |
|FIL | Filipino |
|FILM | Film and Digital Media |
|FMST | Feminist Studies |
|FREN | French |
|GAME | Games and Playable Media |
|GCH | Global and Community Health |
|GERM | German |
|GIST | Geographic Info Systems, Science, & Technologies |
|GRAD | Graduate |
|GREE | Greek |
|HAVC | History of Art and Visual Culture |
|HEBR | Hebrew |
|HISC | History of Consciousness |
|HIS | History |
|HCI | Human Computer Interaction |
|HUMN | Humanities |
|ITAL | Italian |
|JAPN | Japanese |
|JRLC | John R Lewis College |
|JWST | Jewish Studies |
|KRSG | Kresge College |
|LAAD | Languages |
|LALS | Latin American and Latino Studies |
|LATN | Latin |
|LGST | Legal Studies |
|LING | Linguistics |
|LIT | Literature |
|MATH | Mathematics |
|MERR | Merrill College |
|METX | Microbiology and Environmental Toxicology |
|MSE | Materials Science and Engineering |
|MUSC | Music |
|NLP | Natural Language Processing |
|OAKS | Oakes College |
|OCEA | Ocean Sciences |
|PBS | Physical Biological Sciences |
|PERS | Persian |
|PHIL | Philosophy |
|PHYE | Physical Education |
|PHYS | Physics |
|POLI | Politics |
|PORT | Portuguese |
|PRTR | Porter College |
|PSYC | Psychology |
|PUNJ | Punjabi |
|RUSS | Russian |
|SCIC | Science Communication |
|SOCD | Social Documentation |
|SOCY | Sociology |
|SPAN | Spanish |
|SPHS | Spanish for Heritage Speakers |
|STAT | Statistics |
|STEV | Stevenson College |
|THEA | Theater Arts |
|TIM | Technology Information Management |
|UCDC | UCDC |
|VAST | Visualizing Abolition Studies |
|WRIT | Writing |
|YIDD | Yiddish |

### Term
The term number for the Winter 2025 quarter is 2250 and the further ones can be determined by adding +1 for every quarter passed.

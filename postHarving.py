from pydantic import BaseModel
from openai import OpenAI
import csv
import json
from pydantic import ValidationError
from typing import List

client = OpenAI()

post='''Description Our software engineers develop next generation technologies that enable the creation of media entertainment that you enjoy at home or on the go. Our software plays a significant role in producing and delivering your favourite sports, shows and movies. Anything you watch on TV or stream online, there's a good chance Evertz software is behind the scenes making it happen. When you join our team, you will immediately begin developing software that ships.  While doing so, you will apply your academic and professional backgrounds to interesting and challenging problems. Your software will be used by skilled media professionals in critical media operations around the world. This is your opportunity to be part of an exciting industry that is undergoing rapid technological advancement.
 
Our employment philosophy is simple. Hire extremely talented people, give them opportunities to make a positive impact and nurture their need for challenge and growth.
Our work philosophy is simple, too. We emphasize teamwork, promote creativity and enjoy being at the leading edge of high-tech in our industry. We offer excellent compensation and generous benefits along with a team of intelligent professionals that will help you succeed.
 
Your work will mainly involve developing solutions for tailored customer applications, use-cases, and systems.
 
Required Skills:
C/C
Git
Gcc/make
Linux environment
Scripting (sh, bash, python)
Multithreading
Networking (sockets, TCP/UDP/RTP, multicast/unicast)
Shared memory
Recommended Skills:
Image properties (fourcc, colour space, HDR/SDR)
Video codecs (H.264, H.265, JPEG2000, JPEG-XS, DnXHD, ProRes)
Media containers (MPEG-TS, mov, mxf)
Broadcast production (SDI, SMPTE ST2110, timecode, NLE)
Time systems and time distribution (UTC/TAI, IEEE1588, SMPTE ST2059, leap seconds)
Network streaming (SRT, RIST)
Processing acceleration (SIMD/SSE/AVX, CUDA, OpenCL)
Optional Skills:
Linux kernel knowledge (drivers, networking, filesystems, memory management, tracing)
FFmpeg
Matrox DSX SDK
NewTek NDI SDK
Linux packaging/distribution (dpkg-deb, debootstrap, pbuilder, rootfs
What we Offer:

Employer funded benefits program 
Competitive total compensation package
Work-Life Balance
Employee assistance plan
Employee Discount Platform 
Career Progression 
Casual Work Environment 
Social Events and Sports Teams
Onsite Counsellor 
About Us:

Evertz Microsystems (TSX:ET) is a leading global manufacturer of broadcast equipment and solutions that deliver content to television sets, on-demand services, WebTV, IPTV, and mobile devices (like phones and tablets). Evertz has expertise in delivering complete end-to-end broadcast solutions for all aspects of broadcast production including content creation, content distribution and content delivery.

Considered as an innovator by their customers, Evertz delivers cutting edge solutions that are unmatched in the industry in both hardware and software. Evertz delivers products and solutions that can be found in major broadcast facilities on every continent. Evertz’ customer base also includes telcos, satellite, cable TV, and IPTV providers.

With over 2,000 employees, that include hardware and software engineers, Evertz is one of the leaders in the broadcast industry. Evertz has a global presence with offices located in: Canada, United States, United Kingdom, Germany, United Arab Emirates, India, Hong Kong, China, Singapore, and Australia. Evertz was named one of Canada’s 50 Best Managed Companies, which recognizes excellence in Canadian-owned and Canadian-managed companies. Canada’s 50 Best Managed Companies identifies Canadian corporate success through companies focused on their core vision, creating stakeholder value and excelling in the global economy.

Evertz makes certain there is an equal employment opportunity for all employees and applicants for employment, including persons with disabilities. In compliance with AODA, Evertz will strive to provide accommodation to persons with disabilities in the recruitment process upon request. If you are selected for an interview and you require accommodation due to a disability during the recruitment process, please notify Human Resources upon scheduling your interview.

Thank you for considering a career with Evertz!

When you apply to a job on this site, the personal data contained in your application will be collected by Evertz Microsystems Ltd (“Controller”), which is located at 5292 John Lucas Drive, Burlington, Ontario, Canada and can be contacted by emailing privacy@evertz.com. Controller’s data protection officer is Nadiera Toolsieram, who can be contacted at privacy@evertz.com. Your personal data will be processed for the purposes of managing Controller’s and its' subsidiaries' and affiliates' recruitment related activities, which include setting up and conducting interviews and tests for applicants, evaluating and assessing the results thereto, and as is otherwise needed in the recruitment and hiring processes. Such processing is legally permissible under Art. 6(1)(f) of Regulation (EU) 2016/679 (General Data Protection Regulation) as necessary for the purposes of the legitimate interests pursued by the Controller, which are the solicitation, evaluation, and selection of applicants for employment.

A complete privacy policy can be found at https://evertz.com/contact/privacy/

Your personal data will be retained by Controller as long as Controller determines it is necessary to evaluate your application for employment. Under the GDPR, you have the right to request access to your personal data, to request that your personal data be rectified or erased, and to request that processing of your personal data be restricted. You also have to right to data portability. In addition, you may lodge a complaint with an EU supervisory authority.

Powered by JazzHR '''


class CalendarEvent(BaseModel):
    company: str
    elaptime: str
    location: str
    job: str
    company_vision: str
    qualification: List[str]
    responsabilities: List[str]

# ... (Your code to get the 'post' content)

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",  # Or your chosen model
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "user", "content": post},
    ],
    response_format=CalendarEvent,
)

event = completion.choices[0].message.parsed

event = completion.choices[0].message.parsed

filename = 'job_data.csv'

# Deduce columns and prepare data
columns = event.__fields__.keys() # More robust way to get fields
row = []
for col in columns:
    value = getattr(event, col)  # Access attribute dynamically
    if isinstance(value, list):
        row.append(', '.join(value))
    else:
        row.append(value)


# Writing to csv file
with open(filename, mode='w', newline='', encoding='utf-8') as file:  # Added encoding
    writer = csv.writer(file)
    # Writing the header
    writer.writerow(columns)
    # Writing the data
    writer.writerow(row)

print(f"Data has been written to {filename}")



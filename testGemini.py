from google import genai

client = genai.Client(api_key="AIzaSyA3aikIB-WfqxjEWxC1bMUcOiqirRTkX24")

# response = client.models.generate_content(
#     model="gemini-2.5-pro-exp-03-25",
#     contents='''Research and summarize the different research centers at UC Berkeley that focus on Artificial Intelligence (AI). For each center, provide:

# The center’s name
# A brief description of its mission or focus
# Key areas of AI research (e.g., machine learning, robotics, NLP, computer vision)
# Notable faculty members or leaders
# Any major projects, labs, or collaborations associated with it
# A link to their official webpage if available.
# Focus on accuracy and thoroughness, but keep each center’s summary concise and organized.
# Return this in HTML format. Don't include any CSS styling. Don't include the body and html tags.''',
# )

response = client.models.generate_content(
    model="gemini-2.5-pro-exp-03-25",
    contents='''Access the following paper: https://openaccess.thecvf.com/content_cvpr_2017/papers/Isola_Image-To-Image_Translation_With_CVPR_2017_paper.pdf
    Then summarize the contents of the paper in bullet point form. Try writing it in a simple form that is easy to understand by someone who hasn't read the research paper.
Return this in HTML format. Don't include any CSS styling. Don't include the body and html tags.''',
)

position_title = "Undergrad Machine Learning Researcher"
lab_name = "BAIR Labs"
past_experiences = '''Independent Research August 2023 - October 2023
Computer Vision Based AI for Control of High Velocity Autonomous Vehicle with Lane Detection Arcadia, California
◦ Wrote research paper using Python, OpenCV, and linear algebra to develop a realtime lane detection
algorithm under the guidance of a graduate student (Tony Smoragiewicz) at Northeastern University.
◦ Designed and 3D-printed a robotic car to test different algorithms with self-trained Tensorflow CNN.'''

response = client.models.generate_content(
    model="gemini-2.5-pro-exp-03-25",
    contents=f'''You are a professional scientific writer specializing in crafting cover letters for research positions.
Your task is to generate a customized, highly personalized cover letter using the following inputs:
Inputs:
Intended Research Position Title: {position_title}
Target Research Lab Name: {lab_name}
Candidate's Past Research Experiences: {past_experiences} (include publications, methods used, major findings, skills developed)
Instructions:
Research the lab ({lab_name}) online. Find their current research focus, recent publications, methodologies, key themes, and overall mission.
Begin the cover letter with a strong, personalized opening expressing specific excitement for the lab’s work, mentioning one or two recent projects or themes.
In the body, highlight how the candidate’s past experiences align with the lab’s current research focus.
Focus on technical skills, methods, or problem-solving approaches that would add immediate value to the lab.
Include 1-2 sentences proposing how the candidate could contribute to the lab’s ongoing or future projects, based on recent lab developments.
Use a professional yet enthusiastic tone that conveys genuine interest and preparedness.
Keep the cover letter concise (roughly 300–400 words) unless otherwise requested.
Format:
Professional business letter format
3–4 paragraphs
Include formal salutation and closing
Constraints:

Avoid generic statements (e.g., "I am passionate about research") unless immediately linked to the lab’s specific mission.
Avoid repeating the resume — instead, synthesize experiences into a story tailored to the lab’s needs.
Make sure at least one recent project or publication from the lab is explicitly mentioned by name.
End with a polite, confident closing expressing eagerness to discuss further.'''
)

print(response.text)
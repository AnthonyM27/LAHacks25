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

print(response.text)
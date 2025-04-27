from bs4 import BeautifulSoup

# Sample HTML input
html_content = """
<div>
  <strong>Berkeley Sensor & Actuator Center (BSAC)</strong>
  <p>Mission/Focus: An industry-funded, university-based research cooperative focused on micro/nanotechnology, particularly Micro-Electro-Mechanical Systems (MEMS). It conducts interdisciplinary research on sensors, actuators, materials, and integrated systems interfacing electronics with the physical, chemical, and biological world.</p>
  <p>Website: <a href="https://bsac.berkeley.edu/">https://bsac.berkeley.edu/</a></p>
</div>

<div>
  <strong>Berkeley Wireless Research Center (BWRC)</strong>
  <p>Mission/Focus: Concentrates on research in integrated circuits, systems, and communication theory specifically for wireless communications and related applications. BWRC emphasizes innovation in low-power, high-performance radio frequency (RF), mixed-signal, and digital circuits and systems.</p>
  <p>Website: <a href="https://bwrc.eecs.berkeley.edu/">https://bwrc.eecs.berkeley.edu/</a></p>
</div>

<div>
  <strong>SRC Center for Research on Intelligent Storage and Processing-in-memory (CRISP)</strong>
  <p>Mission/Focus: Part of the SRC/DARPA Joint University Microelectronics Program (JUMP). CRISP focuses on developing novel hardware solutions, including emerging non-volatile memory technologies and processing-in-memory (PIM) architectures, to enable breakthroughs in data-intensive applications and artificial intelligence.</p>
  <p>Website: <a href="https://crisp.eecs.berkeley.edu/">https://crisp.eecs.berkeley.edu/</a></p>
</div>

<div>
  <strong>Berkeley Device Modeling Center (BSIM Group)</strong>
  <p>Mission/Focus: Develops industry-standard compact models (like BSIM) for semiconductor devices (MOSFETs) used globally in circuit simulation and design. Their research focuses on accurate modeling of advanced transistor physics for nanoscale technologies.</p>
  <p>Website: <a href="https://bsim.berkeley.edu/">https://bsim.berkeley.edu/</a></p>
</div>
"""

# Parse HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all lab divs
labs = []
for div in soup.find_all('div'):
    lab_name = div.find('strong').text.strip()
    mission_focus = div.find_all('p')[0].text.strip().replace("Mission/Focus: ", "")
    website = div.find('a')['href']
    
    # Append the lab details as a dictionary
    labs.append({
        "name": lab_name,
        "mission_focus": mission_focus,
        "website": website
    })

# Print the resulting list of lab dictionaries
for lab in labs:
    print(lab)
    print(lab["name"])

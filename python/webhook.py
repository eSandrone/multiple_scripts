import pymsteams
import sys
myTeamsMessage = pymsteams.connectorcard("https://reply.webhook.office.com/webhookb2/59c3cad9-c5a1-4759-a4f9-9860eac71458@b00367e2-193a-4f48-94de-7245d45c0947/IncomingWebhook/8447494272b54e51b87e7fcaa3f4b961/96114bde-0d35-4577-9a52-4a1fb34fc9eb")
myTeamsMessage.text("Vulnerabilities found in the project's dependencies")
myTeamsMessage.title("SBOM - Vulnerability found")
myTeamsMessage.color("<Hex Color Code>")
myTeamsMessage.addLinkButton("View issue on Jira", "https://google.com")
#myTeamsMessage.send()


#### Adding Sections ####
# create the section
myMessageSection = pymsteams.cardsection()

# Section Title
myMessageSection.title("Vulnerabilities details")

# Activity Elements
#myMessageSection.activityTitle(sys.argv[1])
#myMessageSection.activitySubtitle("Severity level")
myMessageSection.activityImage("http://i.imgur.com/c4jt321l.png")
#myMessageSection.activityText(sys.argv[3])

# Facts are key value pairs displayed in a list.
myMessageSection.addFact("Severity", "2")
myMessageSection.addFact("Description", "Desc")

# Section Text
#myMessageSection.text("Details")

# Section Images
myMessageSection.addImage("http://i.imgur.com/c4jt321l.png", ititle="This Is Fine")

# Add your section to the connector card object before sending
myTeamsMessage.addSection(myMessageSection)

myTeamsMessage.send()

# Check status code
last_status_code = myTeamsMessage.last_http_response.status_code
print(last_status_code) #200
#print(type(myTeamsMessage))
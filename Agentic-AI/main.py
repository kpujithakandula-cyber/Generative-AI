from langchain import messages
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()
model = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite"
)

@tool("send_email")
def send_email(content: str, destination: str):
    """
    This tool will help in sending email with content to the destination.

    Args:
        content (str): The content of the email to be sent.
        destination (str): The email address of the recipient.

    """
    print(f"Sending email to {destination} with content: {content}")
    print("Email sent successfully")
    return f"Email sent successfully to {destination}"


@tool("send_sms")
def send_sms(content: str, destination: str):
    """
    This tool will help in sending sms with content to the destination.

    Args:
        content (str): The content of the sms to be sent.
        destination (str): The number address of the recipient.

    """
    print(f"Sending SMS to {destination} with content: {content}")
    print("SMS sent successfully")
    return f"SMS sent successfully to {destination}"


def test():
    result = model.invoke("What is capital of India?")
    print(result)

def main():
    agent = create_agent(
        model = model,
        tools = [
            send_email, send_sms
        ], 
        system_prompt="You are a helpful assistant with access to tools"
    )
    response = agent.invoke(
        {
            "messages" : 
            [
                {
                    "role":"user", 
                    "content": "Send how are you to 9999999999 and hello email to test@gmail.com"
                }
            ]
        }
    )
    for message in response['messages']:
        print(message)
if __name__ == "__main__":
    #test()
    main()
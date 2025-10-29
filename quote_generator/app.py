import os
from dotenv import load_dotenv
from openai import OpenAI
from prompt import prompts  # Import your prompt class


class QuoteGenerator:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.prompts = prompts()  # Initialize the prompt class

    def generate_quote(self, category: str, number: int):
        """Generate multiple inspirational quotes following a given category using their given prompt strictly(using yield)."""

        # Select prompt dynamically based on category
        if category.lower() == "fitness":
            custom_prompt = self.prompts.fitness_prompt()
        elif category.lower() == "career":
            custom_prompt = self.prompts.career_prompt()
        elif category.lower() == "business":
            custom_prompt = self.prompts.business_prompt()
        elif category.lower() == "mindset":
            custom_prompt = self.prompts.mindset_prompt()
        elif category.lower() == "discipline":
            custom_prompt = self.prompts.discipline_prompt()
        else:
            custom_prompt = f"Generate a motivational quote for {category} strictly following those category prompt."

        # ✅ Print the selected custom prompt before generating quotes
        #print(f"\n=== Using Prompt for '{category}' Category ===\n{custom_prompt}\n")

        for _ in range(number):
            prompt = f"""
                {custom_prompt}

                Strict rules:
                - The quote must be in English but in short not too long.
                - The quote must be **inspirational** and strictly related to the {category} category.
                - The quote must follow **strictness** and given **prompt** to the {category} category.
                - Follow this exact JSON format:

                Example output:
                {{
                    "{category}": "quote"
                    "author": "ai-generated"
                }}

                Now, provide one valid quote for the {category} category:
            """

            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful but strict assistant that generates short, motivational quotes with a no-mercy attitude."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=50,
                    temperature=1.0
                    
                )
                yield response.choices[0].message.content.strip()
            except Exception as e:
                yield {"error": str(e)}


# ✅ Test (remove later when turning into API)
if __name__ == "__main__":
    quote_generator = QuoteGenerator()
    category = "career"  # Example: try "career" or "mindset"
    number = 2

    for quote in quote_generator.generate_quote(category, number):
        print(quote)

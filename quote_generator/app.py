# import os
# from dotenv import load_dotenv
# from openai import OpenAI


# class QuoteGenerator:
#     def __init__(self):
#         load_dotenv()
#         api_key = os.getenv("OPENAI_API_KEY")
#         self.client = OpenAI(api_key=api_key)

#     def generate_quote(self, category: str, number: int):
#         """Generate multiple inspirational quotes for a given category (using yield)."""
#         for _ in range(number):
#             prompt = f"""
#                 Generate a motivational quote for {category}.

#                 Strict rules:
#                 - The quote must be **real and verifiable** (from a known person).
#                 - The quote must include a **real author's full name**.
#                 - If the author is unknown, anonymous, or cannot be verified, **do not include that quote** — generate another instead.
#                 - Do **not** write "Unknown" or "Anonymous" as author.
#                 - The quote must be **inspirational** and related to the {category} category.
#                 - Follow this exact JSON format:

#                 Example output:
#                 {{
#                     "{category}": "quote",
#                     "author": "author_name"
#                 }}

#                 Now, provide one valid quote for the {category} category:
#                 """

#             try:
#                 response = self.client.chat.completions.create(
#                     model="gpt-4o",
#                     messages=[
#                         {"role": "system", "content": "You are a helpful assistant that generates inspirational quotes."},
#                         {"role": "user", "content": prompt}
#                     ],
#                     max_tokens=50,
#                     temperature=1.7
#                 )
#                 yield response.choices[0].message.content.strip()
#             except Exception as e:
#                 yield {"error": str(e)}


# # Test (remove later when turning into API)
# if __name__ == "__main__":
#     quote_generator = QuoteGenerator()
#     category = "Fitness"
#     number = 20

#     for quote in quote_generator.generate_quote(category, number):
#         print(quote)



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
        """Generate multiple inspirational quotes for a given category (using yield)."""

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
            custom_prompt = f"Generate a motivational quote for {category}."

        for _ in range(number):
            prompt = f"""
                {custom_prompt}

                Strict rules:
                - The quote must be in English.
                - The quote must be **real and verifiable** (from a known person).
                - The quote is not real write AI GENERATED.
                - The quote must be **inspirational** and related to the {category} category.
                - Follow this exact JSON format:

                Example output:
                {{
                    "{category}": "quote",
                    "author": "author_name"
                }}

                Now, provide one valid quote for the {category} category:
            """

            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that generates inspirational quotes."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=50,
                    temperature=1.7
                )
                yield response.choices[0].message.content.strip()
            except Exception as e:
                yield {"error": str(e)}


# ✅ Test (remove later when turning into API)
if __name__ == "__main__":
    quote_generator = QuoteGenerator()
    category = "discipline"  # Try "Career" as well
    number = 2

    for quote in quote_generator.generate_quote(category, number):
        print(quote)

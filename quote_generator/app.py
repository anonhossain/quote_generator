# import os
# from dotenv import load_dotenv
# from openai import OpenAI
# from prompt import prompts  # Import your prompt class


# class QuoteGenerator:
#     def __init__(self):
#         load_dotenv()
#         api_key = os.getenv("OPENAI_API_KEY")
#         self.client = OpenAI(api_key=api_key)
#         self.prompts = prompts()  # Initialize the prompt class

#     def generate_quote(self, category: str, number: int):
#         """Generate multiple inspirational quotes following a given category using their given prompt strictly(using yield)."""

#         # Select prompt dynamically based on category
#         if category.lower() == "fitness":
#             custom_prompt = self.prompts.fitness_prompt()
#         elif category.lower() == "career":
#             custom_prompt = self.prompts.career_prompt()
#         elif category.lower() == "business":
#             custom_prompt = self.prompts.business_prompt()
#         elif category.lower() == "mindset":
#             custom_prompt = self.prompts.mindset_prompt()
#         elif category.lower() == "discipline":
#             custom_prompt = self.prompts.discipline_prompt()
#         else:
#             custom_prompt = f"Generate a motivational quote for {category} strictly following those category prompt."

#         # ✅ Print the selected custom prompt before generating quotes
#         #print(f"\n=== Using Prompt for '{category}' Category ===\n{custom_prompt}\n")

#         for _ in range(number):
#             prompt = f"""
#                 {custom_prompt}

#                 Strict rules:
#                 - The quote must be in English but in short not too long.
#                 - The quote must be **inspirational** and strictly related to the {category} category.
#                 - The quote must follow **strictness** and given **prompt** to the {category} category.
#                 - Follow this exact JSON format:

#                 Example output:
#                 {{
#                     "{category}": "quote"
#                     "author": "ai-generated"
#                 }}

#                 Now, provide one valid quote for the {category} category:
#             """

#             try:
#                 response = self.client.chat.completions.create(
#                     model="gpt-4o",
#                     messages=[
#                         {"role": "system", "content": "You are a helpful but strict assistant that generates short, motivational quotes with a no-mercy attitude."},
#                         {"role": "user", "content": prompt}
#                     ],
#                     max_tokens=50,
#                     temperature=1.0
                    
#                 )
#                 yield response.choices[0].message.content.strip()
#             except Exception as e:
#                 yield {"error": str(e)}


# # ✅ Test (remove later when turning into API)
# if __name__ == "__main__":
#     quote_generator = QuoteGenerator()
#     category = "career"  # Example: try "career" or "mindset"
#     number = 20

#     for quote in quote_generator.generate_quote(category, number):
#         print(quote)



# import os
# import json
# from dotenv import load_dotenv
# from openai import OpenAI
# from pydantic import BaseModel, Field, ValidationError
# from prompt import prompts  # Import your prompt class


# # ---------- Pydantic Output Model ----------
# class FinalOutput(BaseModel):
#     category: str = Field(..., description="AI Generated Quotation")
#     author: str = Field(..., description="Only write AI-Generated")


# # ---------- Helper Function to Clean JSON ----------
# def clean_json(raw_text: str) -> str:
#     """Clean ```json fenced blocks returned by GPT."""
#     return (
#         raw_text.replace("```json", "")
#                 .replace("```", "")
#                 .strip()
#     )


# class QuoteGenerator:
#     def __init__(self):
#         load_dotenv()
#         api_key = os.getenv("OPENAI_API_KEY")
#         self.client = OpenAI(api_key=api_key)
#         self.prompts = prompts()

#     def generate_quote(self, category: str, number: int):
#         """Generate multiple inspirational quotes following a given category using yield."""

#         # Select prompt dynamically
#         if category.lower() == "fitness":
#             custom_prompt = self.prompts.fitness_prompt()
#         elif category.lower() == "career":
#             custom_prompt = self.prompts.career_prompt()
#         elif category.lower() == "business":
#             custom_prompt = self.prompts.business_prompt()
#         elif category.lower() == "mindset":
#             custom_prompt = self.prompts.mindset_prompt()
#         elif category.lower() == "discipline":
#             custom_prompt = self.prompts.discipline_prompt()
#         else:
#             custom_prompt = (
#                 f"Generate a motivational quote for the category '{category}' "
#                 "strictly following the category prompt."
#             )

#         for _ in range(number):

#             # Main prompt
#             prompt = f"""
#                 {custom_prompt}

#                 Strict rules:
#                 - The quote must be short and in English.
#                 - It must be inspirational and strictly related to the {category} category.
#                 - Must follow strictness and the given prompt for {category}.
#                 - MUST follow EXACT JSON format:

#                 Example:
#                 {{
#                     "{category}": "quote",
#                     "author": "ai-generated"
#                 }}

#                 Now provide one valid JSON output for {category}. Do NOT use backticks.
#             """

#             try:
#                 response = self.client.chat.completions.create(
#                     model="gpt-4o",
#                     messages=[
#                         {"role": "system",
#                          "content": "You generate strict, short, motivational quotes. ALWAYS return raw JSON without markdown fences."},
#                         {"role": "user", "content": prompt}
#                     ],
#                     max_tokens=60,
#                     temperature=1.0
#                 )

#                 raw_text = response.choices[0].message.content.strip()
#                 cleaned = clean_json(raw_text)

#                 # Try parsing clean JSON
#                 try:
#                     json_data = json.loads(cleaned)
#                 except json.JSONDecodeError:
#                     # Try Pydantic fallback
#                     try:
#                         validated = FinalOutput.model_validate_json(cleaned)
#                         yield validated.model_dump()
#                         continue
#                     except ValidationError:
#                         yield {"error": "Invalid JSON output", "raw": cleaned}
#                         continue

#                 # Validate required category key
#                 if category in json_data:
#                     validated = FinalOutput(
#                         category=json_data[category],
#                         author=json_data.get("author", "AI-Generated")
#                     )
#                     yield validated.model_dump()
#                 else:
#                     yield {"error": "Missing category key", "raw": json_data}

#             except Exception as e:
#                 yield {"error": str(e)}


# # -------------- TEST --------------
# if __name__ == "__main__":
#     quote_generator = QuoteGenerator()
#     category = "career"
#     number = 20

#     for quote in quote_generator.generate_quote(category, number):
#         print(quote)



import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field, create_model
from prompt import prompts  # Your prompt class file


# ---------- Helper Function to Clean JSON ----------
def clean_json(raw_text: str) -> str:
    """Remove ```json and ``` fences if present."""
    return raw_text.replace("```json", "").replace("```", "").strip()


class QuoteGenerator:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file")
        self.client = OpenAI(api_key=api_key)
        self.prompts = prompts()

    def generate_quote(self, category: str, number: int = 1):
        """
        Generate motivational quotes.
        Output format: { "category_name": "quote text", "author": "ai-generated" }
        """
        category_lower = category.lower()

        # Select the correct prompt
        if category_lower == "fitness":
            base_prompt = self.prompts.fitness_prompt()
        elif category_lower == "career":
            base_prompt = self.prompts.career_prompt()
        elif category_lower == "business":
            base_prompt = self.prompts.business_prompt()
        elif category_lower == "mindset":
            base_prompt = self.prompts.mindset_prompt()
        elif category_lower == "discipline":
            base_prompt = self.prompts.discipline_prompt()
        else:
            base_prompt = f"Generate a short, powerful, original motivational quote about {category}."

        # Dynamically create Pydantic model with the actual category as the key
        DynamicQuoteModel = create_model(
            "DynamicQuoteModel",
            **{
                category: (str, Field(..., description="The motivational quote")),
                "author": (str, Field("ai-generated", description="Author is always ai-generated"))
            }
        )

        for _ in range(number):
            system_message = "You are a precise quote generator. Always return clean, valid JSON only. No explanations. No markdown."

            user_prompt = f"""
                {base_prompt}

                INSTRUCTIONS:
                - Generate ONE original, short, powerful motivational quote strictly about {category}.
                - Return ONLY valid JSON with exactly these two keys:
                  • "{category}": your quote (as a string)
                  • "author": "ai-generated"
                - Do NOT use markdown fences.
                - Do NOT add any extra text.

                Example of correct output:
                {{
                    "{category}": "Success demands discomfort — embrace it.",
                    "author": "ai-generated"
                }}

                Now generate one quote for {category}:
            """

            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=100,
                    temperature=1.1
                    # top_p=0.9,
                    # frequency_penalty=0.7
                )

                raw_text = response.choices[0].message.content.strip()
                cleaned_text = clean_json(raw_text)

                # Parse JSON
                data = json.loads(cleaned_text)

                # Validate with dynamic Pydantic model
                validated = DynamicQuoteModel.model_validate(data)
                yield validated.model_dump()

            except json.JSONDecodeError as e:
                yield {"error": "Invalid JSON from model", "raw": cleaned_text, "details": str(e)}
            except Exception as e:
                yield {"error": "Unexpected error", "details": str(e), "raw": raw_text if 'raw_text' in locals() else None}


# -------------- TEST RUN --------------
# if __name__ == "__main__":
#     generator = QuoteGenerator()

#     print("Generating 5 CAREER quotes:\n")
#     for quote in generator.generate_quote("career", 5):
#         print(json.dumps(quote, indent=2))

#     print("\nGenerating 3 FITNESS quotes:\n")
#     for quote in generator.generate_quote("fitness", 3):
#         print(json.dumps(quote, indent=2))

# -------------- TEST --------------
if __name__ == "__main__":
    quote_generator = QuoteGenerator()
    category = "career"
    number = 200

    for quote in quote_generator.generate_quote(category, number):
        print(quote)
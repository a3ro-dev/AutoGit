import openai
import keys

openai.api_key = keys.api

class ReadmeGen():
    """
    Readme Generator Using OpenAI API key
    """
    license = "MIT"

    @staticmethod
    def generate_readme(main_file: str) -> str:
        """
        Generate a README.md file for the given file.
     
        Args:
     	    main_file: Path to the main file.
     
        Returns: 
     	    Contents of the README.md.
        """  
        with open(main_file, "r") as f:
            main_file_contents = f.read()

        prompt = f"Generate a README.md (it'll be uploaded to GitHub)(license is {ReadmeGen.license})(please write a detailed one with information regarding how to use the scripts what all packages are used and other information) file for the following Python file named {main_file}:\n\n\n" + main_file_contents + "\n"
        name = str(input("Enter your github username: "))
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You're {name} and you write beautiful readme files with a very detailed documentation and very easy to understand language you also write it in such a way that any non tech savvy person can also understand the documentation"},
                {"role": "user", "content": prompt}
            ],
        )

        assistant_reply = response.choices[0].message.content.strip()
        return assistant_reply

if __name__ == "__main__":
    main_file = input("Enter the name of the file: ")
    readme_contents = ReadmeGen.generate_readme(main_file)

    with open("README.md", "w") as f:
        f.write(readme_contents)

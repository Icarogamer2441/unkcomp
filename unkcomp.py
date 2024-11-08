import google.generativeai as genai
import sys
import platform
import os

def search_config_file():
    if platform.system() == 'Windows':
        arquivo_config = os.path.join(os.path.expanduser('~'), 'api.txt')
    else:
        arquivo_config = os.path.join(os.path.expanduser('~'), 'api.txt')
    if os.path.exists(arquivo_config):
        return arquivo_config
    else:
        return None


config_file = search_config_file()
if config_file is not None:
    with open(config_file, 'r') as f:
        api_key = f.read().replace("\n", "")
else:
    print("create a file api.txt with your api key in your user directory")
    api_key = input("What's your api key? > ")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-pro")

def compileCode(file, output):
    with open(file, "r") as f:
        code = f.read()
    
    outputCcode = model.generate_content("""you can compile a code from an unknown language to the C language. if the main functions don't exist, you can create it, and if the language doesn't have static typing, you can add it. if the language code is in other language, you can translate to english
you compile the code and show the output like this:
                                         
```c
// code here
```

don't say nothing, only send the code like i showed. my code to you compile: ```unknownlang
{}
```""".format(code), generation_config=genai.GenerationConfig(max_output_tokens=500000))
    outputcode = "\n".join(outputCcode.text.split("\n")[1:-1])
    with open(output, "w") as out:
        out.write(outputcode)

argc = len(sys.argv)
argv = sys.argv

if argc > 2:
    compileCode(argv[1], argv[2])
else:
    print("no <input.yourext> and <output.c> file given")
    sys.exit(1)

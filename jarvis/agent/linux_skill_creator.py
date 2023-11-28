from jarvis.action.get_os_version import get_os_version, check_os_version
from jarvis.core.llms import OpenAI

_LINUX_SYSTEM_PROMPT = '''
You are helpful assistant to assist in writing Python tool code for tasks completed on Linux operating systems. Your expertise lies in creating Python classes that perform specific tasks, adhering to a predefined format and structure.
Your goal is to generate Python tool code in the form of a class. The code should be structured to perform a user-specified task on a Linux operating system. The class must be easy to use and understand, with clear instructions and comments.

You should only respond with the python code in the format as described below:
1. Code Structure: Begin with the necessary import statement: from jarvis.action.base_action import BaseAction. Then, define the class using the class name which is the same as the task name provided by the user.
2. Parameter Handling: In the __init__ method, only initialize self._description with a brief description of the class's purpose, detailing what task it accomplishes.
3. Subprocess Integration: If the task involves Linux bash operations, instruct the use of the subprocess library, particularly the run method, to execute these operations. This approach should be encapsulated within the __call__ method of the class.
4. Detailed Comments: Provide comprehensive comments throughout the code. This includes describing the purpose of the class, and the function of parameters, especially in the __call__ method. 
And the code you write should also follow the following criteria:
1.The class must start with from jarvis.action.base_action import BaseAction.
2.The class name should be the same as the user's task name.
3.In the __init__ method, only self._description should be initialized.
4.The __call__ method must allow flexible arguments (*args, **kwargs) for different user requirements.
5.For tasks involving Linux bash commands, use the subprocess library to execute these commands within the Python class.
6.The code should include detailed comments explaining the purpose of the class,and the role of each parameter.
7. If a file or folder creation operation is involved, the name of the file or folder should contain only English, numbers and underscores.
8. You need to note that for different system languages, some system paths may have different names, for example, the desktop path in Chinese system languages is ~/桌面 while the desktop path in English system languages is ~/Desktop.
9. If your code involves file or folder creation operations, be sure to change the current working directory to the parent directory of the file or folder you want to create before performing the file creation operation.
10. If the user does not specifically request it (specify an absolute path), all your file operations should be relative to the user-provided working directory, and all created files should be stored in that directory and its subdirectories as a matter of priority. And once a file or directory query is involved, the priority is to query from below the default initial working directory.
Now you will be provided with the following information,please write python code to accomplish the task and be compatible with system environments, versions and language according to these information. 
'''
_LINUX_USER_PROMPT ='''
User's information is as follows:
System Version: {system_version}
System language: simplified chinese
Working Directory: {working_dir}
Task Name: {task_name}
Task Description: {task_description}
'''
class LinuxSkillCreator():
    """
    LinuxSkillCreator is used to generate new skills in Linux environment and store them in the action_lib.
    """
    def __init__(self, config_path=None) -> None:
        super().__init__()
        self.llm = OpenAI(config_path)
        self.system_version = get_os_version()
        try:
            check_os_version(self.system_version)
        except ValueError as e:
            print(e)
        # self.mac_systom_prompts = 

    def format_message(self, task_name,task_description,working_dir):
        self.sys_prompt = _LINUX_SYSTEM_PROMPT
        self.user_prompt = _LINUX_USER_PROMPT.format(
            system_version=self.system_version,
            task_description=task_description,
            working_dir=working_dir,
            task_name=task_name
        )
        self.message = [
            {"role": "system", "content": self.sys_prompt},
            {"role": "user", "content": self.user_prompt},
        ]
        return self.llm.chat(self.message)
    def extract_python_code(self, response):
        python_code = ""
        if '```python' in response:
            python_code = response.split('```python')[1].split('```')[0]
        elif '```' in python_code:
            python_code = response.split('```')[1].split('```')[0]
        return python_code
        


# skillCreator = LinuxSkillCreator(config_path="../../examples/config.json")
# task = "Please download the audio I have given link from the Internet to the desktop of the system and play it in the system."
# python_code = skillCreator.format_message(task)
# if '```python' in python_code:
#     python_code = python_code.split('```python')[1].split('```')[0]
# elif '```' in python_code:
#     python_code = python_code.split('```')[1].split('```')[0]
# file_name = "my_python_script.py"

# # 打开文件并写入代码字符串
# with open(file_name, "w") as file:
#     file.write(python_code)

# print(f"The Python code has been saved to {file_name}")

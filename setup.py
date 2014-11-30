from setuptools import setup

setup(name="whisperscope",
      version="0.0",
      description="Processing on the unspoken parts of JS files.",
      url="",
      author="Aeva Palecek",
      author_email="aeva.ntsc@gmail.com",
      license="GPLv3",
      packages=["whisperscope"],
      zip_safe=False,
      entry_points = {
        "console_scripts" : [
            "docshound=whisperscope.docstrings:export_to_sphinx",
            ],
        },
      install_requires = [
           "sh",
      ]
)
      

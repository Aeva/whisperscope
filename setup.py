from setuptools import setup

setup(name="whjsper",
      version="0.0",
      description="Processing on the unspoken parts of JS files.",
      url="",
      author="Aeva Palecek",
      author_email="aeva.ntsc@gmail.com",
      license="GPLv3",
      packages=["whjsper"],
      zip_safe=False,
      entry_points = {
        "console_scripts" : [
            "js_autodoc=whjsper.autodoc:autodoc",
            ],
        },
      install_requires = [
           "sh",
      ]
)
      

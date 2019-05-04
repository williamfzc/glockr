from setuptools import setup, find_packages


setup(
    name='glockr',
    version='0.1.4',
    description='Make everything lockable.',
    author='williamfzc',
    author_email='fengzc@vip.qq.com',
    url='https://github.com/williamfzc/glockr',
    python_requires=">=3.6",
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'requests',
        'uvicorn',
        'fire',
    ],
    entry_points={
        "console_scripts": [
            "glockrs = glockr.server:main",
            "glockrc = glockr.client:main",
        ],
    },
)

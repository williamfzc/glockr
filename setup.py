from setuptools import setup, find_packages


setup(
    name='glockr',
    version='0.1.1',
    description='global lockable resources for all',
    author='williamfzc',
    author_email='fengzc@vip.qq.com',
    url='https://github.com/williamfzc/glockr',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'requests',
        'uvicorn',
        'fire',
    ],
    entry_points={
        "console_scripts": [
            "glockr = glockr.client.GClient",
        ],
    },
)

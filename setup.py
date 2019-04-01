from setuptools import setup, find_packages

setup(
    name="key-frame-detector",
    version="1.0.0",
    author="Joel Ibaceta",
    author_email="mail@joelibaceta.com",
    license='MIT',
    description="It is a simple python tool to extract key frame images from a video file",
    long_description="A simple tool to detect and extract key frame images from a video file",
    url="https://github.com/joelibaceta/video-keyframe-extractor",
    project_urls={
        'Source': 'https://github.com/joelibaceta/video-keyframe-extractor',
        'Tracker': 'https://github.com/joelibaceta/video-keyframe-extractor/issues'
    },
    packages=find_packages(),
    include_package_data=True,
    install_requires=['opencv-python', 'numpy', 'peakutils'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='video key-frame terminal opencv extractor',
    entry_points={
        "console_scripts": [
            'key-frames-detector=cli:main'
        ]
    }
)
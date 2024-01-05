# anyDownloader
anyDownloader is a versatile Django application that enables you to download MP4 videos from various platforms, including Twitter, Instagram, YouTube (also in MP3), and TikTok. The application utilizes libraries such as Instaloader, pytube, Beautiful Soup 4 (bs4), and requests to interact with different APIs and scrape the necessary data.

## Prerequisites
- **Python:** Ensure you have Python 3.x installed on your machine.
- **ffmpeg:** Install ffmpeg on your system as it is necessary for video processing.
- **Python Packages:** Install the required packages using the following command:
```bash
pip install django instaloader pytube beautifulsoup4 requests
```
## Configuration
Clone the GitHub repository:

```bash
git clone https://github.com/aymene69/anyDownloader.git
```
Navigate to the project directory:

```bash
cd anyDownloader
```
Apply Django migrations:

```bash
python manage.py migrate
```
Start the development server:

```bash
python manage.py runserver
```
Open your web browser and go to http://localhost:8000/ to use anyDownloader.

## Usage
On the homepage, enter the link of the video you want to download.

Click the "Download" button.

The video will be processed, and a download link will be generated.


## Disclaimer
Make sure to comply with the terms of use of different platforms when using this application. The application is provided for educational and testing purposes, and its use should adhere to the policies of third-party platforms. Developers are not responsible for any misuse of this application.







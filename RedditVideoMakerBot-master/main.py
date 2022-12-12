#!/usr/bin/env python

# Imports
import math
import re
from subprocess import Popen
from os import name

from prawcore import ResponseException

from reddit.subreddit import get_subreddit_threads
from utils.cleanup import cleanup
from utils.console import print_markdown, print_step, print_substep
from utils import settings
from utils.id import id
from utils.version import checkversion

from video_creation.background import (
    download_background,
    chop_background_video,
    get_background_config,
)
from video_creation.final_video import make_final_video
from video_creation.screenshot_downloader import download_screenshots_of_reddit_posts
from video_creation.voices import save_text_to_mp3

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Variables
options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")
options.add_argument("--headless")
options.add_argument("user-data-dir=C:\\Users\\noelm\\AppData\\Local\Google\\Chrome\\User Data\\")
options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
dir_path = 'C:\\Users\\noelm\\Documents\\Youtube Channels\\Instant Reddit\\Video Creation Bot\\RedditVideoMakerBot-master\\results\\AskReddit'
count = 0


for i in range(10):
    try:
        __VERSION__ = "2.4.1"

        print(
            """
        ██████╗ ███████╗██████╗ ██████╗ ██╗████████╗    ██╗   ██╗██╗██████╗ ███████╗ ██████╗     ███╗   ███╗ █████╗ ██╗  ██╗███████╗██████╗
        ██╔══██╗██╔════╝██╔══██╗██╔══██╗██║╚══██╔══╝    ██║   ██║██║██╔══██╗██╔════╝██╔═══██╗    ████╗ ████║██╔══██╗██║ ██╔╝██╔════╝██╔══██╗
        ██████╔╝█████╗  ██║  ██║██║  ██║██║   ██║       ██║   ██║██║██║  ██║█████╗  ██║   ██║    ██╔████╔██║███████║█████╔╝ █████╗  ██████╔╝
        ██╔══██╗██╔══╝  ██║  ██║██║  ██║██║   ██║       ╚██╗ ██╔╝██║██║  ██║██╔══╝  ██║   ██║    ██║╚██╔╝██║██╔══██║██╔═██╗ ██╔══╝  ██╔══██╗
        ██║  ██║███████╗██████╔╝██████╔╝██║   ██║        ╚████╔╝ ██║██████╔╝███████╗╚██████╔╝    ██║ ╚═╝ ██║██║  ██║██║  ██╗███████╗██║  ██║
        ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═════╝ ╚═╝   ╚═╝         ╚═══╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
        """
        )
        # Modified by JasonLovesDoggo
        print_markdown(
            "### Thanks for using this tool! [Feel free to contribute to this project on GitHub!](https://lewismenelaws.com) If you have any questions, feel free to reach out to me on Twitter or submit a GitHub issue. You can find solutions to many common problems in the [Documentation](https://luka-hietala.gitbook.io/documentation-for-the-reddit-bot/)"
        )
        checkversion(__VERSION__)


        def main(POST_ID=None):
            reddit_object = get_subreddit_threads(POST_ID)
            global redditid
            redditid = id(reddit_object)
            length, number_of_comments = save_text_to_mp3(reddit_object)
            length = math.ceil(length)
            download_screenshots_of_reddit_posts(reddit_object, number_of_comments)
            bg_config = get_background_config()
            download_background(bg_config)
            chop_background_video(bg_config, length, reddit_object)
            make_final_video(number_of_comments, length, reddit_object, bg_config)


        def run_many(times):
            for x in range(1, times + 1):
                print_step(
                    f'on the {x}{("th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th")[x % 10]} iteration of {times}'
                )  # correct 1st 2nd 3rd 4th 5th....
                main()
                Popen("cls" if name == "nt" else "clear", shell=True).wait()


        def shutdown():
            print_markdown("## Clearing temp files")
            try:
                redditid
            except NameError:
                print("Exiting...")
                exit()
            else:
                cleanup(redditid)
                print("Exiting...")
                exit()

        if __name__ == "__main__":
            config = settings.check_toml("utils/.config.template.toml", "config.toml")
            config is False and exit()
            try:
                if config["settings"]["times_to_run"]:
                    run_many(config["settings"]["times_to_run"])

                elif len(config["reddit"]["thread"]["post_id"].split("+")) > 1:
                    for index, post_id in enumerate(config["reddit"]["thread"]["post_id"].split("+")):
                        index += 1
                        print_step(
                            f'on the {index}{("st" if index % 10 == 1 else ("nd" if index % 10 == 2 else ("rd" if index % 10 == 3 else "th")))} post of {len(config["reddit"]["thread"]["post_id"].split("+"))}'
                        )
                        main(post_id)
                        Popen("cls" if name == "nt" else "clear", shell=True).wait()
                else:
                    main()
            except KeyboardInterrupt:
                shutdown()
            except ResponseException:
                # error for invalid credentials
                print_markdown("## Invalid credentials")
                print_markdown("Please check your credentials in the config.toml file")

                shutdown()

                # todo error
    except:
        continue

    # Check how many Videos
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1

    print("   ", count, " Videos found in the videos folder, ready to upload...")

    # Upload to YouTube
    for i in range(0, count):
        simp_path = os.listdir(dir_path)[i]
        abs_path = dir_path + '\\' + simp_path

        if len(simp_path) > 74:
            continue

        else:
            # Start Chrome
            bot = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)
            # Go to Website
            bot.get("https://studio.youtube.com")
            time.sleep(3)
            # Click Upload Button
            upload_button = bot.find_element(By.XPATH, '//*[@id="upload-icon"]')
            upload_button.click()
            time.sleep(1)
            # Upload File
            file_input = bot.find_element(By.XPATH, '//*[@id="content"]/input')
            file_input.send_keys(abs_path)
            time.sleep(7)
            # Format Title
            video_name = simp_path
            video_name = video_name[:-4]
            video_name.strip()
            video_name += '?'
            video_name.replace("whats", "what's")
            video_name.replace("youve", "you've")
            video_name.replace("havent", "haven't")
            video_name.replace("Whats", "What's")
            video_name.capitalize()
            # Title
            title_input = bot.find_element(By.XPATH,
                                           '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[1]/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div')
            title_input.send_keys(video_name + ' #AskReddit #RedditStories')
            time.sleep(5)
            # Description
            description_input = bot.find_element(By.XPATH,
                                                 '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[2]/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div')
            description_input.send_keys(
                video_name + '\n\nSubscribe to Instant Reddit for more Reddit Stories.\n#shorts')
            time.sleep(1)
            # Reuse Details
            reuse_details = bot.find_element(By.XPATH, '//*[@id="reuse-details-button"]')
            reuse_details.click()
            time.sleep(2)
            select_video = bot.find_element(By.XPATH,
                                            '//*[@id="dialog"]/div[2]/div/ytcp-video-pick-dialog-contents/div/div/div/ytcp-entity-card[2]')
            select_video.click()
            time.sleep(2)
            uncheck_title = bot.find_element(By.XPATH, '//*[@id="dialog"]/div[2]/div/div[1]/ytcp-checkbox-lit')
            uncheck_title.click()
            time.sleep(2)
            uncheck_description = bot.find_element(By.XPATH, '//*[@id="dialog"]/div[2]/div/div[2]/ytcp-checkbox-lit')
            uncheck_description.click()
            time.sleep(2)
            confirm_reuse = bot.find_element(By.XPATH, '//*[@id="select-button"]')
            confirm_reuse.click()
            time.sleep(2)
            # Skip the Rest
            next_button = bot.find_element(By.XPATH, '//*[@id="next-button"]')
            for i in range(3):
                next_button.click()
                time.sleep(1)

            done_button = bot.find_element(By.XPATH, '//*[@id="done-button"]')
            done_button.click()
            time.sleep(5)
            bot.quit()
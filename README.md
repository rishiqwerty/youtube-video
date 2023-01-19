## Youtube Data Fetch
### Installation and setup:
- Intall Docker in the system. [Download here](https://www.docker.com/products/docker-desktop/)

- Clone this repo
    ```
    git clone https://github.com/rishiqwerty/youtube-video.git
    ```

- Now go to project directory and run this command
    ```
        docker-compose up
    ```

- Now the server will start. Visit http://localhost:8000/

Home page will appear. Here we can sort data by Newest or oldest publishing date
![doc](readme_images\2.png)

In search if we search some phrases, only video's whose title/description matches the pattern will appear in the result. Per page only shows 10 data. We can navigate to different page with next button.
![doc](readme_images\3.png)
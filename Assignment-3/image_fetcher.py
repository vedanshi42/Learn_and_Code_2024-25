class ImageFetcher:
    def __init__(self, blog_name, request_handler):
        self.blog_name = blog_name
        self.request_handler = request_handler

    def fetch_images_from_range(self, starting_range, ending_range):
        for post_number in range(starting_range, ending_range + 1):
            self.process_post_for_images(post_number)

    def process_post_for_images(self, post_number):
        url = self.build_url_for_post(post_number)
        response = self.request_handler.make_request(url, params={'num': 1, 'start': post_number - 1})
        print(f"Fetching post {post_number}")
        self.fetch_post(response, post_number)

    def build_url_for_post(self, post_number):
        return f"https://{self.blog_name}.tumblr.com/api/read/json"

    def fetch_post(self, response, post_number):
        if response:
            data = self.request_handler.parse_response(response.text)
            if data:
                posts = data.get('posts', [])
                self.handle_post_for_images(posts, post_number)

    def handle_post_for_images(self, posts, post_number):
        if not posts:
            print(f"No posts found in post {post_number}.")
            return
        self.extract_and_display_images_from_post(posts[0], post_number)

    def extract_and_display_images_from_post(self, post, post_number):
        if 'photos' not in post:  # Looking for photos key in post (json format)
            self.no_photos_found(post_number)
            return
        photos = post['photos']
        found_image = False
        for photo in photos:
            image_url = self.build_image_url(photo)
            if image_url:
                print(f"Post {post_number}: {image_url}")
                found_image = True
        if not found_image:
            self.no_high_res_images_found(post_number)

    def build_image_url(self, photo, resolution='1280'):
        key = f"photo-url-{resolution}" # Only fetching the highest resolution image i.e. 1280 px
        return photo.get(key)

    def no_photos_found(self, post_number):
        print(f"No photos found in post {post_number}.")

    def no_high_res_images_found(self, post_number):
        print(f"No high resolution (1280px) images found in post {post_number}.")

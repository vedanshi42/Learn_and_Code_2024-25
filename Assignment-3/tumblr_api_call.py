from blog_info_fetcher import BlogInfoFetcher
from image_fetcher import ImageFetcher
from request_handler import RequestHandler


class TumblrAPICall:
    def __init__(self, blog_name):
        self.request_handler = RequestHandler()
        self.blog_info_fetcher = BlogInfoFetcher(blog_name, self.request_handler)
        self.image_fetcher = ImageFetcher(blog_name, self.request_handler)

    def fetch_and_display_blog_info(self):
        self.blog_info_fetcher.fetch_info()
        self.blog_info_fetcher.display_info()

    def fetch_and_display_images(self, start, end):
        self.image_fetcher.fetch_images_from_range(start, end)

    def validate_range(self, post_range):
        try:
            starting_range, ending_range = map(int, post_range.split('-'))
            if starting_range < 1 or ending_range < starting_range:
                raise ValueError("Invalid range values")
            return starting_range, ending_range
        except ValueError as e:
            print(f"Error in range input: {e}")
            return None, None

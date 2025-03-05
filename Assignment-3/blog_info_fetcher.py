class BlogInfoFetcher:
    def __init__(self, blog_name, request_handler):
        self.blog_name = blog_name
        self.request_handler = request_handler
        self.title = None
        self.name = None
        self.description = None
        self.no_of_posts = None

    def fetch_info(self):
        url = f"https://{self.blog_name}.tumblr.com/api/read/json"
        response = self.request_handler.make_request(url, params={'num': 1})  # Fetching only a single post at once to get blog info.
        if response:
            data = self.request_handler.parse_response(response.text)
            if data:
                self.extract_blog_info(data)

    def extract_blog_info(self, data):
        blog_info = data.get('tumblelog', {}) # Getting data of tumblelog key as the format of response has all data inside this key e.g. tumblelog: {blog_data}
        self.title = self.get_info_or_default(blog_info, 'title', 'No Title')
        self.name = self.get_info_or_default(blog_info, 'name', 'No Name')
        self.description = self.get_info_or_default(blog_info, 'description', 'No Description')
        self.no_of_posts = data.get('posts-total', 0)

    def get_info_or_default(self, blog_info, key, default_value):
        return blog_info.get(key, default_value)

    def display_info(self):
        print(f"title: {self.title}")
        print(f"name: {self.name}")
        print(f"description: {self.description}")
        print(f"no of posts: {self.no_of_posts}")

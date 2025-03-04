from tumblr_api_call import TumblrAPICall


def main():
    blog_name = input("Enter the Tumblr blog name: ").strip()
    post_range = input("Enter the range (start-end): ").strip()

    tumblr_api = TumblrAPICall(blog_name)

    start, end = tumblr_api.validate_range(post_range)
    if start is None or end is None:
        return

    tumblr_api.fetch_and_display_blog_info()
    tumblr_api.fetch_and_display_images(start, end)


if __name__ == "__main__":
    main()

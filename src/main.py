from copy_static import copy_static
from generate_pages import generate_pages_recursive

def main():
    try:
        copy_static()
    except FileNotFoundError as err:
        print(err)

    # generate_page('content/index.md', 'template.html', 'public/index.html')
    generate_pages_recursive('content', 'template.html', 'public')

if __name__ == '__main__':
    main()

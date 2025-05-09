import sys
from copy_static import copy_static
from generate_pages import generate_pages_recursive

def main():
    if len(sys.argv) == 2: 
        basepath = sys.argv[1]
    else:
        basepath = "/"

    try:
        copy_static()
    except FileNotFoundError as err:
        print(err)

    # generate_page('content/index.md', 'template.html', 'public/index.html')
    # generate_pages_recursive('content', 'template.html', 'public', basepath)

    # GitHub pages serves sites from the docs directory of your main branch by default
    generate_pages_recursive('content', 'template.html', 'docs', basepath) 

if __name__ == '__main__':
    main()

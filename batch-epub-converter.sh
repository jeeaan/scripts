for book in *.mobi; do echo "Converting $book"; ebook-convert "$book" "$(basename "$book" .mobi).azw3"; done

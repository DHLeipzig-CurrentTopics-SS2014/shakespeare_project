
class BookWithMostWords:
    def url(self):
        return "books_with_most_words"
    
    def name(self):
        # shown in the navigation
        return "Books with Most Words"
    
    def title(self):
        # title for the page
        return "What could this mean?"
    
    def calc(self, parsed_request):
        # your calculations
        return {'x': '[]', 'y':'[]'}
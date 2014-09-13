# this is an example showing you the methods you need to implement.


class ExampleQuestion:
    def url(self):
        return "example"

    def name(self):
        # shown in the navigation
        return "A Question"
    
    def title(self):
        # title for the page
        return "What could this mean?"
    
    def calc(self, parsed_request):
        # your calculations
        return {'x': '[]', 'y':'[]'}
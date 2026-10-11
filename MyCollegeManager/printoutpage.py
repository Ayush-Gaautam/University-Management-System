class my_cust_PDF:
    def __init__(self):
        self.title = ''
        self.headings = []
        self.rows = []

    def content(self, title, headings, rows):
        self.title = title
        self.headings = headings
        self.rows = rows

    def output(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.title + '\n')
            f.write(', '.join(self.headings) + '\n')
            for row in self.rows:
                f.write(', '.join(str(v) for v in row) + '\n')

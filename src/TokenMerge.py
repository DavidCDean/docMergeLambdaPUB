import os.path
from docxtpl import DocxTemplate

class TokenMerge(object):

    def __init__(self, template_path):
        if(os.path.isfile(template_path) == False):
            raise Exception('Error Locating Template File')
        else:
            self.template = DocxTemplate(template_path)
            self.context = {}

    def add_context(self, context_dict):
        for key in context_dict.keys():
            if(key in self.context):
                raise Exception('Duplicate Merge Key Supplied')
            else:
                self.context.update({ key : context_dict[key] })

    def merge(self, output_path):
        self.template.render(self.context)
        self.template.save(output_path)
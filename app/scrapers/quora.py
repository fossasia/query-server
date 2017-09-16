from __future__ import print_function
import os, json, sys
import requests
import re
from bs4 import BeautifulSoup

class Quora:
    """Scrapper class for quora"""
    def __init__(self):
        pass

    def get_page(self,query):
        """ Fetch the quora search results page
        Returns : Results Page
        """
        query_string = '-'.join(query.strip(' ').split(' '))
        response = requests.get('https://www.quora.com/%s' %(query_string))
        return response

    def results_search(self,query):
        """ Search quora for the query and return set of urls
        Returns: list(result) list((dict))
            result = {
                'question' : query,
                'tags' : tags,
            }
                
        """
        result = {}
        result['question'] = query
        response = self.get_page(query)
        
        # only if it is a valid search query
        if response.status_code == 200:
            
            soup = BeautifulSoup(response.text, 'html.parser')

            # getting the tags for the particular question
            tags = [tag.getText() for tag in soup.findAll('a', { 'class' : 'TopicNameLink'})]
            result['tags'] = tags

            # related questions to the asked question
            related_questions = [_.getText().encode('utf-8') \
                for _ in soup.findAll('li', {'class' : "related_question"})]
            result['related_questions'] = related_questions
            
            # no of answers for the particular question
            result['answer_count'] = int(re.findall(r'\d+', ''.join([g.getText() for g \
                in soup.findAll('div', {'class' : 'answer_count' })]))[0])
            answers = []
            
            ans_temp = soup.findAll('div', {'class' : "Answer AnswerBase"})
            ans_bodies = soup.select("div.ExpandedAnswer")
            
            # make sure answers are parsed properly
            try:
                assert(len(ans_temp) == ans_bodies)
                is_proper = True
            except:
                is_proper = False
            
            for ans, body in zip(ans_temp, ans_bodies):
                answer = {}
                answer['author'] = {
                    'name' : ans.findAll('a', {'class' : 'user'})[0].getText(),
                    'description' : ans.findAll('span', { 'class' : \
                        'IdentityNameCredential NameCredential'})[0].getText()[1:].strip(' ')
                }
                answer['links'] = [_.get('href') for _ in ans.findAll('a', {'class' : 'external_link'})]
                answer['images'] = [_.get('src') for _ in ans.findAll('img')]
                
                elements = []
                for ele in body.descendants:
                    try:
                        if 'rendered_qtext' in ele.get('class'):
                            elements.append(ele.getText())
                    except:
                        pass

                answer['content'] = ' '.join(elements)
                try:
                    answer['views'] = ans.findAll('span', {'class' : 'meta_num'})[0].getText()
                except:
                    answer['views'] = 0
                try:
                    answer['upvotes'] = ''.join(re.findall(r'\d+', \
                        ans.findAll('a', id = re.compile(r"_modal_link$"))))
                except:
                    answer['upvotes'] = 0
                answers.append(answer)

            result['answers'] = answers

        else:
            result['error'] = "No macthing search results"

        return [result]


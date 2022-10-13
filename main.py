import sys
from workflow import Workflow, web

def main(wf):
  query = wf.args[0].encode('utf-8')

  url = 'https://ordnet.dk/ws/ddo/livesearch'
  params = {
    'text': query,
    'size': 20
  }
  headers = {
    'Accept': 'application/json'
  }

  response = web.get(url, params, headers)
  response.raise_for_status()
  
  suggestions = response.json()

  is_at_least_one_suggestion_found = len(suggestions) > 0
  if (not is_at_least_one_suggestion_found):
    wf.add_item(title='No suggestion found for "' + query + '"')
    wf.send_feedback()
  
  for suggestion in suggestions:
    wf.add_item(
      title=suggestion,
      subtitle='https://ordnet.dk/ddo/ordbog?query=' + suggestion,
      arg=suggestion,
      valid=True
    )

  wf.send_feedback()

if __name__ == u"__main__":
  wf = Workflow()
  sys.exit(wf.run(main))

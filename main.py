import sys
from workflow import Workflow, web

def main(wf):
  query = sys.argv[1]

  url = 'https://ordnet.dk/ws/ddo/livesearch'
  params = dict(text=query, size=20)
  headers = dict(Accept='application/json')

  r = web.get(url, params, headers)
  r.raise_for_status()
  
  result = r.json()
  
  for suggestion in result:
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

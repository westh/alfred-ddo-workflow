import sys
import json
import urllib
from workflow import Workflow

def get_web_data(url, params=None, headers=None):
  if params:
    encoded_params = urllib.parse.urlencode(params)
    url = f"{url}?{encoded_params}"
  req = urllib.request.Request(url, headers=headers)
  with urllib.request.urlopen(req) as f:
    data = f.read().decode("utf-8")
  return json.loads(data)

def main(wf):
  query = wf.args[0].encode("utf-8")

  url = "https://ordnet.dk/ws/ddo/livesearch"
  params = {"text": query, "size": 20}
  headers = {"Accept": "application/json"}

  suggestions = get_web_data(url, params, headers)

  is_at_least_one_suggestion_found = len(suggestions) > 0
  if not is_at_least_one_suggestion_found:
    wf.add_item(title='No suggestion found for "' + query.decode("utf-8") + '"')
    return wf.send_feedback()

  for suggestion in suggestions:
    wf.add_item(
      title=suggestion,
      subtitle="https://ordnet.dk/ddo/ordbog?query=" + suggestion,
      arg=suggestion,
      valid=True,
    )

  wf.send_feedback()

if __name__ == "__main__":
  wf = Workflow()
  sys.exit(wf.run(main))
